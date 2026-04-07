# Changelog

All notable changes to this project will be documented in this file.

The format is based on **Keep a Changelog**, and this project follows **Semantic Versioning**.

---

## [1.1.0] - 2026-04-07

### Added
- Windows standalone `.exe` build using PyInstaller
- No Python or dependency installation required on target PCs
- Automatic browser launch on application start
- System tray icon:
  - Run server in background
  - Open QR page from tray
  - Exit application cleanly
- Resource-safe loading for bundled assets (icons, shared folder)

### Packaging
- Single-file executable (`--onefile`)
- Bundled FastAPI, Uvicorn, QR, and tray dependencies
- Compatible with Windows 10 and Windows 11

---

## [1.0.0] - 2026-04-07

### Added
- Local mobile → PC file upload via QR code
- FastAPI backend with upload endpoints
- Web-based, mobile-friendly upload UI
- Time-limited QR token security
- Multiple file upload support
- Sequential and parallel upload modes
- Per-file and total progress indicators
- Real-time upload speed display
- Duplicate file detection with overwrite confirmation
- Debug mode to open upload page without QR scanning

### Security
- Token validation on all upload requests
- Local network–only design

### Notes
- Python runtime required
- Not packaged as executable in this version

---

## [Unreleased]

### Planned
- Chunked uploads with true resume
- Start / Stop server from tray menu
- Port configuration from UI or tray
- Auto-start with Windows
- MSI installer
- Code-signed executable