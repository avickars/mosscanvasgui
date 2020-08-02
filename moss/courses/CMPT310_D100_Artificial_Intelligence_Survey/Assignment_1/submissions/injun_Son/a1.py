"""
    Class: CMPT 310
    Name: Injun Son
    Date: May 29, 2020
    Assignment1 : Experementing with the 8-puzzle
"""

#a1.py
import sys
sys.path.insert(0, 'C:\\Users\\injoo\\Desktop\\SFU\\2020.5 Sixth Semester\\CMPT 310\\aima-python-master\\aima-python-master')
from search import *
import random
import copy



#-----------------------

#Question1: Helper functions
def make_rand_8puzzle():
    state = list(range(9))
    random.shuffle(state)
    #state  = [1,2,3,4,5,6,7,0,8]
    eightPuzzle = EightPuzzle(tuple(state))

    while (eightPuzzle.check_solvability(state)== False):
        random.shuffle(state)
        eightPuzzle = EightPuzzle(tuple(state))
    return eightPuzzle


def display(state):
    for i in range(len(state)):
        if(state[i]==0):
            print('*', end=" ")
        else:
            print(state[i], end=" ")
        if(i%3== 2):
            print()


#---------------------------------------------
#this is from TA's tutorial file.
# g(n): the cost to reach the node n (the path cost from the start node to node n)
# h(n): the estimated cost to get from node n to the goal
# A∗ search is a form of best-first search. It tries first the node with the
# lowest value of f(n) = g(n) + h(n).

# Conditions for optimality: Admissibility and consistency
# number of misplaced tiles: h1 = 8
# Manhattan distance: h2 = 3 + 1 + 2 + 2 + 2 + 3 + 3 + 2 = 18
# An admissible heuristic is one that never overestimates the cost to reach the goal.

# As expected, neither of these overestimates the true solution cost, which is 26.
#Question2
import time

#https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game
def Manhattan(node):
    state = node.state
    mhd = 0
    for i, item in enumerate(state):
        prev_row, prev_col = int(i/3), i%3
        goal_row, goal_col = int(item/3), item%3
        mhd += abs(prev_row - goal_row) + abs(prev_col - goal_col)

    return mhd


answer = []
for i in range(0,0):
    eightPuzzle = make_rand_8puzzle()
    manhAstar = copy.deepcopy(eightPuzzle)
    maxAstar = copy.deepcopy(eightPuzzle)

    display(eightPuzzle.initial)
    print("----------Below is result from A* algorithm---------")
    startTime = time.time()
    node, pop_sum= astar_search(eightPuzzle)
    elapsedTime = time.time() - startTime
    print('Solution: ', node.solution())
    print("Path: ", node.path())
    print("total number of nodes that were removed from frontier: ", pop_sum)
    print(len(node.path()))
    print("elapsed time:", elapsedTime)
    lst = [elapsedTime, len(node.path()), pop_sum]
    answer.append(lst)

    display(manhAstar.initial)
    print("----------Below is result from Manhattan algorithm---------")
    startTime = time.time()
    manhatan_result, man_pop_sum= astar_search(manhAstar, h=Manhattan)
    elapsedTime = time.time() - startTime
    print('Solution: ', manhatan_result.solution())
    print("Path: ", manhatan_result.path())
    print("total number of nodes that were removed from frontier: ", man_pop_sum)
    print(len(manhatan_result.path()))
    print("elapsed time:", elapsedTime)
    lst = [elapsedTime, len(manhatan_result.path()), man_pop_sum]
    answer.append(lst)

    display(maxAstar.initial)
    print("----------Below is using the max of the misplaced tile heuristic and the Manhattan distance heuristic---------")
    startTime = time.time()
    mixed_result, mixed_pop_sum= astar_search(maxAstar, h=max_mixed)
    elapsedTime = time.time() - startTime
    print('Solution: ', mixed_result.solution())
    print("Path: ", mixed_result.path())
    print("total number of nodes that were removed from frontier: ", mixed_pop_sum)
    print(len(mixed_result.path()))
    print("elapsed time:", elapsedTime)
    lst = [elapsedTime, len(mixed_result.path()), mixed_pop_sum]
    answer.append(lst)

#---------------------------------------------
#Below is changed class and functions is search.py 
#Q3: The House-puzzle (Duck-puzzle)

