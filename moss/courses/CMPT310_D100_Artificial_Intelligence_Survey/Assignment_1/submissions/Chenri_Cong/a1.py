# a1.py
# Name: Chenri Cong     Student ID： 301243458    SFU Email: chenric@sfu.ca
# Help: Zheng Zhou (Manhattan heuristic  array)

import time
import random
import numpy
from utils import memoize, PriorityQueue
from search import Problem, Node


Manhattan_8pz = numpy.array([[4, 3, 2, 3, 2, 1, 2, 1, 0],
                             [0, 1, 2, 1, 2, 3, 2, 3, 4],
                             [1, 0, 1, 2, 1, 2, 3, 2, 3],
                             [2, 1, 0, 3, 2, 1, 4, 3, 2],
                             [1, 2, 3, 0, 1, 2, 1, 2, 3],
                             [2, 1, 2, 1, 0, 1, 2, 1, 2],
                             [3, 2, 1, 2, 1, 0, 3, 2, 1],
                             [2, 3, 4, 1, 2, 3, 0, 1, 2],
                             [3, 2, 3, 2, 1, 2, 1, 0, 1]])

Manhattan_Hpz = numpy.array([[5, 4, 4, 3, 2, 1, 2, 1, 0],
                             [0, 1, 1, 2, 3, 4, 3, 4, 5],
                             [1, 0, 2, 1, 2, 3, 2, 3, 4],
                             [1, 2, 0, 1, 2, 3, 2, 3, 4],
                             [2, 1, 1, 0, 1, 2, 1, 2, 3],
                             [3, 2, 2, 1, 0, 1, 2, 1, 2],
                             [4, 3, 3, 2, 1, 0, 3, 2, 1],
                             [3, 2, 2, 1, 2, 3, 0, 1, 2],
                             [4, 3, 3, 2, 1, 2, 1, 0, 1]])


