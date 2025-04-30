import socket
import threading
from data.profiles import get_username
from data.friends import add_friend, get_friend_details
from chat.chat_window import ChatWindow

peers = {}

def start_server(on_connect_callback):
    def server():
        s = socket.socket()
        s.bind(("", 5050))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_peer_connection, args=(conn, addr, on_connect_callback), daemon=True).start()

    threading.Thread(target=server, daemon=True).start()

def handle_peer_connection(conn, addr, on_connect_callback):
    try:
        peer_name = conn.recv(1024).decode()
        add_friend(peer_name, addr[0], addr[1])
        conn.sendall(get_username().encode())
        peers[peer_name] = conn
        on_connect_callback(peer_name, addr[0], addr[1])
        while True:
            data = conn.recv(4096)
            if not data:
                break
            ChatWindow.receive_message(peer_name, data.decode())
    except Exception as e:
        print("Connection error:", e)
    finally:
        conn.close()
        if peer_name in peers:
            del peers[peer_name]

def connect_to_peer(ip, port, on_connect_callback):
    try:
        s = socket.socket()
        s.connect((ip, int(port)))
        s.sendall(get_username().encode())
        peer_name = s.recv(1024).decode()
        add_friend(peer_name, ip, port)
        peers[peer_name] = s
        on_connect_callback(peer_name, ip, port)

        def listen():
            try:
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    ChatWindow.receive_message(peer_name, data.decode())
            except Exception as e:
                print("Connection error:", e)
            finally:
                s.close()
                if peer_name in peers:
                    del peers[peer_name]

        threading.Thread(target=listen, daemon=True).start()
    except Exception as e:
        print("Connection failed:", e)

def send_message_to_peer(friend_name, message):
    conn = peers.get(friend_name)
    if conn:
        try:
            conn.sendall(message.encode())
        except Exception as e:
            print(f"Send failed to {friend_name}:", e)
