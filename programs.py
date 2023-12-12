"""
Модуль с программами.
Каждая программа - отдельный класс.

Для создания программы пишем:

class ProgName(Program): # сосдаём класс

    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = ImageTk.PhotoImage(Image.open('path/to/image.png').resize((icon_size, icon_size)))

    @staticmethod
    def open() -> None:
        # код при открытии

"""

import tkinter
import os
from tkinter import ttk
import json
from pynput.keyboard import Key, Controller
from tkinter import Canvas, Tk, PhotoImage, Button, Menu, Toplevel, Label, simpledialog
from abc import ABC, abstractmethod
from PIL import Image, ImageTk
import win32gui
import win32ui
import win32api
import win32con


class Program(ABC):
    """
    Абстрактный класс для создания программ
    """

    @abstractmethod
    def __init__(self, c: Canvas, root: Tk) -> None:
        r"""
        Абстрактный метод создания программы.
        Необгодимо изменить self.icon_image на tkinter.PhotoImage(file='path\to\image.gif')
        :param c: холст
        :param root: окно
        :return None
        """
        self.c: Canvas = c
        self.root: Tk = root
        self.is_create: bool = False
        # self.icon_image: PhotoImage = ImageTk.PhotoImage(Image.open('').resize((icon_size, icon_size)))
        self.icon_pos_x = None

    def create_link(self, x: float, y: float) -> None:
        """
        Создание ярлыка на координатах x и y
        :param x: x
        :param y: y
        :return: None
        """
        button: Button = tkinter.Button(height=icon_size, width=icon_size, image=self.icon_image, command=self.open)
        link_id: int = self.c.create_window(x, y, height=icon_size, width=icon_size, anchor='sw', window=button)
        menu: Menu = tkinter.Menu(tearoff=0)
        menu.add_command(label='Удалить', command=lambda: self.delete_link(link_id))
        button.bind('<Button-3>', lambda event: menu.post(event.x_root, event.y_root))
        self.is_create = True

    def delete_link(self, link_id: int) -> None:
        """
        Удоляет ярлык
        :param link_id: индефикатор ссылки
        :return: None
        """
        self.c.delete(link_id)
        self.is_create = False
        icon_pos.remove(self.icon_pos_x)

    def create_link_on_task_bar(self) -> None:
        """
        Создание ярлыка на панели задач
        :return: None
        """
        if not self.is_create:
            pos = 0
            while True:  # перебор позицый иконки
                if pos not in icon_pos:  # берём не занятую
                    self.create_link(pos, canvas_height)
                    icon_pos.add(pos)  # добавляем в список позицый
                    self.icon_pos_x = pos
                    return
                pos += icon_size

    @staticmethod
    @abstractmethod
    def open() -> None:
        """
        Открытие программы
        :return: None
        """


class About(Program):

    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = ImageTk.PhotoImage(Image.open('imgs/about/about.png').resize((icon_size, icon_size)))

    @staticmethod
    def open() -> None:
        _root: Toplevel = tkinter.Toplevel()
        _root.geometry('250x150')
        _root.iconbitmap('imgs/about/about.ico')
        _root.title('Getting started')
        text: Label = ttk.Label(_root, text='''
        Опирационая система vladOS.
        
        Для перезагруски и гибернации
        нажмите правой кнопкой мышы
        по кнопке питания
        
        Дальше рабирайтесь сами :)
        ''')
        text.pack()
        _root.mainloop()


class Prog(Program):
    """
    debug prog
    """

    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = ImageTk.PhotoImage(Image.open('imgs/hw/HW.png').resize((icon_size, icon_size)))

    @staticmethod
    def open() -> None:
        _root: Toplevel = tkinter.Toplevel()
        _root.geometry('170x100')
        _root.iconbitmap('imgs/hw/HW.ico')
        _root.title('HW')
        text: Label = ttk.Label(_root, text='hello world')
        text.pack()
        _root.mainloop()


