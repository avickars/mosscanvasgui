# a1.py

from search import *
from utils import *
import random
import time

NUM_SCRAMBLES = 50
EIGHT_PUZZLE_DIMENSION = 3
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0) # tuple

# Manhattan Distance Tables
# Pattern Databases: Inspired by the lecture notes,
# Chapter 3 - Solving Problems by Search
MD_8Puzzle_TILE_1 = (0, 1, 2, 1, 2, 3, 2, 3, 4)
MD_8Puzzle_TILE_2 = (1, 0, 1, 2, 1, 2, 3, 2, 3)
MD_8Puzzle_TILE_3 = (2, 1, 0, 3, 2, 1, 4, 3, 2)
MD_8Puzzle_TILE_4 = (1, 2, 3, 0, 1, 2, 1, 2, 3)
MD_8Puzzle_TILE_5 = (2, 1, 2, 1, 0, 1, 2, 1, 2)
MD_8Puzzle_TILE_6 = (3, 2, 1, 2, 1, 0, 3, 2, 1)
MD_8Puzzle_TILE_7 = (2, 3, 4, 1, 2, 3, 0, 1, 2)
MD_8Puzzle_TILE_8 = (3, 2, 3, 2, 1, 2, 1, 0, 1)

MD_DuckPuzzle_Tile_1 = (0, 1, 1, 2, 3, 4, 3, 4, 5)
MD_DuckPuzzle_Tile_2 = (1, 0, 2, 1, 2, 3, 2, 3, 4)
MD_DuckPuzzle_Tile_3 = (1, 2, 0, 1, 2, 3, 2, 3, 4)
MD_DuckPuzzle_Tile_4 = (2, 1, 1, 0, 1, 2, 1, 2, 3)
MD_DuckPuzzle_Tile_5 = (3, 2, 2, 1, 0, 1, 2, 1, 2)
MD_DuckPuzzle_Tile_6 = (4, 3, 3, 2, 1, 0, 3, 2, 1)
MD_DuckPuzzle_Tile_7 = (3, 2, 2, 1, 2, 3, 0, 1, 2)
MD_DuckPuzzle_Tile_8 = (4, 3, 3, 2, 1, 2, 1, 0, 1)


# _____________________________________________________________________________________________________
# Modified code originally from search.py
def best_first_graph_search_with_node_count(problem, f, display=False): # From the textbook code
    """
    Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned.
    """
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    num_nodes_removed = 0
    while frontier:
        node = frontier.pop()
        num_nodes_removed += 1

        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, num_nodes_removed
        
        # add tuple() to remove unhashable error
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)

    return None, num_nodes_removed


# _____________________________________________________________________________________________________
# 8-Puzzle
def make_rand_8puzzle():
    """ 
    Returns a new instance of an EightPuzzle problem 
    with a random initial state that is solvable.

    Tip from Toby: Randomly scramble tiles from the goal state.
    """
    state = list(goal_state) # makes state mutable
    puzzle = EightPuzzle(goal_state)
    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        
    count = 0
    while (count < NUM_SCRAMBLES):
        move = random.choice(possible_actions)
        if move in puzzle.actions(state):  # make legal moves only
            count += 1
            state = list(puzzle.result(state, move))
            puzzle = EightPuzzle(tuple(state))

    return puzzle, tuple(state) # state is now immutable


