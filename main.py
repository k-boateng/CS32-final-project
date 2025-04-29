import sys
from gui import start_server_gui, start_client_gui
from config import is_new_user  # Importing the folder setup

def main():
    # Ensure the necessary directories are created
    is_new_user()

    if len(sys.argv) < 2:
        print("Usage: python main.py <server|client>")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "server":
        start_server_gui(host="localhost", port=5050, name="Server", peer_name="Client")
    elif mode == "client":
        start_client_gui(host="localhost", port=5050, name="Client", peer_name="Server")
    else:
        print("Invalid mode. Please choose 'server' or 'client'.")
        sys.exit(1)

if __name__ == "__main__":
    main()