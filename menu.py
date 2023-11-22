"""
Основное контекстное меню
"""

from tkinter import Menu, Canvas, Tk, Event
from datetime import datetime
import traceback

from programs import About, Prog, ControlPanel, Pentagon, Cmd, Word


class MainMenu:
    """
    Основное контекстное меню
    """

    def __init__(self, c: Canvas, root: Tk) -> None:
        """
        Создание основного контекстного меню
        :param c: холст
        :param root: окно
        """

        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: menu_init_start\n')

        self.menu: Menu = Menu(tearoff=0, background='#a24ead')

        def init(program):
            return program(c, root)

        try:
            about: About = init(About)
            prog: Prog = init(Prog)
            control_panel: ControlPanel = init(ControlPanel)
            pentagon: Pentagon = init(Pentagon)
            cmd: Cmd = init(Cmd)
            word: Word = init(Word)
        except Exception:  # error_handler
            with open('log.txt', 'a') as file:
                _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                file.write(f'{_date}: ERROR:\n{traceback.format_exc()}\n')
            exit()

        self.menu.add_command(label='Open Control panel', command=control_panel.open)
        self.menu.add_command(label='Open About', command=about.open)
        self.menu.add_command(label='Open Terminal', command=cmd.open)
        self.menu.add_command(label='Open Word', command=word.open)

        self.menu.add_separator()

        self.menu.add_command(label='Place on taskbar Control panel',
                              command=control_panel.create_link_on_task_bar)
        self.menu.add_command(label='Place on taskbar About', command=about.create_link_on_task_bar)
        self.menu.add_command(label='Place on taskbar Terminal', command=cmd.create_link_on_task_bar)
        self.menu.add_command(label='Place on taskbar Word', command=word.create_link_on_task_bar)
        self.menu.add_command(label='Place on taskbar HW', command=prog.create_link_on_task_bar)
        self.menu.add_command(label='Place on taskbar "Взлом пентагона"',
                              command=pentagon.create_link_on_task_bar)

        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: menu_init_end\n')

    def popup(self, event: Event) -> None:
        """
        Открытие контекстного меню
        :param event: событее
        :return: None
        """
        self.menu.post(event.x_root, event.y_root)
