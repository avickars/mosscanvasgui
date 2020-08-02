# a1.py

# MODIFIED FROM SEARCH.PY

from search import *
import time


def best_first_graph_search_extended(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned.

    Extended to additionally return the number of nodes removed from the frontier"""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    removed_from_frontier = 0
    explored = set()
    while frontier:
        node = frontier.pop()
        removed_from_frontier += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, removed_from_frontier
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, None


def astar_search_extended(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass.

    Modified to use the extended best first graph search"""

    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_extended(problem, lambda n: n.path_cost + h(n), display)


def h(self, node):
    """ Return the heuristic value for a given state. Default heuristic function used is
    h(n) = number of misplaced tiles

    This function has been fixed so that the empty tile is not counted as a misplaced tile"""

    count = sum(s != g for (s, g) in zip(node.state, self.goal))
    if self.find_blank_square(self.goal) != self.find_blank_square(node.state):
        count -= 1

    return count


EightPuzzle.h = h   # Patch the method in EightPuzzle to return the correct result


# DUCK PUZZLE CLASS


class DuckPuzzle(Problem):
    """Similar to EightPuzzle, but the shape is different, and the goal is the following state:
    1 2
    3 4 5 6
      7 8 *

    The indexes of each position are then as follows:
    0 1
    2 3 4 5
      6 7 8"""

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

        # the following coordinates are in the format of (column, row)
        self.index_to_coord = {
            0: (0, 0),
            1: (1, 0),
            2: (0, 1),
            3: (1, 1),
            4: (2, 1),
            5: (3, 1),
            6: (1, 2),
            7: (2, 2),
            8: (3, 2)
        }

        self.coord_to_index = {
            (0, 0): 0,
            (1, 0): 1,
            (0, 1): 2,
            (1, 1): 3,
            (2, 1): 4,
            (3, 1): 5,
            (1, 2): 6,
            (2, 2): 7,
            (3, 2): 8
        }

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = []
        index_blank_square = self.find_blank_square(state)
        col_blank, row_blank = self.index_to_coord[index_blank_square]

        if (col_blank - 1, row_blank) in self.coord_to_index:
            possible_actions.append('LEFT')
        if (col_blank, row_blank - 1) in self.coord_to_index:
            possible_actions.append('UP')
        if (col_blank + 1, row_blank) in self.coord_to_index:
            possible_actions.append('RIGHT')
        if (col_blank, row_blank + 1) in self.coord_to_index:
            possible_actions.append('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        col_blank, row_blank = self.index_to_coord[blank]

        delta = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }

        col_delta, row_delta = delta[action]

        neighbor = self.coord_to_index[col_blank + col_delta, row_blank + row_delta]

        new_state = list(state)
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

        This function has been fixed so that the empty tile is not counted as a misplaced tile"""

        count = sum(s != g for (s, g) in zip(node.state, self.goal))
        if self.find_blank_square(self.goal) != self.find_blank_square(node.state):
            count -= 1

        return count

    def manhattan_distance(self, node):
        total_distance = 0

        for i in range(1, 9):
            node_x, node_y = self.index_to_coord[node.state.index(i)]
            goal_x, goal_y = self.index_to_coord[self.goal.index(i)]
            total_distance += abs(node_x - goal_x) + abs(node_y - goal_y)

        return total_distance

    def max_heuristic(self, node):
        return max(self.h(node) - 1, self.manhattan_distance(node))


# ASSIGNMENT FUNCTIONS


def get_shuffled_puzzle(puzzle, moves):
    """Generates a random puzzle by shuffling the initial state of a puzzle,
    which guarantees that the puzzle can be returned to its initial state.
    If the initial state is solvable, this also guarantees that the shuffled
    puzzle is solvable.
    """
    state = puzzle.initial

    for i in range(moves):
        move = random.choice(puzzle.actions(state))
        state = puzzle.result(state, move)

    return puzzle.__class__(tuple(state))


def make_rand_8puzzle():
    return get_shuffled_puzzle(EightPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0)), random.choice(range(300, 350)))


def make_rand_duck_puzzle():
    return get_shuffled_puzzle(DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0)), random.choice(range(300, 350)))


def tile_representation(tile):
    return "*" if tile == 0 else str(tile)


def display(state):
    state_string = " ".join(["*" if tile == 0 else str(tile) for tile in state])

    print(state_string[0:5])
    print(state_string[6:11])
    print(state_string[12:17])


def display_duck(state):
    state_string = " ".join(["*" if tile == 0 else str(tile) for tile in state])

    print(state_string[0:3])
    print(state_string[4:11])
    print("  " + state_string[12:17])


def manhattan_distance(self, node):
    def position_coordinates(position):
        return position % 3, position // 3

    total_distance = 0

    for i in range(1, 9):
        node_x, node_y = position_coordinates(node.state.index(i))
        goal_x, goal_y = position_coordinates(self.goal.index(i))
        total_distance += abs(node_x - goal_x) + abs(node_y - goal_y)

    return total_distance


EightPuzzle.manhattan_distance = manhattan_distance


def max_heuristic(self, node):
    return max(self.h(node), self.manhattan_distance(node))


EightPuzzle.max_heuristic = max_heuristic


def display_8puzzle_moves(node):
    if node.parent is not None:
        display_8puzzle_moves(node.parent)

    display(node.state)
    print()


def display_duck_puzzle_moves(node):
    if node.parent is not None:
        display_duck_puzzle_moves(node.parent)

    display_duck(node.state)
    print()


def heuristic_benchmark(puzzle, *heuristics, display=None):
    for heuristic in heuristics:
        print(name(heuristic))

        start_time = time.time()
        result, removed = astar_search_extended(puzzle, heuristic)
        elapsed_time = time.time() - start_time

        if(display is not None):
            print("Game Moves:")
            display(result)

        print("Running Time:", elapsed_time)
        print("Final Node:", result)
        print("Solution Length:", result.depth)
        print("Removed From Frontier:", removed)
        print()


if __name__ == "__main__":
    print()
    puzzle = make_rand_duck_puzzle()
    display_duck(puzzle.initial)
    print()

    heuristic_benchmark(puzzle,
                        puzzle.manhattan_distance, puzzle.max_heuristic, puzzle.h,
                        display=display_duck_puzzle_moves)

    for i in range(9):
        print()
        puzzle = make_rand_duck_puzzle()
        display_duck(puzzle.initial)
        print()

        heuristic_benchmark(puzzle, puzzle.manhattan_distance, puzzle.max_heuristic, puzzle.h)

    print()
    puzzle = make_rand_duck_puzzle()
    display_duck(puzzle.initial)
    print()

    heuristic_benchmark(puzzle,
                        puzzle.manhattan_distance, puzzle.max_heuristic, puzzle.h,
                        display=display_duck_puzzle_moves)

    for i in range(9):
        print()
        puzzle = make_rand_8puzzle()
        display(puzzle.initial)
        print()

        heuristic_benchmark(puzzle, puzzle.manhattan_distance, puzzle.max_heuristic, puzzle.h)
