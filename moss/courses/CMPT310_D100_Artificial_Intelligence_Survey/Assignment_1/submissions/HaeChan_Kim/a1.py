# a1.py

import sys
sys.path.insert(0, '/Users/haechankim/Desktop/cmpt310/aima-python')
from search import *
import numpy
import random
import time
import math
from utils import PriorityQueue, memoize

# ...

# Course: CMPT310 2020 summer
# Assignment: 1-Experimenting with the 8-puzzle
# Author: William (Haechan) Kim
# Student Number: 301169901
# email: hka64@sfu.ca

# CreatedDate: 2020-05-29
# TA: Mahmoud Khademi
# Professor: Toby John Donaldson



#Helper Functions
# -------------------------------------------------------------------------
# function to make random solvable  8 puzzle
def make_rand_8puzzle(state: list, iteration: int):

    for x in range(iteration):
        index_blank_square = search_blank(state, 0, 9)
        delta = random.randrange(-3, 4, 2) 
        #['UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1]

        if delta == -3 and index_blank_square > 2: #up
            swap_position(state, index_blank_square, index_blank_square-3)
        elif delta == 3 and index_blank_square < 6: #down
            swap_position(state, index_blank_square, index_blank_square+3)
        elif delta == -1 and index_blank_square % 3 != 0: #left
            swap_position(state, index_blank_square, index_blank_square-1)
        elif delta == 1 and index_blank_square % 3 != 2: #right
            swap_position(state, index_blank_square, index_blank_square+1)

    state_tuple = tuple(state)
    puzzle = EightPuzzle(state_tuple)

    if puzzle.check_solvability(state_tuple) == True:
        print("solvability is verified")

        return puzzle
    else:
        return -1
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# function to find position of blank *
def search_blank(state: list, index_blank_square: int, length: int)-> int:
    if length < 1:
        return -1
    if state[index_blank_square] == 0:
        return index_blank_square
    else:
        return search_blank(state, index_blank_square+1, length-1)
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# function to swap position
def swap_position(state: list, index_blank_square: int, index_target_square: int):
    tmp = state[index_blank_square]
    state[index_blank_square] = state[index_target_square]
    state[index_target_square] = tmp
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
# function to make random solvable house puzzle
def make_rand_HousePuzzle(state: list, iteration: int):

    for x in range(iteration):
        index_blank_square = search_blank(state, 0, 9)
        delta = random.randrange(-3, 4, 2) 
        #['UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1]

        # Move backword from goal state to make random values
        if delta == -3 and index_blank_square > 5 or index_blank_square == 2 or index_blank_square == 3: #UP
            swap_position(state, index_blank_square, index_blank_square-3)
        elif delta == 3 and index_blank_square < 6 and index_blank_square != 2: #DOWN
            swap_position(state, index_blank_square, index_blank_square+3)
        elif delta == -1 and index_blank_square % 3 > 0 and index_blank_square != 2: #LEFT
            swap_position(state, index_blank_square, index_blank_square-1)
        elif delta == 1 and index_blank_square % 4 != 1 and index_blank_square != 8: #RIGHT
            swap_position(state, index_blank_square, index_blank_square+1)

    state_tuple = tuple(state)
    puzzle = HousePuzzle(state_tuple)
    print("Solvability: verified") #solvability is verified by moving backword from goal state

    return puzzle

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# function to make House solvable puzzle
class HousePuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        self.goal = goal
        Problem.__init__(self, initial, goal)

    def find_blank_square(self, state):

        return state.index(0)

    def actions(self, state):

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = search_blank(state, 0, 9)

        if index_blank_square % 2 == 0 and index_blank_square != 4 and index_blank_square != 8:
            possible_actions.remove('LEFT')
        if index_blank_square < 6 and index_blank_square != 2 and index_blank_square != 3:
            possible_actions.remove('UP')
        if (index_blank_square % 3 == 2 and index_blank_square > 4) or index_blank_square == 1:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):

        return state == self.goal
# -------------------------------------------------------------------------
     

