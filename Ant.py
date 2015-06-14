# -*- coding: utf-8 -*-

class Ant(object):
    '''Базовый класс муравья. Кастомные классы муравьев должны быть отнаследованы от него.'''

    def __init__(self, base):
        '''
        :param coord: координаты муравья, кортеж (x, y).
        :param base: экземпляр класса Base, муравейник, к которому принадлежит муравей.
        :return:
        '''
        self.base = base
        # todo: игрок не должен контролировать, есть ли у муравья еда
        self.has_food = False

    # todo: ходить должна только база, она будет отдавать словарь {ant: move}. метод move муравью не нужен
    def move(self):
        '''Должен вернуть ход муравья -- кортеж (destination_coord, строка с типом хода)'''
        return (self.base.API.ask_for_coord(self), 'move')
