import threading
import time
import platform
from collections import deque
from datetime import datetime

from scapy.all import sniff, get_if_list, wrpcap, conf
from scapy.packet import Raw
from scapy.layers.l2 import Ether, ARP
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.inet6 import IPv6
from scapy.layers.dns import DNS

try:
    
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


PROTO_COLORS = {
    "TCP": "tcp", "UDP": "udp", "DNS": "dns", "HTTP": "http",
    "ICMP": "icmp", "ARP": "arp", "TLS": "tls", "IPv6": "ipv6",
    "OTHER": "other",
}


def _friendly_ifaces():
    """Return list of {id, name} for the interface dropdown."""
    ifaces = []
    raw_ifaces = get_if_list()
    pretty = {}
    if HAS_PSUTIL:
        try:
            stats = psutil.net_if_addrs()
            pretty = {k: k for k in stats.keys()}
        except Exception:
            pretty = {}
    for i in raw_ifaces:
        ifaces.append({"id": i, "name": pretty.get(i, i)})
    return ifaces


def _highest_layer_name(pkt):
    if pkt.haslayer(DNS):
        return "DNS"
    if pkt.haslayer(TCP):
        sport, dport = pkt[TCP].sport, pkt[TCP].dport
        if sport in (80, 8080) or dport in (80, 8080):
            return "HTTP"
        if sport == 443 or dport == 443:
            return "TLS"
        return "TCP"
    if pkt.haslayer(UDP):
        return "UDP"
    if pkt.haslayer(ICMP):
        return "ICMP"
    if pkt.haslayer(ARP):
        return "ARP"
    if pkt.haslayer(IPv6):
        return "IPv6"
    if pkt.haslayer(IP):
        return "IP"
    return pkt.lastlayer().name.upper() if pkt.lastlayer() else "OTHER"


def _layer_tree(pkt):
    """Walk scapy layers -> nested list of {layer, fields:[...]}."""
    layers = []
    cur = pkt
    while cur is not None:
        try:
            fields = []
            for fname, fval in cur.fields.items():
                try:
                    fields.append({"name": fname, "value": str(fval)})
                except Exception:
                    continue
            layers.append({"layer": cur.__class__.__name__, "fields": fields})
        except Exception:
            pass
        cur = cur.payload if hasattr(cur, "payload") and cur.payload else None
        if cur is not None and cur.__class__.__name__ == "NoPayload":
            break
    return layers


def _hexdump(raw_bytes):
    lines = []
    for i in range(0, len(raw_bytes), 16):
        chunk = raw_bytes[i:i + 16]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append({
            "offset": f"{i:04x}",
            "hex": hex_part,
            "ascii": ascii_part,
        })
    return lines


