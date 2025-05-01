import socket
import threading
import json

HOST = '0.0.0.0'
PORT = 5000

# Map username → { socket: socket_obj, addr: (ip, port) }
clients = {}

def send_json(sock, data):
    """Safely send a JSON‐encoded dict over the given socket."""
    try:
        sock.sendall(json.dumps(data).encode())
    except Exception as e:
        print(f"[ERROR] send_json: {e}")

def broadcast(to_username, message_data):
    """Forward a chat message to the intended recipient if they're online."""
    entry = clients.get(to_username)
    if entry:
        send_json(entry['socket'], message_data)

def handle_client(client_socket, addr):
    username = None
    try:
        # 1) Expect a login packet first
        raw = client_socket.recv(4096)
        login = json.loads(raw.decode())
        if login.get("type") != "login" or "username" not in login:
            client_socket.close()
            return

        username = login["username"]
        clients[username] = { 'socket': client_socket, 'addr': addr }
        print(f"[LOGIN] {username} @ {addr} connected.")

        # Acknowledge login
        send_json(client_socket, { "type": "login_ack", "status": "ok" })

        # 2) Enter main receive loop
        while True:
            raw = client_socket.recv(4096)
            if not raw:
                break

            data = json.loads(raw.decode())
            kind = data.get("type")

            if kind == "status_request":
                # { "type":"status_request", "friend":"bob" }
                friend = data.get("friend")
                if friend in clients:
                    fentry = clients[friend]
                    resp = {
                        "type": "status_response",
                        "friend": friend,
                        "status": "online",
                        "ip": fentry['addr'][0],
                        "port": fentry['addr'][1]
                    }
                else:
                    resp = {
                        "type": "status_response",
                        "friend": friend,
                        "status": "offline"
                    }
                send_json(client_socket, resp)

            elif kind == "message":
                # { "type":"message","from":"alice","to":"bob","content":"Hi!" }
                to_user = data.get("to")
                broadcast(to_user, data)

            else:
                print(f"[WARN] Unknown packet type from {username}: {kind}")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        # Cleanup on disconnect
        if username:
            del clients[username]
            print(f"[DISCONNECT] {username} disconnected.")
        client_socket.close()

def start_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"[STARTED] Server listening on {HOST}:{PORT}")

    while True:
        client_sock, addr = server_sock.accept()
        threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
