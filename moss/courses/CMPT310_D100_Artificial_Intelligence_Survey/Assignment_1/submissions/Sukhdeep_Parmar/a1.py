# a1.py
from search import *
import random
import datetime
import copy

# ----------------------------------------------------------------------------------------------------------------------
# Search.py modified functions
# ----------------------------------------------------------------------------------------------------------------------

def a1_best_first_graph_search(problem, f, display_data=False):
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

    num_nodes_removed = 0

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display_data:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")

            print("Length of solution (Node path cost): " + str(node.path_cost))
            print("Total number of nodes removed: " + str(num_nodes_removed))
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
                    num_nodes_removed += 1
    return None

def a1_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return a1_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# ----------------------------------------------------------------------------------------------------------------------
# Classes
# ----------------------------------------------------------------------------------------------------------------------

class DuckPuzzle(Problem):
    duck_delta = []

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

        # Handle the top row
        if index_blank_square < 2:
            possible_actions.remove('UP')

            # Handle left and right case
            if index_blank_square == 0:
                possible_actions.remove('LEFT')
            else:
                possible_actions.remove('RIGHT')

        # Handle the middle row
        elif 2 <= index_blank_square < 6:
            if index_blank_square != 3:
                if index_blank_square == 2:
                    possible_actions.remove('LEFT')
                    possible_actions.remove('DOWN')

                elif index_blank_square == 4:
                    possible_actions.remove('UP')

                else:
                    possible_actions.remove('UP')
                    possible_actions.remove('RIGHT')

        # Handle the bottom row
        else:
            if index_blank_square == 6:
                possible_actions.remove('LEFT')
                possible_actions.remove('DOWN')

            elif index_blank_square == 7:
                possible_actions.remove('DOWN')

            else:
                possible_actions.remove('DOWN')
                possible_actions.remove('RIGHT')

        return possible_actions

    def delta_calculator(self, state):
        blank_tile_location = self.find_blank_square(state)
        delta = {
            0: {'DOWN': 2, 'RIGHT': 1},
            1: {'DOWN': 2, 'LEFT': -1},
            2: {'UP': -2, 'RIGHT': 1},
            3: {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1},
            4: {'DOWN': 3, 'LEFT': -1, 'RIGHT': 1},
            5: {'DOWN': 3, 'LEFT': -1},
            6: {'UP': -3, 'RIGHT': 1},
            7: {'UP': -3, 'LEFT': -1, 'RIGHT': 1},
            8: {'UP': -3, 'LEFT': -1},
        }

        return delta.get(blank_tile_location)

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = self.delta_calculator(state)
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

# ----------------------------------------------------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------------------------------------------------

# Manhattan algorithm explanation here:
# https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game
# https://dataaspirant.com/2015/04/11/five-most-popular-similarity-measures-implementation-in-python/
def manhattan_dist(self, node, eight_puzzle_variant=True):
    manhattan_sum = 0
    for i in range(len(self.goal)):
        manhattan_sum += coordinate_calculation(node.state.index(i), self.goal.index(i), eight_puzzle_variant)
    return manhattan_sum

def coordinate_calculation(state_coordinate, goal_coordinate, eight_puzzle_variant=True):
    coordinates = {
        0: (0, 0), 1: (1, 0), 2: (2, 0),
        3: (0, 1), 4: (1, 1), 5: (2, 1),
        6: (0, 2), 7: (1, 2), 8: (2, 2)
    } if eight_puzzle_variant else {
        0: (0, 0), 1: (1, 0),
        2: (0, 1), 3: (1, 1), 4: (2, 1), 5: (3, 1),
        6: (1, 2), 7: (2, 2), 8: (3, 2)
    }

    # take the distance of the coordinates from where it is in comparison to where it is supposed to be
    x1, y1 = coordinates.get(state_coordinate)
    x2, y2 = coordinates.get(goal_coordinate)
    return abs(x1 - x2) + abs(y1 - y2)

