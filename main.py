import tkinter as tk
from gui.app import App
from setup import initialize_directories

if __name__ == '__main__':
    initialize_directories()
    root = tk.Tk()
    app = App(root)
    root.mainloop()