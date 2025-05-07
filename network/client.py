import socket
import threading
import json

SERVER_IP = '127.0.0.1'   # change to the server’s IP when this script is ran on the other client
PORT = 5000

class Client:
    def __init__(self, username, message_callback):
        self.username = username
        self.message_callback = message_callback
        self.status_callbacks = {}    # friend → callback
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        #Connect to server and send the login packet.
        self.sock.connect((SERVER_IP, PORT))
        login = {"type": "login", "username": self.username}
        self.sock.sendall(json.dumps(login).encode())
        threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def listen_for_messages(self):
        #Receive JSON packets
        while True:
            try:
                raw = self.sock.recv(4096)
                if not raw:
                    break
                data = json.loads(raw.decode())
                kind = data.get("type")

                if kind == "status_response":
                    friend = data.get("friend")
                    cb = self.status_callbacks.pop(friend, None)
                    if cb:
                        cb(data)

                elif kind == "message":
                    # data includes: type, from, to, content
                    self.message_callback(data)

                else:
                    # ignore other packets
                    pass

            except Exception as e:
                print(f"[ERROR] listening: {e}")
                break

    def request_status(self, friend, callback):
        #Asks the server if `friend` is online. Invoke callback with the status_response."""
        self.status_callbacks[friend] = callback
        pkt = {"type": "status_request", "friend": friend}
        try:
            self.sock.sendall(json.dumps(pkt).encode())
        except Exception as e:
            print(f"[ERROR] request_status: {e}")

    def send(self, to_username, content):
        #Send a chat message packet through the server.
        msg = {
            "type": "message",
            "from": self.username,
            "to": to_username,
            "content": content
        }
        try:
            self.sock.sendall(json.dumps(msg).encode())
        except Exception as e:
            print(f"[ERROR] send_message: {e}")
