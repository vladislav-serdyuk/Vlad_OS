"""
Модуль отвечающий за рабочий стол
"""

import json
from tkinter import PhotoImage, Canvas
from datetime import datetime


class Desktop:
    """
    Рабочий стол.
    """

    def __init__(self, c: Canvas):
        """
        Создаёт рабочий стол на холсте.
        :param c: холст, на котором создаётся рабочий стол.
        """

        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: desktop_init_start\n')

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

        try:
            self.image: PhotoImage = PhotoImage(file=config['background'])
        except Exception as e:  # error_handler
            with open('log.txt', 'a') as file:
                _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                file.write(f'{_date}: failedToDesktopImage_theImageMayNotExist: {e}\n')
            exit(-1)

        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: desktop_init_end\n')

        c.create_image(0, 0, image=self.image, anchor='nw')
