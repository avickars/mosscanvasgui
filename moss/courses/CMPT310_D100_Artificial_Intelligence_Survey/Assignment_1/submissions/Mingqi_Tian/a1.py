from search import *
import numpy as np
import time
import math

# Return a new instance of an EightPuzzle
# problem with a random initial state that
# is solvable
def make_rand_8puzzle():
    while 1:
        # generate a random tuple from 0 to 8
        state = tuple(np.random.permutation(9))
        new_puzzle = EightPuzzle(initial = state)
        # check the initail state is solvable or not
        if new_puzzle.check_solvability(state):
            return new_puzzle

# Print an 8-puzzle in 3*3 matrix
def display(state):
    # convert tuple to list
    temp = list(state)
    for i in range(len(temp)):
        if temp[i] == 0:
            temp[i] = '*'
    # print 3*3 matrix
    print(temp[0], temp[1], temp[2])
    print(temp[3], temp[4], temp[5])
    print(temp[6], temp[7], temp[8])




def row_num(n):
    return (n-1)//3

def col_num(n):
    return (n-1)%3

# Manhattan distance heuristic
def manhattan_h(node):
    state = node.state
    distance = 0
    for i in range(len(state)):
        if state[i] != 0:
            distance = distance + abs(row_num(i+1) - row_num(state[i])) + abs(col_num(i+1) - col_num(state[i]))   
    return distance

# max heuristic
def max_h(node):
    puzzle = EightPuzzle(initial=node.state)
    h1 = puzzle.h(node)
    h2 = manhattan_h(node)
    return max(h1, h2)

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
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta1 = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        delta2 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        delta3 = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank < 3:
            neighbor = blank + delta1[action]
        elif blank == 3:
            neighbor = blank + delta2[action]
        else:
            neighbor = blank + delta3[action]

        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """
        blank = self.find_blank_square(state)
        inversion = 0
        constraint1 = 0
        constraint2 = 0
        possible_2_by_2_state = [(1,2,3,0), (1,0,3,2), (0,1,3,2), \
            (3,1,0,2), (3,1,2,0), (3,0,2,1), (0,3,2,1), (2,3,0,1), \
                (2,3,1,0), (2,0,1,3), (0,2,1,3), (1,2,0,3)]

        if blank <= 3:
            constraint1 = state[0:4] in possible_2_by_2_state
            for i in range(4, len(state)):
                for j in range(i+1, len(state)):
                    if state[i] > state[j]:
                        inversion += 1
            constraint2 = inversion % 2 == 0
        else:
            constraint1 = state[0:3] == (1,2,3)
            for i in range(3, len(state)):
                for j in range(i+1, len(state)):
                    if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                        inversion += 1
            constraint2 = inversion % 2 == 0

        return (constraint1 and constraint2)


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

def row_num_duck(n):
    if n == 1 or n == 2:
        return 0
    if n == 3 or n == 4 or n == 5 or n == 6:
        return 1
    if n == 7 or n == 8 or n == 9:
        return 2

def col_num_duck(n):
    if n == 1 or n == 3:
        return 0
    if n == 2 or n == 4 or n == 7:
        return 1
    if n == 5 or n == 8:
        return 2
    if n == 6 or n == 9:
        return 3
        
def manhattan_duck_h(node):
    state = node.state
    distance = 0
    for i in range(len(state)):
        if state[i] != 0:
            distance = distance + abs(row_num_duck(i+1) - row_num_duck(state[i])) + abs(col_num_duck(i+1) - col_num_duck(state[i]))   
    return distance

def max_duck_h(node):
    puzzle = DuckPuzzle(initial=node.state)
    h1 = puzzle.h(node)
    h2 = manhattan_duck_h(node)
    return max(h1, h2)

def make_rand_duck_puzzle():
    while 1:
        # generate a random tuple from 0 to 8
        state = tuple(np.random.permutation(9))
        new_puzzle = DuckPuzzle(initial = state)
        # check the initail state is solvable or not
        if new_puzzle.check_solvability(state):
            return new_puzzle

def display_duck(state):
    # convert tuple to list
    temp = list(state)
    for i in range(len(temp)):
        if temp[i] == 0:
            temp[i] = '*'

    print(temp[0], temp[1])
    print(temp[2], temp[3], temp[4], temp[5])
    print(' ', temp[6], temp[7], temp[8])


def test_8puzzle(problem):
    h_list = [problem.h, manhattan_h, max_h]
    title_list = ['misplaced', 'Manhattan', 'max']
    for j in range(3):
        print('---------------------------' + title_list[j] + '-------------------------')
        start_time = time.time()
        node = astar_search(problem, h_list[j], True)
        elapsed_time = time.time() - start_time
        print('running time (in seconds): %fs' %elapsed_time)
        print(len(node.solution()))
        #print(node.path())
        #print(node.solution())

def test_duck(problem):
    h_list = [problem.h, manhattan_duck_h, max_duck_h]
    title_list = ['misplaced', 'Manhattan', 'max']
    for j in range(3):
        print('---------------------------' + title_list[j] + '-------------------------')
        start_time = time.time()
        node = astar_search(problem, h_list[j], True)
        elapsed_time = time.time() - start_time
        print('running time (in seconds): %fs' %elapsed_time)
        print(len(node.solution()))
        #print(node.path())
        #print(node.solution())
# --------------------------------test------------------------------
print('********************EIGHT PUZZLE**************************')
myPuzzle = make_rand_8puzzle()
display(myPuzzle.initial)
test_8puzzle(myPuzzle)
print('\n\n*********************DUCK PUZZLE**************************')
myPuzzle = make_rand_duck_puzzle()
display_duck(myPuzzle.initial)
test_duck(myPuzzle)


