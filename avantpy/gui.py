"""This module provides a GUI to the conversion function.

It makes it possible to load up a source file written in a given dialect
and convert it into another dialect or into Python, showing both the
original source and the converted one in two different editor frames,
with Python keyword, as well as their counterpart in various dialects,
highlighted.

.. todo::

   This module needs to be documented properly

"""
import os
import tkinter as tk
import tokenize

from io import StringIO
from tkinter import filedialog, ttk

from .converter import transcode
from .session import state
from .utils import Token
from . import exception_handling


class EditorWidget(tk.Frame):
    """A scrollable text editor, that can save files."""

    def __init__(self, parent, parent_frame, other=None):
        super().__init__()
        self.parent = parent
        self.parent_frame = parent_frame
        self.other = other
        self.frame = tk.Frame(self, width=600, height=600)
        self.text_area = self.init_text_area()
        self.set_horizontal_scroll()
        self.set_vertical_scroll()
        self.linenumbers = TextLineNumbers(self.frame, width=30)
        self.linenumbers.attach(self.text_area)
        if self.other is None:
            self.linenumbers.pack(side="right", fill="y")
        else:
            self.linenumbers.pack(side="left", fill="y")
        self.text_area.pack(side="left", fill="both", expand=True)
        self.text_area.bind("<Key>", self.colorize)
        self.frame.pack(fill="both", expand=True)

    def init_text_area(self):
        text_area = tk.Text(
            self.frame,
            wrap="none",
            width=600,
            height=600,
            padx=10,
            pady=10,
            font="Monaco 12",
        )
        text_area.tag_config("Python", font="Monaco 12 bold", foreground="forest green")
        text_area.tag_config("source", font="Monaco 12 bold", foreground="blue")
        text_area.tag_config(
            "converted", font="Monaco 12 bold", foreground="dark violet"
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
        def scroll_vertical(*args):
            self.text_area.yview(*args)
            if self.other is not None:
                self.other.text_area.yview(*args)

        if self.other is not None:
            scroll_y = tk.Scrollbar(self.frame)
            scroll_y.config(command=scroll_vertical)
            self.text_area.configure(yscrollcommand=scroll_y.set)
            scroll_y.pack(side="right", fill="y")

    def insert_text(self, txt):
        """Inserts the text in the editor, replacing any previously existing
           content.
        """
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", txt)
        self.parent.update_idletasks()
        self.colorize()

    def get_text(self):
        """Gets the current content and returns it as a string"""
        # For some reason, an extra "\n" is added, which we need to remove.
        return self.text_area.get("1.0", tk.END)[:-1]

    def colorize(self, event=None):
        """Colorizes the Python keywords and a few builtins, as well as the
           corresponding version in other dialects.
        """
        content = self.text_area.get("1.0", tk.END)
        try:
            tokens = tokenize.generate_tokens(StringIO(content).readline)
            for tok in tokens:
                token = Token(tok)
                if token.string in self.parent_frame.python_words:
                    begin_index = "{0}.{1}".format(token.start_line, token.start_col)
                    end_index = "{0}.{1}".format(token.end_line, token.end_col)
                    self.text_area.tag_add("Python", begin_index, end_index)
                elif token.string in self.parent_frame.source_words:
                    begin_index = "{0}.{1}".format(token.start_line, token.start_col)
                    end_index = "{0}.{1}".format(token.end_line, token.end_col)
                    self.text_area.tag_add("source", begin_index, end_index)
                elif token.string in self.parent_frame.converted_words:
                    begin_index = "{0}.{1}".format(token.start_line, token.start_col)
                    end_index = "{0}.{1}".format(token.end_line, token.end_col)
                    self.text_area.tag_add("converted", begin_index, end_index)
        except tokenize.TokenError:
            pass

    def save_file(self, event=None):
        """Saves the file currently in the Texteditor"""
        filename = filedialog.asksaveasfilename(
            filetypes=(("AvantPy/Python", "*.py*"),)
        )
        if filename is not None:
            with open(filename, "w", encoding="utf8") as f:
                data = self.get_text()
                f.write(data)


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, textwidget):
        self.textwidget = textwidget
        self.redraw()

    def redraw(self, *args):
        """redraw line numbers"""
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, font="Monaco 12")
            i = self.textwidget.index("%s+1line" % i)
        self.after(30, self.redraw)


class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title("Converter")
        self.all_dialects = ["py"] + state.all_dialects()
        ext = ["*.%s" % d for d in self.all_dialects]
        self.filetypes = " ".join(ext)
        self.add_ui()
        self.python_words = []
        self.source_words = []
        self.converted_words = []

    def add_ui(self):
        """Adds UI elements to the main window"""

        for r in range(3):
            self.master.rowconfigure(r, weight=1, minsize=20)
        for c in [1, 5]:
            self.master.columnconfigure(c, weight=1, minsize=40)

        tk.Label(self.master, text="Source").grid(row=0, column=1)
        tk.Label(self.master, text="Converted").grid(row=0, column=4)

        self.converted_editor = EditorWidget(self.master, self)
        self.converted_editor.grid(row=1, column=3, columnspan=4, sticky="news")
        self.source_editor = EditorWidget(
            self.master, self, other=self.converted_editor
        )
        self.source_editor.grid(row=1, column=0, columnspan=3, sticky="news")

        tk.Button(self.master, text="Open", command=self.get_source).grid(
            row=2, column=0, sticky="w"
        )
        tk.Button(self.master, text="Save", command=self.source_editor.save_file).grid(
            row=2, column=1, sticky="w"
        )
        tk.Button(self.master, text="Convert source", command=self.convert_source).grid(
            row=2, column=3, sticky="w"
        )
        # if the following is assigned a local value, it will be garbage collected
        # and the combobox will show nothing initially.
        self._choice = tk.StringVar()
        self.dialects = ttk.Combobox(
            self.master, textvariable=self._choice, values=self.all_dialects
        )
        self.dialects.grid(row=2, column=4, sticky="w")
        self.dialects.current(0)
        self.dialects.bind("<<ComboboxSelected>>", self.get_conversion_dialect)
        self.conversion_dialect = self.all_dialects[0]
        tk.Button(
            self.master, text="Save", command=self.converted_editor.save_file
        ).grid(row=2, column=5, sticky="w")

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
            with open(txt_file, encoding="utf8") as new_file:
                self.source_editor.insert_text(new_file.read())

    def convert_source(self, event=None):
        """Converts the content of the source window into the requested dialect."""
        text = self.source_editor.get_text()
        if self.conversion_dialect != "py":
            self.converted_words = set(
                state.get_to_python(self.conversion_dialect).keys()
            )
        else:
            self.converted_words = set(state.get_from_python("pyen").keys())

        try:
            new_text = transcode(text, self.source_dialect, self.conversion_dialect)
        except Exception as exc:
            exception_handling.write_err = self.converted_editor.insert_text
            exception_handling.write_exception_info(exc, text)
        else:
            self.converted_editor.insert_text(new_text)


def main():
    root = tk.Tk()
    root.geometry("900x600+200+200")
    root.minsize(600, 600)
    app = App(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
