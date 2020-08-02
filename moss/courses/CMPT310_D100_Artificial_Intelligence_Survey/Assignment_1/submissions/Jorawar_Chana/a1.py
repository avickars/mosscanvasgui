# a1.py
# Running this file will test all the heuristics against 15 puzzles
# The script wll the generate two csv files which containing the collected data


from search import *
import random
import time
from collections import namedtuple
import csv

# Used to collect and output data into a csv
TrialData = namedtuple("TrialData", ["time", "length", "removed_nodes"])


# ----------------------------------- Duck Puzzle ----------------------------------- #
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x4 board, where one of the
    squares is a blank represented by 0 and some tiles are 'out-of-bounds' represented by None.
    The overall state can be interpreted conceptually as follows:

      1  2 -1 -1
      3  4  5  6
     -1  7  8  0

     (-1 represents None)
     """

    horizontal_dimension = 4
    vertical_dimension = 3

    def __init__(self, initial, goal=(1, 2, None,  None, 3, 4, 5, 6, None, 7, 8, 0)):
        super().__init__(initial, goal)
        pass

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = []

        # the action_mask maps the available actions the blank tile
        # has if it were at index i
        action_mask = {'UP': [False, False, False, False,
                              True, True, False, False,
                              False, True, True, True],
                       'DOWN': [True, True, False, False,
                                False, True, True, True,
                                False, False, False, False],
                       'LEFT': [False, True, False, False,
                                False, True, True, True,
                                False, False, True, True],
                       'RIGHT': [True, False, False, False,
                                 True, True, True, False,
                                 False, True, True, False]}

        index_blank_square = self.find_blank_square(state)

        for action, lookup_mask in action_mask.items():
            if lookup_mask[index_blank_square]:
                possible_actions.append(action)

        return possible_actions

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index(0)

    def result(self, state, action):
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == tuple(self.goal)

    def display(self, state):
        """Display the duck puzzle properly formatted"""
        display_list = [x if x is not None else '-' for x in state]
        display_list = ['*' if i == 0 else i for i in display_list]
        print("{} {} {} {}\n{} {} {} {}\n{} {} {} {}".format(*display_list))

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles
        Note: Has been adjusted to exclude the 0 tile"""

        return sum(s != g for (s, g) in zip(node.state, self.goal) if s != 0)

    def manhattan_distance_heuristic(self, node):
        """ Returns the heuristic value for a given state. Calculates the distance as the
        total movement required by all tiles to reach the goal state
        Note: This implementation does not count the movement of the 0 tile """
        s = 0
        for i, value in enumerate(node.state):
            if value:
                goal_index = self.goal.index(value)
                horizontal_movement = abs(goal_index % self.horizontal_dimension - i % self.horizontal_dimension)
                vertical_movement = abs(goal_index // self.horizontal_dimension - i // self.horizontal_dimension)
                s += horizontal_movement + vertical_movement
        return s

    def max_heuristic(self, node):
        """Takes the maximum of the manhattan distance and misplaced title heuristic"""
        return max(self.manhattan_distance_heuristic(node), self.h(node))


def make_rand_duck_puzzle(goal_state=(1, 2, None,  None, 3, 4, 5, 6, None, 7, 8, 0)):
    """Generate random, solvable duck puzzle
       returns the puzzle and the initial  state"""
    shuffles = random.randint(0, 1000000)
    puzzle = DuckPuzzle(goal_state)
    new_state = goal_state
    inverse_actions = {'UP': 'DOWN',
                       'DOWN':  'UP',
                       'LEFT': 'RIGHT',
                       'RIGHT': 'LEFT'}
    last_move = None
    for i in range(shuffles):
        possible_actions = puzzle.actions(new_state)
        if last_move:
            possible_actions.remove(inverse_actions[last_move])
        last_move = random.choice(possible_actions)
        new_state = puzzle.result(new_state, last_move)
    return DuckPuzzle(new_state), tuple(new_state)


# ----------------------------------- Eight Puzzle  ----------------------------------- #
class EightPuzzle(Problem):
    # Modified from search.py in the aima-python package
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    vertical_dimension = 3
    horizontal_dimension = 3

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
        h(n) = number of misplaced tiles
        Note: Has been adjusted to exclude the 0 tile"""

        return sum(s != g for (s, g) in zip(node.state, self.goal) if s != 0)

    def manhattan_distance_heuristic(self, node):
        """ Returns the heuristic value for a given state. Calculates the distance as the
        total movement required by all tiles to reach the goal state
        Note: This implementation does not count the movement of the 0 tile """
        s = 0
        for i, value in enumerate(node.state):
            if value:
                goal_index = self.goal.index(value)
                horizontal_movement = abs(goal_index % self.horizontal_dimension - i % self.horizontal_dimension)
                vertical_movement = abs(goal_index // self.horizontal_dimension - i // self.horizontal_dimension)
                s += horizontal_movement + vertical_movement
        return s

    def max_heuristic(self, node):
        """Takes the maximum of the manhattan distance and misplaced title heuristic"""
        return max(self.manhattan_distance_heuristic(node), self.h(node))


def make_rand_8puzzle():
    """Generate a random, solvable 8 puzzle
       returns the puzzle and the initial state"""
    is_solvable = False
    while not is_solvable:
        initial_state = list(range(0, 9))
        random.shuffle(initial_state)
        puzzle = EightPuzzle(tuple(initial_state))
        if puzzle.check_solvability(initial_state):
            return puzzle, tuple(initial_state)


def display(state):
    """Display the 8 puzzle properly formatted"""
    display_list = ['*' if i == 0 else i for i in state]
    output = "{} {} {}\n{} {} {}\n{} {} {}".format(*display_list)
    print(output)


# ----------------------------------- Search Functions ----------------------------------- #
def astar_search(problem, h=None, display=False):
    # Modified from search.py in the aima-python package
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def best_first_graph_search(problem, f, display=False):
    # Modified from search.py in the aima-python package
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    start_time = time.time()
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    nodes_removed = 0
    explored = set()
    while frontier:
        node = frontier.pop()
        nodes_removed += 1
        if problem.goal_test(node.state):
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 6)
            if display:
                print("Time : {}s\nLength : {}\nRemoved nodes : {}"
                      .format(elapsed_time, len(node.solution()), nodes_removed))
            return TrialData(elapsed_time, len(node.solution()), nodes_removed)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


# ----------------------------------- Testing Functions ----------------------------------- #
def run_puzzle_test(puzzle_function, name="Data.csv", trials=10, write_to_csv=False):
    """Run search tests using either the duck puzzle or the 8 puzzle"""
    print("Generating puzzles...")
    test_puzzles = [puzzle_function()[0] for _ in range(trials)]

    manifest = dict()
    manifest["misplaced_tile"] = {i: None for i in range(trials)}
    manifest["manhattan_distance_heuristic"] = {i: None for i in range(trials)}
    manifest["max_heuristic"] = {i: None for i in range(trials)}

    print("Running tests...")
    for i, puzzle in enumerate(test_puzzles):
        print("-> running trial {}...".format(i))
        manifest['misplaced_tile'][i] = astar_search(puzzle, h=puzzle.h, display=False)
        manifest["manhattan_distance_heuristic"][i] = astar_search(puzzle, h=puzzle.manhattan_distance_heuristic,
                                                                   display=False)
        manifest["max_heuristic"][i] = astar_search(puzzle, h=puzzle.max_heuristic, display=False)

    if write_to_csv:
        print("Writing to '{}'...".format(name))
        # Modified example from python csv library documentation
        with open(name, 'w', newline='') as fd:
            writer = csv.writer(fd, delimiter='\t')
            writer.writerow(["Name", "Time", "Length", "Nodes Removed", "Trial"])
            for heuristic, data in manifest.items():
                for trial, result in data.items():
                    writer.writerow([heuristic, result.time, result.length, result.removed_nodes, trial])
    print("Done.")
    return manifest


if __name__ == '__main__':
    n = 15
    run_puzzle_test(make_rand_duck_puzzle, name="duck_puzzle.csv", trials=n, write_to_csv=True)
    run_puzzle_test(make_rand_8puzzle, name="8_puzzle.csv", trials=n, write_to_csv=True)
