# a1.py - Jeff Wang - 301309384 - CMPT310
#   cd mnt/c/users/17789/desktop/310/HW/a1
#   python3 a1.py
###   installing numpy - https://stackoverflow.com/questions/7818811/import-error-no-module-named-numpy

from utils import *

from random import *
import time

# ______________________________________________________________________________

# Copied functions from search.py for modifications #########################################################################################

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
    nodesremoved = 0

    while frontier:
        node = frontier.pop()
        nodesremoved += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            #print("the length (i.e. number of tiles moved) of the solution: ", sollength)
            print("that total number of nodes that were removed from frontier: ", nodesremoved)
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
                    #nodesremoved += 1
    return None

# ______________________________________________________________________________

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# ______________________________________________________________________________

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


# ______________________________________________________________________________

### Modifiyed from the EightPuzzle above for the assignment
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a Duck board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

#Modified for duck puzzle moves
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
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

#Modified for duck puzzle moves
    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = 0
        #delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if action == "UP" and blank > 5:
            delta =  -3
        elif action == "UP" and blank < 4:
            delta = -2
        if action == "DOWN" and blank > 2:
            delta =  3
        elif action == "DOWN" and blank < 2:
            delta = 2
        if action == "LEFT":
            delta = -1
        if action == "RIGHT":
            delta = 1

        neighbor = blank + delta
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

# Prof said we do not need a check solvability function if we make legal random moves from goal state for make_rand_duckpuzzle()

    # def check_solvability(self, state):
    #     """ Checks if the given state is solvable """
    #
    #     inversion = 0
    #     for i in range(len(state)):
    #         for j in range(i + 1, len(state)):
    #             if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
    #                 inversion += 1
    #
    #     return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


# My Functions ####################################################################################

# Disply function for the 8 puzzle
def display(state):
    for i in range(len(state)):
        ###   Printing with no newlines in Python 3 - https://www.afternerd.com/blog/how-to-print-without-a-newline-in-python/
        if state[i] == 0:
            print("* ", end = '')
        else:
            print(state[i], "", end = '')
        if i % 3 == 2:
            print()


# Disply function for the duck puzzle
def duckdisplay(state):
    for i in range(len(state)):
        if state[i] == 0:
            print("* ", end = '')
        else:
            print(state[i], "", end = '')
        if i == 1 or i == 5 or i == 8:
            print()
        if i == 5:
            print("  ", end = '')


# Make a random 8 puzzle function - basically creates a shuffled sequesnce until solvability is true
def make_rand_8puzzle():
    ###   Randomly shuffle a list - https://machinelearningmastery.com/how-to-generate-random-numbers-in-python/
    # prepare a sequence
    sequence = [i for i in range(9)]
    # randomly shuffle the sequence
    shuffle(sequence)

    Puzzle = EightPuzzle(sequence)
    Puzzle.check_solvability(sequence)

    #repeat until .check_solvability == True
    while(Puzzle.check_solvability(sequence) == False):
        shuffle(sequence)
        Puzzle = EightPuzzle(sequence)
    return tuple(sequence)


# Make a random Duck Puzzle function - basically it shuffles the goal state with 1000 random legal duck puzzle moves
def make_rand_duckpuzzle():
    goalstate = 1,2,3,4,5,6,7,8,0

    for i in range(1000):
        #set p1 as goal state
        p1 = DuckPuzzle(goalstate)
        #create a random int from 0 to legal action range
        k = randint(0, len(p1.actions(goalstate))-1)
        #set old goalstate as result of the action (newstate)
        goalstate = p1.result(goalstate,p1.actions(goalstate)[k])
        #repeat 1000 times before returning result

    return goalstate


# 8 Puzzle Function for Manhattan distance heuristic - DOES NOT INCLUDE 0 TILE JUST LIKE THE TEXTBOOK
def mdh(state):
    sum = 0
    mdhtable = [[0, 1, 2, 1, 2, 3, 2, 3, 4],
                [1, 0, 1, 2, 1, 2, 3, 2, 3],
                [2, 1, 0, 3, 2, 1, 4, 3, 2],
                [1, 2, 3, 0, 1, 2, 1, 2, 3],
                [2, 1, 2, 1, 0, 1, 2, 1, 2],
                [3, 2, 1, 2, 1, 0, 3, 2, 1],
                [2, 3, 4, 1, 2, 3, 0, 1, 2],
                [3, 2, 3, 2, 1, 2, 1, 0, 1]]
                #[4, 3, 2, 3, 2, 1, 2, 1, 0]]      EXCULDE 0 TILE

    for i in range(9):
        if state.state[i] != 0:
            sum = sum + mdhtable[state.state[i]-1][i]
            #print(mdhtable[state.state[i]-1][i])
    return sum


