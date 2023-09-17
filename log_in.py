import tkinter

from desktop import Desktop
from taskbar import Taskbar
from menu import MainMenu
from programs import Power
from tkinter import Tk, Canvas, messagebox
from create_new_user_manager import NewUser
import json


class LogIn:
    def __init__(self, root: Tk, c: Canvas):
        self.c = c
        self.root = root

        try:
            with open('user_config.json') as file:
                self.config = json.load(file)
        except FileNotFoundError:
            NewUser()
            # self.log_in()
        else:
            self._root = tkinter.Toplevel(root)
            self._root.title('Log in manager')

            for r in range(3):
                self._root.grid_rowconfigure(r, weight=1)

            for c in range(3):
                self._root.grid_columnconfigure(c, weight=1)

            tkinter.Label(self._root, text='Name').grid(column=0, row=0)
            self.name_label = tkinter.Label(self._root, text=self.config['name'])
            self.name_label.grid(column=1, row=0, columnspan=2)
            tkinter.Label(self._root, text='Password').grid(column=0, row=1)
            self.password_entry = tkinter.Entry(self._root)
            self.password_entry.grid(column=1, row=1, columnspan=2, sticky='NSEW')
            tkinter.Button(self._root, text='Log in', command=self.authentication).grid(column=2, row=2, sticky='NSEW')

    def authentication(self):
        if self.password_entry.get() == self.config['password']:
            self._root.destroy()
            self.log_in()
        else:
            messagebox.showwarning('Password incorrect', 'Password incorrect')

    def log_in(self):
        c = self.c
        root = self.root
        try:
            Taskbar(c)
            menu: MainMenu = MainMenu(c, root)
            power_button: Power = Power(c, root)

            power_button.create_on_task_bar()
        except Exception as e:  # error_handler
            with open('log.txt', 'a') as file:
                _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                file.write(f'{_date}: initSystem: {e}\n')
            exit()

        c.bind('<Button-3>', menu.popup)

        try:
            root.mainloop()
        except Exception as e:  # error_handler
            with open('log.txt', 'a') as file:
                _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                file.write(f'{_date}: procession: {e}\n')
            exit()
