# a1.py

from search import *
import random
import time
import pandas as pd
import matplotlib.pyplot

# Altered code from search.py...............................................................


class EightPuzzle(Problem):
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
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        """ Returns the Manhattan heuristic value for a given state """
        state = node.state
        index_goal = {1: [0, 0], 2: [0, 1], 3: [0, 2],
                      4: [1, 0], 5: [1, 1], 6: [1, 2],
                      7: [2, 0], 8: [2, 1], 0: [2, 2]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2],
                 [1, 0], [1, 1], [1, 2],
                 [2, 0], [2, 1], [2, 2]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhd_x = 0
        mhd_y = 0

        """
        in manhattan you don't really care how far is the blank tile away from its "home tile".
        Hence to ensure we do not count the empty tile or zero tile, we make sure i will never be 0 cuz it will never reference the key: 0
        """
        for i in range(1, 9):
            mhd_x += abs(index_goal[i][0] - index_state[i][0])
            mhd_y += abs(index_goal[i][1] - index_state[i][1])

        return mhd_x + mhd_y

    def max_heuristic(self, node):
        """ Returns the max value between the manhattan heuristic and misplaced tile heuristic """
        return max(self.h(node), self.manhattan(node))


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
    frontier_counter = 0  # added code: keeps track of nodes removed from frontier
    while frontier:
        node = frontier.pop()
        frontier_counter += 1  # added code: increment frontier counter when removed from frontier
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and",
                      len(frontier), "paths remain in the frontier")
            return [node, frontier_counter]  # altered code: return node and frontier counter
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


# .......................................................end of altered code from search.py

# unaltered code from search.py............................................................

""" code was copied to ensure astar_search runs best_first graph function in a1.py instead of search.py"""


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# ......................................................end of unaltered code from search.py


