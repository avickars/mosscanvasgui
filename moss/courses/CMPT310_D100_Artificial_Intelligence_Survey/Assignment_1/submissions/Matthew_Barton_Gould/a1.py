# a1.py
import random
import time
import csv
from search import *


#### Modified best_first_graph_search (search.py) to include count  ####
#### of nodes removed from the frontier. Returns a list of this     ####
#### count along with the goal node.                                ####
########################################################################

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    removed_count = 0
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        removed_count = removed_count + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                print("nodes removed from frontier ", removed_count)
            return [node, removed_count]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


#### 8 puzzle functions ####
############################

def make_rand_8puzzle():
    """Generates a random permutation state of the 8 puzzle by making random valid moves."""

    # start with a solved state and mix up randomly
    curr_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = EightPuzzle(curr_state)

    # for a random number of moves
    for i in range(0, random.randint(10, 10000)):
        valid_moves = puzzle.actions(curr_state)

        # select random move and make it
        curr_state = puzzle.result(curr_state, random.choice(valid_moves))

    return curr_state


def display_8puzzle(state):
    """Print a state of the 8 puzzle."""
    print("\n")
    col = 1
    for tile in state:
        if(tile == 0):
            print(" * ", end='')
        else:
            print(" " + str(tile) + " ", end='')
        if(col == 3):
            col = 1
            print("\r")
        else:
            col = col + 1
    print("\n")


#### Heuristic functions ####
#############################

def misplaced_8puzzle(node):
    """Misplaced tiles distance  ** not including the blank ** from goal same function for the 8puzzle."""
    return sum(s != g and s != 0 for (s, g) in zip(node.state, (1, 2, 3, 4, 5, 6, 7, 8, 0)))


def manhattan_8puzzle(node):
    """Manhattan distance from goal for each tile ** not including the blank ** in the 8 puzzle"""
    distance = 0
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    state = node.state

    # Use modulus and remainder to determine row/col then calculate Manhattan distance
    for tile in range(1, 9):
        col_state = state.index(tile) % 3
        row_state = state.index(tile) // 3

        col_goal = goal.index(tile) % 3
        row_goal = goal.index(tile) // 3
        distance += abs(col_state - col_goal) + abs(row_state - row_goal)

    return(distance)


def max_misplaced_manhattan_8puzzle(node):
    """Max of the misplaced_tile and Manhattan distances for 8 puzzle"""
    return(max(misplaced_8puzzle(node), manhattan_8puzzle(node)))


def misplaced_duck(node):
    """Misplaced tiles distance  ** not including the blank ** from goal same function for the duck puzzle."""
    return sum(s != g and s != 0 for (s, g) in zip(node.state, (1, 2, 3, 4, 5, 6, 7, 8, 0)))


def duck_offset(tile_index):
    """ Returns an offset version of tile index so that it is the same as 3 row 4 col puzzle board size"""
    if(tile_index > 1):  # middle row
        return(tile_index + 2)
    elif(tile_index > 5):
        return(tile_index + 3)
    else:
        return(tile_index)


def manhattan_duck(node):
    """Manhattan distance from goal for each tile ** not including the blank ** for the duck puzzle"""
    distance = 0
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    state = node.state

    # Use modulus and remainder to determine row/col and then calculate Manhattan distance
    for tile in range(1, 9):
        col_state = duck_offset(state.index(tile)) % 4
        row_state = duck_offset(state.index(tile)) // 3

        col_goal = duck_offset(goal.index(tile)) % 4
        row_goal = duck_offset(goal.index(tile)) // 3
        distance += abs(col_state - col_goal) + abs(row_state - row_goal)

    return(distance)


def max_misplaced_manhattan_duck(node):
    """Max of the misplaced_tile and Manhattan distances for duck puzzle"""
    return(max(misplaced_duck(node), manhattan_duck(node)))


#### duck puzzle functions and class ####
#########################################

def make_rand_duck_puzzle():
    """Generates a random permutation state of the duck puzzle by making random valid moves."""
    curr_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = DuckPuzzle(curr_state)

    # for a random number of moves
    for i in range(0, random.randint(10, 10000)):
        valid_moves = puzzle.actions(curr_state)

        # select random move and make it
        curr_state = puzzle.result(curr_state, random.choice(valid_moves))

    return curr_state


