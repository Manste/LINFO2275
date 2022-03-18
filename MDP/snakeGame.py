import numpy as np
from numpy.random import randint

DICES_FEATURES = {
    1: {
        "name": "security",
        "trap_probability": 0,
        "outcomes": {0: 1 / 2, 1: 1 / 2}
    },
    2: {
        "name": "normal",
        "trap_probability": 1/2,
        "outcomes": {0: 1 / 3, 1: 1 / 3, 2: 1 / 3}
    },
    3: {
        "name": "risky",
        "trap_probability": 1,
        "outcomes": {0: 1 / 4, 1: 1 / 4, 2: 1 / 4, 3: 1 / 4}
    }
}

def markovDecision(layout, circle):
    """This function computes the expected cost and choice of dice for the snake Ladder game
    -Layout is a ndarray containing the layout of the game
    -circle is a boolean specifying whether the game is circular(True) or not
    """

    # The variable max_iterations specifies the maximum allowed number of iterations
    # epsilon is used for the convergence criterion
    max_iterations = 1000
    epsilon = 10 ** (-6)

    # initialisation of the snake and ladder game
    # the costs are set to 0 for the first iteration and the strategy is set to 1 (security dice)
    game = SnakeGame(layout, circle)
    expec = [0 for square in range(0, 14)]
    dice = [1 for square in range(0, 14)]
    for iteration in range(max_iterations):

        # for every square we compute a new cost and dice strategy based on Bellman recurring relation
        for square in reversed(range(1, 15)):
            dice[square - 1], expec[square - 1] = game.compute_best_strategy(square)

        # we check if the convergence has been achieved. If it is the case then the game is ended
        if max([abs(expec[i] - game.V[i]) for i in range(0, 14)]) < epsilon:
            print("the game has converged in " + str(iteration) + " iterations")
            print("the best strategy is", dice)
            print("the associated cost is", game.V[0])
            print(np.array(expec))
            return [np.array(expec), np.array(dice)]

        # If convergence is not yet achieved we save the cost of the previous iteration and move to the next one
        for i in range(0, 14):
            game.best_strategy[i] = dice[i]
            game.V[i] = expec[i]


def simulate_strategy(layout, circle, game_strategy, simulations=1000):
    """This function simulates the ladder snakes game for a given game strategy
    game strategy is a vector of strategy for each square
    The output of the function is the simulated number of turn of the game
    """
    game = SnakeGame(layout, circle)
    game.simulated_strategy = game_strategy
    expec_cost = []
    for i in range(len(layout)-1):
        temp = []
        for _ in range(simulations):
            next_position, turn = game.play_strategy(i+1, 0)
            while next_position != 15:
                next_position, turn = game.play_strategy(next_position, turn)
            temp.append(turn)
        expec_cost.append(np.mean(temp))
    return expec_cost

class DiceStrategy:
    """This class defines what a dice is.
    - name is the name of the strategy induced by the dice: security,normal,risky
    - symbol is the number associated to the dice : 1,2,3
    - trap_probability is the probability that a trap is triggered when using the dice
    - outcomes is a dictionnary which the key is the number of squares the dice allow
      the user to move and the value the associated probability
    """

    def __init__(self, symbol):
        self.name = DICES_FEATURES[symbol]["name"]
        self.symbol = symbol
        self.trap_probability = DICES_FEATURES[symbol]["trap_probability"]
        self.outcomes = DICES_FEATURES[symbol]["outcomes"]


def diceToDiceStrategy(strategy):
    """
    This function converts an array of integer representing a strategy into a
    list of diceStrategy necessary for launching some simulations
    - strategy: list of integer
    return list of DiceStrategy
    """
    return [DiceStrategy(i) for i in strategy]


