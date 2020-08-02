import random
from search import *
import time


# QUESTION 1

def make_rand_8puzzle():
    init_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(init_state)  # random shuffle the states
    puzzle = EightPuzzle(tuple(init_state))
    while puzzle.check_solvability(init_state) is False:
        random.shuffle(init_state)
        puzzle = EightPuzzle(tuple(init_state))
    return puzzle


def display(state):
    star_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(9):
        star_state[i] = state[i]
        if star_state[i] == 0:
            star_state[i] = "*"
    print(star_state[0], star_state[1], star_state[2], sep=" ")
    print(star_state[3], star_state[4], star_state[5], sep=" ")
    print(star_state[6], star_state[7], star_state[8], sep=" ")


# QUESTION 2

def best_first_graph_search(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    count = 0
    while frontier:
        node = frontier.pop()
        count += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, count
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, count


def astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def manhattan(node):
    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0
    for i in range(1, 9):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
    return mhd


def relative_max(node):
    puzzle = EightPuzzle(node.state)
    return max(manhattan(node), puzzle.h(node))


def time_analysis():
    print("\n")
    for instance in range(10):
        print("Instance Number: ", instance)
        default_puzzle = make_rand_8puzzle()
        man_search_puzzle = default_puzzle
        relative_max_puzzle = man_search_puzzle

        display(default_puzzle.initial)
        print("\nBy using the Default Heuristic Search: ")
        start_time = time.time()
        result_default, no_nodes_removed = astar_search(default_puzzle)
        elapsed_time = time.time() - start_time
        print("The elapsed time (in seconds): ", elapsed_time)
        result_length = len(result_default.solution())
        print("The length of solution is", result_length)
        print("The total number of nodes that were removed from frontier is ", no_nodes_removed)

        print("\nBy using the Manhattan Distance Heuristic Search:")
        start_time_manhattan = time.time()
        result_manhattan, no_nodes_removed_manhattan = astar_search(man_search_puzzle, h=manhattan)
        elapsed_time_manhattan = time.time() - start_time_manhattan
        print("The elapsed time (in seconds): ", elapsed_time_manhattan)
        result_length_manhattan = len(result_manhattan.solution())
        print("The length of solution is", result_length_manhattan)
        print("The total number of nodes that were removed from frontier is ", no_nodes_removed_manhattan)

        print("\nBy using the max of both Heuristic Searches: ")
        start_time_max = time.time()
        result_default_max, no_nodes_removed_max = astar_search(relative_max_puzzle, h=relative_max)
        elapsed_time_max = time.time() - start_time_max
        print("The elapsed time (in seconds): ", elapsed_time_max)
        result_length_max = len(result_default_max.solution())
        print("The length of solution is", result_length_max)
        print("The total number of nodes that were removed from frontier is ", no_nodes_removed_max)
        print("\n")


time_analysis()
