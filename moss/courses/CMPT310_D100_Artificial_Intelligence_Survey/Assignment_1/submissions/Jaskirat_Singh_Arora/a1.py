from search import *
import random
import time

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
    removed_nodes = 0 # number of nodes removed
    while frontier:
        node = frontier.pop()
        removed_nodes += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, removed_nodes]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def manhattan_h(node):
    """Implementing the Manhattan Distance Heuristic for both the EightPuzzle and HousePuzzle
        Code reference from test_search.py for correct formula"""

    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    for k in range(len(state)):
        index_state[state[k]] = index[k]

    mhd = 0

    for i in range(9):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd  # formula for Manhattan Distance

    return mhd

def max_h(node):
    """Return the max value between the Manhattan Distance heuristic
        and the Misplaced Tile heuristic"""

    puzzle = EightPuzzle(node.state)
    MisplacedTiles = puzzle.h(node)
    ManhattanDist = manhattan_h(node)
    return max(MisplacedTiles, ManhattanDist)


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

        return sum(s != g for (s, g) in zip(node.state, self.goal))


# Question 1-------------------------------------------------------------------------------------------------------


def make_rand_8puzzle():
    """Generate random 8 puzzle which is solvable (valid)"""

    puzzle_set = {}
    puzzle = []
    flag = 0
    while flag == 0:
        puzzle_set = tuple(random.sample(range(0, 9), 9))
        puzzle = EightPuzzle(puzzle_set, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))
        flag = puzzle.check_solvability(puzzle_set)
    else:
        return puzzle

def display(state):
    """Display the 8puzzle in the format of a 3x3 matrix"""

    index = 0
    array = ""
    for ii in range(len(state)):
        if state[index] == 0:
            array = array + '*'
        else:
            array += str(state[index])
        index = index + 1

    index = 0
    for ii in range(3):
        print(array[index] + " " + array[index + 1] + " " + array[index + 2])
        index = index + 3

    print('')

#Question 2------------------------------------------------------------------------------------------------------------


def run(puzzle, heuristic):
    #The function to run A* Search and record time, length and removed nodes for all the three heuristics

    start_time = time.time()

    result = astar_search(puzzle, heuristic)

    elapsed_time = time.time() - start_time

    print(f'Elapsed time (in seconds): {elapsed_time}s')
    print('Length (number of tiles moved): ' + str(result[0].path_cost))
    print(f'Number of nodes removed: {result[1]} \n')
    return puzzle


def eight_puzzle_analyzer():
    """This function helps in analysis of 10 instances of random solvable eight puzzle"""

    puzzles = []  # Create an empty array of puzzles
    for i in range(10):
        puzzles.append(make_rand_8puzzle())

    for i in range(len(puzzles)):
        print(f"\n8puzzle in 3x3: {i + 1}")
        display(puzzles[i].initial)

        print("Misplaced Tiles Heuristic...")
        run(puzzles[i], puzzles[i].h)

        print("Manhattan Distance Heuristic...")
        run(puzzles[i], manhattan_h)

        print("Maximum Heuristic...")
        run(puzzles[i], max_h)

        print("")


#eight_puzzle_analyzer()  # run the algorithm for 8Puzzle


#Question 3-----------------------------------------------------------------------------------------------------------

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

        UP = (0, 1, 4, 5)  # Tuples that can't move UP
        DOWN = (2, 6, 7, 8)  # Tuples that can't move DOWN
        LEFT = ( 0, 2, 6)  # Tuples that can't move LEFT
        RIGHT = (1, 5, 8)  # Tuples that can't move RIGHT

        if index_blank_square in LEFT:
            possible_actions.remove('LEFT')
        if index_blank_square in UP:
            possible_actions.remove('UP')
        if index_blank_square in RIGHT:
            possible_actions.remove('RIGHT')
        if index_blank_square in DOWN:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        """
                    +--+--+
                    |0 | 1|
                    +--+--+--+--+
                    |2 |3 |4 |5 |
                    +--+--+--+--+
                       | 6| 7| 8|
                       +--+--+--+

            """

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        Exception1 = (2,3)
        deltaException1 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        Exception2 = (0,1)
        deltaException2 = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}

        if blank in Exception1:
            neighbor = blank + deltaException1[action]
        elif blank in Exception2:
            neighbor = blank + deltaException2[action]
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


def make_rand_duck_puzzle():
    """Generate solvable random duck puzzle """
    puzzle_set = {}
    puzzle = []
    flag = 0
    while flag == 0:
        puzzle_set = tuple(random.sample(range(0, 9), 9))
        puzzle = EightPuzzle(puzzle_set, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))
        flag = puzzle.check_solvability(puzzle_set)
    else:
        return puzzle

def display_duck(state):
    """This function displays the duck puzzle in the required format"""
    # This step removes the 0 and replaces it with *
    index = 0
    array = ""
    for ii in range(len(state)):
        if state[index] == 0:
            array = array + '*'
        else:
            array += str(state[index])
        index = index + 1

    # This step displays in the correct format
    index = 0
    print(array[index] + " " + array[index + 1])
    index = index + 2
    print(array[index] + " " + array[index + 1]+ " " + array[index+2]+ " " + array[index+3])
    index = index + 4
    print("  " + array[index] + " " + array[index + 1] + " " + array[index + 2])

    print('')

def duck_puzzle_analyzer():
    """ This function analyzes 10 instances of solvable random Duck Puzzle """

    puzzles = []  # Create an empty array of puzzles
    for i in range(10):
            puzzles.append(make_rand_duck_puzzle())

    for i in range(len(puzzles)):
        print(f"\n8puzzle in its proper format: {i + 1}")
        display_duck(puzzles[i].initial)

        print("Misplaced Tiles Heuristic...")
        run(puzzles[i], puzzles[i].h)

        print("Manhattan Distance Heuristic...")
        run(puzzles[i], manhattan_h)

        print("Maximum Heuristic...")
        run(puzzles[i], max_h)

    print('')

duck_puzzle_analyzer()

#----------------------------------------------------------------------------------------------------------------------