class ControlPanel(Program):

    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = ImageTk.PhotoImage(Image.open('imgs/control_panel/control_panel.png')
                                             .resize((icon_size, icon_size)))

    def open(self) -> None:
        _root: Toplevel = tkinter.Toplevel()
        _root.geometry('250x80')
        _root.iconbitmap('imgs/control_panel/control_panel.ico')
        _root.title('Control panel')

        for r in range(3):
            _root.grid_rowconfigure(r, weight=1)

        for c in range(2):
            _root.grid_columnconfigure(c, weight=1)

        ttk.Button(_root, text='Mouse', command=self.open_mouse_menu).grid(row=0, column=0, sticky='NSEW')
        ttk.Button(_root, text='Shutdown', command=Power.shutdown, ) \
            .grid(row=1, column=0, sticky='NSEW')
        ttk.Button(_root, text='Screenshot', command=ControlPanel.screenshot) \
            .grid(row=0, column=1, sticky='NSEW')
        ttk.Button(_root, text='Getting started', command=About.open) \
            .grid(row=1, column=1, sticky='NSEW')
        ttk.Button(_root, text='Components', command=self.open_modul_menu) \
            .grid(row=2, column=0, sticky='NSEW')
        ttk.Button(_root, text='Sound', command=self.open_sound_menu).grid(row=2, column=1, sticky='NSEW')

        _root.mainloop()

    @staticmethod
    def screenshot() -> None:
        keyboard: Controller = Controller()
        keyboard.press(Key.cmd)  # win
        keyboard.press(Key.print_screen)
        keyboard.release(Key.print_screen)
        keyboard.release(Key.cmd)

    def open_mouse_menu(self) -> None:
        _root: Toplevel = tkinter.Toplevel()
        _root.geometry('300x100')
        _root.iconbitmap('imgs/control_panel/control_panel.ico')
        _root.title('Mouse')

        for r in range(4):
            _root.grid_rowconfigure(r, weight=1)

        for c in range(4):
            _root.grid_columnconfigure(c, weight=1)

        ttk.Button(_root, text='Set default cursor', command=lambda: self.root.config(cursor='arrow')) \
            .grid(row=0, column=0, columnspan=2, sticky='NSEW')
        ttk.Button(_root, text='Set hand2 cursor', command=lambda: self.root.config(cursor='hand2')) \
            .grid(row=1, column=0, columnspan=2, sticky='NSEW')

        ttk.Label(_root, text='Other cursor').grid(row=0, column=2, columnspan=2, sticky='NSEW')
        entry = ttk.Entry(_root)
        entry.grid(row=1, column=2, columnspan=2, sticky='NSEW')

        ttk.Button(_root, text='Man', command=lambda: self.root.config(cursor='man')) \
            .grid(row=2, column=0, sticky='NSEW')
        ttk.Button(_root, text='Star', command=lambda: self.root.config(cursor='star')) \
            .grid(row=2, column=1, sticky='NSEW')
        ttk.Button(_root, text='Plus', command=lambda: self.root.config(cursor='plus')) \
            .grid(row=2, column=2, sticky='NSEW')
        ttk.Button(_root, text='Cross', command=lambda: self.root.config(cursor='cross')) \
            .grid(row=2, column=3, sticky='NSEW')
        ttk.Button(_root, text='Circle', command=lambda: self.root.config(cursor='circle')) \
            .grid(row=3, column=0, sticky='NSEW')
        ttk.Button(_root, text='Dot', command=lambda: self.root.config(cursor='dot')) \
            .grid(row=3, column=1, sticky='NSEW')
        ttk.Button(_root, text='Target', command=lambda: self.root.config(cursor='target')) \
            .grid(row=3, column=2, sticky='NSEW')
        ttk.Button(_root, text='Hand1', command=lambda: self.root.config(cursor='hand1')) \
            .grid(row=3, column=3, sticky='NSEW')

        entry.bind('<Return>', lambda event: self.root.config(cursor=entry.get()))

        _root.mainloop()

    @staticmethod
    def open_modul_menu() -> None:
        _root: Toplevel = tkinter.Toplevel()
        _root.geometry('150x150')
        _root.iconbitmap('imgs/control_panel/control_panel.ico')
        _root.title('Components')

        for c in range(1):
            _root.grid_columnconfigure(c, weight=1)

        for r in range(9):
            _root.grid_rowconfigure(r, weight=1)

        ttk.Label(_root, text='Desktop').grid(row=0, column=0, sticky='w')
        ttk.Label(_root, text='Taskbar').grid(row=1, column=0, sticky='w')
        ttk.Label(_root, text='Main context menu').grid(row=2, column=0, sticky='w')
        ttk.Label(_root, text='About').grid(row=3, column=0, sticky='w')
        ttk.Label(_root, text='Control Panel').grid(row=4, column=0, sticky='w')
        ttk.Label(_root, text='HW').grid(row=5, column=0, sticky='w')
        ttk.Label(_root, text='Pentagon').grid(row=6, column=0, sticky='w')
        ttk.Label(_root, text='Log in manager').grid(row=7, column=0, sticky='w')
        ttk.Label(_root, text='Create new user manager').grid(row=8, column=0, sticky='w')

        _root.mainloop()

    @staticmethod
    def open_sound_menu() -> None:
        _root: Toplevel = tkinter.Toplevel()
        _root.geometry('150x75')
        _root.iconbitmap('imgs/control_panel/control_panel.ico')
        _root.title('Sound')

        _root.grid_columnconfigure(0, weight=1)
        for r in range(3):
            _root.grid_rowconfigure(r, weight=1)

        ttk.Button(_root, text='Up sound',
                   command=ControlPanel.sound_up).grid(row=0, column=0, sticky='NSEW')
        ttk.Button(_root, text='Down sound',
                   command=ControlPanel.sound_down).grid(row=1, column=0, sticky='NSEW')
        ttk.Button(_root, text='Mute sound',
                   command=ControlPanel.sound_mute).grid(row=2, column=0, sticky='NSEW')
        _root.mainloop()

    @staticmethod
    def sound_up() -> None:
        keyboard = Controller()
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)

    @staticmethod
    def sound_down() -> None:
        keyboard = Controller()
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)

    @staticmethod
    def sound_mute() -> None:
        keyboard = Controller()
        keyboard.press(Key.media_volume_mute)
        keyboard.release(Key.media_volume_mute)


