# -*- coding: utf-8 -*-

from itertools import chain
from random import uniform, randint, choice


class Ant(object):
    '''Базовый класс муравья. Кастомные классы муравьев должны быть отнаследованы от него.'''

    def __init__(self, coord, base):
        '''
        :param coord: координаты муравья, кортеж (x, y).
        :param base: экземпляр класса Base, муравейник, к которому принадлежит муравей.
        :return:
        '''
        self.base = base
        self.coord = coord
        self.has_food = False

    def move(self):
        '''Должен вернуть ход муравья -- кортеж (destination_coord, строка с типом хода)'''
        return self.coord + ('move', )


class Base(object):
    '''Базовый класс муравейника. Кастомные классы муравейников должны быть отнаследованы от него.'''
    label = 'B'

    # todo: база не должна знать про планету, не должна иметь доступ к клеткам для изменения. \
    # todo: можно завести новый класс, который и будем просить о spawn, size, locate
    def __init__(self, AntClass, coord, planet, team):
        '''
        :param AntClass: кастомный класс муравьев
        :param coord: кортеж (x, y)
        :param planet: экземпляр класса Planet, чье поле будет использовано для расположения фигур
        :param team: идентификатор, используется для различения команд. str(team) должно содержать ровно один символ
        :return:
        '''
        self.AntClass = AntClass
        self.coord = coord
        self.planet = planet
        self.team = team
        self.food = 3 * Planet.cost_of_ant      # количество собранной еды
        self.catalog = set()        # множество всех живых муравьев этой команды

    def locate(self, x, y): # todo: врагам нужно отдавать копию. а вообще лучше отдавать тип
        '''По координатам возвращает объект, хранимый планетой в клетке с этими координатами'''
        return self.planet.cell(x, y).data

    def advance(self):
        '''Обработка события "ход базы". Тут можно парсить поле, оценивать обстановку, создавать муравьев'''
        pass

    def spawn(self):
        ''' Обработка события "создать муравья". Возвращает True, если удалось, False иначе '''
        cell = self.locate
        x0, y0 = self.coord
        x_max, y_max = self.planet.size

        # если ресурсов достаточно для создания
        if self.food >= type(self.planet).cost_of_ant:
            # может случиться, что возле базы нет своодной клетки
            try:
                x, y = choice([(x0 + dx, y0 + dy) for dx in range(-1, 2) for dy in range(-1, 2)
                               if 0 <= x0 + dx < x_max and 0 <= y0 + dy < y_max
                               and not isinstance(cell(x0 + dx, y0 + dy), (Base, Ant))])
                ant = self.AntClass(coord=(x, y), base=self)
                self.catalog.update({ant})
                self.planet.cell(x, y).set(ant)
                return True
            except IndexError:
                return False
        else:
            return False


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
        self.Base1 = BaseClass1(AntClass=AntClass1,
                          coord=(0, 0),     # муравейник первой команды всегда в левом верхнем углу
                          planet=self,
                          team=1)
        self.Base2 = BaseClass2(AntClass=AntClass2,
                          coord=(self.size[0] - 1, self.size[1] - 1),   # муравейник второй в правом нижнем
                          planet=self,
                          team=2)

        self.land = []
        for y in range(self.size[1]):
            self.land.append([])
            for x in range(self.size[0]):
                coord = (x, y)
                cell = Cell(coord, self)
                if coord == self.Base1.coord:
                    cell.set(self.Base1)
                elif coord == self.Base2.coord:
                    cell.set(self.Base2)
                elif 0 <= uniform(0,1) < Food.prob:     # рандомим еду
                    cell.set(Food(randint(1, 5)))       # здесь магические константы для количества еды
                self.land[y].append(cell)
            self.land[y] = tuple(self.land[y])        # игровое поле -- двумерный кортеж из клеток
        self.land = tuple(self.land)

    def cell(self, x, y):
        '''Обертка для доступа к клетке по координатам без четырех квадратных скобочек'''
        return self.land[y][x]

    def advance(self):
        '''Ход планеты, он же игровой день'''

        def hit_move(base, enemy_base, destination_coord, ant):
            '''обработка события "муравей бьет муравья чужой команды"'''
            if 0 <= uniform(0, 1) <= self.hit_prob:
                enemy = self.cell(*destination_coord).data()
                # удаляем муравья из каталога чужой базы
                enemy_base.catalog.difference_update({enemy})

        def move_move(base, enemy_base, destination_coord, ant):
            self.cell(*ant.coord).set(None)
            ant.coord = destination_coord
            self.cell(*ant.coord).set(ant)

        def drop_food_move(base, enemy_base, destination_coord, ant):
            # todo: переброска еды на соседа без потери хода последним

            if destination_coord == base.coord:
                base.food += 1
            elif destination_coord == enemy_base.coord:
                enemy_base.food += 1
            elif isinstance(self.cell(*destination_coord), Food):
                self.cell(*destination_coord).data.quantity += 1
            else:
                self.cell(*destination_coord).set(Food(1))

        def take_food_move(base, enemy_base, destination_coord, ant):
            if self.cell(*destination_coord).data.quantity == 1:
                # еда было мало, обнуляем клетку
                self.cell(*destination_coord).set(None)
            elif self.cell(*destination_coord).data.quantity > 1:
                # еды много, просто уменьшаем количество на единицу
                self.cell(*destination_coord).data.quantity -= 1

        def update_base(base, enemy_base):
            move_functions = {'hit': hit_move, \
                     'move': move_move, \
                     'drop_food': drop_food_move, \
                     'take_food': take_food_move}

            ant_quantity_old = len(base.catalog)
            base.advance()      # ход базы. могут появляться новые муравьи, нужно вычесть денег
            ant_quantity_new = len(base.catalog)
            ant_quantity_diff = ant_quantity_new - ant_quantity_old
            if ant_quantity_diff > 0:
                base.food -= ant_quantity_diff * Planet.cost_of_ant

            for ant in base.catalog:
                destination_coord, move = ant.move()

                # поверхностная проверка на корректность хода
                if self.move_checker(ant.coord, destination_coord, move, base, enemy_base) is True:
                    move_functions[move](base, enemy_base, destination_coord, ant)
                else:
#                    print 'Uncorrect move detected, ant skipped'
                    continue

        # собственно, ходы баз
        update_base(self.Base1, self.Base2)
        update_base(self.Base2, self.Base1)                    

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
        Buffer.append('Base 1: ' + str(self.Base1.food) + '  Base 2: ' + str(self.Base2.food))
        return "".join(Buffer)

    def __repr__(self):
        return str(self)

    def move_checker(self, old_coord, destination_coord, move, base, enemy_base):
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

        # todo: это можно ловить на уровне планеты и не делать ничего
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
        if move == 'move' and ((x, y) == enemy_base.coord \
                               or (x, y) == base.coord):
#            print "tried to step down base someone's. too smal for that", x, y
            return False

        # сброс еды в клетку, где есть муравей.
        # todo: если муравей свой, нужно сделать фичу: передача еды
        if move == 'drop_food' and \
           isinstance(cell(x, y), Ant):
#            print 'tried to kill other ant by sugar. bad boy', x, y
            return False

        return True
