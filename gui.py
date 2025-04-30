import tkinter as tk
from tkinter import simpledialog
from friends import get_friends, add_friend
from profiles import get_username, set_username
from networking import listen_for_peers, connect_to_peer
from chat import ChatBox
from pathlib import Path

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Message App")

        self.friends_frame = tk.Frame(self.root)
        self.friends_frame.pack(padx=10, pady=10)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(padx=10, pady=10)

        self.profile_btn = tk.Button(self.bottom_frame, text="Profile", command=self.set_profile)
        self.profile_btn.pack(side='left', padx=5)

        self.connect_btn = tk.Button(self.bottom_frame, text="Connect/Add", command=self.add_friend)
        self.connect_btn.pack(side='left', padx=5)

        self.load_friends()
        listen_for_peers(self.on_peer_connected)

    def set_profile(self):
        name = simpledialog.askstring("Profile", "Enter your username")
        if name:
            set_username(name)

    def add_friend(self):
        ip = simpledialog.askstring("Connect", "Friend IP Address:")
        port = simpledialog.askstring("Connect", "Friend Port:")
        if ip and port:
            connect_to_peer(ip, port, lambda sock: print("Connected to peer"))

    def load_friends(self):
        for widget in self.friends_frame.winfo_children():
            widget.destroy()
        for friend in get_friends():
            btn = tk.Button(self.friends_frame, text=friend['name'], command=lambda n=friend['name']: ChatBox(self.root, n))
            btn.pack(pady=2)

    def on_peer_connected(self, name, ip, port):
        self.load_friends()
        print(f"Connected with {name} at {ip}:{port}")

    def run(self):
        self.root.mainloop()

def launch_app():
    App().run()
