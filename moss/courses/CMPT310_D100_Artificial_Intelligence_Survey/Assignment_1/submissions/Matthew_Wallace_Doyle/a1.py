# a1.py
# Matthew Doyle 301322233
# 2020-05-27

import time
from search import *


# ______________________________________________________________________________
# Altered code from search.py

def my_best_first_graph_search(problem, f, display=False):
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
    removedNode = 0
    while frontier:
        node = frontier.pop()
        removedNode += 1  # count number of times frontier is removed
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, removedNode]  # return number of times frontier is removed
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


# ______________________________________________________________________________
# Informed (Heuristic) Search

def my_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return my_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# ______________________________________________________________________________
# A* heuristics

class MyEightPuzzle(Problem):
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

    # http: // theory.stanford.edu / ~amitp / GameProgramming / Heuristics.html
    def manhattan_dist(self, node):
        return sum(abs(a - b) for a, b in zip(node.state, self.goal))


# ______________________________________________________________________________
# My Class

class DuckPuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        # special cases for the duck puzzle
        up_not_possible = (0, 1, 4, 5)
        down_not_possible = (2, 6, 7, 8)
        right_not_possible = (1, 5, 8)
        left_not_possible = (0, 2, 6)

        if index_blank_square in left_not_possible:
            possible_actions.remove('LEFT')
        if index_blank_square in up_not_possible:
            possible_actions.remove('UP')
        if index_blank_square in right_not_possible:
            possible_actions.remove('RIGHT')
        if index_blank_square in down_not_possible:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
         Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        # special cases added for the duck puzzle
        delta_duck = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        blank_duck = (0, 1, 2, 3)

        if blank in blank_duck:
            neighbor = blank + delta_duck[action]
        else:
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

    # http: // theory.stanford.edu / ~amitp / GameProgramming / Heuristics.html
    def manhattan_dist(self, node):
        return sum(abs(a - b) for a, b in zip(node.state, self.goal))


# ______________________________________________________________________________
# My Helper functions

def display(state):
    n = 0
    for item in state:
        if item == 0:
            print("*", end=" ")
        else:
            print(str(item), end=" ")
        n += 1
        if n % 3 == 0:
            print()


def display_duck(state):
    n = 0
    for item in state:
        if item == 0:
            print("*", end=" ")
        else:
            print(str(item), end=" ")
        n += 1
        if n == 2:
            print()
        if n == 6:
            print()
            print(" ", end=" ")
    print()


def make_rand_8puzzle():
    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    puzzle = MyEightPuzzle(state)
    permutation = []
    perm_solve = False
    while not perm_solve:
        random.shuffle(state)
        perm_solve = puzzle.check_solvability(state)

        if perm_solve:
            permutation = tuple(state)

    return MyEightPuzzle(permutation)


def make_rand_duck_puzzle():
    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    puzzle = DuckPuzzle(state)
    permutation = []
    perm_solve = False
    while not perm_solve:
        random.shuffle(state)
        perm_solve = puzzle.check_solvability(state)

        if perm_solve:
            permutation = tuple(state)

    return EightPuzzle(permutation)


def test_8_puzzles():
    # misplaced tile
    puzzle = make_rand_8puzzle()
    display(puzzle.initial)
    start_time = time.time()
    result = my_astar_search(puzzle)
    elapsed_time = time.time() - start_time
    print(f'A*-search (missing tile) elapsed time (in seconds): {elapsed_time}s')
    print("Length of the solution: ", result[0].path_cost)
    print("Total number of nodes removed: ", result[1], "\n")

    # manhattan distance
    start_time = time.time()
    result = my_astar_search(puzzle, puzzle.manhattan_dist)
    elapsed_time = time.time() - start_time
    print(f'A*-search (manhattan distance) elapsed time (in seconds): {elapsed_time}s')
    print("Length of the solution: ", result[0].path_cost)
    print("Total number of nodes removed: ", result[1], "\n")

    # using both
    start_time = time.time()
    result = my_astar_search(puzzle, lambda n: max(puzzle.h(n), puzzle.manhattan_dist(n)))
    elapsed_time = time.time() - start_time
    print(f'A*-search (max of both) elapsed time (in seconds): {elapsed_time}s')
    print("Length of the solution: ", result[0].path_cost)
    print("Total number of nodes removed: ", result[1], "\n")


def test_duck_puzzles():
    # misplaced tile
    puzzle = make_rand_duck_puzzle()
    display_duck(puzzle.initial)
    start_time = time.time()
    result = my_astar_search(puzzle)
    elapsed_time = time.time() - start_time
    print(f'A*-search time using the misplaced tile heuristic:  {elapsed_time}s')
    print("Length of the solution: ", result[0].path_cost)
    print("Total number of nodes removed: ", result[1], "\n")

    # manhattan distance
    start_time = time.time()
    result = my_astar_search(puzzle, puzzle.manhattan_dist)
    elapsed_time = time.time() - start_time
    print(f'A*-search time using the Manhattan Distance heuristic:  {elapsed_time}s')
    print("Length of the solution: ", result[0].path_cost)
    print("Total number of nodes removed: ", result[1], "\n")

    # using both
    start_time = time.time()
    result = my_astar_search(puzzle, lambda n: max(puzzle.h(n), puzzle.manhattan_dist(n)))
    elapsed_time = time.time() - start_time
    print(f'A*-search time using the Max of both heuristic:  {elapsed_time}s')
    print("Length of the solution: ", result[0].path_cost)
    print("Total number of nodes removed: ", result[1], "\n")


# ______________________________________________________________________________
# My Test Functions

# Question 1: Helper Function
def q1():
    print("Question 1")
    print("----------")
    display(make_rand_8puzzle().initial)
    print()


# Question 2: Comparing Algorithms
def q2():
    print("Question 2")
    print("----------")

    for i in range(10):
        print("8-Puzzle Test:", i + 1)
        test_8_puzzles()


# Question 3: The House-Puzzle
def q3():
    print("Question 3")
    print("----------")

    for i in range(10):
        print("Duck Puzzle Test:", i + 1)
        test_duck_puzzles()


# ______________________________________________________________________________
# Calling My Test Functions

q1()
q2()
q3()