"""
Создаёт, инецеалезирует и обрабатывает окно с псевдо-опеционой системой
"""

import json
import os
import tkinter as tk
import tkinter
from tkinter import Tk, Canvas, messagebox, ttk
from datetime import datetime
import traceback

from desktop import Desktop
from taskbar import Taskbar
from programs import Power
from log_in import LogIn


class VladOSApp(Tk):
    def __init__(self):
        super().__init__()

        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: app_init_start\n')

        os.popen('taskkill /f /im explorer.exe')

        self.overrideredirect(True)  # delete - o x
        # self.state('zoomed')  # full screen
        self.title('vladOS')
        self.iconbitmap('icon_os.ico')

        self.protocol('WM_DELETE_WINDOW', self.delete_window)
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
        self.geometry(f'{config["canvas_width"]}x{config["panel_h"]}+0+{config["canvas_height"]-config["panel_h"]}')

        self.canvas: Canvas = Canvas(self, width=config['canvas_width'],
                                     height=config['panel_h'])  # создание холста
        self.canvas.pack()

        try:
            self.desktop = Desktop()
            Taskbar(self.canvas)
            self.power_button = Power(self.canvas, self)
            self.power_button.create_link_on_task_bar()
            LogIn(self, self.canvas)  # login
        except Exception:  # error_handler
            with open('log.txt', 'a') as file:
                _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                file.write(f'{_date}: ERROR:\n{traceback.format_exc()}\n')
            exit()

        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: app_init_end\n')

    def delete_window(self) -> None:
        """
        Новый протокол закрытия.
        Спрашевает перед закрытием.
        :return: None
        """
        _ask: bool = messagebox.askyesno('Exiting', 'Exit?')
        if _ask:
            with open('log.txt', 'a') as file:
                _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                file.write(f'{_date}: INFO: app_exit\n')
            os.popen('explorer')
            self.destroy()

    def restart(self):
        self.destroy()
        os.popen('restart.bat')
