from itertools import chain
from random import uniform, randint, choice


class Ant(object):
    pass

class Base(object):
    label = 'B'
    def __init__(self, AntClass, coord, planet, team):
        self.AntClass = AntlCass
        self.coord = coord
        self.planet = planet
        self.team = team

    def spawn(self):
        pass

    def locate(self, x, y):
        return self.planet.land(x, y)._data

class Food(object):
    prob = 0.05
    label = 'f'
    def __init__(self, quantity):
        self.quantity = quantity

class Cell(object):
    def __init__(self, x, y, planet):
        self._planet = planet
        self._coord = (x, y)
        self._data = None

    def set(self, data):
        self._data = data

    def __repr__(self):
        return "Cell with " + str(self._data)


class Planet(object):
    hit_prob = 0.5
    def __init__(self, size, AntClass1, AntClass2, BaseClass1, BaseClass2):
        self.size = size
        self.Base1 = BaseClass1(AntClass=AntClass1,
                          coord=(0, 0),
                          planet=self,
                          team=1)
        self.Base2 = BaseClass2(AntClass=AntClass1,
                          coord=(self.size[0] - 1, self.size[1] - 1),
                          planet=self,
                          team=2)

        self._land = []
        for y in range(self.size[1]):
            self._land.append([])
            for x in range(self.size[0]):
                cell = Cell(x, y, self)
                if (x, y) == self.Base1.coord:
                    cell.set(self.Base1)
                elif (x, y) == self.Base2.coord:
                    cell.set(self.Base2)
                elif 0 <= uniform(0,1) < Food.prob:
                    cell.set(Food(randint(1, 2)))
                self._land[y].append(cell)
            self._land[y] = tuple(self._land[y])
        self._land = tuple(self._land)

    def land(self, x, y):
        return self._land[y][x]

    def advance(self):
        def update_base(base, enemy_base):
            dead_ants_set = set()
            for ant in base.catalog:
                x, y, move = ant.move()
                if self.move_checker(ant.coord, x, y, move, base, enemy_base) is True:
                    if move == 'hit':
                        if 0 <= uniform(0, 1) <= self.hit_prob:
                            dead_ants.update({self.land(x, y).data()})
                    elif move == 'move':
                        self.land(*ant.coord).set(None)
                        ant.coord = (x, y)
                        self.land(*ant.coord).set(ant)
                    elif move == 'drop_food':
                        if (x, y) == base.coord:
                            base.food += 1
                        else:
                            self.land(x, y).set(Food(1))
                    elif move == 'take_food':
                        if self.land(x, y)._data.quantity == 1:
                            ant.has_food = True
                            self.land(x, y).set(None)
                        elif self.land(x, y)._data.quantity > 1:
                            ant.has_food = True
                            self.land(x, y)._data.quantity -= 1
                else:
                    print 'Uncorrect move detected, ant skipped'
                    continue
            if len(base.catalog) < base.max_ant_quantity:
                base.spawn()
            enemy_base.catalog.difference_update(dead_ants_set)

        update_base(self.Base1, self.Base2)
        update_base(self.Base2, self.Base1)                    

    def __str__(self):
        Buffer = []
        ind = 0
        for cell in chain.from_iterable(self._land):
            figure = cell._data
            label = ' ' if figure == None \
                else Food.label if isinstance(figure, Food) \
                else Base.label if isinstance(figure, Base) \
                else str(figure.base.team)
            Buffer.append(label)

            ind += 1
            if ind == len(self._land[0]):
                Buffer.append('\n')
                ind = 0
        Buffer.append('Base 1: ' + str(self.Base1.food) + '  Base 2: ' + str(self.Base2.food))
        return "".join(Buffer)

    def __repr__(self):
        return str(self)

    def move_checker(self, old_coord, x, y, move, base, enemy_base):
        cell = lambda x, y: self.land(x, y)._data
        if move == 'take_food' and not isinstance(cell(x, y), Food):
            print 'take food from empty place', x, y
            return False
        if move == 'move' and isinstance(cell(x, y), Ant):
            if (x, y) == old_coord:
                return True
            else:
                print 'tried to step down over other ant. you are monster himself', x, y
                return False
        if move == 'move' and ((x, y) == enemy_base.coord \
                               or (x, y) == base.coord):
            print "tried to step down base someone's. too smal for that", x, y
            return False
        if not (0 <= x < self.size[0] and 0 <= y < self.size[1]):
            print 'your ant goes too far. fare thee well, brave ant', x, y
            return False
        if move == 'drop_food' and \
           isinstance(cell(x, y), Ant):
            print 'tried to kill other ant by sugar. bad boy', x, y
            return False

        return True
