# -*- coding: utf-8 -*-

import argparse
from datetime import datetime

from World import Team
from gameController import gameController
from ConfigDialog import ConfigDialog
from loader import Strategy

if __name__ == '__main__':
    # # TODO: Return console interface.
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-s', '--size', type=str, dest='size', default='50 21', help='Size of map, pair of integer as "x_size y_size". By default equals to "50 21"')
    # parser.add_argument('-d', '--delay', type=float, dest='delay', default=500, help='Delay between turns in ms.')
    # parser.add_argument('--logs', action='store_true', dest='logs_flag', help='Enable logs gathering.')
    # parser.add_argument('-t', '--theme', type=str, dest='theme', default='constructor', help='Theme for graphical interface.')

    # args = parser.parse_args()
    
    # # Not working anyway.
    # log_name = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    log_name = None
    
    teams = set()
    strategies = []
    config = dict()
    ConfigDialog(strategies, config)
    for i in range(len(strategies)):
        teams.update({Team(AntClass=strategies[i].AntClass, BaseClass=strategies[i].BaseClass, team_id=i + 1)})
    
    AntWarsGame = gameController(size=(config['width'], config['height']),
                                 delay=config['delay'],
                                 log_name=(log_name if config['enable_logs'] else None),
                                 themeStr=config['theme']
                                 )

    AntWarsGame.Init(teams=teams)
    AntWarsGame.launch()
