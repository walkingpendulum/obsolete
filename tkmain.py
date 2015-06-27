# -*- coding: utf-8 -*-

import argparse
from time import sleep
from datetime import datetime

from AntWars import World, Team
from BasicStrategy import BasicAnt, BasicBase

from anttk import Painter


def dump(planet, filename):
    ''' Сбрасывает текущее состояние поля str(planet) в файл filename.'''
    with open(filename, mode='a') as f:
        f.write(str(planet).replace('\n', '$') + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=str, dest='size', default='50 21', help='Size of map, pair of integer as "x_size y_size". By default equals to "50 21"')
    parser.add_argument('-d', '--delay', type=float, dest='delay', default=0.5, help='Delay between turns in second. By deafult equals to 0.3 sec.')
    parser.add_argument('--logs', action='store_true', dest='logs_flag', help='Enable log gathering.')

    args = parser.parse_args()
    log_name = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    team1 = Team(AntClass=BasicAnt, BaseClass=BasicBase, team_id=1)
    team2 = Team(AntClass=BasicAnt, BaseClass=BasicBase, team_id=2)
    Earth = World(size=tuple(map(int, args.size.split())))
    Earth.Init(teams={team1, team2})

    def life(this, earth, painter, log_name, delay):
        earth.advance()
        painter.update(str(earth))
        if args.logs_flag:
            dump(earth, log_name)
        painter.master.after(delay, this)

    w, h = list(map(int, args.size.split()))   
    p = Painter(w, h, Earth)
    
    def run():
        global Earth
        global p
        global log_name
        global run
        global args
        life(run, Earth, p, log_name, int(args.delay * 1000))
    
    p.master.after(1, run)
    p.master.mainloop()