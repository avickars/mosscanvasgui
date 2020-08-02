# a1.py

# from search.py
import sys
from collections import deque

from utils import *


class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


# ______________________________________________________________________________


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)


# ______________________________________________________________________________


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


def best_first_graph_search_display_frontier(problem, f, display=True):
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
                print(len(explored))
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


# ______________________________________________________________________________


# Greedy best-first search is accomplished by specifying f(n) = h(n).


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def astar_search_display_frontier(problem, h=None, display=True):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_display_frontier(problem, lambda n: n.path_cost + h(n), display)


def astar_manhattan_distance_search(problem, manhattanDistance=None, display=True):
    """A* manhattan distance heuristic value search"""
    manhattanDistance = memoize(manhattanDistance or problem.manhattanDistance, 'manhattanDistance')
    return best_first_graph_search_display_frontier(problem, lambda n: n.path_cost + manhattanDistance(n), display)

def astar_max_of_manhattan_distance_and_h_search(problem, maxValue=None, display=True):
    """A* max of manhattan distance and heuristic value search"""
    maxValue = memoize(maxValue or problem.maxValue, 'maxValue')
    return best_first_graph_search_display_frontier(problem, lambda n: n.path_cost + maxValue(n), display)


# ______________________________________________________________________________

# A* heuristics

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

    def manhattanDistanceHelper(s, g):
        if (s == 0):
            g = 9

        if (g == 0):
            s = 9

        absolueValue = abs(s-g)
        upValue = absolueValue / 3
        rowValue = absolueValue % 3 - g
        return upValue + rowValue


    def manhattanDistance(self, node):
        """ Return the Manhattan Distance heuristic value for a given state."""
        return sum( EightPuzzle.manhattanDistanceHelper(s, g)  for (s, g) in zip(node.state, self.goal))


    def maxValue(self, node):
        """ Return max value of the Manhattan Distance and heuristic value for a given state."""

        return max( sum(EightPuzzle.manhattanDistanceHelper(s, g)  for (s, g) in zip(node.state, self.goal)),
                    sum(s != g for (s, g) in zip(node.state, self.goal)))


# ______________________________________________________________________________


# A* heuristics

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

        possible_actions = ['LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square in {2, 3}:
            possible_actions.append('TopUP')

        if index_blank_square in {0, 1}:
            possible_actions.append('TopDOWN')

        if index_blank_square in {6, 7, 8}:
            possible_actions.append('BottomUP')

        if index_blank_square in {3, 4, 5}:
            possible_actions.append('BottomDOWN')

        if index_blank_square in {0, 2, 6}:
            possible_actions.remove('LEFT')

        if index_blank_square in {1, 5, 8}:
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'TopUP': -2, 'TopDOWN': 2,'BottomUP': -2, 'BottomDOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        # check top part
        blank = self.find_blank_square(state)
        if (blank < 3):
            if (blank == 0):
                return state[1] == 3 and state[2] == 2 and state[3] == 1
            elif (blank == 1):
                return state[0] == 2 and state[2] == 1 and state[3] == 3
            else: # (blank == 2)
                return state[0] == 3 and state[1] == 1 and state[3] == 2
        else:
            if (state[0] == 0 and state[1] == 1 and state[2] == 2):
                inversion = 0
                for i in range(6):
                    for j in range(i + 1, 6):
                        i_index = i + 3
                        j_index = j + 3
                        if (state[i_index] > state[j_index]) and state[i_index] != 0 and state[j_index] != 0:
                            inversion += 1

                return inversion % 2 == 0

        return 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattanDistanceHelper(s, g):
        if (s == g):
            return 0

        # s is distination
        # g is current index

        result = 0

        if g > 2: # if now it is in 1st row

            if s > 2: # if distination is in 1st row

                return 1

            elif s > 5: # if distination is in 3rd row

                result += 2 # columns

                result += abs(g - (s - 5)) # rows

                return result

            else: # if distination in 2nd row

                result += 1 # columns

                result += abs(g - (s - 1))

                return result

        elif g > 5: # if now it is in 3rd row

            if s > 2: # if distination is in 1st row

                result += 2 # columns

                result += abs((g - 5) - s) # rows

                return result

            elif s > 5: # if distination is in 3rd row

                return abs(s - g)

            else: # if distination in 2nd row

                result += 1 # columns

                result += abs((g - 5) - (s - 1)) # rows

                return result

        else: # if now it is in 2nd row

            if g > 2: # if distination is in 1st row

                result += abs((g - 1) - s) # rows

                return result

            elif g > 5: # if distination is in 3rd row

                result += abs((g - 1) - (s - 5)) # rows

                return result

            else: # if distination in 2nd row

                return abs(s - g)


    def manhattanDistance(self, node):
        """ Return the Manhattan Distance heuristic value for a given state."""
        return sum( DuckPuzzle.manhattanDistanceHelper(s, g)  for (s, g) in zip(node.state, self.goal))


    def maxValue(self, node):
        """ Return max value of the Manhattan Distance and heuristic value for a given state."""

        return max( sum(DuckPuzzle.manhattanDistanceHelper(s, g)  for (s, g) in zip(node.state, self.goal)),
                    sum(s != g for (s, g) in zip(node.state, self.goal)))

# ______________________________________________________________________________


# end of from search.py


from random import shuffle
import time
random.seed("a")

def make_rand_8puzzle():
    combinations = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    solvable = 0
    while solvable == 0:
        random.shuffle(combinations)
        solvable = EightPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0)).check_solvability(tuple(combinations))

    return tuple(combinations)


