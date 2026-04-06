# 📲 Local Mobile‑to‑PC File Upload via QR Code

A **local, self‑hosted file upload system** that allows you to upload files from a **mobile device to a PC** by scanning a **QR code**, without using cloud services, accounts, or the Internet.

All transfers happen **directly over the local network (Wi‑Fi / LAN)**, ensuring **privacy, speed, and full control**.

---

## ✨ Features

- ✅ **Upload files from mobile → PC only** (one‑way)
- ✅ **QR‑code based access**
- ✅ **Local network only** (no Internet required)
- ✅ **No cloud, no login, no account**
- ✅ **Multiple file upload**
- ✅ **Sequential or parallel upload modes**
- ✅ **Per‑file progress bar**
- ✅ **Total upload progress**
- ✅ **Real‑time upload speed display**
- ✅ **Duplicate file detection**
  - Prompt user before overwriting existing files
- ✅ **Debug mode**
  - Button to open upload page directly with active token
- ✅ **Mobile‑friendly UI**
- ✅ **Lightweight & easy to run**

---

## 🏗 Architecture Overview
- **PC** runs a FastAPI server
- Server generates a **temporary upload token**
- QR code embeds the upload URL + token
- **Mobile browser** scans QR and uploads files
- Files are saved directly on the PC

```
Mobile Browser
      │
      │  HTTP (Local Network)
      ↓
PC (FastAPI Server)
      │
      └── Local File System
```

---

## 🔐 Security Model

- Each QR code contains a **temporary token**
- Tokens expire automatically (default: 5 minutes)
- Upload requests without a valid token are rejected
- Duplicate file uploads require **explicit confirmation**
- Server is accessible only on the local network

> ⚠️ This project is designed for **local/private networks**, not public Internet exposure.

---

## 📂 Project Structure

```
 mobile_to_pc_share/
│
├── server.py
├── shared/
└── templates/
    └── upload.html
```


---

## 🧰 Requirements

- Python **3.8+**
- Desktop / Laptop running Windows, macOS, or Linux
- Mobile device with a modern browser (Chrome, Safari, Firefox)

---

## 📦 Installation

### 1️⃣ Clone or copy the project

```bash
git clone https://github.com/trido276/selfhost-files-transfer-mobile-pc
cd selfhost-files-transfer-mobile-pc
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn qrcode[pil] pillow python-multipart
python -m uvicorn server:app --host 0.0.0.0 --port 8080
```

### Scan QR → upload from phone → file appears in:
```
shared/
```


