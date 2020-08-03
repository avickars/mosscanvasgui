import random
import time
from search import *


# ### Question 1: Helper Functions
# Write a function called **make_rand_8puzzle()** that returns a new instance of an EightPuzzle problem with a random initial state that is solvable. Note that EightPuzzle has a method called check_solvability that you should use to help ensure your initial state is solvable.
# 
# Write a function called **display(state)** that takes an 8-puzzle state (i.e. a tuple that is a permutation of (0, 1, 2, …, 8)) as input and prints a neat and readable representation of it. 0 is the blank, and should be printed as a * character.
# 
# For example, if state is (0, 3, 2, 1, 8, 7, 4, 6, 5), then display(state) should print:

def make_rand_8puzzle():
    state =list((1, 2, 3, 4, 5, 6, 7, 8, 0))
    solvable = False
    eight_puzzle = EightPuzzle(tuple(state))

    while(not solvable):
        random.shuffle(state)
        solvable = eight_puzzle.check_solvability(state)

    eight_puzzle = EightPuzzle(tuple(state)) 
    
    return eight_puzzle

def display(state):
    # convert state to list
    state_list = list(state)
    row_length = 3
    i = 0
    
    for i in range(len(state)):
        print(state[i], end = " ")
        if((i+1) % row_length == 0):
            print()    


# ### Question 2: Comparing Algorithms¶
# Create 10 (more would be better!) random 8-puzzle instances (using your code from above), and solve each of them using the algorithms below. Each algorithm should be run on the exact same set of problems to make the comparison fair.
# 
# For each solved problem, record:
# 
# the total running time in seconds
# the length (i.e. number of tiles moved) of the solution
# that total number of nodes that were removed from frontier
# You will probably need to make some modifications to the A* code to get all this data.
# 
# Also, be aware that the time it takes to solve random 8-puzzle instances can vary from less than a second to hundreds of seconds — so solving all these problems might take some time!
# 
# The algorithms you should test are:
# 
# - A*-search using the misplaced tile heuristic (this is the default heuristic in the EightPuzzle class)
# - A*-search using the Manhattan distance heuristic Please implement your own (correctly working!) version of the Manhattan heuristic. (Be careful: there is an incorrect Manhattan distance function in tests/test_search.py. So don’t use that!)
# - A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic
# Summarize all your data in a single table in a spreadsheet as described below.
# 
# Based on your data, which algorithm is the best? Explain how you came to your conclusion.

class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
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

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum((s != 0 and s != g) for (s, g) in zip(node.state, self.goal))
    
def manhattan(node):
    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        
    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0
    
    # exclude 0 since it's not a tile
    for i in range(1,9):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

    return mhd

def max_distance(node):
    eight_puzzle = EightPuzzle(node.state)
    return max(manhattan(node), eight_puzzle.h(node))

# search.py functions:

# astar_search
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# best_first_graph_search
def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    remove_counter = 0
    
    while frontier:
        node = frontier.pop()
        remove_counter += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, remove_counter
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    
    return None, remove_counter


# ### Question 3: The House-Puzzle¶
# (Duck-puzzle) Implement a new Problem class called DuckPuzzle that is the same as the 8-puzzle, except the board has this shape (that looks a bit like a duck facing to the left)
#    
# Tiles slide into the blank (the *) as in the regular 8-puzzle, but now the board has a different shape which changes the possible moves.
# 
# As in the previous question, test this problem using the same approach, and the same algorithms, as in the previous problem.
# 
# Be careful generating random instances: the check_solvability function from the EightPuzzle probably doesn’t work with this board!

# adapted from aima-python eight puzzle 
class DuckPuzzle(Problem):

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
        if index_blank_square == 2 or index_blank_square >= 6:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        # delta changes depending where blank is
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
        "does not need to be implemented according to Prof"

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum((s != 0 and s != g) for (s, g) in zip(node.state, self.goal))
    
# generate random valid state by traversing backwards from goal state
def make_rand_dpuzzle():
    # start from goal state
    dp = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))
    
    for i in range(10000000):
        state = dp.initial
        # find valid actions for 0-tile from current state
        # and randomly select one of the valid actions
        action = random.choice(dp.actions(state))
        # render new state from selected, valid action
        dp.initial = dp.result(state, action)
    
    dp = DuckPuzzle(tuple(dp.initial))

    return dp       
        
def duck_manhattan(node):
    state = node.state
    index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
    index_state = {}
    index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]
        
    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0
    
    # exclude 0 since it's not a tile
    for i in range(1,9):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
            
    return mhd
            
def duck_max_distance(node):
    duck_puzzle = DuckPuzzle(node.state)
    return max(duck_manhattan(node), duck_puzzle.h(node))

# Tests------------------------------------------------------------------------------------------------------------
# Test Problem #1
p = make_rand_8puzzle()
print(p.initial)
display(p.initial)

# Test Problem #2
for i in range(10):
    eight_puzzle = make_rand_8puzzle()
    print('Puzzle #', (i + 1), ': ', eight_puzzle.initial)

    # misplaced tile heuristic
    start_time = time.time()
    astar, rm_nodes = astar_search(eight_puzzle)
    elapsed_time = time.time() - start_time
    
    print('A*-search using the misplaced tile heuristic')
    print('The total running time in seconds: ', elapsed_time)
    print('The length of solution: ', len(astar.solution()))
    print('The total number of nodes that were removed from frontier: ', rm_nodes)

    # Manhattan distance heuristic
    start_time = time.time()
    astar, rm_nodes = astar_search(eight_puzzle, h = manhattan)
    elapsed_time = time.time() - start_time
    
    print('A*-search using the Manhattan distance heuristic')
    print('The total running time in seconds: ', elapsed_time)
    print('The length of solution: ', len(astar.solution()))
    print('The total number of nodes that were removed from frontier: ', rm_nodes)

    # max of the misplaced tile and Manhattan heuristic
    start_time = time.time()
    astar, rm_nodes = astar_search(eight_puzzle, h = max_distance)
    elapsed_time = time.time() - start_time
    
    print('A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic')
    print('The total running time in seconds: ', elapsed_time)
    print('The length of solution: ', len(astar.solution()))
    print('The total number of nodes that were removed from frontier: ', rm_nodes)

# Test Problem #3
for i in range(10):
    duck_puzzle = make_rand_dpuzzle()
    print('Puzzle #', (i + 1), ': ', duck_puzzle.initial)

    # misplaced tile heuristic
    start_time = time.time()
    astar, rm_nodes = astar_search(duck_puzzle)
    elapsed_time = time.time() - start_time
    
    print('A*-search using the misplaced tile heuristic')
    print('The total running time in seconds: ', elapsed_time)
    print('The length of solution: ', len(astar.solution()))
    print('The total number of nodes that were removed from frontier: ', rm_nodes)

    # Manhattan distance heuristic
    start_time = time.time()
    astar, rm_nodes = astar_search(duck_puzzle, h = duck_manhattan)
    elapsed_time = time.time() - start_time
    
    print('A*-search using the Manhattan distance heuristic')
    print('The total running time in seconds: ', elapsed_time)
    print('The length of solution: ', len(astar.solution()))
    print('The total number of nodes that were removed from frontier: ', rm_nodes)

    # max of the misplaced tile and Manhattan heuristic
    start_time = time.time()
    astar, rm_nodes = astar_search(duck_puzzle, h = duck_max_distance)
    elapsed_time = time.time() - start_time
    
    print('A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic')
    print('The total running time in seconds: ', elapsed_time)
    print('The length of solution: ', len(astar.solution()))
    print('The total number of nodes that were removed from frontier: ', rm_nodes)