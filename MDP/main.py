import numpy as np

layout = np.zeros(15)
REWARD = -0.01 # constant reward for non-terminal states
MAX_ERROR = 1e-3
"""
The actions in this project is related to the choice of the dice
"""
ACTIONS = {
    1: {            # "security" dice
        "prob": 1/2,
        "values": [0, 1],
        "trigger": 0 # percentage of chance of triggering trap/bonus
    },
    2: {            # "normal" dice
        "prob": 1/3,
        "values": [0, 1, 2],
        "trigger": .5
    },
    3: {            # "risky"
        "prob": 1/4,
        "values": [0, 1, 2, 3],
        "trigger": 1
    }
}

"""
Generate states
"""
def get_sucessors(layout, circle=False):
    for


def markovDecision(layout,circle):
    """
    :param layout: a vector of type numpy.ndarray that represents the layout of the game, containing 15 values representing the 15 squares of the Snakes and Ladders game:
        layout[i] = 0 if it is an ordinary square
        = 1 if it is a “restart” trap (go back to square 1)
        = 2 if it is a “penalty” trap (go back 3 steps)
        = 3 if it is a “prison” trap (skip next turn)
        = 4 if it is a “bonus” (play again, without waiting next turn)
    :param circle: a boolean variable (type bool), indicating if the player must land exactly on
    the final, goal, square 15, to win (circle = True) or still wins by overstepping the final
    square (circle = False).
    :return:Your function markovDecision is expected to return a type list containing the two
        vectors [Expec,Dice]:
        • Expec: a vector of type numpy.ndarray containing the expected cost (= number of turns)
        associated to the 14 squares of the game, excluding the goal square. The vector starts at
        index 0 (corresponding to square 1) and ends at index 13 (square 14).
        • Dice: a vector of type numpy.ndarray containing the choice of the dice to use for each of
        the 14 squares of the game (1 for “security” dice, 2 for “normal” dice and 3 for “risky”),
        excluding the goal square. Again, the vector starts at index 0 (square 1) and ends at
        index 13 (square 14).
    """
