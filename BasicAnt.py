'''
class Planet():
    get_neighborhood(x, y) -> ((x_i, y_i, type) for x, y if dist((x,y), (x_i, y_i)) <= r)
    types: Food, NoneType, Base, %AntClass%

'''

from random import choice
from planet import Food, Base

class Ant(object):
    pass

class BasicAnt(Ant):
    X_SIZE, Y_SIZE = 10, 10
    planet = None

    def __init__(self, coord, team):
        self.team = team
        self.coord = coord
        self.has_food = False
        self.food_time = 0
        self.stack = []
        self.base_coord = (0, 0) if 0 <= self.coord[0] < 2 \
                          else (BasicAnt.X_SIZE - 1, BasicAnt.Y_SIZE - 1)

    def move(self):
        '''
            move() -> (x_new, y_new, move)
            moves: 'hit', 'move', 'take_food', 'drop_food'

        '''
        def next_coordinates(x, y, step=None):
            ''' steps: 'up', 'down', 'left', 'right' '''
            add = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)}
            x_new, y_new = x + add[step][0], y + add[step][1]

            if not (0 <= x_new < BasicAnt.X_SIZE and 0 <= y_new < BasicAnt.Y_SIZE):
                return x, y
            data = BasicAnt.planet.get_data_from_cell(x_new, y_new)
            if not isinstance(data, Ant):                  
                    return (x_new, y_new)
            else:
                return (x, y)


        if self.has_food is False:
            next_step = choice(['up', 'down', 'left', 'right'])
            x, y = next_coordinates(*self.coord, step=next_step)
            data = BasicAnt.planet.get_data_from_cell(x, y)
            if isinstance(data, Food):
                self.has_food = True
                self.food_share_time = 20
                return (x, y) + ('take_food',)
            elif data is None:
                return (x, y) + ('move',)
            else:
                return self.coord + ('move',)
        elif self.has_food is True:
            data = BasicAnt.planet.get_data_from_cell
            if self.base_coord[0] == 0:
                steps = ['down', 'left']
            else:
                steps = ['up', 'right']
            x, y = next_coordinates(*self.coord, step=choice(steps))
            if (x, y) == self.base_coord:
                self.has_food = False
                self.food_time = 0
                return (x, y) + ('drop_food',)
            else:
                if self.food_share_time == 1:
                    self.has_food = False
                self.food_time -= 1
                return (x, y) + ('move',)
