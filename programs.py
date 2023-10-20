"""
Модуль с программами.
Каждая программа - отдельный класс.

Для создания программы пишем:

class ИмяПрограмы(Program): # сосдаём класс

    def __init__(self, c: Canvas, root: Tk): # lоопределяем метод __init__
        super().__init__(c, root)
        self.icon_image = tkinter.PhotoImage(file='путь/до/изображния.gif')

    @staticmethod
    def open() -> None:
        # код прои открытии

"""

import tkinter
import json
from pynput.keyboard import Key, Controller
from tkinter import Canvas, Tk, PhotoImage, Button, Menu, Toplevel, Label
from abc import ABC, abstractmethod


class Program(ABC):
    """
    Абстрактный класс для создания программ
    """

    @abstractmethod
    def __init__(self, c: Canvas, root: Tk) -> None:
        r"""
        Абстрактный метод создания программы.
        Необгодимо изменить self.icon_image на tkinter.PhotoImage(file='путь\до\изображения.gif')
        :param c: холст
        :param root: окно
        """
        self.c: Canvas = c
        self.root: Tk = root
        self.is_create: bool = False
        self.icon_image: PhotoImage = tkinter.PhotoImage(file='')
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
        # global icon_shift
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
        self.icon_image = tkinter.PhotoImage(file='imgs/about/about.gif')

    @staticmethod
    def open() -> None:
        _root: Toplevel = tkinter.Toplevel()
        _root.geometry('250x150')
        _root.iconbitmap('imgs/about/about.ico')
        _root.title('Приступая к работе')
        text: Label = tkinter.Label(_root, text='''
        Опирационая система vladOS.
        
        Для перезагруски и гибернации
        нажмите правой кнопкой мышы
        по кнопке питания.
        
        Дальше рабирайтесь сами.
        ''')
        text.pack()
        _root.mainloop()


class Prog(Program):
    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = tkinter.PhotoImage(file='imgs/hw/HW.gif')

    @staticmethod
    def open() -> None:
        _root: Toplevel = tkinter.Toplevel()
        _root.geometry('170x100')
        _root.iconbitmap('imgs/hw/HW.ico')
        _root.title('HW')
        text: Label = tkinter.Label(_root, text='hello world')
        text.pack()
        _root.mainloop()


