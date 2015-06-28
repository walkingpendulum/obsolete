# -*- coding: utf-8 -*-

from Tkinter import *
import AntWars
import random

BG_COLOR = 'white'
EMPTY_CELL_COLOR = 'blanched almond'
FOOD_COLOR = 'lime green'
BASE_COLOR = 'black'
CELL_SIZE = 20

class Painter:
    def __init__(self, width, height, earth):
        self.width = width
        self.height = height
        self.master = Tk()
        self.master['bg'] = BG_COLOR
        self.master.title('Ant Wars')
        self.canvas = Canvas(self.master,
                             width=width * CELL_SIZE,
                             height=height * CELL_SIZE,
                             bg=BG_COLOR\
                             )
        self.canvas.pack(ipadx=0, ipady=0)

        hexToRGB = lambda s: map(lambda x: int(x, base=16), [s[i:i+2] for i in range(1, 7, 2)])
        isClose = lambda la, ra: abs(la[0] - ra[0]) < 40 \
                                 or abs(la[1] - ra[1]) < 40 \
                                 or abs(la[2] - ra[2]) < 40
        isCloseWithOther = lambda newColor: any(isClose(hexToRGB(newColor), hexToRGB(color)) 
                                                for color in self.teamColors)
        # рандомим цвета для команд
        self.teamColors = []
        for i in range(len(earth.teams_by_base)):
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
        statsSrc = sorted(str(earth)[width * height:].split('\n'))
        for i in range(len(self.teamColors)):
            self.stats.append(StringVar())
            self.stats[i].set(statsSrc[i])
            Label(self.master, textvariable=self.stats[i], fg=self.teamColors[i], bg=BG_COLOR).pack()

    def update(self, inst):
        self.canvas.delete(ALL)
#        self.canvas.create_rectangle(0, 0, CELL_SIZE * self.width, CELL_SIZE * self.height, fill=EMPTY_CELL_COLOR)
        field = inst.split('\n')
        for line in range(self.height):
            for cell in range(self.width):
                char = field[line][cell]
                figure = 'rectangle'
                if char == ' ':
                    color = EMPTY_CELL_COLOR
                elif char == AntWars.Food.label:
                    color = FOOD_COLOR
                elif char == AntWars.Base.label:
                    color = BASE_COLOR
                else:
                    color = self.teamColors[int(char) - 1]
                    figure = 'oval'
                # отрисовываем свою фигуру для каждого из случаев: "муравей" или "все остальное"
                getattr(self.canvas, 'create_%s' % figure)(cell * CELL_SIZE,
                                                           line * CELL_SIZE,
                                                           (cell + 1) * CELL_SIZE,
                                                           (line + 1) * CELL_SIZE,
                                                           fill=color,
                                                           outline=EMPTY_CELL_COLOR\
                                                           )
        statsSrc = sorted(field[self.height:])[1:]
        for i in range(len(statsSrc)):
            self.stats[i].set(statsSrc[i])
        
