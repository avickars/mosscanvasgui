"""
Assignment #1
-------------
CMPT 310
Mark Nielsen
301348725
Last updated: May 29, 2020
-------------
-------------
References:
    All following code is my own, however many functions were heavily inspired / derived from their counterparts within
    aima-python search.py

    As well, while no code was copied, tutorial_1.py (author: mahkh) and tutorial_2.py (author: mahkh) were
    heavily reference over the course of writing this program. Particularly with regard to forming calls
    to a*star_search and the use of python dictionaries
"""


import random
import math
import time
from search import *

"""
GLOBAL PARAMETERS
#################

DEBUG:        = True will print additional information for debug & testing
      Default = False
      
ALLTESTS:     = True will run all test drivers, ALLTESTS = False will give a slimmed down test suite (1 / heuristic)
      Default = False
      
DISPLAYSTATS: = True will enable additional information including run time, path, path_length. Path and path_length
                are acquired using the "display" parameter of A* search. See search.py for more details
      Default = True
      
#################
"""
DEBUG = False
ALLTESTS = True
MORETESTS = False
DISPLAYSTATS = True


"""
PART 1
Helper Functions

make_rand_8puzzle()
    returns a newly generated, solvable 8_Puzzle. As well it returns the tuple
    representation of the board, useful for testing other functions.
    
display(state)
    takes a tuple representation of an eight puzzle as an argument
    and prints it as a 3x3 grid. Replaces the value 0 with *
    
"""


def make_rand_8puzzle():
    tiles = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    solvable = False
    while not solvable:
        tiles_l = list(tiles)
        tiles_shuffled = tuple(random.sample(tiles_l, 9))
        rand_eight = EightPuzzle(tiles_shuffled)
        if EightPuzzle.check_solvability(rand_eight, tiles_shuffled):
            solvable = True
    return rand_eight, tiles_shuffled


def display(state):
    row_split = tuple(state[x:x + 3] for x in range(0, len(state), 3))
    row_1 = ' '.join(map(str, row_split[0]))
    row_2 = ' '.join(map(str, row_split[1]))
    row_3 = ' '.join(map(str, row_split[2]))
    print(row_1.replace("0", "*"))
    print(row_2.replace("0", "*"))
    print(row_3.replace("0", "*"))


"""
PART 2
Eight Puzzle heuristic functions. 
Testing for PART 2 can be found in "PART 4 - TEST DRIVERS"

NOTE: All heuristics were implemented to avoid counting the *(0) tile in their tally. Failing to do
      this prevents the heuristics guaranteeing A*search performs optimally
--------------------

misplaced_tile(node)
    The misplaced tile heuristic. Returns the number of tiles out of position by checking if their 
    current position is equal to their position in the goal state.
    Returns values in the range: 0 (solved board) -> 8 (every tile out of position) 
    
manhattan(node)
    The manhattan tile heuristic. Takes a node as an argument, and returns the sum of the manhattan distance
    for each tile (i.e. the sum of how many moves it would take for each tile to be in place).
    
max_h(node)
    Returns the max of manhattan and misplaced_tile. In practice this is almost always the manhattan heuristic.
    Turn on DEBUG to print which is used.
"""


def misplaced_tile(node):
    state = node.state
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    mpt = sum(s != g for (s, g) in zip(node.state, goal))
    if state[8] != 0:
        mpt += -1
    return mpt


def manhattan(node):
    state = node.state
    mhd = 0
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    index_state = dict(zip(state, index))
    if DEBUG:
        print("index_state = ", index_state)
        print("index_goal = ", index_goal)
    for t in index_state.keys():
        if t != 0:
            [x1, y1] = index_state[t]
            [x2, y2] = index_goal[t]
            mhd += (abs(x1 - x2) + abs(y1 - y2))
            if DEBUG:
                print("Tile:", t, "x1, y1 = ", [x1, y1], "x2, y2 = ", [x2, y2])
                print("Manhattan heuristic total: ", mhd)
    return mhd


def max_h(node):
    score_mh = manhattan(node)
    score_mp = misplaced_tile(node)
    if DEBUG:
        print("Manhattan h = ", score_mh, "Misplaced-Tile h = ", score_mp)
        if score_mh > score_mp:
            print("max_h using manhattan heuristic")
        else:
            print("max_h using misplaced_tile heuristic")
    return max(score_mh, score_mp)


"""
PART 3
The Duck Puzzle heuristics and helper functions
Testing for PART 2 can be found in "PART 4 - TEST DRIVERS"

NOTE: All heuristics were implemented to avoid counting the *(0) tile in their tally. Failing to do
      this prevents the heuristics guaranteeing A*search performs optimally
--------------------

DuckPuzzle(Problem)
    Implementation of the duck puzzle as a descendant of the Problem class. This class was created by
    altering the EightPuzzle(Problem) class to work with the duck puzzle board. Actions, and the result
    of actions have been appropriately modified to suit the new board shape.
    
make_rand_duckpuzzle()
    Generates a new duck puzzle problem by making random, valid moves to a board in the solved state. The
    default number of moves to shuffle is 2000. Returns a DuckPuzzle object. As well, it returns a tuple
    representing the state of the duck puzzle board, useful for testing.
    
duck_display(state)
    Takes a duck puzzle board represented as a tuple, and prints the board. Replaces 0 with *
    Derived from display(state)
    
duck_misplaced_tile(node)
    The misplaced tile heuristic, modified to work with the duck puzzle
    Takes a node containing a duckpuzzle board as an argument and returns the number of
    tiles out of place
    
duck_manhattan(node)
    The manhattan tile heuristic, modified to work with the duck puzzle
    Takes a node containing a duckpuzzle board as an argument, and returns the sum of the
    manhattan distance formula for all tiles
    
duck_max_h(node)
    Takes a node containing a duckpuzzle board as an argument, and returns the max of
    duck_misplaced_tile(node) and duck_manhattan_node
"""


