from search import Problem, EightPuzzle, astar_search, Node, PriorityQueue, memoize
import numpy as np
import random
import time

# Used to shuffle the duck puzzle starting from goal
NUM_OF_RANDOM_MOVES = 200

#------ QUESTION #1----------------------------------------------------#


def make_rand_8puzzle():
    new8puzzle = EightPuzzle(tuple(np.random.permutation(9)))
    while not new8puzzle.check_solvability(new8puzzle.initial):
        new8puzzle = EightPuzzle(tuple(np.random.permutation(9)))
    return new8puzzle


def display(state):
    toPrint = list(state)
    toPrint[toPrint.index(0)] = '*'
    for i in range(0, len(toPrint), 3):
        print(toPrint[i], toPrint[i+1], toPrint[i+2])


#------ QUESTION #2----------------------------------------------------#
def manhattan_h(node):
    # Goal coordinates for each value
    goal_map = {0: (3, 3), 1: (1, 1), 2: (2, 1), 3: (3, 1), 4: (
        1, 2), 5: (2, 2), 6: (3, 2), 7: (1, 3), 8: (2, 3)}
    # Maps indexes 0-8 to coordinates on the board
    index_map = {0: (1, 1), 1: (2, 1), 2: (3, 1), 3: (1, 2), 4: (
        2, 2), 5: (3, 2), 6: (1, 3), 7: (2, 3), 8: (3, 3)}
    res = 0
    for i, val in enumerate(node.state):
        # Ignore empty space
        if val == 0:
            continue
        res += abs(index_map[i][0] - goal_map[val][0]) + \
            abs(index_map[i][1] - goal_map[val][1])
    return res


def max_h(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    # Misplaced tile heuristic code copied from search.py
    return max(sum(s != g for (s, g) in zip(node.state, goal)), manhattan_h(node))


def solution_report(sol, time):
    sol_node = sol['node']
    print(f' - elapsed time (in seconds): {time}')
    print(' - solution length: ', len(sol_node.solution()))
    print(' - nodes removed from frontier: ', sol['removed'])


def compare_8puzzle():
    for i in range(0, 10):
        print('Puzzle #', i)
        ep = make_rand_8puzzle()
        print('-------')
        display(ep.initial)
        print('-------')

        start_time = time.time()
        misplaced_h_sol = astar_search(ep)
        elapsed_time = time.time() - start_time

        print('Misplaced tile heuristic:')
        solution_report(misplaced_h_sol, elapsed_time)

        start_time = time.time()
        manhattan_h_sol = astar_search(ep, manhattan_h)
        elapsed_time = time.time() - start_time

        print('Manhattan heuristic:')
        solution_report(manhattan_h_sol, elapsed_time)

        start_time = time.time()
        max_h_sol = astar_search(ep, max_h)
        elapsed_time = time.time() - start_time

        print('Max of previous two heuristics:')
        solution_report(max_h_sol, elapsed_time)

        print('<-------------------------------------->')


#------ QUESTION #3----------------------------------------------------#
""" 
MODIFIED best_first_search to return nodes removed from frontier as shown below
"""


def best_first_graph_search(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    removed = 0
    while frontier:
        node = frontier.pop()
        removed += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and",
                      len(frontier), "paths remain in the frontier")
            return {'node': node, 'removed': removed}
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
-------------DUCK PROBLEM CLASS------------------------------
-------*Code was copied from search.py then modified---------
"""


class DuckPuzzle(Problem):
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

        left_blocked = {0, 2, 6}
        right_blocked = {1, 5, 8}
        up_blocked = {0, 1, 4, 5}
        down_blocked = {2, 6, 7, 8}

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square in left_blocked:
            possible_actions.remove('LEFT')
        if index_blank_square in up_blocked:
            possible_actions.remove('UP')
        if index_blank_square in right_blocked:
            possible_actions.remove('RIGHT')
        if index_blank_square in down_blocked:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank in {0, 1}:
            delta['DOWN'] = 2
        elif blank in {2, 3}:
            delta['UP'] = -2

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
*Helper Functions* 
'''


def make_rand_duck_puzzle():
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    dpuzzle = DuckPuzzle(state)
    for i in range(NUM_OF_RANDOM_MOVES):
        actions = dpuzzle.actions(state)
        state = dpuzzle.result(
            state, actions[random.randint(0, len(actions)-1)])
    return DuckPuzzle(state)


def display_duck(state):
    toPrint = list(state)
    toPrint[toPrint.index(0)] = '*'
    print(toPrint[0], toPrint[1])
    print(toPrint[2], toPrint[3], toPrint[4], toPrint[5])
    print(' ', toPrint[6], toPrint[7], toPrint[8])


def manhattan_duck(node):
    # Goal coordinates for each value
    goal_map = {0: (4, 3), 1: (1, 1), 2: (2, 1), 3: (1, 2), 4: (
        2, 2), 5: (3, 2), 6: (4, 2), 7: (2, 3), 8: (3, 3)}
    # Maps indexes 0-8 to coordinates on the board
    index_map = {0: (1, 1), 1: (2, 1), 2: (1, 2), 3: (2, 2), 4: (
        3, 2), 5: (4, 2), 6: (2, 3), 7: (3, 3), 8: (4, 3)}
    res = 0
    for i, val in enumerate(node.state):
        # Ignore empty space
        if val == 0:
            continue
        res += abs(index_map[i][0] - goal_map[val][0]) + \
            abs(index_map[i][1] - goal_map[val][1])
    return res


def max_h_duck(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    # Misplaced tile heuristic code copied from search.py
    return max(sum(s != g for (s, g) in zip(node.state, goal)), manhattan_duck(node))


def compare_duckpuzzle():
    for i in range(0, 10):
        print('Puzzle #', i)
        dp = make_rand_duck_puzzle()
        print('-------')
        display_duck(dp.initial)
        print('-------')

        start_time = time.time()
        misplaced_h_sol = astar_search(dp)
        elapsed_time = time.time() - start_time

        print('Misplaced tile heuristic:')
        solution_report(misplaced_h_sol, elapsed_time)

        start_time = time.time()
        manhattan_h_sol = astar_search(dp, manhattan_duck)
        elapsed_time = time.time() - start_time

        print('Manhattan heuristic:')
        solution_report(manhattan_h_sol, elapsed_time)

        start_time = time.time()
        max_h_sol = astar_search(dp, max_h_duck)
        elapsed_time = time.time() - start_time

        print('Max of previous two heuristics:')
        solution_report(max_h_sol, elapsed_time)

        print('<-------------------------------------->')


print('--8 PUZZLE ANALYSIS')
compare_8puzzle()
print('\n--DUCK PUZZLE ANALYSIS')
compare_duckpuzzle()