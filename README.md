# 📲 QRUpload — Local Mobile‑to‑PC File Upload via QR Code

QRUpload is a **local, self-hosted file upload tool** that allows users to upload files from a **mobile device to a PC** by scanning a **QR code**.

The application supports both:
- **Python-based execution**, and
- **A standalone Windows `.exe` build** that requires **no Python installation**.

All transfers occur **locally over Wi‑Fi or LAN**, without cloud services, accounts, or Internet access.

---

## ✨ Key Features

- 📱 Mobile → PC file upload (one-way)
- 🔳 QR code–based access with time-limited tokens
- 🌐 Local network only (offline friendly)
- ☁️ No cloud, no login
- 📂 Multiple file upload
- 🔁 Sequential or parallel upload modes
- 📊 Per-file and total progress indicators
- ⚡ Real-time upload speed
- 🧠 Duplicate file detection with overwrite confirmation
- 🧪 Debug mode (open upload page without QR scanning)

---

## 🪟 Windows Executable (.exe) Build

QRUpload can be distributed as a **single portable Windows `.exe`**.

### ✅ Features of the `.exe` version

- No Python or dependency installation required
- Automatically opens the QR page in the browser
- Runs as a **system tray application**
- Continues running in background
- Tray menu options:
  - Open QR upload page
  - Exit application

### Supported Platforms
- Windows 10
- Windows 11

---

## 🏗 Architecture

```
Mobile Browser
│
│  HTTP (Local Network)
▼
PC (Windows)
┌───────────────────────────┐
│ QRUpload (.py / .exe)     │
│  ├─ FastAPI Server        │
│  ├─ QR Generator          │
│  ├─ Upload UI             │
│  ├─ System Tray Controller│
└───────────────────────────┘
│
└── shared/ (Uploaded files)
```

---

## ▶️ Usage

### Python Mode

```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8080
```

Requires Python and dependencies.

---

### Windows .exe Mode

- Download or copy QRUpload.exe
- Double-click to start
- Allow access through Windows Firewall (private network)
- Browser opens automatically
- Scan QR from mobile and upload files

No installation required.
---
## 📂 File Storage
### Uploaded files are stored in:
```
shared/
```

---

## 🔐 Security Model

- Time-limited upload tokens (default: 5 minutes)
- Token validation for all uploads
- Duplicate file overwrite confirmation
- Designed for trusted local environments

---

## 🧰 Technology Stack

- Backend: FastAPI, Uvicorn
- Frontend: HTML, CSS, Vanilla JavaScript
- QR code: qrcode + Pillow
- System Tray: pystray
- Packaging: PyInstaller

---

## ⚠️ Known Limitations

- Upload pause/resume restarts the file
- Large files depend on available RAM and network speed
- Not designed for public Internet exposure

---

## 📄 License
MIT License

---

## ✅ Status
QRUpload is considered stable for local file transfer use cases and serves as a foundation for future enhancements.
