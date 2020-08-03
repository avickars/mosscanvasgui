"""
a1.py
Author: Bao (Tyler) Trinh
ID: 301319439
Email: bvtrinh@sfu.ca
"""


from search import *
from random import shuffle, choice, randint
from time import time
import json


""" -------------------------- PART 1 --------------------------"""
def make_rand_8puzzle():
    """ Creates a new EightPuzzle problem with a random initial state that is 
    solvable."""

    # Initial state should be in the range 0-8 inclusive
    state = [i for i in range(9)]

    # Shuffle the numbers
    shuffle(state)

    # Check if this state is solvable
    problem = EightPuzzle(tuple(state))

    # Unsolvable state to test with
    # state = [8, 1, 2, 0, 4, 3, 7, 6, 5]
    while(not problem.check_solvability(state)):
        # Continue to shuffle until the problem is solvable
        shuffle(state)

    # display(state)
    solvable_problem = EightPuzzle(tuple(state))
    return solvable_problem


def display(state):
    """ Displays the state in a neat and readable representation of it """

    for index, item in enumerate(state):
        # Print the element
        if (item == 0):
            print("*", end=" ")
        else:
            print(item, end=" ")

        # Print a newline every 3 elements
        if ((index + 1) % 3 == 0):
            print()


""" -------------------------- PART 2 --------------------------"""

# From search.py
def astar_search_custom(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# From search.py
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
            return node, (len(explored) + 1)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def mismatch_heuristic(puzzle):
    """ Solves the 8-puzzle using the misplaced tile heristic """

    print("MIS,", end="")
    start_time = time()
    puzzle_search, num_removed = astar_search_custom(puzzle,h=h_misplaced)
    total_time = time() - start_time
    return show_stats(puzzle_search, total_time, num_removed)


def manhattan_heuristic(puzzle, standard=True):
    """ Solves the 8-puzzle using the Manhattan distance heristic """

    print("MAN,", end="")

    if standard:
        start_time = time()
        puzzle_search,num_removed = astar_search_custom(puzzle, h=h_manhattan)
        total_time = time() - start_time
    else:
        start_time = time()
        puzzle_search, num_removed = astar_search_custom(puzzle, h=puzzle.h_duck_manhattan)
        total_time = time() - start_time


    return show_stats(puzzle_search, total_time, num_removed)


def combined_heuristic(puzzle, standard=True):
    """ Solves the 8-puzzle using the max of the misplaced tile and Manhattan distance heristic """

    print("COM,", end="")

    if standard:
        start_time = time()
        puzzle_search, num_removed = astar_search_custom(puzzle, h=lambda n: max(h_misplaced(n), h_manhattan(n)))
        total_time = time() - start_time
    else:
        start_time = time()
        puzzle_search, num_removed = astar_search_custom(puzzle, h=lambda n: max(puzzle.h(n), puzzle.h_duck_manhattan(n)))
        total_time = time() - start_time

    return show_stats(puzzle_search, total_time, num_removed)

def h_misplaced(node):
    """ Return the heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles """
    total = 0
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    for (s,g) in zip(node.state, goal):
        if s == 0 or g == 0:
            continue
        if (s != g):
            total += 1

    return total


def h_manhattan(node):
    """ Calculates the Manhattan distance of tiles 1-9 between its current and goal state """

    state = node.state
    index_state = {}
    size = 9
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}


    for i in range(size):
        col = i % 3
        row = i // 3
        index_state[state[i]] = [row, col]
    
    mhd = 0
    # Don't include the 0th tile in the calculation
    for i in range(1,9):
        mhd += abs(index_goal[i][0] - index_state[i][0]) + abs(index_goal[i][1] - index_state[i][1])

    return mhd


