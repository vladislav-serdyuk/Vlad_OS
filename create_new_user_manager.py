import tkinter

import hashlib


class NewUser:
    def __init__(self):
        self.root = tkinter.Toplevel()
        self.root.title('Create new user manager')

        for r in range(3):
            self.root.grid_rowconfigure(r, weight=1)

        for c in range(3):
            self.root.grid_columnconfigure(c, weight=1)

        tkinter.Label(self.root, text='Name').grid(column=0, row=0)
        self.name_entry = tkinter.Entry(self.root)
        self.name_entry.grid(column=1, row=0, columnspan=2, sticky='NSEW')
        tkinter.Label(self.root, text='Password').grid(column=0, row=1)
        self.password_entry = tkinter.Entry(self.root)
        self.password_entry.grid(column=1, row=1, columnspan=2, sticky='NSEW')
        tkinter.Button(self.root, text='Create', command=self.create).grid(column=2, row=2, sticky='NSEW')

    def create(self):
        default_config = \
            '{\n' + \
            f'  "name": "{self.name_entry.get()}",\n' + \
            f'  "password_sha256": "{hashlib.sha256(self.password_entry.get().encode("utf-8")).hexdigest()}"\n' + \
            '}'
        with open('user_config.json', 'w') as file:
            file.write(default_config)
        self.root.destroy()
