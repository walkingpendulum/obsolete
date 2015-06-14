# -*- coding: utf-8 -*-
from Planet import test_Planet


class AntWarsAPI(object):
    planet = test_Planet

    def __init__(self, base):
        planet = type(self).planet
        dicts_of_teams = {planet.team1['base']: planet.team1, planet.team2['base']: planet.team2}

        self.team = dicts_of_teams[base]

    def ask_for_cell(self, *coords):
        '''Возвращает тип данных, хранящихся в клетке с заданными координатами

        :param coords: кортеж (x, y) либо пара координат x, y
        :return:
        '''
        planet = type(self).planet
        if len(coords) == 1:
            coords = coords[0]
        return type(planet.cell(*coords))

    # todo: в ask_for_spawn нужно отдавать подкласс муравья, который игрок решил спавнить
    def ask_for_spawn(self, AntClass):
        '''Обработка события "создать муравья". Возвращает True, если удалось, False иначе '''

        planet = type(self).planet
        x0, y0 = self.team['base'].coord
        x_max, y_max = planet.size

        # если ресурсов достаточно для создания
        if self.team['food'] >= type(planet).cost_of_ant:
            # может случиться, что возле базы нет свободной клетки
            try:
                x, y = choice([(x0 + dx, y0 + dy) for dx in range(-1, 2) for dy in range(-1, 2)
                               if 0 <= x0 + dx < x_max and 0 <= y0 + dy < y_max
                               and not isinstance(self.cell(x0 + dx, y0 + dy), (Base, Ant))])
                ant = AntClass(coord=(x, y), base=base)
                self.team['ants'].update({ant})
                planet.land[y][x].set(ant)
                return True
            except IndexError:
                return False
        else:
            return False

    def ask_for_ants(self):
        return list(self.team['ants'])

    def ask_for_coord(self, obj):
        '''Возвращает кортеж координат объекта одного из классов: Ant, Base. Если объект не найден, вернет None '''
        planet = type(self).planet
        return planet.coords.get(obj, None)