""" -------------------------- PART 3 --------------------------"""
# Class derived from EightPuzzle in search.py
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 duck shaped board, where one of the
    squares is a blank. A state is represented as a tuple of length 12, where  element at
    index i represents the tile number at index i (0 if it's an empty square). The board
    is in the shape of a duck so there are some null areas (indicated by -1) """

    def __init__(self, initial, goal=(1, 2, -1, -1, 3, 4, 5, 6,-1, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        # Use -1 to represent out of bound tiles
        self.clean_initial = initial
        bounded_initial = list(initial)[:]
        bounded_initial.insert(2,-1)
        bounded_initial.insert(3,-1)
        bounded_initial.insert(8,-1)

        super().__init__(tuple(bounded_initial), goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        # First column
        if index_blank_square % 4 == 0:
            possible_actions.remove('LEFT')

        # First row
        if index_blank_square < 4:
            possible_actions.remove('UP')

        # Last column
        if index_blank_square % 4 == 3:
            possible_actions.remove('RIGHT')

        # Last row
        if index_blank_square > 7:
            possible_actions.remove('DOWN')
        
        # (1,2) and (1,3)
        if index_blank_square == 6 or index_blank_square == 7:
            possible_actions.remove('UP')

        # (0,1)
        if index_blank_square == 1:
            possible_actions.remove('RIGHT')

        # (1,0)
        if index_blank_square == 4:
            possible_actions.remove('DOWN')

        # (2,1)
        if index_blank_square == 9:
            possible_actions.remove('LEFT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        total = 0
        for (s,g) in zip(node.state, self.goal):
            if s == 0 or g == 0:
                continue
            if (s != g):
                total += 1

        return total

    def h_duck_manhattan(self, node):
        """ Calculates the Manhattan distance of tiles 1-9 between its current and goal state """

        state = node.state
        index_state = {}
        skip_elements = [2, 3, 8]
        index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
        index = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3],
        [2, 0], [2, 1], [2, 2], [2, 3]]

        # Read the entire state board to determine the location of each tile
        for i in range(12):
            # Out of bound tiles
            if i in skip_elements:
                continue
            col = i % 4
            row = i // 4
            index_state[state[i]] = [row, col]
        
        mhd = 0
        # Don't include the 0th tile in the calculation
        for i in range(1,9):
            mhd += abs(index_goal[i][0] - index_state[i][0]) + abs(index_goal[i][1] - index_state[i][1])

        return mhd

def random_duck_puzzle(num_moves):
    """ Returns a DuckPuzzle with a solution of size num_moves """

    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    duck_puzzle = DuckPuzzle(goal)
    state = duck_puzzle.initial

    moves = {"LEFT": "RIGHT", "RIGHT": "LEFT", "UP": "DOWN", "DOWN": "UP"}
    last_move = ""

    # display_duck(state)
    for i in range(num_moves):
        # Get all possible moves for the blank tile
        possible_moves = duck_puzzle.actions(state)

        # Need to remove the opposite of the last move from the possible moves to prevent redundant moves
        if last_move:
            possible_moves.remove(moves[last_move])
        move = choice(possible_moves)
        last_move = move

        # Return the state of the board after
        state = duck_puzzle.result(state, move)
        # display_duck(state)

    state = list(state)
    for i in range(3):
        state.remove(-1)
    return DuckPuzzle(tuple(state))


def display_duck(state):
    """ Displays the state in a neat and readable representation of it """

    for index, item in enumerate(state):
        # Print the element
        if (item == 0):
            print("*", end=" ")
        elif (item == -1):
            print(" ", end=" ")
        else:
            print(item, end=" ")

        # Print a newline every 4 elements
        if ((index + 1) % 4 == 0):
            print()

    print()


""" -------------------------- TEST AND DEBUG --------------------------"""
def show_stats(solved_puzzle, time, num_removed):
    """ Prints the length of the solution and time """

    trial = {}
    print("{:>10},\t".format(num_removed), end="")
    print("{:>7},\t".format(len(solved_puzzle.solution())), end="")
    print("{:>8.7f} ".format(time))
    trial["removed"] = num_removed
    trial["length"] = len(solved_puzzle.solution())
    trial["time"] = time
    return trial


def show_csv(data):
    
    for alg_type in ["misplaced", "manhattan", "combined"]:
        print(alg_type)
        print("Nodes,Time(s),Length")
        for item in data:
            stat = item[alg_type] 
            print("{:},".format(stat["removed"]), end="")
            print("{:.7f}, ".format(stat["time"]), end="")
            print("{:}".format(stat["length"]))


def test_standard(iterations=10, display_csv=False):
    """ Generate 10 standard puzzles and solve them using the 3 specified heuristics """

    puzzles = []
    results = []
    print("-------------2 STANDARD PUZZLE---------------\n")
    for i in range(iterations):
        trial = {}
        print("\nTEST #{}".format(i+1))
        eight_puzzle = make_rand_8puzzle()
        trial["state"] = eight_puzzle.initial
        print(eight_puzzle.initial)

        print("TYPE,\t NODES,\t LENGTH,\t TIME(s)")

        trial["misplaced"] = mismatch_heuristic(eight_puzzle)
        trial["manhattan"] = manhattan_heuristic(eight_puzzle)
        trial["combined"] = combined_heuristic(eight_puzzle)
        puzzles.append(eight_puzzle.initial)
        results.append(trial)

    # Used when outputing data for csv sheets
    if display_csv:
        print(puzzles)
        show_csv(results)
        write_json(results, "eight_results.json")


def test_set_puzzle(puzzle):
    """ Test a given puzzle state """
    eight_puzzle = EightPuzzle(puzzle)

    if not eight_puzzle.check_solvability(puzzle):
        print("This puzzle isn't solvable")
        exit(-1)

    display(puzzle)

    print("TYPE\t NODES\t LENGTH\t TIME(s)\t")
    mismatch_heuristic(eight_puzzle)
    manhattan_heuristic(eight_puzzle)
    combined_heuristic(eight_puzzle)


def test_duck(iterations=10, display_csv=False):
    """ Generate 10 duck puzzles and solve them using the 3 specified heuristics """

    puzzles = []
    results = []
    print("-------------3 DUCK PUZZLE---------------\n")
    for i in range(iterations):
        trial = {}
        print("\nTEST #{}".format(i+1))
        duck_puzzle = random_duck_puzzle(randint(0, 10000))
        # display_duck(duck_puzzle.initial)
        trial["state"] = duck_puzzle.clean_initial
        print(duck_puzzle.clean_initial)

        print("TYPE,\t NODES,\t LENGTH,\t TIME(s)")

        trial["misplaced"] = mismatch_heuristic(duck_puzzle)
        trial["manhattan"] = manhattan_heuristic(duck_puzzle, False)
        trial["combined"] = combined_heuristic(duck_puzzle, False)
        puzzles.append(duck_puzzle.clean_initial)
        results.append(trial)
    
    # Used for outputing for csv sheets 
    if display_csv:
        print(puzzles)
        show_csv(results)
        write_json(results, "duck_results.json")


def test_set_duck(puzzle):
    """ Test a given puzzle state """
    duck_puzzle = DuckPuzzle(puzzle)

    display_duck(duck_puzzle.initial)

    print("TYPE\t NODES\t LENGTH\t TIME(s)\t")

    mismatch_heuristic(duck_puzzle)
    manhattan_heuristic(duck_puzzle, False)
    combined_heuristic(duck_puzzle, False)


def test_manhattan():
    """ Test the Manhattan heuristic """

    # These puzzle may not be solvable, only used to test Manhattan
    puzzle1 = (1, 2, 5, 6, 8, 0, 7, 4, 3)
    state1 = Node(puzzle1)

    puzzle2 = (1, 2, 4, 7, 5, 6, 0, 8, 3)
    state2 = Node(puzzle2)

    puzzle3 = (1, 2, 3, 7, 8, 0, 4, 5, 6)
    state3 = Node(puzzle3)

    puzzle4 = (1, 2, 3, 4, 5, 6, 7, 0, 8)
    state4 = Node(puzzle4)

    try:
        mhd1 = h_manhattan(state1)
        mhd2 = h_manhattan(state2)
        mhd3 = h_manhattan(state3)
        mhd4 = h_manhattan(state4)
        
        assert mhd1 == 9, "1) Calculated: {} Actual: 9".format(mhd1)
        assert mhd2 == 6, "2) Calculated: {} Actual: 6".format(mhd2)
        assert mhd3 == 5, "3) Calculated: {} Actual: 5".format(mhd3)
        assert mhd4 == 1, "4) Calculated: {} Actual: 1".format(mhd4)
        print("All standard puzzle manhattan tests passed!")
    except AssertionError as msg:
        print(msg)


def write_json(data, filename):
    """ Used to write to json files for record of final data output """
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def main():

    # ----PART 2----
    # test_manhattan()
    # puzzle = (5, 8, 1, 4, 6, 3, 7, 0 ,2)
    # puzzle = (0, 6, 8, 1, 2, 3, 4, 7, 5)
    # test_set_puzzle(puzzle)
    # test_standard(display_csv=True)
    test_standard()

    # ----PART 3----
    # puzzle = (2, 0, 1, 3, 5, 8, 4, 6, 7)
    # puzzle = (1, 2, 3, 5, 6, 8, 0, 4, 7)
    # puzzle = (3, 1, 2, 8, 5, 4, 0, 7, 6)
    # test_set_duck(puzzle)
    # test_duck(display_csv=True)
    test_duck()

if __name__ == "__main__":
    main()
    