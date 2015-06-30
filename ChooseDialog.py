import os
from Tkinter import *
from loader import Strategy, Loader

class ChooseDialog:
    def __init__(self, result, noindex=[]):
        self.result = result
        self.lo = Loader()
        top = self.top = Tk()
        Label(top, text='Choose strategies (just close this window when ready):').grid(row=0, columnspan=2, sticky=W)
        self.index = [self.lo.loadStrategy(filename[:-3]) for filename in os.listdir('strategies')]
        names = [o.name + ' ' + o.version for o in self.index]
        self.selected = StringVar()
        self.selected.set(names[0])
        self.selected.trace('w', self.changeDescription)
        OptionMenu(top, self.selected, *names).grid(row=1, sticky=W)
        self.desc = Text(top)
        self.desc.insert('0.0', self.index[0].description)
        self.desc.grid(row=2, sticky=W)
        Button(top, text='Add =>', command=self.addItem).grid(row=3)
        self.list = Listbox(top)
        self.list.grid(row=0, column=1, rowspan=3)
        Button(top, text='Delete', command=lambda lb=self.list: lb.delete(ANCHOR)).grid(row=3, column=1)
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
        self.top.destroy()