# -*- coding: utf-8 -*-

import argparse
import sys
import os.path
from datetime import datetime

from World import Team
from BasicStrategy import BasicAnt, BasicBase
from gameController import gameController

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=str, dest='size', default='50 21', help='Size of map, pair of integer as "x_size y_size". By default equals to "50 21"')
    parser.add_argument('-d', '--delay', type=float, dest='delay', default=500, help='Delay between turns in ms.')
    parser.add_argument('--logs', action='store_true', dest='logs_flag', help='Enable logs gathering.')
    parser.add_argument('-t', '--theme', type=str, dest='theme', default='constructor', help='Theme for graphical interface.')

    args = parser.parse_args()
    log_name = datetime.now().strftime("%y-%m-%d-%H-%M-%S") if args.logs_flag else None
    if not os.path.isfile('themes/' + args.theme + '.py'):
        raise ValueError('Incorrect theme specified.')
    with open('themes/' + args.theme + '.py') as themeFile:
        exec(themeFile.read())
    if 'theme' not in globals():
        raise ValueError('Incorrect theme specified.')
    team1 = Team(AntClass=BasicAnt, BaseClass=BasicBase, team_id=1)
    team2 = Team(AntClass=BasicAnt, BaseClass=BasicBase, team_id=2)
    AntWarsGame = gameController(size=tuple(map(int, args.size.split())),
                                 delay=args.delay,
                                 log_name=log_name,
                                 theme=theme
                                 )

    AntWarsGame.Init(teams={team1, team2})
    AntWarsGame.launch()