class SnakeGame:
    """This class describes a ladder snake board
    """

    def __init__(self, layout, circle):
        self.nbr_of_squares = layout.size
        self.last_square = self.nbr_of_squares
        self.layout = layout
        self.circle = circle
        self.list_of_dices = {
            'security': DiceStrategy(1),
            'normal': DiceStrategy(2),
            'risky': DiceStrategy(3)
        }
        self.best_strategy = [1 for i in range(0, 15)]
        self.V = [0 for square in range(self.nbr_of_squares)]
        self.simulated_strategy = None

    def move_forward(self, initial_square, mvt_amplitude):
        """make mvt_amplitude movements from initial square
        The movement amplitude which is the displacement is supposed less than 3
        """
        if initial_square in [1, 2, 4, 5, 6, 7, 11, 12, 13, 14, 15]:
            final_position = initial_square + mvt_amplitude
            if final_position > 15:
                return [tuple([(final_position % 15), 1.0])] if self.circle else [tuple([15, 1.0])]
            return [tuple([final_position, 1.0])]
        elif initial_square == 3:
            if mvt_amplitude == 0:
                return [tuple([initial_square, 1.0])]
            else:
                return [tuple([initial_square + mvt_amplitude, 1 / 2]),
                        tuple([initial_square + 7 + mvt_amplitude, 1 / 2])]
        elif initial_square == 8:
            if mvt_amplitude < 3:
                return [tuple([initial_square + mvt_amplitude, 1.0])]
            else:
                return [tuple([15, 1.0])]
        elif initial_square == 9:
            if mvt_amplitude < 2:
                return [tuple([initial_square + mvt_amplitude, 1.0])]
            elif mvt_amplitude == 2:
                return [tuple([15, 1.0])]
            else:
                return [tuple([1, 1.0])] if self.circle else [tuple([15, 1.0])]
        else:
            if mvt_amplitude == 0:
                return [tuple([10, 1.0])]
            if mvt_amplitude == 1:
                return [tuple([15, 1.0])]

            else:
                return [tuple([(15 + mvt_amplitude) % 16, 1.0])] if self.circle else [tuple([15, 1.0])]

    def move_backward_3(self, initial_square):
        """make 3 moves backward on the board
        """
        if initial_square <= 3:
            return 1
        elif initial_square in [11, 12, 13]:
            return initial_square - 10
        return initial_square - 3

    def get_trap_cost(self, square):
        """This function computes the cost function of the square where
        the player is sent after been caught in a trap at the given square
        """
        if self.layout[square - 1] == 0:
            return self.V[square - 1]
        elif self.layout[square - 1] == 1:
            return self.V[0]
        elif self.layout[square - 1] == 2:
            return self.V[self.move_backward_3(square) - 1]
        elif self.layout[square - 1] == 3:
            return self.V[square - 1] + 1
        else:
            return self.V[square - 1] - 1

    def get_strategy_cost(self, square, strategy):
        """This function computes the cost of a given strategy applied on a given square
        """
        v = 1
        for outcome in strategy.outcomes.keys():
            for possible_destination in self.move_forward(square, outcome):
                v += strategy.outcomes[outcome] * possible_destination[1] * (1 - strategy.trap_probability) * self.V[
                    possible_destination[0] - 1]
                v += strategy.outcomes[outcome] * possible_destination[
                    1] * strategy.trap_probability * self.get_trap_cost(
                    possible_destination[0])
        return v

    def compute_best_strategy(self, square):
        """This function computes the best strategy for a given square
        """
        cost_dict = {}
        for strategy in self.list_of_dices.keys():
            cost_dict[strategy] = self.get_strategy_cost(square, self.list_of_dices[strategy])
        for (strategy_symbol, cost) in sorted(cost_dict.items(), key=lambda val: val[1]):
            return self.list_of_dices[strategy_symbol].symbol, cost

    def play_strategy(self, current_position, turn, is_a_bonus_turn=False):
        """This function simulates a dice strategy
        - current_position is the initial position of the player, before playing the strategy
        - turn is the cost of the game so far
        - is_a_bonus is set to true when it is a bonus turn
        The function returns the player position after playing the strategy and the new cost of the game
        """
        turn_after = turn
        # get the possible outcomes of the strategy and the associated probabilities
        choices = [outcome for outcome in self.simulated_strategy[current_position - 1].outcomes.keys()]
        probabilities = [probability for probability in self.simulated_strategy[current_position - 1].outcomes.values()]

        # roll the dice and get the number to play
        roll = np.random.choice(choices, p=probabilities)

        # move to the forward position
        next_probable_position = self.move_forward(current_position, roll)
        if len(next_probable_position) == 1:
            next_position = next_probable_position[0][0]
        else:
            choosen_direction = np.random.choice([0, 1], p=[0.5, 0.5])
            next_position = next_probable_position[choosen_direction][0]
        if not is_a_bonus_turn:
            turn_after += 1

        # check if the trap has been triggered or not
        # if the outcome is 0 then the trap is not triggered, 1 it is triggered
        trap_triggered = np.random.choice([0, 1], p=[1 - self.simulated_strategy[current_position - 1].trap_probability,
                                                     self.simulated_strategy[current_position - 1].trap_probability])

        # If the trap is triggered then handle the trap
        # The 0 layout is not handled since it is a no trap situation
        if trap_triggered == 1:
            if self.layout[next_position - 1] == 1:
                next_position = 1
            elif self.layout[next_position - 1] == 2:
                next_position = self.move_backward_3(next_position)
            elif self.layout[next_position - 1] == 3:
                turn_after += 1
            elif self.layout[next_position - 1] == 4:
                return self.play_strategy(next_position, turn_after, is_a_bonus_turn=True)
        return next_position, turn_after