class ControlPanel(Program):

    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = tkinter.PhotoImage(file='imgs/control_panel/control_panel.gif')

    def open(self) -> None:
        _root: Toplevel = tkinter.Toplevel()
        _root.geometry('250x80')
        _root.iconbitmap('imgs/control_panel/control_panel.ico')
        _root.title('Панель управления')

        for r in range(3):
            _root.grid_rowconfigure(r, weight=1)

        for c in range(2):
            _root.grid_columnconfigure(c, weight=1)

        tkinter.Button(_root, text='Мышь', command=self.open_mouse_menu).grid(row=0, column=0, sticky='NSEW')
        tkinter.Button(_root, text='Завершение работы', command=Power.shutdown, ) \
            .grid(row=1, column=0, sticky='NSEW')
        tkinter.Button(_root, text='Скрин шот', command=ControlPanel.screen_shot) \
            .grid(row=0, column=1, sticky='NSEW')
        tkinter.Button(_root, text='Приступая к работе', command=About.open) \
            .grid(row=1, column=1, sticky='NSEW')
        tkinter.Button(_root, text='Компаненты', command=self.open_modul_menu) \
            .grid(row=2, column=0, sticky='NSEW')
        tkinter.Button(_root, text='Звук', command=self.open_sound_menu).grid(row=2, column=1, sticky='NSEW')

        _root.mainloop()

    @staticmethod
    def screen_shot() -> None:
        keyboard: Controller = Controller()
        keyboard.press(Key.cmd)  # win
        keyboard.press(Key.print_screen)
        keyboard.release(Key.print_screen)
        keyboard.release(Key.cmd)

    def open_mouse_menu(self) -> None:
        _root: Toplevel = tkinter.Toplevel()
        _root.geometry('300x100')
        _root.iconbitmap('imgs/control_panel/control_panel.ico')
        _root.title('Мышь')

        for r in range(4):
            _root.grid_rowconfigure(r, weight=1)

        for c in range(4):
            _root.grid_columnconfigure(c, weight=1)

        tkinter.Button(_root, text='Сделать курсор по умолчанию', command=lambda: self.root.config(cursor='arrow')) \
            .grid(row=0, column=0, columnspan=2, sticky='NSEW')
        tkinter.Button(_root, text='Сделать курсор рука-курсор', command=lambda: self.root.config(cursor='hand2')) \
            .grid(row=1, column=0, columnspan=2, sticky='NSEW')

        tkinter.Label(_root, text='Свой курсор').grid(row=0, column=2, columnspan=2, sticky='NSEW')
        entry = tkinter.Entry(_root)
        entry.grid(row=1, column=2, columnspan=2, sticky='NSEW')

        tkinter.Button(_root, text='Man', command=lambda: self.root.config(cursor='man')) \
            .grid(row=2, column=0, sticky='NSEW')
        tkinter.Button(_root, text='Star', command=lambda: self.root.config(cursor='star')) \
            .grid(row=2, column=1, sticky='NSEW')
        tkinter.Button(_root, text='Plus', command=lambda: self.root.config(cursor='plus')) \
            .grid(row=2, column=2, sticky='NSEW')
        tkinter.Button(_root, text='Cross', command=lambda: self.root.config(cursor='cross')) \
            .grid(row=2, column=3, sticky='NSEW')
        tkinter.Button(_root, text='Circle', command=lambda: self.root.config(cursor='circle')) \
            .grid(row=3, column=0, sticky='NSEW')
        tkinter.Button(_root, text='Dot', command=lambda: self.root.config(cursor='dot')) \
            .grid(row=3, column=1, sticky='NSEW')
        tkinter.Button(_root, text='Target', command=lambda: self.root.config(cursor='target')) \
            .grid(row=3, column=2, sticky='NSEW')
        tkinter.Button(_root, text='Hand1', command=lambda: self.root.config(cursor='hand1')) \
            .grid(row=3, column=3, sticky='NSEW')

        entry.bind('<Return>', lambda event: self.root.config(cursor=entry.get()))

        _root.mainloop()

    @staticmethod
    def open_modul_menu() -> None:
        _root: Toplevel = tkinter.Toplevel()
        _root.geometry('150x150')
        _root.iconbitmap('imgs/control_panel/control_panel.ico')
        _root.title('Компаненты')

        for c in range(1):
            _root.grid_columnconfigure(c, weight=1)

        for r in range(9):
            _root.grid_rowconfigure(r, weight=1)

        tkinter.Label(_root, text='Vlad desktop background').grid(row=0, column=0, sticky='w')
        tkinter.Label(_root, text='Vlad taskbar').grid(row=1, column=0, sticky='w')
        tkinter.Label(_root, text='Vlad main context menu').grid(row=2, column=0, sticky='w')
        tkinter.Label(_root, text='About').grid(row=3, column=0, sticky='w')
        tkinter.Label(_root, text='Control Panel').grid(row=4, column=0, sticky='w')
        tkinter.Label(_root, text='HW').grid(row=5, column=0, sticky='w')
        tkinter.Label(_root, text='Pentagon').grid(row=6, column=0, sticky='w')
        tkinter.Label(_root, text='vlad log in').grid(row=7, column=0, sticky='w')
        tkinter.Label(_root, text='vlad create new user manager').grid(row=8, column=0, sticky='w')

        _root.mainloop()

    @staticmethod
    def open_sound_menu() -> None:
        _root: Toplevel = tkinter.Toplevel()
        _root.geometry('150x75')
        _root.iconbitmap('imgs/control_panel/control_panel.ico')
        _root.title('Рабочий стол')

        _root.grid_columnconfigure(0, weight=1)
        for r in range(3):
            _root.grid_rowconfigure(r, weight=1)

        tkinter.Button(_root, text='Прибавить звук',
                       command=ControlPanel.sound_up).grid(row=0, column=0, sticky='NSEW')
        tkinter.Button(_root, text='Уменьшить звук',
                       command=ControlPanel.sound_down).grid(row=1, column=0, sticky='NSEW')
        tkinter.Button(_root, text='Выключить звук',
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
        self.icon_image: PhotoImage = tkinter.PhotoImage(file='imgs/shut_down/Shutdown.gif')

    def create_link(self, x, y) -> None:
        button: Button = tkinter.Button(height=icon_size, width=icon_size, image=self.icon_image, command=self.shutdown)
        self.c.create_window(x, y, height=icon_size, width=icon_size, anchor='sw', window=button)
        menu = tkinter.Menu(tearoff=0)
        # menu.add_command(label='Сон', command=self.sleep)
        menu.add_command(label='Перезагрузка', command=self.restart)
        menu.add_command(label='Гибернация', command=self.hibernation)
        button.bind('<Button-3>', lambda event: menu.post(event.x_root, event.y_root))

    @staticmethod
    def open() -> None:
        Power.shutdown()

    @staticmethod
    def shutdown() -> None:
        os.system('shutdown /p')

    @staticmethod
    def sleep() -> None:
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
        self.icon_image = tkinter.PhotoImage(file='imgs/penta/pentagon.gif')

    @staticmethod
    def open() -> None:
        import pentagon
        pentagon.start()


class Cmd(Program):
    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = tkinter.PhotoImage(file='imgs/cmd/cmd.gif')

    @staticmethod
    def open() -> None:
        import cmd
        cmd.start()


class Word(Program):
    def __init__(self, c: Canvas, root: Tk):
        super().__init__(c, root)
        self.icon_image = tkinter.PhotoImage(file='imgs/word/word.gif')

    @staticmethod
    def open():
        import word
        word.start()


with open("config.json") as config_file:
    config = json.load(config_file)

canvas_height: int = config['canvas_height']
icon_size: int = config['panel_h']
icon_pos = set()  # координата x иконок
