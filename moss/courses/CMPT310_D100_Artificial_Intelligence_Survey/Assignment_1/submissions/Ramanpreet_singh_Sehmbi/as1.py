# a1.py

import random
import time
from search import *
# ...

# Question 1: Write a function called make_rand_8puzzle() that returns a new instance of an EightPuzzle problem
# with a random initial state that is solvable. Note that EightPuzzle has a method called check_solvability that you should use to help ensure your initial state is solvable.
# Write a function called display(state) that takes an 8 - puzzle state(i.e.a tuple that
# is a permutation of(0, 1, 2, …, 8)) as input and prints a neat and readable representation of it. 0 is the blank, and should be printed as a * character.


def make_rand_8puzzle():

    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    convert_to_list = list(state)
    random.shuffle(convert_to_list)
    final_state = tuple(convert_to_list)
    puzzle = EightPuzzle(final_state)

    # print("Here!")
    while (puzzle.check_solvability(final_state) == False):
        convert_to_list = list(state)
        random.shuffle(convert_to_list)
        final_state = tuple(convert_to_list)
        puzzle = EightPuzzle(final_state)

     # display(final_state)
    return puzzle


def display(state):
    convert_to_list = list(state)

    for index, element in enumerate(convert_to_list):
        if element == 0:
            convert_to_list[index] = '*'

    row1 = ''
    row2 = ''
    row3 = ''

    for iterator in range(0, 3):
        row1 = row1 + str(convert_to_list[iterator]) + ' '

    for iterator in range(3, 6):
        row2 = row2 + str(convert_to_list[iterator]) + ' '

    for iterator in range(6, 9):
        row3 = row3 + str(convert_to_list[iterator]) + ' '

    final_matrix = row1 + '\n' + row2 + '\n' + row3 + '\n'
    # print(final_matrix)
    return final_matrix


# Question 2 : a) Misplaced Tile Heuristic
# b) A*-search using the Manhattan distance heuristic Please implement your own (correctly working!) version of the Manhattan heuristic.
# Be careful: there is an incorrect Manhattan distance function in tests/test_search.py. So don’t use that!
# c) A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic

def astar_search(problem, h=None, display=False):
    # """A* search is best-first graph search with f(n) = g(n)+h(n).
    #     You need to specify the h function when you call astar_search, or
    #     lse in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def misplaced_tile_heuristic(node):
    # """ Return the heuristic value for a given state. Default heuristic function used is
    #     h(n) = number of misplaced tiles """
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return sum(s != g for (s, g) in zip(node.state, goal))

# Code referred from tests/search.py in aima-python library


def Manhattan_heuristic(node):
    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2],
                  4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [
        1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    x, y = 0, 0

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    # Don't include zero. The heuristic function never ever overestimate the true cost
    # but the default one does
    for i in range(1, 9):
        for j in range(2):
            a = index_goal[i][j]
            b = index_state[i][j]
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

    return mhd


def max_misplaced_tile_heuristic_Manhattan_heuristic(node):
    misplaced_tile_heuristics = misplaced_tile_heuristic(node)
    Manhattan_heuristics = Manhattan_heuristic(node)
    maximum_heuristic = max(misplaced_tile_heuristics, Manhattan_heuristics)
    # print("Max of ", h, " and ", mht, " is ", max_h_mht)
    return maximum_heuristic


def best_first_graph_search(problem, f, display=False):
    # """Search the nodes with the lowest f scores first.
    # You specify the function f(node) that you want to minimize; for example,
    # if f is a heuristic estimate to the goal, then we have greedy best
    # first search; if f is node.depth then we have breadth-first search.
    # There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    # values will be cached on the nodes as they are computed. So after doing
    # a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and",
                      len(frontier), "paths remain in the frontier")
            return (node, len(explored))
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


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

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions.remove('UP')
            possible_actions.remove('LEFT')
        if index_blank_square == 1:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 2:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 6:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # delta = {'UP': 0, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 0}

        if blank == 0:
            delta = {'UP': 0, 'DOWN': 2, 'LEFT': 0, 'RIGHT': 1}
        if blank == 1:
            delta = {'UP': 0, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 0}
        if blank == 2:
            delta = {'UP': -2, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}
        if blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank == 4:
            delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank == 5:
            delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 0}
        if blank == 6:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}
        if blank == 7:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
        if blank == 8:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 0}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))


def make_duck_puzzle(duckpuzzle):
    initial_state = duckpuzzle.initial

    for iterator in range(0, 100000):
        possible_actions = duckpuzzle.actions(initial_state)
        choosed_action = random.choice(possible_actions)
        initial_state = duckpuzzle.result(initial_state, choosed_action)

    duckpuzzle.initial = initial_state
    # print("Success")
    # display_duck_puzzle(duckpuzzle.initial)
    return duckpuzzle


