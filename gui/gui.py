import tkinter as tk
from tkinter import messagebox
from network.client import Client
from chat.chat_window import ChatWindow
from data.profiles import get_username, save_username
from data.friends import get_friends, add_friend
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatty")

        # Initializes & connects client to the server
        self.client = Client(username=get_username(), message_callback=self.on_message_received)
        self.client.connect()

        # Friends List Section
        self.friends_frame = tk.Frame(self.root)
        self.friends_frame.pack(pady=10, padx=10, fill='both', expand=True)

        tk.Label(self.friends_frame, text="Your Friends").pack()
        self.friends_listbox = tk.Listbox(self.friends_frame)
        self.friends_listbox.pack(padx=10, pady=10, fill='both', expand=True)
        self.friends_listbox.bind("<ButtonRelease-1>", self.on_friend_select)

        # Buttons for adding and changing username
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(fill='x', padx=10, pady=10)

        tk.Button(self.buttons_frame, text="Add/Connect Friend", command=self.connect_friend).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Profile", command=self.update_profile).pack(side=tk.LEFT, padx=5)

        self.refresh_friends_list()

    #Updates the list section
    def refresh_friends_list(self):
        self.friends_listbox.delete(0, tk.END)
        for friend, *_ in get_friends():
            self.friends_listbox.insert(tk.END, friend)

    #Opens the chat window with saved messages
    def on_friend_select(self, event):
        sel = self.friends_listbox.curselection()
        if sel:
            friend = self.friends_listbox.get(sel)
            self.open_chat_window(friend)

    #Opens the chat window with saved messages
    def open_chat_window(self, friend_name):
        ChatWindow(friend_name, self.client)

    #adding friends dialog box
    def connect_friend(self):
        win = tk.Toplevel(self.root)
        win.title("Connect to Friend")

        tk.Label(win, text="Friend's Username:").pack(pady=5)
        entry = tk.Entry(win)
        entry.pack(pady=5)
        tk.Button(win, text="Connect", command=lambda: self.attempt_connection(entry.get().strip(), win)).pack(pady=10)

    def attempt_connection(self, friend_name, win):
        win.destroy()
        if not friend_name:
            return

        def on_status(data):
            #Contacts the other client to see if it is online
            if data.get("status") == "online":
                ip = data.get("ip"); port = data.get("port")
                add_friend(friend_name, ip, port)
                self.refresh_friends_list()
                self.open_chat_window(friend_name)
                messagebox.showinfo("Connected", f"{friend_name} is online.")
            else:
                messagebox.showwarning("Offline", f"{friend_name} is not online. No messages will be sent")
                self.open_chat_window(friend_name)

        threading.Thread(target=lambda: self.client.request_status(friend_name, on_status), daemon=True).start()

    def update_profile(self):
        win = tk.Toplevel(self.root)
        win.title("Update Profile")

        tk.Label(win, text="Enter your username:").pack(pady=10)
        entry = tk.Entry(win)
        entry.insert(0, get_username())
        entry.pack(pady=10)
        tk.Button(win, text="Save", command=lambda: self.save_profile(entry.get().strip(), win)).pack(pady=10)

    def save_profile(self, new_name, win):
        if new_name:
            save_username(new_name)
            self.client.username = new_name
        win.destroy()

    def on_message_received(self, msg):
        ChatWindow.receive_message(msg["from"], msg["content"])


def launch_gui():
    root = tk.Tk()
    App(root)
    root.mainloop()

