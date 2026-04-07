# run_app.py
import threading
import time
import webbrowser
import uvicorn
import server
import sys
import os

from pystray import Icon, MenuItem, Menu
from PIL import Image


SERVER_URL = "http://localhost:8080"


def open_browser():
    time.sleep(1.5)
    webbrowser.open(SERVER_URL)


def start_server():
    uvicorn.run(
        server.app,
        host="0.0.0.0",
        port=8080,
        reload=False,
        log_level="info"
    )


def on_open(icon, item):
    webbrowser.open(SERVER_URL)


def on_exit(icon, item):
    icon.stop()
    sys.exit(0)


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        # PyInstaller temp folder
        base_path = sys._MEIPASS
    except AttributeError:
        # Normal Python run
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def tray_thread():
    image = Image.open(resource_path("icon.png"))

    menu = Menu(
        MenuItem("Open QR page", on_open),
        MenuItem("Exit", on_exit)
    )

    icon = Icon("QRUpload", image, "QR Upload Server", menu)
    icon.run()


if __name__ == "__main__":
    # Start server in background
    threading.Thread(target=start_server, daemon=True).start()

    # Auto open browser
    threading.Thread(target=open_browser, daemon=True).start()

    # Start system tray icon (blocking)
    tray_thread()

    # Keep console alive
    input("Press ENTER to exit...\n")