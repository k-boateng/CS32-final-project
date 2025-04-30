import tkinter as tk
from tkinter import scrolledtext
from database import Message, MessageDatabase
from datetime import datetime
from pathlib import Path

class ChatBox:
    def __init__(self, root, friend_name):
        self.friend_name = friend_name
        db_path = Path.home() / f"messageapp/Messages/{friend_name}.db"
        self.db = MessageDatabase(str(db_path))

        self.window = tk.Toplevel(root)
        self.window.title(f"Chat with {friend_name}")

        self.chat_display = scrolledtext.ScrolledText(self.window, state='disabled', width=50, height=20)
        self.chat_display.pack(padx=10, pady=10)

        self.msg_entry = tk.Entry(self.window, width=40)
        self.msg_entry.pack(side='left', padx=10)
        self.send_btn = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_btn.pack(side='left')

        self.load_messages()

    def load_messages(self):
        messages = self.db.get_all_messages()
        for msg in messages:
            self._display_message(msg.text, msg.timestamp)

    def send_message(self):
        text = self.msg_entry.get()
        if text:
            timestamp = datetime.now().isoformat()
            self._display_message(text, timestamp)
            self.db.save_message(Message(text, timestamp))
            self.msg_entry.delete(0, tk.END)

    def _display_message(self, text, timestamp):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"[{timestamp}] {text}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
