import tkinter as tk
from tkinter import scrolledtext
from network.networking import connect_to_peer
from chat.chat_window import ChatWindow
from data.profiles import get_username
from data.friends import get_friends, add_friend
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Messaging App")

        # Friends List
        self.friends_frame = tk.Frame(self.root)
        self.friends_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.friends_label = tk.Label(self.friends_frame, text="Your Friends")
        self.friends_label.pack()

        self.friends_listbox = tk.Listbox(self.friends_frame)
        self.friends_listbox.pack(padx=10, pady=10, fill='both', expand=True)

        self.refresh_friends_list()

        self.friends_listbox.bind("<ButtonRelease-1>", self.on_friend_select)

        # Profile and Connect Button Frame
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(fill='x', padx=10, pady=10)

        self.connect_button = tk.Button(self.buttons_frame, text="Add/Connect Friend", command=self.connect_friend)
        self.connect_button.pack(side=tk.LEFT, padx=5)

        self.profile_button = tk.Button(self.buttons_frame, text="Profile", command=self.update_profile)
        self.profile_button.pack(side=tk.LEFT, padx=5)

    def refresh_friends_list(self):
        self.friends_listbox.delete(0, tk.END)
        friends = get_friends()
        for friend in friends:
            self.friends_listbox.insert(tk.END, friend[0])  # Only show friend's name

    def on_friend_select(self, event):
        selected_friend = self.friends_listbox.get(self.friends_listbox.curselection())
        self.open_chat_window(selected_friend)

    def open_chat_window(self, friend_name):
        ChatWindow(friend_name)

    def connect_friend(self):
        # Prompt to enter IP and port to connect
        self.connect_window = tk.Toplevel(self.root)
        self.connect_window.title("Enter Peer Details")

        self.ip_label = tk.Label(self.connect_window, text="Friend's IP Address:")
        self.ip_label.pack(pady=5)

        self.ip_entry = tk.Entry(self.connect_window)
        self.ip_entry.pack(pady=5)

        self.port_label = tk.Label(self.connect_window, text="Friend's Port:")
        self.port_label.pack(pady=5)

        self.port_entry = tk.Entry(self.connect_window)
        self.port_entry.pack(pady=5)

        self.connect_button = tk.Button(self.connect_window, text="Connect", command=self.attempt_connection)
        self.connect_button.pack(pady=10)

    def attempt_connection(self):
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()

        if ip and port:
            threading.Thread(target=self.connect_and_refresh, args=(ip, port), daemon=True).start()
            self.connect_window.destroy()

    def connect_and_refresh(self, ip, port):
        # Connect to peer
        def on_connect(friend_name, ip, port):
            add_friend(friend_name, ip, port)
            self.refresh_friends_list()
            self.open_chat_window(friend_name)

        connect_to_peer(ip, port, on_connect)

    def update_profile(self):
        # Profile settings
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Update Profile")

        self.profile_label = tk.Label(profile_window, text="Enter your username:")
        self.profile_label.pack(pady=10)

        self.profile_entry = tk.Entry(profile_window)
        self.profile_entry.insert(0, get_username())
        self.profile_entry.pack(pady=10)

        self.save_button = tk.Button(profile_window, text="Save", command=self.save_profile)
        self.save_button.pack(pady=10)

    def save_profile(self):
        # Save new username
        new_name = self.profile_entry.get().strip()
        if new_name:
            from data.profiles import save_username
            save_username(new_name)


def launch_gui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()
