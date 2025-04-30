# gui.py
import tkinter as tk
from chat.chat_window import ChatWindow
from data.friends import get_friends, add_friend
from data.profiles import get_username, save_username
from network.networking import connect_to_peer
from tkinter import simpledialog, messagebox

def launch_gui():
    root = tk.Tk()
    root.title("Messaging App")

    # Friends list section
    friends_frame = tk.Frame(root)
    friends_frame.pack(padx=10, pady=10, fill='both', expand=True)

    def open_chat(name):
        ChatWindow(name)

    def load_friends():
        for widget in friends_frame.winfo_children():
            widget.destroy()

        for name, ip, port in get_friends():
            btn = tk.Button(friends_frame, text=name, command=lambda n=name: open_chat(n))
            btn.pack(fill='x', pady=2)

    # Bottom controls
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(padx=10, pady=10, fill='x')

    def on_profile():
        name = simpledialog.askstring("Profile", "Enter your username:", initialvalue=get_username())
        if name:
            save_username(name)

    def on_connect():
        ip = simpledialog.askstring("Connect", "Enter friend's IP:")
        port = simpledialog.askinteger("Connect", "Enter friend's Port:")
        if ip and port:
            try:
                peer_name = connect_to_peer(ip, port)
                add_friend(peer_name, ip, port)
                messagebox.showinfo("Success", f"Connected with {peer_name}")
                load_friends()
            except Exception as e:
                messagebox.showerror("Connection Failed", str(e))

    profile_btn = tk.Button(bottom_frame, text="Profile", command=on_profile)
    profile_btn.pack(side='left', padx=5)

    connect_btn = tk.Button(bottom_frame, text="Add/Connect", command=on_connect)
    connect_btn.pack(side='right', padx=5)

    load_friends()
    root.mainloop()