def display(state):
    for i in range(3):
        for j in range(3):
            if state[i*3+j] == 0:
                print("*", end=" ")
            else:
                print(state[i*3+j], end=" ")
        print("")

def displayQ1Result():
    print("---------------------------------------------")
    print("Q1 (a): returns a new instance of an EightPuzzle problem and:", end="\n\n")
    puzzle = make_rand_8puzzle()
    print("Q1 (b):prints a neat and readable representation of it:", end="\n\n")
    display(puzzle)
    print("---------------------------------------------")


def displayQ2Result(iterations = 1):
    for inc in range(iterations):
        print("---------------------------------------------")
        print("Trial", end=" ")
        print(inc + 1)


        puzzle = make_rand_8puzzle()
        # puzzle = (5, 0, 8, 4, 2, 1, 7, 3, 6)
        display(puzzle)

        print("---------------------------------------------")
        print("A*-search using the misplaced tile heuristic")

        start_time = time.time()

        # ... do something ...
        answer1 = astar_search(EightPuzzle(puzzle), display = False)

        elapsed_time = time.time() - start_time

        # the total running time in seconds
        print("the total running time in seconds:")
        print(elapsed_time)


        # the length (i.e. number of tiles moved) of the solution
        print("the length (i.e. number of tiles moved) of the solution:")
        # print(answer1.solution())
        print(len(answer1.solution()))


        # that total number of nodes that were removed from frontier
        print("that total number of nodes that were removed from frontier")
        astar_search_display_frontier(EightPuzzle(puzzle))

        #------------------------------------------------------------------------
        print("---------------------------------------------")
        print("A*-search using the Manhattan distance heuristic")

        start_time = time.time()

        # ... do something ...
        answer2 = astar_manhattan_distance_search(EightPuzzle(puzzle), display = False)

        elapsed_time = time.time() - start_time

        # the total running time in seconds
        print("the total running time in seconds:")
        print(elapsed_time)


        # the length (i.e. number of tiles moved) of the solution
        print("the length (i.e. number of tiles moved) of the solution:")
        # print(answer2.solution())
        print(len(answer2.solution()))


        # that total number of nodes that were removed from frontier
        print("that total number of nodes that were removed from frontier")
        astar_manhattan_distance_search(EightPuzzle(puzzle))

        #------------------------------------------------------------------------
        print("---------------------------------------------")
        print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic")

        start_time = time.time()

        # ... do something ...
        answer3 = astar_max_of_manhattan_distance_and_h_search(EightPuzzle(puzzle))

        elapsed_time = time.time() - start_time

        # the total running time in seconds
        print("the total running time in seconds:")
        print(elapsed_time)


        # the length (i.e. number of tiles moved) of the solution
        print("the length (i.e. number of tiles moved) of the solution:")
        # print(answer3.solution())
        print(len(answer3.solution()))


        # that total number of nodes that were removed from frontier
        print("that total number of nodes that were removed from frontier")
        astar_max_of_manhattan_distance_and_h_search(EightPuzzle(puzzle))
        print("---------------------------------------------")


