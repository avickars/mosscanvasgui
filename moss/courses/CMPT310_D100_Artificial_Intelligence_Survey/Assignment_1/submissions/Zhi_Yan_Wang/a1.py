# a1.py
# Author: Zhi Yan Wang
# Created: May 20th, 2020
# Last Updated: May 29th, 2020

import time
from search import *


# ______________________________________________________________________________
# Modified functions from search.py


def astar_search(problem, h=None, display=True):  # Modified A* from search.py
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def best_first_graph_search(problem, f, display=False):  # Modified best_first_graph_search
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    n_frontier_nodes_removed = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        n_frontier_nodes_removed = n_frontier_nodes_removed + 1
        if problem.goal_test(node.state):
            if display:
                # print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                print(n_frontier_nodes_removed, "nodes removed from the frontier")
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
# Question 1 : Helper Functions


def make_rand_8puzzle():  # Generates a new solvable EightPuzzle problem
    sol = False
    initial = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    while not sol:  # Checks solvability
        random.shuffle(initial)
        sol = EightPuzzle.check_solvability(EightPuzzle(initial), initial)
    # print(sol)
    # print(initial)
    puzzle = EightPuzzle(tuple(initial))
    return puzzle


def display(state):
    disp = str(state[0]) + " " + str(state[1]) + " " + str(state[2]) + "\n" \
           + str(state[3]) + " " + str(state[4]) + " " + str(state[5]) + "\n" \
           + str(state[6]) + " " + str(state[7]) + " " + str(state[8]) + "\n"
    print(disp.replace("0", "*"))


# ______________________________________________________________________________
# Question 2 : Comparing Algorithms


def manhattan_heuristic(node):
    """Generates Manhattan distance heuristic for 8puzzle A*-search"""
    home_positions = [[4, 3, 2, 3, 2, 1, 2, 1, 0],
                      [0, 1, 2, 1, 2, 3, 2, 3, 4],
                      [1, 0, 1, 2, 1, 2, 3, 2, 3],
                      [2, 1, 0, 3, 2, 1, 4, 3, 2],
                      [1, 2, 3, 0, 1, 2, 1, 2, 3],
                      [2, 1, 2, 1, 0, 1, 2, 1, 2],
                      [3, 2, 1, 2, 1, 0, 3, 2, 1],
                      [2, 3, 4, 1, 2, 3, 0, 1, 2],
                      [3, 2, 3, 2, 1, 2, 1, 0, 1]]
    state = list(node.state)
    h = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for tile_num in state:
        h[state.index(tile_num)] = home_positions[tile_num][state.index(tile_num)]
    del h[state.index(0)]
    # print(h)
    return sum(h)


def max_manhattan_misplaced_tile_heuristic(node):
    """Returns the max value of Manhattan distance or misplaced tile heuristic for 8puzzle A*-search"""
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    h = [0, 0]
    h[0] = sum(s != g for (s, g) in zip(node.state, goal))
    h[1] = manhattan_heuristic(node)
    return max(h)


def test_algorithms(problem, h=None):  # Test algorithms from question 2 for solving 8puzzles
    """A*-search using the Manhattan distance heuristic """
    start_time = time.time()
    sol_node = astar_search(problem, h)
    elapsed_time = time.time() - start_time
    print("# of moves: ", len(sol_node.solution()))
    print(f'elapsed time (in seconds): {elapsed_time}s\n')


def compare_algorithms(n_problems=10):
    """Compares the 3 algorithms from question 2 for solving 8puzzles"""
    for i in range(n_problems):
        print(f'problem {i + 1}')
        test_puzzle = make_rand_8puzzle()
        print("Initial Problem:")
        display(test_puzzle.initial)
        # '''
        print("A*-search w/misplaced tile heuristic:")
        test_algorithms(test_puzzle)
        print("A*-search w/Manhattan distance heuristic:")
        test_algorithms(test_puzzle, manhattan_heuristic)
        print("A*-search w/max of misplaced tile and Manhattan distance heuristic:")
        test_algorithms(test_puzzle, max_manhattan_misplaced_tile_heuristic)
        # '''


