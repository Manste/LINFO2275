import random
from snakeGame import *
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(12)

layouts = []
layouts.append(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
layouts.append(np.array([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]))
layouts.append(np.array([0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0]))
layouts.append(np.array([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0]))
layouts.append(np.array([0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0]))
layouts.append(np.array([0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 0]))
layouts.append(np.array([0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0]))
layouts.append(np.array([0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0]))
layouts.append(np.array([0, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 0]))
layouts.append(np.array([0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 0]))
layouts.append(np.array([0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0]))
layouts.append(np.array([0, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 0]))
layouts.append(np.array([0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 0]))
# add your layout as you wish

# The strategies for simulations
strategies = []
strategies.append([DiceStrategy(1) for _ in range(0, 14)])
strategies.append([DiceStrategy(2) for _ in range(0, 14)])
strategies.append([DiceStrategy(3) for _ in range(0, 14)])

# random strategy
random_strategy = []
for i in range(0, 14):
    strategy = random.choice([1, 2, 3])
    random_strategy.append(DiceStrategy(strategy))

strategies.append(random_strategy)

x = np.arange(1, 15)
tot_true = [[]]
tot_false=[[]]

theoretical_cost1, theoretical_strategy1 = markovDecision(layouts[0], False)
theo_dice_strategy1 = diceToDiceStrategy(theoretical_strategy1)
emperical_cost_1000_1 = simulate_strategy(layouts[0], False, theo_dice_strategy1, 1000)
print("The simulations results for 1000 simulations are:", emperical_cost_1000_1)