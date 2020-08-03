# a1.py

from search import *
import random
import time

# Question 1----------------------------------------------------------------------------------------

def make_rand_8puzzle():
    endLoop = False
    eightPuzzle = 0
    while not endLoop:
        initialTuple = tuple(random.sample(range(9), 9))
        eightPuzzle = EightPuzzle(initialTuple, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))
        endLoop = eightPuzzle.check_solvability(eightPuzzle.initial)
    return eightPuzzle


def display(state):
    list1 = [0, 0, 0]
    list2 = [0, 0, 0]
    list3 = [0, 0, 0]

    for i in range(3):
        if state[i] == 0:
            list1[i] = "*"
        else:
            list1[i] = state[i]
    for i in range(3, 6):
        if state[i] == 0:
            list2[i - 3] = "*"
        else:
            list2[i - 3] = state[i]
    for i in range(6, 9):
        if state[i] == 0:
            list3[i - 6] = "*"
        else:
            list3[i - 6] = state[i]

    print(*list1)
    print(*list2)
    print(*list3)


# -------------------------------------------------------------------------------------------------

# Question 2---------------------------------------------------------------------------------------


def astar_search_modified(problem, h=None, display=False):
    # A* search is best-first graph search with f(n) = g(n)+h(n).
    # You need to specify the h function when you call astar_search, or
    # else in your Problem subclass.
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_modified(problem, lambda n: n.path_cost + h(n), display)


def best_first_graph_search_modified(problem, f, display=True):
    # Search the nodes with the lowest f scores first.
    # You specify the function f(node) that you want to minimize; for example,
    # if f is a heuristic estimate to the goal, then we have greedy best
    # first search; if f is node.depth then we have breadth-first search.
    # There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    # values will be cached on the nodes as they are computed. So after doing
    # a best first search you can examine the f values of the path returned.
    f = memoize(f, 'f')
    nodes_removed_counter = 0
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    while frontier:
        nodes_removed_counter = nodes_removed_counter + 1
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print("Total number of nodes removed from frontier:", nodes_removed_counter)
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


class EightPuzzle(Problem):
    #  The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    # squares is a blank. A state is represented as a tuple of length 9, where  element at
    # index i represents the tile number  at index i (0 if it's an empty square) 

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        #  Define goal state and initialize a problem 
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        # Return the index of the blank square in a given state

        return state.index(0)

    def actions(self, state):
        #  Return the actions that can be executed in the given state.
        # The result would be a list, since there are only four possible actions
        # in any given state of the environment 

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
        #  Given state and action, return a new state that is the result of the action.
        # Action is assumed to be a valid action in the state 

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        #  Given a state, return True if state is a goal state or False, otherwise 

        return state == self.goal

    def check_solvability(self, state):
        #  Checks if the given state is solvable 

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        #  Return the heuristic value for a given state. Default heuristic function used is
        # h(n) = number of misplaced tiles 

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        state = node.state
        goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        manhattanDistance = 0

        for i in range(len(state)):
            for j in range(2):
                manhattanDistance = abs(goal[i][j] - index_state[i][j]) + manhattanDistance
        return manhattanDistance

    def max_misplaced_and_manhattan(self, node):
        misplacedValue = self.h(node)
        manhattanValue = self.manhattan(node)
        return max(misplacedValue, manhattanValue)


def heuristic_records(puzzle):
    print("\nSolving 8-puzzle using the MISPLACED TILE HEURISTIC:")
    start_time = time.time()
    final_state = astar_search_modified(puzzle, puzzle.h, True)
    elapsed_time = time.time() - start_time

    print("Total running time:", elapsed_time, "seconds")
    print("Total length of the solution:", final_state.path_cost)
    print("Final state")
    display(final_state.state)
    print("\n")


def manhattan_records(puzzle):
    print("\nSolving 8-puzzle using the MANHATTAN DISTANCE HEURISTIC:")
    start_time = time.time()
    final_state = astar_search_modified(puzzle, puzzle.manhattan, True)
    elapsed_time = time.time() - start_time

    print("Total running time:", elapsed_time, "seconds")
    print("Total length of the solution:", final_state.path_cost)
    print("Final state")
    display(final_state.state)
    print("\n")


def max_records(puzzle):
    print("\nSolving 8-puzzle using the MAX of both HEURISTICS:")
    start_time = time.time()
    final_state = astar_search_modified(puzzle, puzzle.max_misplaced_and_manhattan, True)
    elapsed_time = time.time() - start_time

    print("Total running time:", elapsed_time, "seconds")
    print("Total length of the solution:", final_state.path_cost)
    print("Final state")
    display(final_state.state)
    print("\n")


def compare_algorithms():
    randomPuzzles = []
    for i in range(10):
        puzzle = make_rand_8puzzle()
        randomPuzzles.append(puzzle)
    for j in range(10):
        print("\nRandom puzzle:", j + 1)
        print("Initial state")
        display(randomPuzzles[j].initial)

        heuristic_records(randomPuzzles[j])

        manhattan_records(randomPuzzles[j])

        max_records(randomPuzzles[j])


compare_algorithms()




# -------------------------------------------------------------------------------------------------

# Question 3---------------------------------------------------------------------------------------


class DuckPuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        # """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        # """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        # """ Return the actions that can be executed in the given state.
        # The result would be a list, since there are only four possible actions
        # in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
        up = [0, 1, 4, 5]
        down = [2, 6, 7, 8]
        left = [0, 2, 6]
        right = [1, 5, 8]

        for i in range(len(up)):
            if index_blank_square == up[i]:
                possible_actions.remove('UP')

        for i in range(len(down)):
            if index_blank_square == down[i]:
                possible_actions.remove('DOWN')

        for i in range(len(right)):
            if index_blank_square == right[i]:
                possible_actions.remove('RIGHT')

        for i in range(len(left)):
            if index_blank_square == left[i]:
                possible_actions.remove('LEFT')

        return possible_actions

    def result(self, state, action):
        # """ Given state and action, return a new state that is the result of the action.
        # Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta_lower = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        delta_centre = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        delta_upper = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}

        upper = [0, 1, 2]
        lower = [4, 5, 6, 7, 8]

        for i in range(len(upper)):
            if blank == upper[i]:
                neighbor = blank + delta_upper[action]
                new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        for i in range(len(lower)):
            if blank == lower[i]:
                neighbor = blank + delta_lower[action]
                new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        if blank == 3:
            neighbor = blank + delta_centre[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        # """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        # """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        # """ Return the heuristic value for a given state. Default heuristic function used is
        # h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan_duck(self, node):
        state = node.state
        goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        manhattanDistance = 0

        for i in range(len(state)):
            for j in range(2):
                manhattanDistance = abs(goal[i][j] - index_state[i][j]) + manhattanDistance
        return manhattanDistance

    def max_misplaced_and_manhattan_duck(self, node):
        misplacedValue = self.h(node)
        manhattanValue = self.manhattan_duck(node)
        return max(misplacedValue, manhattanValue)


def make_rand_duckpuzzle():
    endLoop = False
    duckPuzzle = 0
    while not endLoop:
        initialTuple = tuple(random.sample(range(9), 9))
        duckPuzzle = DuckPuzzle(initialTuple, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))
        endLoop = duckPuzzle.check_solvability(duckPuzzle.initial)
    return duckPuzzle


def display_duck(state):
    list1 = [0, 0]
    list2 = [0, 0, 0, 0]
    list3 = [" ", 0, 0, 0]

    for i in range(2):
        if state[i] == 0:
            list1[i] = "*"
        else:
            list1[i] = state[i]
    for i in range(2, 6):
        if state[i] == 0:
            list2[i - 2] = "*"
        else:
            list2[i - 2] = state[i]
    for i in range(6, 9):
        if state[i] == 0:
            list3[i - 5] = "*"
        else:
            list3[i - 5] = state[i]

    print(*list1)
    print(*list2)
    print(*list3)


def astar_search_modified_duck(problem, h=None, display=False):
    # """A* search is best-first graph search with f(n) = g(n)+h(n).
    # You need to specify the h function when you call astar_search, or
    # else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_modified_duck(problem, lambda n: n.path_cost + h(n), display)


def best_first_graph_search_modified_duck(problem, f, display=True):
    # """Search the nodes with the lowest f scores first.
    # You specify the function f(node) that you want to minimize; for example,
    # if f is a heuristic estimate to the goal, then we have greedy best
    # first search; if f is node.depth then we have breadth-first search.
    # There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    # values will be cached on the nodes as they are computed. So after doing
    # a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    nodes_removed_counter = 0
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    while frontier:
        nodes_removed_counter = nodes_removed_counter + 1
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print("Total number of nodes removed from frontier:", nodes_removed_counter)
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return node


def heuristic_records_duck(puzzle_duck):
    print("\nSolving Duck-puzzle using the MISPLACED TILE HEURISTIC:")
    start_time = time.time()
    final_state = astar_search_modified_duck(puzzle_duck, puzzle_duck.h, True)
    elapsed_time = time.time() - start_time

    print("Total running time:", elapsed_time, "seconds")
    print("Total length of the solution:", final_state.path_cost)
    print("Final state")
    display_duck(final_state.state)
    print("\n")


def manhattan_records_duck(puzzle_duck):
    print("\nSolving Duck-puzzle using the MANHATTAN DISTANCE HEURISTIC:")
    start_time = time.time()
    final_state = astar_search_modified_duck(puzzle_duck, puzzle_duck.manhattan_duck, True)
    elapsed_time = time.time() - start_time

    print("Total running time:", elapsed_time, "seconds")
    print("Total length of the solution:", final_state.path_cost)
    print("Final state")
    display_duck(final_state.state)
    print("\n")


def max_records_duck(puzzle_duck):
    print("\nSolving Duck-puzzle using the MAX of both HEURISTICS:")
    start_time = time.time()
    final_state = astar_search_modified_duck(puzzle_duck, puzzle_duck.max_misplaced_and_manhattan_duck, True)
    elapsed_time = time.time() - start_time

    print("Total running time:", elapsed_time, "seconds")
    print("Total length of the solution:", final_state.path_cost)
    print("Final state")
    display_duck(final_state.state)
    print("\n")


def compare_algorithms_duck():
    randomPuzzles_duck = []
    for i in range(10):
        puzzle = make_rand_duckpuzzle()
        randomPuzzles_duck.append(puzzle)
    for j in range(10):
        print("\nRandom puzzle:", j + 1)
        print("Initial state")
        display_duck(randomPuzzles_duck[j].initial)

        heuristic_records_duck(randomPuzzles_duck[j])

        manhattan_records_duck(randomPuzzles_duck[j])

        max_records_duck(randomPuzzles_duck[j])


compare_algorithms_duck()

""" Help taken from notes, tutorial, python tutorial docs, code taken from aima-python and search.py"""