class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a board with 3 rows, the top row is 2 squares,
    middle is 4, and bottom is 3, where one of the squares is a blank. The board kinda looks like a duck
    A state is represented as a tuple of length 9, where  element at index i represents the tile number
    at index i (0 if it's an empty square). The layout of the goal state is given below. This class is a
    modified version of EightPuzzle from aima-python.

    Board Example in the goal state:
     ___ ___
    |_1_|_2_|___ ___
    |_3_|_4_|_5_|_6_|
        |_7_|_8_|_*_|

    """

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

        # blank is the index of the blank tile
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank in [6, 7, 8]:
            delta = {'UP': -3, 'DOWN': +3, 'LEFT': -1, 'RIGHT': 1}

        elif blank in [2, 3, 4, 5]:
            delta = {'UP': -2, 'DOWN': +3, 'LEFT': -1, 'RIGHT': 1}

        else:
            delta = {'UP': -2, 'DOWN': +2, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal


def make_rand_duckpuzzle():
    tiles = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    for s in range(2000):
        void_counter = s

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        blank = tiles.index(0)
        # print(blank, "loop:", s)

        # Remove action based on position of blank
        if blank in [0, 2, 6]:
            possible_actions.remove('LEFT')
        if blank in [0, 1, 4, 5]:
            possible_actions.remove('UP')
        if blank in [1, 5, 8]:
            possible_actions.remove('RIGHT')
        if blank in [2, 6, 7, 8]:
            possible_actions.remove('DOWN')

        # Set appropriate delta based on position of blank
        if blank in [6, 7, 8]:
            delta = {'UP': -3, 'DOWN': +3, 'LEFT': -1, 'RIGHT': 1}

        elif blank in [2, 3, 4, 5]:
            delta = {'UP': -2, 'DOWN': +3, 'LEFT': -1, 'RIGHT': 1}

        elif blank in [0, 1]:
            delta = {'UP': -2, 'DOWN': +2, 'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[random.choice(possible_actions)]
        tiles[blank], tiles[neighbor] = tiles[neighbor], tiles[blank]

        duck_puzzle = DuckPuzzle(tuple(tiles))
    return duck_puzzle, tuple(tiles)


def duck_display(state):
    split_1 = tuple(state[:2])
    split_2 = tuple(state[2:6])
    split_3 = tuple(state[6:9])
    row_1 = ' '.join(map(str, split_1))
    row_2 = ' '.join(map(str, split_2))
    row_3 = ' '.join(map(str, split_3))
    print(row_1.replace("0", "*"))
    print(row_2.replace("0", "*"))
    print(" ", row_3.replace("0", "*"))


def duck_misplaced_tile(node):
    state = node.state
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    mpt = sum(s != g for (s, g) in zip(node.state, goal))
    if state[8] != 0:
        mpt += -1
    return mpt


def duck_manhattan(node):
    state = node.state
    mhd = 0
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 0], 8: [2, 1]}
    index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2]]
    index_state = dict(zip(state, index))
    if DEBUG:
        print("index_state = ", index_state)
        print("index_goal = ", index_goal)
    for t in index_state.keys():
        if t != 0:
            [x1, y1] = index_state[t]
            [x2, y2] = index_goal[t]
            mhd += (abs(x1 - x2) + abs(y1 - y2))
            if DEBUG:
                print("Tile:", t, "x1, y1 = ", [x1, y1], "x2, y2 = ", [x2, y2])
                print("Manhattan heuristic total: ", mhd)
    return mhd


def duck_max_h(node):
    score_dmh = duck_manhattan(node)
    score_dmp = duck_misplaced_tile(node)
    if DEBUG:
        print("Manhattan h = ", score_mh, "Misplaced-Tile h = ", score_mp)
        if score_mh > score_mp:
            print("max_h using manhattan heuristic")
        else:
            print("max_h using misplaced_tile heuristic")
    return max(score_dmh, score_dmp)


"""
PART 4
Test Drivers
In this section you will find all the heuristic tests, along with timing info.
By default, all tests will be run and will print:
    - The start state of the board
    - Puzzle #, Type, and Heuristic being used
    - Solution, in steps
    
An average of each test types [determined by puzzle type + heuristic used] runtime will
be given when testing completes.

To display timing info, path and path_length set DISPLAYSTATS = True in Global Parameters
To run only one test of each time, set ALLTESTS = False in Global Parameters

"""

"""Test Specific Puzzle Layouts"""
RunTestPuzzle = False
if RunTestPuzzle:
    test_state = (3, 4, 1, 2, 0, 6, 8, 7, 5)
    puzzle_test = EightPuzzle(test_state)

    print("\n")
    print(" EightPuzzle test_state - A* Search using Manhattan h")
    display(test_state)
    node_test = astar_search(puzzle_test, h=manhattan, display=DISPLAYSTATS)
    if DISPLAYSTATS:
        print('Path:', node_test.path())
        print("Path length: ", len(node_test.path()) - 1)
    print('Solution:', node_test.solution())


"""
Generate 10 Eight Puzzles
# variables in the style: puzzle# are EightPuzzle Objects
# variables in the style: puzzle_s# are tuples containing the initial EightPuzzle state
"""

puzzle1, puzzle_s1 = make_rand_8puzzle()
if ALLTESTS:
    puzzle2, puzzle_s2 = make_rand_8puzzle()
    puzzle3, puzzle_s3 = make_rand_8puzzle()
    puzzle4, puzzle_s4 = make_rand_8puzzle()
    puzzle5, puzzle_s5 = make_rand_8puzzle()
    puzzle6, puzzle_s6 = make_rand_8puzzle()
    puzzle7, puzzle_s7 = make_rand_8puzzle()
    puzzle8, puzzle_s8 = make_rand_8puzzle()
    puzzle9, puzzle_s9 = make_rand_8puzzle()
    puzzle10, puzzle_s10 = make_rand_8puzzle()

misplaced_8Puzzle_average_time = 0
manhattan_8Puzzle_average_time = 0
max_h_8Puzzle_average_time = 0


"""
Test solving EightPuzzles using an A* Search utilizing the misplaced tile heuristic
The puzzles initial state is printed using display(state)
The time taken is timed using standard time functions
Number of nodes removed from frontier is given by "# paths have been expanded"
"""


# Puzzle 1
print("\n")
print(" EightPuzzle 1 - A* Search using Misplaced Tile Heuristic")
display(puzzle_s1)
start_time_p_mt1 = time.time()
node_p_mt1 = astar_search(puzzle1, h=misplaced_tile, display=DISPLAYSTATS)
elapsed_time_p_mt1 = time.time() - start_time_p_mt1
misplaced_8Puzzle_average_time += elapsed_time_p_mt1
if DISPLAYSTATS:
    print("Run time: ", elapsed_time_p_mt1)
    print("Path length: ", len(node_p_mt1.path()) - 1)
    print('Path:', node_p_mt1.path())
print('Solution:', node_p_mt1.solution())

if ALLTESTS:
    # Puzzle 2
    print("\n")
    print("EightPuzzle 2 - A* Search using Misplaced Tile Heuristic")
    display(puzzle_s2)
    start_time_p_mt2 = time.time()
    node_p_mt2 = astar_search(puzzle2, h=misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_p_mt2 = time.time() - start_time_p_mt2
    misplaced_8Puzzle_average_time += elapsed_time_p_mt2
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mt2)
        print("Path length: ", len(node_p_mt2.path()) - 1)
        print('Path:', node_p_mt2.path())
    print('Solution:', node_p_mt2.solution())
    
    # Puzzle 3
    print("\n")
    print("EightPuzzle 3 - A* Search using Misplaced Tile Heuristic")
    display(puzzle_s3)
    start_time_p_mt3 = time.time()
    node_p_mt3 = astar_search(puzzle3, h=misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_p_mt3 = time.time() - start_time_p_mt3
    misplaced_8Puzzle_average_time += elapsed_time_p_mt3
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mt3)
        print("Path length: ", len(node_p_mt3.path()) - 1)
        print('Path:', node_p_mt3.path())
    print('Solution:', node_p_mt3.solution())
    
    # Puzzle 4
    print("\n")
    print("EightPuzzle 4 - A* Search using Misplaced Tile Heuristic")
    display(puzzle_s1)
    start_time_p_mt4 = time.time()
    node_p_mt4 = astar_search(puzzle4, h=misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_p_mt4 = time.time() - start_time_p_mt4
    misplaced_8Puzzle_average_time += elapsed_time_p_mt4
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mt4)
        print("Path length: ", len(node_p_mt4.path()) - 1)
        print('Path:', node_p_mt4.path())
    print('Solution:', node_p_mt4.solution())
    
    # Puzzle 5
    print("\n")
    print("EightPuzzle 5 - A* Search using Misplaced Tile Heuristic")
    display(puzzle_s5)
    start_time_p_mt5 = time.time()
    node_p_mt5 = astar_search(puzzle5, h=misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_p_mt5 = time.time() - start_time_p_mt5
    misplaced_8Puzzle_average_time += elapsed_time_p_mt5
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mt5)
        print("Path length: ", len(node_p_mt5.path()) - 1)
        print('Path:', node_p_mt5.path())
    print('Solution:', node_p_mt5.solution())
    
    # Puzzle 6
    print("\n")
    print("EightPuzzle 6 - A* Search using Misplaced Tile Heuristic")
    display(puzzle_s6)
    start_time_p_mt6 = time.time()
    node_p_mt6 = astar_search(puzzle6, h=misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_p_mt6 = time.time() - start_time_p_mt6
    misplaced_8Puzzle_average_time += elapsed_time_p_mt6
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mt6)
        print("Path length: ", len(node_p_mt6.path()) - 1)
        print('Path:', node_p_mt6.path())
    print('Solution:', node_p_mt6.solution())
    
    # Puzzle 7
    print("\n")
    print("EightPuzzle 7 - A* Search using Misplaced Tile Heuristic")
    display(puzzle_s7)
    start_time_p_mt7 = time.time()
    node_p_mt7 = astar_search(puzzle7, h=misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_p_mt7 = time.time() - start_time_p_mt7
    misplaced_8Puzzle_average_time += elapsed_time_p_mt7
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mt7)
        print("Path length: ", len(node_p_mt7.path()) - 1)
        print('Path:', node_p_mt7.path())
    print('Solution:', node_p_mt7.solution())
    
    # Puzzle 8
    print("\n")
    print("EightPuzzle 8 - A* Search using Misplaced Tile Heuristic")
    display(puzzle_s8)
    start_time_p_mt8 = time.time()
    node_p_mt8 = astar_search(puzzle8, h=misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_p_mt8 = time.time() - start_time_p_mt8
    misplaced_8Puzzle_average_time += elapsed_time_p_mt8
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mt8)
        print("Path length: ", len(node_p_mt8.path())-1)
        print('Path:', node_p_mt8.path())
    print('Solution:', node_p_mt8.solution())
    
    # Puzzle 9
    print("\n")
    print("EightPuzzle 9 - A* Search using Misplaced Tile Heuristic")
    display(puzzle_s9)
    start_time_p_mt9 = time.time()
    node_p_mt9 = astar_search(puzzle9, h=misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_p_mt9 = time.time() - start_time_p_mt9
    misplaced_8Puzzle_average_time += elapsed_time_p_mt9
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mt9)
        print("Path length: ", len(node_p_mt9.path()) - 1)
        print('Path:', node_p_mt9.path())
    print('Solution:', node_p_mt9.solution())
    
    # Puzzle 10
    print("\n")
    print("EightPuzzle 10 - A* Search using Misplaced Tile Heuristic")
    display(puzzle_s10)
    start_time_p_mt10 = time.time()
    node_p_mt10 = astar_search(puzzle10, h=misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_p_mt10 = time.time() - start_time_p_mt10
    misplaced_8Puzzle_average_time += elapsed_time_p_mt10
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mt10)
        print("Path length: ", len(node_p_mt10.path()) - 1)
        print('Path:', node_p_mt10.path())
    print('Solution:', node_p_mt10.solution())


"""
Test solving EightPuzzles using an A* Search utilizing the Manhattan tile heuristic
The puzzles initial state is printed using display(state)
The time taken is timed using standard time functions
Number of nodes removed from frontier is given by "# paths have been expanded"
"""

# Puzzle 1
print("\n")
print("EightPuzzle 1 - A* Search using Manhattan Tile Heuristic")
display(puzzle_s1)
start_time_p_mh1 = time.time()
node_p_mh1 = astar_search(puzzle1, h=manhattan, display=DISPLAYSTATS)
elapsed_time_p_mh1 = time.time() - start_time_p_mh1
manhattan_8Puzzle_average_time += elapsed_time_p_mh1
if DISPLAYSTATS:
    print("Run time: ", elapsed_time_p_mh1)
    print("Path length: ", len(node_p_mh1.path()) - 1)
    print('Path:', node_p_mh1.path())
print('Solution:', node_p_mh1.solution())

if ALLTESTS:
    # Puzzle 2
    print("\n")
    print("EightPuzzle 2 - A* Search using Manhattan Tile Heuristic")
    display(puzzle_s2)
    start_time_p_mh2 = time.time()
    node_p_mh2 = astar_search(puzzle2, h=manhattan, display=DISPLAYSTATS)
    elapsed_time_p_mh2 = time.time() - start_time_p_mh2
    manhattan_8Puzzle_average_time += elapsed_time_p_mh2
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mh2)
        print("Path length: ", len(node_p_mh2.path()) - 1)
        print('Path:', node_p_mh2.path())
    print('Solution:', node_p_mh2.solution())

    # Puzzle 3
    print("\n")
    print("EightPuzzle 3 - A* Search using Manhattan Tile Heuristic")
    display(puzzle_s3)
    start_time_p_mh3 = time.time()
    node_p_mh3 = astar_search(puzzle3, h=manhattan, display=DISPLAYSTATS)
    elapsed_time_p_mh3 = time.time() - start_time_p_mh3
    manhattan_8Puzzle_average_time += elapsed_time_p_mh3
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mh3)
        print("Path length: ", len(node_p_mh3.path()) - 1)
        print('Path:', node_p_mh3.path())
    print('Solution:', node_p_mh3.solution())

    # Puzzle 4
    print("\n")
    print("EightPuzzle 4 - A* Search using Manhattan Tile Heuristic")
    display(puzzle_s1)
    start_time_p_mh4 = time.time()
    node_p_mh4 = astar_search(puzzle4, h=manhattan, display=DISPLAYSTATS)
    elapsed_time_p_mh4 = time.time() - start_time_p_mh4
    manhattan_8Puzzle_average_time += elapsed_time_p_mh4
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mh4)
        print("Path length: ", len(node_p_mh4.path()) - 1)
        print('Path:', node_p_mh4.path())
    print('Solution:', node_p_mh4.solution())

    # Puzzle 5
    print("\n")
    print("EightPuzzle 5 - A* Search using Manhattan Tile Heuristic")
    display(puzzle_s5)
    start_time_p_mh5 = time.time()
    node_p_mh5 = astar_search(puzzle5, h=manhattan, display=DISPLAYSTATS)
    elapsed_time_p_mh5 = time.time() - start_time_p_mh5
    manhattan_8Puzzle_average_time += elapsed_time_p_mh5
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mh5)
        print("Path length: ", len(node_p_mh5.path()) - 1)
        print('Path:', node_p_mh5.path())
    print('Solution:', node_p_mh5.solution())

    # Puzzle 6
    print("\n")
    print("EightPuzzle 6 - A* Search using Manhattan Tile Heuristic")
    display(puzzle_s6)
    start_time_p_mh6 = time.time()
    node_p_mh6 = astar_search(puzzle6, h=manhattan, display=DISPLAYSTATS)
    elapsed_time_p_mh6 = time.time() - start_time_p_mh6
    manhattan_8Puzzle_average_time += elapsed_time_p_mh6
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mh6)
        print("Path length: ", len(node_p_mh6.path()) - 1)
        print('Path:', node_p_mh6.path())
    print('Solution:', node_p_mh6.solution())

    # Puzzle 7
    print("\n")
    print("EightPuzzle 7 - A* Search using Manhattan Tile Heuristic")
    display(puzzle_s7)
    start_time_p_mh7 = time.time()
    node_p_mh7 = astar_search(puzzle7, h=manhattan, display=DISPLAYSTATS)
    elapsed_time_p_mh7 = time.time() - start_time_p_mh7
    manhattan_8Puzzle_average_time += elapsed_time_p_mh7
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mh7)
        print("Path length: ", len(node_p_mh7.path()) - 1)
        print('Path:', node_p_mh7.path())
    print('Solution:', node_p_mh7.solution())

    # Puzzle 8
    print("\n")
    print("EightPuzzle 8 - A* Search using Manhattan Tile Heuristic")
    display(puzzle_s8)
    start_time_p_mh8 = time.time()
    node_p_mh8 = astar_search(puzzle8, h=manhattan, display=DISPLAYSTATS)
    elapsed_time_p_mh8 = time.time() - start_time_p_mh8
    manhattan_8Puzzle_average_time += elapsed_time_p_mh8
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mh8)
        print("Path length: ", len(node_p_mh8.path()) - 1)
        print('Path:', node_p_mh8.path())
    print('Solution:', node_p_mh8.solution())

    # Puzzle 9
    print("\n")
    print("EightPuzzle 9 - A* Search using Manhattan Tile Heuristic")
    display(puzzle_s9)
    start_time_p_mh9 = time.time()
    node_p_mh9 = astar_search(puzzle9, h=manhattan, display=DISPLAYSTATS)
    elapsed_time_p_mh9 = time.time() - start_time_p_mh9
    manhattan_8Puzzle_average_time += elapsed_time_p_mh9
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mh9)
        print("Path length: ", len(node_p_mh9.path()) - 1)
        print('Path:', node_p_mh9.path())
    print('Solution:', node_p_mh9.solution())

    # Puzzle 10
    print("\n")
    print("EightPuzzle 10 - A* Search using Manhattan Tile Heuristic")
    display(puzzle_s10)
    start_time_p_mh10 = time.time()
    node_p_mh10 = astar_search(puzzle10, h=manhattan, display=DISPLAYSTATS)
    elapsed_time_p_mh10 = time.time() - start_time_p_mh10
    manhattan_8Puzzle_average_time += elapsed_time_p_mh10
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mh10)
        print("Path length: ", len(node_p_mh10.path()) - 1)
        print('Path:', node_p_mh10.path())
    print('Solution:', node_p_mh10.solution())


"""
Test solving EightPuzzles using an A* Search utilizing the max of the Manhattan tile & Misplaced tile heuristics
The puzzles initial state is printed using display(state)
The time taken is timed using standard time functions
Number of nodes removed from frontier is given by "# paths have been expanded"
"""

# Puzzle 1
print("\n")
print("EightPuzzle 1 - A* Search using max of Manhattan tile & Misplaced tile heuristics")
display(puzzle_s1)
start_time_p_mx1 = time.time()
node_p_mx1 = astar_search(puzzle1, h=max_h, display=DISPLAYSTATS)
elapsed_time_p_mx1 = time.time() - start_time_p_mx1
max_h_8Puzzle_average_time += elapsed_time_p_mx1
if DISPLAYSTATS:
    print("Run time: ", elapsed_time_p_mx1)
    print("Path length: ", len(node_p_mx1.path()) - 1)
    print('Path:', node_p_mx1.path())
print('Solution:', node_p_mx1.solution())

if ALLTESTS:
    # Puzzle 2
    print("\n")
    print("EightPuzzle 2 - A* Search using max of Manhattan tile & Misplaced tile heuristics")
    display(puzzle_s2)
    start_time_p_mx2 = time.time()
    node_p_mx2 = astar_search(puzzle2, h=max_h, display=DISPLAYSTATS)
    elapsed_time_p_mx2 = time.time() - start_time_p_mx2
    max_h_8Puzzle_average_time += elapsed_time_p_mx2
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mx2)
        print("Path length: ", len(node_p_mx2.path()) - 1)
        print('Path:', node_p_mx2.path())
    print('Solution:', node_p_mx2.solution())

    # Puzzle 3
    print("\n")
    print("EightPuzzle 3 - A* Search using max of Manhattan tile & Misplaced tile heuristics")
    display(puzzle_s3)
    start_time_p_mx3 = time.time()
    node_p_mx3 = astar_search(puzzle3, h=max_h, display=DISPLAYSTATS)
    elapsed_time_p_mx3 = time.time() - start_time_p_mx3
    max_h_8Puzzle_average_time += elapsed_time_p_mx3
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mx3)
        print("Path length: ", len(node_p_mx3.path()) - 1)
        print('Path:', node_p_mx3.path())
    print('Solution:', node_p_mx3.solution())

    # Puzzle 4
    print("\n")
    print("EightPuzzle 4 - A* Search using max of Manhattan tile & Misplaced tile heuristics")
    display(puzzle_s1)
    start_time_p_mx4 = time.time()
    node_p_mx4 = astar_search(puzzle4, h=max_h, display=DISPLAYSTATS)
    elapsed_time_p_mx4 = time.time() - start_time_p_mx4
    max_h_8Puzzle_average_time += elapsed_time_p_mx4
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mx4)
        print("Path length: ", len(node_p_mx4.path()) - 1)
        print('Path:', node_p_mx4.path())
    print('Solution:', node_p_mx4.solution())

    # Puzzle 5
    print("\n")
    print("EightPuzzle 5 - A* Search using max of Manhattan tile & Misplaced tile heuristics")
    display(puzzle_s5)
    start_time_p_mx5 = time.time()
    node_p_mx5 = astar_search(puzzle5, h=max_h, display=DISPLAYSTATS)
    elapsed_time_p_mx5 = time.time() - start_time_p_mx5
    max_h_8Puzzle_average_time += elapsed_time_p_mx5
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mx5)
        print("Path length: ", len(node_p_mx5.path()) - 1)
        print('Path:', node_p_mx5.path())
    print('Solution:', node_p_mx5.solution())

    # Puzzle 6
    print("\n")
    print("EightPuzzle 6 - A* Search using max of Manhattan tile & Misplaced tile heuristics")
    display(puzzle_s6)
    start_time_p_mx6 = time.time()
    node_p_mx6 = astar_search(puzzle6, h=max_h, display=DISPLAYSTATS)
    elapsed_time_p_mx6 = time.time() - start_time_p_mx6
    max_h_8Puzzle_average_time += elapsed_time_p_mx6
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mx6)
        print("Path length: ", len(node_p_mx6.path()) - 1)
        print('Path:', node_p_mx6.path())
    print('Solution:', node_p_mx6.solution())

    # Puzzle 7
    print("\n")
    print("EightPuzzle 7 - A* Search using max of Manhattan tile & Misplaced tile heuristics")
    display(puzzle_s7)
    start_time_p_mx7 = time.time()
    node_p_mx7 = astar_search(puzzle7, h=max_h, display=DISPLAYSTATS)
    elapsed_time_p_mx7 = time.time() - start_time_p_mx7
    max_h_8Puzzle_average_time += elapsed_time_p_mx7
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mx7)
        print("Path length: ", len(node_p_mx7.path()) - 1)
        print('Path:', node_p_mx7.path())
    print('Solution:', node_p_mx7.solution())

    # Puzzle 8
    print("\n")
    print("EightPuzzle 8 - A* Search using max of Manhattan tile & Misplaced tile heuristics")
    display(puzzle_s8)
    start_time_p_mx8 = time.time()
    node_p_mx8 = astar_search(puzzle8, h=max_h, display=DISPLAYSTATS)
    elapsed_time_p_mx8 = time.time() - start_time_p_mx8
    max_h_8Puzzle_average_time += elapsed_time_p_mx8
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mx8)
        print("Path length: ", len(node_p_mx8.path()) - 1)
        print('Path:', node_p_mx8.path())
    print('Solution:', node_p_mx8.solution())

    # Puzzle 9
    print("\n")
    print("EightPuzzle 9 - A* Search using max of Manhattan tile & Misplaced tile heuristics")
    display(puzzle_s9)
    start_time_p_mx9 = time.time()
    node_p_mx9 = astar_search(puzzle9, h=max_h, display=DISPLAYSTATS)
    elapsed_time_p_mx9 = time.time() - start_time_p_mx9
    max_h_8Puzzle_average_time += elapsed_time_p_mx9
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mx9)
        print("Path length: ", len(node_p_mx9.path()) - 1)
        print('Path:', node_p_mx9.path())
    print('Solution:', node_p_mx9.solution())

    # Puzzle 10
    print("\n")
    print("EightPuzzle 10 - A* Search using max of Manhattan tile & Misplaced tile heuristics")
    display(puzzle_s10)
    start_time_p_mx10 = time.time()
    node_p_mx10 = astar_search(puzzle10, h=max_h, display=DISPLAYSTATS)
    elapsed_time_p_mx10 = time.time() - start_time_p_mx10
    max_h_8Puzzle_average_time += elapsed_time_p_mx10
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_p_mx10)
        print("Path length: ", len(node_p_mx10.path()) - 1)
        print('Path:', node_p_mx10.path())
    print('Solution:', node_p_mx10.solution())


"""
Generate 10 DuckPuzzles
# variables in the style: duck# are DuckPuzzle Objects
# variables in the style: duck_s# are tuples containing the initial DuckPuzzle state
"""

duck1, duck_s1 = make_rand_duckpuzzle()
if ALLTESTS:
    duck2, duck_s2 = make_rand_duckpuzzle()
    duck3, duck_s3 = make_rand_duckpuzzle()
    duck4, duck_s4 = make_rand_duckpuzzle()
    duck5, duck_s5 = make_rand_duckpuzzle()
    duck6, duck_s6 = make_rand_duckpuzzle()
    duck7, duck_s7 = make_rand_duckpuzzle()
    duck8, duck_s8 = make_rand_duckpuzzle()
    duck9, duck_s9 = make_rand_duckpuzzle()
    duck10, duck_s10 = make_rand_duckpuzzle()

misplaced_DuckPuzzle_average_time = 0
manhattan_DuckPuzzle_average_time = 0
max_h_DuckPuzzle_average_time = 0


"""
Test solving DuckPuzzles using an A* Search utilizing the misplaced tile heuristic
The puzzles initial state is printed using duck_display(state)
The time taken is timed using standard time functions
Number of nodes removed from frontier is given by "# paths have been expanded"
"""

# Puzzle 1
print("\n")
print("DuckPuzzle 1 - A* Search using Misplaced Tile Heuristic")
duck_display(duck_s1)
start_time_d_mt1 = time.time()
node_d_mt1 = astar_search(duck1, h=duck_misplaced_tile, display=DISPLAYSTATS)
elapsed_time_b_mt1 = time.time() - start_time_d_mt1
misplaced_DuckPuzzle_average_time += elapsed_time_b_mt1
if DISPLAYSTATS:
    print("Run time: ", elapsed_time_b_mt1)
    print("Path length: ", len(node_d_mt1.path()) - 1)
    print('Path:', node_d_mt1.path())
print('Solution:', node_d_mt1.solution())

if ALLTESTS:
    # Puzzle 2
    print("\n")
    print("DuckPuzzle 2 - A* Search using Misplaced Tile Heuristic")
    duck_display(duck_s2)
    start_time_d_mt2 = time.time()
    node_d_mt2 = astar_search(duck2, h=duck_misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_d_mt2 = time.time() - start_time_d_mt2
    misplaced_DuckPuzzle_average_time += elapsed_time_d_mt2
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mt2)
        print("Path length: ", len(node_d_mt2.path()) - 1)
        print('Path:', node_d_mt2.path())
    print('Solution:', node_d_mt2.solution())

    # Puzzle 3
    print("\n")
    print("DuckPuzzle 3 - A* Search using Misplaced Tile Heuristic")
    duck_display(duck_s3)
    start_time_d_mt3 = time.time()
    node_d_mt3 = astar_search(duck3, h=duck_misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_d_mt3 = time.time() - start_time_d_mt3
    misplaced_DuckPuzzle_average_time += elapsed_time_d_mt3
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mt3)
        print("Path length: ", len(node_d_mt3.path()) - 1)
        print('Path:', node_d_mt3.path())
    print('Solution:', node_d_mt3.solution())

    # Puzzle 4
    print("\n")
    print("DuckPuzzle 4 - A* Search using Misplaced Tile Heuristic")
    duck_display(duck_s1)
    start_time_d_mt4 = time.time()
    node_d_mt4 = astar_search(duck4, h=duck_misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_d_mt4 = time.time() - start_time_d_mt4
    misplaced_DuckPuzzle_average_time += elapsed_time_d_mt4
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mt4)
        print("Path length: ", len(node_d_mt4.path()) - 1)
        print('Path:', node_d_mt4.path())
    print('Solution:', node_d_mt4.solution())

    # Puzzle 5
    print("\n")
    print("DuckPuzzle 5 - A* Search using Misplaced Tile Heuristic")
    duck_display(duck_s5)
    start_time_d_mt5 = time.time()
    node_d_mt5 = astar_search(duck5, h=duck_misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_d_mt5 = time.time() - start_time_d_mt5
    misplaced_DuckPuzzle_average_time += elapsed_time_d_mt5
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mt5)
        print("Path length: ", len(node_d_mt5.path()) - 1)
        print('Path:', node_d_mt5.path())
    print('Solution:', node_d_mt5.solution())

    # Puzzle 6
    print("\n")
    print("DuckPuzzle 6 - A* Search using Misplaced Tile Heuristic")
    duck_display(duck_s6)
    start_time_d_mt6 = time.time()
    node_d_mt6 = astar_search(duck6, h=duck_misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_d_mt6 = time.time() - start_time_d_mt6
    misplaced_DuckPuzzle_average_time += elapsed_time_d_mt6
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mt6)
        print("Path length: ", len(node_d_mt6.path()) - 1)
        print('Path:', node_d_mt6.path())
    print('Solution:', node_d_mt6.solution())

    # Puzzle 7
    print("\n")
    print("DuckPuzzle 7 - A* Search using Misplaced Tile Heuristic")
    duck_display(duck_s7)
    start_time_d_mt7 = time.time()
    node_d_mt7 = astar_search(duck7, h=duck_misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_d_mt7 = time.time() - start_time_d_mt7
    misplaced_DuckPuzzle_average_time += elapsed_time_d_mt7
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mt7)
        print("Path length: ", len(node_d_mt7.path()) - 1)
        print('Path:', node_d_mt7.path())
    print('Solution:', node_d_mt7.solution())

    # Puzzle 8
    print("\n")
    print("DuckPuzzle 8 - A* Search using Misplaced Tile Heuristic")
    duck_display(duck_s8)
    start_time_d_mt8 = time.time()
    node_d_mt8 = astar_search(duck8, h=duck_misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_d_mt8 = time.time() - start_time_d_mt8
    misplaced_DuckPuzzle_average_time += elapsed_time_d_mt8
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mt8)
        print("Path length: ", len(node_d_mt8.path()) - 1)
        print('Path:', node_d_mt8.path())
    print('Solution:', node_d_mt8.solution())

    # Puzzle 9
    print("\n")
    print("DuckPuzzle 9 - A* Search using Misplaced Tile Heuristic")
    duck_display(duck_s9)
    start_time_d_mt9 = time.time()
    node_d_mt9 = astar_search(duck9, h=duck_misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_d_mt9 = time.time() - start_time_d_mt9
    misplaced_DuckPuzzle_average_time += elapsed_time_d_mt9
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mt9)
        print("Path length: ", len(node_d_mt9.path()) - 1)
        print('Path:', node_d_mt9.path())
    print('Solution:', node_d_mt9.solution())

    # Puzzle 10
    print("\n")
    print("DuckPuzzle 10 - A* Search using Misplaced Tile Heuristic")
    duck_display(duck_s10)
    start_time_d_mt10 = time.time()
    node_d_mt10 = astar_search(duck10, h=duck_misplaced_tile, display=DISPLAYSTATS)
    elapsed_time_d_mt10 = time.time() - start_time_d_mt10
    misplaced_DuckPuzzle_average_time += elapsed_time_d_mt10
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mt10)
        print("Path length: ", len(node_d_mt10.path()) - 1)
        print('Path:', node_d_mt10.path())
    print('Solution:', node_d_mt10.solution())


"""
Test solving DuckPuzzles using an A* Search utilizing the Manhattan tile heuristic
The ducks initial state is printed using display(state)
The time taken is timed using standard time functions
Number of nodes removed from frontier is given by "# paths have been expanded"
"""


# Puzzle 1
print("\n")
print("DuckPuzzle 1 - A* Search using Manhattan Tile Heuristic")
duck_display(duck_s1)
start_time_d_mh1 = time.time()
node_d_mh1 = astar_search(duck1, h=duck_manhattan, display=DISPLAYSTATS)
elapsed_time_d_mh1 = time.time() - start_time_d_mh1
manhattan_DuckPuzzle_average_time += elapsed_time_d_mh1
if DISPLAYSTATS:
    print("Run time: ", elapsed_time_d_mh1)
    print("Path length: ", len(node_d_mh1.path()) - 1)
    print('Path:', node_d_mh1.path())
print('Solution:', node_d_mh1.solution())

if ALLTESTS:
    # Puzzle 2
    print("\n")
    print("DuckPuzzle 2 - A* Search using Manhattan Tile Heuristic")
    duck_display(duck_s2)
    start_time_d_mh2 = time.time()
    node_d_mh2 = astar_search(duck2, h=duck_manhattan, display=DISPLAYSTATS)
    elapsed_time_d_mh2 = time.time() - start_time_d_mh2
    manhattan_DuckPuzzle_average_time += elapsed_time_d_mh2
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mh2)
        print("Path length: ", len(node_d_mh2.path()) - 1)
        print('Path:', node_d_mh2.path())
    print('Solution:', node_d_mh2.solution())

    # Puzzle 3
    print("\n")
    print("DuckPuzzle 3 - A* Search using Manhattan Tile Heuristic")
    duck_display(duck_s3)
    start_time_d_mh3 = time.time()
    node_d_mh3 = astar_search(duck3, h=duck_manhattan, display=DISPLAYSTATS)
    elapsed_time_d_mh3 = time.time() - start_time_d_mh3
    manhattan_DuckPuzzle_average_time += elapsed_time_d_mh3
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mh3)
        print("Path length: ", len(node_d_mh3.path()) - 1)
        print('Path:', node_d_mh3.path())
    print('Solution:', node_d_mh3.solution())

    # Puzzle 4
    print("\n")
    print("DuckPuzzle 4 - A* Search using Manhattan Tile Heuristic")
    duck_display(duck_s1)
    start_time_d_mh4 = time.time()
    node_d_mh4 = astar_search(duck4, h=duck_manhattan, display=DISPLAYSTATS)
    elapsed_time_d_mh4 = time.time() - start_time_d_mh4
    manhattan_DuckPuzzle_average_time += elapsed_time_d_mh4
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mh4)
        print("Path length: ", len(node_d_mh4.path()) - 1)
        print('Path:', node_d_mh4.path())
    print('Solution:', node_d_mh4.solution())

    # Puzzle 5
    print("\n")
    print("DuckPuzzle 5 - A* Search using Manhattan Tile Heuristic")
    duck_display(duck_s5)
    start_time_d_mh5 = time.time()
    node_d_mh5 = astar_search(duck5, h=duck_manhattan, display=DISPLAYSTATS)
    elapsed_time_d_mh5 = time.time() - start_time_d_mh5
    manhattan_DuckPuzzle_average_time += elapsed_time_d_mh5
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mh5)
        print("Path length: ", len(node_d_mh5.path()) - 1)
        print('Path:', node_d_mh5.path())
    print('Solution:', node_d_mh5.solution())

    # Puzzle 6
    print("\n")
    print("DuckPuzzle 6 - A* Search using Manhattan Tile Heuristic")
    duck_display(duck_s6)
    start_time_d_mh6 = time.time()
    node_d_mh6 = astar_search(duck6, h=duck_manhattan, display=DISPLAYSTATS)
    elapsed_time_d_mh6 = time.time() - start_time_d_mh6
    manhattan_DuckPuzzle_average_time += elapsed_time_d_mh6
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mh6)
        print("Path length: ", len(node_d_mh6.path()) - 1)
        print('Path:', node_d_mh6.path())
    print('Solution:', node_d_mh6.solution())

    # Puzzle 7
    print("\n")
    print("DuckPuzzle 7 - A* Search using Manhattan Tile Heuristic")
    duck_display(duck_s7)
    start_time_d_mh7 = time.time()
    node_d_mh7 = astar_search(duck7, h=duck_manhattan, display=DISPLAYSTATS)
    elapsed_time_d_mh7 = time.time() - start_time_d_mh7
    manhattan_DuckPuzzle_average_time += elapsed_time_d_mh7
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mh7)
        print("Path length: ", len(node_d_mh7.path()) - 1)
        print('Path:', node_d_mh7.path())
    print('Solution:', node_d_mh7.solution())

    # Puzzle 8
    print("\n")
    print("DuckPuzzle 8 - A* Search using Manhattan Tile Heuristic")
    duck_display(duck_s8)
    start_time_d_mh8 = time.time()
    node_d_mh8 = astar_search(duck8, h=duck_manhattan, display=DISPLAYSTATS)
    elapsed_time_d_mh8 = time.time() - start_time_d_mh8
    manhattan_DuckPuzzle_average_time += elapsed_time_d_mh8
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mh8)
        print("Path length: ", len(node_d_mh8.path()) - 1)
        print('Path:', node_d_mh8.path())
    print('Solution:', node_d_mh8.solution())

    # Puzzle 9
    print("\n")
    print("DuckPuzzle 9 - A* Search using Manhattan Tile Heuristic")
    duck_display(duck_s9)
    start_time_d_mh9 = time.time()
    node_d_mh9 = astar_search(duck9, h=duck_manhattan, display=DISPLAYSTATS)
    elapsed_time_d_mh9 = time.time() - start_time_d_mh9
    manhattan_DuckPuzzle_average_time += elapsed_time_d_mh9
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mh9)
        print("Path length: ", len(node_d_mh9.path()) - 1)
        print('Path:', node_d_mh9.path())
    print('Solution:', node_d_mh9.solution())

    # Puzzle 10
    print("\n")
    print("DuckPuzzle 10 - A* Search using Manhattan Tile Heuristic")
    duck_display(duck_s10)
    start_time_d_mh10 = time.time()
    node_d_mh10 = astar_search(duck10, h=duck_manhattan, display=DISPLAYSTATS)
    elapsed_time_d_mh10 = time.time() - start_time_d_mh10
    manhattan_DuckPuzzle_average_time += elapsed_time_d_mh10
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mh10)
        print("Path length: ", len(node_d_mh10.path()) - 1)
        print('Path:', node_d_mh10.path())
    print('Solution:', node_d_mh10.solution())


"""
Test solving DuckPuzzles using an A* Search utilizing the max of the Manhattan Tile & Misplaced-Tile heuristics
The ducks initial state is printed using display(state)
The time taken is timed using standard time functions
Number of nodes removed from frontier is given by "# paths have been expanded"
"""

# Puzzle 1
print("\n")
print("DuckPuzzle 1 - A* Search using max of Manhattan tile & Misplaced tile Heuristics")
duck_display(duck_s1)
start_time_d_mx1 = time.time()
node_d_mx1 = astar_search(duck1, h=duck_max_h, display=DISPLAYSTATS)
elapsed_time_d_mx1 = time.time() - start_time_d_mx1
max_h_DuckPuzzle_average_time += elapsed_time_d_mx1
if DISPLAYSTATS:
    print("Run time: ", elapsed_time_d_mx1)
    print("Path length: ", len(node_d_mx1.path()) - 1)
    print('Path:', node_d_mx1.path())
print('Solution:', node_d_mx1.solution())

if ALLTESTS:
    # Puzzle 2
    print("\n")
    print("DuckPuzzle 2 - A* Search using max of Manhattan tile & Misplaced tile Heuristics")
    duck_display(duck_s2)
    start_time_d_mx2 = time.time()
    node_d_mx2 = astar_search(duck2, h=duck_max_h, display=DISPLAYSTATS)
    elapsed_time_d_mx2 = time.time() - start_time_d_mx2
    max_h_DuckPuzzle_average_time += elapsed_time_d_mx2
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mx2)
        print("Path length: ", len(node_d_mx2.path()) - 1)
        print('Path:', node_d_mx2.path())
    print('Solution:', node_d_mx2.solution())

    # Puzzle 3
    print("\n")
    print("DuckPuzzle 3 - A* Search using max of Manhattan tile & Misplaced tile Heuristics")
    duck_display(duck_s3)
    start_time_d_mx3 = time.time()
    node_d_mx3 = astar_search(duck3, h=duck_max_h, display=DISPLAYSTATS)
    elapsed_time_d_mx3 = time.time() - start_time_d_mx3
    max_h_DuckPuzzle_average_time += elapsed_time_d_mx3
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mx3)
        print("Path length: ", len(node_d_mx3.path()) - 1)
        print('Path:', node_d_mx3.path())
    print('Solution:', node_d_mx3.solution())

    # Puzzle 4
    print("\n")
    print("DuckPuzzle 4 - A* Search using max of Manhattan tile & Misplaced tile Heuristics")
    duck_display(duck_s1)
    start_time_d_mx4 = time.time()
    node_d_mx4 = astar_search(duck4, h=duck_max_h, display=DISPLAYSTATS)
    elapsed_time_d_mx4 = time.time() - start_time_d_mx4
    max_h_DuckPuzzle_average_time += elapsed_time_d_mx4
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mx4)
        print("Path length: ", len(node_d_mx4.path()) - 1)
        print('Path:', node_d_mx4.path())
    print('Solution:', node_d_mx4.solution())

    # Puzzle 5
    print("\n")
    print("DuckPuzzle 5 - A* Search using max of Manhattan tile & Misplaced tile Heuristics")
    duck_display(duck_s5)
    start_time_d_mx5 = time.time()
    node_d_mx5 = astar_search(duck5, h=duck_max_h, display=DISPLAYSTATS)
    elapsed_time_d_mx5 = time.time() - start_time_d_mx5
    max_h_DuckPuzzle_average_time += elapsed_time_d_mx5
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mx5)
        print("Path length: ", len(node_d_mx5.path()) - 1)
        print('Path:', node_d_mx5.path())
    print('Solution:', node_d_mx5.solution())

    # Puzzle 6
    print("\n")
    print("DuckPuzzle 6 - A* Search using max of Manhattan tile & Misplaced tile Heuristics")
    duck_display(duck_s6)
    start_time_d_mx6 = time.time()
    node_d_mx6 = astar_search(duck6, h=duck_max_h, display=DISPLAYSTATS)
    elapsed_time_d_mx6 = time.time() - start_time_d_mx6
    max_h_DuckPuzzle_average_time += elapsed_time_d_mx6
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mx6)
        print("Path length: ", len(node_d_mx6.path()) - 1)
        print('Path:', node_d_mx6.path())
    print('Solution:', node_d_mx6.solution())

    # Puzzle 7
    print("\n")
    print("DuckPuzzle 7 - A* Search using max of Manhattan tile & Misplaced tile Heuristics")
    duck_display(duck_s7)
    start_time_d_mx7 = time.time()
    node_d_mx7 = astar_search(duck7, h=duck_max_h, display=DISPLAYSTATS)
    elapsed_time_d_mx7 = time.time() - start_time_d_mx7
    max_h_DuckPuzzle_average_time += elapsed_time_d_mx7
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mx7)
        print("Path length: ", len(node_d_mx7.path()) - 1)
        print('Path:', node_d_mx7.path())
    print('Solution:', node_d_mx7.solution())

    # Puzzle 8
    print("\n")
    print("DuckPuzzle 8 - A* Search using max of Manhattan tile & Misplaced tile Heuristics")
    duck_display(duck_s8)
    start_time_d_mx8 = time.time()
    node_d_mx8 = astar_search(duck8, h=duck_max_h, display=DISPLAYSTATS)
    elapsed_time_d_mx8 = time.time() - start_time_d_mx8
    max_h_DuckPuzzle_average_time += elapsed_time_d_mx8
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mx8)
        print("Path length: ", len(node_d_mx8.path()) - 1)
        print('Path:', node_d_mx8.path())
    print('Solution:', node_d_mx8.solution())

    # Puzzle 9
    print("\n")
    print("DuckPuzzle 9 - A* Search using max of Manhattan tile & Misplaced tile Heuristics")
    duck_display(duck_s9)
    start_time_d_mx9 = time.time()
    node_d_mx9 = astar_search(duck9, h=duck_max_h, display=DISPLAYSTATS)
    elapsed_time_d_mx9 = time.time() - start_time_d_mx9
    max_h_DuckPuzzle_average_time += elapsed_time_d_mx9
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mx9)
        print("Path length: ", len(node_d_mx9.path()) - 1)
        print('Path:', node_d_mx9.path())
    print('Solution:', node_d_mx9.solution())

    # Puzzle 10
    print("\n")
    print("DuckPuzzle 10 - A* Search using max of Manhattan tile & Misplaced tile Heuristics")
    duck_display(duck_s10)
    start_time_d_mx10 = time.time()
    node_d_mx10 = astar_search(duck10, h=duck_max_h, display=DISPLAYSTATS)
    elapsed_time_d_mx10 = time.time() - start_time_d_mx10
    max_h_DuckPuzzle_average_time += elapsed_time_d_mx10
    if DISPLAYSTATS:
        print("Run time: ", elapsed_time_d_mx10)
        print("Path length: ", len(node_d_mx10.path()) - 1)
        print('Path:', node_d_mx10.path())
    print('Solution:', node_d_mx10.solution())

if ALLTESTS:
    misplaced_8Puzzle_average_time = misplaced_8Puzzle_average_time / 10
    manhattan_8Puzzle_average_time = manhattan_8Puzzle_average_time / 10
    max_h_8Puzzle_average_time = max_h_8Puzzle_average_time / 10
    misplaced_DuckPuzzle_average_time = misplaced_DuckPuzzle_average_time / 10
    manhattan_DuckPuzzle_average_time = manhattan_DuckPuzzle_average_time / 10
    max_h_DuckPuzzle_average_time = max_h_DuckPuzzle_average_time / 10


# noinspection PyTypeChecker
print("Average time for 8Puzzle with Misplaced Tile Heuristic: ", end="", flush="True")
print("{:.2f}".format(1000*misplaced_8Puzzle_average_time), "ms")
# noinspection PyTypeChecker
print("Average time for 8Puzzle with Manhattan Tile Heuristic: ", end="", flush="True")
print("{:.2f}".format(1000*manhattan_8Puzzle_average_time), "ms")
# noinspection PyTypeChecker
print("Average time for 8Puzzle with Max Tile Heuristic: ", end="", flush="True")
print("{:.2f}".format(1000*max_h_8Puzzle_average_time), "ms")
# noinspection PyTypeChecker
print("Average time for DuckPuzzle with Misplaced Tile Heuristic: ", end="", flush="True")
print("{:.2f}".format(1000*misplaced_DuckPuzzle_average_time), "ms")
# noinspection PyTypeChecker
print("Average time for DuckPuzzle with Manhattan Tile Heuristic: ", end="", flush="True")
print( "{:.2f}".format(1000*manhattan_DuckPuzzle_average_time), "ms")
# noinspection PyTypeChecker
print("Average time for DuckPuzzle with Max Tile Heuristic: ", end="", flush="True")
print("{:.2f}".format(1000*max_h_DuckPuzzle_average_time), "ms")