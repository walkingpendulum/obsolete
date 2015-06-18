# -*- coding: utf-8 -*-

from itertools import product
from random import uniform, randint, sample
from Ant import Ant
from Base import Base
from AntWarsAPI import AntWarsAPI


class Food(object):
    '''Обертка для еды'''
    label = 'f'

    def __init__(self, food):
        self.food = food

class AntWarsTeam(object):
    '''Обертка вокруг набора данных, относящихся к одной из команд'''
    def __init__(self, AntClass, BaseClass, team_id):
        self.AntClass = AntClass
        self.BaseClass = BaseClass
        self.team_id = team_id
        self.food = 0
        self.base = None
        self.ants_set = set()

class Planet(object):
    '''Игровой мир: игровое поле, обработка ходов команд, перемещение муравьев'''
    hit_prob = 0.8      # вероятность убить муравья при ударе
    cost_of_ant = 5     # стоимость создания одного муравья
    food_prob = 0.3     # вероятность появления еды в клетке при создании планеты
    food_min_start_quantity_in_cell = 3
    food_max_start_quantity_in_cell = 7

    def __init__(self, size):
        self.size = size
        self.coord_by_obj = dict()
        self.obj_by_coord = dict()
        self.teams_by_base = dict()
        self.cargo_by_ant = dict()   # по муравью дает его загрузку (едой)

        for coord in product(*map(range, self.size)):
            self.obj_by_coord[coord] = None
            if 0 <= uniform(0,1) < type(self).food_prob:
                self.obj_by_coord[coord] = Food(randint(type(self).food_min_start_quantity_in_cell,
                                                        type(self).food_max_start_quantity_in_cell))
    def add_team(self, team):
        team.base = team.BaseClass()
        self.teams_by_base[team.base] = team
        team.food = 3 * type(self).cost_of_ant

    def Init(self, teams):
        for team in teams:
            self.add_team(team)

        # рандомим места для баз, размещаем их там и инициализируем
        coord_for_bases = sample(self.obj_by_coord, len(teams))
        for base, coord in zip(self.teams_by_base, coord_for_bases):
            API_for_setup = AntWarsAPI(planet=self)
            API_for_setup.Init(base)
            base.Init(API=API_for_setup)
            self.obj_by_coord[coord] = base
            self.set_coord(obj=base, coord=coord)

    def set_coord(self, obj, coord):
        self.coord_by_obj[obj] = coord

    def hit(self, dst_coord, ant):
        enemy = self.obj_by_coord.get(dst_coord, None)
        if not isinstance(enemy, Ant):
            return
        else:
            if 0 <= uniform(0, 1) <= type(self).hit_prob:
                # удаляем муравья отовсюду
                self.teams_by_base[enemy.base].ants_set.difference_update({enemy})
                self.coord_by_obj.pop(enemy)
                self.cargo_by_ant.pop(enemy, default=None)

    def drop_food(self, dst_coord, ant):
        obj = self.obj_by_coord.get(dst_coord, None)
        if self.cargo_by_ant.get(ant, 0):
            self.cargo_by_ant[ant] = 0
            if isinstance(obj, Base):
                self.teams_by_base[obj].food += 1
            elif isinstance(obj, Food):
                obj.food += 1
            elif isinstance(obj, Ant):
                if not self.cargo_by_ant.get(obj, 0):
                    self.cargo_by_ant[obj] = 1
            elif dst_coord in self.obj_by_coord:
                self.obj_by_coord[dst_coord] = Food(1)

    def take_food(self, dst_coord, ant):
        obj = self.obj_by_coord.get(dst_coord, None)
        if isinstance(obj, Food):
            self.cargo_by_ant[ant] = 1
            if obj.food == 1:
                self.obj_by_coord[dst_coord] = None
            elif obj.food > 1:
                obj.food -= 1

    def move(self, dst_coord, ant):
        old_coord = self.coord_by_obj[ant]
        # todo: может быть стоит не пропускать ход в planet.move(), если перемещение некорректное, а бросать исключение?
        if dst_coord not in self.obj_by_coord:
            return
        elif old_coord == dst_coord:
            return
        elif isinstance(self.obj_by_coord[dst_coord], Ant):
            return
        elif isinstance(self.obj_by_coord[dst_coord], Base):
            return
        else:
            old_coord = self.coord_by_obj[ant]
            self.obj_by_coord[old_coord] = None
            self.obj_by_coord[dst_coord] = ant
            self.set_coord(obj=ant, coord=dst_coord)

    def advance(self):
        '''Ход планеты, он же игровой день'''
        for team in self.teams_by_base.itervalues():
            team.base.advance()
            for ant in team.ants_set:
                dst_coord, move = ant.move()
                # todo: вставить проверку на то, что муравей не прыгнул дальше одной клетки
                getattr(self, move)(dst_coord, ant)

    def __str__(self):
        Buffer = list()
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                figure = self.obj_by_coord[x, y]
                label = ' ' if figure == None \
                    else Food.label if isinstance(figure, Food) \
                    else Base.label if isinstance(figure, Base) \
                    else str(figure.base.team_id)
                Buffer.append(label)
            Buffer.append('\n')

        ext_inf = list()
        for base in self.teams_by_base:
            ext_inf.append('Team %d: food %d, ants %d\n' %
                           (base.team_id,
                            self.teams_by_base[base].food,
                            len(self.teams_by_base[base].ants_set)))
        Buffer.extend(ext_inf)
        return "".join(Buffer)
