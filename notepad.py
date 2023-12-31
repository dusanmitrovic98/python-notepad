import tkinter as tk
from tkinter import filedialog, messagebox

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.text_area = tk.Text(self.root, undo=True)
        self.text_area.pack(expand=True, fill='both')
        self.current_file = None
        self.dark_mode = False  # Default is light mode
        self.create_menu()
        self.create_shortcuts()

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Line: 1 | Column: 0")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Alt+F4")
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode, accelerator="Ctrl+T")
        menubar.add_cascade(label="View", menu=view_menu)

        self.root.config(menu=menubar)

    def create_shortcuts(self):
        self.root.bind_all("<Control-n>", lambda event: self.new_file())
        self.root.bind_all("<Control-o>", lambda event: self.open_file())
        self.root.bind_all("<Control-s>", lambda event: self.save_file())
        self.root.bind_all("<Control-S>", lambda event: self.save_file_as())
        self.root.bind_all("<Control-z>", lambda event: self.text_area.edit_undo())
        self.root.bind_all("<Control-y>", lambda event: self.text_area.edit_redo())
        self.root.bind_all("<Any-KeyPress>", self.update_status_bar)
        self.root.bind_all("<Control-T>", lambda event: self.toggle_dark_mode())

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.current_file = file_path

    def save_file(self):
        try:
            if self.current_file:
                content = self.text_area.get(1.0, tk.END)
                with open(self.current_file, "w") as file:
                    file.write(content)
            else:
                self.save_file_as()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            content = self.text_area.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)
            self.current_file = file_path

    def update_status_bar(self, event=None):
        cursor_position = self.text_area.index(tk.INSERT)
        line, column = cursor_position.split('.')
        line_num, col_num = int(line), int(column)
        status_text = f"Line: {line_num} | Column: {col_num}"
        self.status_bar.config(text=status_text)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg_color = "#505050" if self.dark_mode else "white"
        fg_color = "white" if self.dark_mode else "black"
        self.root.configure(bg=bg_color)
        self.text_area.configure(bg=bg_color, fg=fg_color)
        self.status_bar.configure(bg=bg_color, fg=fg_color)

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
