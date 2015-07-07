# -*- coding: utf-8 -*-

import os.path
from Tkinter import *
from World import Food, World
from Base import Base
from Ant import Ant
from random import randint
from itertools import izip
from functools import partial

class gameController:
    def loadTheme(self, themeStr):
        if not os.path.isfile('themes/' + themeStr + '.py'):
            raise ValueError('Incorrect theme specified.')
        with open('themes/' + themeStr + '.py') as themeFile:
            exec(themeFile.read())
        if not hasattr(self, 'theme'):
            raise ValueError('Smth goes wrong, theme loading crashed')

    def __init__(self, size, delay, log_name, themeStr):
        # todo: написать спецификацию для loadTheme() и файлов с темами
        self.loadTheme(themeStr)
        self.world = World(size, log_name)
        self.delay = delay
        self.teamColors = []
        self.statStringVars = []
        self.master = Tk()
        self.figure_by_obj = dict()
        self.canvas = Canvas(self.master,
                             width=size[0] * self.theme['CELL_SIZE'],
                             height=size[1] * self.theme['CELL_SIZE'],
                             bg=self.theme['BG_COLOR']
                             )

    def Init(self, teams):
        def hexToRGB(s):
            return map(partial(int, base=16), [s[i:i+2] for i in range(1, 7, 2)])

        def isClose(la, ra):
            return abs(la[0] - ra[0]) < 40\
                   or abs(la[1] - ra[1]) < 40 \
                   or abs(la[2] - ra[2]) < 40

        def isCloseWithOther(newColor):
            return any(isClose(hexToRGB(newColor), hexToRGB(color)) for color in self.teamColors)

        def getNewColor():
            newColor = ''
            while not newColor \
                    or isClose(hexToRGB(newColor), (255, 255, 255)) \
                    or isClose(hexToRGB(newColor), (0, 0, 0)) \
                    or isClose(hexToRGB(newColor), (255, 0, 0)) \
                    or isCloseWithOther(newColor)\
                    :
                newColor = ("#%06x" % randint(0, 0xFFFFFF))
            return newColor

        self.master.title('Ant Wars')
        self.master['bg'] = self.theme['BG_COLOR']
        self.canvas.create_rectangle(0,
                                     0,
                                     (self.world.size[0] + 1) * self.theme['CELL_SIZE'],
                                     (self.world.size[1] + 1) * self.theme['CELL_SIZE'],
                                     fill=self.theme['EMPTY_CELL_COLOR'],
                                     )
        if self.theme['EMPTY_OUTLINE']:
            for i in range(0, self.world.size[0]):
                for j in range(0, self.world.size[1]):
                    self.canvas.create_rectangle(i * self.theme['CELL_SIZE'],\
                                                 j * self.theme['CELL_SIZE'],\
                                                 (i + 1) * self.theme['CELL_SIZE'],\
                                                 (j + 1) * self.theme['CELL_SIZE'],\
                                                 fill='',
                                                 outline=self.theme['OUTLINE_COLOR'])
        self.canvas.pack(ipadx=0, ipady=0)
        self.world.Init(teams)
        self.teamColors = [getNewColor() for _ in sorted(self.world.teams_by_base, key=lambda base: base.team_id)]
        self.statStringVars = [StringVar() for _ in sorted(self.world.teams_by_base, key=lambda base: base.team_id)]
        for stringVar, color in izip(self.statStringVars, self.teamColors):
            lbl = Label(self.master, textvariable=stringVar, fg=color, bg=self.theme['BG_COLOR'])
            lbl.pack()
        self.repaint()

    def repaint(self):
        for obj, method in self.world.repaint_method_by_obj.items():
            getattr(self, method)(obj)

        for stringVar, line in izip(self.statStringVars, self.world.getTeamStatList()):
            stringVar.set(line)

    def deleteCell(self, obj):
        self.canvas.delete(self.figure_by_obj[obj])
        self.canvas.update_idletasks()

    def moveCell(self, obj):
        x, y = self.world.coord_by_obj[obj]
        figure = self.figure_by_obj[obj]
        self.canvas.coords(figure,
                           x * self.theme['CELL_SIZE'],
                           y * self.theme['CELL_SIZE'],
                           (x + 1) * self.theme['CELL_SIZE'],
                           (y + 1) * self.theme['CELL_SIZE']
                           )
        self.canvas.update_idletasks()

    def createCell(self, obj):
        x, y = self.world.coord_by_obj[obj]
        if obj is None:
            color = self.theme['EMPTY_CELL_COLOR']
        elif isinstance(obj, Food):
            color = self.theme['FOOD_COLOR']
        elif isinstance(obj, Base):
            color = self.theme['BASE_COLOR']
        elif isinstance(obj, Ant):
            color = self.teamColors[obj.base.team_id - 1]
        figure = self.canvas.create_rectangle(x * self.theme['CELL_SIZE'],
                                              y * self.theme['CELL_SIZE'],
                                              (x + 1) * self.theme['CELL_SIZE'],
                                              (y + 1) * self.theme['CELL_SIZE'],
                                              fill=color,
                                              outline=self.theme['OUTLINE_COLOR'],
                                              )
        self.figure_by_obj[obj] = figure
        self.canvas.update_idletasks()

    def advance(self):
        self.world.advance()
        self.repaint()
        self.master.after(self.delay, self.advance)

    def launch(self):
        self.master.after(1, self.advance)
        self.master.mainloop()