# CMPT310 Assignment 1
# Peter Lan
# 301331631

import time
import random
from search import *

#-------------------------------------- Question 1: Helper Functions --------------------------------------

# Returns a shuffled version of the given tuple
def shuffle_tuple(t):
    l = list(t)
    random.shuffle(l)
    t = tuple(l)
    return t

# Returns a new instance of an EightPuzzle problem with a random initial state that is solvable
def make_rand_8puzzle():
    t = (1,2,3,4,5,6,7,8,0)
    initial = shuffle_tuple(t)
    puzzle = EightPuzzle(initial)
    while (puzzle.check_solvability(puzzle.initial) == False):
        puzzle.initial = shuffle_tuple(initial)
    return puzzle

# Takes an 8-puzzle state as input and prints a neat and readable representation of it
def display(state):
    i = 0
    while (i < len(state)):
        c = state[i] 
        if (c == 0):
            c = "*"
        if ((i+1)%3 == 0):
            print(c)
        else:
            print(c, end = " ")
        i += 1


#-------------------------------------- Question 2: Comparing Algorithms --------------------------------------

# Returns the misplaced tile heuristic value(excluding 0) for a given Eight-puzzle or House-puzzle state
# Modified version of h() from search.py
def misplaced_tile_heuristic(state, goal):
    return sum((g != 0 and s != g) for (s, g) in zip(state, goal))

# Returns the Manhattan distance heuristic value(excluding 0) for a given Eight-puzzle or House-puzzle state
# puzzle_type: "eight-puzzle" => Eight-puzzle
#              "house-puzzle" => House-puzzle
def manhattan_distance_heuristic(state, puzzle_type):
    assert(len(state) == 9)
    puzzle_type = puzzle_type.lower()
    assert(puzzle_type == "eight-puzzle" or puzzle_type == "house-puzzle" )

    # Look up table for pre-calculated distance
    if (puzzle_type == "eight-puzzle"):
        distance = ((0,1,2,1,2,3,2,3,4),
                    (1,0,1,2,1,2,3,2,3),
                    (2,1,0,3,2,1,4,3,2),
                    (1,2,3,0,1,2,1,2,3),
                    (2,1,2,1,0,1,2,1,2),
                    (3,2,1,2,1,0,3,2,1),
                    (2,3,4,1,2,3,0,1,2),
                    (3,2,3,2,1,2,1,0,1))
    else:
        distance = ((0,1,1,2,3,4,3,4,5),
                    (1,0,2,1,2,3,2,3,4),
                    (1,2,0,1,2,3,2,3,4),
                    (2,1,1,0,1,2,1,2,3),
                    (3,2,2,1,0,1,2,1,2),
                    (4,3,3,2,1,0,3,2,1),
                    (3,2,2,1,2,3,0,1,2),
                    (4,3,3,2,1,2,1,0,1))
    res = 0 
    pos = 0           
    for num in state:
        if (num != 0):
            res += distance[num-1][pos]
        pos += 1
    return res

# Returns the heuristic value for a given state according to the heuristic method
# heuristic_method: 1 =>  misplaced tile heuristic
#                   2 =>  Manhattan distance heuristic
#                   3 =>  max of misplaced tile heuristic and Manhattan distance heuristic
# The returned heuristic value does not include tile 0
def calculate_heuristic(state, goal, puzzle_type, heuristic_method):
    assert(heuristic_method >= 1 and heuristic_method <= 3)
    if (heuristic_method == 1):
        return misplaced_tile_heuristic(state, goal)
    elif (heuristic_method == 2):
        return manhattan_distance_heuristic(state, puzzle_type)
    else:
        return max(misplaced_tile_heuristic(state, goal),manhattan_distance_heuristic(state, puzzle_type))

# Returns true if item exists in the list or tuple, false otherwise
def exist(item, list1, tuple1):
    if (item in list1):
        return True
    if (any(item in element for element in tuple1)) :
        return True
    return False

