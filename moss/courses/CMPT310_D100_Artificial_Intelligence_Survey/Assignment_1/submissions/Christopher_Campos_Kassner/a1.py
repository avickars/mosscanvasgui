'''
Created on May 14, 2020

@author: chris
'''

import numpy as np #Take out later?
import time
import random
import math

from search import *
from _operator import index

state = tuple(np.random.permutation(9))
n = 3
# ______________________________________________________________________________
# Informed (Heuristic) Search

def astar_searchManhattan(problem, h=None):
    h = memoize(h or problem.manhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def astar_searchMaxHeuristic(problem, h=None): 
    h = memoize(h or problem.maxHeuristic, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

# ______________________________________________________________________________
# A* heuristics 

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

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def Manhattan(self, node):
        state = node.state
        L = list(state)
        dist = 0
        for i, item in enumerate(L):
            x1 = int(i/3)
            y1 = i % 3
            x2 = int(item/3)
            y2 = item % 3
            dist += abs(x1 - x2) + abs(y1 - y2)
        return dist


    def maxHeuristic(self, node):
        #    L = list(state)
        misplacedH = self.h(node)
        manhattanH = self.manhattan(node)
        return (max(misplacedH, manhattanH))


# ______________________________________________________________________________


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
        if index_blank_square in (1, 3, 7):
            possible_actions.remove('LEFT')
        if index_blank_square in (1, 2, 5, 6):
            possible_actions.remove('UP')
        if index_blank_square in (2, 6, 8, 0):#Take out 8?
            possible_actions.remove('RIGHT')
        if index_blank_square == 3:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

# blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        if blank < 2:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        if blank > 5:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank > 1 and blank < 6:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
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
    
# ______________________________________________________________________________

def display(state):
    #Convert tuple to list
    L = list(state)
    for i in range(len(L)):
        if L[i] == 0:
            L[i] = '*'
    #Convert list back to tuple        
    L = tuple(L)
    print('\n'.join(' '.join(map(str, L[i:i+n])) for i in range(0, len(L), n)))
    #return L
    return

def make_rand_8puzzle():
    L = list(state)
    for i in range(len(L)):
        z = random.sample(L, 9)
    z = tuple(z)
    puzzle = EightPuzzle(z) #EightPuzzle(z)
    if(puzzle.check_solvability(puzzle.initial) == False):
        make_rand_8puzzle()
    return puzzle

def make_rand_duckPuzzle():
    L = list(state)
    for i in range(len(L)):
        z = random.sample(L, 9)
    z = tuple(z)
    puzzle = DuckPuzzle(z)
    if(puzzle.check_solvability(puzzle.initial) == False):
        make_rand_duckPuzzle()
    return puzzle

def displayDuckPuzzle(state):
    L = list(state)
#    sd = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(9):
        L[i] = state[i]
        if(L[i] == 0):
            L[i] = "*"
    print(L[1], L[2], " ", " ")
    print(L[3], L[4], L[5], L[6])
    print(" ", L[7], L[8], L[0])
    
    

'''
#WORKS FOR GETTING THE ELAPSED TIME OF 1ST A* SEARCH
p1 = make_rand_8puzzle()
start_time= time.time()
astar_search(p1, h=p1.h)
elapsed_time = time.time() - start_time
print(f'elapsed time (in seconds) for A* search: {elapsed_time}s')
print("The number of nodes popped is ", )

#TESTING MANHATTAN HEURISTIC
start_time= time.time()
astar_searchManhattan(p1, h=p1.h)
elapsed_time = time.time() - start_time
print(f'elapsed time (in seconds) for Manhattan Heuristic: {elapsed_time}s')

#TESTING ASTAR MAX HEURISTIC
start_time= time.time()
astar_searchMaxHeuristic(p1, h=p1.h)
elapsed_time = time.time() - start_time
print(f'elapsed time (in seconds) for Max Heuristic: {elapsed_time}s')
'''


'''
#Testing EightPuzzle
for i in range(10):
    p = make_rand_8puzzle()
    
    startAstarsearch = time.time()
    astar_search(p, h=p.h)
    endAstarsearch = time.time() - startAstarsearch
    print(f'elapsed time (in seconds) for Astar search: {endAstarsearch}s')
    
    startManhattan= time.time()
    astar_searchManhattan(p, h=p.h)
    endManhattan = time.time() - startManhattan
    print(f'elapsed time (in seconds) for Manhattan Heuristic: {endManhattan}s')

    startMax= time.time()
    astar_searchMaxHeuristic(p, h=p.h)
    endMax = time.time() - startMax
    print(f'elapsed time (in seconds) for Max Heuristic: {endMax}s')
'''

#Testing duck puzzle
for i in range(10):
    p2 = make_rand_duckPuzzle()

    startAstarsearch = time.time()
    astar_search(p2, h=p2.h)
    endAstarsearch = time.time() - startAstarsearch
    print(f'elapsed time (in seconds) for Astar search: {endAstarsearch}s')
    

    startManhattan= time.time()
    astar_searchManhattan(p2, h=p2.h)
    endManhattan = time.time() - startManhattan
    print(f'elapsed time (in seconds) for Manhattan Heuristic: {endManhattan}s')


    startMax= time.time()
    astar_searchMaxHeuristic(p2, h=p2.h)
    endMax = time.time() - startMax
    print(f'elapsed time (in seconds) for Max Heuristic: {endMax}s')


#~~~~~~~~~~~~~
    
    
    
'''
#randpuzzle = EightPuzzle(initial=state)
#display(state)

#dpuzzle = DuckPuzzle(initial=state)
#displayY2(state)
#dpuzzle.check_solvability(state)

p2 = make_rand_ypuzzle()
start_time= time.time()
astar_search(p2, h=p2.h)
elapsed_time = time.time() - start_time
print(f'elapsed time (in seconds) for A* search: {elapsed_time}s')
'''

#dpuzzle = DuckPuzzle(initial=state)
#displayDuckPuzzle(state)

