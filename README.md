# WIRE-CLOUD

**A Wireshark-style, web-based network traffic analyzer — runs locally on Windows & Linux.**
**یک تحلیل‌گر ترافیک شبکه‌ی تحت وب، شبیه Wireshark — به‌صورت لوکال روی ویندوز و لینوکس اجرا می‌شود.**

> ⚠️ **Legal & ethical notice / نکته‌ی قانونی و اخلاقی**
> Only capture traffic on networks and devices you own or have explicit permission to monitor. Unauthorized packet sniffing may be illegal in your jurisdiction.
> فقط روی شبکه‌ها و دستگاه‌هایی که مالک آن‌ها هستید یا اجازه‌ی صریح دارید ترافیک ضبط کنید. شنود غیرمجاز پکت‌ها ممکن است در کشور شما غیرقانونی باشد.

---

## 1. Overview / معرفی

**EN —** WIRE-CLOUD is a local, self-hosted packet capture and analysis tool with a dark, professional web dashboard. It shows live traffic in a sortable packet list, a per-packet protocol layer tree, and a hex/ASCII dump — the same mental model as Wireshark, but reachable from any browser on `http://127.0.0.1:5000` with no desktop GUI framework required.

**FA —** WIRE-CLOUD یک ابزار ضبط و تحلیل پکت است که به‌صورت لوکال روی سیستم خودتان اجرا می‌شود و یک داشبورد وب تیره و حرفه‌ای دارد. ترافیک زنده را در یک جدول قابل مرتب‌سازی نمایش می‌دهد، برای هر پکت درخت لایه‌های پروتکل و یک نمایش Hex/ASCII دارد — دقیقاً همان مدل ذهنی Wireshark، اما از طریق هر مرورگری روی آدرس `http://127.0.0.1:5000` قابل دسترسی است، بدون نیاز به فریم‌ورک گرافیکی دسکتاپ.

### Tech stack / پشته‌ی فناوری

| Layer / لایه | Technology / فناوری | Role / نقش |
|---|---|---|
| Capture engine / موتور ضبط | **Python** + Scapy | Cross-platform live sniffing, protocol parsing, pcap export |
| Web backend / بک‌اند وب | **Python** (Flask + Flask-SocketIO) | REST API + real-time WebSocket packet stream |
| Web frontend / فرانت‌اند وب | **HTML5 / CSS3 / JavaScript** | Wireshark-like dashboard, live oscilloscope, hex viewer |
| Reporting module / ماژول گزارش‌گیری | **PHP** | Read-only dashboard listing saved capture sessions (`php/`) |
| High-performance capture (optional) / ضبط پرسرعت (اختیاری) | **C++** + libpcap | Standalone raw-socket sniffer emitting JSON lines (`cpp/`) |

---

## 2. Features / امکانات

- **EN**
  - **Startup capture setup** — a modal asks you to pick the interface and an optional BPF filter (with quick presets: TCP/UDP/Web/DNS/ICMP) right when the app opens, before anything else happens
  - **Light / dark theme toggle** (☀ / ☾ button in the header), remembered between visits
  - Live packet capture over any local interface, with BPF filter syntax (`tcp port 443`, `udp`, `host 8.8.8.8`, …)
  - Real-time packet list pushed over WebSocket, batched every ~120 ms for smooth scrolling even at high packet rates
  - Protocol-coded rows (TCP / UDP / DNS / HTTP / TLS / ICMP / ARP / IPv6) with quick filter chips that show a live per-protocol count
  - New packets briefly flash so you can track live traffic without losing your place
  - **Auto-scroll toggle** — pause auto-scroll to inspect packets without the list jumping around
  - Click any packet → full layer-by-layer detail tree + hex/ASCII dump, resizable panes
  - Live "pulse" throughput graph in the header
  - Display filter box (search by IP, port, or info text) — client-side, instant
  - Export the current capture buffer to a standard `.pcap` file (openable in real Wireshark)
  - "Save session" → persists a `.pcap` + JSON summary that the PHP dashboard can list and let you re-download
  - Optional C++ helper for lower-overhead raw capture (`cpp/raw_capture.cpp`)

