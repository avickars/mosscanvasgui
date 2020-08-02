# Assignment 1: Experimenting with the 8-puzzle
# by Winston Ye, 301299259, winstony@sfu.ca
# a1.py

import random
import time

# From search.py
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

    """ The misplaced tile heuristic has been modified to not account the empty tile in the
        calculation. For example, 0 will not be considered as a misplaced tile. """
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        misplaced = 0
        for i in range(9):
            if self.goal[i] != 0:
                if node.state[i] != self.goal[i]:
                    misplaced += 1
        return misplaced

    def h_manhattan(self, node):
        """ Returns the heuristic value for a given state. The Manhattan distance is calculated
            by creating two 2D array representation of the node and goal states. The distances are
            calculated by finding, and comparing the distance for each tile in the node and goal states.
            A is the 2D goal array
            B is the 2D intiial array """
        A = []
        B = []
        sublistA = []
        sublistB = []
        dist = 0

        for i in range(9):
            sublistA.append(self.goal[i])
            sublistB.append(node.state[i])
            if(len(sublistA) == 3):
                A.append(sublistA)
                B.append(sublistB)
                sublistA = []
                sublistB = []

        for y in range(3):
            for x in range(3):
                if(B[y][x] != 0):
                    row = 0
                    while B[y][x] not in A[row]:
                        row += 1
                    dist += abs(row - y) + abs(A[row].index(B[y][x]) - x)
        return dist

    def h_max(self, node):
        """ Returns the max of either the manhattan or misplaced tile heuristic value"""
        return max(self.h_manhattan(node), self.h(node))

