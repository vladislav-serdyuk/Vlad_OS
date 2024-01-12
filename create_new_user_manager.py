import tkinter
from tkinter import ttk
import hashlib
from datetime import datetime


class NewUser:
    def __init__(self, root: tkinter.Tk):
        self.root = root
        self._root = tkinter.Toplevel(root)
        self._root.resizable(True, False)
        self._root.title('Create new user manager')

        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: newuser_init_start\n')

        for r in range(3):
            self._root.grid_rowconfigure(r, weight=1)

        for c in range(3):
            self._root.grid_columnconfigure(c, weight=1)

        ttk.Label(self._root, text='Name').grid(column=0, row=0)
        self.name_entry = ttk.Entry(self._root)
        self.name_entry.grid(column=1, row=0, columnspan=2, sticky='NSEW')
        ttk.Label(self._root, text='Password').grid(column=0, row=1)
        self.password_entry = ttk.Entry(self._root)
        self.password_entry.grid(column=1, row=1, columnspan=2, sticky='NSEW')
        ttk.Button(self._root, text='Create', command=self.create).grid(column=2, row=2, sticky='NSEW')

        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: newuser_init_end\n')

    def create(self):
        default_config = \
            '{\n' + \
            f'  "name": "{self.name_entry.get()}",\n' + \
            f'  "password_sha256": "{hashlib.sha256(self.password_entry.get().encode("utf-8")).hexdigest()}"\n' + \
            '}'
        with open('user_config.json', 'w') as file:
            file.write(default_config)
        self._root.destroy()

        with open('log.txt', 'a') as file:
            _date: str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            file.write(f'{_date}: INFO: newuser_create_user\n')
        self.root.restart()
