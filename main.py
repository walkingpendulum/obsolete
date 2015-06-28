# -*- coding: utf-8 -*-

import argparse
from datetime import datetime

from World import Team
from BasicStrategy import BasicAnt, BasicBase
from gameController import gameController

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=str, dest='size', default='50 21', help='Size of map, pair of integer as "x_size y_size". By default equals to "50 21"')
    parser.add_argument('-d', '--delay', type=float, dest='delay', default=500, help='Delay between turns in ms.')
    parser.add_argument('--logs', action='store_true', dest='logs_flag', help='Enable logs gathering.')
    args = parser.parse_args()
    log_name = datetime.now().strftime("%y-%m-%d-%H-%M-%S") if args.logs_flag else None

    # измените две строчки ниже, вставив туда ваши классы и классы соперника, с которым будете соревноваться
    team1 = Team(AntClass=BasicAnt, BaseClass=BasicBase, team_id=1)
    team2 = Team(AntClass=BasicAnt, BaseClass=BasicBase, team_id=2)

    AntWarsGame = gameController(size=tuple(map(int, args.size.split())),
                                 delay=args.delay,
                                 log_name=log_name
                                 )

    AntWarsGame.Init(teams={team1, team2})
    AntWarsGame.launch()
