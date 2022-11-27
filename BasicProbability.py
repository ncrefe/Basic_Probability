import random
from matplotlib import pyplot as plt

"""
Instructions:
5 dice are rolled. Following probabilities are defined:
● P1: The probability that at least one dice is 3.
● P2: The probability that at least one dice is 3 given one of the dice is even.
● P3: The probability that at least one dice is 3 given only one of the dice is even.
Write a small code in Python:
● to compute the theoretical probabilities Pi
● to compute the empirical probabilities P’i by simulating the experiment and repeating it
N=[10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000] times.
● to plot the P’i vs N graphs. Include a P’i = Pi line ‘n your graph to show your theoretical
finding. Use log scale for N axis.
"""

# I got the result by subtracting the undesired state from the whole state in P1. I found how many different ways there
# would be placements in P2 by accepting the 3s as separators. In this way, I was able to find the necessary intersection
# for Bayes Rule. I made a solution in P3 similar to P2. I used the combination as it was in the stick split method. I designed
# the code to work independently of the number of dice. In some math operations, I shortened expressions like 5*(1/6) to 5/6.
# If you want me to explain unclear statements, I can. I think I managed to solve it by following a different way than
# I thought too much about the solution.
# I plotted the probabilities as 80% over the percentile on the graph.

N = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]


def rollADie():
    return random.randint(1, 6)


def rollDice(n=5):
    results = []
    for roll in range(n):
        results.append(rollADie())
    return results


def combination(whole, piece):
    top = whole
    result = 1
    for i in range(piece):
        result *= top / (i + 1)
        top -= 1
    return result


# I took out P1's processes because I need to use it for P2 as well.
def atLeastOneDiceIsThree(numberOfDice=5):
    total = 6 ** numberOfDice
    notDesired = 5 ** numberOfDice
    desired = total - notDesired
    return desired


def P1Theoretical(numberOfDice=5):
    total = 6 ** numberOfDice
    return atLeastOneDiceIsThree(numberOfDice) / total


def P2Theoretical(numberOfDice=5):
    notDesired = 1  # 3 3 3 3 3 is included
    total = 6 ** numberOfDice
    splitterCounter = numberOfDice  # I used the box method. The 3's act as separators.

    for twoNumber in range(1, numberOfDice):
        notDesired += combination(splitterCounter - 1 + twoNumber, twoNumber) * (2 ** twoNumber)
        splitterCounter -= 1

    dividend = (atLeastOneDiceIsThree(numberOfDice) - notDesired) / total  # P(intersection of A and B)
    divisor = 1 - ((1 / 2) ** numberOfDice)  # P(B)
    return dividend / divisor


def P3Theoretical(numberOfDice=5):
    total = 6 ** numberOfDice
    result = 0
    for i in range(numberOfDice - 1):
        result += combination(numberOfDice, numberOfDice - (i + 2)) * (2 ** (numberOfDice - (i + 2))) * (i + 2) * 3
    dividend = result / total  # P(intersection of A and B)
    divisor = numberOfDice * (3 ** numberOfDice) / total  # P(B)
    return dividend / divisor


def numberOfEvens(array):
    number = 0
    for num in array:
        if num % 2 == 0:
            number += 1
    return number


def P1Experimental():
    graph = []  # For the percentiles to use in the chart
    for n in N:
        true = 0
        for i in range(n):
            array = rollDice()
            if 3 in array:
                true += 1
        graph.append(true / n * 100)
    return graph


def P2Experimental():
    graph = []  # For the percentiles to use in the chart
    for n in N:
        true = 0
        counter = 0
        while counter != n:
            array = rollDice()
            if numberOfEvens(array) > 0:
                counter += 1
                if 3 in array:
                    true += 1
        graph.append(true / n * 100)
    return graph


def P3Experimental():
    graph = []  # For the percentiles to use in the chart
    for n in N:
        true = 0
        counter = 0
        while counter != n:
            array = rollDice()
            if numberOfEvens(array) == 1:
                counter += 1
                if 3 in array:
                    true += 1
        graph.append(true / n * 100)
    return graph


# I made the theoretical values into an "array" to be able to use them in the graph.
def createALineForTheoreticalResult(N, possibility):
    result = []
    for n in N:
        result.append(possibility * 100)
    return result


# To get the experimental output properly
def percentageFormatterForArrays(array):
    string = ""
    for element in array:
        string += f"{element:.2f}, "
    return string[:-2:]


def plotResult1(array=N):
    plt.xlabel("N")
    plt.ylabel("Probability")
    plt.plot(array, P1Experimental())
    plt.plot(array, createALineForTheoreticalResult(array, P1Theoretical()))
    plt.xscale("log")
    plt.title("Results of P1")
    plt.show()


def plotResult2(array=N):
    plt.xlabel("N")
    plt.ylabel("Probability")
    plt.plot(array, P2Experimental())
    plt.plot(array, createALineForTheoreticalResult(array, P2Theoretical()))
    plt.xscale("log")
    plt.title("Results of P2")
    plt.show()


def plotResult3(array=N):
    plt.xlabel("N")
    plt.ylabel("Probability")
    plt.plot(array, P3Experimental())
    plt.plot(array, createALineForTheoreticalResult(array, P3Theoretical()))
    plt.xscale("log")
    plt.title("Results of P3")
    plt.show()


def printTheoreticalResults():
    print("Theoretical Results:")
    print(f"P1: The probability that at least one dice is 3 : {P1Theoretical() :.5%}\n"
          f"P2: The probability that at least one dice is 3 given one of the dice is even : {P2Theoretical() :.5%}\n"
          f"P3: The probability that at least one dice is 3 given only one of the dice is even : {P3Theoretical() :.5%}")


def printExperimentalResults():
    print("Experimental Results:")
    print(f"P1: The probabilities that at least one dice is 3 : {percentageFormatterForArrays(P1Experimental())}\n"
          f"P2: The probabilities that at least one dice is 3 given one of the dice is even : {percentageFormatterForArrays(P2Experimental())}\n"
          f"P3: The probabilities that at least one dice is 3 given only one of the dice is even : {percentageFormatterForArrays(P3Experimental())}")


printTheoreticalResults()
printExperimentalResults()
plotResult1(N)
plotResult2()
plotResult3(N)
