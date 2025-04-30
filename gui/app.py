import tkinter as tk
from tkinter import simpledialog, messagebox
from data.profiles import get_username, save_username
from data.friends import get_friends
from chat.chat_window import ChatWindow
from network.networking import start_discovery_server, connect_to_peer

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Messaging App")
        self.friend_buttons = []

        self.friend_frame = tk.Frame(self.root)
        self.friend_frame.pack(fill='both', expand=True)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill='x')

        self.profile_btn = tk.Button(self.bottom_frame, text="Profile", command=self.set_profile)
        self.profile_btn.pack(side='left', expand=True, fill='x')

        self.add_btn = tk.Button(self.bottom_frame, text="Add/Connect", command=self.add_friend)
        self.add_btn.pack(side='right', expand=True, fill='x')

        self.refresh_friend_list()
        start_discovery_server(self.on_new_connection)

    def refresh_friend_list(self):
        for btn in self.friend_buttons:
            btn.destroy()
        self.friend_buttons.clear()
        for name, ip, port in get_friends():
            b = tk.Button(self.friend_frame, text=name, command=lambda n=name: ChatWindow(n))
            b.pack(fill='x', pady=2)
            self.friend_buttons.append(b)

    def set_profile(self):
        name = simpledialog.askstring("Profile", "Enter your name:")
        if name:
            save_username(name)

    def add_friend(self):
        ip = simpledialog.askstring("Connect", "Enter friend's IP:")
        port = simpledialog.askstring("Connect", "Enter friend's Port:")
        if ip and port:
            connect_to_peer(ip, port, self.on_new_connection)

    def on_new_connection(self, name, ip, port):
        messagebox.showinfo("Connected", f"Connected with {name}!")
        self.refresh_friend_list()
