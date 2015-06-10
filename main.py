import argparse
from time import sleep
from datetime import datetime
from Planet import Planet

from BasicStrategy import BasicAnt, BasicBase
from FireAnt import FireAnt, FireAntBase


def dump(planet, path):
    with open(path, mode='a') as f:
        f.write(str(planet).replace('\n', '$') + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=str, dest='size', default='50 30', help='Size of map, pair of integer as "x_size y_size". By default equals to "50 30"')
    parser.add_argument('-d', '--delay', type=float, dest='delay', default=0.5, help='Delay between turns in second. By deafult equals to 0.3 sec.')
    args = parser.parse_args()
    log_name = datetime.now().strftime("%y-%m-%d-%H-%M-%S")

    FirstAntClass, FirstBaseClass = BasicAnt, BasicBase
    SecondAntClass, SecondBaseClass = BasicAnt, BasicBase
    Earth = Planet(size=map(int, args.size.split()),
                   AntClass1=FirstAntClass, BaseClass1=FirstBaseClass,
                   AntClass2=SecondAntClass, BaseClass2=SecondBaseClass)
    while True:
        Earth.advance()
#        dump(Earth, log_name)
        print Earth
        sleep(args.delay)

    print Earth
