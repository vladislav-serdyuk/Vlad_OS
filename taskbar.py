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
        self.time_text_id: int = 0
        self.date_text_id: int = 0
        self.c: Canvas = c

        with open("config.json") as config_file:
            config = json.load(config_file)

        canvas_width: int = config['canvas_width']
        canvas_height: int = config['canvas_height']
        panel_h: int = config['panel_h']
        self.canvas_width: int = canvas_width
        self.canvas_height: int = canvas_height

        self.c.create_rectangle(0, self.canvas_height - panel_h, self.canvas_width,  # create taskbar
                                self.canvas_height, fill='black', outline='grey')

        now: datetime = datetime.now()

        self.time_text_id: int = self.c.create_text(  # create time text
            canvas_width - 50, canvas_height - panel_h * 0.75, anchor='center',
            text=now.strftime('%H:%M'), fill='white')

        self.date_text_id: int = self.c.create_text(  # create date text
            canvas_width - 50, canvas_height - panel_h * 0.3, anchor='center',
            text=f"{Taskbar.weekday()} {now.strftime('%d.%m.%Y')}", fill='white')

        self.c.after(0, self.run_taskbar)

    @staticmethod
    def weekday() -> str:
        """
        :return: день недели из списка Пн, Вт, Ср, Чт, Пт, Сб, Вс
        """
        n: int = datetime.weekday(datetime.now())
        return ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'][n]

    def run_taskbar(self) -> None:
        """
        Обрабатывает панель задач
        :return: None
        """
        now: datetime = datetime.now()

        self.c.itemconfig(self.time_text_id, text=now.strftime('%H:%M'))  # time
        self.c.itemconfig(self.date_text_id, text=f"{Taskbar.weekday()} {now.strftime('%d.%m.%Y')}")  # date

        self.c.after(1, self.run_taskbar)
