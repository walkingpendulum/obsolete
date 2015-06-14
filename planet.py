# -*- coding: utf-8 -*-

from itertools import chain
from random import uniform, randint, choice
from Ant import *
from Base import *


class Food(object):
    '''Класс-обертка для еды.'''
    prob = 0.3      # вероятность появления в клетке при создании планеты
    label = 'f'

    def __init__(self, quantity):
        '''
        :param quantity: количество хранимых ресурсов
        :return:
        '''
        self.quantity = quantity


class Cell(object):
    '''Клетки, из которых составлено игровое поле'''

    # todo: клетке не нужно знать планету
    def __init__(self, coord, planet):
        '''
        :param coord:
        :param planet: экземпляр планеты, на чьем поле клетка расположена
        :return:
        '''
        self.planet = planet
        self.coord = coord
        self.data = None

    def set(self, data):
        '''Поместить объект в клетку'''
        self.data = data


class Planet(object):
    '''Игровой мир: игровое поле, обработка ходов команд, перемещение муравьев'''
    hit_prob = 0.5      # вероятность убить муравья при ударе
    cost_of_ant = 5     # стоимость создания одного муравья

    def __init__(self, size, AntClass1, AntClass2, BaseClass1, BaseClass2):
        '''
        :param size: размеры игрового поля (x_size, y_size)
        :param AntClass1: кастомный класс муравья для первой команды
        :param AntClass2: кастомный класс муравья для второй команды
        :param BaseClass1: кастомный класс муравейника для первой команды
        :param BaseClass2: кастомный класс муравейника для второй команды
        :return:
        '''
        self.size = size
        self.coords = dict()    # словарь, по объекту дает его координаты как кортеж

        # todo: нужно что-то сделать с дублированием поля team и полей team1-team2, пока остается из-за вывода на консоль
        self.team1 = {'base': BaseClass1(team=1),
                      'AntClass': AntClass1,
                      'BaseClass': BaseClass1,
                      'food': 3 * type(self).cost_of_ant,
                      'ants': set()}
        self.team2 = {'base': BaseClass2(team=2),
                      'AntClass': AntClass2,
                      'BaseClass': BaseClass2,
                      'food': 3 * type(self).cost_of_ant,
                      'ants': set()}

        self.land = [] # todo: можно сделать land не списком, а словарем, тогда проще будет обрабатывать некорректные кооординаты
        for y in range(self.size[1]):
            self.land.append([])
            for x in range(self.size[0]):
                coord = (x, y)
                cell = Cell(coord, self)
                # todo: муравейники тоже могут быть где угодно!
                if coord == (0, 0):  # первый муравейник в левом верхнем углу
                    self.set_coord(self.team1['base'], coord)
                    cell.set(self.team1['base'])
                elif coord == (self.size[0] - 1, self.size[1] - 1):     # второй муравейник в правом нижнем
                    self.set_coord(self.team2['base'], coord)
                    cell.set(self.team2['base'])
                elif 0 <= uniform(0,1) < Food.prob:     # рандомим еду
                    cell.set(Food(randint(1, 5)))       # здесь магические константы для количества еды
                self.land[y].append(cell)
            self.land[y] = tuple(self.land[y])        # игровое поле -- двумерный кортеж из клеток
        self.land = tuple(self.land)

    @staticmethod
    def testPlanet():
        return Planet(size=(10, 10), AntClass1=Ant, AntClass2=Ant, BaseClass1=Base, BaseClass2=Base)

    # todo: этот метод планете не нужен, перенести в API, удалив зависимости
    def cell(self, x, y):
        '''Обертка для доступа к клетке по координатам без четырех квадратных скобочек'''
        return self.land[y][x]

    def set_coord(self, obj, coord):
        self.coords[obj] = coord

    def advance(self):
        '''Ход планеты, он же игровой день'''

        def hit_move(team_dict, enemy_team_dict, destination_coord, ant):
            '''обработка события "муравей бьет муравья чужой команды"'''
            if 0 <= uniform(0, 1) <= self.hit_prob:
                enemy = self.cell(*destination_coord).data()
                # удаляем муравья из каталога чужой базы
                enemy_team_dict['ants'].difference_update({enemy})

        def move_move(team_dict, enemy_team_dict, destination_coord, ant):
            self.cell(*ant.coord).set(None)
            ant.coord = destination_coord
            self.cell(*ant.coord).set(ant)

        def drop_food_move(team_dict, enemy_team_dict, destination_coord, ant):
            cell = self.cell(*destination_coord)
            ant.has_food = False

            if destination_coord == base.coord:
                base.food += 1
            elif destination_coord == enemy_base.coord:
                enemy_team_dict['food'] += 1
            elif isinstance(cell.data, Food):
                cell.data.quantity += 1
            # фича: если скинули на пустого муравья, то он берет без потери своего хода
            elif isinstance(cell.data, Ant):
                cell.data = other_ant
                if not other_ant.has_food:
                    ant.has_food = True
            else:
                cell.set(Food(1))

        def take_food_move(team_dict, enemy_team_dict, destination_coord, ant):
            cell = self.cell(*destination_coord)

            # попытка взять еду там, где ее нету -- ничего не делаем
            if not isinstance(cell.data, Food):
                return
            elif cell.data.quantity == 1:
                # еды было мало, обнуляем клетку
                cell.set(None)
            elif cell.data.quantity > 1:
                # еды много, просто уменьшаем количество на единицу
                cell.data.quantity -= 1

        def update_base(team_dict, enemy_team_dict):
            move_functions = {'hit': hit_move, \
                     'move': move_move, \
                     'drop_food': drop_food_move, \
                     'take_food': take_food_move}

            # todo: теперь создание муравьев обрабатывается в API, пусть там и вычитаются деньги
            ant_quantity_old = len(team_dict['ants'])
            team_dict['base'].advance()      # ход базы. могут появляться новые муравьи, нужно вычесть денег
            ant_quantity_new = len(team_dict['ants'])
            ant_quantity_diff = ant_quantity_new - ant_quantity_old
            if ant_quantity_diff > 0:
                team_dict['food'] -= ant_quantity_diff * type(self).cost_of_ant

            for ant in team_dict['ants']:
                destination_coord, move = ant.move()

                # поверхностная проверка на корректность хода
                if self.move_checker(ant.coord,
                                     destination_coord,
                                     move,
                                     team_dict,
                                     enemy_team_dict) is True:
                    move_functions[move](team_dict, enemy_team_dict, destination_coord, ant)
                else:
