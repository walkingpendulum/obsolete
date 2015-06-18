'''
    ant.move() -> (destination_coord, move)
    moves: 'hit', 'move', 'take_food', 'drop_food'
'''
from random import choice, randint
from itertools import product
from Base import Base
from Ant import Ant

def dist(old_coord, new_coord):
    return min(abs(old_coord[0] - new_coord[0]), abs(old_coord[1] - new_coord[1]))

class BasicBase(Base):
    max_ant_quantity = 7

    def __init__(self):
        Base.__init__(self)
        self.ant_sets_by_type = dict()


    def advance(self):
        if len(self.API.get_list_of_ants()) < type(self).max_ant_quantity and\
                self.API.get_cost_of_ant_spawn() <= self.API.get_food_quantity():
            self.API.ask_for_spawn(AntClass=BasicRanger)

    def ask_for_move(self, ant):
        if self.API.cargo_load(ant):
            pass
        else:
            x, y = self.API.get_coord(ant)
            return choice([(a, b) for a in range(x-1, x+2) for b in range(y-1, y+2)])

    def is_enemy_class(self, ones_class):
        return issubclass(ones_class, Ant) and not issubclass(ones_class, BasicAnt)

class BasicAnt(Ant):
    def move(self):
        return (self.base.ask_for_move(self), 'move')

class BasicRanger(BasicAnt):
    def __init__(self, base):
        Ant.__init__(self, base)
        self.next_cell_for_patrol = self.base.API.get_coord_by_obj(self)

    def nhood(self, radius):
        API = self.base.API
        x0, y0, x_max, y_max = API.get_coord_by_obj(self) + API.get_size_of_world()
        type_by = API.get_type_by_coord
        return [(x, y, type_by(x, y)) for x, y in
                product(range(-radius + x0, radius + 1 + x0), range(-radius + y0, radius + 1 + y0))
                if 0 <= x < x_max and 0 <= y < y_max]

    def get_horizon_with_enemies(self, radius):
        return [(x, y) for x, y, t in self.nhood(radius) if self.base.is_enemy_class(t)]

    def set_next_cell_for_patrol(self):
        x_max, y_max = self.base.API.get_size_of_world()
        while True:
            self.next_cell_for_patrol = randint(0, x_max), randint(0, y_max)
            if not issubclass(self.base.API.get_type_by_coord(self.next_cell_for_patrol), Base):
                break

    def patrol(self):
        nhood = [(x, y) for x, y, t in self.nhood(1) if
                 not issubclass(t, Base)]

        x, y = self.next_cell_for_patrol
        return min(nhood, key=lambda coord: dist(old_coord=(x, y), new_coord=coord))

    def attack(self, horizon):
        enemies_coord = [(x, y) for x, y, t in self.nhood(1) if self.base.is_enemy_class(t)]
        if enemies_coord:
            return (choice(enemies_coord), 'hit')
        else:
            coord = min(self.nhood(1),
                       key=lambda x, y, t: min(dist(enemy_coord, (x, y))
                                                 for enemy_coord in horizon))
            return (coord, 'move')

    def move(self):
        if self.next_cell_for_patrol is None:
            self.next_cell_for_patrol = self.base.API.get_coord_by_obj(self)
        horizon = self.get_horizon_with_enemies(radius=3)
        if horizon:
            return self.attack(horizon)
        else:
            if self.base.API.get_coord_by_obj(self) == self.next_cell_for_patrol:
                self.set_next_cell_for_patrol()
            return (self.patrol(), 'move')



