'''
    ant.move() -> (x_new, y_new, move)
    moves: 'hit', 'move', 'take_food', 'drop_food'

'''
from random import choice
from Planet import Food, Base, Ant


class BasicBase(Base):
    label = 'B'
    max_ant_quantity = 20

    def __init__(self, AntClass, coord, planet, team):
        self.AntClass = AntClass
        self.planet = planet
        self.coord = coord
        self.team = team
        self.food = 0
        self.catalog = set()

    def spawn(self):
        cell = self.locate
        x0, y0 = self.coord
        x_max, y_max = self.planet.size
        try:
            x, y = choice([(x0 + dx, y0 + dy) for dx in range(-1, 2) for dy in range(-1, 2)
                           if 0 <= x0 + dx < x_max and 0 <= y0 + dy < y_max
                           and not isinstance(cell(x0 + dx, y0 + dy), (Base, Ant))])
            ant = self.AntClass(coord=(x, y), base=self)
            self.catalog.update({ant})
            self.planet.land(x, y).set(ant)
        except IndexError:
            pass

    def advance(self):
        if len(self.catalog) < self.max_ant_quantity:
            self.spawn()

class BasicAnt(Ant):
    max_food_time = 10

    def __init__(self, coord, base):
        Ant.__init__(self)
        self.base = base
        self.coord = coord
        self.has_food = False
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
            x_new, y_new = compute_next_coord_by_str_with_step(*ant.coord, str_with_step=next_step)
            cell = self.base.locate

            if isinstance(cell(x_new, y_new), Food):
                ant.has_food = True
                ant.food_time = BasicAnt.max_food_time
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
