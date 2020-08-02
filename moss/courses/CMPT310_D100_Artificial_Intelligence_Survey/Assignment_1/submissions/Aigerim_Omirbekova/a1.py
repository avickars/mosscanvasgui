#!/usr/bin/env python3
import random
import time
import os
import csv
import argparse
from utils import *
from search import *

# There are some modified functions taken from other files within this
# project. Those functions' copies are placed in this files and indicted in the description
# where they're coming from.

# Optional, taking arguments from the user
parser = argparse.ArgumentParser(description='To output a description file (.csv)')
parser.add_argument('--output_dir', '-o', help='Path to output directory to write file into', required=False)
parser.add_argument('--tests', '-t', help='Number of test puzzles to generate', required=False)
args = parser.parse_args()

# Modified algorithms
def best_first_graph_search_modified(problem, f, display=False):
    """This is a modified copy of best_first_graph_search from search.py. Returns 
    number of removed nodes from frontier and number of tiles moved. Search the nodes with 
    the lowest f scores first.
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
    removed = 0
    while frontier:
        node = frontier.pop()
        removed = removed + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, removed]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def astar_search_modified(problem, h=None, display=False):
    """This is a modified copy of astar_search from search.py. A* search is 
    best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_modified(problem, lambda n: n.path_cost + h(n), display)


#--------- QUESTION 1 ---------------------------------------------------------------------------------------------------

def make_rand_8puzzle():
    state = random.sample(range(0, 9), 9)
    puzzle_tuple = EightPuzzle(tuple(state))
    while True:
        if puzzle_tuple.check_solvability(state):
            return puzzle_tuple
        else:
            state = random.sample(range(0, 9), 9)
            puzzle_tuple.initial = tuple(state)

def display(state):
    if len(state) == 0:
        print("State is empty")
    state_list = list(state)
    state_list[state.index(0)] = "*"
    for i in range(0, 7, 3):
        print(state_list[i], state_list[i+1], state_list[i+2])
    print("\n")


#--------- QUESTION 2 ---------------------------------------------------------------------------------------------------

if not args.tests:
    print("No tests number specified, default 1")
    tests_num = 1
else:
    tests_num = int(args.tests)

def manhattan_h(node):
    """This is a modified version of manhattan function from test_search.py that doesn't 
    include the estimation for 0 tile to maintain admissibility of the algorithm"""

    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    moves_sum = 0

    for i in range(1, 9):
        for j in range(2):
            moves_sum = abs(index_goal[i][j] - index_state[i][j]) + moves_sum

    return moves_sum

def max_h(node):
    """This function returns the max of the misplaced tile heuristic and the 
    Manhattan distance heuristic"""

    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    man_sum = manhattan_h(node)
    max_sum = sum(s != g for (s, g) in zip(node.state, goal))
    return man_sum if man_sum > max_sum else max_sum

