# -*- coding: utf-8 -*-

import argparse

from World import Team
from gameController import gameController
from ConfigDialog import ConfigDialog
from loader import Loader
import states

if __name__ == '__main__':
    # TODO: Return console interface.
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cli', dest='cli', action='store_true', help='Skip graphical config and use console options.')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Enable debugging for developers.')
    parser.add_argument('-s', '--size', type=str, dest='size', default='50 21', help='Size of map, pair of integer as "x_size y_size". By default equals to "50 21"')
    parser.add_argument('-d', '--delay', type=int, dest='delay', default=500, help='Delay between turns in ms.')
    parser.add_argument('--logs', action='store_true', dest='logs_flag', help='Enable logs gathering.')
    parser.add_argument('-t', '--theme', type=str, dest='theme', default='constructor', help='Theme for graphical interface.')
    parser.add_argument('-a', '--algorithm', type=str, dest='strategies', action='append', help='Specifes one strategy. Use few -a to specify few strategies')
   
    args = parser.parse_args()
    
    # # Not working anyway.
    # log_name = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    log_name = None

    states.DEBUG = args.debug

    if not args.cli:
        teams = set() 
        strategies = []
        config = dict()
        defaults = {
            'width': int(args.size.split()[0]),
            'height': int(args.size.split()[1]),
            'delay': args.delay,
            'enable_logs': args.logs_flag,
            'theme': args.theme,
            'strategies': (args.strategies if args.strategies else [])
        }
        ConfigDialog(strategies, config, defaults)
        size = (config['width'], config['height'])
        delay = config['delay']
        ready_log_name = (log_name if config['enable_logs'] else None)
        themeStr=config['theme']
    else:
        size = tuple(map(int, args.size.split()))
        delay = args.delay
        ready_log_name = (log_name if args.logs_flag else None)
        themeStr = args.theme
        teams = set()
        if args.strategies:
            strategies = Loader().loadStrategies(args.strategies)
        else:
            strategies = []
    for i, strategy in enumerate(strategies):
        teams.update({Team(AntClass=strategy.AntClass,
                           BaseClass=strategy.BaseClass,
                           team_id=i + 1,
                           team_name=strategy.name)})
    AntWarsGame = gameController(size=size,
                                 delay=delay,
                                 log_name=ready_log_name,
                                 themeStr=themeStr
                                 )

    AntWarsGame.Init(teams=teams)
    AntWarsGame.launch()