# Solve the given Eight-puzzle or House-puzzle by A*-search using specified heuristic method
# Output the solution, total running time, number of tiles moved, and number of nodes removed from frontier upon completion
# Puzzle is assumed to be solvable
# puzzle_type: "eight-puzzle" => Eight-puzzle
#              "house-puzzle" => House-puzzle
# heuristic_method: 1 =>  misplaced tile heuristic
#                   2 =>  Manhattan distance heuristic
#                   3 =>  max of misplaced tile heuristic and Manhattan distance heuristic
def a_star_search(puzzle, puzzle_type, heuristic_method):
    start_time = time.time()
    frontier = []
    explored = []
    tiles_moved = 0
    nodes_removed = 0
    goal = puzzle.goal

    f = 0
    g = 0
    state = puzzle.initial
    taken_actions = []
    # push initial state into the priority queue with the following format
    # ( f(n), g(n), state, taken_actions)
    heapq.heappush(frontier, (f,g,state,taken_actions))

    while (len(frontier) > 0):
        node = heapq.heappop(frontier)
        nodes_removed += 1
        tiles_moved = node[1]
        state = node[2]
        taken_actions = node[3]

        if (state == goal):
            elapsed_time = time.time() - start_time
            print("Solution:", taken_actions)
            print("Total running time in seconds:", elapsed_time)
            print("Number of tiles moved:", tiles_moved)
            print("Total number of nodes removed from frontier:", nodes_removed)
            return

        explored.append(state)
        available_actions = puzzle.actions(state)

        for action in available_actions:
            new_state = puzzle.result(state, action)

            if (not exist(new_state, explored, frontier)):
                g = tiles_moved + 1
                h = calculate_heuristic(new_state, goal, puzzle_type, heuristic_method)
                f = g + h
                new_taken_actions = taken_actions + list(action[0])
                heapq.heappush(frontier, (f, g, new_state, new_taken_actions))
    print("Failed to find a solution for the given puzzle")

# Create random 8-puzzle instances and solve each of them using the algorithms listed in the requirements
num_of_trials = 10
for i in range(num_of_trials):
    puzzle = make_rand_8puzzle()
    print("=============================================================================================")
    print("Trial", i+1)
    print("---------------------------------------------------------------------------------------------")
    print("Initial state of the 8-puzzle")
    display(puzzle.initial)
    print("---------------------------------------------------------------------------------------------")
    print("A*-search using the misplaced tile heuristic")
    a_star_search(puzzle, "eight-puzzle", 1)
    print("---------------------------------------------------------------------------------------------")
    print("A*-search using the Manhattan distance heuristic")
    a_star_search(puzzle, "eight-puzzle", 2)
    print("---------------------------------------------------------------------------------------------")
    print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic")
    a_star_search(puzzle, "eight-puzzle", 3)
    print("=============================================================================================")


#-------------------------------------- Question 3: The House-Puzzle --------------------------------------

# Returns a new instance of a Duck-puzzle problem with a random initial state that is solvable
def make_rand_duck_puzzle():
    initial = (1,2,3,4,5,6,7,8,0)
    puzzle = DuckPuzzle(initial)
    num_of_moves = random.randint(100,1000)
    for i in range(num_of_moves):
        state = puzzle.initial
        actions = puzzle.actions(state)
        x = random.randint(0,len(actions)-1)
        action = actions[x]
        puzzle.initial = puzzle.result(state, action)
    return puzzle

# Takes a Duck-puzzle state as input and prints a neat and readable representation of it
def display_duck_puzzle(state):
    for i in range(len(state)):
        c = state[i] 
        if (c == 0):
            c = "*"
        if (i == 1 or i == 8):
            print(c)
        elif (i == 5):
            print(c, end="\n ")
        else:
            print(c, end="")

class DuckPuzzle(Problem):
    # Defines goal state and initializes a problem
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    # Returns the index of the blank square in a given state
    def find_blank_square(self, state):
        return state.index(0)
    
    # Returns the possible actions for the given state of a Duck-puzzle problem
    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
        if (index_blank_square == 0):
            possible_actions.remove('UP')
            possible_actions.remove('LEFT')
        elif (index_blank_square == 1 or index_blank_square == 5):
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        elif (index_blank_square == 2 or index_blank_square == 6):
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif (index_blank_square == 4):
            possible_actions.remove('UP')
        elif (index_blank_square == 7):
            possible_actions.remove('DOWN')
        elif (index_blank_square == 8):
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')
        return possible_actions

    # Given state and action, returns a new state that is the result of the action
    # Action is assumed to be a valid action in the state
    def result(self, state, action):
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if (blank == 0 or blank == 1):
            delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif (blank == 2 or blank == 3):
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else: 
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

# Create random Duck-puzzle instances and solve each of them using the algorithms listed in the requirements
for i in range(num_of_trials):
    puzzle = make_rand_duck_puzzle()
    print("=============================================================================================")
    print("Trial", i+1)
    print("---------------------------------------------------------------------------------------------")
    print("Initial state of the Duck-puzzle")
    display_duck_puzzle(puzzle.initial)
    print("---------------------------------------------------------------------------------------------")
    print("A*-search using the misplaced tile heuristic")
    a_star_search(puzzle, "house-puzzle", 1)
    print("---------------------------------------------------------------------------------------------")
    print("A*-search using the Manhattan distance heuristic")
    a_star_search(puzzle, "house-puzzle", 2)
    print("---------------------------------------------------------------------------------------------")
    print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic")
    a_star_search(puzzle, "house-puzzle", 3)
    print("---------------------------------------------------------------------------------------------")