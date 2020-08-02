# a1.py

from search import *
from random import randint, seed
from time import time

# I generated a random number from 1 - 1,000,000 on random.org. This value will be used for the seed
# This will ensure that the randomly generated puzzles are the same between runs
seed(6357)

# Question 1: Helper Functions -----------------------------------------------------------------------

# for use in display() only
# Returns the numbers within a tuple in a string
def print_line(tup):
    line = ""
    for i in tup:
        num = str(i)
        if num == "0":
            line += "* "
        else:
            line += num + " "
    
    return line

def display(state):
    print(print_line(state[0:3]))
    print(print_line(state[3:6]))
    print(print_line(state[6:9]))

# Perform 100 random moves from the goal state to make a random solvable initial state
def make_rand_8puzzle():

    possible_moves = []

    new_8puzzle = EightPuzzle((1,2,3,4,5,6,7,8,0))
    state = new_8puzzle.initial
    
    # Perform 100 random moves from the goal state to make a random solvable initial state
    for i in range (100):
        possible_moves = new_8puzzle.actions(state)
        num_possible_moves = len(possible_moves)
        rand_move = possible_moves[randint(0, num_possible_moves - 1)]
        state = new_8puzzle.result(state, rand_move)

    new_8puzzle.initial = state

    return new_8puzzle

# ----------------------------------------------------------------------------------------------------

# Question 2: Comparing Algorithms -------------------------------------------------------------------


# Copied from search.py to make some modifications
def my_best_first_graph_search(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    nodes_removed = 0
    while frontier:
        node = frontier.pop()
        nodes_removed += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return (node, nodes_removed)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

# copied from search.py to make some modifications
def my_astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return my_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def solve_puzzles(puzzles, heuristic, heuristic_name):

    print ("\n--- Now solving puzzles for the " + heuristic_name + " ---\n")

    i = 1
    for puzz in puzzles:
        print ("Solving puzzle " + str(i))

        # Time functionality from: https://docs.python.org/3/library/time.html#time.time
        starttime = time()
        (solution, nodes_removed) = my_astar_search(puzz, heuristic)
        time_elapsed = time() - starttime
        print ("Seconds to solve this puzzle:       " + str(time_elapsed))
        print ("Moves to the solution:              " + str(solution.depth))
        print ("Nodes removed from the frontier:    " + str(nodes_removed) + "\n")
        i += 1

### HEURISTIC FUNCTIONS ###########################################

# adapted from the h() method from class EightPuzzle in search.py
def displaced(node):
    return sum(s != g for (s, g) in zip(node.state, (1,2,3,4,5,6,7,8,0)))

# adapted from manhattan() from tests/test_search.py
def manhattan(node):
    state = node.state
    index_goal = {  0: [2, 2], 
                    1: [0, 0], 
                    2: [0, 1], 
                    3: [0, 2], 
                    4: [1, 0], 
                    5: [1, 1], 
                    6: [1, 2], 
                    7: [2, 0], 
                    8: [2, 1]}
    index = [   [0, 0], 
                [0, 1], 
                [0, 2], 
                [1, 0], 
                [1, 1], 
                [1, 2], 
                [2, 0], 
                [2, 1], 
                [2, 2]]

    mhd = 0

    for i in range(9):
        num = state[i]
        curr_pos = index[i]
        goal_pos = index_goal[num]

        for j in range(2):
            mhd += abs(curr_pos[j] - goal_pos[j])

    return mhd

# returns the max of the displaced() and manhattan()
def max_displace_manhattan(node):
    displaced_tiles = displaced(node)
    manhattan_distance = manhattan(node)

    return(max(displaced_tiles, manhattan_distance))

###################################################################



### PUZZLE GENERATION #############################################

print ("\n\n######### 8-PUZZLE SECTION #########\n\n")

print ("\nThese are the randomly generated 8-puzzles:\n")

# Create a set of 15 random 8-puzzles
puzzle_set = []

for i in range(15):
    rand_puzz = make_rand_8puzzle()
    puzzle_set.append(rand_puzz)
    print ("8-Puzzle " + str(i + 1) + ":\n")
    display(rand_puzz.initial)
    print()

###################################################################



### DATA COLLECTION ###############################################

solve_puzzles(puzzle_set, displaced, "Misplaced Tile Heuristic")
solve_puzzles(puzzle_set, manhattan, "Manhattan Distance Heuristic")
solve_puzzles(puzzle_set, max_displace_manhattan, "Max of Displaced and Manhattan")

###################################################################

# ----------------------------------------------------------------------------------------------------


# Question 3: House Puzzle ---------------------------------------------------------------------------

# Adapted from class EightPuzzle
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

        if index_blank_square in [0, 2, 6]:
            possible_actions.remove('LEFT')
        if index_blank_square in [0, 1, 4, 5]:
            possible_actions.remove('UP')
        if index_blank_square in [1, 5, 8]:
            possible_actions.remove('RIGHT')
        if index_blank_square in [2, 6, 7, 8]:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        up = 0
        down = 0

        if action == 'UP' and blank in [2, 3]:
            up = 1
        if action == 'DOWN' and blank in [0, 1]:
            down = 1

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action] + up - down
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

def display_duck(state):
    print(print_line(state[0:2]))
    print(print_line(state[2:6]))
    print ("  " + print_line(state[6:9]))

def make_rand_duckpuzzle():

    possible_moves = []

    new_duckpuzzle = DuckPuzzle((1,2,3,4,5,6,7,8,0))
    state = new_duckpuzzle.initial
    
    # Perform 100 random moves from the goal state to make a random solvable initial state
    for i in range (100):
        possible_moves = new_duckpuzzle.actions(state)
        num_possible_moves = len(possible_moves)
        rand_move = possible_moves[randint(0, num_possible_moves - 1)]
        state = new_duckpuzzle.result(state, rand_move)

    new_duckpuzzle.initial = state

    return new_duckpuzzle

print ("\n\n######### DUCK PUZZLE SECTION #########\n\n")

print ("\nThese are the randomly generated Duck puzzles:\n")

# Create 15 random solvable duck puzzles
duck_set = []

for i in range(15):
    rand_puzz = make_rand_duckpuzzle()
    duck_set.append(rand_puzz)
    print ("Duck Puzzle " + str(i + 1) + ":\n")
    display_duck(rand_puzz.initial)
    print()

solve_puzzles(duck_set, displaced, "Misplaced Tile Heuristic")
solve_puzzles(duck_set, manhattan, "Manhattan Distance Heuristic")
solve_puzzles(duck_set, max_displace_manhattan, "Max of Displaced and Manhattan")

# ----------------------------------------------------------------------------------------------------
