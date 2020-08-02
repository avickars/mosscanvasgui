# a1.py
import time
from search import *
import random

# Constants used for printing info
misplaced_tiles_text = "-------------------- Misplaced Tiles --------------------"
manhattan_text = "----------------------- Manhattan -----------------------"
max_man_tiles_text = "---------- Max of Manhattan & Misplaced Tiles -----------"


def make_rand_8puzzle():
    """Create 8puzzle with solvable initial state"""
    initial_state = (1,2,3,4,5,6,7,8,0)
    is_solvable = False
    while not is_solvable:
        initial_state = tuple(random.sample(range(0, 9), 9))
        problem = Problem(initial=initial_state)
        puzzle = EightPuzzle(initial=problem)
        is_solvable = puzzle.check_solvability(state=initial_state)

    return initial_state


def make_rand_duck_puzzle():
    """Creates a valid initial state for the duck-puzzle by randomly moving tiles, using legal moves"""
    # Create new instance of DuckPuzzle
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    problem = Problem(initial=state)
    duck = DuckPuzzle(initial=problem)

    # Make random moves to generate valid state
    num_moves = 5000
    for i in range(num_moves):
        possible_actions = duck.actions(state) # get list of possible actions for current state
        action = random.choice(possible_actions) # choose a random action from the list
        state = duck.result(state, action) # apply the random action to the current state

    # Return the random initial state
    return state


def display(state):
    """Prints 8puzzle state"""
    for i in range(0, 9):
        num = state[i]
        if i != 3 and i != 6:
            if num != 0:
                print(num, end=" ")
            else:
                print("*", end=" ")
        else:
            if num != 0:
                print("\n" + str(num), end=" ")
            else:
                print("\n" + "*", end=" ")
    print()


def display_duck(state):
    """Prints duck-puzzle state"""
    for i in range(0, 9):
        num = state[i]
        if i != 2 and i != 6:
            if num != 0:
                print(num, end=" ")
            else:
                print("*", end=" ")
        else:
            if i == 6:
                if num != 0:
                    print("\n" + "  " + str(num), end=" ")
                else:
                    print("\n" + "  " + "*", end=" ")
            else:
                if num != 0:
                    print("\n" + str(num), end=" ")
                else:
                    print("\n" + "*", end=" ")
    print()


def misplaced_tiles(node):
    """Misplaced tiles formula
    Note: The default misplaced tiles in EightPuzzle includes the 0 tile in its calculation, according to the textbook
    we should not include it, so re-wrote that formula to exclude 0"""
    goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    state = node.state
    misplaced_tiles_count = 0
    for (s, g) in zip(state, goal):
        if s != g and g != 0: # do not include 0 tile in calculation
            misplaced_tiles_count = misplaced_tiles_count+1

    return misplaced_tiles_count


def manhattan_distance(node):
    """Manhattan distance formula
    Reference: http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html"""
    state = node.state
    index = [[0, 2], [1, 2], [2, 2], [0, 1], [1, 1], [2, 1], [0, 0], [1, 0], [2, 0]]
    index_state = {}
    index_goal = {1: [0, 2], 2: [1, 2], 3: [2, 2], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 0], 8: [1, 0], 0: [2, 0]}
    x_tile=0
    y_tile=0
    mhd = 0

    # Get indexes of current state
    for i in range(len(state)):
        index_state[state[i]] = index[i]

    for i in range(len(state)):
        if state[i] != 0: # do not include 0 tile in calculation
            x_tile = abs(index_state[i][0] - index_goal[i][0])
            y_tile = abs(index_state[i][1] - index_goal[i][1])
            mhd = (x_tile + y_tile) + mhd

    return mhd

def manhattan_distance_duck(node):
    """Manhattan distance formula for duck-puzzle
    Different coordinates needed compared to 8puzzle
    Reference: http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html"""
    state = node.state
    index = [[0, 2], [1, 2], [0, 1], [1, 1], [2, 1], [3, 1], [1, 0], [2, 0], [3, 0]]
    index_state = {}
    index_goal = {1: [0, 2], 2: [1, 2], 3: [0, 1], 4: [1, 1], 5: [2, 1], 6: [3, 1], 7: [1, 0], 8: [2, 0], 0: [3, 0]}
    x_tile=0
    y_tile=0
    mhd = 0

    # Get indexes of current state
    for i in range(len(state)):
        index_state[state[i]] = index[i]

    for i in range(len(state)):
        if state[i] != 0: # do not include 0 tile in calculation
            x_tile = abs(index_state[i][0] - index_goal[i][0])
            y_tile = abs(index_state[i][1] - index_goal[i][1])
            mhd = (x_tile + y_tile) + mhd

    return mhd


def max_manhattan_misplaced_tiles(node):
    """Returns max of manhattan and misplaced tiles"""
    state = node.state
    goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    misplaced_tiles_count = misplaced_tiles(node)
    manhattan_count = manhattan_distance(node)
    return max(misplaced_tiles_count, manhattan_count)

def max_manhattan_misplaced_tiles_duck(node):
    """Returns max of manhattan and misplaced tiles for duck-puzzle"""
    state = node.state
    goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    misplaced_tiles_count = misplaced_tiles(node)
    manhattan_count = manhattan_distance_duck(node)
    return max(misplaced_tiles_count, manhattan_count)


