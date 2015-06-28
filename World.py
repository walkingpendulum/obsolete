# -*- coding: utf-8 -*-

from itertools import product
from random import uniform, randint, sample, choice
from Ant import Ant
from Base import Base
from API import API

class Food(object):
    '''Обертка для еды'''
    label = 'f'

    def __init__(self, food):
        self.food = food

class Team(object):
    '''Обертка вокруг набора данных, относящихся к одной из команд'''
    def __init__(self, AntClass, BaseClass, team_id):
        self.AntClass = AntClass
        self.BaseClass = BaseClass
        self.team_id = team_id
        self.food = 0
        self.base = None
        self.ants_set = set()

class World(object):
    '''Игровой мир: игровое поле, обработка ходов команд, перемещение муравьев'''
    hit_prob = 0.9      # вероятность убить муравья при ударе
    cost_of_ant = 5     # стоимость создания одного муравья
    start_food_multiplier = 3   # на сколько муравьев хватит стартовой еды 
    food_prob = 0.3     # вероятность появления еды в клетке при создании планеты
    food_min_start_quantity_in_cell = 3     #магические константы при рандоме еды для размещения в клетку
    food_max_start_quantity_in_cell = 7

    def __init__(self, size, log_name):
        self.log_name = log_name
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
        team.food = type(self).start_food_multiplier * type(self).cost_of_ant

    def Init(self, teams):
        for team in teams:
            self.add_team(team)

        # рандомим места для баз, размещаем их там и инициализируем
        coord_for_bases = sample(self.obj_by_coord, len(teams))
        for base, coord in zip(self.teams_by_base, coord_for_bases):
            API_for_setup = API(world=self)
            API_for_setup.Init(base)
            base.Init(API=API_for_setup)
            self.set_obj_coord_relation(obj=base, coord=coord)

    def set_obj_coord_relation(self, obj, coord):
        self.coord_by_obj[obj] = coord
        self.obj_by_coord[coord] = obj

    def del_obj(self, obj):
        self.obj_by_coord[self.coord_by_obj[obj]] = None
        del self.coord_by_obj[obj]

    def hit(self, dst_coord, ant):
        enemy = self.obj_by_coord.get(dst_coord, None)
        if not isinstance(enemy, Ant):
            return
        else:
            if 0 <= uniform(0, 1) <= type(self).hit_prob:
                # удаляем муравья отовсюду
                self.teams_by_base[enemy.base].ants_set.difference_update({enemy})
                self.del_obj(enemy)
                self.cargo_by_ant.pop(enemy, None)

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
        # todo: может быть стоит не пропускать ход в world.move(), если перемещение некорректное, а бросать исключение?
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
            self.set_obj_coord_relation(obj=ant, coord=dst_coord)

    def spawn(self, team, AntClass=type(None)):
        '''Обработка события "создать муравья". Возвращает True, если удалось, False иначе '''

        AntClass = team.AntClass if AntClass is type(None) else AntClass
        x_base, y_base = self.coord_by_obj[team.base]

        # если ресурсов достаточно для создания
        if team.food >= type(self).cost_of_ant:
            # может случиться, что возле базы нет свободной клетки
            try:
                coord = choice([(x_base + dx, y_base + dy)
                               for dx, dy in product(range(-1, 2), repeat=2)
                               if (x_base + dx, y_base + dy) in self.obj_by_coord
                               and self.obj_by_coord.get((x_base + dx, y_base + dy), None) is None])
                ant = AntClass(base=team.base)
                team.ants_set.update({ant})
                self.set_obj_coord_relation(obj=ant, coord=coord)
                team.food -= type(self).cost_of_ant
                return True
            except IndexError:
                return False
        else:
            return False

    def advance(self):
        '''Ход планеты, он же игровой день'''
        for team in self.teams_by_base.itervalues():
            team.base.advance()
            for ant in team.ants_set:
                dst_coord, move = ant.move()
                # todo: вставить проверку на то, что муравей не прыгнул дальше одной клетки
                getattr(self, move)(dst_coord, ant)

        # срабатывает, если при запуске был задан флаг --logs
        self.dump()

    def dump(self):
        ''' Сбрасывает текущее состояние поля str(world) в файл filename.'''
        # если при запуске флаг "--logs" не был указан, то self.log_name == None
        if self.log_name:
            with open(self.log_name, mode='a') as f:
                f.write(str(self).replace('\n', '$') + '\n')

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
