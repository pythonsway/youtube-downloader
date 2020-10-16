import tkinter as tk
from tkinter import scrolledtext, ttk

from . import __version__

class LicenseWindow(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master

        with open('LICENSE', 'r') as f:
            self.license_txt = f.read()
        sw = self.master.winfo_rootx()
        sh = self.master.winfo_rooty()
        ww = 830
        wh = 380
        x = int(sw)
        y = int(sh)
        self.geometry(f'{ww}x{wh}+{x}+{y}')
        self.resizable(tk.FALSE, tk.FALSE)
        # self.iconbitmap('assets/favicon.ico')
        self.title('License')
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.CHAR, width=78, height=15)
        self.text_area.grid(column=0, row=0, sticky=(tk.W, tk.E), pady=15, padx=15)
        self.text_area.insert(tk.INSERT, self.license_txt)
        self.text_area['state'] = 'disabled'
        self.ok_button = ttk.Button(self, text="Got it", command=self.destroy)
        self.ok_button.grid(column=0, row=1, sticky=(tk.W, tk.E), pady=5, padx=15)
        self.focus()


class AboutWindow(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master

        sw = self.master.winfo_rootx()
        sh = self.master.winfo_rooty()
        ww = 450
        wh = 300
        x = int(sw + (ww / 2))
        y = int(sh + (wh / 2))
        self.geometry(f'{ww}x{wh}+{x}+{y}')
        self.resizable(tk.FALSE, tk.FALSE)
        # self.iconbitmap('assets/favicon.ico')
        self.title('About this application')
        self.about_msg = ttk.Label(self, text=f'YouTube-Downloader {__version__}')
        self.about_msg.grid(column=0, row=0, columnspan=2, pady=5)
        self.s = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.s.grid(column=0, row=1, columnspan=4, sticky=(tk.E, tk.W), pady=5, padx=15)
        self.about_descr = ttk.Label(self, text='Simple application to download YouTube videos.')
        self.about_descr.grid(column=0, row=2, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=15)
        self.license_button = ttk.Button(self, text='License', command=lambda: LicenseWindow(master))
        self.license_button.grid(column=0, row=3, pady=5, padx=15)
        with open('disclaimer.txt', 'r') as f:
            self.disclaimer_txt = f.read()
        self.about_lf = ttk.Labelframe(self, text='Disclaimer')
        self.about_lf.grid(column=0, row=4, sticky=(tk.W, tk.E), pady=5, padx=15)
        self.about_discl = ttk.Label(self.about_lf, text=self.disclaimer_txt, wraplength=390)
        self.about_discl.grid(column=0, row=0, sticky=(tk.W, tk.E), pady=5, padx=15)
        self.ok_button = ttk.Button(self, text="Got it", command=self.destroy)
        self.ok_button.grid(column=0, row=5, sticky=(tk.W, tk.E), pady=5, padx=15)
        self.focus()
