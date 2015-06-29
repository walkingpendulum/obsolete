# -*- coding: utf-8 -*-

import sys
import os.path
from Tkinter import *
from World import Food, Base, World
from random import randint

class gameController:
    def __init__(self, size, delay, log_name, themeStr):
        self.world = World(size, log_name)
        self.delay = delay
        self.width, self.height = size
        self.theme = None
        self.loadTheme(themeStr)
        self.master = Tk()
        self.canvas = Canvas(self.master,
                             width=self.width * self.theme['CELL_SIZE'],
                             height=self.height * self.theme['CELL_SIZE'],
                             bg=self.theme['BG_COLOR']
                             )

    def Init(self, teams):
        self.world.Init(teams)

        self.master['bg'] = self.theme['BG_COLOR']
        self.master.title('Ant Wars')
        self.canvas.pack(ipadx=0, ipady=0)

        def hexToRGB(s):
            return map(lambda x: int(x, base=16), [s[i:i+2] for i in range(1, 7, 2)])

        def isClose(la, ra):
            return abs(la[0] - ra[0]) < 40\
                   or abs(la[1] - ra[1]) < 40 \
                   or abs(la[2] - ra[2]) < 40

        def isCloseWithOther(newColor):
            return any(isClose(hexToRGB(newColor), hexToRGB(color)) for color in self.teamColors)

        # рандомим цвета для команд
        self.teamColors = []
        for i in range(len(self.world.teams_by_base)):
            newColor = ''
            while not newColor \
                    or isClose(hexToRGB(newColor), (255, 255, 255)) \
                    or isClose(hexToRGB(newColor), (0, 0, 0)) \
                    or isClose(hexToRGB(newColor), (255, 0, 0)) \
                    or isCloseWithOther(newColor)\
                    :
                newColor = ("#%06x" % randint(0, 0xFFFFFF))
            self.teamColors.append(newColor)

        # отрисовываем статистику
        self.stats = []
        # todo: тут адский ад со сбором статистики, нужно прикрутить нормальную
        statsSrc = sorted(str(self.world)[self.width * self.height:].split('\n'))
        for i in range(len(self.teamColors)):
            self.stats.append(StringVar())
            self.stats[i].set(statsSrc[i])
            Label(self.master, textvariable=self.stats[i], fg=self.teamColors[i], bg=self.theme['BG_COLOR']).pack()

    def repaint(self):
        self.canvas.delete(ALL)
        field = str(self.world).split('\n')
        for line in range(self.height):
            for cell in range(self.width):
                char = field[line][cell]
                if char == ' ':
                    color = self.theme['EMPTY_CELL_COLOR']
                elif char == Food.label:
                    color = self.theme['FOOD_COLOR']
                elif char == Base.label:
                    color = self.theme['BASE_COLOR']
                else:
                    color = self.teamColors[int(char) - 1]
                self.canvas.create_rectangle(cell * self.theme['CELL_SIZE'],
                                             line * self.theme['CELL_SIZE'],
                                             (cell + 1) * self.theme['CELL_SIZE'],
                                             (line + 1) * self.theme['CELL_SIZE'],
                                             fill=color,
                                             outline=self.theme['OUTLINE_COLOR']
                                             )
        statsSrc = sorted(field[self.height:])[1:]
        for i in range(len(statsSrc)):
            self.stats[i].set(statsSrc[i])

    def loadTheme(self, themeStr):
        if not os.path.isfile('themes/' + themeStr + '.py'):
            raise ValueError('Incorrect theme specified.')
        with open('themes/' + themeStr + '.py') as themeFile:
            exec(themeFile.read())
#        if 'theme' not in globals():
#            raise ValueError('Incorrect theme specified.')

    def advance(self):
        self.world.advance()
        self.repaint()
        self.master.after(self.delay, self.advance)

    def launch(self):
        self.master.after(1, self.advance)
        self.master.mainloop()