class DuckPuzzle(Problem):
    """

    The problem of sliding tiles numbered from 1 to 8 on a duck board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) 

    Duck puzzle board: 
    +--+--+
    |  |  |
    +--+--+--+--+
    |  |  |  |  |
    +--+--+--+--+
       |  |  |  |
       +--+--+--+

    """

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

        indexes_that_cant_move_up = [0, 1, 4, 5]
        indexes_that_cant_move_down = [2, 6, 7, 8]
        indexes_that_cant_move_left = [0, 2, 6]
        indexes_that_cant_move_right = [1, 5, 8]

        if index_blank_square in indexes_that_cant_move_left:
            possible_actions.remove('LEFT')
        if index_blank_square in indexes_that_cant_move_up:
            possible_actions.remove('UP')
        if index_blank_square in indexes_that_cant_move_right:
            possible_actions.remove('RIGHT')
        if index_blank_square in indexes_that_cant_move_down:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        """
        delta is how much tile moves it takes to do 1 action
        in other words,
        delta is the number of positions the black space has to move IN THE ARRAY OR LIST to do 1 action
        1 2
        3 * 5 6   ->   [1 ,2 ,3 ,0 ,5 ,6 ,4 ,7 ,8] 
          4 7 8
        for example, for the case above:
        if * (the blank space) moves DOWN then 0 moves 3 steps forwards in the array or list
        if * moves UP then 0 moves 2 steps backwards in the array or list
        if * moves LEFT then 0 moves 1 steps backwards in the array or list
        if * moves RIGHT then 0 moves 1 steps backwards in the array or list
        thus, delta = {'UP': 3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta_row_1 = {'UP': 0, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        delta_row_2 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        delta_row_3 = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}

        row_1 = [0, 1]
        row_2 = [2, 3, 4, 5]
        row_3 = [6, 7, 8]

        if blank in row_1:
            neighbor = blank + delta_row_1[action]
        elif blank in row_2:
            neighbor = blank + delta_row_2[action]
        elif blank in row_3:
            neighbor = blank + delta_row_3[action]

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

    def manhattan(self, node):
        """ Returns the Manhattan heuristic value for a given state """

        """ The map was altered so that the x and y index coordinates match that of a duck puzzle in a 3 x 4 matrix """

        state = node.state
        index_goal = {1: [0, 0], 2: [0, 1],
                      3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3],
                      7: [2, 1], 8: [2, 2], 0: [2, 3]}
        index_state = {}
        index = [[0, 0], [0, 1],
                 [1, 0], [1, 1], [1, 2], [1, 3],
                 [2, 1], [2, 2], [2, 3]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhd_x = 0
        mhd_y = 0

        """
        in manhattan you don't really care how far is the blank tile away from its "home tile".
        Hence to ensure we do not count the 0, we make sure i will never be 0 cuz it will never reference the key: 0
        """
        for i in range(1, 9):
            mhd_x += abs(index_goal[i][0] - index_state[i][0])
            mhd_y += abs(index_goal[i][1] - index_state[i][1])

        return mhd_x + mhd_y

    def max_heuristic(self, node):
        """ Returns the max value between the manhattan heuristic and misplaced tile heuristic """
        return max(self.h(node), self.manhattan(node))


def make_rand_8puzzle():
    """
        @INPUT: no input
        @OUTPUT: returns a new instance of an EightPuzzle problem with a random initial state that is solvable.
    """
    while(True):
        unique_ints = random.sample(range(0, 9), 9)
        unique_ints = tuple(unique_ints)
        puzzle = EightPuzzle(unique_ints)
        if puzzle.check_solvability(puzzle.initial) == True:
            return puzzle


def display(state):
    """
        @INPUT: EightPuzzle state
        @OUTPUT: prints out readable EightPuzzle state
    """
    for i in range(3):
        for j in range(3):
            if state[i*3+j] == 0:
                print(end="* ")
            else:
                print(end=str(state[i*3+j]) + " ")
        print(end="\n")


def make_rand_duckpuzzle():
    """
        @INPUT: no input
        @OUTPUT: returns a new instance of an DuckPuzzle problem with a random initial state that is solvable.
        @DESCRIPTION: we make a random puzzle by starting from the goal state and later do random number of moves to randomize it, 
                        THIS ENSURES PUZZLE SOLVABILITY.

        version 1 (same as EightPuzzle) :
        while(True):
            unique_ints = random.sample(range(0, 9), 9)
            unique_ints = tuple(unique_ints)
            puzzle = EightPuzzle(unique_ints)
            if puzzle.check_solvability(puzzle.initial) == True:
                return puzzle
    """

    goal_state = tuple([1, 2, 3, 4, 5, 6, 7, 8, 0])
    temp = goal_state
    solved_duck_puzzle = DuckPuzzle(goal_state)
    random_range = random.randint(500, 1000)

    for i in range(random_range):
        possible_actions = solved_duck_puzzle.actions(temp)
        random_move = random.choice(possible_actions)
        temp = solved_duck_puzzle.result(temp, random_move)

    randomized_puzzle = DuckPuzzle(temp)

    return randomized_puzzle


def display_duckpuzzle(state):
    """
        @INPUT: DuckPuzzle state
        @OUTPUT: prints out readable DuckPuzzle state
    """
    k = 0  # array/list index
    for i in range(3):
        for j in range(4):
            # row one
            if i == 0:
                if (j >= 0) and (j <= 1):
                    if state[k] == 0:
                        print(end="* ")
                        k += 1
                    else:
                        print(end=str(state[k]) + " ")
                        k += 1
                elif j >= 2:
                    print(end="  ")
            # row two
            if i == 1:
                if state[k] == 0:
                    print(end="* ")
                    k += 1
                else:
                    print(end=str(state[k]) + " ")
                    k += 1
            # row three
            if i == 2:
                if j == 0:
                    print(end="  ")
                elif (j >= 1) and (j <= 3):
                    if state[k] == 0:
                        print(end="* ")
                        k += 1
                    else:
                        print(end=str(state[k]) + " ")
                        k += 1
        print(end="\n")


def create_8puzzle_set(size):
    """
        @INPUT: size (int)
        @OUTPUT: returns a set of EightPuzzles of size specified by input
    """
    eight_puzzle_set=[]
    for i in range(size):
        eight_puzzle_set.append(make_rand_8puzzle())
    return eight_puzzle_set


def create_duckpuzzle_set(size):
    """
        @INPUT: size (int)
        @OUTPUT: returns a set of DuckPuzzles of size specified by input
    """
    duckpuzzle_set=[]
    for i in range(size):
        duckpuzzle_set.append(make_rand_duckpuzzle())
    return duckpuzzle_set


def analyse_8puzzle(eight_puzzle_set):
    """
        @INPUT: eight puzzle set
        @OUTPUT: logs eight puzzle analysis results
    """
    print("><><><><><><><><><><><><><>")
    print("><                       ><")
    print("<> Eight Puzzle Analysis <>")
    print("><                       ><")
    print("><><><><><><><><><><><><><>")

    for puzzle in eight_puzzle_set:

        # test casees
        # puzzle = EightPuzzle(tuple([5, 0, 8, 4, 2, 1, 7, 3, 6]))
        # puzzle = EightPuzzle(tuple([2, 7, 4, 0, 5, 6, 3, 8, 1]))
        # puzzle = EightPuzzle(tuple([4, 6, 7, 0, 8, 5, 1, 2, 3]))

        display(puzzle.initial)

        start_time = time.time()
        solution_node_and_frontier_count = astar_search(puzzle, puzzle.h)
        elapsed_time = time.time() - start_time
        print("+---------------------------+")
        print("| Misplaced Tiles Heuristic |")
        print("+---------------------------+")
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print(
            f'length of solution (number of tiles moved): {solution_node_and_frontier_count[0].path_cost}')
        print(f'number of nodes removed from frontier: {solution_node_and_frontier_count[1]}')

        start_time = time.time()
        solution_node_and_frontier_count = astar_search(puzzle, puzzle.manhattan)
        elapsed_time = time.time() - start_time
        print("+------------------------------+")
        print("| Manhattan Distance Heuristic |")
        print("+------------------------------+")
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print(
            f'length of solution (number of tiles moved): {solution_node_and_frontier_count[0].path_cost}')
        print(f'number of nodes removed from frontier: {solution_node_and_frontier_count[1]}')

        start_time = time.time()
        solution_node_and_frontier_count = astar_search(puzzle, puzzle.max_heuristic)
        elapsed_time = time.time() - start_time
        print("+---------------+")
        print("| Max Heuristic |")
        print("+---------------+")
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print(
            f'length of solution (number of tiles moved): {solution_node_and_frontier_count[0].path_cost}')
        print(f'number of nodes removed from frontier: {solution_node_and_frontier_count[1]}')


def analyse_duckpuzzle(duck_puzzle_set):
    """
        @INPUT: eight puzzle set
        @OUTPUT: logs duck puzzle analysis results
    """
    print("><><><><><><><><><><><><><")
    print("<>                      <>")
    print(">< Duck Puzzle Analysis ><")
    print("<>                      <>")
    print("><><><><><><><><><><><><><")

    for puzzle in duck_puzzle_set:

        # test cases
        # puzzle = DuckPuzzle(tuple([5, 0, 8, 4, 2, 1, 7, 3, 6]))
        # puzzle = DuckPuzzle(tuple([2, 3, 1, 7, 0, 8, 6, 4, 5]))

        display_duckpuzzle(puzzle.initial)

        start_time = time.time()
        solution_node_and_frontier_count = astar_search(puzzle, puzzle.h)
        elapsed_time = time.time() - start_time
        print("+---------------------------+")
        print("| Misplaced Tiles Heuristic |")
        print("+---------------------------+")
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print(
            f'length of solution (number of tiles moved): {solution_node_and_frontier_count[0].path_cost}')
        print(f'number of nodes removed from frontier: {solution_node_and_frontier_count[1]}')

        start_time = time.time()
        solution_node_and_frontier_count = astar_search(puzzle, puzzle.manhattan)
        elapsed_time = time.time() - start_time
        print("+------------------------------+")
        print("| Manhattan Distance Heuristic |")
        print("+------------------------------+")
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print(
            f'length of solution (number of tiles moved): {solution_node_and_frontier_count[0].path_cost}')
        print(f'number of nodes removed from frontier: {solution_node_and_frontier_count[1]}')

        start_time = time.time()
        solution_node_and_frontier_count = astar_search(puzzle, puzzle.max_heuristic)
        elapsed_time = time.time() - start_time
        print("+---------------+")
        print("| Max Heuristic |")
        print("+---------------+")
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print(
            f'length of solution (number of tiles moved): {solution_node_and_frontier_count[0].path_cost}')
        print(f'number of nodes removed from frontier: {solution_node_and_frontier_count[1]}')


def main():
    # specify how many puzzles to generate
    puzzle_set_size = 10

    # create puzzle sets
    eight_puzzle_set = create_8puzzle_set(puzzle_set_size)
    duck_puzzle_set = create_duckpuzzle_set(puzzle_set_size)

    # analyse puzzle sets, logs algorithm runtimes, number of nodes removed from frontier and number of moves
    analyse_8puzzle(eight_puzzle_set)
    analyse_duckpuzzle(duck_puzzle_set)


if __name__ == "__main__":
    main()