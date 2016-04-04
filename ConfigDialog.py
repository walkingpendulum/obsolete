# coding=utf-8
import os
from Tkinter import *
from loader import Strategy, Loader
import strategies


def make_human_readable_names(path):
    return os.path.split(path)[-1].split('.')[0]


class ConfigDialog:
    def __init__(self, result, config, defaults):
        self.result = result
        self.config = config
        self.lo = Loader()
        self.master = Tk()

        Label(self.master, text='Choose strategies (just close this window when ready):').grid(
            row=0, columnspan=2)
        # Create list of strategies.
        stratFiles = filter(lambda t:
                                not t.endswith('.pyc')
                                and not t.startswith('__init__.py'),
                            os.listdir(strategies.__path__[0]))
        self.index = {
            make_human_readable_names(filename): self.lo.loadStrategy(os.path.join(strategies.__path__[0], filename)) for filename in stratFiles
        }
        names = [make_human_readable_names(f) for f in stratFiles]

        # todo: выпилить опцию "изменить описание"
        # Strategies combo box.
        self.selected = StringVar()
        self.selected.set(names[0])
        self.selected.trace('w', self.changeDescription)
        OptionMenu(self.master, self.selected, *names).grid(row=1)

        # Description field.
        self.desc = Text(self.master, width=1)
        self.desc.insert('0.0', sorted(self.index.values())[0].description)
        self.desc.grid(row=2, sticky=NSEW)

        # "Add" button for strategies.
        Button(self.master, text='Add =>',
               command=self.addStrategy).grid(row=3)

        # Selected strategies list.
        self.stratList = Listbox(self.master)
        for name in defaults['strategies']:
            self.stratList.insert(
                END, name)
        self.stratList.grid(row=1, column=1, rowspan=2, sticky=NS)

        # "Delete" button for strategies.
        Button(self.master, text='Delete', command=lambda lb=self.stratList: lb.delete(
            ANCHOR)).grid(row=3, column=1)

        # Themes combo box.
        Label(self.master, text='Choose theme:').grid(
            row=4, column=0, sticky=W)
        self.theme = StringVar()
        self.theme.set(defaults['theme'])
        OptionMenu(self.master, self.theme, *[filename[:-3] for filename in os.listdir(
            'themes')]).grid(row=4, column=1, sticky=EW)

        # Width spinbox.
        Label(self.master, text='Field width:').grid(row=5, column=0, sticky=W)
        self.width = Spinbox(self.master, from_=10, to=300)
        self.width.delete(0, END)
        self.width.insert(0, defaults['width'])
        self.width.grid(row=5, column=1, sticky=EW)

        # Height spinbox.
        Label(self.master, text='Field height:').grid(
            row=6, column=0, sticky=W)
        self.height = Spinbox(self.master, from_=10, to=300)
        self.height.grid(row=6, column=1, sticky=EW)
        self.height.delete(0, END)
        self.height.insert(0, defaults['height'])

        # Delay spinbox.
        Label(self.master, text='Step delay (in ms):').grid(
            row=7, column=0, sticky=W)
        self.delay = Spinbox(self.master, from_=100, to=5000)
        self.delay.delete(0, END)
        self.delay.insert(0, defaults['delay'])
        self.delay.grid(row=7, column=1, sticky=EW)

        # # Logs checkbox. (logs dont working anyway)
        # self.enable_logs = IntVar()
        # self.enable_logs.set(int(defaults['enable_logs']))
        # Checkbutton(self.master, text='Enable logs', variable=self.enable_logs).grid(row=8, column=0, columnspan=2, sticky=W)

        self.master.protocol('WM_DELETE_WINDOW', self.ok)
        self.master.mainloop()

    def addStrategy(self):
        name = self.selected.get()
        dir_path = os.path.split(strategies.__path__[0])[-1]
        self.stratList.insert(END, os.path.join(dir_path, name + '.py'))

    def changeDescription(self, *nothing, **nowhere):
        self.desc.delete('0.0', END)
        self.desc.insert('0.0', self.index[self.selected.get()].description)

    def ok(self):
        self.result.extend([self.index[make_human_readable_names(name)] for name in list(self.stratList.get(0, END))])
        self.config['theme'] = (
            self.theme.get() if self.theme.get() else 'constructor')
        self.config['width'] = (int(self.width.get())
                                if self.width.get().isdigit() else 50)
        self.config['height'] = (
            int(self.height.get()) if self.height.get().isdigit() else 21)
        self.config['delay'] = (int(self.delay.get())
                                if self.delay.get().isdigit() else 500)

        # # Logs dont working anyway.
        # self.config['enable_logs'] = bool(self.enable_logs.get())
        self.config['enable_logs'] = False

        self.master.destroy()
