import sys
import pickle
import csv
import numpy

class BettingMDP():
    def __init__(self, probs, payoffs, bucketSizes=100, startAmt=1000):
        """
        probs: the probability of the home team winning for each game, given by our model.
        Accessed in the form probs[game number]

        payoffs: the multiplier for a specific game if you correctly pick home or away. 
        Accessed in the form payoffs[game number]['H' or 'A']
        """
        self.probs = probs
        self.payoffs = payoffs
        self.bucketSizes = bucketSizes
        self.startAmt = startAmt

    # Return the start state.
    # Each state is a tuple with 2 elements:
    #   (money currently have, game number)
    def startState(self):
        return (self.startAmt, 0)

    # Return set of actions possible from |state|.
    # Each actin is a tuple with 2 elements:
    #   (money to bet, 'A' or 'H')
    def actions(self, state):
        money = state[0]
        bucketSizes = self.bucketSizes
        game = state[1]

        if money < bucketSizes or game == len(self.probs):
            return []

        actions = [(i * bucketSizes, l) for i in range(int(money//bucketSizes) + 1) for l in ['H', 'A']]

        return actions


    # Given a |state| and |action|, return a list of (newState, prob) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # A few reminders:
    # * Indicate a terminal state (after quitting, busting, or running out of cards)
    #   by setting the deck to None.
    # * If |state| is an end state, you should return an empty list [].
    # * When the probability is 0 for a transition to a particular new state,
    #   don't include that state in the list returned by succAndProbReward.
    def succAndProbs(self, state, action):
        money, game = state
        bet, team = action
        probs = self.probs
        payoffs = self.payoffs
        bucketSizes = self.bucketSizes

        returnList = []

        if team == 'H':
            prob = probs[game]
        else:
            prob = 1 - probs[game]

        payoff = payoffs[game][team]

        succBetMoney = money - bet + bet*payoff
        unsuccBetMoney = money - bet

        returnList.append(((succBetMoney, state[1] + 1), prob))
        returnList.append(((unsuccBetMoney, state[1] + 1), 1 - prob))

        return returnList

    def discount(self):
        return 1

def Vopt(mdp, state, minVal, cache):
    if state in cache:
        return cache[state]

    actions = mdp.actions(state)

    if len(actions) == 0: 
        if state[0] >= minVal:
            return (None, 1)
        else:
            return (None, 0)

    maxActionVal = (None, float('-inf'))

    for action in actions:
        val = Qopt(mdp, state, action, minVal, cache)
        if val > maxActionVal[1]:
            maxActionVal = (action, val)

    cache[state] = maxActionVal
    return maxActionVal


def Qopt(mdp, state, action, minVal, cache):
    newStateProbs = mdp.succAndProbs(state, action)

    tot = 0
    for newState, prob in newStateProbs:
        tot += prob * Vopt(mdp, newState, minVal, cache)[1]

    return tot

def test(teams, results, probs, payoffs, desiredAmt, bucketSizes=100, startAmt=1000):
    # results should be a list of who won each game e.x. ['H', 'A', 'A']
    for result in results:
        mdp = BettingMDP(probs, payoffs, bucketSizes, startAmt)
        action, vopt = Vopt(mdp, mdp.startState(), desiredAmt, {})
        bet, team = action

        if team == result:
            startAmt += bet * (payoffs[0][team] - 1)
        else:
            startAmt -= bet

        del probs[0]
        del payoffs[0]


        print("bet", bet, "on", teams[0][team])
        print('prob achieve desiredAmt ', vopt)
        print(teams[0][result], "won")
        print("new amount:", startAmt)
        print()
        del teams[0]
    return startAmt >= desiredAmt


bucketSizes = int(sys.argv[1])
goal = int(sys.argv[2])
season = sys.argv[3]
date = int(sys.argv[4])
year = int(date / 10000)
file = sys.argv[5]


with open(file, 'rb') as handle:
    allProbs = pickle.load(handle)

with open('payoffs.pickle', 'rb') as handle:
    allPayoffs = pickle.load(handle)




probs = allProbs[season][date]

payoffs = allPayoffs[season][date]


results = []
teams = []

prev = None
reader = csv.reader(open('nhl_odds_20' + season +'.csv', 'r'))
for data in reader:
    if prev:
        if data[3] > prev[3]:
            results.append('H')
        else:
            results.append('A')
        teams.append({'H': data[2], 'A': prev[2]})
        prev = None

    elif data[0] == str(date % 10000):
        prev = data

test(teams, results, probs, payoffs, goal, bucketSizes)