# class DPuzzle(Problem):
#     """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
#     squares is a blank. A state is represented as a tuple of length 9, where  element at
#     index i represents the tile number  at index i (0 if it's an empty square) """
#
#     def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
#         """ Define goal state and initialize a problem """
#         super().__init__(initial, goal)
#
#     def find_blank_square(self, state):
#         """Return the index of the blank square in a given state"""
#
#         return state.index(0)
#
#     def actions(self, state):
#         """ Return the actions that can be executed in the given state.
#         The result would be a list, since there are only four possible actions
#         in any given state of the environment """
#
#         possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
#         index_blank_square = self.find_blank_square(state)
#
#         if index_blank_square == 0:
#             possible_actions.remove('LEFT')
#             possible_actions.remove('UP')
#         if index_blank_square == 1 or index_blank_square == 5:
#             possible_actions.remove('UP')
#             possible_actions.remove('RIGHT')
#
#         if index_blank_square == 2 or index_blank_square == 6:
#             possible_actions.remove('LEFT')
#             possible_actions.remove('DOWN')
#
#         if index_blank_square== 4:
#             possible_actions.remove('UP')
#
#         if index_blank_square== 7:
#             possible_actions.remove('DOWN')
#         if index_blank_square==8:
#             possible_actions.remove('DOWN')
#             possible_actions.remove('RIGHT')
#
#         return possible_actions
#
#     def result(self, state, action):
#         """ Given state and action, return a new state that is the result of the action.
#         Action is assumed to be a valid action in the state """
#
#         # blank is the index of the blank square
#         blank = self.find_blank_square(state)
#         new_state = list(state)
#         delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
#
#         if blank==0:
#             delta = {'UP': 0, 'DOWN': 2, 'LEFT': 0, 'RIGHT': 1}
#             neighbor = blank + delta[action]
#             new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
#         if blank==1:
#             delta = {'UP': 0, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 0}
#             neighbor = blank + delta[action]
#             new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
#         if blank==2:
#             delta = {'UP': -2, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}
#             neighbor = blank + delta[action]
#             new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
#         if blank==3:
#             delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
#             neighbor = blank + delta[action]
#             new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
#         if blank==4:
#             delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
#             neighbor = blank + delta[action]
#             new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
#         if blank==5:
#             delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 0}
#             neighbor = blank + delta[action]
#             new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
#         if blank==6:
#             delta = {'UP': -3, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}
#             neighbor = blank + delta[action]
#             new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
#         if blank==7:
#             delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
#             neighbor = blank + delta[action]
#             new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
#         if blank==8:
#             delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 0}
#             neighbor = blank + delta[action]
#             new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
#
#         return tuple(new_state)
#
#     def goal_test(self, state):
#         """ Given a state, return True if state is a goal state or False, otherwise """
#
#         return state == self.goal
#
#     def check_solvability(self, state):
#         """ Checks if the given state is solvable """
#
#         return True
#
#     def h(self, node):
#         """ Return the heuristic value for a given state. Default heuristic function used is
#         h(n) = number of misplaced tiles """
#
#         return sum(s != g for (s, g) in zip(node.state, self.goal))
#
#
# def make_rand_Dpuzzle():
#
#     #below are all solvable
#     states = [[1,2,3,4,5,6,7,0,8], [1,2,3,4,5,0,7,8,6], [1,2,3,4,0,6,7,5,8], [1,2,3,4,5,6,0,7,8] , [1,2,3,4,0,5,7,8,6], [1,2,3,0,4,5,7,8,0]]
#     randIndex = random.randint(0, 6)
#     DPuzzle = DPuzzle(tuple(states[randIndex]))
#
#     return DPuzzle
#
#
# def dispaly_Dpuzzle(state):
#     for i in range(len(state)):
#         if state[i] == 0:
#             state[i] = '*'
#
#     for i in range(2):
#         print(state[i]+' ', end='')
#     print()
#     for i in range (2, 6):
#         print(state[i]+' ', end='')
#     print()
#     print(' ', end='')
#     for i in range (6, 9):
#         print(state[i]+' ', end='')
#     print()

#-----------------------------

for i in range (0, 10):
    DPuzzle = make_rand_Dpuzzle()
    DmanhAstar = copy.deepcopy(DPuzzle)
    DmaxAstar = copy.deepcopy(DPuzzle)

    dispaly_Dpuzzle(DPuzzle.initial)
    print("----------Below is result from D_A* algorithm---------")
    startTime = time.time()
    node, pop_sum= astar_search(DPuzzle)
    elapsedTime = time.time() - startTime
    print('Solution: ', node.solution())
    print("Path: ", node.path())
    print("total number of nodes that were removed from frontier: ", pop_sum)
    print(len(node.path()))
    print("elapsed time:", elapsedTime)
    lst = [elapsedTime, len(node.path()), pop_sum]
    answer.append(lst)

    dispaly_Dpuzzle(DPuzzle.initial)
    print("----------Below is result from D_Manhattan algorithm---------")
    startTime = time.time()
    node, pop_sum= astar_search(DmanhAstar)
    elapsedTime = time.time() - startTime
    print('Solution: ', node.solution())
    print("Path: ", node.path())
    print("total number of nodes that were removed from frontier: ", pop_sum)
    print(len(node.path()))
    print("elapsed time:", elapsedTime)
    lst = [elapsedTime, len(node.path()), pop_sum]
    answer.append(lst)


    dispaly_Dpuzzle(DmaxAstar.initial)
    print("----------Below is using the max of the misplaced tile heuristic and the Manhattan distance heuristic---------")
    startTime = time.time()
    mixed_result, mixed_pop_sum= astar_search(DmaxAstar, h=max_mixed)
    elapsedTime = time.time() - startTime
    print('Solution: ', mixed_result.solution())
    print("Path: ", mixed_result.path())
    print("total number of nodes that were removed from frontier: ", mixed_pop_sum)
    print(len(mixed_result.path()))
    print("elapsed time:", elapsedTime)
    lst = [elapsedTime, len(mixed_result.path()), mixed_pop_sum]
    answer.append(lst)
