import socket
import threading
from profile import get_username
from friends import save_friend

DISCOVERY_PORT = 8888
BROADCAST_MESSAGE = b'DISCOVER_PEER'

import socket
import threading
import time

HOST = 'localhost'
PORT = 5050

def _handle_receive(sock, peer_name):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print(f"\n[{peer_name}]: {data}")
        except:
            break

def _handle_send(sock, name, db):
    while True:
        msg = input(f"[{name}]: ")
        if msg.lower() == 'bye':
            sock.sendall(msg.encode())
            sock.close()
            break
        sock.sendall(msg.encode())

def start_server(host=HOST, port=PORT, name="Server", peer_name="Client"):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"{name}: Waiting for connection on {host}:{port}...")
    conn, addr = server.accept()
    print(f"{name}: Connected to {addr}")

    threading.Thread(target=_handle_receive, args=(conn, peer_name), daemon=True).start()
    _handle_send(conn, name, db=None)

def start_client(host=HOST, port=PORT, name="Client", peer_name="Server"):
    time.sleep(1)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"{name}: Connected to {host}:{port}")

    threading.Thread(target=_handle_receive, args=(client, peer_name), daemon=True).start()
    _handle_send(client, name, db=None)

def listen_for_peers():
    def _listen():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', DISCOVERY_PORT))
        while True:
            msg, addr = sock.recvfrom(1024)
            if msg == BROADCAST_MESSAGE:
                sock.sendto(get_username().encode(), addr)
            elif msg.decode().isalpha():
                save_friend(msg.decode(), addr[0])
    threading.Thread(target=_listen, daemon=True).start()

def broadcast_discovery():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(BROADCAST_MESSAGE, ('<broadcast>', DISCOVERY_PORT))
    sock.close()
