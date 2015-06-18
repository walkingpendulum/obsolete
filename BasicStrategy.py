'''
    ant.move() -> (destination_coord, move)
    moves: 'hit', 'move', 'take_food', 'drop_food'
'''
from random import choice
from Base import Base
from Ant import Ant


class BasicBase(Base):
    max_ant_quantity = 7

    def advance(self):
        if len(self.API.get_list_of_ants()) < type(self).max_ant_quantity and\
                self.API.get_cost_of_ant_spawn() <= self.API.get_food_quantity():
            self.API.ask_for_spawn()

    def ask_for_move(self, ant):
        if self.API.cargo_load(ant):
            pass
        else:
            x, y = self.API.get_coord(ant)
            return choice([(a, b) for a in range(x-1, x+2) for b in range(y-1, y+2)])

class BasicAnt(Ant):
    max_food_time = 10

    def __init__(self, base):
        Ant.__init__(self, base)
        self.food_time = 0

    def move(self):
        return (self.base.ask_for_move(self), 'move')