def display(state):
    """
    Takes an 8-puzzle state
    (i.e. a tuple that is a permutation of (0, 1, 2, …, 8)) as input and 
    prints a neat and readable representation of it. 

    0 is the blank, and should be printed as a * character.
    """
    # Convert state from tuple to list so it's mutable, and
    # Swap 0 with '*'
    blank_index = state.index(0)
    state_list = list(state)
    state_list[blank_index] = '*'

    i = 0
    while (i < len(state_list)):
        print("{} {} {}".format(
            state_list[i],
            state_list[i + 1], 
            state_list[i + 2]))
        i += EIGHT_PUZZLE_DIMENSION


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
        """ Return the heuristic value for a given state. 
        Default heuristic function used is h(n) = number of misplaced tiles,
        EXCLUDING the blank tile to keep the heuristic admissible per our lecture. """
        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

    def astar_search_misplaced_tile(self, problem, h=None, display=False): # From the textbook code
        """
        A* search is best-first graph search with f(n) = g(n) + h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass.
        """
        h = memoize(h or problem.h, 'h')
        return best_first_graph_search_with_node_count(
                problem, 
                lambda n: n.path_cost + h(n), # f(n) = g(n) + h(n), where n is a given node
                display)

    def get_manhattan_distance(self, tile_num, index):
        if tile_num == 1:
            return MD_8Puzzle_TILE_1[index]
        elif tile_num == 2:
            return MD_8Puzzle_TILE_2[index]
        elif tile_num == 3:
            return MD_8Puzzle_TILE_3[index]
        elif tile_num == 4:
            return MD_8Puzzle_TILE_4[index]
        elif tile_num == 5:
            return MD_8Puzzle_TILE_5[index]
        elif tile_num == 6:
            return MD_8Puzzle_TILE_6[index]
        elif tile_num == 7:       
            return MD_8Puzzle_TILE_7[index] 
        elif tile_num == 8:
            return MD_8Puzzle_TILE_8[index]
        else: # tile_num == 0, the blank tile is excluded per our lecture
            return 0

    def h_manhattan_distance(self, node):
        sum = 0
        state = node.state # tuple
        for i in range(len(state)):
            tile_num = state[i]
            if tile_num != i + 1:
                sum += self.get_manhattan_distance(tile_num, i)
        return sum

    def astar_search_manhattan_distance(self, problem, h=None, display=False):
        """
        A* search is best-first graph search with f(n) = g(n) + h(n),
        using Manhattan distance heuristic.
        """
        return best_first_graph_search_with_node_count(
                problem, 
                lambda n: n.path_cost + self.h_manhattan_distance(n), # f(n) = g(n) + h(n), where n is a given node
                display)

    def astar_search_max(self, problem, h=None, display=False):
        """
        A* search is best-first graph search with f(n) = g(n) + h(n),
        using max of misplaced tile heuristic and Manhattan distance heuristic.
        """
        h = memoize(h or problem.h, 'h')
        return best_first_graph_search_with_node_count(
                problem, 
                lambda n: n.path_cost + max(h(n), self.h_manhattan_distance(n)), # f(n) = g(n) + h(n), where n is a given node
                display)


# _____________________________________________________________________________________________________
# Duck Puzzle
def make_rand_duckpuzzle():
    """ 
    Returns a new instance of an DuckPuzzle problem 
    with a random initial state that is solvable.

    Tip from Toby: Randomly scramble tiles from the goal state.
    """
    state = list(goal_state)
    puzzle = DuckPuzzle(goal_state)
    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        
    count = 0
    while (count < NUM_SCRAMBLES):
        move = random.choice(possible_actions)
        if move in puzzle.actions(state):  # Make legal moves only
            count += 1
            state = list(puzzle.result(state, move))
            puzzle = DuckPuzzle(tuple(state))

    return puzzle, tuple(state) # state is now immutable
        

def display_duckpuzzle(state):
    """
    Takes an duck puzzle state
    (i.e. a tuple that is a permutation of (0, 1, 2, …, 8)) as input and 
    prints a neat and readable representation of it. 

    0 is the blank, and should be printed as a * character.
    """
    # Convert state from tuple to list so it's mutable, and
    # Swap 0 with '*'
    blank_index = state.index(0)
    state_list = list(state)
    state_list[blank_index] = '*'

    i = 0
    print("{} {}".format(state_list[i],
                         state_list[i + 1]))

    print("{} {} {} {}".format(state_list[i + 2], 
                               state_list[i + 3],
                               state_list[i + 4],
                               state_list[i + 5]))

    print("  {} {} {}".format(state_list[i + 6],
                           state_list[i + 7],
                           state_list[i + 8]))