def run_algorithm_comparison(puzzle_arr, algorithm, eight_puzzle=True):
    num_puzzles_per_algorithm = 10

    for i in range(num_puzzles_per_algorithm):
        print("Test " + str(i + 1) + ":")

        # display puzzle being solved
        display(puzzle_arr[i].initial, eight_puzzle)

        # Grab a copy of the puzzle to not modify it
        puzzle_test = copy.deepcopy(puzzle_arr[i])
        start = 0
        end = 0

        # Run the specific test
        if algorithm == 0:
            # default heuristic
            start = datetime.datetime.now()
            a1_astar_search(puzzle_test)
            end = datetime.datetime.now()

        elif algorithm == 1:
            # manhattan heuristic
            start = datetime.datetime.now()
            a1_astar_search(puzzle_test, lambda n: manhattan_dist(puzzle_test, n, eight_puzzle))
            end = datetime.datetime.now()

        else:
            # max heuristic
            start = datetime.datetime.now()
            a1_astar_search(puzzle_test, lambda n: max(puzzle_test.h(n), manhattan_dist(puzzle_test, n, eight_puzzle)))
            end = datetime.datetime.now()

        # end = datetime.datetime.now()
        print("Time taken for test " + str(i + 1) + ": " + str(end - start) + "\n")

def display(state, eight_puzzle=True):
    list_state = list(state)

    if eight_puzzle:
        row_max_limit = 3
        current_row_amount = 0
        for i in list_state:

            # Check to make sure the current one being displayed is not the third one in the row
            if current_row_amount + 1 != row_max_limit:
                current_row_amount += 1

                if i == 0:
                    print("*", end=" ")
                else:
                    print(i, end=" ")
            else:
                current_row_amount = 0
                if i == 0:
                    print("*")
                else:
                    print(i)

    else:
        top_row_limit = 2
        middle_row_limit = 6
        bottom_row_limit = 9

        for i in range(len(state)):
            value = state[i]
            if value == 0:
                value = "*"

            if i < top_row_limit:
                if i == top_row_limit - 1:
                    print(value)
                else:
                    print(value, end=" ")

            elif i < middle_row_limit:
                if i == middle_row_limit - 1:
                    print(value)
                else:
                    print(value, end=" ")

            else:
                if i == bottom_row_limit - 1:
                    print(value)
                else:
                    if i == middle_row_limit:
                        print(" ", end=" ")

                    print(value, end=" ")

def make_rand_8puzzle():
    # Set the parameter to stop the loop, the default permutation, and the temp_puzzle
    permutation_solvable = False
    initial_permutation = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    temp_puzzle = EightPuzzle(initial_permutation)

    # Final permutation will go here after one that is solvable is found
    final_permutation = []

    # while we don't have a solvable permutation, permute and test again
    while not permutation_solvable:
        random.shuffle(initial_permutation)
        permutation_solvable = temp_puzzle.check_solvability(initial_permutation)

        # Set the final permutation variable
        if permutation_solvable:
            final_permutation = tuple(initial_permutation)

    # Generate the new puzzle with the final permutation
    return EightPuzzle(final_permutation)

def swap_arr_locations(original, destination, state):
    state[original], state[destination] = state[destination], state[original]
    return state

def make_rand_duck_puzzle():
    initial_permutation = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    temp_puzzle = DuckPuzzle(initial_permutation)
    loop_permutation_arr = initial_permutation

    for i in range(1000):
        possible_moves = temp_puzzle.actions(loop_permutation_arr)

        # shuffle the possible moves to make the selection completely random
        random.shuffle(possible_moves)
        move_index_to_make = random.randrange(len(possible_moves))
        move_direction = possible_moves[move_index_to_make]

        # ---------------- HANDLE ARRAY INDEX SWAPPING FOR THE ARRAY PERMUTATION ----------------
        loop_permutation_arr = temp_puzzle.result(loop_permutation_arr, move_direction)

    return DuckPuzzle(loop_permutation_arr)

