# -*- coding: utf-8 -*-

import argparse
from time import sleep
from datetime import datetime

from AntWars import World, Team
from BasicStrategy import BasicAnt, BasicBase

from anttk import gameController

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=str, dest='size', default='50 21', help='Size of map, pair of integer as "x_size y_size". By default equals to "50 21"')
    parser.add_argument('-d', '--delay', type=float, dest='delay', default=500, help='Delay between turns in ms.')
    parser.add_argument('--logs', action='store_true', dest='logs_flag', help='Enable log gathering.')

    args = parser.parse_args()
    log_name = datetime.now().strftime("%y-%m-%d-%H-%M-%S") if args.logs_flag else None
    team1 = Team(AntClass=BasicAnt, BaseClass=BasicBase, team_id=1)
    team2 = Team(AntClass=BasicAnt, BaseClass=BasicBase, team_id=2)
    Earth = World(size=tuple(map(int, args.size.split())), log_name=log_name)
    Earth.Init(teams={team1, team2})

    AntWarsGame = gameController(world=Earth, delay=args.delay)
    AntWarsGame.Init()
    AntWarsGame.launch()
