import numpy as np
import time

from search import *
from utils import memoize

RUN_QUESTION_2_TIME_TEST = False
RUN_QUESTION_3_TIME_TEST = False

# Randomly generated puzzles that are solvable
solvable_duckpuzzle_states = [
    (2, 3, 1, 6, 4, 8, 0, 5, 7), (1, 2, 3, 0, 4, 5, 7, 8, 6), (0, 2, 1, 3, 5, 4, 7, 6, 8), (0, 2, 1, 3, 7, 5, 6, 8, 4), (2, 0, 1, 3, 7, 8, 5, 6, 4),
    (2, 3, 1, 6, 7, 8, 4, 5, 0), (3, 1, 2, 4, 6, 5, 8, 7, 0), (2, 0, 1, 3, 5, 4, 8, 7, 6), (2, 3, 1, 8, 6, 7, 4, 5, 0), (2, 3, 1, 8, 0, 7, 4, 6, 5),
    (2, 0, 1, 3, 6, 8, 4, 7, 5), (3, 1, 2, 8, 0, 7, 4, 6, 5), (3, 0, 2, 1, 5, 8, 4, 6, 7), (1, 2, 3, 0, 7, 8, 5, 6, 4), (1, 2, 3, 6, 5, 8, 0, 7, 4),
    (3, 1, 2, 6, 0, 8, 5, 4, 7), (1, 2, 3, 6, 5, 8, 7, 4, 0), (1, 2, 3, 4, 8, 6, 0, 5, 7), (2, 0, 1, 3, 5, 7, 6, 4, 8), (3, 1, 2, 4, 6, 8, 0, 7, 5)
]

# 1 HELPERS -------------------------------------------
def make_rand_8puzzle():
    random_sequence = tuple(np.random.permutation(9))
    dummy_puzzle = EightPuzzle(random_sequence)

    while(not dummy_puzzle.check_solvability(random_sequence)):
        random_sequence = tuple(np.random.permutation(9))

    return EightPuzzle(random_sequence)

def display(state):
    count = 0
    print_string = ""
    for i in state:
        count += 1
        if i == 0:
            print_string += '*'
        else:
            print_string += str(i)
        
        print_string += ' '
        if(count % 3 == 0):
            print_string += '\n'
    
    print(print_string)
    pass

# 2 Comparing Algorithms -------------------------------------------
def manhattan_heuristic(node):
        index_dict = {
            1: [0, 1, 2, 1, 2, 3, 2, 3, 4],
            2: [1, 0, 1, 2, 1, 2, 3, 2, 3],
            3: [2, 1, 0, 3, 2, 1, 4, 3, 2],
            4: [1, 2, 3, 0, 1, 2, 1, 2, 3],
            5: [2, 1, 2, 1, 0, 1, 2, 1, 2],
            6: [3, 2, 1, 2, 1, 0, 3, 2, 1],
            7: [2, 3, 4, 1, 2, 3, 0, 1, 2],
            8: [3, 2, 3, 2, 1, 2, 1, 0, 1]
        }

        total_mhv = 0
        for position in range(9):
            tile = node.state[position]

            if(tile == 0):
                continue

            total_mhv += index_dict[tile][position]
        
        return total_mhv

# best first graph search function from search.py with prints 
def best_first_graph_search_with_print(problem, f, display=False):
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
    pop_count = 0
    while frontier:
        node = frontier.pop()
        pop_count += 1
        if problem.goal_test(node.state):
            print(f"Num_tiles_moved = {f(node)}")
            print(f"Num_popped_off_frontier = {pop_count}")
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    pop_count += 1
                    frontier.append(child)
    return None

