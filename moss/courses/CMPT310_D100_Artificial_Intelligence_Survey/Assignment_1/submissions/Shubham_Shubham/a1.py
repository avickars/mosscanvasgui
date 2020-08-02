# a1.py
from search import *
import random
import time

""" References:
 https://docs.python.org/3/tutorial/
 https://docs.python.org/3/library/random.html?highlight=random#module-random
 https://docs.python.org/3/library/stdtypes.html?highlight=tuple#tuple
 https://docs.python.org/3/tutorial/introduction.html#lists
 https://www.andrew.cmu.edu/course/15-121/labs/HW-7%20Slide%20Puzzle/lab.html
 
 
"""


# Question 1: Helper Functions

# Creates an initial random puzzle using random sample as the data is used without replacement.
# Checks the solvability of the puzzle using check_solvability fuction from inherited Eight puzzle class.
# If the puzzle is not solvable create the random puzzle again until the puzzle becomes solvable.
# return the solvable puzzle.


def make_rand_8puzzle():
    randomPuzzleTuple = tuple(random.sample(range(9), k=9))
    puzzleObject = EightPuzzle(randomPuzzleTuple, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))

    condition = puzzleObject.check_solvability(puzzleObject.initial)
    while not condition:
        randomPuzzleTuple = tuple(random.sample(range(9), k=9))
        puzzleObject.initial = randomPuzzleTuple
        condition = puzzleObject.check_solvability(puzzleObject.initial)

    return puzzleObject


def display(state):
    list1 = list(state)
    for i in range(len(list1)):
        if state[i] == 0:
            list1[i] = "*"
    list2 = [list1[0], " ", list1[1], " ", list1[2], "\n", list1[3], " ", list1[4], " ", list1[5], "\n", list1[6], " ",
             list1[7], " ", list1[8]]
    print(*list2, sep="")


# Question 2: Comparing Algorithms

