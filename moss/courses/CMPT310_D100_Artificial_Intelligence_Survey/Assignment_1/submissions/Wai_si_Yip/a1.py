# a1.def ():

from search import *
import time
import random


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

        # Refer the idea from test_search.py but modify some section
    def manhatten_h(self, node):
        state = node.state  # store all the movement
        goal = {1: [0, 0], 2: [0, 1], 3: [0, 2],
                4: [1, 0], 5: [1, 1], 6: [1, 2],
                7: [2, 0], 8: [2, 1], 0: [2, 2]}
        stateIndex = {}
        index = [[0, 0], [0, 1], [0, 2],
                 [1, 0], [1, 1], [1, 2],
                 [2, 0], [2, 1], [2, 2]]
        cost = 0
        # source learn from
        # https://www.youtube.com/watch?v=GuCzYxHa7iA&t=188s
        for i in range(len(state)):
            # give the 3x3 matrix have [horizontal,vertical] cost
            stateIndex[state[i]] = index[i]

        for i in range(8):
            for j in range(2):
                cost = abs(goal[i][j] - goal[i][j]) + cost

        return cost
# ------------------------------------------------Q1----------------------------------------
# return new instance of 8puzzle
# random inital state
# use check_solvability(self, state)


def make_rand_8puzzle():
    instance = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while 1:
        puzzle = EightPuzzle(random.shuffle(instance))
        if puzzle.check_solvability(instance):
            # able to solve
            break
    return tuple(instance)

# * ,1 ,2
# 3 ,4 ,5
# 6 ,7 ,8


def display(state):
    for i in range(0, 3):
        if(state[i] == 0):
            print("*", end=" ")
        else:
            print(state[i], end=" ")

    print("")
    for i in range(3, 6):
        if(state[i] == 0):
            print("*", end=" ")
        else:
            print(state[i], end=" ")
    print("")
    for i in range(6, 9):
        if(state[i] == 0):
            print("*", end=" ")
        else:
            print(state[i], end=" ")
    print("")


def question1():
    starting_state = make_rand_8puzzle()
    puzzle = EightPuzzle(starting_state)
    current_state = puzzle.initial
    display(current_state)

# ------------------------------------------------Q2----------------------------------------

# Create 10 puzzles

# record in spreadsheet, excel a1.xlsx
# include min, max, avge, median
# graph

# 1. total running times in second
# 2. count of movement
# 3. total number of nodes removed from frontier

# which algorithms is the best?
# 1. misplaced tile heuristic ( in EightPuzzle class)
# 2. Manhattan distance heuristic <<write on my own>>
# 3. Max of (1) (2)


def ten_puzzle():
    for i in range(1, 11):
        print("Puzzle:", i)
        print("-----------")
        starting_state = make_rand_8puzzle()
        puzzle = EightPuzzle(starting_state)
        current_state = puzzle.initial
        display(current_state)
        print("")
        runTime(puzzle)


def runTime(state):
    print("Run Time <Misplaced Tile Heuristic>")
    start = time.time()
    removeNum = astar_search(state, display=True)
    end = time.time() - start
    print("Used:", end, "s")
    print("Cost:", removeNum, "moves")
    print("========FINISH========")
    print("\n")

    print("Run Time <Manhattan Distance Heuristic>")
    start = time.time()
    removeNum = aster_search_manhatten(state, display=True)
    end = time.time() - start
    print("Used:", end, "s")
    print("Cost:", removeNum, "moves")
    print("========FINISH========")
    print("\n")

# Citeation: serach.py + utils.py
# (1)astar_search (2)best_first_graph_search


def best_first_graph_search(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    counter = 0
    while frontier:
        node = frontier.pop()
        counter = counter + 1
        if problem.goal_test(node.state):
            if display:    # Changed section
                print("Number of removed node:", counter)
                # refer to the class Node
                # path(self) mathod
            return len(node.path())
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

# seraching


def astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def aster_search_manhatten(problem, h=None, display=False):
    h = memoize(h or problem.manhatten_h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


    # ------------------------------------------------Q3----------------------------------------
    # new problem class -> DuckPuzzle
    #       1 2 _ _
    #       3 4 5 6
    #       _ 7 8 *
    # duck-puzzle v.s 8 puzzle , which is harder ?
    # ------------------------------------------------MAIN----------------------------------------
if __name__ == '__main__':
    # question1()
    ten_puzzle()
    # ...
