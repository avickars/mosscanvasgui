# a1.py

from search import *
import random
import time

# --------------------------------------------------------------------------------
def astar_search_duck(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def astar_searchManhattan_duck(problem, h=None, display=False):
    h = memoize(h or problem.manhattan_duck, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def astar_searchMax_duck(problem, h=None, display=False):
    h = memoize(h or problem.max_hueristic_duck, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
# -------------------------------------------------------------------------------
# duckpuzzle

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

        if index_blank_square % 2 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square % 4 == 3:
            possible_actions.remove('RIGHT')
        if index_blank_square < 4:
            possible_actions.remove('UP')
        if index_blank_square > 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
       Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
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

    def manhattan_duck(self, node):
        state = node.state
        index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3], 5: [1, 0], 6: [1, 1], 7: [1, 2], 8: [1, 3],
                      9: [2, 0], 10: [2, 1], 11: [2, 2]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhd = 0

        for i in range(11):
            for j in range(3):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

        return mhd

    def max_hueristic_duck(self, node):
        misplace = self.h(node)
        manhat = self.manhattan(node)

        if misplace > manhat:
            return misplace
        else:
            return manhat
# ______________________________________________________________________________
# Informed (Heuristic) Search

greedy_best_first_graph_search = best_first_graph_search

# Greedy best-first search is accomplished by specifying f(n) = h(n).

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def astar_searchManhattan(problem, h=None, display=False):
    h = memoize(h or problem.manhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def astar_searchMax(problem, h=None, display=False):
    h = memoize(h or problem.max_hueristic, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
# ______________________________________________________________________________
# A* heuristics

class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def best_first_graph_search(problem, f, display=False):
        """Search the nodes with the lowest f scores first.
        You specify the function f(node) that you want to minimize; for example,
        if f is a heuristic estimate to the goal, then we have greedy best
        first search; if f is node.depth then we have breadth-first search.
        There is a subtlety: the line "f = memoize(f, 'f')" means that the f
        values will be cached on the nodes as they are computed. So after doing
        a best first search you can examine the f values of the path returned."""
        count_pop = 0
        f = memoize(f, 'f')
        node = Node(problem.initial)
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        explored = set()
        while frontier:
            node = frontier.pop()
            count_pop += 1
            if problem.goal_test(node.state):
                if display:
                    print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                return node
                return count_pop
            explored.add(node.state)
            for child in node.expand(problem):
                if child.state not in explored and child not in frontier:
                    frontier.append(child)
                elif child in frontier:
                    if f(child) < frontier[child]:
                        del frontier[child]
                        frontier.append(child)
        return None, count_pop

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

    def manhattan(self, node):
        state = node.state
        index_goal = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1], 0: [2, 2]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhd = 0

        for i in range(8):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

        return mhd

    def max_hueristic(self, node):
        misplace = self.h(node)
        mhd = self.manhattan(node)

        if misplace > mhd:
            return misplace
        else:
            return mhd
# -----------------------------------------------------------------

def make_rand_8puzzle():
    # create a list of numbers
    puzzle = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    # randomly select one from the list
    state = random.sample(puzzle, 9)
    new_state = (state[0], state[1], state[2], state[3], state[4], state[5], state[6], state[7], state[8])
    state = EightPuzzle(new_state)
    return state

def display(state):
    for i in range(0, 9):
        if i % 3 == 0:
            print("")

        if state[i] != 0:
            print(state[i], " ", end="")

        else:
            print("* ", end=" ")

def duckpuzzle():
    # create a list of numbers
    duck_puzzle = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    # randomly select one from the list
    duckstate = random.sample(duck_puzzle, 9)
    ducknew_state = (
    duckstate[0], duckstate[1], duckstate[2], duckstate[3], duckstate[4], duckstate[5], duckstate[6], duckstate[7],
    duckstate[8])
    duckstate = DuckPuzzle(ducknew_state)
    return state


def display_duck(duckstate):
    # for each value in state
    for i in range(len(duckstate)):
        if duckstate[i] == 0:
            duckstate = list(duckstate)
            duckstate[i] = "*"
            duckstate = tuple(duckstate)

    print(duckstate[0], duckstate[1])
    print(duckstate[2], duckstate[3], duckstate[4], duckstate[5])
    print(" ", duckstate[6], duckstate[7], duckstate[8])


# main method
if __name__ == "__main__":
    state = make_rand_8puzzle()

    print("\nHere is the initial state of the 8-puzzle")
    display(state.initial)

    print("\nHere is the goal state of the 8-puzzle")
    display(state.goal)

    duckystate = duckpuzzle()

    print("\n\nHere is the initial state of the Duck-puzzle")
    display_duck(duckystate.initial)

    print('\n' + "Here is the goal state of the Duck-puzzle")
    display_duck(duckystate.goal)

    t1 = time.time()

    man = astar_searchManhattan(state)
    print("\nLength of solution for manhattan for 3x3:", len(man.path()))

    t2 = time.time()

    print('\n' + "Time taken for Manhattan Distance hueristic for 3x3: " + str(t2 - t1))

    t3 = time.time()

    node = astar_search(state)
    print("\nLength of solution for misplaced for 3x3: ", len(node.path()))

    t4 = time.time()

    print('\n' + "Time taken for Misplaced Tile hueristic for 3x3: " + str(t4 - t3))

    t5 = time.time()

    maxi = astar_searchMax(state)
    print("\nLength of solution for max for 3x3: ", len(maxi.path()))

    t6 = time.time()

    print('\n' + "Time taken for Max hueristic for 3x3: " + str(t6 - t5))
