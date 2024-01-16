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
import tkinter as tk
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
        self.icon_image: PhotoImage = ImageTk.PhotoImage(Image.open('imgs\\default.png').resize((icon_size, icon_size)))
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
                    self.create_link(pos, icon_size)
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
        os.popen('explorer Shell:::{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}')


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


class Taskmgr(Program):
    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = ImageTk.PhotoImage(Image.open('imgs\\taskmgr\\taskmgr.png').resize((icon_size, icon_size)))

    @staticmethod
    def open() -> None:
        os.popen('taskmgr')

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