def display_duck_puzzle(state):
    convert_to_list = list(state)

    for index, element in enumerate(convert_to_list):
        if element == 0:
            convert_to_list[index] = '*'

    row1 = ''
    row2 = ''
    row3 = ' '

    for iterator in range(0, 2):
        row1 = row1 + str(convert_to_list[iterator]) + ' '

    for iterator in range(2, 6):
        row2 = row2 + str(convert_to_list[iterator]) + ' '

    for iterator in range(6, 9):
        row3 = row3 + str(convert_to_list[iterator]) + ' '

    final_matrix = row1 + '\n' + row2 + '\n' + row3 + '\n'
    print(final_matrix)
    return final_matrix


def h(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return sum(s != g for (s, g) in zip(node.state, goal))


def manhattan(node):
    state = node.state
    index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [
        1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
    index_state = {}
    index = [[0, 0], [0, 1], [1, 0], [1, 1], [
        1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]
    x, y = 0, 0

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    # Don't include zero. The heuristic function never ever overestimate the true cost
    # but the default one does
    for i in range(1, 9):
        for j in range(2):
            a = index_goal[i][j]
            b = index_state[i][j]
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

    return mhd


def max_(node):
    heu = h(node)
    man = manhattan(node)
    maximum_heuristic = max(heu, man)
    return maximum_heuristic


if __name__ == "__main__":
    # Question1 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("Question 1 Created a random puzzle and printing a random 8 word puzzle")
    rand_puzzle = make_rand_8puzzle()
    created_puzzle = display(rand_puzzle.initial)
    print(created_puzzle)
    # Question2-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("Question2:- Results------------------------------- ")
    print("\n")
    for iterator in range(1, 11):
        print("Iteration"+str(iterator)+"\n")
        puzzle = make_rand_8puzzle()

        start_time = time.time()
        node_1, frontier_1 = astar_search(puzzle, misplaced_tile_heuristic)
        elapsed_time = time.time() - start_time

        print("Nodes removed from frontier for Misplaced Tile Heuristic", frontier_1)
        print("Number of tiles moved Misplaced Tile Heuristic",
              len(node_1.solution()))
        print("Elapsed time for Misplaced Tile Heuristic (in seconds):", elapsed_time)
        print("\n")

        start_time = time.time()
        node_2, frontier_2 = astar_search(puzzle, Manhattan_heuristic)
        elapsed_time2 = time.time() - start_time
        print("Nodes removed from frontier for Manhattan Heuristic", frontier_2)
        print("Number of tiles moved for Manhattan Heuristic",
              len(node_2.solution()))
        print("Elapsed time for Manhattan (in seconds):", elapsed_time2)
        print("\n")

        start_time = time.time()
        node_3, frontier_3 = astar_search(
            puzzle, max_misplaced_tile_heuristic_Manhattan_heuristic)
        elapsed_time3 = time.time() - start_time
        print("Nodes removed from frontier for Max(Misplaced, Manhattan) Heuristic ", frontier_3)
        print("Number of tiles moved for Max(Misplaced, Manhattan) Heuristic", len(
            node_3.solution()))
        print("elapsed time for Max(Misplaced, Manhattan) Heuristic(in seconds):", elapsed_time3)
        print("\n")

    print("\n")
    # Question3:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("Question3:- Results------------------------------- \n")
    for iterator in range(1, 11):
        print("Iteration"+str(iterator)+"\n")
        state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        duck = DuckPuzzle(state)
        duckpuzzle = make_duck_puzzle(duck)

        start_time = time.time()
        node_1, frontier_1 = astar_search(duckpuzzle, duckpuzzle.h)
        elapsed_time_1 = time.time() - start_time

        print("Nodes removed from frontier for Misplaced Tile Heuristic for Duck Puzzle", frontier_1)
        print("Number of tiles moved for Misplaced Tile Heuristic for Duck Puzzle", len(
            node_1.solution()))
        print("Elapsed time for Misplaced Tile Heuristic for Duck Puzzle (in seconds):", elapsed_time_1)
        print("\n")

        start_time = time.time()
        node_2, frontier_2 = astar_search(duckpuzzle, manhattan)
        elapsed_time_2 = time.time() - start_time

        print("Nodes removed from frontier for Manhattan Heuristic for Duck Puzzle", frontier_2)
        print("Number of tiles moved for Manhattan Heuristic for Duck Puzzle",
              len(node_2.solution()))
        print("Elapsed time for Manhattan Heuristic for Duck Puzzle (in seconds):", elapsed_time_2)
        print("\n")

        start_time = time.time()
        node_3, frontier_3 = astar_search(duckpuzzle, max_)
        elapsed_time_3 = time.time() - start_time

        print("Nodes removed from frontier for max(Misplaced Tile, Manhattan) Heuristic for Duck Puzzle", frontier_3)
        print("Number of tiles moved for max(Misplaced Tile, Manhattan) Heuristic for Duck Puzzle", len(
            node_3.solution()))
        print("Elapsed time for max(Misplaced Tile, Manhattan) Heuristic for Duck Puzzle (in seconds):", elapsed_time_3)
        print("\n")
