# a1.py
from abc import ABC

import numpy
import random
from search import *
import time


# Override A*
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# Override best first graph search
def best_first_graph_search(problem, f, display=False):
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
    node_counter = 0
    while frontier:
        node = frontier.pop()
        node_counter += 1  # add 1 for each pop executed
        if problem.goal_test(node.state):
            if display:
                print("Nodes Removed : \t", node_counter)  # print removed nodes
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


# Manhattan distance heuristic function
def manhattan_d(self):
    """ Return the Manhattan distance heuristic value for a given state.
    """
    standard_state = [[0, 0], [0, 1], [0, 2],  # referenced map
                      [1, 0], [1, 1], [1, 2],
                      [2, 0], [2, 1], [2, 2]
                      ]
    goal_state = {1: [0, 0], 2: [0, 1], 3: [0, 2],  # goal state
                  4: [1, 0], 5: [1, 1], 6: [1, 2],
                  7: [2, 0], 8: [2, 1], 0: [2, 2]
                  }
    return universal_manhattan_calc(self, goal_state, standard_state)


# generalized Manhattan distance calculator
def universal_manhattan_calc(self, goal_state, standard_map):
    mhd = 0
    current_state = {}  # current state
    for i in range(len(self.state)):  # initialize current state
        current_state[self.state[i]] = standard_map[i]

    for i in range(1, 9):  # loop to count mhd for each tile and add them up
        for j in range(2):
            mhd += abs(goal_state[i][j] - current_state[i][j])

    return mhd


# make_rand_8puzzle
def make_rand_8puzzle():
    self = tuple(numpy.random.permutation(9))
    dummy_puzzle = EightPuzzle(initial=self)
    while not dummy_puzzle.check_solvability(self):
        self = tuple(numpy.random.permutation(9))
        dummy_puzzle = EightPuzzle(initial=self)
    return self


# display
def display(state):
    for i in range(9):
        if state[i] == 0:
            print('*', end=' ')
            if i == 2 or i == 5:
                print('\n', end='')
            continue
        print(state[i], end=' ')
        if i == 2 or i == 5:
            print('\n', end='')


# House-puzzle
class HousePuzzle(Problem):
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
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
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

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


def make_rand_housepuzzle():
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    dummy_puzzle = HousePuzzle(initial=goal_state)
    possible_action = dummy_puzzle.actions(dummy_puzzle.initial)

    for i in range(100):
        dummy_puzzle.initial = dummy_puzzle.result(dummy_puzzle.initial, possible_action[random.randint(0, len(possible_action)-1)])
        possible_action = dummy_puzzle.actions(dummy_puzzle.initial)

    return dummy_puzzle.initial


# Manhattan distance heuristic function
def manhattan_d_hp(self):
    """ Return the Manhattan distance heuristic value for a given state.
        """
    standard_state = [[0, 0], [0, 1],  # referenced map
                      [1, 0], [1, 1], [1, 2], [1, 3],
                      [2, 1], [2, 2], [2, 3]
                      ]
    goal_state = {1: [0, 0], 2: [0, 1],  # goal state
                  3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3],
                  7: [2, 1], 8: [2, 2], 0: [2, 3]
                  }
    return universal_manhattan_calc_hp(self, goal_state, standard_state)


# generalized Manhattan distance calculator
def universal_manhattan_calc_hp(self, goal_state, standard_map):
    mhd = 0
    current_state = {}  # current state
    for i in range(len(self.state)):  # initialize current state
        current_state[self.state[i]] = standard_map[i]

    for i in range(1, 9):  # loop to count mhd for each tile and add them up
        for j in range(2):
            mhd += abs(goal_state[i][j] - current_state[i][j])

    return mhd


# main
'''
Solving 8-puzzle
'''

dividing_line = "\n----------------------------------------------------------\n"
# misplaced tile heuristic
puzzle = EightPuzzle(initial=make_rand_8puzzle())
print("Solving 8-puzzle\n")
print(dividing_line)
print("A*-search using the misplaced tile heuristic :\n")
start_time = time.time()
sol = astar_search(puzzle, puzzle.h, True)
elapsed_time = time.time() - start_time
print("Solution Length : \t", sol.path_cost)
print("Running Time : \t", elapsed_time)

# Manhattan distance heuristic
print(dividing_line)
print("A*-search using the Manhattan distance heuristic :\n")
start_time = time.time()
sol = astar_search(puzzle, manhattan_d, True)
elapsed_time = time.time() - start_time
print("Solution Length : \t", sol.path_cost)
print("Running Time : \t", elapsed_time)

# Max of two
print(dividing_line)
print("A*-search using the max of misplaced tile heuristic and Manhattan distance heuristic :\n")
if puzzle.h(Node(puzzle.initial)) > manhattan_d(Node(puzzle.initial)):
    print("Use Misplaced tile heuristic : \n")
    start_time = time.time()
    sol = astar_search(puzzle, puzzle.h, True)
    elapsed_time = time.time() - start_time
    print("Solution Length : \t", sol.path_cost)
    print("Running Time : \t", elapsed_time)
else:
    print("Use Manhattan distance heuristic : \n")
    start_time = time.time()
    sol = astar_search(puzzle, manhattan_d, True)
    elapsed_time = time.time() - start_time
    print("Solution Length : \t", sol.path_cost)
    print("Running Time : \t", elapsed_time)

'''
Solving House-puzzle
'''
puzzle = HousePuzzle(make_rand_housepuzzle())

print(dividing_line)
print("Solving House-puzzle\n")
print("A*-search using the misplaced tile heuristic :\n")
start_time = time.time()
sol = astar_search(puzzle, puzzle.h, True)
elapsed_time = time.time() - start_time
print("Solution Length : \t", sol.path_cost)
print("Running Time : \t", elapsed_time)

# Manhattan distance heuristic
print(dividing_line)
print("A*-search using the Manhattan distance heuristic :\n")
start_time = time.time()
sol = astar_search(puzzle, manhattan_d_hp, True)
elapsed_time = time.time() - start_time
print("Solution Length : \t", sol.path_cost)
print("Running Time : \t", elapsed_time)

# Max of two
print(dividing_line)
print("A*-search using the max of misplaced tile heuristic and Manhattan distance heuristic :\n")
if puzzle.h(Node(puzzle.initial)) > manhattan_d(Node(puzzle.initial)):
    print("Use Misplaced tile heuristic : \n")
    start_time = time.time()
    sol = astar_search(puzzle, puzzle.h, True)
    elapsed_time = time.time() - start_time
    print("Solution Length : \t", sol.path_cost)
    print("Running Time : \t", elapsed_time)
else:
    print("Use Manhattan distance heuristic : \n")
    start_time = time.time()
    sol = astar_search(puzzle, manhattan_d_hp, True)
    elapsed_time = time.time() - start_time
    print("Solution Length : \t", sol.path_cost)
    print("Running Time : \t", elapsed_time)


