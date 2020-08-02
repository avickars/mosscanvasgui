# a1.py

from search import *
import random
import time


# ---------- Question 1 ----------

def make_rand_8puzzle():
    state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    solvability = False
    while not solvability:
        random.shuffle(state)
        solvability = EightPuzzle.check_solvability(None, state)
    problem = EightPuzzle(tuple(state))
    return problem


def display(state):
    tmp = ''
    for i in range(9):
        num = state[i]
        if num != 0:
            tmp += str(num)
        else:
            tmp += '*'

        if i % 3 == 2:
            print(tmp)
            tmp = ''
        else:
            tmp += ' '


# ---------- End of Question 1 ----------


# ---------- function from textbook code (modified for Q2) ----------

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
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored))
            return node, len(explored)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def astar_search(problem, h_name, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    if h_name == 'misplaced_tiles':
        h = memoize(problem.misplaced_tiles_heuristic, 'h')
    elif h_name == 'manhattan_distance':
        h = memoize(problem.manhattan_distance_heuristic, 'h')
    else:
        h = memoize(problem.max_heuristic, 'h')
    # print(problem.h(Node(problem.initial)))
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


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

    def misplaced_tiles_heuristic(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))
        # return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan_distance_heuristic(self, node):
        """ return the smallest number of move to be the goal state as heuristic value """

        dist = 0
        for i in range(9):
            statenum = node.state[i]
            if statenum != self.goal[i] and statenum != 0:
                current_row = i // 3
                goal_row = (statenum - 1) // 3
                current_col = i % 3
                goal_col = (statenum - 1) % 3
                move = abs(current_row - goal_row) + abs(current_col - goal_col)
                dist += move
        return dist

    def max_heuristic(self, node):
        """ return the max number between misplaced tiles heuristic value and manhattan distance heuristic value """

        return max(self.misplaced_tiles_heuristic(node), self.manhattan_distance_heuristic(node))


# ---------- End of Textbook Code ----------


# ---------- Question 3 ----------

class DuckPuzzle(Problem):
    """ Duck Puzzle is like 8-puzzle, but with a little change on the shape"""

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

        if index_blank_square in (0, 2, 7):
            possible_actions.remove('LEFT')
        if index_blank_square in (0, 1, 4, 5):
            possible_actions.remove('UP')
        if index_blank_square in (1, 5, 8):
            possible_actions.remove('RIGHT')
        if index_blank_square in (2, 6, 7, 8):
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank < 2:
            delta['DOWN'] = 2
        elif blank < 4:
            delta['UP'] = -2

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def misplaced_tiles_heuristic(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

    def manhattan_distance_heuristic(self, node):
        """ return the smallest number of move to be the goal state as heuristic value """

        dist = 0
        row = {0: 1, 1: 1, 2: 2, 3: 2, 4: 2, 5: 2, 6: 3, 7: 3, 8: 3}
        col = {0: 1, 1: 2, 2: 1, 3: 2, 4: 3, 5: 4, 6: 2, 7: 3, 8: 4}

        for i in range(9):
            statenum = node.state[i]
            if statenum != self.goal[i] and statenum != 0:
                current_row = row[i]
                goal_row = row[statenum - 1]
                current_col = col[i]
                goal_col = col[statenum - 1]
                move = abs(current_row - goal_row) + abs(current_col - goal_col)
                dist += move

        return dist

    def max_heuristic(self, node):
        """ return the max number between misplaced tiles heuristic value and manhattan distance heuristic value """

        return max(self.misplaced_tiles_heuristic(node), self.manhattan_distance_heuristic(node))


def make_rand_duck_puzzle():
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    duck_puzzle = DuckPuzzle(state)
    while duck_puzzle.goal_test(state):
        for i in range(10000):
            action = random.choice(duck_puzzle.actions(state))
            state = duck_puzzle.result(state, action)
    return DuckPuzzle(state)


def display_duck_puzzle(state):
    tmp = str(state[0]) + ' ' + str(state[1])
    tmp = tmp.replace('0', '*')
    print(tmp)
    tmp = str(state[2]) + ' ' + str(state[3]) + ' ' + str(state[4]) + ' ' + str(state[5])
    tmp = tmp.replace('0', '*')
    print(tmp)
    tmp = '  ' + str(state[6]) + ' ' + str(state[7]) + ' ' + str(state[8])
    tmp = tmp.replace('0', '*')
    print(tmp)

# ---------- End of Question 3 ----------


def solve_puzzle(problem, method):
    start_time = time.time()
    node, explored = astar_search(problem, method)
    elapsed_time = time.time() - start_time
    print(f'{method}:')
    print(f'\telapsed time (in seconds): {elapsed_time}s')
    print(f'\tsolution length: {len(node.solution())}')
    print(f'\tnumber of nodes removed from frontier: {explored}\n')


print('Eight-Puzzle:\n')
for i in range(10):
    eight_puzzle = make_rand_8puzzle()
    print(f'Eight Puzzle {i + 1}:')
    display(eight_puzzle.initial)
    print()
    solve_puzzle(eight_puzzle, 'misplaced_tiles')
    solve_puzzle(eight_puzzle, 'manhattan_distance')
    solve_puzzle(eight_puzzle, 'mix_heuristic')

print('Duck-Puzzle:\n')
for i in range(10):
    duck_puzzle = make_rand_duck_puzzle()
    print(f'Duck Puzzle {i + 1}:')
    display_duck_puzzle(duck_puzzle.initial)
    print(duck_puzzle.initial)
    print()
    solve_puzzle(duck_puzzle, 'misplaced_tiles')
    solve_puzzle(duck_puzzle, 'manhattan_distance')
    solve_puzzle(duck_puzzle, 'mix_heuristic')
