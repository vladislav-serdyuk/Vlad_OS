"""
Создаёт, инецеалезирует и обрабатывает окно с псевдо-опеционой системой
"""

import json
import tkinter as tk
import tkinter
from tkinter import Tk, Canvas, messagebox, ttk
from datetime import datetime

from desktop import Desktop
from taskbar import Taskbar
from programs import Power
from log_in import LogIn


class VladOSApp(Tk):
    def __init__(self):
        super().__init__()
        # self.overrideredirect(True)  # delete - o x
        self.state('zoomed')  # full screen
        self.title('vladOS')
        self.iconbitmap('icon_os.ico')

        self.protocol('WM_DELETE_WINDOW', self.delete_window)
        with open("config.json") as config_file:
            config = json.load(config_file)

        self.canvas: Canvas = Canvas(self, width=config['canvas_width'],
                                     height=config['canvas_height'])  # создание холста
        self.canvas.pack(side="left", fill="both", expand=True)

        # self.scroll_x = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        # self.scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL)
        # self.scroll_x.pack(side="right", fill="x")
        # self.scroll_y.pack(side="right", fill="y")
        #
        # self.canvas.config(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        # self.scroll_x.config(command=self.canvas.xview)
        # self.scroll_y.config(command=self.canvas.yview)

        try:
            self.desktop = Desktop(self.canvas)
            Taskbar(self.canvas)
            self.power_button = Power(self.canvas, self)
            self.power_button.create_link_on_task_bar()
        except Exception as e:  # error_handler
            with open('log.txt', 'a') as file:
                _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                file.write(f'{_date}: initSystem: {e}\n')
            exit()

        LogIn(self, self.canvas)  # login

        # self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def delete_window(self) -> None:
        """
        Новый протокол закрытия.
        Спрашевает перед закрытием.
        :return: None
        """
        _ask: bool = messagebox.askyesno('Exiting', 'Exit?')
        if _ask:
            self.destroy()