def eight_test(tests_num):
    # EightPuzzle test
    eight_puzzle_list = []
    eight_initial_states = []
    mis_8p_solutions = []
    man_8p_solutions = []
    max_8p_solutions = []

    # EightPuzzle instances initialization
    for i in range(tests_num):
        eight_puzzle_list.append(make_rand_8puzzle())
        eight_initial_states.append(eight_puzzle_list[i].initial)
        display(eight_initial_states[i])


    # Misplaced tile heuristic test
    mis_8p_sum = 0
    mis_removed_tot = 0
    mis_start_time = time.time()
    for i in range(tests_num):
        mis_8p_solutions.append(astar_search_modified(eight_puzzle_list[i]))
        mis_8p_sum = mis_8p_sum + len(mis_8p_solutions[i][0].solution())
        mis_removed_tot = mis_removed_tot + mis_8p_solutions[i][1]
    mis_tot_time = time.time() - mis_start_time
    print("Misplaced tile heuristic time test: \n--- %s seconds ---" % (mis_tot_time))
    print("Number of moves in total: ", mis_8p_sum)
    print("Number of removed nodes in total: ", mis_removed_tot, "\n\n")

    # Manhattan distance heuristic test
    man_8p_sum = 0
    man_removed_tot = 0
    man_start_time = time.time()
    for i in range(tests_num):
        man_8p_solutions.append(astar_search_modified(eight_puzzle_list[i], h = manhattan_h))
        man_8p_sum = man_8p_sum + len(man_8p_solutions[i][0].solution())
        man_removed_tot = man_removed_tot + man_8p_solutions[i][1]
    man_tot_time = time.time() - man_start_time
    print("Manhattan distance heuristic time test: \n--- %s seconds ---" % (man_tot_time))
    print("Number of moves in total: ", man_8p_sum)
    print("Number of removed nodes in total: ", man_removed_tot, "\n\n")


    # Max test
    max_8p_sum = 0
    max_removed_tot = 0
    max_start_time = time.time()
    for i in range(tests_num):
        max_8p_solutions.append(astar_search_modified(eight_puzzle_list[i], h = max_h))
        max_8p_sum = max_8p_sum + len(max_8p_solutions[i][0].solution())
        max_removed_tot = max_removed_tot + max_8p_solutions[i][1]
    max_tot_time = time.time() - max_start_time
    print("Max time test: \n--- %s seconds ---" % (max_tot_time))    
    print("Number of moves in total: ", max_8p_sum)
    print("Number of removed nodes in total: ", max_removed_tot, "\n\n")
    return [mis_tot_time, man_tot_time, max_tot_time, mis_8p_sum, man_8p_sum, max_8p_sum,
    mis_removed_tot, man_removed_tot, max_removed_tot]

#--------- QUESTION 3 ---------------------------------------------------------------------------------------------------

class DuckPuzzle(Problem):
    """ This is a modified version of EightPuzzle class with some additions. A state is represented as 
    a tuple of length 9, where  element at index i represents the tile number  
    at index i (0 if it's empty) """

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
        if index_blank_square <= 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square >= 6:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
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
    
    def manhattan_h(self, node):
        """This is a modified version of manhattan function from test_search.py that doesn't 
        include the estimation for 0 tile to maintain admissibility of the algorithm"""

        state = node.state
        print("The state is ", state)
        index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
        index_state = {}
        index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]
        print("Index state: ", index_state)

        moves_sum = 0

        for i in range(1, 9):
            print("Move ", i, " from ", index_state[i], "to", index_goal[i])
            for j in range(2):
                moves_sum = abs(index_goal[i][j] - index_state[i][j]) + moves_sum
                print(abs(index_goal[i][j] - index_state[i][j]))

        return moves_sum

    def max_h(self, node):
        """This function returns the max of the misplaced tile heuristic and the 
        Manhattan distance heuristic"""

        goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        man_sum = manhattan_h(node)
        max_sum = sum(s != g for (s, g) in zip(node.state, goal))
        print("Manhattan: ", man_sum)
        print("Misplaced Heuristic: ", max_sum)
        return man_sum if man_sum > max_sum else max_sum

    def display(self):
        """ Display an object """
        state = self.initial
        if len(state) == 0:
            print("State is empty")
        state_list = list(state)
        state_list[state.index(0)] = "*"
        print(state_list[0], state_list[1]) 
        print(state_list[2], state_list[3], state_list[4], state_list[5])
        print(" ", state_list[6], state_list[7], state_list[8])
        print("\n")

def make_rand_duckPuzzle():
    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    puzzle_tuple = DuckPuzzle(tuple(state))
    shuffles = random.randint(50, 100)
    for i in range(shuffles):
        rand_action = puzzle_tuple.actions(state)
        action_num = random.randint(0, len(rand_action) - 1)
        state = list(puzzle_tuple.result(state, rand_action[action_num]))
        puzzle_tuple.initial = tuple(state)
    return puzzle_tuple

    # DuckPuzzle test
