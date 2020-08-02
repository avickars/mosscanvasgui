# a1.py

from search import *
import random
import time

# Name: Josh Arik Miguel Fernandez
# Student Number: 301246300
# CMPT 310 with Dr. Toby Donaldson

# References:
#   Introduction to Python: https://www.w3schools.com/python/default.asp
#   The randint() function:
#       https://www.w3schools.com/python/ref_random_randint.asp
#   Passing a function as an argument:
#       https://www.geeksforgeeks.org/passing-function-as-an-argument-in-python/
#   Returning multiple values in a function using a tuple:
#       https://www.geeksforgeeks.org/g-fact-41-multiple-return-values-in-python/
#   Using isinstance() to differentiate the 8-puzzle from the duck puzzle:
#       https://www.w3schools.com/python/ref_func_isinstance.asp
#   test_search.py for showing me how to use the different methods
#       (It especially helped me with finding the solution node of
#       an EightPuzzle problem)
#   search.ipynb (the Jupyter Notebook) for giving me an idea for
#       the Manhattan distance algorithm

# Contents:
#   Extended EightPuzzle class for Assignment 1
#       class EightPuzzleExtended(EightPuzzle)
#   DuckPuzzle class for Question 3
#       class DuckPuzzle(Problem)
#   For question 1: EightPuzzle helper functions
#       def make_rand_8puzzle()
#       def display(state)
#   For question 3: DuckPuzzle helper functions
#       def make_rand_duckpuzzle()
#       def display_duck_puzzle(state)
#   For questions 2 & 3
#       def best_first_graph_search_a1(problem, f, display=False)
#       def astar_search_a1(problem, h=None, display=False)
#   Main functions
#       def solve_puzzle_and_analyze_algorithm(title, problem, h=None, display=False)
#       def main_EightPuzzle()
#       def main_EightPuzzle_test()
#       def main_DuckPuzzle()


"""""""""""""""""""""""""""""""""""""""""""""
EXTENDED EIGHTPUZZLE CLASS FOR ASSIGNMENT 1
"""""""""""""""""""""""""""""""""""""""""""""

class EightPuzzleExtended(EightPuzzle):

    # Improved h function that does not take include 0 as a tile
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum((s != 0 and s != g) for (s, g) in zip(node.state, self.goal))
    
    # Manhattan distance algorithm for Question 2.
    # Inspired by search.ipynb from the Jupyter notebook.
    def manhattan_distance(self, node):
        current_state = node.state
        goal_state = self.goal
        position_list = ((0, 0), (0, 1), (0, 2),
                         (1, 0), (1, 1), (1, 2),
                         (2, 0), (2, 1), (2, 2))
        manhattan_sum = 0
        
        for number in range(1, 9):
            index_in_current_state = 0
            for index in range(9):
                if(current_state[index] == number): index_in_current_state = index
         
            x_current = position_list[index_in_current_state][0]
            y_current = position_list[index_in_current_state][1]

            index_in_goal_state = 0
            for index in range(9):
                if(goal_state[index] == number): index_in_goal_state = index

            x_goal = position_list[index_in_goal_state][0]
            y_goal = position_list[index_in_goal_state][1]

            distance_needed = abs(x_goal - x_current) + abs(y_goal - y_current)
            manhattan_sum += distance_needed

        return manhattan_sum

    # Maximum value between the misplaced tile and
    # Manhattan distance heuristics for Question 2.
    # Inspired by search.ipynb from the Jupyter notebook.
    def max_heuristic(self, node):
        score_misplaced_tile = self.h(node)
        score_manhattan_distance = self.manhattan_distance(node)
        return max(score_misplaced_tile, score_manhattan_distance)


"""""""""""""""""""""""""""""""""""""""""""""
DUCKPUZZLE CLASS FOR QUESTION 3
"""""""""""""""""""""""""""""""""""""""""""""