# Duck Puzzle Function for Manhattan distance heuristic - DOES NOT INCLUDE 0 TILE JUST LIKE THE TEXTBOOK
def duckmdh(state):
    sum = 0
    mdhtable = [[0, 1, 1, 2, 3, 4, 3, 4, 5],
                [1, 0, 2, 1, 2, 3, 2, 3, 4],
                [1, 2, 0, 1, 2, 3, 2, 3, 4],
                [2, 1, 1, 0, 1, 2, 1, 2, 3],
                [3, 2, 2, 1, 0, 1, 2, 1, 2],
                [4, 3, 3, 2, 1, 0, 3, 2, 1],
                [3, 2, 2, 1, 2, 3, 0, 1, 2],
                [4, 3, 3, 2, 1, 2, 1, 0, 1]]

    for i in range(9):
        if state.state[i] != 0:
            sum = sum + mdhtable[state.state[i]-1][i]
            #print(mdhtable[state.state[i]-1][i])
    #print("Sum = ", sum)
    return sum


# 8 Puzzle Function for returning the max of the misplaced tile heuristic or the Manhattan distance heuristic
def maxh(state):
    #print(mdh(state))
    #print(EightPuzzle(state.state).h(state))

    return max(mdh(state), EightPuzzle(state.state).h(state))


# Duck Puzzle Function for returning the max of the misplaced tile heuristic or the Manhattan distance heuristic
def duckmaxh(state):
    #print(mdh(state))
    #print(EightPuzzle(state.state).h(state))

    return max(duckmdh(state), DuckPuzzle(state.state).h(state))


# Main Function #####################################################################################################################################
if __name__ == "__main__":
    #Create random 8 puzzle that is solvable, displays the puzzle state, checks solvability again to prove it's true
    print("---------- Creating a random 8 puzzle that is solvable ----------\n")
    state1 = make_rand_8puzzle()
    display(state1)
    print("Solvable = ", EightPuzzle(state1).check_solvability(state1), "\n")

    prob1 = EightPuzzle(state1)
    print("----- A* Search using -----\n")
# ############################################################################
    # Misplaced tile heuristic (Default Function)
    print('-- Misplaced Tile Heuristic -- ')
    start_time = time.time()
    a = astar_search(prob1, prob1.h)
    elapsed_time = time.time() - start_time
    print(f'the total running time in seconds: {elapsed_time}s')
    print("the length (i.e. number of tiles moved) of the solution: ", a.path_cost, "\n")

# ############################################################################
    # Manhattan distance heuristic
    print('-- Manhattan Distance Heuristic -- ')
    start_time = time.time()
    a = astar_search(prob1, mdh)
    elapsed_time = time.time() - start_time
    print(f'the total running time in seconds: {elapsed_time}s')
    print("the length (i.e. number of tiles moved) of the solution: ", a.path_cost, "\n")

# ############################################################################
    # Max of the misplaced tile heuristic and the Manhattan distance heuristic
    print('-- Max of the Misplaced Tile and Manhattan Distance Heuristic -- ')
    start_time = time.time()
    a = astar_search(prob1, maxh)
    elapsed_time = time.time() - start_time
    print(f'the total running time in seconds: {elapsed_time}s')
    print("the length (i.e. number of tiles moved) of the solution: ", a.path_cost, "\n")


# ########################################################################################################################################################

    # DUCK PUZZLE #
    #Create random duck puzzle that is solvable, displays the puzzle state
    print("---------- Creating a random DUCK puzzle that is solvable ----------\n")
    state2 = make_rand_duckpuzzle()
    duckdisplay(state2)
    print()

    prob2 = DuckPuzzle(state2)
    print("----- A* Search using -----\n")
    
############################################################################
    # Misplaced tile heuristic (Default Function)
    print('-- Misplaced Tile Heuristic -- ')
    start_time = time.time()
    a = astar_search(prob2, prob2.h)
    elapsed_time = time.time() - start_time
    print(f'the total running time in seconds: {elapsed_time}s')
    print("the length (i.e. number of tiles moved) of the solution: ", a.path_cost, "\n")

# ############################################################################
    # Manhattan distance heuristic
    print('-- Manhattan Distance Heuristic -- ')
    start_time = time.time()
    a = astar_search(prob2, duckmdh)
    elapsed_time = time.time() - start_time
    print(f'the total running time in seconds: {elapsed_time}s')
    print("the length (i.e. number of tiles moved) of the solution: ", a.path_cost, "\n")

# ############################################################################
    # Max of the misplaced tile heuristic and the Manhattan distance heuristic
    print('-- Max of the Misplaced Tile and Manhattan Distance Heuristic -- ')
    start_time = time.time()
    a = astar_search(prob2, duckmaxh)
    elapsed_time = time.time() - start_time
    print(f'the total running time in seconds: {elapsed_time}s')
    print("the length (i.e. number of tiles moved) of the solution: ", a.path_cost, "\n")

# ########################################################################################################################################################
