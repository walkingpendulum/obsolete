# -*- coding: utf-8 -*-

class Base(object):
    '''Базовый класс муравейника. Кастомные классы муравейников должны быть отнаследованы от него.'''
    label = 'B'

    def __init__(self, API, team_id):
        self.team_id = team_id
        self.API = API

    def advance(self):
        '''Обработка события "ход базы". Тут можно парсить поле, оценивать обстановку, создавать муравьев'''
        pass
