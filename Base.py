# -*- coding: utf-8 -*-
from AntWarsAPI import AntWarsAPI


class Base(object):
    '''Базовый класс муравейника. Кастомные классы муравейников должны быть отнаследованы от него.'''
    label = 'B'

    def __init__(self, team):
        '''
        :param team: идентификатор, используется для различения команд. str(team) должно содержать ровно один символ
        :return:
        '''
        self.team = team
        self.API = AntWarsAPI(base=self)

    def advance(self):
        '''Обработка события "ход базы". Тут можно парсить поле, оценивать обстановку, создавать муравьев'''
        pass
