import tkinter
from tkinter import Tk, Canvas, messagebox, ttk
import json
import hashlib
import traceback
from datetime import datetime

from menu import MainMenu
from create_new_user_manager import NewUser


class LogIn:
    def __init__(self, root: Tk, c: Canvas):
        self.c = c
        self.root = root

        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: login_init_start\n')

        try:
            with open('user_config.json') as file:
                self.config = json.load(file)
        except FileNotFoundError:
            NewUser()
        else:
            self._root = tkinter.Toplevel(root)  # create login window
            self._root.resizable(True, False)
            self._root.title('Log in manager')

            for r in range(3):
                self._root.grid_rowconfigure(r, weight=1)

            for c in range(3):
                self._root.grid_columnconfigure(c, weight=1)

            ttk.Label(self._root, text='Name').grid(column=0, row=0)
            self.name_label = ttk.Label(self._root, text=self.config['name'])
            self.name_label.grid(column=1, row=0, columnspan=2)
            ttk.Label(self._root, text='Password').grid(column=0, row=1)
            self.password_entry = ttk.Entry(self._root)
            self.password_entry.grid(column=1, row=1, columnspan=2, sticky='NSEW')
            ttk.Button(self._root, text='Log in', command=self.authentication).grid(column=2, row=2, sticky='NSEW')
            with open('log.txt', 'a') as file:
                _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                file.write(f'{_date}: INFO: login_init_end\n')

    def authentication(self):
        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: authentication_start\n')
        if hashlib.sha256(self.password_entry.get().encode('utf-8')).hexdigest() == self.config['password_sha256']:
            with open('log.txt', 'a') as file:
                _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                file.write(f'{_date}: INFO: authentication_good\n')
            self._root.destroy()
            self.log_in()
        else:
            with open('log.txt', 'a') as file:
                _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                file.write(f'{_date}: INFO: authentication_no\n')
            messagebox.showwarning('Password incorrect', 'Password incorrect')

    def log_in(self):
        c = self.c
        root = self.root
        try:
            menu: MainMenu = MainMenu(c, root)
        except Exception:  # error_handler
            with open('log.txt', 'a') as file:
                _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                file.write(f'{_date}: ERROR:\n{traceback.format_exc()}\n')
            exit()

        c.bind('<Button-3>', menu.popup)
