import threading
from network.networking import start_server
from gui.gui import launch_gui
from setup import initialize_directories

if __name__ == '__main__':
    initialize_directories()
    threading.Thread(target=start_server, daemon=True).start()
    launch_gui()