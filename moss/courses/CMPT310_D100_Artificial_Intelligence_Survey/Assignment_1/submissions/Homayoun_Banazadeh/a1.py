#please run this one because this is the last one that worked

from search import *
import time
import numpy as np

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
        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        if index_blank_square == 1:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        if index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')      
        if index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_actions.remove('RIGHT')
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


def make_rand_8puzzle():
    my_check_state = False
    while my_check_state == False:
        state = tuple(np.random.permutation(9))
        my_initial_puzzle = EightPuzzle(initial=state)
        my_check_state = my_initial_puzzle.check_solvability(state)
    return my_initial_puzzle

def make_rand_8puzzle():
    my_check_state = False
    while my_check_state == False:
        state = tuple(np.random.permutation(9))
        my_initial_puzzle = EightPuzzle(initial=state)
        my_check_state = my_initial_puzzle.check_solvability(state)
    return my_initial_puzzle

def linear_distance(node):
    state=node.state
    sum=0
    for i in range(9):
        if state[i] != 0:
            if state[i] != i+1:
                sum+=1
    return sum

def aStar_misplayed_tile(instance):
    start_time = time.time()
    node= astar_search(instance)
    elapsed_time = time.time() - start_time
    return elapsed_time



def manhattan_distance(node):
    state=node.state
    arr = [[state[0],state[1],state[2]],
           [state[3],state[4],state[5]],
           [state[6],state[7],state[8]]]
    sum = 0
    for i in range(3):
        for j in range(3):
            if arr[i][j] != 0:
                if arr[i][j] == 1:
                    sum += abs(i-0) + abs(j-0)
                if arr[i][j] == 2:
                    sum += abs(i-0) + abs(j-1)
                if arr[i][j] == 3:
                    sum += abs(i-0) + abs(j-2)
                if arr[i][j] == 4:
                    sum += abs(i-1) + abs(j-0)
                if arr[i][j] == 5:
                    sum += abs(i-1) + abs(j-1)
                if arr[i][j] == 6:
                    sum += abs(i-1) + abs(j-2)
                if arr[i][j] == 7:
                    sum += abs(i-2) + abs(j-0)
                if arr[i][j] == 8:
                    sum += abs(i-2) + abs(j-1)
    return sum
def aStar_manhattan_tile(instance):
    start_time = time.time()
    astar_search(instance,h=manhattan_distance)
    elapsed_time = time.time() - start_time
    return elapsed_time



def max_manhattan_versus_misplayed_distance(node):
    score1 = manhattan_distance(node)
    score2 = linear_distance(node)
    return max(score1, score2)
def aStar_manhattan_versus_misplayed_tile(instance):
    start_time = time.time()
    node = astar_search(instance,h=max_manhattan_versus_misplayed_distance)
    elapsed_time = time.time() - start_time
    return elapsed_time


def make_rand_DuckPuzzle():
    state = tuple(np.random.permutation(9))
    my_initial_puzzle = DuckPuzzle(initial=state)
    return my_initial_puzzle


timeForMisplayed = [0,0,0,0,0,0,0,0,0,0]
timeForManhattan = [0,0,0,0,0,0,0,0,0,0]
timeForMaxBoth = [0,0,0,0,0,0,0,0,0,0]
LengthForMisplayed = [0,0,0,0,0,0,0,0,0,0]
LengthForManhattan = [0,0,0,0,0,0,0,0,0,0]
LengthForMaxBoth = [0,0,0,0,0,0,0,0,0,0]

Duck_timeForMisplayed = [0,0,0,0,0,0,0,0,0,0]
Duck_timeForManhattan = [0,0,0,0,0,0,0,0,0,0]
Duck_timeForMaxBoth = [0,0,0,0,0,0,0,0,0,0]
Duck_LengthForMisplayed = [0,0,0,0,0,0,0,0,0,0]
Duck_LengthForManhattan = [0,0,0,0,0,0,0,0,0,0]
Duck_LengthForMaxBoth = [0,0,0,0,0,0,0,0,0,0]


for i in range(1):
    instance = make_rand_8puzzle()
    LengthForMisplayed[i] = len(astar_search(instance, h=linear_distance).solution())



print(timeForMisplayed)
print(timeForManhattan)
print(timeForMaxBoth)
print(LengthForMisplayed)
print(LengthForManhattan)
print(LengthForMaxBoth)
print(Duck_timeForMisplayed)
print(Duck_timeForManhattan)
print(Duck_timeForMaxBoth)
print(Duck_LengthForMisplayed)
print(Duck_LengthForManhattan)
print(Duck_LengthForMaxBoth)


