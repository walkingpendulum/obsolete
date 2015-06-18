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
    hit_prob = 0.5      # вероятность убить муравья при ударе
    cost_of_ant = 5     # стоимость создания одного муравья
    food_prob = 0.3     # вероятность появления еды в клетке при создании планеты
    food_min_quantity = 3
    food_max_quantity = 7

    def __init__(self, size):
        self.size = size
        self.dict_of_objects_coord = dict()    # по объекту дает его координаты как кортеж
        self.cargo = dict()   # по муравью дает его загрузку (едой)
        self.land = dict()
        self.teams = dict()     # по id команды дает объект AntWarsTeam

        for coord in product(*map(range, self.size)):
            self.land[coord] = None
            if 0 <= uniform(0,1) < type(self).food_prob:
                food_max, food_min = type(self).food_max_quantity, type(self).food_min_quantity
                self.land[coord] = Food(randint(food_min, food_max))

    def Init(self, teams):
        for team in teams:
            team.base = team.BaseClass(API=AntWarsAPI(planet=self),
                                       team_id=team.team_id)
            team.food = 3 * type(self).cost_of_ant
            self.teams[team.team_id] = team

        # рандомим места для баз, размещаем их там и инициализируем
        coord_for_bases = sample(self.land, len(teams))
        bases = map(lambda team: team.base, self.teams.itervalues())
        for base, coord in zip(bases, coord_for_bases):
            base.API.Init(base)
            self.land[coord] = base
            self.set_coord(obj=base, coord=coord)

    def set_coord(self, obj, coord):
        self.dict_of_objects_coord[obj] = coord

    def hit(self, dst_coord, ant):
        enemy = self.land.get(dst_coord, None)
        if not isinstance(enemy, Ant):
            return
        else:
            if 0 <= uniform(0, 1) <= type(self).hit_prob:
                # удаляем муравья отовсюду
                self.teams[enemy.base.team_id].ants_set.difference_update({enemy})
                self.dict_of_objects_coord.pop(enemy)
                self.cargo.pop(enemy, default=None)

    def drop_food(self, dst_coord, ant):
        obj = self.land.get(dst_coord, None)
        if self.cargo.get(ant, 0):
            self.cargo[ant] = 0
            if isinstance(obj, Base):
                self.teams[obj.team_id].food += 1
            elif isinstance(obj, Food):
                obj.food += 1
            elif isinstance(obj, Ant):
                if not self.cargo.get(obj, 0):
                    self.cargo[obj] = 1
            elif dst_coord in self.land:
                self.land[dst_coord] = Food(1)

    def take_food(self, dst_coord, ant):
        obj = self.land.get(dst_coord, None)
        if isinstance(obj, Food):
            self.cargo[ant] = 1
            if obj.food == 1:
                self.land[dst_coord] = None
            elif obj.food > 1:
                obj.food -= 1

    def move(self, dst_coord, ant):
        old_coord = self.dict_of_objects_coord[ant]
        # todo: может быть стоит не пропускать ход в planet.move(), если перемещение некорректное, а бросать исключение?
        if dst_coord not in self.land:
            return
        elif old_coord == dst_coord:
            return
        elif isinstance(self.land[dst_coord], Ant):
            return
        elif isinstance(self.land[dst_coord], Base):
            return
        else:
            old_coord = self.dict_of_objects_coord[ant]
            self.land[old_coord] = None
            self.land[dst_coord] = ant
            self.set_coord(obj=ant, coord=dst_coord)

    def advance(self):
        '''Ход планеты, он же игровой день'''
        for team in self.teams.itervalues():
            team.base.advance()
            for ant in team.ants_set:
                dst_coord, move = ant.move()
                # todo: вставить проверку на то, что муравей не прыгнул дальше одной клетки
                getattr(self, move)(dst_coord, ant)

    def __str__(self):
        Buffer = list()
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                figure = self.land[x, y]
                label = ' ' if figure == None \
                    else Food.label if isinstance(figure, Food) \
                    else Base.label if isinstance(figure, Base) \
                    else str(figure.base.team_id)
                Buffer.append(label)
            Buffer.append('\n')

        ext_inf = list()
        for team_ind in self.teams:
            ext_inf.append('Team %d: food %d, ants %d\n' %
                           (team_ind,
                            self.teams[team_ind].food,
                            len(self.teams[team_ind].ants_set)))
        Buffer.extend(ext_inf)
        return "".join(Buffer)
