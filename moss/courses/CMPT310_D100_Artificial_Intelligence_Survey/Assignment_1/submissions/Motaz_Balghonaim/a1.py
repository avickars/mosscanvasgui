# a1.py
# Author: Motaz Balghonaim

from search import *
import time

"""
This function is copied and adapted from:
https://github.com/aimacode/aima-python/blob/master/search.py#L415
"""


def astar_search_extended(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_extended(problem, lambda n: n.path_cost + h(n), display)


"""
This function is copied and adapted from:
https://github.com/aimacode/aima-python/blob/f502be974dae001a4e3af4d6cdf876abcb8f121e/search.py#L260
"""


def best_first_graph_search_extended(problem, f, display=False):
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
    num_of_frontier_pops = 0
    explored = set()
    while frontier:
        node = frontier.pop()
        num_of_frontier_pops += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded,", len(frontier), "paths remain in the frontier,",
                      len(node.path()), "is the solution length, and ", num_of_frontier_pops,
                      " nodes were removed from the frontier")
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


"""
############################################ QUESTIONS 1 & 2 #######################################################
"""

"""
This class is copied and adapted from:
https://github.com/aimacode/aima-python/blob/master/search.py#L426
"""


class EightPuzzleExtended(EightPuzzle):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0), heuristic=None):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)
        self.heuristic = heuristic

    def misplaced_tiles(self, node):
        # Don't count the blank tile as misplaced as per the textbook
        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

    def manhattan_distance(self, node):
        mhd = 0
        # x_goal, y_goal = self.find_2d_blank_index(node.state)

        for i in range(9):
            value = node.state[i]
            if value != 0:
                goal_index = self.goal.index(value)
                x_goal, y_goal = goal_index // 3, goal_index % 3
                x_value, y_value = i // 3, i % 3
                mhd += abs(x_value - x_goal) + abs(y_value - y_goal)

        return mhd

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        if self.heuristic == 'Misplaced Tiles':
            return self.misplaced_tiles(node)
        elif self.heuristic == 'Manhattan Distance':
            return self.manhattan_distance(node)
        elif self.heuristic == 'Hybrid':
            return max(self.misplaced_tiles(node), self.manhattan_distance(node))
        else:
            raise ValueError


def get_legal_steps(empty_loc: tuple) -> list:
    steps = []
    if empty_loc[0] > 0:
        steps.append('UP')
    if empty_loc[0] < 2:
        steps.append('DOWN')
    if empty_loc[1] > 0:
        steps.append('LEFT')
    if empty_loc[1] < 2:
        steps.append('RIGHT')
    return steps


def make_rand_8puzzle() -> tuple:
    # Start with valid initial state
    puzzle = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    def perform_step(curr_puzzle: list, empty_loc: tuple):

        legal_steps = get_legal_steps(empty_loc)

        def swap(a: tuple, b: tuple):
            temp = curr_puzzle[a[0]][a[1]]
            curr_puzzle[a[0]][a[1]] = curr_puzzle[b[0]][b[1]]
            curr_puzzle[b[0]][b[1]] = temp

        random_step = legal_steps[random.randint(0, len(legal_steps) - 1)]

        if random_step == 'UP':
            new_location = (empty_loc[0] - 1, empty_loc[1])
            swap(empty_loc, new_location)
        elif random_step == 'DOWN':
            new_location = (empty_loc[0] + 1, empty_loc[1])
            swap(empty_loc, new_location)
        elif random_step == 'LEFT':
            new_location = (empty_loc[0], empty_loc[1] - 1)
            swap(empty_loc, new_location)
        elif random_step == 'RIGHT':
            new_location = (empty_loc[0], empty_loc[1] + 1)
            swap(empty_loc, new_location)
        else:
            raise ValueError

        return new_location

    empty_location = (2, 2)

    # Perform random legal actions on the valid initial state
    for s in range(50):
        empty_location = perform_step(puzzle, empty_location)

    return puzzle[0][0], puzzle[0][1], puzzle[0][2], \
           puzzle[1][0], puzzle[1][1], puzzle[1][2], \
           puzzle[2][0], puzzle[2][1], puzzle[2][2]


def display(state: tuple):
    # Check if state shape is a valid one (AxA)
    if len(state) != 9:
        print()
        print('Invalid state representation')
        return

    def asterisk_if_zero(num: Number) -> str:
        return num if num != 0 else '*'

    print(asterisk_if_zero(state[0]), asterisk_if_zero(state[1]), asterisk_if_zero(state[2]))
    print()
    print(asterisk_if_zero(state[3]), asterisk_if_zero(state[4]), asterisk_if_zero(state[5]))
    print()
    print(asterisk_if_zero(state[6]), asterisk_if_zero(state[7]), asterisk_if_zero(state[8]))


