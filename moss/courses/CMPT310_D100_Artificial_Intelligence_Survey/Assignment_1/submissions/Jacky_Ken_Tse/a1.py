"""
A1.py
Created By: Jacky Ken Tse, 301301625, jktse@sfu.ca

Citations:
    -https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
    Specifically for the manhattan code of both 8 puzzle and duck puzzle. (duck puzzle is a modified one)
    In the comments for their respective function I also have it stated I used a fragment from this stackoverflow.
"""


import sys
import os
import time
# Please update to the path of aima-python
sys.path.insert(0, 'C:\\Users\\Jacky\\Desktop\\SFU Stuff\\Cmpt 310\\Assignment1\\aima-python')
from search import *  # This should run without error messages
from utils import *


puzzle_states = []
misplace_steps = []
misplace_frontier = []
misplace_time = []
manhattan_steps = []
manhattan_frontier = []
manhattan_time = []
max_steps = []
max_frontier = []
max_time = []

"""
Moved code from search.py as I made some changes to them
"""


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    frontier_removed = 0
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    return_value = []
    while frontier:
        node = frontier.pop()
        frontier_removed = frontier_removed + 1
        if problem.goal_test(node.state):
            if display:
                """
                Mainly added print statements to show what happened.
                Also changed the return from just a node to a list containing node and a variable.
                """
                print("Number of steps to get to the solution: ", len(Node.solution(node)))
                print("The steps to get to the solution: ", Node.solution(node))
                print("Number of frontier removed: ", frontier_removed)
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                return_value.append(node)
                return_value.append(frontier_removed)
            return return_value
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
End of code copied directly over from search.py
"""


class DuckPuzzle(Problem):
    """ Duck puzzle code that uses the EightPuzzle code in search.py """

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

        if index_blank_square in {0, 2, 6}:
            possible_actions.remove('LEFT')
        if index_blank_square in {0, 1, 4, 5}:
            possible_actions.remove('UP')
        if index_blank_square in {1, 5, 8}:
            possible_actions.remove('RIGHT')
        if index_blank_square in {2, 6, 7, 8}:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank > 3:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Misplace heuristic copied from the method below. """
        b = node.state
        g = self.goal
        val = 0
        for j in range(1, 9):
            if b.index(j) != g.index(j):
                val = val + 1
        return val


def make_rand_duck_puzzle():
    """
    Starting with the goal state we will randomly choose a valid move for a random number of time between 1000 to 10000
    Initially it was 10 to 100 but I frequently got puzzles that can be solved in 5 or less steps
    Once all random move have been applied we will receive a solvable random duck_puzzle.
    Observation, no matter how many moves I make 1,2,3 will never get out of the corner.
    """
    shuffled_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = DuckPuzzle(shuffled_tuple)
    for j in range(random.randint(10000, 100000)):
        possible_actions = puzzle.actions(shuffled_tuple)
        random_action = random.randint(0, len(possible_actions)-1)
        shuffled_tuple = puzzle.result(shuffled_tuple, possible_actions[random_action])
        puzzle.initial = shuffled_tuple
    return puzzle


def display_duck_puzzle(state, goal=False):
    """
    A helper function to help visualize the duck puzzle
    """
    concat_string = ""
    if goal:
        print("Goal")
        when_zero = state.find_blank_square(state.goal)
        display_tuple = state.goal
    else:
        when_zero = state.find_blank_square(state.initial)
        display_tuple = state.initial
    for j in range(9):
        if j == when_zero:
            concat_string = concat_string + " *"
        else:
            concat_string = concat_string + " " + str(display_tuple[j])
        if j in {1, 5}:
            concat_string = concat_string + os.linesep
            if j == 5:
                concat_string = concat_string + "  "
    print(concat_string)