class DuckPuzzle(Problem):
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

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'LEFT': -1, 'RIGHT': 1}

        if blank < 3:
            delta['UP'] = -2
            delta['DOWN'] = 2
        elif blank > 3:
            delta['UP'] = -3
            delta['DOWN'] = 3
        else: # blank == 3
            delta['UP'] = -2
            delta['DOWN'] = 3

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        pass # It is difficult to check the solvability of the DuckPuzzle

    # Improved h function that does not take include 0 as a tile
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum((s != 0 and s != g) for (s, g) in zip(node.state, self.goal))

    # Manhattan distance algorithm for Question 3.
    def manhattan_distance(self, node):
        current_state = node.state
        goal_state = self.goal
        position_list = ((0, 0), (0, 1),
                         (1, 0), (1, 1), (1, 2), (1, 3),
                                 (2, 1), (2, 2), (2, 3))
        manhattan_sum = 0
        
        for number in range(1, 9):
            index_in_current_state = 0
            for index in range(9):
                if(current_state[index] == number): index_in_current_state = index
         
            x_current = position_list[index_in_current_state][0]
            y_current = position_list[index_in_current_state][1]

            index_in_goal_state = 0
            for index in range(9):
                if(goal_state[index] == number): index_in_goal_state = index

            x_goal = position_list[index_in_goal_state][0]
            y_goal = position_list[index_in_goal_state][1]

            distance_needed = abs(x_goal - x_current) + abs(y_goal - y_current)
            manhattan_sum += distance_needed

        return manhattan_sum

    # Maximum value between the misplaced tile and
    # Manhattan distance heuristics for Question 3.
    # Inspired by search.ipynb from the Jupyter notebook.
    def max_heuristic(self, node):
        score_misplaced_tile = self.h(node)
        score_manhattan_distance = self.manhattan_distance(node)
        return max(score_misplaced_tile, score_manhattan_distance)


"""""""""""""""""""""""""""""""""""""""""""""
FOR QUESTION 1: EIGHTPUZZLE HELPER FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""

def make_rand_8puzzle():
    original_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    new_8puzzle = EightPuzzleExtended(original_state)

    for index in range(50):
        current_actions = new_8puzzle.actions(new_8puzzle.initial)
        new_action = random.randint(0, len(current_actions) - 1)
        new_state = new_8puzzle.result(new_8puzzle.initial, current_actions[new_action])
        new_8puzzle.initial = new_state

    print("Initial state: ", new_8puzzle.initial)
    check_initial_state = new_8puzzle.check_solvability(new_8puzzle.initial)
    print("Initial state's solvability check: ", check_initial_state)

    return new_8puzzle


def display(state):
    for index in range(0, 8, 3):
        first_num = state[index]
        second_num = state[index + 1]
        third_num = state[index + 2]

        if (first_num == 0): first_num = '*'
        if (second_num == 0): second_num = '*'
        if (third_num == 0): third_num = '*'

        print(first_num, second_num, third_num)


"""""""""""""""""""""""""""""""""""""""""""""
FOR QUESTION 3: DUCKPUZZLE HELPER FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""

def make_rand_duckpuzzle():
    original_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    new_duckpuzzle = DuckPuzzle(original_state)

    for index in range(50):
        current_actions = new_duckpuzzle.actions(new_duckpuzzle.initial)
        new_action = random.randint(0, len(current_actions) - 1)
        new_state = new_duckpuzzle.result(new_duckpuzzle.initial, current_actions[new_action])
        new_duckpuzzle.initial = new_state

    print("Initial state: ", new_duckpuzzle.initial)
    return new_duckpuzzle

def display_duck_puzzle(state):
    state_list = list(state)
    for index in range(9):
        if (state_list[index] == 0): state_list[index] = '*'

    print(state_list[0], state_list[1])
    print(state_list[2], state_list[3], state_list[4], state_list[5])
    print(" ", state_list[6], state_list[7], state_list[8])


"""""""""""""""""""""
FOR QUESTIONS 2 & 3
"""""""""""""""""""""

# Best first graph search algorithm, customized for Assignment 1
def best_first_graph_search_a1(problem, f, display=False):
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
    nodes_removed_from_frontier = 0
    
    while frontier:
        node = frontier.pop() # This is removing from the frontier
        nodes_removed_from_frontier += 1
        
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return (node, nodes_removed_from_frontier)

        explored.add(node.state)

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child] # This is also removing from the frontier
                    nodes_removed_from_frontier += 1
                    frontier.append(child)
               
    return (None, nodes_removed_from_frontier)


