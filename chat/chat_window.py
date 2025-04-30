import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from data.database import MessageDatabase, Message
from pathlib import Path
from network.networking import send_message_to_peer

class ChatWindow:
    windows = {}

    def __init__(self, friend_name):
        if friend_name in ChatWindow.windows:
            ChatWindow.windows[friend_name].window.lift()
            return
        self.friend_name = friend_name
        self.window = tk.Toplevel()
        self.window.title(f"Chat with {friend_name}")
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.text_area = scrolledtext.ScrolledText(self.window, state='disabled', wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10, fill='both', expand=True)

        self.entry = tk.Entry(self.window)
        self.entry.pack(padx=10, pady=(0, 10), fill='x')
        self.entry.bind("<Return>", self.send_message)

        self.db_path = Path.home() / "messageapp" / "Messages" / f"{friend_name}.db"
        self.db = MessageDatabase(str(self.db_path))
        self.load_messages()

        ChatWindow.windows[friend_name] = self

    def load_messages(self):
        for message in self.db.get_all_messages():
            self.display_message(message)

    def send_message(self, event=None):
        content = self.entry.get().strip()
        if content:
            message = Message(content)
            self.db.save_message(message)
            self.display_message(message)
            send_message_to_peer(self.friend_name, content)
            self.entry.delete(0, tk.END)

    def display_message(self, message):
        self.text_area['state'] = 'normal'
        self.text_area.insert(tk.END, f"[{message.timestamp}] {message.text}\n")
        self.text_area['state'] = 'disabled'
        self.text_area.see(tk.END)

    def close(self):
        ChatWindow.windows.pop(self.friend_name, None)
        self.window.destroy()

    @staticmethod
    def receive_message(friend_name, content):
        win = ChatWindow.windows.get(friend_name) or ChatWindow(friend_name)
        message = Message(content)
        win.db.save_message(message)
        win.display_message(message)
