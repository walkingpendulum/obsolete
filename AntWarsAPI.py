# -*- coding: utf-8 -*-
from random import choice
from itertools import product


class AntWarsAPI(object):
    planet = None

    def __init__(self, planet):
        type(self).planet = planet
        self.team = None

    def Init(self, base):
        planet = type(self).planet
        self.team = type(self).planet.teams_by_base[base]

    def get_team_id_by_base(self, base):
        planet = type(self).planet
        return planet.teams_by_base[base].team_id

    def ask_for_spawn(self, AntClass=type(None)):
        '''Обработка события "создать муравья". Возвращает True, если удалось, False иначе '''

        planet = type(self).planet
        AntClass = self.team.AntClass if AntClass is type(None) else AntClass
        x_base, y_base = planet.coord_by_obj[self.team.base]
        x_max, y_max = planet.size

        # если ресурсов достаточно для создания
        if self.team.food >= type(planet).cost_of_ant:
            # может случиться, что возле базы нет свободной клетки
            try:
                x, y = choice([(x_base + dx, y_base + dy)
                               for dx, dy in product(range(-1, 2), repeat=2)
                               if (x_base + dx, y_base + dy) in planet.obj_by_coord
                               and planet.obj_by_coord.get((x_base + dx, y_base + dy), None) is None])
                ant = AntClass(base=self.team.base)
                self.team.ants_set.update({ant})
                planet.set_coord(obj=ant, coord=(x, y))
                planet.obj_by_coord[x, y] = ant
                self.team.food -= type(planet).cost_of_ant
                return True
            except IndexError:
                return False
        else:
            return False

    def get_list_of_ants(self):
        return list(self.team.ants_set)

    def get_food_quantity(self):
        return self.team.food

    def get_size_of_planet(self):
        return type(self).planet.size

    def get_cost_of_ant_spawn(self):
        planet = type(self).planet
        return planet.cost_of_ant

    def get_type_from_cell(self, *coords):
        planet = type(self).planet
        if len(coords) == 1:    # дали кортеж (x, y)
            coords = coords[0]
        return type(planet.obj_by_coord.get(coords, None))

    def get_coord(self, obj):
        '''Возвращает кортеж координат объекта одного из классов: Ant, Base. Если объект не найден, вернет None '''
        planet = type(self).planet
        return planet.coord_by_obj.get(obj, None)

    def cargo_load(self, ant):
        planet = type(self).planet
        return planet.cargo_by_ant.get(ant, 0)