#                    print 'Uncorrect move detected, ant skipped'
                    continue

        # собственно, ходы баз
        update_base(self.team1, self.team2)
        update_base(self.team2, self.team1)

    def __str__(self):
        Buffer = []
        ind = 0
        for cell in chain.from_iterable(self.land):
            figure = cell.data
            label = ' ' if figure == None \
                else Food.label if isinstance(figure, Food) \
                else Base.label if isinstance(figure, Base) \
                else str(figure.base.team)
            Buffer.append(label)

            ind += 1
            if ind == len(self.land[0]):
                Buffer.append('\n')
                ind = 0
        additional_inf = []
        additional_inf.append('Team 1: food %d, ants %d\n' % (self.team1['food'], len(self.team1['base'].catalog)))
        additional_inf.append('Team 2: food %d, ants %d\n' % (self.team2['food'], len(self.team2['base'].catalog)))
        Buffer.extend(additional_inf)
        return "".join(Buffer)

    def __repr__(self):
        return str(self)

    def move_checker(self, old_coord, destination_coord, move, team_dict, enemy_team_dict):
        '''Поверхностная проверка хода move на корректность'''
        cell = lambda x, y: self.cell(x, y).data
        x, y = destination_coord

        # выход за пределы поля
        if not (0 <= x < self.size[0] and 0 <= y < self.size[1]):
#            print 'your ant goes too far. fare thee well, brave ant', x, y
            return False

        # перемещение дальше, чем на одну клетку
        if not (x - 2 < old_coord[0] < x + 2 and y - 2 < old_coord[1] < y + 2):
#            print "Ant cannot fly but for jump that was too long distance", x, y
            return False

        if move == 'take_food' and not isinstance(cell(x, y), Food):
#            print 'take food from empty place', x, y
            return False

        # перемещение на клетку, в которой есть муравей
        if move == 'move' and isinstance(cell(x, y), Ant):
            # остаться на месте -- корректный ход
            if (x, y) == old_coord:
                return True
            else:
#                print 'tried to step down over other ant. you are monster himself', x, y
                return False

        # перемещение на клетку, в которой стоит база
        if move == 'move' and ((x, y) == enemy_team_dict['base'].coord \
                               or (x, y) == team_dict['base'].coord):
#            print "tried to step down on the base. too smal for that", x, y
            return False

        return True

test_Planet = Planet(size=(10, 10), AntClass1=Ant, AntClass2=Ant, BaseClass1=Base, BaseClass2=Base)