# Extracted from search.py
class EightPuzzle(Problem):
    # The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    # squares is a blank. A state is represented as a tuple of length 9, where  element at
    # index i represents the tile number  at index i (0 if it's an empty square) 

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        # Define goal state and initialize a problem 
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        # Return the index of the blank square in a given state

        return state.index(0)

    def actions(self, state):
        # Return the actions that can be executed in the given state.
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
        # Given state and action, return a new state that is the result of the action.
        # Action is assumed to be a valid action in the state. 

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        # Given a state, return True if state is a goal state or False, otherwise.

        return state == self.goal

    def check_solvability(self, state):
        # Checks if the given state is solvable 

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
    # Return the heuristic value for a given state. Default heuristic function used is
    # h(n) = number of misplaced tiles 

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    # Extracted from search.ipnynb file
    # Calculates Manhattan distance heuristic
    def manhattan(self, node):

        state = node.state
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        i, j = 0, 0
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        mhd = 0
        for i in range(9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        return mhd

    # Returns max of manhattan and misplaced tile heuristic value
    # Extracted from search.ipnynb file
    def max_h_manhattan(self, node):
        value_misplaced = self.h(node)
        value_manhattan = self.manhattan(node)
        return max(value_misplaced, value_manhattan)


# Extracted from search.py and added a counter to calculate the number of removed nodes.
def best_first_search(problem, f, display=False):
    # Search the nodes with the lowest f scores first.
    # You specify the function f(node) that you want to minimize; for example,
    # if f is a heuristic estimate to the goal, then we have greedy best
    # first search; if f is node.depth then we have breadth-first search.
    # There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    # values will be cached on the nodes as they are computed. So after doing
    # a best first search you can examine the f values of the path returned.
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    counter = 0
    while frontier:
        node = frontier.pop()
        counter += 1
        if problem.goal_test(node.state):
            if display:
                print("that total number of nodes that were removed from frontier:\t", counter)
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


# Extracted from the search.py but the display value was done true in order to call the  modified best_first_search fxn
def a_star(problem, h=None, display=True):
    # A* search is best-first graph search with f(n) = g(n)+h(n).
    # You need to specify the h function when you call a_star_search, or
    # else in your Problem subclass
    h = memoize(h or problem.h, 'h')
    return best_first_search(problem, lambda n: n.path_cost + h(n), display)


# Creates and returns 12 random Eight puzzle instances
def create_puzzle_instance():
    puzzleInstances = []
    for i in range(12):
        generate_puzzle = make_rand_8puzzle()
        puzzleInstances.append(generate_puzzle)
    return puzzleInstances


# Calculates the time taken and length calculated by path cost inbuilt function in search.py to reach the goal.
# prints both time and length.
def running_time(puzzles, puzzles1):
    start_time = time.time()
    goal = a_star(puzzles, puzzles1)
    total_running_time = time.time() - start_time
    print("the total running time in seconds:\t ", total_running_time)
    print("the length (i.e. number of tiles moved) of the solution:\t", goal.path_cost)
    print("\n\n")
    return goal


# Compares the puzzle instances using A* search algorithm using 3 different scnerios.
def comparing_puzzle_instances():
    puzzles = create_puzzle_instance()

    for i in range(len(puzzles)):
        print("Puzzle", i + 1, ':')
        print("Initial State : ")
        display(puzzles[i].initial)
        print("\n")

        # Using the misplaced tile heuristic(this is the default heuristic in the EightPuzzle class)
        print("misplaced tile Heuristic: ")
        running_time(puzzles[i], puzzles[i].h)

        # Using Manhattan Distance
        print("Manhattan distance Heuristic: ")
        running_time(puzzles[i], puzzles[i].manhattan)

        # Using Max of Manhattan and Default
        print("Max of the misplaced tile heuristic and the Manhattan distance heuristic:")
        goal = running_time(puzzles[i], puzzles[i].max_h_manhattan)

        print("Goal State : ")
        display(goal.state)
        print('\n')


comparing_puzzle_instances()

# Question 3

class DuckPuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    # extracted from search.py and modified.
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        # evaluated by calculating the impossible moves
        # for example 0,1,4,5 indexes can not move in the upward direction in the puzzle.
        move_up = [0, 1, 4, 5]
        move_down = [2, 6, 7, 8]
        move_left = [0, 2, 6]
        move_right = [1, 5, 8]

        if index_blank_square in move_up:
            possible_actions.remove('UP')
        if index_blank_square in move_down:
            possible_actions.remove('DOWN')
        if index_blank_square in move_left:
            possible_actions.remove('LEFT')
        if index_blank_square in move_right:
            possible_actions.remove('RIGHT')

        return possible_actions

    # Extracted from search.py
    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state

        +--+--+
        |U |U |
        +--+--+--+--+
        |U |M |L |L |
        +--+--+--+--+
           |L |L |L |
           +--+--+--+

        the puzzle is divided into three parts U, M, L as shown in the diagram.

        """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        U = [0, 1, 2]
        M = [3]
        L = [4, 5, 6, 7, 8]

        delta_U = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        delta_M = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        delta_L = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        if blank in U:
            neighbor = blank + delta_U[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank in M:
            neighbor = blank + delta_M[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank in L:
            neighbor = blank + delta_L[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

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

    def manhattan(self, node):

        state = node.state
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        i, j = 0, 0
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        mhd = 0
        for i in range(9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        return mhd

    # Returns max of manhattan and misplaced tile heuristic value
    # Extracted from search.ipnynb file
    def max_h_manhattan(self, node):
        value_misplaced = self.h(node)
        value_manhattan = self.manhattan(node)
        return max(value_misplaced, value_manhattan)


def a_star_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call a_star_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_search(problem, lambda n: n.path_cost + h(n), display)


def best_first_search(problem, f, display=False):
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
    counter = 0
    while frontier:
        node = frontier.pop()
        counter += 1
        if problem.goal_test(node.state):
            if display:
                print("that total number of nodes that were removed from frontier:\t", counter)
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    print("that total number of nodes that were removed from frontier:\t", counter)
    return node


def make_rand_duckpuzzle():
    randomPuzzleTuple = tuple(random.sample(range(9), k=9))
    puzzleObject = DuckPuzzle(randomPuzzleTuple, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))

    condition = puzzleObject.check_solvability(puzzleObject.initial)
    while not condition:
        randomPuzzleTuple = tuple(random.sample(range(9), k=9))
        puzzleObject.initial = randomPuzzleTuple
        condition = puzzleObject.check_solvability(puzzleObject.initial)

    return puzzleObject


def display_duckpuzzle(state):
    list1 = list(state)
    for i in range(len(list1)):
        if state[i] == 0:
            list1[i] = "*"
    list2 = [list1[0], " ", list1[1], "\n", list1[2], " ", list1[3], " ", list1[4], " ", list1[5], "\n  ", list1[6], " ",
             list1[7], " ", list1[8]]
    print(*list2, sep="")


def create_duckpuzzle_instance():
    puzzleInstances = []
    for i in range(12):
        generate_puzzle = make_rand_duckpuzzle()
        puzzleInstances.append(generate_puzzle)
    return puzzleInstances


# Calculates the time taken and length calculated by path cost inbuilt function in search.py to reach the goal.
# prints both time and length.
def running_time(puzzles, puzzles1):
    start_time = time.time()
    goal = a_star_search(puzzles, puzzles1)

   #while goal is None:
    #   puzzle = make_rand_duckpuzzle()
     #  goal = a_star_search(puzzle, puzzles1)

    total_running_time = time.time() - start_time
    print("the total running time in seconds:\t ", total_running_time)
    print("the length (i.e. number of tiles moved) of the solution:\t", goal.path_cost)
    print("\n\n")
    return goal


# Compares the puzzle instances using A* search algorithm using 3 different scnerios.
def comparing_duckpuzzle_instances():
    puzzles = create_duckpuzzle_instance()

    for i in range(len(puzzles)):
        print("Puzzle", i + 1, ':')
        print("Initial State : ")
        display_duckpuzzle(puzzles[i].initial)
        print("\n")

        # Using the misplaced tile heuristic(this is the default heuristic in the EightPuzzle class)
        print("misplaced tile Heuristic: ")
        running_time(puzzles[i], puzzles[i].h)

        # Using Manhattan Distance
        print("Manhattan distance Heuristic: ")
        running_time(puzzles[i], puzzles[i].manhattan)

        # Using Max of Manhattan and Default
        print("Max of the misplaced tile heuristic and the Manhattan distance heuristic:")
        goal = running_time(puzzles[i], puzzles[i].max_h_manhattan)

        print("Goal State : ")
        display_duckpuzzle(goal.state)
        print('\n')


comparing_duckpuzzle_instances()


