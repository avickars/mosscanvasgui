# Evan Lam 301292135
# CMPT 310 Assignment 1 Summer 2020
# Used tutorials from Mohammadmahdi Jahanara as a reference to use numpy random permutation function
# Used tutorials from Mohammadmahdi Jahanara as a reference to check solvability via dummy puzzle states
# Used tutorial to figure out that len is how to find out length
# Used help from tutorial to figure out the A star algorithm implementation for Misplaced and Manhattan
# Did not finish Q3, the frontier question, or the maximum A-star heuristic

# ---
# Question 1. Generation of helper functions for random states and display of states

import numpy as np
import time
from search import * # Import all search.py
state = (0,1,2,3,4,5,6,7,8) # Initial state, for testing
# This make_rand_8puzzle function generates a solvable state and uses check_solvability from aima-python
def make_rand_8puzzle():
    while True:
        state = tuple(np.random.permutation(9))
        
        dummy_puzzle = EightPuzzle(initial=state)
        solvability = dummy_puzzle.check_solvability(state)
        if solvability:
            break
        print(state, "This is not solvable. Trying another state.")

    print(state, "This is a solvable state.")
    return state # Return the solvable state
    
state = make_rand_8puzzle() # Test the make rand function

def display(state):
    stateLength = 0 # Iterating variable
    item1 = '0'
    item2 = '0'
    item3 = '0'
    while stateLength < 9: # This variable is 9 because the 8 puzzle has 9 elements, including the empty space 0
        if state[stateLength] == 0: # These loops are necessary to check for a 0 and replace it with * when printing
            item1 = "*"
            item2 = state[stateLength + 1]
            item3 = state[stateLength + 2]
        elif state[stateLength + 1] == 0:
            item1 = state[stateLength + 0]
            item2 = "*"
            item3 = state[stateLength + 2]
        elif state[stateLength + 2] == 0:
            item1 = state[stateLength + 0]
            item2 = state[stateLength + 1]
            item3 = "*"
        else: # If the code reaches this block, none of the values in the row are a 0
            item1 = state[stateLength + 0]
            item2 = state[stateLength + 1]
            item3 = state[stateLength + 2]
        print(item1, item2, item3) # Print out the 3 items that were just iterated through
        stateLength += 3 # As the program has just printed out 3 items, the next 3 are to be printed out


display(state) # Test the display function

# For question2, define the Manhattan Heuristic and call it recursively to find the total Manhattan distance
def manhattan(node):
    state = node.state

    manhattanDistance = 0 # Initialize to 0
    base_state = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]] # index list
    index_state, index_base_state = {}, {}
    goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}

    for i in range(len(state)):
        index_state[state[i]] = base_state[i]

    k = 8 #iteration variable, there are a required 9 - 1 = 8 iterations for Manhattan
    j = 2 #iteration variable 2 
    while (k < 8):
        while (j < 2):
            manhattanDistance = abs(manhattanDistance + goal[i][j] - index_state[i][j] )

    return manhattanDistance

# Maximum heuristic would go here if it were finished
# def maxHeuristic(node):
#     heuristic = manhattan(node)
#     h_test = EightPuzzle(initial)
#     heuristic2 = h_test.h(node)
#     return max(heuristic, heuristic2) # return the maximum of these 2 values

tile_time, man_time, tile_length, man_length= [], [], [], []
# max_time, max_length = [], [] # Did not implement

i = 0 # iteration variable
def question2():
    while (i < 10): #change to change the number of iterations
        rand8_puzzle = make_rand_8puzzle()
        display(rand8_puzzle) 

        # A star Misplaced
        time_mis_1 = time.time() #temp variable for time
        tile_h_astar = astar_search(rand8_puzzle, EightPuzzle.h)
        time_mis_2 = time.time() - time_mis_1 # Calculate the time with the temp variable
        tile_time.append(time_mis_2) # Add time to the running total
        tile_length.append(len(tile_h_astar)) # Add length to the running total
        print("Average Misplaced Tile Heuristic Time:", mean(tile_time))
        print("Misplaced Tile Heuristic Length:", tile_length)

        # A star Manhattan
        time_man_1 = time.time() # temp variable for time
        manhattan_h_astar = astar_search(rand8_puzzle, manhattan)
        time_man_2 = time.time() - time_man_1 # Calculate the time with the temp variable
        man_time.append(time_man_2) # Add time to the running total
        man_length.append(len(manhattan_h_astar)) # Add length to the running total
        print("Average Manhattan Distance Heuristic Time:", mean(man_time))
        print("Manhattan Heuristic Length:", man_length)

        # A star Maximum - Did not implement
        #time_max_1 = time.time()  # temp variable for time
        #max_h_astar = astar_search(rand8_puzzle, EightPuzzle.maximumHeuristic).solution()
        #time_max_2 = time.time() - time_max_1 
        #max_time.append(time_max_2)
        #max_length.append(len(max_h_astar))
        #print("Maximum Heuristic Time:", mean(max_time))
        #print("Max Length:", max_length)


question2()