"""
Основное контекстное меню
"""

from tkinter import Menu, Canvas, Tk, Event
from datetime import datetime
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
        except Exception as e:  # error_handler
            with open('log.txt', 'a') as file:
                _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                file.write(f'{_date}: initModuls: {e}\n')
            return

        self.menu.add_command(label='Открыть панель управления', command=control_panel.open)
        self.menu.add_command(label='Открыть приложение "О программе"', command=about.open)
        self.menu.add_command(label='Открыть командную строку', command=cmd.open)
        self.menu.add_command(label='Открыть Word', command=word.open)

        self.menu.add_separator()

        self.menu.add_command(label='Создать ярлык приложения "Панель управления"',
                              command=control_panel.create_link_on_task_bar)
        self.menu.add_command(label='Создать ярлык приложения "О программе"', command=about.create_link_on_task_bar)
        self.menu.add_command(label='Создать ярлык приложения "Командная строка"', command=cmd.create_link_on_task_bar)
        self.menu.add_command(label='Создать приложение "Word"',
                              command=word.create_link_on_task_bar)
        self.menu.add_command(label='создать ярлык приложения', command=prog.create_link_on_task_bar)
        self.menu.add_command(label='Создать ярлык приложения "взлом пентагона"',
                              command=pentagon.create_link_on_task_bar)

    def popup(self, event: Event) -> None:
        """
        Открытие контекстного меню
        :param event: событее
        :return: None
        """
        self.menu.post(event.x_root, event.y_root)

    # def error_handler(self, command:):