def make_rand_house_puzzle():
    combinations = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    solvable = 0
    while solvable == 0:
        random.shuffle(combinations)
        solvable = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0)).check_solvability(tuple(combinations))

    return tuple(combinations)


def display_house_puzzle(state):

    for i in range(2):
        if state[i] == 0:
            print("*", end=" ")
        else:
            print(state[i], end=" ")

    print("")

    for i in range(4):
        i_index = i + 2
        if state[i_index] == 0:
            print("*", end=" ")
        else:
            print(state[i_index], end=" ")

    print("")

    print(" ", end=" ")

    for i in range(3):
        i_index = i + 6
        if state[i_index] == 0:
            print("*", end=" ")
        else:
            print(state[i_index], end=" ")

    print("")

def displayQ3Result(iterations = 1):
    for inc in range(iterations):
        print("---------------------------------------------")
        print("Trial", end=" ")
        print(inc + 1)


        puzzle = make_rand_house_puzzle()
        # puzzle = (5, 0, 8, 4, 2, 1, 7, 3, 6)
        display_house_puzzle(puzzle)

        print("---------------------------------------------")
        print("A*-search using the misplaced tile heuristic")

        start_time = time.time()

        # ... do something ...
        answer1 = astar_search(DuckPuzzle(puzzle), display = False)

        elapsed_time = time.time() - start_time

        # the total running time in seconds
        print("the total running time in seconds:")
        print(elapsed_time)


        # the length (i.e. number of tiles moved) of the solution
        print("the length (i.e. number of tiles moved) of the solution:")
        # print(answer1.solution())
        print(len(answer1.solution()))


        # that total number of nodes that were removed from frontier
        print("that total number of nodes that were removed from frontier")
        astar_search_display_frontier(DuckPuzzle(puzzle))

        #------------------------------------------------------------------------
        print("---------------------------------------------")
        print("A*-search using the Manhattan distance heuristic")

        start_time = time.time()

        # ... do something ...
        answer2 = astar_manhattan_distance_search(DuckPuzzle(puzzle), display = False)

        elapsed_time = time.time() - start_time

        # the total running time in seconds
        print("the total running time in seconds:")
        print(elapsed_time)


        # the length (i.e. number of tiles moved) of the solution
        print("the length (i.e. number of tiles moved) of the solution:")
        # print(answer2.solution())
        print(len(answer2.solution()))


        # that total number of nodes that were removed from frontier
        print("that total number of nodes that were removed from frontier")
        astar_manhattan_distance_search(DuckPuzzle(puzzle))

        #------------------------------------------------------------------------
        print("---------------------------------------------")
        print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic")

        start_time = time.time()

        # ... do something ...
        answer3 = astar_max_of_manhattan_distance_and_h_search(DuckPuzzle(puzzle))

        elapsed_time = time.time() - start_time

        # the total running time in seconds
        print("the total running time in seconds:")
        print(elapsed_time)


        # the length (i.e. number of tiles moved) of the solution
        print("the length (i.e. number of tiles moved) of the solution:")
        # print(answer3.solution())
        print(len(answer3.solution()))


        # that total number of nodes that were removed from frontier
        print("that total number of nodes that were removed from frontier")
        astar_max_of_manhattan_distance_and_h_search(DuckPuzzle(puzzle))
        print("---------------------------------------------")

# displayQ1Result()
# displayQ2Result()
displayQ2Result(10)
# displayQ3Result()
# displayQ3Result(10)


# ...
