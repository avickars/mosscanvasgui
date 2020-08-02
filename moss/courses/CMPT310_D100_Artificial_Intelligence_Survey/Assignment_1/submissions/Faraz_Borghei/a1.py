# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+ # 
# | a1.py                     | #
# | CMPT 310                  | #
# | Author: Faraz Borghei     | #
# | Student #: 301273484      | #
# | Date Created: May 8, 2020 | #
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+ # 

import time, random
from search import *
MAX_TRIES = 10 # Max tries to generate solvable EightPuzzle state
NUM_RUNS = 1 # Number of runs to perform the three A* heuristic searches
random.seed() # Generate pseudo-random seed based on system time
global_start_time = time.time()

# =============================== #
#  QUESTION 1 - Helper Functions  #
# =============================== #

# Return EightPuzzle instance with a random initial state that is solvable
def make_rand_8puzzle(puzzleType='normal', test=False, debug=False):
    # 1. generate random tuple of inital state
    # 2. check if the permuted state is solvable
    # 3. if it is solvable, return instance; else repeat
    if test:
        test_state = (1, 2, 0, 3, 4, 5, 8, 7, 6)
        display(test_state)
        if puzzleType == 'duck':
            test_eight_puzzle = DuckPuzzle(test_state)
        else:
            test_eight_puzzle = EightPuzzle(test_state)
        return test_eight_puzzle
    counter = 0
    solvable = False
    while not solvable:
        counter += 1 
        if counter > MAX_TRIES: # in case our random generator doesnt work for some reason
            print('Reached max amount of allowed permutation attempts')
            break
        init_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        rand_state_list = random.sample(init_state, k=len(init_state))
        rand_state = tuple(rand_state_list)
        if puzzleType == 'duck':
            eight_puzzle = DuckPuzzle(rand_state)
        else:
            eight_puzzle = EightPuzzle(rand_state)
        solvable = eight_puzzle.check_solvability(rand_state)
        if solvable:
            display(rand_state)
            return eight_puzzle
        if debug:
            print(f'Unsolvable State (Try #{counter}): ')
            display(rand_state)

# Print a 3x3 matrix representation of the 8-puzzle state given in tuple form
def display(state, puzzle='normal'):
    stateStr = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Copy state values to string list
    for i in range(9):
        # Assign * to 0 slot
        if state[i] == 0:
            stateStr[i] = '*'           
        else:
            stateStr[i] = state[i]

    if puzzle == 'duck':
        print(stateStr[0], stateStr[1])
        print(stateStr[2], stateStr[3], stateStr[4], stateStr[5])
        print(stateStr[6], stateStr[7], stateStr[8])
    else:
        print(stateStr[0], stateStr[1], stateStr[2])
        print(stateStr[3], stateStr[4], stateStr[5])
        print(stateStr[6], stateStr[7], stateStr[8])
    print('--------')


# ================================== #
#  QUESTION 2 - Comparing Algorithms #
# ================================== #    

# List of times for the three different heuristics per run
tile_times, max_tile_times, manhattan_times = [], [], []
tile_lengths, manhattan_lengths, max_lengths = [], [], []
tile_nodes_removed, manhattan_nodes_removed, max_nodes_removed = [], [], []
nodes_removed = []

# Taken from search.py (required for keeping track of nodes removed from frontier)
def a1_best_first_graph_search(problem, f, display=False):
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
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        explored.add(node.state)
        nodes_removed.append(node)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

# Taken from search.py (required for keeping track of nodes removed from frontier)
def a1_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return a1_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# Taken from the h function in the EightPuzzle class defined in search.py
def tile_h(node):
    """ Return the heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles """
    return sum(s != g for (s, g) in zip(node.state, (1, 2, 3, 4, 5, 6, 7, 8, 0)))

# Taken from search.ipynb jupyter notebook
def manhattan_h(node):
    state = node.state
    #define goal coordinates for each number and store as dictionary
    index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    x, y = 0, 0
    # populate current index dict
    for i in range(len(state)):
        index_state[state[i]] = index[i] 
    mhd = 0
    # evaluate each mhd
    for i in range(8):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
    return mhd

