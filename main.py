import threading
from network.networking import start_server
from gui.gui import launch_gui
from setup import initialize_directories

def start_app():
    threading.Thread(target=start_server, daemon=True).start()

    launch_gui()

if __name__ == '__main__':
    initialize_directories()
    start_app()
