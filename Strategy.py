import random
from Environement import Environement


class Strategy:
    """
    This class is a general stategy.
    It is used to create subclass of strategies that can play.
    """
    def __init__(self, population=100):
        self.value = 100
        self.population = population
        self.position = 0

    def increaseValue(self, value):
        self.value += value

    def name(self):
        return self.__class__.__name__




class playNice(Strategy, Environement):
    """
    A strategy that always play 1
    """
    def __init__(self, payoffMatrix, population):
        Environement.__init__(self, payoffMatrix)
        Strategy.__init__(self,population)

    def play(self, *args):
        return 1

class playMean(Strategy, Environement):
    """
    A strategy that always play 0
    """
    def __init__(self, payoffMatrix, population):
        Environement.__init__(self, payoffMatrix)
        Strategy.__init__(self, population)

    def play(self, *args):
        return 0

class playRandom(Strategy, Environement):
    """
    A strategy that randomly choose between 1 or 0
    """
    def __init__(self, payoffMatrix, population):
        Environement.__init__(self, payoffMatrix)
        Strategy.__init__(self, population)

    def play(self, *args):
        return random.randint(0,1)

class titForTat(Strategy, Environement):

    def __init__(self, payoffMatrix, population):
        Environement.__init__(self, payoffMatrix)
        Strategy.__init__(self, population)

    def play(self, *args):
        turn, history = args
        if turn == 0:
            return 0
        else:
            return history[-1][1-self.position]
