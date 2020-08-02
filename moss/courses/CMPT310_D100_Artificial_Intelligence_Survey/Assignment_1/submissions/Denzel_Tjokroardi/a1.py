# a1.py

import random
import time
from random import randint

from search import *


# EightPuzzle Class
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
        puzzle_initial = node.state
        return sum(s != g for (s, g) in ((puzzle_initial.index(i), self.goal.index(i)) for i in range(1, 9)))


# DuckPuzzle Class
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
        if index_blank_square == 8 or index_blank_square == 5 or index_blank_square == 1:
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

        if blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        elif blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        elif blank > 3:
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
        puzzle_initial = node.state
        return sum(s != g for (s, g) in ((puzzle_initial.index(i), self.goal.index(i)) for i in range(1, 9)))


# Best first graph search
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
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                sum = 0
                for i in range(len(node.path())):
                    sum += i
                print("PATH SUM= " + str(sum))
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


# A* search
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# 8PUZZLE GENERATION

def num_list_generator():
    num_list = random.sample(range(9), 9)
    return num_list


def instantiate_rand_8puzzle(new_problem):
    new_eight_puzzle = EightPuzzle(new_problem)
    num_tuple = tuple(num_list_generator())
    new_eight_puzzle.initial = num_tuple
    return new_eight_puzzle


def make_rand_8puzzle():
    new_problem = Problem
    new_eight_puzzle = instantiate_rand_8puzzle(new_problem)
    while new_eight_puzzle.check_solvability(new_eight_puzzle.initial) == False:
        new_eight_puzzle = instantiate_rand_8puzzle(new_problem)
    return new_eight_puzzle


def display(state):
    for i in range(9):
        if (i + 1) % 3 == 0:
            if state[i] == 0:
                print("*", end="\n")
            else:
                print(state[i], end="\n")
        else:
            if state[i] == 0:
                print("*", end=" ")
            else:
                print(state[i], end=" ")


def create_testing_puzzles():
    list_of_tests = [0] * 15
    for i in range(15):
        list_of_tests[i] = make_rand_8puzzle()
    return list_of_tests


# Adapted code source: https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight
# -puzzle
def manhattan(node):
    puzzle_initial = list(node.state)
    puzzle_goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    return sum(abs(initial % 3 - goal % 3) + abs(initial // 3 - goal // 3)
               for initial, goal in ((puzzle_initial.index(i), puzzle_goal.index(i)) for i in range(1, 9)))


def test_puzzles():
    list_of_test = create_testing_puzzles()
    print("PRINTING LIST OF TESTS *****")
    for i in list_of_test:
        print(i.initial)

    print()
    # A*-search using default heuristic
    print("DEFAULT HEURISTIC ******")
    for i in list_of_test:
        start = time.time()
        astar_search(i, display=True)
        end = time.time()
        print("Time " + str(end - start))

    print()
    # A*-search using Manhattan Heuristic
    print("MANHATTAN HEURISTIC ******")
    for i in list_of_test:
        start = time.time()
        astar_search(i, h=manhattan, display=True)
        end = time.time()
        print("Time " + str(end - start))

    print()
    # A*-search using Max Heuristic
    print("MAX HEURISTIC ********")
    for i in list_of_test:
        new_node = Node(i.initial)
        manhattan_sum = manhattan(new_node)
        default_sum = i.h(new_node)
        if manhattan_sum >= default_sum:
            start = time.time()
            astar_search(i, h=manhattan, display=True)
            end = time.time()
            print("Time " + str(end - start))
        else:
            start = time.time()
            astar_search(i, display=True)
            end = time.time()
            print("Time " + str(end - start))


# DUCKPUZZLE  GENERATION
def generate_DuckPuzzle():
    new_problem = Problem
    new_duck_puzzle = DuckPuzzle(new_problem)
    new_duck_puzzle.initial = new_duck_puzzle.goal
    actions = new_duck_puzzle.actions(new_duck_puzzle.initial)
    result = new_duck_puzzle.result(new_duck_puzzle.initial, actions[0])
    rand_num = randint(1, 100000)
    i = 0
    while i < rand_num:
        actions = new_duck_puzzle.actions(result)
        rand_movement = randint(0, len(actions) - 1)
        result = new_duck_puzzle.result(result, actions[rand_movement])
        i += 1
    new_duck_puzzle.initial = result
    return new_duck_puzzle


def create_duck_puzzles():
    list_of_tests = [0] * 15
    for i in range(15):
        list_of_tests[i] = generate_DuckPuzzle()
    return list_of_tests


def test_duck_puzzles():
    list_of_duck_puzzles = create_duck_puzzles()
    print("LIST OF INITIAL STATES")
    for i in list_of_duck_puzzles:
        print(i.initial)

    print()
    # A*-search using default heuristic
    print("DEFAULT HEURISTIC ******")
    for i in list_of_duck_puzzles:
        start = time.time()
        astar_search(i, display=True)
        end = time.time()
        print("Time " + str(end - start))

    print()
    # A*-search using Manhattan Heuristic
    print("MANHATTAN HEURISTIC ******")
    for i in list_of_duck_puzzles:
        start = time.time()
        astar_search(i, h=manhattan_duck, display=True)
        end = time.time()
        print("Time " + str(end - start))

    print()
    # A*-search using Max Heuristic
    print("MAX HEURISTIC ********")
    for i in list_of_duck_puzzles:
        new_node = Node(i.initial)
        manhattan_sum = manhattan(new_node)
        default_sum = i.h(new_node)
        if manhattan_sum >= default_sum:
            start = time.time()
            astar_search(i, h=manhattan_duck, display=True)
            end = time.time()
            print("Time " + str(end - start))
        else:
            start = time.time()
            astar_search(i, display=True)
            end = time.time()
            print("Time " + str(end - start))


def manhattan_duck(node):
    puzzle_initial = list(node.state)
    puzzle_goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    coords = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2)]
    total = 0
    for i in range(1, 9):
        initial_index = puzzle_initial.index(i)
        x1, y1 = coords[initial_index]
        goal_index = puzzle_goal.index(i)
        x2, y2 = coords[goal_index]
        total += abs(x2 - x1) + abs(y2 - y1)
    return total


# test_puzzles()
test_duck_puzzles()
