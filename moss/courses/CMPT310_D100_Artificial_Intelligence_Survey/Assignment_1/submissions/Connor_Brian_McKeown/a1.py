# a1.py

from search import *
import random
import time
# import pandas as pd


# Duck Puzzle Class
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

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if action == 'UP' and (blank == 2 or blank == 3):  # blank in second row
            action = 'UP_2'
        elif action == 'UP':                                            # blank in third row
            action = 'UP_3'

        if action == 'DOWN' and (blank == 0 or blank == 1):  # blank in first row
            action = 'DOWN_1'
        elif action == 'DOWN':                                              # blank in second row
            action = 'DOWN_2'

        delta = {'UP_2': -2, 'UP_3': -3, 'DOWN_1': 2, 'DOWN_2': 3, 'LEFT': -1, 'RIGHT': 1}  # 3
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]  # swap

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))





# Overriding best_first_graph_search() in order to return the # of nodes removed from the frontier
def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    nodes_removed = 0 # added line
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
            # return node
            return (node.path_cost, nodes_removed)  # (length, nodes_removed)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    nodes_removed += 1  # added line
                    frontier.append(child)
    return None



# From aima-python
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


#astar_search with added max lamba for max heuristic
def astar_search_max(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + max(problem.h(n), manhattan_h(n)), display)

#astar_search with added max lamba for max heuristic
def astar_search_max_duck(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + max(problem.h(n), duck_manhattan_h(n)), display)

# Generates a random solvable state
def rand_state():
    t = tuple(range(9))
    state = tuple(random.sample(t, len(t)))
    while EightPuzzle(state).check_solvability(state) is False:
        state = tuple(random.sample(t, len(t)))
    return state


# prints the state to the console in a 3x3 grid
def display(state):
    next_row = 0
    for i in range(9):
        if (next_row == 3):
            next_row = 0
            print()
        if (state[i] == 0):
            print("*", end=" ")
        else:
            print(state[i], end=" ")
        next_row += 1
    print()

def display_duck(state):
    for i in range(9):
        if i == 2:
            print()
        elif i == 6:
            print()
            print(" ", end=" ")

        if state[i] == 0:
            print("*", end=" ")
            continue

        if (i < 2):
            print(state[i], end=" ")
        elif (i < 6):
            print(state[i], end=" ")
        else:
            print(state[i], end=" ")
    print()

def make_rand_8puzzle():
    # state = (0, 3, 2, 1, 8, 7, 4, 6, 5)
    state = rand_state()
    # display(state)
    # new instance of eightpuzzle
    instance = EightPuzzle(state)
    return instance

def make_rand_duck():
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    instance = DuckPuzzle(state)

    n = 1000
    for i in range(n):
        actions = instance.actions(state)  # list of possible actions
        action = random.randint(0, len(actions) - 1)  # choosing a random action
        state = instance.result(state, actions[action])  # changing state based on the action

    new_instance = DuckPuzzle(state)
    return new_instance


# returns a 3-tuple (total_run_time, length, nodes_removed)
def misplaced_tile(puzzle):
    start = time.time()
    t = astar_search(puzzle, puzzle.h)
    elapsed = time.time() - start
    total_time = round(elapsed, 6)
    print((total_time,) + t)
    return (total_time,) + t

# returns a 3-tuple (total_run_time, length, nodes_removed)
def manhattan(puzzle):
    start = time.time()
    t = astar_search(puzzle, manhattan_h)
    elapsed = time.time() - start
    total_time = round(elapsed, 6)
    print((total_time,) + t)
    return (total_time,) + t

def manhattan_duck(puzzle):
    start = time.time()
    t = astar_search(puzzle, duck_manhattan_h)
    elapsed = time.time() - start
    total_time = round(elapsed, 6)
    print((total_time,) + t)
    return (total_time,) + t

# sum each tiles manhattan distance
def manhattan_h(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    mhd = 0
    for s, g in ((node.state.index(i), goal.index(i)) for i in range(1, 9)):
        mhd += abs(s % 3 - g % 3) + abs(s // 3 - g // 3)

    return mhd


# returns a 3-tuple (total_run_time, length, nodes_removed)
def max_func(puzzle):
    start = time.time()
    t = astar_search_max(puzzle, puzzle.h)
    elapsed = time.time() - start
    total_time = round(elapsed, 6)
    print((total_time,) + t)
    return (total_time,) + t

def max_func_duck(puzzle):
    start = time.time()
    t = astar_search_max_duck(puzzle, puzzle.h)
    elapsed = time.time() - start
    total_time = round(elapsed, 6)
    print((total_time,) + t)
    return (total_time,) + t


# manhattan function for duck puzzle
def duck_manhattan_h(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    mhd = 0
    for s, g in ((node.state.index(i), goal.index(i)) for i in range(1, 9)):
        mhd += abs(s % 4 - g % 4) + abs(s // 3 - g // 3)  # |x1 - x2| + |y1 - y2|

    return mhd



# list of 10 8-puzzles
n = 25
puzzles = []
while len(puzzles) < n:
    puzzles.append(make_rand_8puzzle())

misplaced_tile_tests = []
manhattan_tests = []
max_tests = []



for puzzle in puzzles:
    print("Running misplaced_tile on")
    display(puzzle.initial)
    misplaced_tile_tests.append(misplaced_tile(puzzle))

    print("Running manhattan on ")
    display(puzzle.initial)
    manhattan_tests.append(manhattan(puzzle))

    print("Running max on ")
    display(puzzle.initial)
    max_tests.append(max_func(puzzle))

"""
# write data to excel
df1 = pd.DataFrame(misplaced_tile_tests, columns=['total_run_time', 'length', 'nodes_removed'])
df2 = pd.DataFrame(manhattan_tests, columns=['total_run_time', 'length', 'nodes_removed'])
df3 = pd.DataFrame(max_tests, columns=['total_run_time', 'length', 'nodes_removed'])
"""


# duck puzzles

# n = 10
duck_puzzles = []
while len(duck_puzzles) < n:
    duck_puzzles.append(make_rand_duck())

misplaced_tile_tests = []
manhattan_tests = []
max_tests = []

for duck_puzzle in duck_puzzles:
    print("Running misplaced_tile on")
    display_duck(duck_puzzle.initial)
    misplaced_tile_tests.append(misplaced_tile(duck_puzzle))

    print("Running manhattan on ")
    display_duck(duck_puzzle.initial)
    manhattan_tests.append(manhattan_duck(duck_puzzle))

    print("Running max on ")
    display_duck(duck_puzzle.initial)
    max_tests.append(max_func_duck(duck_puzzle))

"""
df4 = pd.DataFrame(misplaced_tile_tests, columns=['total_run_time', 'length', 'nodes_removed'])
df5 = pd.DataFrame(manhattan_tests, columns=['total_run_time', 'length', 'nodes_removed'])
df6 = pd.DataFrame(max_tests, columns=['total_run_time', 'length', 'nodes_removed'])
writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
pd.concat([df1, df2, df3, df4, df5, df6], axis=1).to_excel(writer, index=False)
writer.save()
"""