class CaptureEngine:
    def __init__(self, buffer_size=8000):
        self.buffer_size = buffer_size
        self.packets = deque(maxlen=buffer_size)
        self.raw_packets = deque(maxlen=buffer_size)  
        self.lock = threading.Lock()
        self._thread = None
        self._stop_flag = threading.Event()
        self._counter = 0
        self._start_time = None
        self.running = False
        self.interface = None
        self.bpf_filter = ""
        self.on_packet = None  
        self.stats = {"total": 0, "bytes": 0, "by_proto": {}}


    def list_interfaces(self):
        return _friendly_ifaces()

    def start(self, interface=None, bpf_filter="", on_packet=None):
        if self.running:
            return False, "Capture already running / ضبط از قبل در حال اجراست"
        self.interface = interface or conf.iface
        self.bpf_filter = bpf_filter or ""
        self.on_packet = on_packet
        self._stop_flag.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._start_time = time.time()
        self.running = True
        self._thread.start()
        return True, "started"

    def stop(self):
        if not self.running:
            return False, "Capture not running / ضبط در حال اجرا نیست"
        self._stop_flag.set()
        self.running = False
        return True, "stopped"

    def clear(self):
        with self.lock:
            self.packets.clear()
            self.raw_packets.clear()
            self._counter = 0
            self.stats = {"total": 0, "bytes": 0, "by_proto": {}}

    def export_pcap(self, path):
        with self.lock:
            pkts = list(self.raw_packets)
        if not pkts:
            return False
        wrpcap(path, pkts)
        return True

    def get_packets(self, offset=0, limit=200, proto=None, search=None):
        with self.lock:
            items = list(self.packets)
        if proto:
            items = [p for p in items if p["protocol"] == proto]
        if search:
            s = search.lower()
            items = [p for p in items if s in p["info"].lower()
                     or s in p["src"].lower() or s in p["dst"].lower()]
        total = len(items)
        return items[offset:offset + limit], total

    def get_packet_detail(self, pkt_id):
        with self.lock:
            raw = None
            for p in self.raw_packets:
                if p.pcap_meta_id == pkt_id:
                    raw = p
                    break
        if raw is None:
            return None
        return {
            "id": pkt_id,
            "layers": _layer_tree(raw),
            "hex": _hexdump(bytes(raw)),
            "summary": raw.summary(),
        }


    def _run(self):
        try:
            sniff(
                iface=self.interface,
                filter=self.bpf_filter or None,
                prn=self._handle_packet,
                store=False,
                stop_filter=lambda p: self._stop_flag.is_set(),
                timeout=1,
            )
            
            while not self._stop_flag.is_set():
                sniff(
                    iface=self.interface,
                    filter=self.bpf_filter or None,
                    prn=self._handle_packet,
                    store=False,
                    stop_filter=lambda p: self._stop_flag.is_set(),
                    timeout=1,
                )
        except PermissionError:
            self.running = False
            if self.on_packet:
                self.on_packet({"error": "permission",
                                 "message": "Run as root/Administrator to capture packets."})
        except Exception as e:
            self.running = False
            if self.on_packet:
                self.on_packet({"error": "capture", "message": str(e)})

    def _handle_packet(self, pkt):
        try:
            setattr(pkt, "pcap_meta_id", None)
            with self.lock:
                self._counter += 1
                pid = self._counter
                pkt.pcap_meta_id = pid

            proto = _highest_layer_name(pkt)
            length = len(pkt)

            src = dst = ""
            sport = dport = None
            if pkt.haslayer(IP):
                src, dst = pkt[IP].src, pkt[IP].dst
            elif pkt.haslayer(IPv6):
                src, dst = pkt[IPv6].src, pkt[IPv6].dst
            elif pkt.haslayer(ARP):
                src, dst = pkt[ARP].psrc, pkt[ARP].pdst
            elif pkt.haslayer(Ether):
                src, dst = pkt[Ether].src, pkt[Ether].dst

            if pkt.haslayer(TCP):
                sport, dport = pkt[TCP].sport, pkt[TCP].dport
            elif pkt.haslayer(UDP):
                sport, dport = pkt[UDP].sport, pkt[UDP].dport

            info = pkt.summary()

            entry = {
                "id": pid,
                "time": round(time.time() - self._start_time, 6) if self._start_time else 0,
                "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
                "src": src,
                "dst": dst,
                "sport": sport,
                "dport": dport,
                "protocol": proto,
                "css_class": PROTO_COLORS.get(proto, "other"),
                "length": length,
                "info": info,
            }

            with self.lock:
                self.packets.append(entry)
                self.raw_packets.append(pkt)
                self.stats["total"] += 1
                self.stats["bytes"] += length
                self.stats["by_proto"][proto] = self.stats["by_proto"].get(proto, 0) + 1

            if self.on_packet:
                self.on_packet(entry)
        except Exception:
           
            pass


def platform_hint():
    return {
        "system": platform.system(),
        "needs_admin": platform.system() == "Windows",
        "needs_root": platform.system() != "Windows",
    }
