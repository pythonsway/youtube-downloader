import tkinter as tk

from gui import MainApp


def main():
    root = tk.Tk()
    app = MainApp(root)
    app.mainloop()


if __name__ == '__main__':
    main()