# A* search algorithm, customized for Assignment 1
def astar_search_a1(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_a1(problem, lambda n: n.path_cost + h(n), display)


"""""""""""""""""""""
MAIN FUNCTIONS
"""""""""""""""""""""

def solve_puzzle_and_analyze_algorithm(title, problem, h=None, display=False):
    print(f"\nDoing A* search with {title}:")
    start_time = time.time()
    search_puzzle, nodes_removed = astar_search_a1(problem, h, display)
    elapsed_time = time.time() - start_time

    print("Solution: ", search_puzzle.solution())
    print(f'Elapsed time (in seconds): {elapsed_time}s')
    print("Length of the solution: ", len(search_puzzle.solution()))
    print("Nodes removed from frontier: ", nodes_removed)

    return search_puzzle


# Create 10 random EightPuzzle problems, and solve and analyze them
def main_EightPuzzle():
    for round in range(10):
        print("========== 8-PUZZLE ROUND", round + 1, "==========")
        new_puzzle = make_rand_8puzzle()
        print("Displaying initial state:")
        display(new_puzzle.initial)

        # For all these algorithms, Display = False
        solved_puzzle_mt = solve_puzzle_and_analyze_algorithm("the misplaced tile heuristic", new_puzzle, new_puzzle.h)
        display(solved_puzzle_mt.state)
        solved_puzzle_md = solve_puzzle_and_analyze_algorithm("the Manhattan distance heuristic", new_puzzle, new_puzzle.manhattan_distance)
        display(solved_puzzle_md.state)
        solved_puzzle_max = solve_puzzle_and_analyze_algorithm("the heuristic of the maximum value", new_puzzle, new_puzzle.max_heuristic)
        display(solved_puzzle_max.state)


# Solve and analyze 10 explicitly known EightPuzzle problems
def main_EightPuzzle_test():
    # Test puzzles, from:
    # https://www.andrew.cmu.edu/course/15-121/labs/HW-7%20Slide%20Puzzle/lab.html
    test_8puzzles = ((1, 2, 3, 4, 0, 5, 7, 8, 6), # 2 moves
                     (1, 2, 3, 4, 8, 0, 7, 6, 5), # 5 moves
                     (1, 6, 2, 5, 3, 0, 4, 7, 8), # 9 moves
                     (5, 1, 2, 6, 3, 0, 4, 7, 8), # 11 moves
                     (1, 2, 6, 3, 5, 0, 4, 7, 8), # 13 moves
                     (3, 5, 6, 1, 4, 8, 0, 7, 2), # 16 moves
                     (4, 3, 6, 8, 7, 1, 0, 5, 2), # 18 moves
                     (3, 0, 2, 6, 5, 1, 4, 7, 8), # 21 moves
                     (5, 0, 3, 2, 8, 4, 6, 7, 1), # 23 moves
                     (8, 7, 4, 3, 2, 0, 6, 5, 1)  # 25 moves
                    )

    
    for round in range(10):
        print("========== 8-PUZZLE ROUND", round + 1, "==========")
        new_puzzle = EightPuzzleExtended(test_8puzzles[round])
        
        check_initial_state = new_puzzle.check_solvability(new_puzzle.initial)
        print("Initial state's solvability check: ", check_initial_state)
        print("Displaying initial state:")
        display(new_puzzle.initial)

        # For all these algorithms, Display = False
        solved_puzzle_mt = solve_puzzle_and_analyze_algorithm("the misplaced tile heuristic", new_puzzle, new_puzzle.h)
        display(solved_puzzle_mt.state)
        solved_puzzle_md = solve_puzzle_and_analyze_algorithm("the Manhattan distance heuristic", new_puzzle, new_puzzle.manhattan_distance)
        display(solved_puzzle_md.state)
        solved_puzzle_max = solve_puzzle_and_analyze_algorithm("the heuristic of the maximum value", new_puzzle, new_puzzle.max_heuristic)
        display(solved_puzzle_max.state)


# Create 10 random DuckPuzzle problems, and solve and analyze them
def main_DuckPuzzle():
    for round in range(10):
        print("========== DUCK PUZZLE ROUND", round + 1, "==========")
        new_puzzle = make_rand_duckpuzzle()
        print("Displaying initial state:")
        display_duck_puzzle(new_puzzle.initial)

        # For all these algorithms, Display = False
        solved_puzzle_mt = solve_puzzle_and_analyze_algorithm("the misplaced tile heuristic", new_puzzle, new_puzzle.h)
        display_duck_puzzle(solved_puzzle_mt.state)
        solved_puzzle_md = solve_puzzle_and_analyze_algorithm("the Manhattan distance heuristic", new_puzzle, new_puzzle.manhattan_distance)
        display_duck_puzzle(solved_puzzle_md.state)
        solved_puzzle_max = solve_puzzle_and_analyze_algorithm("the heuristic of the maximum value", new_puzzle, new_puzzle.max_heuristic)
        display_duck_puzzle(solved_puzzle_max.state)


if __name__ == "__main__":
    main_EightPuzzle()
    # main_EightPuzzle_test()
    # main_DuckPuzzle()
