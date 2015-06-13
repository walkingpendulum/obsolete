# -*- coding: utf-8 -*-

import argparse
from time import sleep
from datetime import datetime

from planet import Planet
from BasicStrategy import BasicAnt, BasicBase


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

    FirstAntClass, FirstBaseClass = BasicAnt, BasicBase
    SecondAntClass, SecondBaseClass = BasicAnt, BasicBase
    Earth = Planet(size=map(int, args.size.split()),
                   AntClass1=FirstAntClass, BaseClass1=FirstBaseClass,
                   AntClass2=SecondAntClass, BaseClass2=SecondBaseClass)
    while True:
        Earth.advance()
        print Earth
        print len(Earth.Base1.catalog), len(Earth.Base2.catalog)
        if args.logs_flag:
            dump(Earth, log_name)
        sleep(args.delay)
