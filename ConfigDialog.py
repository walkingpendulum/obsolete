import os
from Tkinter import *
from loader import Strategy, Loader

class ConfigDialog:
    def __init__(self, result, config):
        self.result = result
        self.config = config
        self.lo = Loader()
        top = self.top = Tk()
        Label(top, text='Choose strategies (just close this window when ready):').grid(row=0, columnspan=2)
        self.index = [self.lo.loadStrategy(filename[:-3]) for filename in os.listdir('strategies')]
        names = [o.name + ' ' + o.version for o in self.index]
        self.selected = StringVar()
        self.selected.set(names[0])
        self.selected.trace('w', self.changeDescription)
        OptionMenu(top, self.selected, *names).grid(row=1)
        self.desc = Text(top, width=1)
        self.desc.insert('0.0', self.index[0].description)
        self.desc.grid(row=2, sticky=NSEW)
        Button(top, text='Add =>', command=self.addItem).grid(row=3)
        self.list = Listbox(top)
        self.list.grid(row=1, column=1, rowspan=2, sticky=NS)
        Button(top, text='Delete', command=lambda lb=self.list: lb.delete(ANCHOR)).grid(row=3, column=1)
        self.theme = StringVar()
        Label(top, text='Choose theme:').grid(row=4, column=0, sticky=W)
        OptionMenu(top, self.theme, *[filename[:-3] for filename in os.listdir('themes')]).grid(row=4, column=1, sticky=EW)
        Label(top, text='Field width:').grid(row=5, column=0, sticky=W)
        self.width = Spinbox(top, from_=10, to=300)
        self.width.delete(0, END)
        self.width.insert(0, 50)
        self.width.grid(row=5, column=1, sticky=EW)
        Label(top, text='Field height:').grid(row=6, column=0, sticky=W)
        self.height = Spinbox(top, from_=10, to=300)
        self.height.grid(row=6, column=1, sticky=EW)
        self.height.delete(0, END)
        self.height.insert(0, 21)
        Label(top, text='Step delay (in ms):').grid(row=7, column=0, sticky=W)
        self.delay = Spinbox(top, from_=100, to=5000)
        self.delay.delete(0, END)
        self.delay.insert(0, 500)
        self.delay.grid(row=7, column=1, sticky=EW)  
        self.enable_logs = IntVar()
        Checkbutton(top, text='Enable logs', variable=self.enable_logs).grid(row=8, column=0, columnspan=2, sticky=W)
        top.protocol('WM_DELETE_WINDOW', self.ok)
        top.mainloop()
        
    def addItem(self):
        self.list.insert(END, self.selected.get())
        
    def changeDescription(self, *nothing, **nowhere):
        names = [o.name + ' ' + o.version for o in self.index]
        i = names.index(self.selected.get())
        self.desc.delete('0.0', END)
        self.desc.insert('0.0', self.index[i].description)

    def ok(self):
        names = [o.name + ' ' + o.version for o in self.index]
        for name in list(self.list.get(0, END)):
            self.result.append(self.index[names.index(name)])
        self.config['theme'] = (self.theme.get() if self.theme.get() else 'constructor')
        self.config['width'] = (int(self.width.get()) if self.width.get().isdigit() else 50)
        self.config['height'] = (int(self.height.get()) if self.height.get().isdigit() else 21)
        self.config['delay'] = (int(self.delay.get()) if self.delay.get().isdigit() else 500)
        self.config['enable_logs'] = bool(self.enable_logs.get())
        self.top.destroy()