def display_duck_puzzle(state):
    """Print a state of the duck puzzle."""
    print("\n")
    row = 1
    col = 1
    for tile in state:
        if(tile == 0):
            print(" * ", end='')
        else:
            print(" " + str(tile) + " ", end='')

        if(col == 2 and row == 1):
            col = 1
            row = row + 1
            print("\r")
        elif(col == 4 and row == 2):
            col = 1
            row = row + 1
            print("\r")
            print("   ", end='')
        else:
            col = col + 1

    print("\n")


# This class is based off modified from the 8puzzle class in search.py
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a board shaped like a duck, where one of the
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

        # hard code the possible moves given the duck shape
        if(index_blank_square == 0):
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        elif(index_blank_square == 1):
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        elif(index_blank_square == 2 or index_blank_square == 6):
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif(index_blank_square == 4):
            possible_actions.remove('UP')
        elif(index_blank_square == 5):
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        elif(index_blank_square == 7):
            possible_actions.remove('DOWN')
        elif(index_blank_square == 8):
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # hard code the offset depending on section of duck puzzle
        if (blank == 0 or blank == 1 or blank == 2):
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif (blank == 3):
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[action]

        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal


#### Functions for comparing the different heuristics on the 8/duck puzzle ####
###############################################################################

def write_to_csv(filename, data):
    """Writes data generated in compare_heuristics to csv for import into spreadsheet."""
    with open(filename, mode='w') as algo_compare:
        writer = csv.writer(algo_compare)
        writer.writerow(["Elapsed time (s)", "Length of the solution", "Nodes removed from frontier"])
        writer.writerows(data)


def compare_heuristics(random_puzzle_gen, puzzle_class, num_reps, question_string, duck=False):
    """Takes argument puzzle class and generator and compares time to solution, length of solution
    and # of nodes removed from frontier for the three heuristics. Repeats comparison num_reps times and
    writes results out to csv."""

    # arrays of arrays for results
    mis_data = [[0 for cols in range(3)] for rows in range(num_reps)]
    manhat_data = [[0 for cols in range(3)] for rows in range(num_reps)]
    max_mis_manhat_data = [[0 for cols in range(3)] for rows in range(num_reps)]

    for i in range(num_reps):
        # print progress
        print(question_string + " rep " + str(i))

        # generate random puzzle for test
        rand_puzzle = random_puzzle_gen()

        # A* search with misplaced tile heuristic
        puzzle = puzzle_class(rand_puzzle)
        start_time = time.time()
        search_info = astar_search(puzzle, h=misplaced_duck if duck else misplaced_8puzzle)
        mis_data[i][0] = time.time() - start_time
        mis_data[i][1] = len(search_info[0].solution())
        mis_data[i][2] = search_info[1]

        # A* search with Manhattan distance heuristic
        puzzle = puzzle_class(rand_puzzle)
        start_time = time.time()
        search_info = astar_search(puzzle, h=manhattan_duck if duck else manhattan_8puzzle)
        manhat_data[i][0] = time.time() - start_time
        manhat_data[i][1] = len(search_info[0].solution())
        manhat_data[i][2] = search_info[1]

        # A* search using the max of misplaced tile heuristic and Manhattan distance heuristic
        puzzle = puzzle_class(rand_puzzle)
        start_time = time.time()
        search_info = astar_search(puzzle, h=max_misplaced_manhattan_duck if duck else max_misplaced_manhattan_8puzzle)
        max_mis_manhat_data[i][0] = time.time() - start_time
        max_mis_manhat_data[i][1] = len(search_info[0].solution())
        max_mis_manhat_data[i][2] = search_info[1]

    write_to_csv("mis_data_" + question_string + ".csv", mis_data)
    write_to_csv("manhat_data_" + question_string + ".csv", manhat_data)
    write_to_csv("max_mis_manhat_data_" + question_string + ".csv", max_mis_manhat_data)


def main():
    # demo display random puzzles
    display_8puzzle(make_rand_8puzzle())

    display_duck_puzzle(make_rand_duck_puzzle())

    # number of times to repeat comparison
    num_reps = 30

    # question 2 :
    compare_heuristics(make_rand_8puzzle, EightPuzzle, num_reps=num_reps, question_string="q2", duck=False)

    # question 3 :
    compare_heuristics(make_rand_duck_puzzle, DuckPuzzle, num_reps=num_reps, question_string="q3", duck=True)


if __name__ == "__main__":
    main()
