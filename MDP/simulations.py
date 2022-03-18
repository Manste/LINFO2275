import random
from snakeGame import *
import numpy as np
import matplotlib.pyplot as plt

layouts = []
layouts.append(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))  # 0
layouts.append(np.array([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]))  # 1
layouts.append(np.array([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0]))  # 2
layouts.append(np.array([0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0]))  # 3
layouts.append(np.array([0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0]))  # 4
layouts.append(np.array([0, 1, 3, 2, 4, 2, 1, 3, 3, 0, 2, 1, 2, 4, 0]))  # 5
layouts.append(np.array([0, 3, 3, 4, 2, 1, 2, 4, 1, 0, 2, 3, 0, 2, 0]))  # 6
layouts.append(np.array([0, 4, 3, 2, 1, 4, 3, 1, 1, 4, 1, 4, 3, 2, 0]))  # 7
layouts.append(np.array([0, 2, 3, 3, 1, 1, 4, 4, 3, 0, 1, 2, 2, 0, 0]))  # 8
layouts.append(np.array([0, 2, 2, 1, 3, 2, 3, 3, 2, 1, 0, 1, 1, 0, 0]))  # 9
layouts.append(np.array([0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0]))  # 10
layouts.append(np.array([0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0]))  # 11
layouts.append(np.array([0, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 3, 3, 0]))  # 12
layouts.append(np.array([0, 4, 4, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0]))  # 13
# feel free to add your layout

# We are adding some strategies
strategies = []
strategies.append([DiceStrategy(1) for _ in range(0, 14)])  # 0
strategies.append([DiceStrategy(2) for _ in range(0, 14)])  # 1
strategies.append([DiceStrategy(3) for _ in range(0, 14)])  # 2

# random strategy
random_strategy = []
strat_int = []
for i in range(0, 14):
    strategy = random.choice([1, 2, 3])
    random_strategy.append(DiceStrategy(strategy))
    strat_int.append(strategy)
strategies.append(random_strategy)  # 3
x = np.arange(1, 15)
"""
# Comparison between the theoretical expected cost
theoretical_cost1, theoretical_strategy1 = markovDecision(layouts[0], False)
theo_dice_strategy1 = diceToDiceStrategy(theoretical_strategy1)
emperical_cost_1000_1 = simulate_strategy(layouts[0], False, theo_dice_strategy1)
emperical_cost_10000_1 = simulate_strategy(layouts[0], False, theo_dice_strategy1, 10000)

theoretical_cost2, theoretical_strategy2 = markovDecision(layouts[0], True)
theo_dice_strategy2 = diceToDiceStrategy(theoretical_strategy2)
emperical_cost_1000_2 = simulate_strategy(layouts[0], True, theo_dice_strategy2)
emperical_cost_10000_2 = simulate_strategy(layouts[0], True, theo_dice_strategy2, 10000)


x = np.arange(1, 15)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(x, theoretical_cost1,'-D', label='Theoretical', linewidth=.7, color="#ed5f5a")
plt.plot(x,emperical_cost_1000_1, '-D', label='1000 Simulations', linewidth=.7, color="#f5b042")
plt.plot(x,emperical_cost_10000_1, '-D', label='10000 Simulations', linewidth=.7, color="#f54298")
plt.xticks(x)
plt.title("Layout without circle")
plt.xlabel('Squares')
plt.ylabel('Expected cost')

plt.legend()
plt.subplot(1, 2, 2)
plt.plot(x, theoretical_cost2,'-D', label='Theoretical', linewidth=.7, color="#ed5f5a")
plt.plot(x,emperical_cost_1000_2, '-D', label='1000 Simulations', linewidth=.7, color="#f5b042")
plt.plot(x,emperical_cost_10000_2, '-D', label='10000 Simulations', linewidth=.7, color="#f54298")
plt.xticks(x)
plt.title("Layout with circle")
plt.xlabel('Squares')
plt.ylabel('Expected cost')
plt.legend()
#plt.savefig('empirical.jpg')
plt.show()
"""
# Comparison between layouts and others strategies
for j, layout in enumerate(layouts):
    temp_only_dice_empirical_cost_false = [] # circle false
    temp_only_dice_empirical_cost_true = [] # circle true

    theoretical_cost1, theoretical_strategy1 = markovDecision(layout, False)
    strategy1 = diceToDiceStrategy(theoretical_strategy1)
    temp_only_dice_empirical_cost_false.append(simulate_strategy(layout, False, strategy1))

    theoretical_cost2, theoretical_strategy2 = markovDecision(layout, True)
    strategy2 = diceToDiceStrategy(theoretical_strategy2)
    temp_only_dice_empirical_cost_true.append(simulate_strategy(layout, True, strategy2))

    for i, strategy in enumerate(strategies):
        temp_only_dice_empirical_cost_false.append(simulate_strategy(layout, False, strategy))
        temp_only_dice_empirical_cost_true.append(simulate_strategy(layout, True, strategy))

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x, theoretical_cost1, '-D', label='Theoretical', linewidth=.7, color="#eb4034")
    plt.plot(x, temp_only_dice_empirical_cost_false[0], '-D', label='Empirical', linewidth=.7, color="#000")
    plt.plot(x, temp_only_dice_empirical_cost_false[1], '-D', label='Only dice 1', linewidth=.7, color="#5beb34")
    plt.plot(x, temp_only_dice_empirical_cost_false[2], '-D', label='Only dice 2', linewidth=.7, color="#3446eb")
    plt.plot(x, temp_only_dice_empirical_cost_false[3], '-D', label='Only dice3', linewidth=.7, color="#eb34de")
    plt.plot(x, temp_only_dice_empirical_cost_false[4], '-D', label='Random dices', linewidth=.7, color="#ebdc34")
    plt.xticks(x)
    plt.title("layout{} without circle".format(j))
    plt.xlabel('Squares')
    plt.ylabel('Expected cost')

    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(x, theoretical_cost2, '-D', label='Theoretical', linewidth=.7, color="#eb4034")
    plt.plot(x, temp_only_dice_empirical_cost_true[0], '-D', label='Empirical', linewidth=.7, color="#000")
    plt.plot(x, temp_only_dice_empirical_cost_true[1], '-D', label='Only dice 1', linewidth=.7, color="#5beb34")
    plt.plot(x, temp_only_dice_empirical_cost_true[2], '-D', label='Only dice 2', linewidth=.7, color="#3446eb")
    plt.plot(x, temp_only_dice_empirical_cost_true[3], '-D', label='Only dice3', linewidth=.7, color="#eb34de")
    plt.plot(x, temp_only_dice_empirical_cost_true[4], '-D', label='Random dices', linewidth=.7, color="#ebdc34")
    plt.xticks(x)
    plt.title("layout{} with circle".format(j))
    plt.xlabel('Squares')
    plt.ylabel('Expected cost')
    plt.legend()
    plt.savefig('others_dices_layout{}.jpg'.format(j))
    plt.show()