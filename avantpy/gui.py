import tkinter as tk

import sys


root = tk.Tk()
root.geometry("300x300")
root.title("Window Title")


def command():
    root2 = tk.Tk()
    root2.geometry("300x300")
    root2.title("New Window")
    label = tk.Label(root2, text="This is the new window")
    label.pack()
    root2.mainloop()
    sys.exit()


newwindow = tk.Button(root, text="Open New Window", command=command)
newwindow.pack()
root.mainloop()
sys.exit()