- **FA**
  - **تنظیم ضبط در همان ابتدا** — یک پنجره‌ی مودال همان لحظه‌ی باز شدن برنامه از شما می‌خواهد کارت شبکه و در صورت تمایل یک فیلتر BPF انتخاب کنید (همراه با پیش‌تنظیم‌های سریع: TCP/UDP/وب/DNS/ICMP)
  - **سوییچ حالت روشن/تیره** (دکمه‌ی ☀ / ☾ در بالای صفحه) که بین بازدیدها به خاطر سپرده می‌شود
  - ضبط زنده‌ی پکت‌ها روی هر کارت شبکه‌ی لوکال، همراه با فیلترهای BPF (`tcp port 443`، `udp`، `host 8.8.8.8` و ...)
  - نمایش لحظه‌ای پکت‌ها از طریق WebSocket، با دسته‌بندی هر ۱۲۰ میلی‌ثانیه برای اسکرول روان حتی در نرخ بالای پکت
  - رنگ‌بندی ردیف‌ها بر اساس پروتکل (TCP، UDP، DNS، HTTP، TLS، ICMP، ARP، IPv6) همراه با چیپ‌های فیلتر سریع که شمارنده‌ی زنده‌ی هر پروتکل را نشان می‌دهند
  - پکت‌های جدید برای لحظه‌ای چشمک می‌زنند تا بدون گم‌کردن جای خود، ترافیک زنده را دنبال کنید
  - **سوییچ اسکرول خودکار** — برای بررسی پکت‌ها بدون جابه‌جایی مداوم لیست، اسکرول خودکار را متوقف کنید
  - کلیک روی هر پکت → نمایش کامل درخت لایه‌های پروتکل و نمایش Hex/ASCII آن، با پنل‌های قابل تغییر اندازه
  - نمودار زنده‌ی نبض ترافیک در بالای صفحه
  - جعبه‌ی فیلتر نمایش (جست‌وجو بر اساس IP، پورت یا متن اطلاعات) — سمت کلاینت و آنی
  - خروجی گرفتن از بافر جاری به فرمت استاندارد `.pcap` (قابل باز شدن در Wireshark واقعی)
  - "ذخیره‌ی جلسه" → یک فایل `.pcap` و خلاصه‌ی JSON ذخیره می‌کند که داشبورد PHP آن را لیست و قابل دانلود می‌کند
  - ابزار کمکی اختیاری با C++ برای ضبط خام با سربار کمتر (`cpp/raw_capture.cpp`)

---

## 3. Project structure / ساختار پروژه

```
wire-cloud/
├── backend/
│   ├── app.py                # Flask + Socket.IO server (REST + WebSocket API)
│   ├── capture_engine.py     # Scapy-based cross-platform sniffer
│   └── requirements.txt
├── frontend/
│   ├── templates/index.html  # Main dashboard page
│   └── static/
│       ├── css/style.css     # Dark professional theme
│       └── js/app.js         # Live table, filters, hex view, splitters
├── php/
│   ├── index.php             # Session-history reporting dashboard
│   ├── download.php          # Safe .pcap download endpoint
│   └── report.css
├── cpp/
│   ├── raw_capture.cpp       # Optional high-performance libpcap sniffer
│   └── Makefile
├── captures/                 # Saved sessions land here (.pcap + .json)
├── run_linux.sh              # One-command launcher for Linux
├── run_windows.bat           # One-command launcher for Windows
└── README.md
```

---

## 4. Requirements / پیش‌نیازها

