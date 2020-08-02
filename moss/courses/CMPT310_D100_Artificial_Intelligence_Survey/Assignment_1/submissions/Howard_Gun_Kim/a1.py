from time import time
from math import floor
from random import shuffle, randint
from search import astar_search_with_number_of_node_removal, DuckPuzzle, EightPuzzle, Node

# ______________________Q1 Helper Functions______________________

def make_rand_8puzzle():
    initial = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    shuffle(initial)
    randomPermutation = tuple(initial)
    newPuzzle = EightPuzzle(randomPermutation)

    while( not newPuzzle.check_solvability(initial) ):
        shuffle(initial)
        randomPermutation = tuple(initial)
        newPuzzle = EightPuzzle(randomPermutation)
    
    return newPuzzle


def display(state):
    mutableState = list(state)
    tupleLength = len(mutableState)
    assert( tupleLength is 9 )

    for i in range(0, tupleLength):
        if mutableState[i] is 0:
            mutableState[i] = '*'

    for i in range(0, tupleLength, 3):
        print(mutableState[i], mutableState[i+1], mutableState[i+2])


# ______________________Q2 Comparing Algorithms______________________

# adopted from EightPuzzle.h() in search.py
def missing_tile(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return sum(s != g for (s, g) in zip(node.state, goal))


def manhattan_distance(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    total_manhattan_distance = 0
    n = 3

    for i in range(0, n):
        for j in range(0, n):
            # convert 3x3 matrix indices to list index, then get element at the index
            index_for_list = 3*i + j
            state_element_at_ij = node.state[index_for_list]

            # find the list index for the state element in goal
            index_in_goal = goal.index(state_element_at_ij)

            # convert list index to 3x3 matrix indices
            row_for_goal = floor(index_in_goal / n)
            col_for_goal = index_in_goal % n

            # add manhattan_distance to the running total
            total_manhattan_distance += abs(i-row_for_goal) + abs(j-col_for_goal)

    return total_manhattan_distance


def max_of_missing_tile_and_manhattan_distance(node):
    total_missing_tile = missing_tile(node)
    total_manhattan_distance = manhattan_distance(node)
    return max(total_missing_tile, total_manhattan_distance)


# ______________________Q3 The House-Puzzle______________________

def make_rand_duckpuzzle():
    initial = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    duckpuzzle = DuckPuzzle(initial)

    '''
    make N random legal moves, where N is a random integer between 1 and 200

    at any given state, some number of random moves are possible and one move is selected
    if the total number of moves made are constant and relatively small (< 10),
        the distribution of 'time to solution' per algorithm may not have meaningful information for analyzing algorithm performance
    '''
    
    # root node
    node = Node(duckpuzzle.initial)

    # N
    remaining_number_of_moves = randint(1, 200)
    
    while remaining_number_of_moves > 0:
        possible_states = node.expand(duckpuzzle)
        next_state_index = randint(0, len(possible_states)-1)
        node = possible_states[next_state_index]
        remaining_number_of_moves -= 1

    solvable_random_duck_puzzle = DuckPuzzle(node.state)
    
    return solvable_random_duck_puzzle
    
# _______________________________________________________________


def main():
    new_puzzles = []
    number_of_puzzles = 10

    for i in range(0, number_of_puzzles):
        # new_puzzles.insert(i, make_rand_8puzzle())
        new_puzzles.insert(i, make_rand_duckpuzzle())
        

    results_from_missing_tiles = []
    results_from_manhattan_distance = []
    results_from_max_of_both = []

    for i in range(0, number_of_puzzles):
        # missing_tile
        missing_tile_start_time = time()
        missing_tile_result = astar_search_with_number_of_node_removal(new_puzzles[i], missing_tile)
        missing_tile_execution_time = time() - missing_tile_start_time
        missing_tile_result.append(missing_tile_execution_time)

        assert missing_tile_result[0] is not None
        missing_tile_solution = missing_tile_result[0].solution()
        missing_tile_solution_length = len(missing_tile_solution)
        missing_tile_result.append(missing_tile_solution)
        missing_tile_result.append(missing_tile_solution_length)

        results_from_missing_tiles.append(missing_tile_result)


        # manhattan_distance
        manhattan_distance_start_time = time()
        manhattan_distance_result = astar_search_with_number_of_node_removal(new_puzzles[i], manhattan_distance)
        manhattan_distance_execution_time = time() - manhattan_distance_start_time
        manhattan_distance_result.append(manhattan_distance_execution_time)

        assert manhattan_distance_result[0] is not None
        manhattan_distance_solution = manhattan_distance_result[0].solution()
        manhattan_distance_solution_length = len(manhattan_distance_solution)
        manhattan_distance_result.append(manhattan_distance_solution)
        manhattan_distance_result.append(manhattan_distance_solution_length)

        results_from_manhattan_distance.append(manhattan_distance_result)


        # max_of_both
        max_of_both_start_time = time()
        max_of_both_result = astar_search_with_number_of_node_removal(new_puzzles[i], max_of_missing_tile_and_manhattan_distance)
        max_of_both_execution_time = time() - max_of_both_start_time
        max_of_both_result.append(max_of_both_execution_time)

        assert max_of_both_result[0] is not None
        max_of_both_result_solution = max_of_both_result[0].solution()
        max_of_both_result_solution_length = len(max_of_both_result_solution)
        max_of_both_result.append(max_of_both_result_solution)
        max_of_both_result.append(max_of_both_result_solution_length)

        results_from_max_of_both.append(max_of_both_result)

    for i in range(0, number_of_puzzles):
        print(new_puzzles[i].initial)
        print(results_from_missing_tiles[i])
        print(results_from_manhattan_distance[i])
        print(results_from_max_of_both[i])
        print('\n')

if __name__ == '__main__':
    main()


# ______________________Modifications to search.py______________________
'''
def best_first_graph_search_with_number_of_node_removal(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    number_of_removed_nodes = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        number_of_removed_nodes += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, number_of_removed_nodes]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return [None, number_of_removed_nodes]


def astar_search_with_number_of_node_removal(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_with_number_of_node_removal(problem, lambda n: n.path_cost + h(n), display)


class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        # possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        """ There probably is a more elegant solution than hardcoding legal moves per index_blank_square, 
        but this is easy to show that it's correct """

        if index_blank_square == 0:
            possible_actions = ['RIGHT', 'DOWN']
        elif index_blank_square == 1:
            possible_actions = ['DOWN', 'LEFT']
        elif index_blank_square == 2:
            possible_actions = ['UP', 'RIGHT']
        elif index_blank_square == 3:
            possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        elif index_blank_square == 4:
            possible_actions = ['DOWN', 'LEFT', 'RIGHT']
        elif index_blank_square == 5:
            possible_actions = ['DOWN', 'LEFT']
        elif index_blank_square == 6:
            possible_actions = ['UP', 'RIGHT']
        elif index_blank_square == 7:
            possible_actions = ['UP', 'LEFT', 'RIGHT']
        elif index_blank_square == 8:
            possible_actions = ['UP', 'LEFT']

        return possible_actions

    def result(self, state, action):
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        """ 
        assuming the moves are legal:

        LEFT is always -1 and RIGHT is always +1
                
        UP in second row = -2
        UP in third row = -3
        DOWN in first row = +2
        DOWN in second row = +3
        """

        # get right delta for row number
        delta = None
        if blank < 2:
            # row = 0
            delta = {'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank < 6:
            # row = 1
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif blank < 9:
            # row = 2
            delta = {'UP': -3, 'LEFT': -1, 'RIGHT': 1}
        assert delta is not None

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


'''