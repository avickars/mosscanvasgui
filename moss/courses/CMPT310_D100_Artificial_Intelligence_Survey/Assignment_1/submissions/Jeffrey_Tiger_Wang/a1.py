import random
import time
from search import *

"""Question 1"""


class EightPuzzle1(Problem):
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

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))


def make_rand_8puzzle():
    state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(state)

    puzzle = EightPuzzle1(tuple(state))
    while not puzzle.check_solvability(state):
        random.shuffle(state)
        puzzle = EightPuzzle1(tuple(state))
    return puzzle


def display(state):
    for i in range(0, 9):
        if i == 2 or i == 5 or i == 8:
            if state[i] == 0:
                print("*")
            else:
                print(state[i])
        else:
            if (state[i] == 0):
                print("*", end=" ")
            else:
                print(state[i], end=" ")


"""Question 2"""


def best_first_graph_search1(problem, f, display=False):
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
    countpop = 0
    while frontier:
        node = frontier.pop()
        countpop = countpop + 1
        if problem.goal_test(node.state):
            return node, countpop
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, countpop


def astar_search1(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search1(problem, lambda n: n.path_cost + h(n))


def manhattan1(node):  # from test_search.py but edited.
    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    for i in range(1, 9):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

    return mhd


def max_of_misplaced_and_Manh(node):
    makepuzzle = EightPuzzle1(node.state)
    return max(manhattan1(node), makepuzzle.h(node))


for i in range(1, 11):
    print(i, "Eight Puzzle")
    puzzle0 = make_rand_8puzzle()

    display(puzzle0.initial)
    start_time = time.time()
    misplacedpuzzle, misplacedpop = astar_search1(puzzle0)
    elapsed_time = time.time() - start_time

    print("A* - search using the misplaced tile heuristic")
    print(misplacedpuzzle.solution)  # check solution
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("The length of the solution is: ", len(misplacedpuzzle.solution()))
    print("The total number of nodes that were removed from frontier is: ", misplacedpop)
    print('\n')

    start_time = time.time()
    misplacedpuzzlemanh, misplacedpopmanh = astar_search1(puzzle0, manhattan1)
    elapsed_time = time.time() - start_time

    print("A* - search using the Manhattan distance heuristic")
    print(misplacedpuzzlemanh.solution)  # check solution
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("The length of the solution is: ", len(misplacedpuzzlemanh.solution()))
    print("The total number of nodes that were removed from frontier is: ", misplacedpopmanh)
    print('\n')

    start_time = time.time()
    misplacedpuzzlemax, misplacedpopmax = astar_search1(puzzle0, max_of_misplaced_and_Manh)
    elapsed_time = time.time() - start_time

    print("A* - search using the max of the misplaced tile heuristic and Manhattan distance heuristic")
    print(misplacedpuzzlemax.solution)  # check solution
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("The length of the solution is: ", len(misplacedpuzzlemax.solution()))
    print("The total number of nodes that were removed from frontier is: ", misplacedpopmax)
    print('\n')


"""Question 3"""


class House(Problem):
    """ Duck puzzle/house-puzzle problem. The following code is based on the function EightPuzzle from search.py"""

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
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')

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

        if (blank == 0) or (blank == 1):
            delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        if blank == 2 or blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        if blank > 3:
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

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))


def make_rand_house():
    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    pmove = ["UP", "DOWN", "LEFT", "RIGHT"]
    pmove1 = ["UP", "LEFT"]
    hpuzzle = House(tuple(state))
    random.shuffle(pmove)
    random.shuffle(pmove1)

    something1 = hpuzzle.result(state, pmove1[0])
    # print(something1)
    hpuzzle = House(tuple(something1))

    for x in range(50000):
        random.shuffle(pmove)
        if pmove[0] in hpuzzle.actions(something1):
            something1 = hpuzzle.result(something1, pmove[0])
            hpuzzle = House(tuple(something1))
    return hpuzzle


def displayh(state):
    for i in range(0, 9):
        if i == 1 or i == 5 or i == 8:
            if state[i] == 0:
                print("*")
            else:
                print(state[i])
        elif i == 6:
            if state[i] == 0:
                print("  *", end=" ")
            else:
                print(" ", state[i], end=" ")
        else:
            if state[i] == 0:
                print("*", end=" ")
            else:
                print(state[i], end=" ")


def manhattanh(node):  # from test_search.py but edited.
    state = node.state
    index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
    index_state = {}
    index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    for i in range(1, 9):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

    return mhd


def max_of_h(node):
    makepuzzle = House(node.state)
    return max(manhattanh(node), makepuzzle.h(node))


for i in range(1, 11):
    print(i, "House Puzzle")
    puzzle0 = make_rand_house()

    displayh(puzzle0.initial)
    start_time = time.time()
    misplacedpuzzle, misplacedpop = astar_search1(puzzle0)
    elapsed_time = time.time() - start_time

    print("A* - search using the misplaced tile heuristic")
    print(misplacedpuzzle.solution)  # check solution
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("The length of the solution is: ", len(misplacedpuzzle.solution()))
    print("The total number of nodes that were removed from frontier is: ", misplacedpop)
    print('\n')

    start_time = time.time()
    misplacedpuzzlemanh, misplacedpopmanh = astar_search1(puzzle0, manhattanh)
    elapsed_time = time.time() - start_time

    print("A* - search using the Manhattan distance heuristic")
    print(misplacedpuzzlemanh.solution)  # check solution
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("The length of the solution is: ", len(misplacedpuzzlemanh.solution()))
    print("The total number of nodes that were removed from frontier is: ", misplacedpopmanh)
    print('\n')

    start_time = time.time()
    misplacedpuzzlemax, misplacedpopmax = astar_search1(puzzle0, max_of_h)
    elapsed_time = time.time() - start_time

    print("A* - search using the max of the misplaced tile heuristic and Manhattan distance heuristic")
    print(misplacedpuzzlemax.solution)  # check solution
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("The length of the solution is: ", len(misplacedpuzzlemax.solution()))
    print("The total number of nodes that were removed from frontier is: ", misplacedpopmax)
    print('\n')