class DuckPuzzle(Problem):
    """
    The problem of sliding tiles numbered from 1 to 8 on a board,
    where one of the squares is a blank.
    
    The board has a shape that looks like a duck facing to the left.

    A state is represented as a tuple of length 9,
    where element at index i represents the tile number at index i
    (0 if it's an empty square)
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

        if (index_blank_square == 0 or 
            index_blank_square == 2 or
            index_blank_square == 6):
            possible_actions.remove('LEFT')
            
        if (index_blank_square < 2 or
            index_blank_square == 4 or
            index_blank_square == 5):
            possible_actions.remove('UP')

        if (index_blank_square == 1 or
            index_blank_square == 5 or
            index_blank_square == 8):
            possible_actions.remove('RIGHT')

        if (index_blank_square == 2 or
            index_blank_square > 5):
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state) # mutalbe

        neighbor = blank
        if action == 'UP':
            if (blank == 2 or blank == 3):
                neighbor -= 2
            else:
                neighbor -= 3
        elif action == 'DOWN':
            if (blank == 0 or blank == 1):
                neighbor += 2
            else:
                neighbor += 3
        elif action == 'LEFT':
            neighbor -= 1
        else: # action == 'RIGHT'
            neighbor += 1

        # Swap blank and neighbor
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

    def h(self, node):        
        """ Return the heuristic value for a given state. 
        Default heuristic function used is h(n) = number of misplaced tiles,
        EXCLUDING the blank tile to keep the heuristic admissible per our lecture. """
        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

    def astar_search_misplaced_tile(self, problem, h=None, display=False): # From the textbook code
        """
        A* search is best-first graph search with f(n) = g(n) + h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass.
        """
        h = memoize(h or problem.h, 'h')
        return best_first_graph_search_with_node_count(
                problem, 
                lambda n: n.path_cost + h(n), # f(n) = g(n) + h(n), where n is a given node
                display)

    def get_manhattan_distance(self, tile_num, index):
        if tile_num == 1:
            return MD_DuckPuzzle_Tile_1[index]
        elif tile_num == 2:
            return MD_DuckPuzzle_Tile_2[index]
        elif tile_num == 3:
            return MD_DuckPuzzle_Tile_3[index]
        elif tile_num == 4:
            return MD_DuckPuzzle_Tile_4[index]
        elif tile_num == 5:
            return MD_DuckPuzzle_Tile_5[index]
        elif tile_num == 6:
            return MD_DuckPuzzle_Tile_6[index]
        elif tile_num == 7:       
            return MD_DuckPuzzle_Tile_7[index] 
        elif tile_num == 8:
            return MD_DuckPuzzle_Tile_8[index]
        else: # tile_num == 0, the blank tile is excluded per our lecture
            return 0

    def h_manhattan_distance(self, node):
        sum = 0
        state = node.state # tuple
        for i in range(len(state)):
            tile_num = state[i]
            if tile_num != i + 1:
                sum += self.get_manhattan_distance(tile_num, i)
        return sum

    def astar_search_manhattan_distance(self, problem, h=None, display=False):
        """
        A* search is best-first graph search with f(n) = g(n) + h(n),
        using Manhattan distance heuristic.
        """
        return best_first_graph_search_with_node_count(
                problem, 
                lambda n: n.path_cost + self.h_manhattan_distance(n), # f(n) = g(n) + h(n), where n is a given node
                display)

    def astar_search_max(self, problem, h=None, display=False):
        """
        A* search is best-first graph search with f(n) = g(n) + h(n),
        using max of misplaced tile heuristic and Manhattan distance heuristic.
        """
        h = memoize(h or problem.h, 'h')
        return best_first_graph_search_with_node_count(
                problem, 
                lambda n: n.path_cost + max(h(n), self.h_manhattan_distance(n)), # f(n) = g(n) + h(n), where n is a given node
                display)


# _____________________________________________________________________________________________________
# Comparing Algorithms
def time_algorithm(puzzle, initial_state, count, f):
    start_time = time.time()
    node, num_nodes_removed = f(puzzle)
    elapsed_time = time.time() - start_time

    solution = []
    if (num_nodes_removed != 1): # if initial_state != goal_state
        solution = node.solution()
    
    # Print csv format
    print(f"Puzzle #{count}: {initial_state} | {f} | Solution: {solution}")
    print(f"Puzzle #{count}: {initial_state} | {f} | Elapsed time (in seconds): {elapsed_time}s")
    print(f"Puzzle #{count}: {initial_state} | {f} | Number of tiles moved: {len(solution)}")
    print(f"Puzzle #{count}: {initial_state} | {f} | Number of nodes removed from frontier: {num_nodes_removed}")
    print()
    

def compare_algorithms_8puzzle(count):
    """
    Create 10 (more would be better!) random 8-puzzle instances, and
    solve each of them using the algorithms below. 

    Each algorithm should be run on the exact same set of problems to make the comparison fair.

    For each solved problem, record:
    - the total running time in seconds
    - the length (i.e. number of tiles moved) of the solution
    - that total number of nodes that were removed from frontier

    Also, be aware that the time it takes to solve random 8-puzzle instances can vary from 
    less than a second to hundreds of seconds — so solving all these problems might take some time!
    """
    puzzle, initial_state = make_rand_8puzzle()

    # Three algorithms to be tested with random 8-puzzle instances
    time_algorithm(puzzle, initial_state, count, puzzle.astar_search_misplaced_tile)
    time_algorithm(puzzle, initial_state, count, puzzle.astar_search_manhattan_distance)
    time_algorithm(puzzle, initial_state, count, puzzle.astar_search_max)

    node1, _ = puzzle.astar_search_misplaced_tile(puzzle)
    node2, _ = puzzle.astar_search_manhattan_distance(puzzle)
    node3, _ = puzzle.astar_search_max(puzzle)
    # Admissible A*-search guarantees an optimal solution
    assert len(node1.solution()) == len(node2.solution()) == len(node3.solution()) 


def compare_algorithms_duckpuzzle(count):
    """
    Create 10 (more would be better!) random duck-puzzle instances, and
    solve each of them using the algorithms below. 

    Each algorithm should be run on the exact same set of problems to make the comparison fair.

    For each solved problem, record:
    - the total running time in seconds
    - the length (i.e. number of tiles moved) of the solution
    - that total number of nodes that were removed from frontier
    """    
    puzzle, initial_state = make_rand_duckpuzzle()

    # Three algorithms to be tested with random duck puzzle instances
    time_algorithm(puzzle, initial_state, count, puzzle.astar_search_misplaced_tile)
    time_algorithm(puzzle, initial_state, count, puzzle.astar_search_manhattan_distance)
    time_algorithm(puzzle, initial_state, count, puzzle.astar_search_max)
    
    node1, _ = puzzle.astar_search_misplaced_tile(puzzle)
    node2, _ = puzzle.astar_search_manhattan_distance(puzzle)
    node3, _ = puzzle.astar_search_max(puzzle)
    # Admissible A*-search guarantees an optimal solution
    assert len(node1.solution()) == len(node2.solution()) == len(node3.solution()) 


def compare_algorithms_nTimes(n, f):
    print(f"Starting comparisons of {n} puzzles...")
    count = 0
    while (count < n):
        count += 1
        f(count)
    print(f"Total puzzles solved: {count}")


# _____________________________________________________________________________________________________
# Test Function(s) - 8-puzzle
def test_make_rand_8puzzle():
    """
    Use the mechod called check_solvability in the EightPuzzle
    to help ensure your initial state is solvable.
    """
    print("Testing make_rand()...")
    for _ in range(10000):
        puzzle, initial_state = make_rand_8puzzle()
        assert puzzle.check_solvability(initial_state) == True
    print("Test completed without exception.")

  
def test_display():
    display(goal_state)
    print()

    state = (1, 2, 3, 4, 0, 6, 7, 8, 5)
    display(state)
    print()

    _, initial_state = make_rand_8puzzle()
    display(initial_state)


def test_impossible_state():
    impossible_state = (1, 2, 3, 4, 5, 6, 8, 7, 0)
    puzzle = EightPuzzle(impossible_state)
    assert puzzle.check_solvability(impossible_state) == False


def test_get_manhattan_distance():
    print("Testing get_manhattan_distance()...")

    puzzle, _ = make_rand_8puzzle()
    tile_num = 1
    index = 0
    assert puzzle.get_manhattan_distance(tile_num, index) == 0

    tile_num = 4
    index = 5
    assert puzzle.get_manhattan_distance(tile_num, index) == 2

    tile_num = 7
    index = 2
    assert puzzle.get_manhattan_distance(tile_num, index) == 4

    tile_num = 0
    index = 3
    assert puzzle.get_manhattan_distance(tile_num, index) == 0
    
    tile_num = 0
    index = 8
    assert puzzle.get_manhattan_distance(tile_num, index) == 0
    
    tile_num = 0
    index = 6
    assert puzzle.get_manhattan_distance(tile_num, index) == 0

    tile_num = 2
    index = 0
    assert puzzle.get_manhattan_distance(tile_num, index) == 1


def test_h_manhattan_distance():
    print("Testing h_manhattan_distance()...")
    puzzle, _ = make_rand_8puzzle()

    state = (7, 2, 4, 5, 0, 6, 8, 3, 1) # Textbook: Fig 3.28, P.103)
    node = Node(state)
    assert puzzle.h_manhattan_distance(node) == 14

    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    node = Node(state)
    assert puzzle.h_manhattan_distance(node) == 0

    state = (0, 6, 2, 1, 3, 8, 4, 7, 5)
    node = Node(state)
    assert puzzle.h_manhattan_distance(node) == 12

    state = (1, 6, 2, 0, 3, 8, 4, 7, 5)
    node = Node(state)
    assert puzzle.h_manhattan_distance(node) == 11


def test_algorithms_8puzzle():

    # sample 1
    count = 1
    initial_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = EightPuzzle(initial_state)

    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_misplaced_tile)
    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_manhattan_distance)
    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_max)

    node1, _ = puzzle.astar_search_misplaced_tile(puzzle)
    node2, _ = puzzle.astar_search_manhattan_distance(puzzle)
    node3, _ = puzzle.astar_search_max(puzzle)

    # Admissible A*-search guarantees an optimal solution
    assert len(node1.solution()) == len(node2.solution()) == len(node3.solution()) 

    # sample 2
    count += 1
    initial_state = (0, 6, 2, 1, 3, 8, 4, 7, 5)
    # ['DOWN', 'DOWN', 'RIGHT', 'RIGHT', 'UP', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT']
    puzzle = EightPuzzle(initial_state)

    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_misplaced_tile)
    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_manhattan_distance)
    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_max)

    node1, _ = puzzle.astar_search_misplaced_tile(puzzle)
    node2, _ = puzzle.astar_search_manhattan_distance(puzzle)
    node3, _ = puzzle.astar_search_max(puzzle)

    # Admissible A*-search guarantees an optimal solution
    assert len(node1.solution()) == len(node2.solution()) == len(node3.solution()) 

    # sample 3
    count += 1
    puzzle, initial_state = make_rand_8puzzle()
    time_algorithm(puzzle, initial_state, count, puzzle.astar_search_misplaced_tile)
    time_algorithm(puzzle, initial_state, count, puzzle.astar_search_manhattan_distance)
    time_algorithm(puzzle, initial_state, count, puzzle.astar_search_max)

    node1, _ = puzzle.astar_search_misplaced_tile(puzzle)
    node2, _ = puzzle.astar_search_manhattan_distance(puzzle)
    node3, _ = puzzle.astar_search_max(puzzle)

    # Admissible A*-search guarantees an optimal solution
    assert len(node1.solution()) == len(node2.solution()) == len(node3.solution()) 


# Test Function(s) - DuckPuzzle
def test_make_rand_duckpuzzle():
    """
    Be careful generating random instances: 
    the check_solvability function from the EightPuzzle probably doesn’t work with this board!
    """
    print("Testing test_make_rand_duckpuzzle()...")

    for i in range(1000):
        puzzle, initial_state = make_rand_duckpuzzle()

        # Three algorithms to be tested with random 8-puzzle instances
        node1, _ = puzzle.astar_search_misplaced_tile(puzzle)
        node2, _ = puzzle.astar_search_manhattan_distance(puzzle)
        node3, _ = puzzle.astar_search_max(puzzle)

        # Admissible A*-search guarantees an optimal solution
        assert len(node1.solution()) == len(node2.solution()) == len(node3.solution()) 


def test_display_duckPuzzle():
    initial_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    display_duckpuzzle(initial_state)
    print()
    
    initial_state = (0, 6, 2, 1, 3, 8, 4, 7, 5)
    display_duckpuzzle(initial_state)
    print()

    initial_state = (8, 7, 6, 4, 0, 3, 5, 2, 1) # this one takes time to solve!
    display_duckpuzzle(initial_state)
    print()

    initial_state = (8, 4, 2, 7, 0, 3, 6, 1, 5)
    display_duckpuzzle(initial_state)
    print()


def test_get_manhattan_distance_duckpuzzle():

    puzzle, _ = make_rand_duckpuzzle()

    print("Testing get_manhattan_distance_duckpuzzle()...")
    tile_num = 1
    index = 0
    assert puzzle.get_manhattan_distance(tile_num, index) == 0

    tile_num = 4
    index = 5
    assert puzzle.get_manhattan_distance(tile_num, index) == 2

    tile_num = 7
    index = 2
    assert puzzle.get_manhattan_distance(tile_num, index) == 2

    tile_num = 0
    index = 1
    assert puzzle.get_manhattan_distance(tile_num, index) == 0

    tile_num = 0
    index = 8
    assert puzzle.get_manhattan_distance(tile_num, index) == 0
    
    tile_num = 0
    index = 3
    assert puzzle.get_manhattan_distance(tile_num, index) == 0

    tile_num = 2
    index = 0
    assert puzzle.get_manhattan_distance(tile_num, index) == 1


def test_h_manhattan_distance_duckpuzzle():

    puzzle, _ = make_rand_duckpuzzle()

    print("Testing h_manhattan_distance_duckpuzzle()...")
    state = (7, 2, 4, 5, 0, 6, 8, 3, 1)
    node = Node(state)
    assert puzzle.h_manhattan_distance(node) == 14

    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    node = Node(state)
    assert puzzle.h_manhattan_distance(node) == 0

    state = (0, 6, 2, 1, 3, 8, 4, 7, 5)
    node = Node(state)
    assert puzzle.h_manhattan_distance(node) == 15

    state = (1, 6, 2, 0, 3, 8, 4, 7, 5)
    node = Node(state)
    assert puzzle.h_manhattan_distance(node) == 13


def test_algorithms_duckpuzzle():

    print("Testing test_algorithms_duckpuzzle()...")

    # sample #1
    count = 1
    initial_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = DuckPuzzle(initial_state)

    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_misplaced_tile)
    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_manhattan_distance)
    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_max)
    
    node1, _ = puzzle.astar_search_misplaced_tile(puzzle)
    node2, _ = puzzle.astar_search_manhattan_distance(puzzle)
    node3, _ = puzzle.astar_search_max(puzzle)

    # Admissible A*-search guarantees an optimal solution
    assert len(node1.solution()) == len(node2.solution()) == len(node3.solution()) 
   
    # sample #2
    count += 1
    initial_state = (3, 1, 0, 2, 5, 8, 4, 6, 7)
    # ['UP', 'RIGHT', 'DOWN', 'RIGHT', 'DOWN', 'RIGHT', 'UP', 'LEFT', 'LEFT', 'DOWN', 'RIGHT', 'RIGHT']
    puzzle = DuckPuzzle(initial_state)

    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_misplaced_tile)
    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_manhattan_distance)
    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_max)

    node1, _ = puzzle.astar_search_misplaced_tile(puzzle)
    node2, _ = puzzle.astar_search_manhattan_distance(puzzle)
    node3, _ = puzzle.astar_search_max(puzzle)

    # Admissible A*-search guarantees an optimal solution
    assert len(node1.solution()) == len(node2.solution()) == len(node3.solution()) 

    # sample #3
    count += 1
    initial_state = (1, 0, 3, 2, 8, 5, 7, 6, 4)
    # ['DOWN', 'DOWN', 'RIGHT', 'RIGHT', 'UP', 'LEFT', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'RIGHT', 'UP', 'LEFT', 'DOWN', 'RIGHT']
    puzzle = DuckPuzzle(initial_state)

    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_misplaced_tile)
    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_manhattan_distance)
    # time_algorithm(puzzle, initial_state, count, puzzle.astar_search_max)
        
    node1, _ = puzzle.astar_search_misplaced_tile(puzzle)
    node2, _ = puzzle.astar_search_manhattan_distance(puzzle)
    node3, _ = puzzle.astar_search_max(puzzle)

    # Admissible A*-search guarantees an optimal solution
    assert len(node1.solution()) == len(node2.solution()) == len(node3.solution()) 

    # sample #4
    count += 1
    puzzle, initial_state = make_rand_duckpuzzle()
    
    time_algorithm(puzzle, initial_state, count, puzzle.astar_search_misplaced_tile)
    time_algorithm(puzzle, initial_state, count, puzzle.astar_search_manhattan_distance)
    time_algorithm(puzzle, initial_state, count, puzzle.astar_search_max)
    
    node1, _ = puzzle.astar_search_misplaced_tile(puzzle)
    node2, _ = puzzle.astar_search_manhattan_distance(puzzle)
    node3, _ = puzzle.astar_search_max(puzzle)

    # Admissible A*-search guarantees an optimal solution
    assert len(node1.solution()) == len(node2.solution()) == len(node3.solution()) 


# _____________________________________________________________________________________________________
"""Run the following to save the result into a file"""
# /path/to/python /path/to/a1.py > result.txt

"""Main"""
# ________________________________________________
# 8-puzzle
# test_make_rand_8puzzle()
# test_display()
# test_impossible_state()
# test_get_manhattan_distance()
# test_h_manhattan_distance()
# test_algorithms_8puzzle()

# n = 100
# compare_algorithms_nTimes(n, compare_algorithms_8puzzle)

# ________________________________________________
# Duck Puzzle
# test_make_rand_duckpuzzle()
# test_display_duckPuzzle()
# test_get_manhattan_distance_duckpuzzle()
# test_h_manhattan_distance_duckpuzzle()
# test_algorithms_duckpuzzle()

# n = 100
# compare_algorithms_nTimes(n, compare_algorithms_duckpuzzle)