# Question 3: The House-Puzzle - Duck Puzzle implementation
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a duck board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ The possible actions for my duck board have 2 seperate UP and DOWN actions,
            UP/DOWN2 signifies an action where the index of a tile 2 spaces up/down will
            be swapped. The UP/DOWN3 signifies an action where the index of a tile 3 spaces
            up/down will be swapped. Based on the index, certain actions are removed.
            They are organized removals in common removals to each tile, and unique removals. """
        possible_actions = ['UP2', 'UP3', 'DOWN2', 'DOWN3', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        """ Common removes """
        if index_blank_square < 2 or index_blank_square > 3 and index_blank_square < 6:
            possible_actions.remove('UP2')
            possible_actions.remove('UP3')

        if index_blank_square > 5:
            possible_actions.remove('UP2')

        if index_blank_square < 4 and index_blank_square > 1:
            possible_actions.remove('UP3')

        if index_blank_square > 5:
            possible_actions.remove('DOWN2')
            possible_actions.remove('DOWN3')

        if index_blank_square < 6 and index_blank_square > 2:
            possible_actions.remove('DOWN2')

        if index_blank_square < 2:
            possible_actions.remove('DOWN3')

        """ Unique removes """
        if index_blank_square == 0 or index_blank_square == 6:
            possible_actions.remove('LEFT')

        elif index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')

        elif index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN2')
            possible_actions.remove('DOWN3')

        return possible_actions

    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP2': -2, 'UP3': -3, 'DOWN2': 2, 'DOWN3': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    """ The misplaced tile heuristic has been modified to not account the empty tile in the
    calculation. For example, 0 will not be considered as a misplaced tile. """
    def h(self, node):
        misplaced = 0
        for i in range(9):
            if self.goal[i] != 0:
                if node.state[i] != self.goal[i]:
                    misplaced += 1
        return misplaced
    
    def h_manhattan(self, node):
        """ Returns the heuristic value for a given state. The Manhattan distance is calculated
            by creating two 4x4 2D array representation of the node and goal states. The distances are
            calculated by finding, and comparing the distance for each tile in the node and goal states.
            -1 is used in the 4x4 array to mimic the duck shape, these values are ignored.
            A is the 2D goal array
            B is the 2D intiial array """
        A = []
        B = []
        sublistA = []
        sublistB = []
        dist = 0

        for i in range(9):
            if i == 6:
                sublistA.append(-1)
                sublistB.append(-1)

            sublistA.append(self.goal[i])
            sublistB.append(node.state[i])
            
            if i == 1:
                sublistA += [-1] * 2
                sublistB += [-1] * 2

            if len(sublistA) == 4:
                A.append(sublistA)
                B.append(sublistB)
                sublistA = []
                sublistB = []

        for y in range(3):
            for x in range(4):
                if B[y][x] != 0 and B[y][x] != -1:
                    row = 0
                    while B[y][x] not in A[row]:
                        row += 1
                    dist += abs(row - y) + abs(A[row].index(B[y][x]) - x)
        
        return dist

    def h_max(self, node):
        """ Returns the max of either the manhattan or misplaced tile heuristic value"""
        return max(self.h_manhattan(node), self.h(node))

# Best First Graph Search
""" Modifications have been made to record the total number of nodes removed
    from the frontier and the length of the solution """
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
    numRemoved = 0
    while frontier:
        node = frontier.pop()
        numRemoved += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                print(node.path_cost, "length of the solution")
                print(numRemoved, "nodes have been removed from the frontier")
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

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# Question 1: Helper Functions
def make_rand_8puzzle():
    """ Utilizes check_solvability from the EightPuzzle class to check if a randomly
        shuffled goal state is a valid puzzle and can be solved. Returns a EightPuzzle
        when a valid puzzle is found. """
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    eightPuzzleTester = EightPuzzle(num_list)
    random.shuffle(num_list)

    while True:
        if(eightPuzzleTester.check_solvability(num_list)):
            print(num_list)
            display(num_list)
            return EightPuzzle(tuple(num_list))
        else:
            random.shuffle(num_list)

def make_rand_duckpuzzle(n):
    """ Utilizes n random actions from the DuckPuzzle class to create a random
        duck puzzle. The DuckPuzzle will be solvable as it uses valid actions
        for the puzzle for every new iteration of the puzzle generated. Returns
        a random duck puzzle upon completion of n iterations """
    currState = tuple([1, 2, 3, 4, 5, 6, 7, 8, 0])
    duckPuzzle = DuckPuzzle(currState)

    for i in range(n):
        possibleActions = duckPuzzle.actions(duckPuzzle.initial)
        randomAction = random.choice(possibleActions)
        currState = duckPuzzle.result(state=currState, action=randomAction)
        duckPuzzle = DuckPuzzle(currState)
    print(list(currState))
    displayDuck(currState)
    return DuckPuzzle(currState)

def display(state):
    outputStr = ""
    for index, num in enumerate(state, start=1):
        if num == 0:
            outputStr += "* "
        else:
            outputStr += str(num) + " "
        if index % 3 == 0 and index != len(state):
            outputStr += "\n"
    print(outputStr)

def displayDuck(state):
    outputStr = ""
    for i in range(9):
        if i == 2:
            outputStr += "\n"
        elif i == 6:
            outputStr += "\n " + " "
        
        if state[i] != 0:
            outputStr += str(state[i]) + " "
        else:
            outputStr += "*"
    print(outputStr)

# Question 2 and 3: Comparing Algorithms

###################  SETUP  #####################
# Defines the number of puzzles you want to test
N_PUZZLES = 10
# Defines the number of actions performed to make a random duck puzzle
N_ACTIONS = 1000
# Defines what heuristic function you want to run
RUN_MISPLACED = True
RUN_MANHATTAN = True
RUN_MAX = True
# Defines what puzzles you want to test
TEST_EIGHT_PUZZLE = True
TEST_DUCK_PUZZLE = True
# Defines if goal states are printed
DISPLAY_EIGHT_GOAL = True
DISPLAY_DUCK_GOAL = True
#################################################

if TEST_EIGHT_PUZZLE:
    for i in range(N_PUZZLES):
        eightPuzzle = make_rand_8puzzle()

        if RUN_MISPLACED:
            print("Eight Puzzle Misplaced Tile")
            start_time = time.time()
            astar_search(problem=eightPuzzle, display=True, h=eightPuzzle.h)
            elapsed_time = time.time() - start_time
            print("Time taken: ", elapsed_time, "s", "\n")
        
        if RUN_MANHATTAN:
            print("Eight Puzzle Manhattan")
            start_time = time.time()
            astar_search(problem=eightPuzzle, display=True, h=eightPuzzle.h_manhattan)
            elapsed_time = time.time() - start_time
            print("Time taken: ", elapsed_time, "s", "\n")

        if RUN_MAX:
            print("Eight Puzzle h_max")
            start_time = time.time()
            astar_search(problem=eightPuzzle, display=True, h=eightPuzzle.h_max)
            elapsed_time = time.time() - start_time
            print("Time taken: ", elapsed_time, "s", "\n")

if TEST_DUCK_PUZZLE:
    for i in range(N_PUZZLES):
        duckPuzzle = make_rand_duckpuzzle(N_ACTIONS)

        if RUN_MISPLACED:
            print('Duck Puzzle Misplaced tile')
            start_time = time.time()
            astar_search(duckPuzzle, display=True, h=duckPuzzle.h)
            elapsed_time = time.time() - start_time
            print("Time taken: ", elapsed_time, "s", "\n")

        if RUN_MANHATTAN:
            print('Duck Puzzle Manhattan')
            start_time = time.time()
            astar_search(duckPuzzle, display=True, h=duckPuzzle.h_manhattan)
            elapsed_time = time.time() - start_time
            print("Time taken: ", elapsed_time, "s", "\n")

        if RUN_MAX:
            print('Duck Puzzle h_max')
            start_time = time.time()
            astar_search(duckPuzzle, display=True, h=duckPuzzle.h_max)
            elapsed_time = time.time() - start_time
            print("Time taken: ", elapsed_time, "s", "\n")

if DISPLAY_EIGHT_GOAL:
    display(tuple([1,2,3,4,5,6,7,8,0]))

if DISPLAY_DUCK_GOAL and DISPLAY_EIGHT_GOAL:
    print("")

if DISPLAY_DUCK_GOAL:
    displayDuck(tuple([1,2,3,4,5,6,7,8,0]))