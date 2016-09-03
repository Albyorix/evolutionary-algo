

from Strategy import playNice, playMean, playRandom, titForTat
import matplotlib.pyplot as plt
import random
from copy import deepcopy

class Arena:
    """
    The arena in which the strategies play against each other.
    It is defined by the number of turn 2 strategies fight. This gives a game.
    And the total number of games that are played.
    It can plot the evolution of payoff and populations over time.
    """
    def __init__(self, totalTurnPerGame=10, totalGame=10, strategies=[], fixedPopulation=True):
        self.totalTurnPerGame = totalTurnPerGame
        self.totalGame = totalGame
        self.strategies =  strategies
        self.valueHistory = []
        self.renewPopulation()
        self.polulationHistory =  [[self.strategies[i].population for i in xrange(len(self.strategies))]]
        self.valueHistory = [[self.strategies[i].value for i in xrange(len(self.strategies))]]
        self.fixedPopulation = fixedPopulation

    def getPlayerList(self):
        playerList = []
        for i in xrange(len(self.strategies)):
            for _ in xrange(self.strategies[i].population):
                playerList.append(self.strategies[i])
        return playerList

    def renewPopulation(self, population = 100.):
        if self.valueHistory == []:
            pass
        else:
            lastValue = deepcopy(self.valueHistory[-1])
            s = sum(lastValue)
            for i in range(len(lastValue)):
                lastValue[i] *= population / s

            for i in range(len(strategies)):
                self.strategies[i].population = (self.strategies[i].population + lastValue[i] ) / 2

    def pairFight(self, player0, player1):
        self.gameHistory = []
        self.gameTurn = 0
        player0.position = 0
        player1.position = 1
        for _ in xrange(self.totalTurnPerGame):
            p0play = player0.play(self.gameTurn, self.gameHistory )
            p1play = player1.play(self.gameTurn, self.gameHistory )
            p1payoff = player0.getPlayerPayoff( 0, p0play , p1play)
            p2payoff = player1.getPlayerPayoff( 1, p0play , p1play)
            player0.increaseValue(p1payoff)
            player1.increaseValue(p2payoff)
            self.gameHistory.append([p0play , p1play])
            self.gameTurn += 1

    def run(self):
        self.playerList = self.getPlayerList()

        for _ in xrange(self.totalGame):
            pairs = self.playerList[:]
            random.shuffle(pairs)
            while len(pairs) >= 2:
                p1 = pairs.pop()
                p2 = pairs.pop()
                self.pairFight(p1, p2)
            currentValues = []
            for i in xrange(len(self.strategies)):
                currentValues.append(self.strategies[i].value)
            self.valueHistory.append(currentValues)
            if not self.fixedPopulation:
                self.renewPopulation()
            currentPopulation = []
            for i in xrange(len(self.strategies)):
                currentPopulation.append(self.strategies[i].population)
            self.polulationHistory.append(currentPopulation)

        return self.formatResults()

    def formatResults(self):
        names = [self.strategies[i].name() for i in xrange(len(strategies))]
        results = deepcopy(self.valueHistory)
        results2 = deepcopy(self.polulationHistory)
        normalizedValues = []
        normalizedPopulation = []
        for i in xrange(len(results)):
            s1 = sum(results[i])
            s2 = sum(results2[i])
            normalizedValues.append([])
            normalizedPopulation.append([])
            for j in xrange(len(self.strategies)):
                normalizedValues[i].append( results[i][j] * 100. / s1)
                normalizedPopulation[i].append( results2[i][j] * 100 / s2)
        return names, normalizedValues, normalizedPopulation

    def turnList(self, a):
        b = []
        for i in range(len(a[0])):
            b.append([])
        for i in range(len(a[0])):
            for j in range(len(a)):
                b[i].append(a[j][i])
        return b

    def plot(self, names, value, population):

        fig = plt.figure(figsize=(18, 8))
        title = 'Evolution'
        fig.suptitle(title, fontsize=18, color='r')

        ax1 = plt.subplot(311)
        value2 = self.turnList(value)
        for i in range(len(names)):
            plt.plot(value2[i], label=str(names[i]))
        plt.legend(bbox_to_anchor=(1, 1), loc=2)
        ax1.set_title('Total Value', fontsize=14)

        ax2 = plt.subplot(312)
        plt.plot(population)
        ax2.set_title('Proportion of Populations', fontsize=14)

        ax3 = plt.subplot(313)
        valuePerHead = deepcopy(value)
        for i in range(len(value)):
            for j in range(len(value[i])):
                valuePerHead[i][j] = value[i][j] / float(population[i][j])
        plt.plot(valuePerHead)
        ax3.set_title('Value per head', fontsize=14)

        plt.show()




if __name__ == "__main__":
    totalTurnPerGame = 1
    totalGame = 100
    myPayoffMatrix =  [[ [0,0] , [10,0] ] , [ [0,10] , [5,5] ]]
    strategyPopulations = [10, 10]
    fixedPopulation = False
    strats = [playMean, playNice]
    strategies = []
    for i in xrange(len(strats)):
        strategies.append(strats[i](myPayoffMatrix, strategyPopulations[i]))

    arena = Arena( totalTurnPerGame, totalGame, strategies, fixedPopulation)
    names, values, population = arena.run()


    arena.plot(names, values, population)

    """
    a= initialData[0][0]()
    print a.play()
    print a.value
    a.increaseValue(2)
    print a.value
    """