def eight_puzzle_tests():
    heuristics = ['Misplaced Tiles', 'Manhattan Distance', 'Hybrid']

    puzzles = []
    for j in range(10):
        puzzles.append(make_rand_8puzzle())

    for i in range(len(heuristics)):
        print(f'Currently testing Eight Puzzle: {heuristics[i]}')
        print()

        for j in range(len(puzzles)):
            start_time = time.time()
            problem = EightPuzzleExtended(puzzles[j], heuristic=heuristics[i])
            astar_search_extended(problem, display=True)
            elapsed_time = time.time() - start_time

            print(f'elapsed time (in seconds): {elapsed_time}s')
            print()

        print('################################')
        print()

    print()


"""
############################################ QUESTIONS 3 #######################################################
"""


def get_legal_duck_steps(empty_idx: tuple) -> list:
    steps = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    if empty_idx < 2 or empty_idx == 4 or empty_idx == 5:
        steps.remove('UP')
    if empty_idx > 5 or empty_idx == 2:
        steps.remove('DOWN')
    if empty_idx == 0 or empty_idx == 2 or empty_idx == 6:
        steps.remove('LEFT')
    if empty_idx == 1 or empty_idx == 5 or empty_idx == 8:
        steps.remove('RIGHT')
    return steps


def perform_duck_step(puzzle: tuple, empty_idx: Number):
    legal_steps = get_legal_duck_steps(empty_idx)
    random_step = legal_steps[random.randint(0, len(legal_steps) - 1)]
    new_state = list(puzzle)

    if random_step == 'UP':
        new_idx = empty_idx - 2 if empty_idx < 6 else empty_idx - 3
    elif random_step == 'DOWN':
        new_idx = empty_idx + 2 if empty_idx < 2 else empty_idx + 3
    elif random_step == 'LEFT':
        new_idx = empty_idx - 1
    elif random_step == 'RIGHT':
        new_idx = empty_idx + 1
    else:
        raise ValueError

    new_state[new_idx], new_state[empty_idx] = new_state[empty_idx], new_state[new_idx]

    return new_idx, tuple(new_state)


def make_rand_duck_puzzle() -> tuple:
    # Start with valid initial state
    puzzle = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    empty_idx = puzzle.index(0)

    # Perform random legal actions on the valid initial state
    for s in range(50):
        empty_idx, puzzle = perform_duck_step(puzzle, empty_idx)

    return puzzle


def display_duck_puzzle(state: tuple):
    # Check if state shape is a valid one (AxA)
    if len(state) != 9:
        print()
        print('Invalid state representation')
        return

    def asterisk_if_zero(num: Number) -> str:
        return num if num != 0 else '*'

    print(asterisk_if_zero(state[0]), asterisk_if_zero(state[1]))
    print()
    print(asterisk_if_zero(state[2]), asterisk_if_zero(state[3]), asterisk_if_zero(state[4]),
          asterisk_if_zero(state[5]))
    print()
    print(' ', asterisk_if_zero(state[6]), asterisk_if_zero(state[7]), asterisk_if_zero(state[8]))


class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    # Maps one dimensional index to 3x4 x and y indexes
    dim_map = {
        0: (0, 0),
        1: (0, 1),
        2: (1, 0),
        3: (1, 1),
        4: (1, 2),
        5: (1, 3),
        6: (2, 1),
        7: (2, 2),
        8: (2, 3)
    }

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0), heuristic=None):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)
        self.heuristic = heuristic

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {
            'UP': -2 if blank < 6 else -3,
            'DOWN': 2 if blank < 2 else 3,
            'LEFT': -1,
            'RIGHT': 1
        }

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def misplaced_tiles(self, node):
        # Don't count the blank tile as misplaced as per the textbook
        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

    def manhattan_distance(self, node):
        mhd = 0

        for i in range(9):
            value = node.state[i]
            if value != 0:
                goal_index = self.goal.index(value)
                mhd += abs(self.dim_map[i][0] - self.dim_map[goal_index][0]) + \
                       abs(self.dim_map[i][1] - self.dim_map[goal_index][1])

        return mhd

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        if self.heuristic == 'Misplaced Tiles':
            return self.misplaced_tiles(node)
        elif self.heuristic == 'Manhattan Distance':
            return self.manhattan_distance(node)
        elif self.heuristic == 'Hybrid':
            return max(self.misplaced_tiles(node), self.manhattan_distance(node))
        else:
            raise ValueError


def duck_puzzle_tests():
    heuristics = ['Misplaced Tiles', 'Manhattan Distance', 'Hybrid']

    puzzles = []
    for j in range(10):
        puzzles.append(make_rand_duck_puzzle())

    for i in range(len(heuristics)):
        print(f'Currently testing Ducke Puzzle: {heuristics[i]}')
        print()

        for j in range(len(puzzles)):
            start_time = time.time()
            problem = DuckPuzzle(puzzles[j], heuristic=heuristics[i])
            astar_search_extended(problem, display=True)
            elapsed_time = time.time() - start_time

            print(f'elapsed time (in seconds): {elapsed_time}s')
            print()

        print('################################')
        print()

    print()


eight_puzzle_tests()
duck_puzzle_tests()
