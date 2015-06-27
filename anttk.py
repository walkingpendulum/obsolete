from Tkinter import *
import AntWars
import random

class Painter:
    def __init__(self, width, height, earth):
        self.width = width
        self.height = height
        self.master = Tk()
        self.master['bg'] = 'black'
        self.master.title('Ant Wars')
        self.cellSize = 10
        self.canvas = Canvas(self.master, width=width * self.cellSize, height=height * self.cellSize)
        self.canvas.pack(ipadx=0, ipady=0)
        def hexToRGB(s):
            red = int(s[1:3], base=16)
            green = int(s[3:5], base=16)
            blue = int(s[5:7], base=16)
            return red, green, blue
        def isClose(la, ra):
            print la, ra
            return abs(la[0] - ra[0]) + abs(la[1] - ra[1]) + abs(la[2] - ra[2]) < 150
        def isCloseWithOther(j):
            for i in range(j):
                if isClose(hexToRGB(self.teamColors[j]), hexToRGB(self.teamColors[i])):
                    return True
            return False
        self.teamColors = []
        for i in range(len(earth.teams_by_base)):
            self.teamColors.append("#%06x" % random.randint(0,0xFFFFFF))
            while isClose(hexToRGB(self.teamColors[i]), (255, 255, 255)) or\
                  isClose(hexToRGB(self.teamColors[i]), (0, 0, 0)) or\
                  isClose(hexToRGB(self.teamColors[i]), (255, 0, 0)) or\
                  isCloseWithOther(i):
                self.teamColors[i] = ("#%06x" % random.randint(0,0xFFFFFF))
        self.stats = []
        self.statsLabels = []
        statsSrc = sorted(str(earth)[width * height:].split('\n'))
        for i in range(len(self.teamColors)):
            self.stats.append(StringVar())
            self.stats[i].set(statsSrc[i])
            self.statsLabels.append(Label(self.master, textvariable=self.stats[i], fg=self.teamColors[i], bg='black'))
            self.statsLabels[i].pack()

    def update(self, inst):
        self.canvas.delete(ALL)
        cs = self.cellSize
        field = inst.split('\n')
        for line in range(self.height):
            for cell in range(self.width):
                char = field[line][cell]
                if char == ' ':
                    color = 'white'
                elif char == AntWars.Food.label:
                    color = 'red'
                elif char == AntWars.Base.label:
                    color = 'black'
                else:
                    color = self.teamColors[int(char) - 1]
                self.canvas.create_rectangle(cell * cs, line * cs, (cell + 1) * cs, (line + 1) * cs, fill=color)
        statsSrc = sorted(field[self.height:])[1:]
        for i in range(len(statsSrc)):
            self.stats[i].set(statsSrc[i])
        
