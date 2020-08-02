# f(n) = h(n) + g(n)
# f(n): 从初始点经由节点n到目标点的估价函数
# h(n): 从n到目标节点最佳路径的估计代价（此状态与目标状态的九宫格中相异数字的个数）
# g(n): 在状态空间中从初始节点到n节点的实际代价

# a1.py
import random

from search import *

import time


# modified search class and functions

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
    count = 0
    while frontier:
        node = frontier.pop()
        count += 1
        if problem.goal_test(node.state):
            print("The total nodes removed from frontier is: ", count)
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


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """
    count = 0

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

    def display(self, state):
        """ take an 8-puzzle state (i.e. a tuple that is a permutation of (0, 1, 2, ..., 8)) as input
            and prints a neat and readable representation of it """
        print("*-------------Eight puzzle display-------------*")
        for i in range(0, len(state), 3):
            if state[i] == 0:
                print('*', state[i + 1], state[i + 2])
            elif state[i + 1] == 0:
                print(state[i], '*', state[i + 2])
            elif state[i + 2] == 0:
                print(state[i], state[i + 1], '*')
            else:
                print(state[i], state[i + 1], state[i + 2])
        print()

    def h1(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s!=0 and s != g for (s, g) in zip(node.state, self.goal))

    def h2(self, node):
        """ Return the heuristic value for a given state. The heuristic function used is
        h(n) = sum of the distances of the tiles from their goal positions. """
        manhattan_distance = 0
        for i in range(1, 9):
            position_required = i - 1
            x_required = position_required % 3
            y_required = position_required // 3
            position_actual = node.state.index(i)
            x_actual = position_actual % 3
            y_actual = position_actual // 3
            manhattan_distance += abs(x_required - x_actual) + abs(y_required - y_actual)
        return manhattan_distance

    def h3(self, node):
        if self.h1(node) > self.h2(node):
            return self.h1(node)
        else:
            return self.h2(node)


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

        possible_actions = ['UP1', 'UP2', 'DOWN0', 'DOWN1', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square < 2:
            possible_actions.remove('UP1')
            possible_actions.remove('UP2')
            possible_actions.remove('DOWN1')
        if index_blank_square > 1 and index_blank_square < 6:
            possible_actions.remove('UP2')
            possible_actions.remove('DOWN0')
        if index_blank_square > 5:
            possible_actions.remove('UP1')
            possible_actions.remove('DOWN0')
            possible_actions.remove('DOWN1')
        if index_blank_square == 2:
            possible_actions.remove('DOWN1')
        if index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP1')
        return possible_actions

    def rand_action(self, state):
        possible_actions = self.actions(state)
        rand_index = random.randint(0, len(possible_actions) - 1)
        rand_action = possible_actions[rand_index]
        return rand_action

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP1': -2, 'UP2': -3, 'DOWN0': 2, 'DOWN1': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def display(self, state):
        print("*-------------Duck puzzle display-------------*")
        index0 = self.find_blank_square(state)
        state = list(state)
        state[index0] = '*'
        i = 0
        while i < len(state):
            if i == 0:
                print(state[0], state[1])
                i += 2
            elif i == 2:
                print(state[2], state[3], state[4], state[5])
                i += 4
            else:
                print(' ', state[6], state[7], state[8])
                i += 3
        print()

    def h1(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def h2(self, node):
        """ Return the heuristic value for a given state. The heuristic function used is
        h(n) = sum of the distances of the tiles from their goal positions. """
        manhattan_distance = 0
        for i in range(1, 9):
            position_required = i - 1
            if position_required < 2:
                x_required = position_required
                y_required = 0
            elif position_required > 5:
                x_required = position_required - 5
                y_required = 3
            else:
                x_required = position_required - 2
                y_required = 2
            position_actual = node.state.index(i)
            if position_actual < 2:
                x_actual = position_actual
                y_actual = 0
            elif position_actual > 5:
                x_actual = position_actual - 5
                y_actual = 3
            else:
                x_actual = position_actual - 2
                y_actual = 2
            manhattan_distance += (abs(x_required - x_actual) + abs(y_required - y_actual))
        return manhattan_distance

    def h3(self, node):
        if self.h1(node) > self.h2(node):
            return self.h1(node)
        else:
            return self.h2(node)


def show_result(puzzle):
    print("*------------- Misplaced tiles -------------*")
    start = time.time()
    node = astar_search(puzzle, h=puzzle.h1)
    end = time.time()

    # the total running time in seconds
    print("The total running time in seconds: ", end - start)

    # the length of the solution
    print("The length of the solution: ", len(node.path()) - 1)

    """ uncomment the following codes to see the path and each step"""
    # print(node.path())
    # for n in node.path():
    #     n = n.state
    #     puzzle.display(tuple(n))
    # print(node.solution())
    print()

    print("*------------- Manhattan_distance -------------*")
    start = time.time()
    node = astar_search(puzzle, h=puzzle.h2)
    end = time.time()

    # the total running time in seconds
    print("The total running time in seconds: ", end - start)

    # the length of the solution
    print("The length of the solution: ", len(node.path()) - 1)

    """ uncomment the following codes to see the path and each step"""
    # print(node.path())
    # for n in node.path():
    #     n = n.state
    #     puzzle.display(tuple(n))
    # print(node.solution())
    print()

    print("*-- Max of misplaced tiles and manhattan distance --*")
    start = time.time()
    node = astar_search(puzzle, h=puzzle.h3)
    end = time.time()

    # the total running time in seconds
    print("The total running time in seconds: ", end - start)

    # the length of the solution
    print("The length of the solution: ", len(node.path()) - 1)

    """ uncomment the following codes to see the path and each step"""
    # print(node.path())
    # for n in node.path():
    #     n = n.state
    #     puzzle.display(tuple(n))
    # print(node.solution())
    print()


def make_rand_8puzzle():
    """ returns a new instance of an EightPuzzel problem with a random initial state that is solvable. """
    # randomly generate a list with numbers 0~8 (without repeat)
    state = tuple(random.sample(range(0, 9), 9))

    # initialize a Problem and an EightPuzzle
    # problem = Problem(state)
    eightPuzzle = EightPuzzle(state)

    # check if eightPuzzle is solvable
    isSolvable = eightPuzzle.check_solvability(state)

    while not isSolvable:
        # randomly generate a list with numbers 0~8 (without repeat)
        state = tuple(random.sample(range(0, 9), 9))

        # initialize a Problem and an EightPuzzle
        # problem = Problem(state)
        eightPuzzle = EightPuzzle(state)

        # check if eightPuzzle is solvable
        isSolvable = eightPuzzle.check_solvability(state)

    return eightPuzzle


def make_rand_duck_puzzle():
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    temp_duck_puzzle = DuckPuzzle(goal)
    n = random.randint(100, 999)
    state = goal
    for i in range(n):
        action = temp_duck_puzzle.rand_action(state)
        state = temp_duck_puzzle.result(state, action)

    duckPuzzle = DuckPuzzle(state)
    return duckPuzzle


def eight_puzzle_compare():
    for i in range(10):
        print("*-----------------------Eight Puzzle-----------------------*")
        eightPuzzle = make_rand_8puzzle()
        eightPuzzle.display(eightPuzzle.initial)
        show_result(eightPuzzle)


def duck_puzzle_compare():
    for i in range(10):
        print("*-----------------------Duck Puzzle------------------------*")
        duckPuzzle = make_rand_duck_puzzle()
        duckPuzzle.display(duckPuzzle.initial)
        show_result(duckPuzzle)


def main():
    eight_puzzle_compare()
    duck_puzzle_compare()


if __name__ == "__main__":
    main()