def print_info(heuristic_name, elapsed_time, solution_length, frontier_nodes_removed):
    """Prints info for the solved puzzles"""
    print(heuristic_name)
    print("Elapsed Time (in seconds): " + "{:.5f}".format(elapsed_time) + "s")
    print("Solution length: " + str(solution_length))
    print("Nodes removed from frontier: " + str(frontier_nodes_removed))


# ______________________________________________________________________________________________________________________
# Needed to add code to best_first_graph_search to get the the length (i.e. number of tiles moved) of the solution,
# and the that total number of nodes that were removed from frontier, so copied code from search.py here
def astar_search_assignment1(problem, h=None):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_assignment1(problem, lambda n: n.path_cost + h(n))

def best_first_graph_search_assignment1(problem, f):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    frontier_nodes_removed = 0 # counter for nodes removed from frontier

    while frontier:
        node = frontier.pop()

        frontier_nodes_removed = frontier_nodes_removed + 1

        if problem.goal_test(node.state):
            solution_length = len(node.solution())
            return solution_length, frontier_nodes_removed

        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None
# ______________________________________________________________________________________________________________________


# ______________________________________________________________________________________________________________________
class DuckPuzzle(Problem):
    """ Problem class called DuckPuzzle that is the same as the 8-puzzle, except the board looks a bit like a duck
    facing to the left"""
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

        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # If the blank is within the first 3 squares in the top left
        if blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        # If the blank is equal to the fourth tile
        if blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        # If the blank is within the last 5 squares in the bottom right
        if blank > 3:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal
# ______________________________________________________________________________________________________________________


# ______________________________________________________________________________________________________________________
def question2():
    """Code for question 2: Comparing Algorithms"""
    n = 10 # number of puzzles to generate
    initial_state_list = []

    # Generate n initial states for the 8-puzzle
    for i in range(n):
        initial_state = make_rand_8puzzle()
        initial_state_list.append(initial_state)

    # A*-search using different heruistics for 8puzzle
    for i in range(n):
        # Display puzzle
        print("Puzzle-" + str(i+1))
        display(initial_state_list[i])

        # A* search using the misplaced tile heuristic
        start_time = time.time()
        solution_length, frontier_nodes_removed = astar_search_assignment1(EightPuzzle(initial_state_list[i]),
                                                                      h=misplaced_tiles)
        elapsed_time = time.time() - start_time
        print_info(misplaced_tiles_text, elapsed_time, solution_length, frontier_nodes_removed)

        # A*-search using the Manhattan distance heuristic
        start_time = time.time()
        solution_length, frontier_nodes_removed = astar_search_assignment1(EightPuzzle(initial_state_list[i]),
                                                                      h=manhattan_distance)
        elapsed_time = time.time() - start_time
        print_info(manhattan_text, elapsed_time, solution_length, frontier_nodes_removed)

        # A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic
        start_time = time.time()
        solution_length, frontier_nodes_removed = astar_search_assignment1(EightPuzzle(initial_state_list[i]),
                                                               h=max_manhattan_misplaced_tiles)
        elapsed_time = time.time() - start_time
        print_info(max_man_tiles_text, elapsed_time, solution_length, frontier_nodes_removed)

        # Some space between puzzles
        print()
        print()
# ______________________________________________________________________________________________________________________


# ______________________________________________________________________________________________________________________
def question3():
    """Code for question 3: The House Puzzle"""
    n = 10 # number of puzzles to generate
    initial_state_list = []

    # Generate n initial states for the duck-puzzle
    for i in range(n):
        initial_state = make_rand_duck_puzzle()
        initial_state_list.append(initial_state)

    # A*-search using different heruistics for duck-puzzle
    for i in range(n):
        # Display puzzle
        print("Puzzle-" + str(i+1))
        display_duck(initial_state_list[i])

        # A* search using the misplaced tile heuristic
        start_time = time.time()
        solution_length, frontier_nodes_removed = astar_search_assignment1(DuckPuzzle(initial_state_list[i]),
                                                                           h=misplaced_tiles)
        elapsed_time = time.time() - start_time
        print_info(misplaced_tiles_text, elapsed_time, solution_length, frontier_nodes_removed)

        # # A*-search using the Manhattan distance heuristic
        start_time = time.time()
        solution_length, frontier_nodes_removed = astar_search_assignment1(DuckPuzzle(initial_state_list[i]),
                                                                           h=manhattan_distance_duck)
        elapsed_time = time.time() - start_time
        print_info(manhattan_text, elapsed_time, solution_length, frontier_nodes_removed)

        # A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic
        start_time = time.time()
        solution_length, frontier_nodes_removed = astar_search_assignment1(DuckPuzzle(initial_state_list[i]),
                                                                           h=max_manhattan_misplaced_tiles_duck)
        elapsed_time = time.time() - start_time
        print_info(max_man_tiles_text, elapsed_time, solution_length, frontier_nodes_removed)

        # Some space between puzzles
        print()
        print()
# ______________________________________________________________________________________________________________________


def main():
    print("|||||||||||||||||||||| QUESTION 2 |||||||||||||||||||||||")
    question2()
    print("\n\n" + "|||||||||||||||||||||| QUESTION 3 |||||||||||||||||||||||")
    question3()


if __name__ == "__main__":
    main()




