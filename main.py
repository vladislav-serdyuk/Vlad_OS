"""
Создаёт, инецеалезирует и обрабатывает окно с псевдо-опеционой системой
"""

import json
from tkinter import Tk, Canvas, messagebox
from datetime import datetime

from desktop import Desktop
from taskbar import Taskbar
from programs import Power
from log_in import LogIn


def delete_window() -> None:
    """
    Новый протокол закрытия.
    Спрашевает перед закрытием.
    :return: None
    """
    _ask: bool = messagebox.askyesno('Потверждение выхода из оболочки', 'Вы дествительно хотите выйти из оболочки?')
    if _ask:
        root.destroy()


if __name__ == '__main__':
    root: Tk = Tk()  # создание окна
    root.overrideredirect(True)  # delete - o x
    root.state('zoomed')  # full screen
    root.title('vladOS')
    root.iconbitmap('icon_os.ico')

    root.protocol('WM_DELETE_WINDOW', delete_window)

    with open("config.json") as config_file:
        config = json.load(config_file)
    c: Canvas = Canvas(root, width=config['canvas_width'], height=config['canvas_height'])  # создание холста
    c.pack()

    try:
        desktop = Desktop(c)
        Taskbar(c)
        power_button = Power(c, root)
        power_button.create_on_task_bar()
    except Exception as e:  # error_handler
        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: initSystem: {e}\n')
        exit()

    LogIn(root, c)  # login
    root.mainloop()
