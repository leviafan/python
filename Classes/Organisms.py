from typing import Dict
import random
'''
Придумать систему классов, реализующих, например, геометрические фигуры
(фигура, квадрат, прямоугольник) или алгебраические типы (число,
вектор, матрица), или что-то своё. Придумать, как поинтересней перегрузить
стандартные операции, использовать полиморфизм). Все действия должны быть
покрыты тестами.
'''


class Organism:
    def __init__(self, mut_dict: Dict = {}, ):
        self.age = 0
        self._max_age = 10
        self.is_alive = True
        self.is_male = bool(random.getrandbits(1))
        self.mother = None
        self.father = None
        self.can_fly = False
        self.can_swim = False
        self.mutations: Dict[str, bool] = {}
        """ If mutations['name'] is True, it is strong and transits to the
        child. The weak mutation transits to child only from both parents
        having mutations['name'] and it will be weak mutation too.
        """
        for m in mut_dict.keys():
            if type(mut_dict[m]) is bool:
                self.mutations[m] = mut_dict[m]
            else:
                raise TypeError('mutations must contain boolean values')

    """ In my world this means breeding. Can be applied to mother object with
        father as an argument. If all was done right, returns a new organism
        of the same type, else returns None.
    """

    def __add__(self, partner):
        if not partner.is_alive:
            print('Dead can\'t breed!')
            return None

        if not self.is_alive:
            print('Necrophilia leads to injury!')
            partner.take_injury()
            return None

        if type(self) != type(partner):
            print('Interrace breeding!')
            self.take_injury()
            return None

        if self.is_male or not partner.is_male:
            print('Wrong gender breeding!')
            self.take_injury()
            return None
# read comment in __init__
        mutations = {}

        for mut, strength in self.mutations.items():
            if strength:
                mutations[mut] = True
            elif partner.mutations.get(mut) is not None:
                mutations[mut] = False

        for mut, strength in enumerate(partner.mutations):
            if not strength:
                mutations[mut] = False

        child = type(self)(mutations)
        child.mother = self
        child.father = partner

        if self.mother and partner.mother:
            if self.mother == partner.mother or self.father == partner.father:
                print('Incest produces dead child')
                child.is_alive = False

        return child

    """ A - B means that B have tried to eat A
    """
    def __sub__(self, eater) -> bool:
        if not eater.is_alive:
            print('Dead can\'t eat!')
            return False

        if not self.is_alive:
            print('Ewww! He is eating a corpse!')
            eater.take_injury()
            return True

        if self.age >= eater.age:
            self.take_injury()
            eater.take_injury()
            return False

        else:
            self.kill()
            return True

    def increase_age(self, years: int) -> bool:
        if not self.is_alive:
            print('Dead are always young!')
            return self.is_alive

        self.age += years
        if self.age >= self._max_age:
            self.kill()

        return self.is_alive

    def kill(self):
        if not self.is_alive:
            print('What is dead may never die!')
            return False

        self.is_alive = False

        return True

    def take_injury(self) -> bool:
        if not self.is_alive:
            print('Dead can\'t take hurt')
            return False

        self._max_age -= 1
        if self.age >= self._max_age:
            self.kill()

        return self.is_alive

    """ Returns true if mutation was succeed,
        returns false if mutation already present
    """
    def mutate(self, mut_name: str, mut_strong: bool) -> bool:
        if not self.is_alive:
            print('Dead mutation is worthless')
            return False

        if self.mutations.get(mut_name):
            return False

        if self.mutations.get(mut_name) is not None and not mut_strong:
            return False

        self.mutations[mut_name] = mut_strong
        return True


class Fish(Organism):
    def __init__(self, mut_dict: Dict = {}):
        Organism.__init__(self, mut_dict)
        self.can_swim = True

    def __sub__(self, eater):
        if not eater.can_swim and self.can_swim:
            eater.take_injury()
            return False

        return Organism.__sub__(self, eater)

    def swim(self):
        if self.is_alive:
            return True

        else:
            return False


class Bird(Organism):
    def __init__(self, mut_dict: Dict = {}):
        Organism.__init__(self, mut_dict)
        self.can_fly = True

    def __sub__(self, eater):
        if not eater.can_fly and self.can_fly and self.is_alive:
            eater.take_injury()
            return False

        return Organism.__sub__(self, eater)

    def fly(self):
        if self.is_alive:
            return True

        else:
            return False


class Mammal(Organism):
    def feed_with_milk(self, feedable: Organism) -> bool:
        if not feedable.is_alive or not self.is_alive:
            return False

        if self.is_male:
            self.take_injury()
            return False

        if type(self) != type(feedable):
            self.take_injury()
            return False

        if feedable.mother != self:
            self.take_injury()

        return True
