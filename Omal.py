import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os
import subprocess

class VSCodeInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Omal Code editor")
        self.root.geometry("800x800")  # Increased height to fit debug section

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New File")
        self.file_menu.add_command(label="Open File", command=self.open_file)
        self.file_menu.add_command(label="Save File", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo")
        self.edit_menu.add_command(label="Redo")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.root.config(menu=self.menu_bar)

        # Create a sidebar
        self.sidebar = tk.Frame(self.root, width=200, bg="gray")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_label = tk.Label(self.sidebar, text="Explorer", font=("Arial", 18))
        self.sidebar_label.pack(pady=10)
        self.sidebar_listbox = tk.Listbox(self.sidebar, width=20)
        self.sidebar_listbox.pack(fill=tk.BOTH, expand=True)

        # Create a language selection dropdown
        self.language_var = tk.StringVar()
        self.language_var.set("Python")  # default language
        self.language_menu = tk.OptionMenu(self.sidebar, self.language_var, "Python", "Java", "C++", "JavaScript", "Batch", "Lua")
        self.language_menu.pack(pady=10)

        # Create a code editor
        self.code_editor = tk.Text(self.root, width=80, height=30, font=("Monaco", 12))
        self.code_editor.pack(fill=tk.BOTH, expand=True)

        # Create a run button
        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack(pady=10)

        # Create a status bar
        self.status_bar = tk.Label(self.root, text="Ready", font=("Arial", 12), anchor=tk.W)
        self.status_bar.pack(fill=tk.X)

        # Create a debug section
        self.debug_label = tk.Label(self.root, text="Debug Output", font=("Arial", 14))
        self.debug_label.pack(fill=tk.X)

        # Create a text box to display debug output
        self.debug_output = tk.Text(self.root, width=80, height=10, font=("Monaco", 12))
        self.debug_output.pack(fill=tk.BOTH, expand=True)

        # Create a console for testing and debugging
        self.console_label = tk.Label(self.root, text="Console", font=("Arial", 14))
        self.console_label.pack(fill=tk.X)

        # Create a text box to display console output
        self.console_output = tk.Text(self.root, width=80, height=10, font=("Monaco", 12))
        self.console_output.pack(fill=tk.BOTH, expand=True)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Python files", "*.py"),
                ("Lua files", "*.lua"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            with open(file_path, "r") as file:
                self.code_editor.delete("1.0", tk.END)
                self.code_editor.insert("1.0", file.read())
            self.status_bar.config(text=f"File opened: {file_path}")

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[
                ("Python files", "*.py"),
                ("Lua files", "*.lua"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.code_editor.get("1.0", tk.END))
            self.status_bar.config(text=f"File saved to {file_path}")

    def run_code(self):
        # Get the selected language
        language = self.language_var.get()

        # Get the code from the code editor
        code = self.code_editor.get("1.0", tk.END)

        # Create a new window to display the output
        output_window = tk.Toplevel(self.root)
        output_window.title("Output")
        output_window.geometry("800x600")

        # Create a text widget to display the output
        output_text = tk.Text(output_window, width=80, height=30, font=("Monaco", 12))
        output_text.pack(fill=tk.BOTH, expand=True)

        # Run the code and display the output
        try:
            if language == "Batch":
                # Run the Batch code using the cmd executable
                output = subprocess.check_output(["cmd", "/c", code], universal_newlines=True, stderr=subprocess.STDOUT)
            elif language == "Lua":
                # Run the Lua code using the Lua executable
                output = subprocess.check_output(["lua", "-e", code], universal_newlines=True)
            else:
                # Run the code using the Python executable
                output = subprocess.check_output(["python", "-c", code], universal_newlines=True)
            output_text.insert(tk.END, output)
            output_text.insert(tk.END, "\n")
            self.status_bar.config(text="Ran successfully!")
            messagebox.showinfo("Success", "Code ran successfully!")
        except subprocess.CalledProcessError as e:
            output_text.insert(tk.END, f"Error: {e.returncode}\n")
            self.status_bar.config(text=f"Error: {e.returncode}")
            messagebox.showerror("Error", f"Error: {e.returncode}")

        # Add debug output
        self.debug_output.insert(tk.END, f"Code: {code}\n")
        self.debug_output.insert(tk.END, f"Output: {output}\n")
        self.debug_output.insert(tk.END, "\n")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VSCodeInterface()
    app.run()