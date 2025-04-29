import socket
import threading
import time

HOST = 'localhost'
PORT = 5050

def _handle_receive(sock, peer_name, db):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            db.save_message(f"[{peer_name}]: {data}")
        except:
            break

def _handle_send(sock, name):
    while True:
        msg = input(f"[{name}]: ")
        if msg.lower() == 'bye':
            sock.sendall(msg.encode())
            sock.close()
            break
        sock.sendall(msg.encode())

def start_server(host=HOST, port=PORT, name="Server", peer_name="Client", db=None):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"{name}: Waiting for connection on {host}:{port}...")
    conn, addr = server.accept()
    print(f"{name}: Connected to {addr}")

    threading.Thread(target=_handle_receive, args=(conn, peer_name, db), daemon=True).start()
    _handle_send(conn, name)

def start_client(host=HOST, port=PORT, name="Client", peer_name="Server", db=None):
    time.sleep(1)  # ensure server is up
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"{name}: Connected to {host}:{port}")

    threading.Thread(target=_handle_receive, args=(client, peer_name, db), daemon=True).start()
    _handle_send(client, name)
