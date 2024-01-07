"""
Отвечает за панель задач
"""

import json
from datetime import datetime
from tkinter import Canvas


class Taskbar:
    """
    Панель задач
    """

    def __init__(self, c: Canvas):
        """
        Создаёт панель задачь на хосте
        :param c: холст
        """

        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: taskbar_init_start\n')

        self.time_text_id: int = 0
        self.date_text_id: int = 0
        self.c: Canvas = c

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

        canvas_width: int = config['canvas_width']
        canvas_height: int = config['canvas_height']
        panel_h: int = config['panel_h']
        self.canvas_width: int = canvas_width
        self.canvas_height: int = canvas_height

        self.c.create_rectangle(0, 0, self.canvas_width,  # create taskbar
                                panel_h, fill='black', outline='grey')

        now: datetime = datetime.now()

        self.time_text_id: int = self.c.create_text(  # create time text
            canvas_width - 50, panel_h * 0.25, anchor='center',
            text=now.strftime('%H:%M'), fill='white')

        self.date_text_id: int = self.c.create_text(  # create date text
            canvas_width - 50, panel_h * 0.7, anchor='center',
            text=f"{Taskbar.weekday()} {now.strftime('%d.%m.%Y')}", fill='white')

        self.c.after(0, self.run_taskbar)

        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: taskbar_init_end\n')

    @staticmethod
    def weekday() -> str:
        """
        :return: день недели из списка Пн, Вт, Ср, Чт, Пт, Сб, Вс
        """
        n: int = datetime.weekday(datetime.now())
        return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][n]

    def run_taskbar(self) -> None:
        """
        Обрабатывает панель задач
        :return: None
        """
        now: datetime = datetime.now()

        self.c.itemconfig(self.time_text_id, text=now.strftime('%H:%M'))  # time
        self.c.itemconfig(self.date_text_id, text=f"{Taskbar.weekday()} {now.strftime('%d.%m.%Y')}")  # date

        self.c.after(1, self.run_taskbar)
