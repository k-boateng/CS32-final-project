import tkinter as tk
import socket
from tkinter import scrolledtext
import threading
from storage import MessageDatabase

class ChatApp:
    def __init__(self, master, sock, name, peer_name, db):
        self.master = master
        self.sock = sock
        self.name = name
        self.peer_name = peer_name
        self.db = db

        master.title(f"Chat with {peer_name}")

        self.chat_area = scrolledtext.ScrolledText(master, state='disabled', width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(master, width=50)
        self.entry.pack(padx=10, pady=10)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack()

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break
                self.append_message(f"[{self.peer_name}]: {data}", is_friend=True)
                self.db.save_message(f"[{self.peer_name}]: {data}")
            except:
                break

    def send_message(self, event=None):
        msg = self.entry.get()
        if msg:
            self.sock.sendall(msg.encode())
            self.append_message(f"[{self.name}]: {msg}", is_friend=False)
            self.db.save_message(f"[{self.name}]: {msg}")
            self.entry.delete(0, tk.END)

    def append_message(self, msg, is_friend):
        self.chat_area.configure(state='normal')
        color = 'blue' if is_friend else 'green'
        self.chat_area.insert(tk.END, msg + "\n", color)
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)  # auto-scroll down

        self.chat_area.tag_configure('green', foreground='green')
        self.chat_area.tag_configure('blue', foreground='blue')

def start_server_gui(host='localhost', port=5050, name="Server", peer_name="Client"):
    db = MessageDatabase(friend_name=peer_name)  # Now passing friend name
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"{name}: Waiting for connection on {host}:{port}...")
    conn, addr = server.accept()
    print(f"{name}: Connected to {addr}")

    root = tk.Tk()
    app = ChatApp(root, conn, name, peer_name, db)
    root.mainloop()

    db.close()
    conn.close()

def start_client_gui(host='localhost', port=5050, name="Client", peer_name="Server"):
    db = MessageDatabase(friend_name=peer_name)  # Now passing friend name
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"{name}: Connected to {host}:{port}")

    root = tk.Tk()
    app = ChatApp(root, client, name, peer_name, db)
    root.mainloop()

    db.close()
    client.close()