# astar search function from search.py with prints
def astar_search_with_print(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_with_print(problem, lambda n: n.path_cost + h(n), display)

# Implementation of astar_search where the heuristic is the max of the problem's default heuristic and an input heuristic
def astar_search_max_of_2(problem, oh=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+ max(h(n), oh(n)).
    You need to specify the oh function when you call astar_search_max_of_2."""
    h = memoize(problem.h, 'h')
    other_heuristic = memoize(oh, 'oh')
    return best_first_graph_search_with_print(problem, lambda n: n.path_cost + max(h(n), other_heuristic(n)), display)

# 3 The House-Puzzle -------------------------------------------
class DuckPuzzle(Problem):
    
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
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

        no_left = [0, 2, 6]
        no_up = [0, 1, 4, 5]
        no_right = [1, 5, 8]
        no_down = [2, 6, 7, 8]

        if index_blank_square in no_left:
            possible_actions.remove('LEFT')
        if index_blank_square in no_up:
            possible_actions.remove('UP')
        if index_blank_square in no_right:
            possible_actions.remove('RIGHT')
        if index_blank_square in no_down:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        action_delta = delta[action]

        if blank <= 4 and action  == 'UP':
            action_delta += 1
        elif blank < 3 and action == 'DOWN':
            action_delta -= 1

        neighbor = blank + action_delta
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal
    
    def check_solvability(self, state):
        """ NOT functional
        Checks whether state is solvable or not."""
        inversions_2x2 = 0
        inversions_3x2 = 0

        for i in range(4):
            for j in range(i + 1, 4):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversions_2x2 += 1
        
        if self.find_blank_square(state) < 3:
            solvable_2x2 = inversions_2x2 % 2 != 0
        else:
            solvable_2x2 = inversions_2x2 % 2 == 0

        for i in range(4, len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversions_3x2 += 1

        solvable_3x2 = inversions_3x2 % 2 == 0
            
        return solvable_2x2 and solvable_3x2
    
    def h(self, node):
        # print(f"hanswer = {sum(s != g for (s, g) in zip(node.state, self.goal))}")
        # print(f"node = {node.state}, goal = {self.goal}")
        # print(f"answer = {sum(s != g for (s, g) in zip(node.state, self.goal))}")
        return sum(s != g for (s, g) in zip(node.state, self.goal))

def make_rand_duckpuzzle():
    random_sequence = tuple(np.random.permutation(9))
    dummy_puzzle = DuckPuzzle(random_sequence)

    while(not dummy_puzzle.check_solvability(random_sequence)):
        random_sequence = tuple(np.random.permutation(9))

    return DuckPuzzle(random_sequence)

def duck_puzzle_manhattan_heuristic(node):
    index_dict = {
        1: [0, 1, 1, 2, 3, 4, 3, 4, 5],
        2: [1, 0, 2, 1, 2, 3, 2, 3, 4],
        3: [1, 2, 0, 1, 2, 3, 2, 3, 4],
        4: [2, 1, 1, 0, 1, 2, 1, 2, 3],
        5: [3, 2, 2, 1, 0, 1, 2, 1, 2],
        6: [4, 3, 3, 2, 1, 0, 3, 2, 1],
        7: [3, 2, 2, 1, 2, 3, 0, 1, 2],
        8: [4, 3, 3, 2, 1, 2, 1, 0, 1]
    }

    total_mhv = 0
    for position in range(9):
        tile = node.state[position]

        if(tile == 0):
            continue

        total_mhv += index_dict[tile][position]
    
    return total_mhv

# Main function to run data collection loops
# if __name__ == "__main__":

#     if RUN_QUESTION_2_TIME_TEST:
#         for i in range(10):
#             rand_eight_puzzle = make_rand_8puzzle()
#             display(rand_eight_puzzle.initial)

#             start_time = time.time()
#             astar_search_with_print(rand_eight_puzzle)
#             print(f"Misplaced Tile Time: {time.time() - start_time}")

#             start_time = time.time()
#             astar_search_with_print(rand_eight_puzzle, h=manhattan_heuristic)
#             print(f"Manhattan Time: {time.time() - start_time}")

#             start_time = time.time()
#             astar_search_max_of_2(rand_eight_puzzle, oh=manhattan_heuristic)
#             print(f"Max(Misplaced, Manhattan) Time: {time.time() - start_time}")

#             print("\n\n\n")

#     if RUN_QUESTION_3_TIME_TEST:
#         for state in solvable_duckpuzzle_states:
#             duck_puzzle = DuckPuzzle(state)
#             display(state)

#             start_time = time.time()
#             astar_search_with_print(duck_puzzle)
#             print(f"Misplaced Tile Time: {time.time() - start_time}")

#             start_time = time.time()
#             astar_search_with_print(duck_puzzle, h=duck_puzzle_manhattan_heuristic)
#             print(f"Misplaced Tile Time: {time.time() - start_time}")

#             start_time = time.time()
#             astar_search_max_of_2(duck_puzzle, oh=duck_puzzle_manhattan_heuristic)
#             print(f"Max(Misplaced, Manhattan) Time: {time.time() - start_time}")

#             print("\n\n\n")