class Power(Program):
    def __init__(self, c: Canvas, root: Tk) -> None:
        super().__init__(c, root)
        self.icon_image: PhotoImage = ImageTk.PhotoImage(Image.open('imgs/shut_down/Shutdown.png')
                                                         .resize((icon_size, icon_size)))

    def create_link(self, x, y) -> None:
        button: Button = tkinter.Button(height=icon_size, width=icon_size, image=self.icon_image, command=self.shutdown)
        self.c.create_window(x, y, height=icon_size, width=icon_size, anchor='sw', window=button)
        menu = tkinter.Menu(tearoff=0)
        # menu.add_command(label='Сон', command=self.sleep)
        menu.add_command(label='Reboot', command=self.restart)
        menu.add_command(label='Hibernation', command=self.hibernation)
        button.bind('<Button-3>', lambda event: menu.post(event.x_root, event.y_root))

    @staticmethod
    def open() -> None:
        Power.shutdown()

    @staticmethod
    def shutdown() -> None:
        os.system('shutdown /p')

    @staticmethod
    def sleep() -> None:  # in developering
        os.system('rundll32.exe powrprof.dll,SetSuspendState Stadby')

    @staticmethod
    def restart() -> None:
        os.system('shutdown /r /t')

    @staticmethod
    def hibernation() -> None:
        os.system('shutdown /h')


class Pentagon(Program):
    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = ImageTk.PhotoImage(Image.open('imgs/penta/pentagon.png').resize((icon_size, icon_size)))

    @staticmethod
    def open() -> None:
        import pentagon
        pentagon.start()


class Cmd(Program):
    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = ImageTk.PhotoImage(Image.open('imgs/cmd/cmd.png').resize((icon_size, icon_size)))

    @staticmethod
    def open() -> None:
        import cmd
        cmd.start()


class Word(Program):
    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = ImageTk.PhotoImage(Image.open('imgs/word/word.png').resize((icon_size, icon_size)))

    @staticmethod
    def open():
        import word
        word.start()


class Link(Program):
    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = ImageTk.PhotoImage(Image.open('imgs/default.png').resize((icon_size, icon_size)))
        self.obj = ''
        self.link_id = 0

    def create_link(self, x: float, y: float):
        """
        Создание ярлыка на координатах x и y
        :param x: x
        :param y: y
        :return: None
        """
        self.obj = simpledialog.askstring('Creating link', 'Entry object name')
        if self.obj == '':
            return
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
        try:
            large, small = win32gui.ExtractIconEx(self.obj, 0)
            win32gui.DestroyIcon(small[0])

            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
            hbmp = win32ui.CreateBitmap()
            hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
            hdc = hdc.CreateCompatibleDC()

            hdc.SelectObject(hbmp)
            hdc.DrawIcon((0, 0), large[0])
            # print(hbmp.GetBitmapBits())
            img = Image.new('RGBA', (32, 32))
            # print(len(hbmp.GetBitmapBits()))
            data_row = hbmp.GetBitmapBits()
            # print(data_row)
            data_a = list(map(lambda item: item if item >= 0 else 256 + item, data_row[::4]))
            # data_a = list(map(lambda item: 255, data_row[::4]))
            data_g = list(map(lambda item: item if item >= 0 else 256 + item, data_row[1::4]))
            data_r = list(map(lambda item: item if item >= 0 else 256 + item, data_row[2::4]))
            data_b = list(map(lambda item: item if item >= 0 else 256 + item, data_row[3::4]))
            # print(list(zip(data_r, data_g, data_b, data_a)))
            img.putdata(list(zip(data_r, data_g, data_b, data_a)))
            # img = Image.frombuffer('RGB', (icon_size, icon_size),
            #                        hbmp.GetBitmapBits())
            self.icon_image = ImageTk.PhotoImage(img.resize((icon_size, icon_size)))
        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')
        # self.icon_image = ImageTk.PhotoImage(Image.fromhandle(large[0]).resize((icon_size, icon_size)))
        button: Button = tkinter.Button(height=icon_size, width=icon_size, image=self.icon_image, command=self.open)
        self.link_id: int = self.c.create_window(x, y, height=icon_size, width=icon_size, anchor='sw', window=button)
        menu: Menu = tkinter.Menu(tearoff=0)
        menu.add_command(label='Удалить', command=lambda: self.delete_link(self.link_id))
        button.bind('<Button-3>', lambda event: menu.post(event.x_root, event.y_root))

    def open(self) -> None:
        import os
        os.popen(self.obj)


try:
    with open("config.json") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    config = {
        "canvas_width": 1600,
        "canvas_height": 900,
        "panel_h": 40,
        "background": "imgs/desktop/desktop2.png"
    }

canvas_height: int = config['canvas_height']
icon_size: int = config['panel_h']
icon_pos = set()  # координата x иконок
