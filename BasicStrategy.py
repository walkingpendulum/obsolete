'''
    ant.move() -> (destination_coord, move)
    moves: 'hit', 'move', 'take_food', 'drop_food'

'''
from random import choice

from planet import Food, Base, Ant
from planet import AntWarsAPI


class BasicBase(Base):
    max_ant_quantity = 7

    def __init__(self, team):
        Base.__init__(self, team)
        # smth else you want to

    def advance(self):
        if len(self.catalog) < type(self).max_ant_quantity \
                           and type(self.planet).cost_of_ant <= self.food:
            self.API.spawn(base=self)

class BasicAnt(Ant):
    max_food_time = 10

    def __init__(self, base):
        Ant.__init__(self, base)
        self.food_time = 0

    def move(self):
        def compute_next_coord_by_str_with_step(x, y, str_with_step=None):
            add = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)}
            cell = self.base.locate
            x_new, y_new = x + add[str_with_step][0], y + add[str_with_step][1]
            x_max, y_max = self.base.planet.size[0], self.base.planet.size[1]

            if not (0 <= x_new < x_max and 0 <= y_new < y_max):
                # cannot go out of game field -- passed turn
                return x, y

            if not isinstance(cell(x_new, y_new), Ant):                 
                return (x_new, y_new)
            else:
                return (x, y)
                    
        def compute_next_move_for_ant_wo_food(ant):
            next_step = choice(['up', 'down', 'left', 'right'])
            coord_new = compute_next_coord_by_str_with_step(*ant.coord, str_with_step=next_step)
            cell = self.base.locate

            if isinstance(cell(*coord_new), Food):
                ant.has_food = True
                ant.food_time = BasicAnt.max_food_time
                return (coord_new, 'take_food')
            elif cell(*coord_new) is None:
                return (coord_new, 'move')
            else:
                # there are not food nor nothing in cell -- passed turn
                return (self.coord, 'move')
                    
        def compute_next_move_for_ant_w_food(ant):
            strings = ['down', 'left'] if ant.base.coord[0] == 0 else ['up', 'right']
            coord_new = compute_next_coord_by_str_with_step(*ant.coord, str_with_step=choice(strings))

            if coord_new == ant.base.coord: # reached our base
                ant.has_food = False
                ant.food_time = 0
                return (coord_new, 'drop_food')

            # still on our way and food is fresh enough
            if ant.food_time > 1:
                ant.food_time -= 1
                return (coord_new, 'move')
            else: 
                ant.has_food = False
                ant.food_time = 0
                move = 'move' if coord_new == ant.coord else 'drop_food'
                return (coord_new, move)

        return compute_next_move_for_ant_w_food(self) if self.has_food \
                    else compute_next_move_for_ant_wo_food(self)
