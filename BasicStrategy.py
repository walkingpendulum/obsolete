# -*- coding: utf-8 -*-
'''
    ant.move() -> (destination_coord, move)
    moves: 'hit', 'move', 'take_food', 'drop_food'
'''
from random import choice, randint
from itertools import product
from Base import Base
from Ant import Ant
from World import Food

def dist(old_coord, new_coord):
    return max(abs(old_coord[0] - new_coord[0]), abs(old_coord[1] - new_coord[1]))

class BasicBase(Base):
    max_harvester_quantity = 7
    max_ranger_quantity = 4

    def advance(self):
        rangers_quantity = lambda: len([ant for ant in self.API.get_list_of_ants()
                                        if isinstance(ant, BasicRanger)])
        harvesters_quantity = lambda: len([ant for ant in self.API.get_list_of_ants()
                                           if isinstance(ant, BasicHarvester)])
        if harvesters_quantity() == 0:
            self.API.ask_for_spawn(AntClass=BasicHarvester)
        else:
            variety = [(rangers_quantity, BasicRanger, type(self).max_ranger_quantity),
                       (harvesters_quantity, BasicHarvester, type(self).max_harvester_quantity)]
            f, cls, q_max = choice(variety)
            if f() < q_max and self.API.get_cost_of_ant_spawn() <= self.API.get_food_quantity():
                self.API.ask_for_spawn(AntClass=cls)

    def ask_for_move(self, ant):
        if self.API.cargo_load(ant):
            pass
        else:
            x, y = self.API.get_coord(ant)
            return choice([(a, b) for a in range(x-1, x+2) for b in range(y-1, y+2)])

class BasicAnt(Ant):
    def nhood(self, radius):
        '''Возвращает окрестность радиуса radius'''
        API = self.base.API
        x0, y0, x_max, y_max = API.get_coord_by_obj(self) + API.get_size_of_world()
        type_by = API.get_type_by_coord
        return [(x, y, type_by(x, y)) for x, y in
                product(range(-radius + x0, radius + 1 + x0), range(-radius + y0, radius + 1 + y0))
                if 0 <= x < x_max and 0 <= y < y_max]

    def move(self):
        return (self.base.ask_for_move(self), 'move')


class BasicRanger(BasicAnt):
    def __init__(self, base):
        Ant.__init__(self, base)
        self.next_cell_for_patrol = self.base.API.get_coord_by_obj(self)

    def set_next_cell_for_patrol(self):
        x_max, y_max = self.base.API.get_size_of_world()
        while True:
            self.next_cell_for_patrol = randint(0, x_max - 1), randint(0, y_max - 1)
            if not issubclass(self.base.API.get_type_by_coord(self.next_cell_for_patrol), Base):
                break

    def get_horizon_with_enemies(self, radius):
        return [(x, y) for x, y, _ in self.nhood(radius) if self.base.API.is_enemy_by_coord(x, y)]

    def patrol(self):
        nhood = [(x, y) for x, y, t in self.nhood(1) if not issubclass(t, Base)]

        x, y = self.next_cell_for_patrol
        new_coord = min(nhood, key=lambda coord: dist(old_coord=(x, y), new_coord=coord))
        if issubclass(self.base.API.get_type_by_coord(new_coord), Ant):
            new_coord = choice([(x, y) for x, y, _ in self.nhood(1)])
        return new_coord

    def attack(self, horizon):
        enemies_coord = self.get_horizon_with_enemies(1)
        if enemies_coord:
            return (choice(enemies_coord), 'hit')
        else:
            coord = min([(x, y) for x, y, _ in self.nhood(1)],
                       key=lambda coord: min(dist(enemy_coord, coord)
                                             for enemy_coord in horizon))
            return (coord, 'move')

    def move(self):
        if self.next_cell_for_patrol is None:
            self.set_next_cell_for_patrol()
        horizon = self.get_horizon_with_enemies(radius=3)
        if horizon:
            return self.attack(horizon)
        else:
            if self.base.API.get_coord_by_obj(self) == self.next_cell_for_patrol:
                self.set_next_cell_for_patrol()
            new_coord = self.patrol()
            return (new_coord, 'move')

class BasicHarvester(BasicAnt):
    max_food_time = 10

    def __init__(self, base):
        Ant.__init__(self, base)
        self.food_time = 0

    def move(self):
        def compute_next_move_for_ant_wo_food(ant):
            coord_new = choice(self.nhood(radius=1))[:2]
            obj_type = self.base.API.get_type_by_coord(coord_new)
            if issubclass(obj_type, Food):
                ant.food_time = type(self).max_food_time
                return (coord_new, 'take_food')
            elif issubclass(obj_type, type(None)):
                return (coord_new, 'move')
            else:
                # если в клетке не пусто и нет еды -- значит, туда нельзя идти
                return (self.base.API.get_coord_by_obj(self), 'move')

        def compute_next_move_for_ant_w_food(ant):
            nhood = self.nhood(1)
            API = self.base.API
            base_coord, ant_coord = API.get_coord_by_obj(self.base), API.get_coord_by_obj(self)
            if base_coord in [(x, y) for x, y, _ in nhood]:
                return (base_coord, 'drop_food')

            nhood = [(x, y) for x, y, t in nhood if not issubclass(t, Base) and not issubclass(t, Ant)]
            try:
                coord_new = min(nhood, key=lambda coord: dist(coord, base_coord))
            except IndexError:
                coord_new = ant_coord

            if ant.food_time > 1:
                ant.food_time -= 1
                move = 'move'
            else:
                ant.food_time = 0
                move = 'drop_food'

            return (coord_new, move)

        return compute_next_move_for_ant_w_food(self) if self.base.API.cargo_load(self) > 0 \
                    else compute_next_move_for_ant_wo_food(self)