def make_rand_8puzzle():
    """
    Randomizes a solvable 8 puzzle. Uses random.sample to shuffle the values in the tuple
    if the shuffled value is not solvable, we will shuffle again until we have a solvable one.
    """
    goal_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    rand_tuple = tuple(random.sample(goal_tuple, len(goal_tuple)))
    puzzle = EightPuzzle(rand_tuple)
    while not puzzle.check_solvability(puzzle.initial):
        rand_tuple = tuple(random.sample(goal_tuple, len(goal_tuple)))
        puzzle.initial = rand_tuple
    return puzzle


def display_8puzzle(state, goal=False):
    """
    A helper function to help visualize the 8 puzzle
    """
    concat_string = ""
    if goal:
        print("Goal")
        when_zero = state.find_blank_square(state.goal)
        display_tuple = state.goal
    else:
        when_zero = state.find_blank_square(state.initial)
        display_tuple = state.initial
    for j in range(9):
        if j == when_zero:
            concat_string = concat_string + " *"
        else:
            concat_string = concat_string + " " + str(display_tuple[j])
        if (j+1) % 3 == 0:
            concat_string = concat_string + os.linesep
    print(concat_string)


def generate_misplace(node):
    """
    Replaced the misplaced heuristic that search.py as it included the blank
    can be used for both 8 puzzle and duck puzzle.
    """
    b = node.state
    g = currentPuzzle.goal
    val = 0
    for j in range(1, 9):
        if b.index(j) != g.index(j):
            val = val + 1
    return val