# -------------------------------------------------------------------------
# function to disaply current state of 3x3 puzzle
def display(state_tuple):
    state_tuple = list(state_tuple)
    index_blank_square = search_blank(state_tuple, 0, 9)
    state_tuple[index_blank_square] = '*'
    length = len(state_tuple) -1

    for i in range(3):
        for j in range(3):
            print(state_tuple[3*i+j], end="  ")
        print()
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# function to disaply current state of house puzzle
def display_House(state_tuple):
    state_tuple = list(state_tuple)
    index_blank_square = search_blank(state_tuple, 0, 9)
    state_tuple[index_blank_square] = '*'
    length = len(state_tuple) -1

    for i in range(3):
        if i == 0:
            for j in range(2):
                print(state_tuple[3*i+j], end="  ")
        elif i == 1:
            for j in range(4):
                print(state_tuple[2+j], end="  ")
        else:
            for j in range(3):
                if j == 0:
                    indent = 1
                else:
                    indent = 0
                print(('  ')*indent,state_tuple[3*i+j], end=" ")
        print()
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Modified A* search for running time,lenght, number of removed nodes
def astar_search(problem, h=None, display=False):
    start_time = time.time()
    results =[]
    h = memoize(h or problem.h, 'h')
    node, removed_node = best_first_graph_search(problem, lambda n: n.path_cost + h(n))
    end_time = time.time()
    print('Time elapsed: ', end_time - start_time, 's')
    print('Total Length: ',len(node.path())-1)
    print('Total removed nodes: ',removed_node)
    return node
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Modified BFGS  for running time,lenght, number of removed nodes
def best_first_graph_search(problem, f):
    removed_node = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        removed_node = removed_node + 1
        if problem.goal_test(node.state):
            return node, removed_node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    
    return removed_node
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Return maximum number of h value from misplaced fnc and manhtaan fnc
def max_misplaced_menhattan(node):
    score1 = manhattan(node) 
    score2 = h_modified(node) #misplaced fnc

    return max(score1, score2)
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
#manhattan function
def manhattan(node):
    init_state = node.state
    index_goal = {1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1], 0:[2,2]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    x, y = 0, 1
   
    #give coordinate to each init_state
    for i in range(len(init_state)):
        index_state[init_state[i]] = index[i]
    

    mhd = 0
    for i in range(len(init_state)-1): #get distance for each coordinate of index
        x_value = abs(index_state[i+1][x]-index_goal[i+1][x]) #skip index 0 to reduce unnecessary cost
        y_value =abs(index_state[i+1][y]-index_goal[i+1][y])
        mhd = x_value+y_value + mhd
    return mhd
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
#misplaced tile heuristic function
def h_modified(node):
    """ Return the heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles """
    return sum(s != g and s!= 0 for (s, g) in zip(node.state, goal_state))
# -------------------------------------------------------------------------

goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0] #goal state
init_state = [1, 2, 3, 4, 5, 6, 7, 8, 0] #init state (will be changed to random value)


# Test function for 8 puzzle----------------------------------------------
def test8Puzzle(iteration):

    for i in range(iteration):
        make_rand_8puzzle(init_state, 25) #move ~25 times from goal node
        print(init_state)
        problem_instance = EightPuzzle(tuple(init_state), tuple(goal_state))

        print('Misplaced distance heuristic:')
        node =astar_search(problem_instance, h_modified)
        print('\n')
        print('Manhattan distance heuristic:')
        node =astar_search(problem_instance, manhattan)
        print('\n')
        print('Max num of misplaced or menhattan heuristic:')
        node =astar_search(problem_instance, max_misplaced_menhattan)
        print('\n')
#-------------------------------------------------------------------------

# Test function for house puzzle------------------------------------------
def testHousePuzzle(iteration):

    for i in range(iteration):
        make_rand_HousePuzzle(init_state, 25)  #move ~25 times from goal node
        print(init_state)
        problem_instance = HousePuzzle(tuple(init_state), tuple(goal_state))

        print('Misplaced distance heuristic:')
        node =astar_search(problem_instance, h_modified)
        print('\n')
        print('Manhattan distance heuristic:')
        node =astar_search(problem_instance, manhattan)
        print('\n')
        print('Max num of misplaced or menhattan heuristic:')
        node =astar_search(problem_instance, max_misplaced_menhattan)
        print('\n')
#-------------------------------------------------------------------------
#------------------------function call for testing------------------------
#test8Puzzle(10)
#testHousePuzzle(10)
#-------------------------------------------------------------------------

# -------------------------------------------------------
#test for 8 puzzle
('\n\n')
make_rand_8puzzle(init_state, 25) #move ~50 times from goal state
problem_instance = HousePuzzle(tuple(init_state), tuple(goal_state))

print(init_state)
print('\ninit state:')
display(tuple(init_state))
print('\ngoal state:')
display(tuple(goal_state))
print('\nmisplaced distance heuristic:')
node =astar_search(problem_instance, h_modified)
# print('Solution:', node.solution())  
# print('Path:', node.path())
print('\n')

print('menhattan distance heuristic:')
node =astar_search(problem_instance, manhattan)
# print('Solution:', node.solution())  
# print('Path:', node.path())

print('\n')
print('max num of misplaced or menhattan heuristic:')
node =astar_search(problem_instance, max_misplaced_menhattan)
# print('Solution:', node.solution())  
# print('Path:', node.path())
# -------------------------------------------------------

# -------------------------------------------------------
#test for house puzzle
('\n\n')
print(init_state)
print('\ninit state:')
display_House(tuple(init_state))
print('\ngoal state:')
display_House(tuple(goal_state))
print('\nmisplaced distance heuristic:')
node = make_rand_HousePuzzle(init_state, 25)
problem_instance2 = HousePuzzle(tuple(init_state), tuple(goal_state))

print('\nmisplaced distance heuristic:')
node =astar_search(problem_instance2, h_modified)
# print('Solution:', node.solution())  
# print('Path:', node.path())

print('\n')

print('menhattan distance heuristic:')
node =astar_search(problem_instance2, manhattan)
# print('Solution:', node.solution())  
# print('Path:', node.path())

print('\n')
print('max num of misplaced or menhattan heuristic:')
node =astar_search(problem_instance2, max_misplaced_menhattan)
# print('Solution:', node.solution())  
# print('Path:', node.path())
# -------------------------------------------------------



















