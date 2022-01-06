# from functools import partial
from pathlib import Path
from importlib import resources
from threading import Event, Thread
import tkinter as tk
from tkinter import filedialog, ttk

import requests
from PIL import Image, ImageTk

from .about_window import AboutWindow
from utils.custom_paths import resource_path
from utils.custom_threads import KThread
from utils.youtube_downloader import YouTubeDownloader


class MainApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.yt = YouTubeDownloader()
        self.download_option = tk.IntVar()
        self.output_dir = tk.StringVar()
        self.output_file = tk.StringVar()
        self.output_extension = tk.StringVar()
        self.itag = tk.IntVar()
        self.status_text = tk.StringVar()
        self.download_running = tk.BooleanVar()
        self.yt_url = tk.StringVar()
        self.yt_title = tk.StringVar()
        self.yt_thumbnail = None
        self.yt_length = tk.StringVar()
        self.yt_author = tk.StringVar()
        self.yt_file_size = tk.DoubleVar()
        self.yt_current_size = tk.DoubleVar()
        self.thread_flag = Event()

        self.customize_window()
        self.create_styles()
        self.create_widgets()
        self.create_window_menu()
        self.create_contextual_menu()
        self.create_bindings()
        self.additional_styling()

    def customize_window(self):
        self.master.resizable(tk.FALSE, tk.FALSE)
        # self.master.iconbitmap('assets/favicon.ico')
        # with resources.path('assets', 'icon.png') as icon_path:
        #     self._icon = tk.PhotoImage(file=icon_path)
        icon_path = resource_path('assets', 'icon.png')
        self._icon = tk.PhotoImage(file=icon_path)
        self.master.iconphoto(True, self._icon)
        self.master.title('YouTube Downloader')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    def create_styles(self):
        self.s = ttk.Style()
        self.s.configure('Start.TButton', font='-weight bold', foreground='green', padding=10)

    def toggle_check(self, *args):
        if self.yt_url.get():
            self.check_button['state'] = 'focus'
            self.filemenu.entryconfigure('Check URL', state=tk.NORMAL)
        else:
            self.check_button['state'] = 'disabled'
            self.filemenu.entryconfigure('Check URL', state=tk.DISABLED)

    def toggle_download(self, *args):
        self.streams_tree.delete(*self.streams_tree.get_children())
        self.download_button['state'] = 'disabled'
        self.filemenu.entryconfigure('Download', state=tk.DISABLED)
        if self.yt_title.get():
            self.status_text.set('Check URL again.')

    def itag_select(self, e):
        idx = e.widget.selection()[0]
        # streams_tree.item(idx)['text']
        self.itag.set(int(self.streams_tree.set(idx, column='itag')))
        self.output_extension.set(self.streams_tree.set(idx, column='type'))
        self.yt_file_size.set(float(self.streams_tree.set(idx, column='size')))
        self.status_text.set(f'itag selected: {self.itag.get()}.')
        self.download_button['state'] = 'focus'
        self.filemenu.entryconfigure('Download', state=tk.NORMAL)

    def check(self):
        self.check_button.state(['disabled'])
        self.filemenu.entryconfigure('Check URL', state=tk.DISABLED)
        self.status_text.set('Checking provided url...')
        try:
            self.yt.check(self.yt_url.get(), self.download_option.get())
            self.yt_title.set(self.yt.title)
            self.output_file.set(self.yt.title)
            self.yt_thumbnail = self.yt.thumbnail_url
            self.yt_length.set(self.yt.length)
            self.yt_author.set(self.yt.author)
            # 'image'
            image_obj = ImageTk.PhotoImage(Image.open(requests.get(self.yt_thumbnail, stream=True).raw))
            self.image = ttk.Label(self.fileframe, image=image_obj)
            # garbage collector prevention
            self.image.image = image_obj
            self.image.grid(column=1, row=3, sticky=(tk.W), pady=5, padx=5)
            self.streams_tree.delete(*self.streams_tree.get_children())
            for item in self.yt.streams_list:
                self.streams_tree.insert('', 'end', values=item)

            self.check_button['state'] = 'focus'
            self.status_text.set('URL checked.')
        except Exception as err:
            self.status_text.set(f'Something went wrong with {err.__doc__}.')

    def select_dir(self):
        self.dirname = filedialog.askdirectory(title='Select destination folder', initialdir=self.output_dir.get())
        if self.dirname:
            self.output_dir.set(self.dirname)
            self.status_text.set('Folder selected.')

    def paste_url(self):
        try:
            self.yt_url.set(str(self.master.clipboard_get()).strip())
        except tk.TclError:
            pass

        #       stream,    chunk, file_handle, bytes_remaining
    def show_progress_bar(self, stream, chunk, bytes_remaining):
        mbytes_downloaded = float(f'{(stream.filesize - bytes_remaining) / 1024**2:.2f}')
        self.yt_current_size.set(mbytes_downloaded)
        self.p_label['text'] = f'{self.yt_current_size.get()} / {self.yt_file_size.get()} MB'

    def on_complete(self, stream, file_handle):
        self.itag.set(None)
        self.yt_file_size.set(None)
        if not self.yt.file_complete():
            self.status_text.set('Converting to mp3...')
            self.yt.file_converter(file_handle)
            # self.yt.convert()
            # self.convert_thread = KThread(target=self.yt.convert, daemon=True)
            # self.convert_thread.start()
        self.status_text.set('Done.')

    def download(self):
        self.download_button['state'] = 'disabled'
        self.cancel_button['state'] = 'focus'
        self.filemenu.entryconfigure('Download', state=tk.DISABLED)
        self.download_running.set(True)
        self.yt_current_size.set(0.0)
        self.progress_bar.configure(maximum=self.yt_file_size.get())
        self.status_text.set('Downloading...')
        self.yt.register_on_progress_callback(self.show_progress_bar)
        self.yt.register_on_complete_callback(self.on_complete)
        # self.yt.download(self.itag.get(), self.output_dir.get(), self.output_file.get())
        self.download_thread = KThread(target=self.yt.download, daemon=True, args=(self.itag.get(),
                                                                                   self.output_dir.get(),
                                                                                   self.output_file.get(),
                                                                                   self.output_extension.get(),))
        self.download_thread.start()

    def cancel(self):
        self.download_thread.kill()
        self.download_button['state'] = 'focus'
        self.cancel_button['state'] = 'disabled'
        self.filemenu.entryconfigure('Download', state=tk.NORMAL)
        self.status_text.set('Download canceled.')

    def create_widgets(self):
        self.download_option.set(1)
        self.options_frame = ttk.Labelframe(self, text='Download options')
        self.options_frame.grid(column=0, row=0, columnspan=1, sticky=(tk.W, tk.E), pady=5, padx=15)
        self.rb1 = ttk.Radiobutton(self.options_frame, text='Single video', variable=self.download_option, value=1)
        self.rb2 = ttk.Radiobutton(self.options_frame, text='Audio as "mp3"', variable=self.download_option, value=2)
        self.rb1.grid(column=0, row=0, sticky=tk.W)
        self.rb2.grid(column=0, row=1, sticky=tk.W)
        self.download_option.trace_add('write', self.toggle_download)

        # 'download button'
        # self.download_button = ttk.Button(self, text='Download', state='disabled', style='Start.TButton',
        #                                   command=lambda: Thread(target=self.download).start())
        self.download_button = ttk.Button(self, text='Download', state='disabled', style='Start.TButton',
                                          command=self.download)
        self.download_button.grid(column=1, row=0)

        # 'cancel button'
        self.cancel_button = ttk.Button(self, text='Cancel', state='disabled', command=self.cancel)
        self.cancel_button.grid(column=2, row=0)

        # 'url'
        self.url_label = ttk.Label(self, text='YouTube URL: ')
        self.url_label.grid(column=0, row=2, sticky=tk.E)
        self.url_entry = ttk.Entry(self, width=50, textvariable=self.yt_url)
        self.url_entry.grid(column=1, row=2, sticky=(tk.W, tk.E))
        self.yt_url.trace_add('write', self.toggle_check)
        # check_button = ttk.Button(mainframe, text='Check', state='disabled', command=partial(check, yt_url.get()))
        self.check_button = ttk.Button(self, text='Check', state='disabled',
                                       command=lambda: KThread(target=self.check, daemon=True).start())
        self.check_button.grid(column=2, row=2)

        # 'output dir'
        self.dir_label = ttk.Label(self, text='Output dir: ')
        self.dir_label.grid(column=0, row=3, sticky=tk.E)
        self.output_dir.set(str(Path.home()))
        self.dir_entry = ttk.Entry(self, width=50, textvariable=self.output_dir)
        self.dir_entry.grid(column=1, row=3, sticky=(tk.W, tk.E))
        self.dir_button = ttk.Button(self, text='Browse ...', command=self.select_dir)
        self.dir_button.grid(column=2, row=3)

        # 'file name'
        self.file_label = ttk.Label(self, text='File name: ')
        self.file_label.grid(column=0, row=4, sticky=tk.E)
        self.file_entry = ttk.Entry(self, width=50, textvariable=self.output_file)
        self.file_entry.grid(column=1, row=4, sticky=(tk.W, tk.E))

        # 'streams tree'
        self.tree_abel = ttk.Label(self, text='Quality options: ')
        self.tree_abel.grid(column=0, row=8, sticky=(tk.N, tk.E))
        self.treeframe = ttk.Frame(self)
        self.treeframe.grid(column=1, row=8, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S), pady=5)
        tree_columns = ['itag', 'type', 'quality', 'size']
        self.streams_tree = ttk.Treeview(self.treeframe, columns=tree_columns, height=5, padding=5, selectmode='browse')
        self.streams_tree.column('#0', stretch=tk.NO, width=0, minwidth=0)
        self.streams_tree.column('itag', width=50, minwidth=40, anchor='e')
        self.streams_tree.column('type', width=100, minwidth=60, anchor='e')
        self.streams_tree.column('quality', width=100, minwidth=60, anchor='e')
        self.streams_tree.column('size', width=150, minwidth=100, anchor='e')
        self.streams_tree.heading('itag', text='itag', anchor='e')
        self.streams_tree.heading('type', text='File type', anchor='e')
        self.streams_tree.heading('quality', text='Quality', anchor='e')
        self.streams_tree.heading('size', text='Size [MB]', anchor='e')
        self.streams_tree.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.s = ttk.Scrollbar(self.treeframe, orient=tk.VERTICAL, command=self.streams_tree.yview)
        self.s.grid(column=1, row=0, sticky=(tk.N, tk.S))
        self.streams_tree['yscrollcommand'] = self.s.set
        self.treeframe.grid_columnconfigure(0, weight=1)
        self.treeframe.grid_rowconfigure(0, weight=1)
        self.streams_tree.bind('<<TreeviewSelect>>', self.itag_select)

        # 'File info'
        self.fileframe = ttk.Labelframe(self, text='File info', width=280)
        self.fileframe.grid(column=3, row=1, rowspan=9, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S), pady=5, padx=15)
        self.fileframe.grid_propagate(False)
        ttk.Label(self.fileframe, text='Title: ').grid(column=0, row=0, sticky=(tk.E), pady=5)
        ttk.Label(self.fileframe, textvariable=self.yt_title, wraplength=180).grid(column=1, row=0, sticky=(tk.W),
                                                                                   pady=5, padx=5)
        ttk.Label(self.fileframe, text='Author: ').grid(column=0, row=1, sticky=(tk.E), pady=5)
        ttk.Label(self.fileframe, textvariable=self.yt_author).grid(column=1, row=1, sticky=(tk.W), pady=5, padx=5)
        ttk.Label(self.fileframe, text='Length: ').grid(column=0, row=2, sticky=(tk.E), pady=5)
        ttk.Label(self.fileframe, textvariable=self.yt_length).grid(column=1, row=2, sticky=(tk.W), pady=5, padx=5)
        ttk.Label(self.fileframe, text='Thumbnail: ').grid(column=0, row=3, sticky=(tk.N, tk.E), pady=5)

        # 'separator'
        self.s = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.s.grid(column=0, row=9, columnspan=3, sticky=(tk.E, tk.W), pady=30, padx=15)

        # 'progressbar'
        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, variable=self.yt_current_size,
                                            mode='determinate')
        self.progress_bar.grid(column=0, row=10, columnspan=3, pady=5, padx=15, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.p_label = ttk.Label(self, text='0 MB')
        self.p_label.grid(column=3, row=10, pady=5, padx=15, sticky=(tk.N, tk.W, tk.E, tk.S))

        # 'status bar'
        ttk.Label(self, textvariable=self.status_text, anchor=(tk.W), relief=tk.SUNKEN).grid(column=0, row=11,
                                                                                             columnspan=5,
                                                                                             sticky=(tk.W, tk.E))

    def create_window_menu(self):
        self.menubar = tk.Menu(self.master, tearoff=0)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Output dir...', command=self.select_dir)
        self.filemenu.add_command(label='Check URL', state=tk.DISABLED, command=self.check)
        self.filemenu.add_command(label='Download', state=tk.DISABLED, command=self.download)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.master.destroy)
        self.menubar.add_cascade(label='File', menu=self.filemenu)

        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label='Paste URL', command=self.paste_url)
        self.menubar.add_cascade(label='Edit', menu=self.editmenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='About', command=lambda: AboutWindow(self.master))
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)

        self.master.config(menu=self.menubar)

    def create_contextual_menu(self):
        self.contmenu = tk.Menu(self.master, tearoff=0)
        self.contmenu.add_command(label='Paste URL', command=self.paste_url)
        if (self.master.tk.call('tk', 'windowingsystem') == 'aqua'):
            self.master.bind('<2>', lambda e: self.contmenu.post(e.x_root, e.y_root))
            self.master.bind('<Control-1>', lambda e: self.contmenu.post(e.x_root, e.y_root))
        else:
            self.master.bind('<3>', lambda e: self.contmenu.post(e.x_root, e.y_root))

    def create_bindings(self):
        self.master.bind('<Return>', self.download)

    def additional_styling(self):
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.url_entry.focus()
