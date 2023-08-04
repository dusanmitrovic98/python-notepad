import tkinter as tk
from tkinter import filedialog, messagebox

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.text_area = tk.Text(self.root, undo=True)
        self.text_area.pack(expand=True, fill='both')