# ______________________________________________________________________________
# Question 3 : The House-Puzzle


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

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square < 2:
            possible_actions.remove('UP')
            if index_blank_square % 2 == 0:
                possible_actions.remove('LEFT')
            else:
                possible_actions.remove('RIGHT')
        elif index_blank_square > 5:
            possible_actions.remove('DOWN')
            if index_blank_square % 3 == 0:
                possible_actions.remove('LEFT')
            if index_blank_square % 3 == 2:
                possible_actions.remove('RIGHT')
        elif index_blank_square - 2 % 4 == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif index_blank_square - 2 % 4 == 3:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        elif index_blank_square - 2 % 3 == 2:
            possible_actions.remove('UP')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        if blank < 2:
            delta = {'UP': 0, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        if blank > 5:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
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


def make_rand_duck_puzzle():  # Generates a new solvable DuckPuzzle problem
    """Generates a Solvable DuckPuzzle by making 200 random legal moves on a solved puzzle"""
    initial = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    for move in range(0, 200):
        possible_actions = DuckPuzzle.actions(DuckPuzzle(initial), initial)
        action = random.choice(possible_actions)
        initial = DuckPuzzle.result(DuckPuzzle(initial), initial, action)
    puzzle = DuckPuzzle(tuple(initial))
    return puzzle


def duck_display(state):
    disp = str(state[0]) + " " + str(state[1]) + "\n" \
           + str(state[2]) + " " + str(state[3]) + " " + str(state[4]) + " " + str(state[5]) + "\n" \
           + "  " + str(state[6]) + " " + str(state[7]) + " " + str(state[8]) + "\n"
    print(disp.replace("0", "*"))


def duck_manhattan_h(node):
    """Generates Manhattan distance heuristic for 8puzzle A*-search"""
    home_positions = [[5, 4, 4, 3, 2, 1, 2, 1, 0],
                      [0, 1, 1, 2, 3, 4, 3, 4, 5],
                      [1, 0, 2, 1, 2, 3, 2, 3, 4],
                      [1, 2, 0, 1, 2, 3, 2, 3, 4],
                      [2, 1, 2, 0, 1, 2, 1, 2, 3],
                      [3, 2, 2, 1, 0, 1, 2, 1, 2],
                      [4, 3, 3, 2, 1, 0, 3, 2, 1],
                      [3, 2, 2, 1, 2, 3, 0, 1, 2],
                      [4, 3, 3, 2, 1, 2, 1, 0, 1]]
    state = list(node.state)
    h = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for tile_num in state:
        h[state.index(tile_num)] = home_positions[tile_num][state.index(tile_num)]
    del h[state.index(0)]
    # print(h)
    return sum(h)


def duck_max_manhattan_misplaced_tile_h(node):
    """Returns the max value of Manhattan distance or misplaced tile heuristic for 8puzzle A*-search"""
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    h = [0, 0]
    h[0] = sum(s != g for (s, g) in zip(node.state, goal))
    h[1] = duck_manhattan_h(node)
    return max(h)


def compare_duck_algorithms(n_problems=10):
    """Compares the 3 algorithms from the duck puzzle"""
    for i in range(n_problems):
        print(f'problem {i + 1}')
        test_puzzle = make_rand_duck_puzzle()
        print("Initial Problem:")
        duck_display(test_puzzle.initial)
        # '''
        print("A*-search w/misplaced tile heuristic:")
        test_algorithms(test_puzzle)
        print("A*-search w/Manhattan distance heuristic:")
        test_algorithms(test_puzzle, duck_manhattan_h)
        print("A*-search w/max of misplaced tile and Manhattan distance heuristic:")
        test_algorithms(test_puzzle, duck_max_manhattan_misplaced_tile_h)
        # '''
