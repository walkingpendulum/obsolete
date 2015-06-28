# -*- coding: utf-8 -*-

from Tkinter import *
from AntWars import Food, Base
import random

BG_COLOR = 'white'
EMPTY_CELL_COLOR = 'blanched almond'
FOOD_COLOR = 'lime green'
BASE_COLOR = 'black'
CELL_SIZE = 20

class gameController:
    def __init__(self, world, delay):
        self.world = world
        self.delay = delay
        self.width, self.height = world.size
        self.master = Tk()
        self.canvas = Canvas(self.master,
                             width=self.width * CELL_SIZE,
                             height=self.height * CELL_SIZE,
                             bg=BG_COLOR
                             )

    def Init(self):
        self.master['bg'] = BG_COLOR
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
                newColor = ("#%06x" % random.randint(0, 0xFFFFFF))
            self.teamColors.append(newColor)

        # отрисовываем статистику
        self.stats = []
        # todo: тут адский ад со сбором статистики, нужно прикрутить нормальную
        statsSrc = sorted(str(self.world)[self.width * self.height:].split('\n'))
        for i in range(len(self.teamColors)):
            self.stats.append(StringVar())
            self.stats[i].set(statsSrc[i])
            Label(self.master, textvariable=self.stats[i], fg=self.teamColors[i], bg=BG_COLOR).pack()

    def repaint(self):
        self.canvas.delete(ALL)
        field = str(self.world).split('\n')
        for line in range(self.height):
            for cell in range(self.width):
                char = field[line][cell]
                if char == ' ':
                    color = EMPTY_CELL_COLOR
                elif char == Food.label:
                    color = FOOD_COLOR
                elif char == Base.label:
                    color = BASE_COLOR
                else:
                    color = self.teamColors[int(char) - 1]
                self.canvas.create_rectangle(cell * CELL_SIZE,
                                             line * CELL_SIZE,
                                             (cell + 1) * CELL_SIZE,
                                             (line + 1) * CELL_SIZE,
                                             fill=color,
                                             outline=EMPTY_CELL_COLOR
                                             )
        statsSrc = sorted(field[self.height:])[1:]
        for i in range(len(statsSrc)):
            self.stats[i].set(statsSrc[i])

    def advance(self):
        self.world.advance()
        self.repaint()
        self.master.after(self.delay, self.advance)

    def launch(self):
        self.master.after(1, self.advance)
        self.master.mainloop()