**EN**
- Python 3.9+
- **Linux:** `libpcap` (usually pre-installed; if not: `sudo apt install libpcap-dev`) and root privileges to capture.
- **Windows:** [Npcap](https://npcap.com) installed with **"Install Npcap in WinPcap API-compatible Mode"** checked, and Administrator privileges to capture.
- (Optional) PHP 8+ if you want to run the reporting dashboard.
- (Optional) `g++` and libpcap headers if you want to build the C++ helper.

**FA**
- پایتون نسخه‌ی 3.9 یا بالاتر
- **لینوکس:** کتابخانه‌ی `libpcap` (معمولاً از قبل نصب است؛ در غیر این صورت: `sudo apt install libpcap-dev`) و دسترسی root برای ضبط پکت.
- **ویندوز:** نصب [Npcap](https://npcap.com) با تیک‌زدن گزینه‌ی **"Install Npcap in WinPcap API-compatible Mode"** و اجرای برنامه با دسترسی Administrator.
- (اختیاری) PHP نسخه‌ی 8 به بالا در صورت تمایل به اجرای داشبورد گزارش‌گیری.
- (اختیاری) کامپایلر `g++` و هدرهای libpcap در صورت تمایل به کامپایل ابزار کمکی C++.

---

## 5. Installation & run — Linux / نصب و اجرا — لینوکس

**EN**
```bash
# 1. Clone / copy the project, then enter it
cd wire-cloud

# 2. (Recommended) one-command launcher — creates a venv, installs
#    dependencies, and runs the app with sudo automatically:
./run_linux.sh

# --- OR do it manually ---
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
sudo venv/bin/python backend/app.py
```
Then open your browser at **http://127.0.0.1:5000** (it also opens automatically).
Root privileges are required because live packet capture needs raw-socket access.

**FA**
```bash
# ۱. پروژه را کپی/کلون کرده و وارد پوشه‌ی آن شوید
cd wire-cloud

# ۲. (پیشنهادی) اجرای یک‌مرحله‌ای — یک venv می‌سازد، وابستگی‌ها را
#    نصب می‌کند و برنامه را با sudo اجرا می‌کند:
./run_linux.sh

# --- یا به‌صورت دستی ---
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
sudo venv/bin/python backend/app.py
```
سپس مرورگر خود را روی آدرس **http://127.0.0.1:5000** باز کنید (به‌صورت خودکار هم باز می‌شود).
دسترسی root لازم است چون ضبط زنده‌ی پکت به دسترسی raw-socket نیاز دارد.

---

## 6. Installation & run — Windows / نصب و اجرا — ویندوز

**EN**
1. Install [Python 3.9+](https://python.org) and make sure "Add Python to PATH" is checked during setup.
2. Install [Npcap](https://npcap.com) — during setup, check **"Install Npcap in WinPcap API-compatible Mode"**.
3. Right-click `run_windows.bat` → **Run as administrator**.
   The script creates a virtual environment, installs dependencies, and launches the server.
4. Your browser opens automatically at **http://127.0.0.1:5000**.

Manual alternative (in an elevated / Administrator terminal):
```bat
python -m venv venv
venv\Scripts\activate
pip install -r backend\requirements.txt
python backend\app.py
```

**FA**
۱. [پایتون نسخه‌ی 3.9 به بالا](https://python.org) را نصب کنید و در حین نصب گزینه‌ی "Add Python to PATH" را تیک بزنید.
۲. [Npcap](https://npcap.com) را نصب کنید — در حین نصب حتماً گزینه‌ی **"Install Npcap in WinPcap API-compatible Mode"** را تیک بزنید.
۳. روی فایل `run_windows.bat` راست‌کلیک کرده و گزینه‌ی **Run as administrator** را بزنید.
   این اسکریپت به‌طور خودکار محیط مجازی می‌سازد، وابستگی‌ها را نصب کرده و سرور را اجرا می‌کند.
۴. مرورگر شما به‌طور خودکار روی آدرس **http://127.0.0.1:5000** باز می‌شود.

روش دستی (در یک ترمینال با دسترسی Administrator):
```bat
python -m venv venv
venv\Scripts\activate
pip install -r backend\requirements.txt
python backend\app.py
```

---

## 7. Using the dashboard / استفاده از داشبورد

**EN**
1. On first load, a **setup modal** appears — pick a network interface and, optionally, a BPF filter (or use a preset chip like "Web (80/443)" or "DNS"). Click **Start capturing** to jump straight into a live capture, or **Decide later** to just save the choice without starting yet.
2. Packets stream into the table live. Click **STOP** to pause, or the **⚙ settings** button in the header to reopen the setup modal and change interface/filter (capture must be stopped first).
3. Click any row to see its full protocol layer tree and hex/ASCII dump below.
4. Use the **display filter** box or protocol chips (each shows a live count) to narrow what's shown — this only affects the view, not what's captured.
5. Toggle **Auto-scroll** off if you want to inspect older packets without the list jumping to the newest one.
6. Use the **☀ / ☾** button in the header to switch between light and dark themes — your choice is remembered.
7. Use **EXPORT** to download a `.pcap` you can open in real Wireshark, or **SAVE** to archive the session with a JSON summary for the PHP reports dashboard.
8. Use **CLEAR** to empty the in-memory buffer.

**FA**
۱. در اولین بارگذاری صفحه، یک **پنجره‌ی تنظیم اولیه** باز می‌شود — یک کارت شبکه و در صورت تمایل یک فیلتر BPF انتخاب کنید (یا از پیش‌تنظیم‌هایی مثل "وب (80/443)" یا "DNS" استفاده کنید). روی **Start capturing** بزنید تا بلافاصله ضبط زنده شروع شود، یا **Decide later** را بزنید تا فقط انتخاب‌ها ذخیره شود بدون شروع ضبط.
۲. پکت‌ها به‌صورت زنده در جدول نمایش داده می‌شوند. برای توقف روی **STOP** بزنید، یا دکمه‌ی **⚙** در بالای صفحه را بزنید تا پنجره‌ی تنظیمات دوباره باز شود و بتوانید کارت شبکه/فیلتر را تغییر دهید (ابتدا باید ضبط متوقف شود).
۳. روی هر ردیف کلیک کنید تا درخت کامل لایه‌های پروتکل و نمایش Hex/ASCII آن در پایین صفحه دیده شود.
۴. از جعبه‌ی **فیلتر نمایش** یا چیپ‌های پروتکل (هرکدام شمارنده‌ی زنده دارند) برای محدود کردن نمایش استفاده کنید — این فقط روی نمایش تأثیر می‌گذارد نه روی خود ضبط.
۵. در صورت تمایل **Auto-scroll** را خاموش کنید تا بتوانید پکت‌های قدیمی‌تر را بدون پرش مداوم لیست بررسی کنید.
۶. از دکمه‌ی **☀ / ☾** در بالای صفحه برای جابه‌جایی بین حالت روشن و تیره استفاده کنید — انتخاب شما به خاطر سپرده می‌شود.
۷. با **EXPORT** یک فایل `.pcap` دانلود کنید که در Wireshark واقعی هم باز می‌شود، یا با **SAVE** آن را همراه یک خلاصه‌ی JSON برای داشبورد گزارش‌گیری PHP آرشیو کنید.
۸. با **CLEAR** بافر حافظه را خالی کنید.

---

## 8. PHP reporting dashboard (optional) / داشبورد گزارش‌گیری PHP (اختیاری)

**EN** — Sessions saved from the main app (`SAVE SESSION` button) land in `captures/`. To browse them:
```bash
php -S 127.0.0.1:8080 -t php
```
Open **http://127.0.0.1:8080**. This dashboard is read-only and does not itself capture traffic — it only lists and lets you re-download previously saved `.pcap` sessions and their protocol breakdown.

**FA** — جلساتی که از برنامه‌ی اصلی ذخیره می‌شوند (دکمه‌ی `SAVE SESSION`) در پوشه‌ی `captures/` قرار می‌گیرند. برای مشاهده‌ی آن‌ها:
```bash
php -S 127.0.0.1:8080 -t php
```
آدرس **http://127.0.0.1:8080** را باز کنید. این داشبورد فقط خواندنی است و خودش ترافیکی ضبط نمی‌کند — فقط جلسات `.pcap` ذخیره‌شده‌ی قبلی و تفکیک پروتکل‌های آن‌ها را لیست می‌کند و اجازه‌ی دانلود مجدد می‌دهد.

---

## 9. Optional C++ high-performance capture module / ماژول اختیاری ضبط پرسرعت با C++

**EN** — For advanced users who want a lower-overhead capture process outside Python, `cpp/raw_capture.cpp` is a standalone libpcap sniffer that prints one JSON object per packet to stdout. It is **not required** — the default Python/Scapy engine is sufficient for normal use.
```bash
cd cpp
make                      # Linux, requires libpcap-dev + g++
sudo ./raw_capture eth0 "tcp or udp"
```
On Windows, build against the Npcap SDK with MSVC/MinGW (see comments at the top of `raw_capture.cpp`).

**FA** — برای کاربران پیشرفته‌ای که مایل به داشتن یک فرآیند ضبط با سربار کمتر خارج از پایتون هستند، فایل `cpp/raw_capture.cpp` یک ابزار مستقل مبتنی بر libpcap است که برای هر پکت یک شیء JSON در خروجی استاندارد چاپ می‌کند. استفاده از آن **اجباری نیست** — موتور پیش‌فرض پایتون/Scapy برای استفاده‌ی معمول کافی است.
```bash
cd cpp
make                      # لینوکس، نیازمند libpcap-dev و g++
sudo ./raw_capture eth0 "tcp or udp"
```
در ویندوز، با استفاده از Npcap SDK و کامپایلر MSVC یا MinGW آن را بسازید (به توضیحات بالای فایل `raw_capture.cpp` مراجعه کنید).

---

## 10. Troubleshooting / رفع اشکال

| Problem / مشکل | Fix / راه‌حل |
|---|---|
| **EN** "Permission denied" when starting capture | Run with `sudo` (Linux) or as Administrator (Windows). |
| **FA** خطای "Permission denied" هنگام شروع ضبط | برنامه را با `sudo` (لینوکس) یا با دسترسی Administrator (ویندوز) اجرا کنید. |
| **EN** No interfaces listed | Linux: check `ip link`; Windows: confirm Npcap is installed correctly. |
| **FA** هیچ کارت شبکه‌ای نمایش داده نمی‌شود | لینوکس: با `ip link` بررسی کنید؛ ویندوز: از نصب صحیح Npcap مطمئن شوید. |
| **EN** Port 5000 already in use | Edit the last line of `backend/app.py` and change `port=5000`. |
| **FA** پورت ۵۰۰۰ قبلاً استفاده شده | خط آخر فایل `backend/app.py` را ویرایش کرده و `port=5000` را تغییر دهید. |
| **EN** Browser doesn't auto-open | Manually visit `http://127.0.0.1:5000`. |
| **FA** مرورگر به‌صورت خودکار باز نمی‌شود | به‌صورت دستی آدرس `http://127.0.0.1:5000` را باز کنید. |

---

## 11. Roadmap ideas / ایده‌های توسعه‌ی آینده

- **EN:** deeper protocol dissectors (full HTTP/TLS parsing), packet-detail search, multi-user session isolation, saved BPF filter presets, dark/light theme toggle.
- **FA:** تجزیه‌ی عمیق‌تر پروتکل‌ها (پارس کامل HTTP/TLS)، جست‌وجو در جزئیات پکت، جداسازی جلسات چند-کاربره، پیش‌تنظیم‌های فیلتر BPF ذخیره‌شده، سوییچ تم تیره/روشن.

---

## License / مجوز

For personal, educational, and authorized security-testing use. Use responsibly and only on networks you are permitted to monitor.
برای استفاده‌ی شخصی، آموزشی و تست امنیتی مجاز. لطفاً مسئولانه و فقط روی شبکه‌هایی که اجازه‌ی پایش آن‌ها را دارید استفاده کنید.