def max_h(node):
    a = manhattan_h(node)
    b = tile_h(node)
    return max(a, b)

def displayStats(time, length, node):
    print('----------------------------')
    print(f'Time Elapsed: {time}s')
    print('Path Length:', length)
    print('Nodes removed from Frontier:', node)
    print('----------------------------')

# Create 10 (more would be better!) random 8-puzzle instances 
# (using your code from above), and solve each of them using the algorithms below. 
# Each algorithm should be run on the exact same set of problems to make the comparison fair.
def comp_algo(puzzle='normal', test=False, debug=False):
    f = open('a1_data.txt', 'a')
    f.write('Time | Length | Nodes\n')
    for i in range(NUM_RUNS):
        print('===========')
        str = f'RUN #{i+1}'
        print(f'{str:>8}')
        print('===========')
        f.write(f'{str}\n')
        print('Generating random EightPuzzle Problem...')
        rand_puzzle = make_rand_8puzzle(puzzle, test, debug)

        # MISPLACED TILE
        print('Running A* search using the default misplaced tile heuristic...')
        tile_time_start = time.time()
        tile_h_astar = a1_astar_search(rand_puzzle, tile_h, debug).solution()
        tile_time_elapsed = time.time() - tile_time_start
        tile_times.append(tile_time_elapsed)
        tile_lengths.append(len(tile_h_astar))
        tile_nodes_removed.append(len(nodes_removed))
        displayStats(tile_time_elapsed, len(tile_h_astar), len(nodes_removed))
        f.write(f'TILE: {tile_time_elapsed},{len(tile_h_astar)},{len(nodes_removed)}\n')
        nodes_removed.clear()
        # MANHATTAN DISTANCE
        print('Running A* search using the Manhattan Distance heuristics...')
        manhattan_time_start = time.time()
        manhattan_h_astar = a1_astar_search(rand_puzzle, manhattan_h, debug).solution()
        manhattan_time_elapsed = time.time() - manhattan_time_start
        manhattan_times.append(manhattan_time_elapsed)
        manhattan_lengths.append(len(manhattan_h_astar))
        manhattan_nodes_removed.append(len(nodes_removed))
        displayStats(manhattan_time_elapsed, len(manhattan_h_astar), len(nodes_removed))
        f.write(f'MAN: {manhattan_time_elapsed},{len(manhattan_h_astar)},{len(nodes_removed)}\n')
        nodes_removed.clear()
        # MAX
        print('Running A* search using the max of the two heuristics...')
        max_tile_time_start = time.time()
        max_h_astar = a1_astar_search(rand_puzzle, max_h, debug).solution() 
        max_tile_time_elapsed = time.time() - max_tile_time_start
        max_tile_times.append(max_tile_time_elapsed)
        max_lengths.append(len(max_h_astar))
        max_nodes_removed.append(len(nodes_removed))
        displayStats(max_tile_time_elapsed, len(max_h_astar), len(nodes_removed))
        f.write(f'MAX: {max_tile_time_elapsed},{len(max_h_astar)},{len(nodes_removed)}\n')
        nodes_removed.clear()

    print('\n=== TOTAL STATS ===')
    print('*Note: Timing is displayed as average of all values between runs')
    print('\nDefault Misplaced Tile H: ')
    displayStats(mean(tile_times), tile_lengths, tile_nodes_removed)
    print('\nManhattan Distance H:')
    displayStats(mean(manhattan_times), manhattan_lengths, manhattan_nodes_removed)
    print('\nMax of Misplaced Tile H:', mean(max_tile_times))
    displayStats(mean(max_lengths), max_lengths, max_nodes_removed)
    f.close()
    

# =============================== #
#  QUESTION 3 - The House-Puzzle  #
# =============================== #

class DuckPuzzle(Problem):
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

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
            
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
            
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
            
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
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
        return sum(s != g for (s, g) in zip(node.state, self.goal))

# For hardcoded state, set test=True
# To generate random puzzles set test=False
comp_algo('normal', False, True)
global_end_time = time.time() - global_start_time
print('Total Elapsed Time: ', global_end_time)
