# -*- coding: utf-8 -*-

class Base(object):
    '''Базовый класс муравейника. Кастомные классы муравейников должны быть отнаследованы от него.'''
    label = 'B'

    def __init__(self):
        self.team_id = None
        self.API = None

    def Init(self, API):
        self.API = API
        self.team_id = API.get_team_id_by_base(self)

    def advance(self):
        '''Обработка события "ход базы". Тут можно парсить поле, оценивать обстановку, создавать муравьев'''
        pass