def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    node_removed = 0
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        node_removed += 1
        if problem.goal_test(node.state):
            return node, node_removed
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def astar_manhattan_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(problem.h_manhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def astar_max_manhattan_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(problem.h_maxManhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """

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

    def h_manhattan(self, node):
        """ Return the heuristic value for a given state. This heuristic function used is
        h(n) = sum of Manhattan distance """

        # First index finds the right colon, second index finds the distance from goal
        return sum(Manhattan_8pz[node.state[i]][i] for i in node.state)

    def h_maxManhattan(self, node):
        return self.h(node) + self.h_manhattan(node)

    def display(self, state):
        """ Prints a neat and readable representation of state """
        for i in range(0, 3):
            for j in range(0, 3):
                if (state[(3 * i) + j] == 0):
                    print("* ", end=" ")
                else:
                    print(str(state[(3 * i) + j]) + " ", end=" ")
            print("")


def make_rand_8puzzle():
    """ Returns a new instance of an EightPuzzle problem with a random initial
    state that is solvable """
    tiles = list(range(0, 9))
    random.shuffle(tiles)
    puzzle = EightPuzzle(tuple(tiles))
    while (not puzzle.check_solvability(puzzle.initial)):
        random.shuffle(tiles)
        puzzle = EightPuzzle(tuple(tiles))
    return puzzle


def Question1():
    for i in range (0,10):
        test = make_rand_8puzzle()
        print("\nPuzzle", " ", i + 1, ": \n")
        test.display(test.initial)






def Question2():
    for i in range(0, 10):
        print("============================== 8 Puzzle " + str(i + 1) + " ===============================")
        test = make_rand_8puzzle()
        test.display(test.initial)
        start_time = time.time()
        default_search, default_node_removed = astar_search(test)
        elapsed_time = time.time() - start_time
        default_solution_len = len(default_search.solution())
        print("\n=========================== Default Heuristic ===========================")
        print("Total running time: " + str(elapsed_time) + " seconds")
        print("Length of the solution: " + str(default_solution_len) + " steps")
        print("Problem solved with default heuristic with " + str(default_node_removed) + " nodes removed")

        start_time = time.time()
        manhattan_search, manhattan_node_removed = astar_manhattan_search(test)
        elapsed_time = time.time() - start_time
        manhattan_solution_len = len(manhattan_search.solution())
        print("\n========================== Manhattan Heuristic ==========================")
        print("Total running time: " + str(elapsed_time) + " seconds")
        print("Length of the solution: " + str(manhattan_solution_len) + " steps")
        print("Problem solved with Manhattan heuristic with " + str(manhattan_node_removed) + " nodes removed")

        start_time = time.time()
        max_manhattan_search, max_manhattan_node_removed = astar_max_manhattan_search(test)
        elapsed_time = time.time() - start_time
        max_manhattan_solution_len = len(max_manhattan_search.solution())
        print("\n========================== Max misplaced tile Manhattan Heuristic with max mixplcaed tiles==========================")
        print("Total running time: " + str(elapsed_time) + " seconds")
        print("Length of the solution: " + str(max_manhattan_solution_len) + " steps")
        print("Number of nodes removed: " + str(max_manhattan_node_removed) + " nodes removed\n")

class HPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a Y shaped board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """

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

        if index_blank_square in [0,  2, 6]:
            possible_actions.remove('LEFT')
        if index_blank_square in [0, 1,4,5]:
            possible_actions.remove('UP')
        if index_blank_square in [1,5,8]:
            possible_actions.remove('RIGHT')
        if index_blank_square in [2,6,7,8]:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank in [0, 1]:
            delta = {'DOWN': 2,'UP': 0, 'LEFT': -1, 'RIGHT': 1}
        elif blank in [2, 5]:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """
        return True

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def h_manhattan(self, node):
        """ Return the heuristic value for a given state. This heuristic function used is
        h(n) = sum of Manhattan distance """

        # First index finds the right colon, second index finds the distance from goal
        return sum(Manhattan_Hpz[node.state[i]][i] for i in node.state)

    def h_maxManhattan(self, node):
        return max(self.h(node), self.h_manhattan(node))

    def display(self, state):
        """ Prints a neat and readable representation of state """
        for i in range(len(state)):
            if i == 0 or i == 2 or i == 3 or i == 4 or i == 7:
                if state[i] == 0:
                    print ("*  " ,end="")
                else:
                    print(state[i], " ", end="")
            if i == 1:
                if state[i] == 0:
                    print("*", end= "  \n")
                else:
                    print (state[i], end= "  \n")
            if i == 5 or i == 8:
                if state[i] == 0:
                    print("*")
                else:
                    print (state[i])
            if i == 6:
                if state[i] == 0:
                    print("   ",  end="")
                    print("*  ",end="")
                else:
                    print ("   ", end = "")
                    print (state[i]," ", end = "")





def make_rand_Hpuzzle():
    """ Returns a new instance of an EightPuzzle problem with a random initial
    state that is solvable """
    tiles = list(range(0, 9))
    puzzle = HPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))

    for i in range (0,3000):
        puzzle.initial = puzzle.result(puzzle.initial,random.choice(puzzle.actions(puzzle.initial)))

    return puzzle



def Question3():
    for i in range(0, 10):
        print("============================== House Puzzle " + str(i + 1) + " ===============================")
        test = make_rand_Hpuzzle()
        test.display(test.initial)
        start_time = time.time()
        default_search, default_node_removed = astar_search(test)
        elapsed_time = time.time() - start_time
        default_solution_len = len(default_search.solution())
        print("\n=========================== Default Heuristic ===========================")
        print("Total running time: " + str(elapsed_time) + " seconds")
        print("Length of the solution: " + str(default_solution_len) + " steps")
        print("Number of nodes removed: " + str(default_node_removed) + " nodes removed")

        start_time = time.time()
        manhattan_search, manhattan_node_removed = astar_manhattan_search(test)
        elapsed_time = time.time() - start_time
        manhattan_solution_len = len(manhattan_search.solution())
        print("\n========================== Manhattan Heuristic ==========================")
        print("Total running time: " + str(elapsed_time) + " seconds")
        print("Length of the solution: " + str(manhattan_solution_len) + " steps")
        print("Number of nodes removed: " + str(manhattan_node_removed) + " nodes removed")

        start_time = time.time()
        max_manhattan_search, max_manhattan_node_removed = astar_max_manhattan_search(test)
        elapsed_time = time.time() - start_time
        max_manhattan_solution_len = len(max_manhattan_search.solution())
        print("\n========================== Manhattan Heuristic with max misplaced tiles==========================")
        print("Total running time: " + str(elapsed_time) + " seconds")
        print("Length of the solution: " + str(max_manhattan_solution_len) + " steps")
        print("Number of nodes removed: " + str(max_manhattan_node_removed) + " nodes removed\n")

if __name__ == '__main__':
    Question1()
    #Question2()
    #Question3()
