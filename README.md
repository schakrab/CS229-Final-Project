# README

"Because It's The Cup"

Using machine learning to predict the outcome of NHL playoff games and then create an optimal betting strategy for each day of games.

## Files

Data stored in the .csv files. Code stored in:

* *monte_carlo.ipynb*: error analysis monte carlo simulation
* *evaluate_models.ipynb*: main majority of model code here (for reading in the data files, creating the feature sets, testing models, and performing our error analysis). unfortunately it isn't cleaned up at this point.

* *mdp_allPlayoffs.py*: Creates an optimal betting strategy to maximize the likelihood of achieving a certain goal amount. Run for one year's entire playoffs day by day given a starting amount of $1,000. Run with "python3 mdp_allPlayoffs.py 'discretizationAmount' 'desiredAmt' 'season' 'date from that playoff' probs.pickle". For example to run the 2015-2016 playoffs with a discretization of $10 bets and a goal of $1,200, use "python3 mdp_allPlayoffs.py 10 1200 15-16 20160413 probs.pickle".

* *mdp_probs.py*: Creates an optimal betting strategy to maximize the likelihood of achieving a certain goal amount. Run for one day of the playoffs given a starting amount of $1,000. Run with "python3 mdp_allPlayoffs.py 'discretizationAmount' 'desiredAmt' 'season' 'date". For example to run the 2015-2016 playoffs for the day April 17th with a discretization of $50 bets and a goal of $1,600, use "python3 mdp_probs.py 50 1600 15-16 20160417 probs.pickle".

* *mdp_maxReward.py*: Creates an optimal betting strategy to maximize epected returns. Run for one day of the playoffs given a starting amount of $1,000. Run with "python3 mdp_maxReward.py 'discretizationAmt' 'season' 'date' probs.pickle". For example to run the 2015-2016 playoffs for the day of April 26th with a discretization of $100 bets, usepython3 mdp_maxReward.py 100 15-16 20160426 probs.pickle".


## People

* Vineet Kosaraju
* Shuvam Chakraborty
* Mason Swofford
