


class Environement:
    """
    This class represent the environment in which the strategies play.
    The environment determines the payoff of the strategies in function of the choices made.
    """
    def __init__(self, payoffMatrix = [[ [0,0] , [2,0] ] , [ [0,2] , [1,1] ]] ):
        self.payoff = payoffMatrix

    def getPlayerPayoff(self, playerPosition, choicePlayer0, choicePlayer1):
        return self.payoff[choicePlayer0][choicePlayer1][playerPosition]

    def getFullPayoff(self):
        return self.payoff