def duck_test(tests_num):
    duck_puzzle_list = []
    duck_initial_states = []
    mis_duck_solutions = []
    man_duck_solutions = []
    max_duck_solutions = []

    # DuckPuzzle instances initialization
    for i in range(tests_num):
        duck_puzzle_list.append(make_rand_duckPuzzle())
        duck_initial_states.append(duck_puzzle_list[i].initial)
        duck_puzzle_list[i].display()

    # Misplaced tile heuristic test
    mis_duck_sum = 0
    mis_removed_tot = 0
    mis_start_time = time.time()
    for i in range(tests_num):
        mis_duck_solutions.append(astar_search_modified(duck_puzzle_list[i]))
        mis_duck_sum = mis_duck_sum + len(mis_duck_solutions[i][0].solution())
        mis_removed_tot = mis_removed_tot + mis_duck_solutions[i][1]
    mis_tot_time = time.time() - mis_start_time
    print("Misplaced tile heuristic time test: \n--- %s seconds ---" % (mis_tot_time))
    print("Number of moves in total: ", mis_duck_sum)
    print("Number of removed nodes in total: ", mis_removed_tot, "\n\n")


    # Manhattan distance heuristic test
    man_duck_sum = 0
    man_removed_tot = 0
    man_start_time = time.time()
    for i in range(tests_num):
        man_duck_solutions.append(astar_search_modified(duck_puzzle_list[i], h = manhattan_h))
        man_duck_sum = man_duck_sum + len(man_duck_solutions[i][0].solution())
        man_removed_tot = man_removed_tot + man_duck_solutions[i][1]
    man_tot_time = time.time() - man_start_time
    print("Manhattan distance heuristic time test: \n--- %s seconds ---" % (man_tot_time))
    print("Number of moves in total: ", man_duck_sum)
    print("Number of removed nodes in total: ", man_removed_tot, "\n\n")


    # Max test
    max_duck_sum = 0
    max_removed_tot = 0
    max_start_time = time.time()
    for i in range(tests_num):
        max_duck_solutions.append(astar_search_modified(duck_puzzle_list[i], h = max_h))
        max_duck_sum = max_duck_sum + len(max_duck_solutions[i][0].solution())
        max_removed_tot = max_removed_tot + max_duck_solutions[i][1]
    max_tot_time = time.time() - max_start_time
    print("Max time test: \n--- %s seconds ---" % (max_tot_time))
    print("Number of moves in total: ", max_duck_sum)
    print("Number of removed nodes in total: ", max_removed_tot, "\n\n")
    return [mis_tot_time, man_tot_time, max_tot_time, mis_duck_sum, man_duck_sum, max_duck_sum,
    mis_removed_tot, man_removed_tot, max_removed_tot]

# writing output
if args.output_dir:
    print("Output directory specified: ", args.output_dir)
    output_file = os.path.join(args.output_dir, "out.csv")
    with open(output_file, 'w') as out_csv:
        fields = ['number', '8p_misplaced_time', '8p_manhattan_time', '8p_max_time', 
        'duck_misplaced_time', 'duck_manhattan_time', 'duck_max_time', '8p_misplaced_length', '8p_manhattan_length', '8p_max_length', 
        'duck_misplaced_length', 'duck_manhattan_length', 'duck_max_length', '8p_misplaced_removed', '8p_manhattan_removed', '8p_max_removed', 
        'duck_misplaced_removed', 'duck_manhattan_removed', 'duck_max_removed']
        writer = csv.writer(out_csv)
        writer.writerow(fields)
        row_list =[]
        # for i in range(tests_num):
        row_list.append(eight_test(10))
        row_list.append(duck_test(10))
        writer.writerow([str(10), row_list[0], row_list[1]])
        
        writer.writerow({})
else:
    eight_test(1)
    duck_test(1)

        