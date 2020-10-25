import ctypes
import pkg_resources
import tkinter as tk

from gui import MainApp
from utils.console_output import hide_console


def main():
    root = tk.Tk()
    app = MainApp(root)
    app.mainloop()


if __name__ == '__main__':
    hide_console()
    main()