def eight_puzzle_test():
    print("Eight Puzzle Test:")

    # Create the 10 puzzles that will be used for testing each algorithm
    puzzle1 = make_rand_8puzzle()
    puzzle2 = make_rand_8puzzle()
    puzzle3 = make_rand_8puzzle()
    puzzle4 = make_rand_8puzzle()
    puzzle5 = make_rand_8puzzle()
    puzzle6 = make_rand_8puzzle()
    puzzle7 = make_rand_8puzzle()
    puzzle8 = make_rand_8puzzle()
    puzzle9 = make_rand_8puzzle()
    puzzle10 = make_rand_8puzzle()

    puzzle_arr = [puzzle1, puzzle2, puzzle3,
                  puzzle4, puzzle5, puzzle6,
                  puzzle7, puzzle8, puzzle9,
                  puzzle10]

    # Test each algorithm
    num_algorithms_testing = 3

    for i in range(num_algorithms_testing):
        if i == 0:
            print("Testing Misplaced Tile:")
        elif i == 1:
            print("Testing Manhattan:")
        else:
            print("Testing Max of Misplaced and Manhattan:")

        algorithm_set_start = datetime.datetime.now()
        run_algorithm_comparison(puzzle_arr, i, True)
        algorithm_set_end = datetime.datetime.now()

        if i == 0:
            print("Misplaced Tile Set Total Time: " + str(algorithm_set_end - algorithm_set_start))
            print("-------------------------------------------------------------------------------\n")
        elif i == 1:
            print("Manhattan Set Total Time: " + str(algorithm_set_end - algorithm_set_start))
            print("-------------------------------------------------------------------------------\n")
        else:
            print("Max Sum Set Total Time: " + str(algorithm_set_end - algorithm_set_start))
            print("-------------------------------------------------------------------------------\n")


def duck_puzzle_test():
    print("Duck Puzzle Test:")

    # Create the 10 puzzles that will be used for testing each algorithm
    puzzle1 = make_rand_duck_puzzle()
    puzzle2 = make_rand_duck_puzzle()
    puzzle3 = make_rand_duck_puzzle()
    puzzle4 = make_rand_duck_puzzle()
    puzzle5 = make_rand_duck_puzzle()
    puzzle6 = make_rand_duck_puzzle()
    puzzle7 = make_rand_duck_puzzle()
    puzzle8 = make_rand_duck_puzzle()
    puzzle9 = make_rand_duck_puzzle()
    puzzle10 = make_rand_duck_puzzle()

    puzzle_arr = [puzzle1, puzzle2, puzzle3,
                  puzzle4, puzzle5, puzzle6,
                  puzzle7, puzzle8, puzzle9,
                  puzzle10]

    # Test each algorithm
    num_algorithms_testing = 3

    for i in range(num_algorithms_testing):
        if i == 0:
            print("Testing Misplaced Tile:")
        elif i == 1:
            print("Testing Manhattan:")
        else:
            print("Testing Max of Misplaced and Manhattan:")

        algorithm_set_start = datetime.datetime.now()
        run_algorithm_comparison(puzzle_arr, i, False)
        algorithm_set_end = datetime.datetime.now()

        if i == 0:
            print("Misplaced Tile Set Total Time: " + str(algorithm_set_end - algorithm_set_start))
            print("-------------------------------------------------------------------------------\n")
        elif i == 1:
            print("Manhattan Set Total Time: " + str(algorithm_set_end - algorithm_set_start))
            print("-------------------------------------------------------------------------------\n")
        else:
            print("Max Sum Set Total Time: " + str(algorithm_set_end - algorithm_set_start))
            print("-------------------------------------------------------------------------------\n")

eight_puzzle_test()
duck_puzzle_test()