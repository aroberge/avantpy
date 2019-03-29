import os
import tkinter as tk
from tkinter import filedialog

import keyword
import tokenize
from io import StringIO

from .converter import transcode
from .utils import Token


class TextEditor:
    def __init__(self, parent):
        self.text_to_write = ""
        self.parent = parent
        self.parent.geometry("600x550")
        self.frame = tk.Frame(self.parent, width=600, height=550)
        self.text_area = self.init_text_area()
        self.set_horizontal_scroll()
        self.set_vertical_scroll()
        self.text_area.pack(side="left", fill="both", expand=True)
        self.frame.pack()
        self.make_menu()

    def init_text_area(self):
        text_area = tk.Text(
            self.frame,
            wrap="none",
            width=600,
            height=550,
            padx=10,
            pady=10,
            font="Monaco 11",
        )
        text_area.tag_config("blue", foreground="blue")
        text_area.tag_config(
            "bold", font="Monaco 11 bold", foreground="lime green"  # dark violet
        )
        return text_area

    def set_horizontal_scroll(self):
        scroll_x = tk.Scrollbar(
            self.frame, orient="horizontal", command=self.text_area.xview
        )
        scroll_x.config(command=self.text_area.xview)
        self.text_area.configure(xscrollcommand=scroll_x.set)
        scroll_x.pack(side="bottom", fill="x", anchor="w")

    def set_vertical_scroll(self):
        # Scroll Bar y For Height
        scroll_y = tk.Scrollbar(self.frame)
        scroll_y.config(command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")

    def make_menu(self):
        """Makes the main menu"""
        menu = tk.Menu(self.parent)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        menu.add_cascade(label="File", menu=file_menu)
        self.parent.config(menu=menu)

    def open_file(self, event=None):
        """Opens a file by looking first from the current directory."""
        txt_file = filedialog.askopenfilename(initialdir=os.getcwd())
        if txt_file:
            self.text_area.delete(1.0, tk.END)
            with open(txt_file) as new_file:
                self.insert_text(new_file.read())

    def insert_text(self, txt):
        """Inserts the text in the editor, replacing any previously existing
           content.
        """
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, txt)
        self.parent.update_idletasks()
        self.colorize()

    def get_text(self):
        """Gets the current content and returns it as a string"""
        return self.text_area.get("1.0", tk.END)

    def colorize(self):
        """Colorizes the Python keywords"""
        content = self.text_area.get("1.0", tk.END)
        tokens = tokenize.generate_tokens(StringIO(content).readline)
        for tok in tokens:
            token = Token(tok)
            if token.string in keyword.kwlist:
                begin_index = "{0}.{1}".format(token.start_line, token.start_col)
                end_index = "{0}.{1}".format(token.end_line, token.end_col)
                self.text_area.tag_add("bold", begin_index, end_index)

    def save_file(self, event=None):
        """Saves the file currently in the Texteditor"""
        file = filedialog.asksaveasfile(mode="w")
        if file is not None:
            data = self.get_text()
            file.write(data)
            file.close()


class App(tk.Tk):
    def __init__(self, title="Converter"):
        # self.geometry("200x100")
        # self.title = "Main app"
        super().__init__()
        self.title(title)
        self.geometry("300x100")
        self.add_ui()
        self.source_window = None
        self.converted_window = None

    def add_ui(self):
        button = tk.Button(self, text="Open Source File", command=self.get_source)
        button.pack()
        button = tk.Button(self, text="Convert Source", command=self.convert_source)
        button.pack()

    def get_source(self, event=None):
        """Opens a file by looking first from the current directory."""
        txt_file = filedialog.askopenfilename(initialdir=os.getcwd())
        if txt_file:
            if self.source_window is None:
                self.source_window = tk.Toplevel()
                self.source_window.protocol(
                    "WM_DELETE_WINDOW", self.close_source_window
                )
                self.source = TextEditor(self.source_window)
            self.source_window.title("Source: %s" % os.path.basename(txt_file))
            with open(txt_file, encoding="utf8") as new_file:
                self.source.insert_text(new_file.read())

    def close_source_window(self):
        self.source_window.destroy()
        self.source_window = None

    def convert_source(self, event=None):
        """Opens a file by looking first from the current directory."""
        if self.converted_window is None:
            self.converted_window = tk.Toplevel()
            self.converted_window.protocol(
                "WM_DELETE_WINDOW", self.close_converted_window
            )
            self.converted = TextEditor(self.converted_window)
        self.converted_window.title("Converted")
        text = self.source.get_text()
        new_text = transcode(text, "pyfr", "pyen")
        self.converted.insert_text(new_text)

    def close_converted_window(self):
        self.converted_window.destroy()
        self.converted_window = None


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
