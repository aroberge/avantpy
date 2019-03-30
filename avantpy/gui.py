"""This module provides a GUI to the conversion function.

It makes it possible to load up a source file written in a given dialect
and convert it into another dialect or into Python, showing both the
original source and the converted one in two different editor frames,
with Python keyword, as well as their counterpart in various dialects,
highlighted.
"""
import os
import tkinter as tk
import tokenize

from io import StringIO
from tkinter import filedialog, ttk

from .converter import transcode
from .session import state
from .utils import Token


class TextEditor:
    """A scrollable text editor, that can save files."""

    def __init__(self, parent, title="Window title", app=None):
        self.text_to_write = ""
        self.parent = parent
        self.app = app
        self.parent.title(title)
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
            font="Monaco 14",
        )
        text_area.tag_config("Python", font="Monaco 14 bold", foreground="forest green")
        text_area.tag_config("source", font="Monaco 14 bold", foreground="blue")
        text_area.tag_config(
            "converted", font="Monaco 14 bold", foreground="dark violet"
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
        file_menu.add_command(label="Save", command=self.save_file)
        menu.add_cascade(label="File", menu=file_menu)
        self.parent.config(menu=menu)

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
        """Colorizes the Python keywords and a few builtins, as well as the
           corresponding version in other dialects.
        """
        if self.app is None:
            return
        content = self.text_area.get("1.0", tk.END)
        tokens = tokenize.generate_tokens(StringIO(content).readline)
        for tok in tokens:
            token = Token(tok)
            if token.string in self.app.python_words:
                begin_index = "{0}.{1}".format(token.start_line, token.start_col)
                end_index = "{0}.{1}".format(token.end_line, token.end_col)
                self.text_area.tag_add("Python", begin_index, end_index)
            elif token.string in self.app.source_words:
                begin_index = "{0}.{1}".format(token.start_line, token.start_col)
                end_index = "{0}.{1}".format(token.end_line, token.end_col)
                self.text_area.tag_add("source", begin_index, end_index)
            elif token.string in self.app.converted_words:
                begin_index = "{0}.{1}".format(token.start_line, token.start_col)
                end_index = "{0}.{1}".format(token.end_line, token.end_col)
                self.text_area.tag_add("converted", begin_index, end_index)

    def save_file(self, event=None):
        """Saves the file currently in the Texteditor"""
        filename = filedialog.asksaveasfilename(
            filetypes=(("AvantPy/Python", "*.py*"),)
        )
        if filename is not None:
            with open(filename, "w", encoding="utf8") as f:
                data = self.get_text()
                f.write(data)


class App(tk.Tk):
    def __init__(self, title="Converter"):
        # self.geometry("200x100")
        # self.title = "Main app"
        super().__init__()
        self.title(title)
        self.geometry("300x100")
        self.source_window = None
        self.converted_window = None
        self.all_dialects = ["py"] + state.all_dialects()
        ext = ["*.%s" % d for d in self.all_dialects]
        self.filetypes = " ".join(ext)
        self.add_ui()
        self.python_words = []
        self.source_words = []
        self.converted_words = []

    def add_ui(self):
        """Adds UI elements to the main window"""
        button = tk.Button(self, text="Open Source File", command=self.get_source)
        button.pack()
        button = tk.Button(self, text="Convert Source", command=self.convert_source)
        button.pack()
        # if the following is assigned a local value, it will be garbage collected
        # and the combobox will show nothing initially.
        self._choice = tk.StringVar()
        self.dialects = ttk.Combobox(
            self, textvariable=self._choice, values=self.all_dialects
        )
        self.dialects.current(0)
        self.dialects.bind("<<ComboboxSelected>>", self.get_conversion_dialect)
        self.dialects.pack()
        self.conversion_dialect = self.all_dialects[0]

    def get_conversion_dialect(self, event):
        """Gets the conversion dialect selected from the ComboBox."""
        self.conversion_dialect = self.dialects.get()

    def get_source(self, event=None):
        """Opens a file by looking first from the current directory."""
        txt_file = filedialog.askopenfilename(
            initialdir=os.getcwd(), filetypes=(("AvantPy", self.filetypes),)
        )
        self.source_dialect = txt_file.split(".")[-1]
        if self.source_dialect == "py":
            self.source_dialect = "pyen"
        self.python_words = set(state.get_from_python(self.source_dialect).keys())
        self.source_words = set(state.get_to_python(self.source_dialect).keys())
        if txt_file:
            if self.source_window is None:
                self.source_window = tk.Toplevel()
                self.source_window.protocol(
                    "WM_DELETE_WINDOW", self.close_source_window
                )
                self.source = TextEditor(
                    self.source_window,
                    title="Source: %s" % os.path.basename(txt_file),
                    app=self,
                )
            with open(txt_file, encoding="utf8") as new_file:
                self.source.insert_text(new_file.read())

    def close_source_window(self):
        """Closes the source window"""
        # When we get a notice that a request to close the window has been made,
        # , we close it explicitly and set its
        # reference to None, to avoid exceptions being raised if
        # another request is made.
        self.source_window.destroy()
        self.source_window = None

    def convert_source(self, event=None):
        """Converts the content of the source window into the requested dialect."""
        if self.converted_window is None:
            self.converted_window = tk.Toplevel()
            self.converted_window.protocol(
                "WM_DELETE_WINDOW", self.close_converted_window
            )
            self.converted = TextEditor(
                self.converted_window,
                title="Converted: dialect = %s" % self.conversion_dialect,
                app=self,
            )
        text = self.source.get_text()
        if self.conversion_dialect != "py":
            self.converted_words = set(
                state.get_to_python(self.conversion_dialect).keys()
            )
        else:
            self.converted_words = set(state.get_from_python("pyen").keys())

        new_text = transcode(text, self.source_dialect, self.conversion_dialect)
        self.converted.insert_text(new_text)

    def close_converted_window(self):
        """Closes the converted window."""
        # See close_source_window for an explanation
        self.converted_window.destroy()
        self.converted_window = None


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
