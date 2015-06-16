# -*- coding: utf-8 -*-

class Ant(object):
    '''Базовый класс муравья. Кастомные классы муравьев должны быть отнаследованы от него.'''

    def __init__(self, base):
        self.base = base

    # todo: ходить должна только база, она будет отдавать словарь {ant: move}? метод move муравью не нужен?
    def move(self):
        '''Возвращает ход муравья -- кортеж (destination_coord, строка с типом хода)'''
        return (self.base.API.get_coord(self), 'move')