def generate_manhattan_duck_puzzle(node):
    """
    Generates a manhattan heuristic for duck puzzle,
    values 1, 2, 3 after some testing seems to never leave to top 2 by 2 square in the puzzle thus ran an algorithm for
    2 by 2. While 4, 5, 6, 7, 8 were stuck in the 2 by 3 thus had an algorithm for a 3 by 3
    The idea based from:
    https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
    without the help for a 3 by 3 I never would have noticed the relation with // and y value.
    """
    b = node.state
    g = currentPuzzle.goal
    val = 0
    for j in range(1, 9):
        if j < 4:
            temp = abs(((b.index(j)) % 2) - (g.index(j) % 2)) + abs(((b.index(j)) // 2) - (g.index(j) // 2))
        else:
            temp = abs(((b.index(j)-3) % 3) - ((g.index(j)-3) % 3)) + abs(((b.index(j)-3) // 3) - ((g.index(j)-3) // 3))
        val = val + temp
    return val


def generate_manhattan_8puzzle(node):
    """
    Received help from:
    https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
    Takes in a Node class from search.py and returns the heuristic value for the current state of the node
    """
    b = node.state
    g = currentPuzzle.goal
    val = 0
    for j in range(1, 9):
        temp = abs(((b.index(j)) % 3) - (g.index(j) % 3)) + abs(((b.index(j)) // 3) - (g.index(j) // 3))
        val = val + temp
    return val


def max_heuristic_8(node):
    """
    Calls generate_misplace and generate_manhattan and returns the max of the two.
    """
    manhattan = generate_manhattan_8puzzle(node)
    misplace = generate_misplace(node)
    return max(misplace, manhattan)


def max_heuristic_duck(node):
    """
    Calls generate_misplace and generate_manhattan and returns the max of the two.
    """
    manhattan = generate_manhattan_duck_puzzle(node)
    misplace = generate_misplace(node)
    return max(misplace, manhattan)


def solve_misplaced(puzzle):
    """
    Solves the 8 puzzle and duck puzzle using the misplaced tile heuristic
    It also puts all the data for the current run into a list in order to compile the 10 runs easily
    """
    print("Starting Misplaced Tile Heuristic for: ", puzzle.initial)
    start_time = time.time()
    returned_value = astar_search(puzzle, generate_misplace, display=True)
    elapsed_time = time.time() - start_time
    misplace_steps.append(len(Node.solution(returned_value[0])))
    misplace_frontier.append(returned_value[1])
    misplace_time.append(round(elapsed_time, 6))
    print("Elapsed Time (in seconds): ", elapsed_time, " sec")


def solve_manhattan(puzzle, duck):
    """
    Solves the 8 puzzle using the manhattan distance heuristic
    It also puts all the data for the current run into a list in order to compile the 10 runs easily
    """
    print("Starting manhattan distance heuristic for: ", puzzle.initial)
    if duck:
        print("Duck: ")
        start_time = time.time()
        returned_value = astar_search(puzzle, generate_manhattan_duck_puzzle, display=True)
        elapsed_time = time.time() - start_time
    else:
        print("8: ")
        start_time = time.time()
        returned_value = astar_search(puzzle, generate_manhattan_8puzzle, display=True)
        elapsed_time = time.time() - start_time
    manhattan_steps.append(len(Node.solution(returned_value[0])))
    manhattan_frontier.append(returned_value[1])
    manhattan_time.append(round(elapsed_time, 6))
    print("Elapsed Time (in seconds): ", elapsed_time, " sec")


def solve_max(puzzle, duck):
    """
    Solves the 8 puzzle using the max between the manhattan distance heuristic and misplace tile
    It also puts all the data for the current run into a list in order to compile the 10 runs easily
    """
    print("Starting max heuristic for: ", puzzle.initial)
    if duck:
        print("Duck: ")
        start_time = time.time()
        returned_value = astar_search(puzzle, max_heuristic_duck, display=True)
        elapsed_time = time.time() - start_time
    else:
        print("8: ")
        start_time = time.time()
        returned_value = astar_search(puzzle, max_heuristic_8, display=True)
        elapsed_time = time.time() - start_time
    max_steps.append(len(Node.solution(returned_value[0])))
    max_frontier.append(returned_value[1])
    max_time.append(round(elapsed_time, 6))
    print("Elapsed Time (in seconds): ", elapsed_time, " sec")


if __name__ == '__main__':
    print("Pressing 'y' will run duck puzzle, anything else will default to 8 puzzle")
    which_puzzle = input("Run Duck Puzzle? (y/n): ")
    if which_puzzle == 'y':
        print("Starting Duck puzzle...")
        for i in range(1, 11):
            currentPuzzle = make_rand_duck_puzzle()
            if i == 1:
                print("Goal of the Duck puzzle is: ")
                display_8puzzle(currentPuzzle, True)
            print("\n Current test: ", i)
            display_duck_puzzle(currentPuzzle)
            puzzle_states.append(currentPuzzle.initial)
            solve_misplaced(currentPuzzle)
            print(os.linesep)
            solve_manhattan(currentPuzzle, True)
            print(os.linesep)
            solve_max(currentPuzzle, True)
    else:
        print("Starting 8 puzzle...")
        for i in range(1, 11):
            currentPuzzle = make_rand_8puzzle()
            if i == 1:
                print("Goal of the 8 puzzle is: ")
                display_8puzzle(currentPuzzle, True)
            print("\n Current test: ", i)
            display_8puzzle(currentPuzzle)
            puzzle_states.append(currentPuzzle.initial)
            solve_misplaced(currentPuzzle)
            print(os.linesep)
            solve_manhattan(currentPuzzle, False)
            print(os.linesep)
            solve_max(currentPuzzle, False)

    print("All puzzle states: ", puzzle_states)
    print(os.linesep)
    print("Data for the misplace tile heuristic: ")
    print("Steps: ", misplace_steps)
    print("Removed Frontiers: ", misplace_frontier)
    print("Time: ", misplace_time)
    print(os.linesep)
    print("Data for the manhattan distance heuristic: ")
    print("Steps: ", manhattan_steps)
    print("Removed Frontiers: ", manhattan_frontier)
    print("Time: ", manhattan_time)
    print(os.linesep)
    print("Data for the max heuristic: ")
    print("Steps: ", max_steps)
    print("Removed Frontiers: ", max_frontier)
    print("Time: ", max_time)
