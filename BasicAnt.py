'''
    ant.move() -> (x_new, y_new, move)
    moves: 'hit', 'move', 'take_food', 'drop_food'

'''


from random import choice
from planet import Food, Base

class Ant(object):
    pass

class BasicAnt(Ant):
    planet = None
    max_food_time = 5

    def __init__(self, coord, base):
        self.base = base
        self.coord = coord
        self.has_food = False
        self.food_time = 0

    def move(self):
        def compute_next_coord_by_str_with_step(x, y, str_with_step=None):
            add = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)}
            cell = BasicAnt.planet.get_data_from_cell
            x_new, y_new = x + add[str_with_step][0], y + add[str_with_step][1]
            x_max, y_max = BasicAnt.planet.size[0], BasicAnt.planet.size[1]

            if not (0 <= x_new < x_max and 0 <= y_new < y_max):
                # cannot go out of game field -- passed turn
                return x, y

            if not isinstance(cell(x_new, y_new), Ant):                 
                return (x_new, y_new)
            else:
                return (x, y)
                    
        def compute_next_move_for_ant_wo_food(ant):
            next_step = choice(['up', 'down', 'left', 'right'])
            x_new, y_new = compute_next_coord_by_str_with_step(*ant.coord, str_with_step=next_step)
            cell = BasicAnt.planet.get_data_from_cell

            if isinstance(cell(x_new, y_new), Food):
                ant.has_food = True
                ant.food_share_time = BasicAnt.max_food_time
                return (x_new, y_new) + ('take_food',)
            elif cell(x_new, y_new) is None:
                return (x_new, y_new) + ('move',)
            else:
                # there are not food nor nothing in cell -- passed turn
                return self.coord + ('move',)
                    
        def compute_next_move_for_ant_w_food(ant):
            strings = ['down', 'left'] if ant.base.coord[0] == 0 else ['up', 'right']
            x_new, y_new = compute_next_coord_by_str_with_step(*ant.coord, str_with_step=choice(strings))

            if (x_new, y_new) == ant.base.coord: # reached our base
                ant.has_food = False
                ant.food_time = 0
                return (x_new, y_new) + ('drop_food',)

            # still on our way and food is fresh enough
            if ant.food_time > 1:
                ant.food_time -= 1
                return (x_new, y_new, 'move')
            else: 
                ant.has_food = False
                ant.food_time = 0
                move = 'move' if (x_new, y_new) == ant.coord else 'drop_food'
                return (x_new, y_new, move)

        return compute_next_move_for_ant_w_food(self) if self.has_food \
                    else compute_next_move_for_ant_wo_food(self)
