import ctypes


def hide_console():
    """ Hides Windows console, instead of 'pyinstaller --windowed'"""
    # ctypes.windll.kernel32.FreeConsole()
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_HIDE = 0
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, SW_HIDE)
