# a1.py

from search import *
from random import seed
from random import shuffle
import time
import math


"""Explanation of functions is taken from assignment descriptions with some edition."""


def make_rand_8puzzle():
    """Returns a new instance of an EightPuzzle problem
    with a random initial state that is solvable. Including
    a method called check_solvability from EightPuzzle.
    Idea of generating random integers is from:
    https://machinelearningmastery.com/how-to-generate-random-numbers-in-python/"""
    seed(1)
    sequence = [i for i in range(9)]
    shuffle(sequence)
    # Generate a test instance of EightPuzzle
    test = EightPuzzle(tuple(sequence))
    while not test.check_solvability(tuple(sequence)):
        shuffle(sequence)
    # Generate the real return instance
    new_puzzle = EightPuzzle(tuple(sequence))
    display(new_puzzle.initial)
    return new_puzzle


def display(state):
    """Takes an 8-puzzle state (i.e. a tuple that is a
    permutation of (0, 1, 2, ..., 8)) as input and prints a
    neat and readable representation of it. 0 is the blank,
    and should be printed as a * character. For example,
    if state is (0, 3, 2, 1, 8, 7, 4, 6, 5), then display(state)
    should print:
        * 3 2
        1 8 7
        4 6 5	"""
    for i in range(len(state)):
        if state.index(i) == 0:
            print('*', end=' ')
        else:
            print('%d' % state.index(i), end=' ')
        if i == 2 or i == 5 or i == 8:
            print('')


# Q2 Comparing Algorithms ----------------------------


def manhattan(node):
    """ Idea of manhattan comes from:
    https://github.com/aimacode/aima-python/blob/master/search.ipynb"""
    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {state[0]: [0, 0], state[1]: [0, 1], state[2]: [0, 2], state[3]: [1, 0], state[4]: [1, 1],
                   state[5]: [1, 2], state[6]: [2, 0], state[7]: [2, 1], state[8]: [2, 2]}
    # combine state and index into index_state
    # for i in range(len(state)):
    #     index_state[state[i]] = index[i]

    # mhd = abs(x1-x2) + abs(y1-y2)
    mhd = 0
    for i in range(8):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
    return mhd


def max_heuristic(node):
    mhd = manhattan(node)
    mis = sum(s != g for (s, g) in zip(node.state, (1, 2, 3, 4, 5, 6, 7, 8, 0)))
    return max(mhd, mis)


# Q3 The House-Puzzle ----------------------------------


class DuckPuzzle(Problem):
    """Similar with EightPuzzle, but the shape of play boards changed.
       Functions come from EightPuzzle with self edition."""

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        if blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        if blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank > 3:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        counter = 0
        for i in range(8):
            if abs(state.index(i) - state.index(i+1)) > 1:
                counter += 1
        if counter > 2:
            return False
        else:
            return True

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


def make_rand_duckpuzzle():
    """Returns a new instance of an EightPuzzle problem
    with a random initial state that is solvable. Including
    a method called check_solvability from EightPuzzle.
    Idea of generating random integers is from:
    https://machinelearningmastery.com/how-to-generate-random-numbers-in-python/"""
    seed(5)
    sequence = [i for i in range(9)]
    # sequence = [3, 1, 0, 2, 7, 5, 6, 8, 4]
    # sequence = [2, 3, 1, 4, 6, 5, 0, 8, 7]
    shuffle(sequence)
    # Generate a test instance of EightPuzzle
    test = DuckPuzzle(tuple(sequence))
    while not test.check_solvability(tuple(sequence)):
        shuffle(sequence)
    # Generate the real return instance
    new_puzzle = DuckPuzzle(tuple(sequence))
    display_duckpuzzle(new_puzzle.initial)
    return new_puzzle


def display_duckpuzzle(state):
    """Takes an duckpuzzle state (i.e. a tuple that is a
    permutation of (0, 1, 2, ..., 8)) as input and prints a
    neat and readable representation of it. 0 is the blank,
    and should be printed as a * character. For example,
    if state is (0, 3, 2, 1, 8, 7, 4, 6, 5), then display(state)
    should print:
        * 3
        2 1 8 7
          4 6 5     """
    for i in range(len(state)):
        if i == 6:
            print('  ', end='')
        if state.index(i) == 0:
            print('*', end=' ')
        else:
            print('%d' % state.index(i), end=' ')
        if i == 1 or i == 5 or i == 8:
            print('')


def main():

    print("Initial state:")
    # change this to "make_rand_duckpuzzle()" to test duckpuzzle
    puzzle = make_rand_8puzzle()
    backup = puzzle

    print("Part 1 : misplaced tile heuristic (default heuristic)")
    start_time = time.time()
    astar_search(puzzle, display=True)
    elapsed_time = time.time() - start_time
    print('elapsed_time (in seconds) : %fs' % elapsed_time)
    print('length of the solution : %d' % len(astar_search(puzzle).solution()))

    print("Part 2 : Manhattan distance")
    puzzle = backup
    start_time = time.time()
    astar_search(puzzle, manhattan, display=True)
    elapsed_time = time.time() - start_time
    print('elapsed_time (in seconds) : %fs' % elapsed_time)
    print('length of the solution : %d' % len(astar_search(puzzle).solution()))

    print("Part 3 : max of the misplaced tile heuristic and the Manhattan distance")
    puzzle = backup
    start_time = time.time()
    astar_search(puzzle, max_heuristic, display=True)
    elapsed_time = time.time() - start_time
    print('elapsed_time (in seconds) : %fs' % elapsed_time)
    print('length of the solution : %d' % len(astar_search(puzzle).solution()))

    return None


if __name__ == "__main__":
    main()
