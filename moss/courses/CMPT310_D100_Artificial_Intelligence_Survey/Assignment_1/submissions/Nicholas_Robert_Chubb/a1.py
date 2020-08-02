# a1.py

from search import *
from random import *
from datetime import *
from random import *

manhattan_lookup_table = [
    ( 0, 1, 2, 1, 2, 3, 2, 3, 4), # 1
    ( 1, 0, 1, 2, 1, 2, 3, 2, 3), # 2
    ( 2, 1, 0, 3, 2, 1, 4, 3, 2), # 3

    ( 1, 2, 3, 0, 1, 2, 1, 2, 3), # 4
    ( 2, 1, 2, 1, 0, 1, 2, 1, 2), # 5
    ( 3, 2, 1, 2, 1, 0, 3, 2, 1), # 6

    ( 2, 3, 4, 1, 2, 3, 0, 1, 2), # 7
    ( 3, 2, 3, 2, 1, 2, 1, 0, 1), # 8
    ( 4, 3, 2, 3, 2, 1, 2, 1, 0)  # 9
]

duck_manhattan_lookup_table = [
    ( 0, 1, 1, 2, 3, 4, 3, 4, 5), # 1
    ( 1, 0, 2, 1, 2, 3, 2, 3, 4), # 2
    ( 1, 2, 0, 1, 2, 3, 2, 3, 4), # 3

    ( 2, 1, 1, 0, 1, 2, 1, 2, 3), # 4
    ( 3, 2, 2, 1, 0, 1, 2, 1, 2), # 5
    ( 4, 3, 3, 2, 1, 0, 3, 2, 1), # 6

    ( 3, 2, 2, 1, 2, 3, 0, 1, 2), # 7
    ( 4, 3, 3, 2, 1, 2, 1, 0, 1), # 8
    ( 5, 4, 4, 3, 2, 1, 2, 1, 0)  # 9
]

def make_rand_8puzzle():

    solveable = False

    while solveable == False:

        # generate random start state
        start = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        shuffle(start)

        t_start = tuple(start)

        # initialize new EightPuzzle
        ep = EightPuzzle(t_start)

        # Check if solveable, if not, try again
        if EightPuzzle.check_solvability(ep, start) == True:
            
            print(t_start)

            solveable = True
            return ep
            
def make_rand_duckpuzzle():

    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    dp = DuckPuzzle(tuple(state))

    # Shuffles the puzzle using legal moves 10000 times to thoroughly randomize the puzzle while ensuring it is solvable
    for i in range(10000):

        possible_actions = DuckPuzzle.actions(dp, state)
        shuffle(possible_actions)

        state = DuckPuzzle.result(dp, state, possible_actions[0])

        dp = DuckPuzzle(tuple(state))

    print(state)

    return dp

def display(state):

    # list comprehension: filters state to replace 0 with *
    state = [str(x) if x != 0 else "*" for x in state]

    print(state[0] + " " + state[1] + " " + state[2])
    print(state[3] + " " + state[4] + " " + state[5])
    print(state[6] + " " + state[7] + " " + state[8])


''' summarize the total distance for each tile to get to its goal state '''
def manhattan_distance_heuristic(node):
    total = 0

    puzzle = EightPuzzle(node)

    for i in range(9):
        total += manhattan_lookup_table[node.state.index(i)][puzzle.goal.index(i)]

    return total    

def max_heuristic(n):
    puzzle = EightPuzzle(n)
    return max(manhattan_distance_heuristic(n), puzzle.h(n))

''' the modified astar search algorit   hm to always use the manhattan distance heuristic '''
def manhattan_astar_search(problem, display=True):
    h = memoize(manhattan_distance_heuristic, "h")
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def max_astar_search(problem, display=True):
    h = memoize(max_heuristic, "h")
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

''' Solves the EightPuzzle using the Misplaced Tile Heuristic '''
def solve_default(puzzle):

    run_time = 0
    print("Misplaced Tile Heuristic (Default):")
    time_start = datetime.now()

    astar_search(puzzle)

    run_time = datetime.now() - time_start
    print("Run time:", run_time.total_seconds())

''' Solves the EightPuzzle using the Manhattan Distance Heuristic '''
def solve_manhattan(puzzle):
    run_time = 0

    print("Manhattan Distance Heuristic:")

    time_start = datetime.now()

    manhattan_astar_search(puzzle)

    run_time = datetime.now() - time_start

    print("Run time:", run_time.total_seconds())

''' Solves the EightPuzzle using the Maximum of the previous two Heuristics '''
def solve_max(puzzle):
    run_time = 0

    print("Max of Both Heuristics:")

    time_start = datetime.now()

    max_astar_search(puzzle)

    run_time = datetime.now() - time_start

    print("Run time:", run_time.total_seconds())

# ______________________________________________________________________________

class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a duck-shaped board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

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

        # mapping the possible moves for each tile in the duck puzzle 
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # adjusts the delta for up and down based on row:
        # to move up in the middle row only moves two indicies, vs. bottom row which moves 3
        # and vice versa
        if blank < 2:
            delta = {'UP': 0, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank < 6:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else: 
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    # No check_solvability function

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

''' Analyzes 10 random puzzles
for i in range(10):
    rand_puzzle = make_rand_8puzzle()

    solve_default(rand_puzzle)
    solve_manhattan(rand_puzzle)
    solve_max(rand_puzzle)
'''
'''
for i in range(10):
    rand_puzzle = make_rand_duckpuzzle()
    
    solve_default(rand_puzzle)
    solve_manhattan(rand_puzzle)
    solve_max(rand_puzzle)
    print("---------------------------------------------------------------------------")
'''


#def display(state):

