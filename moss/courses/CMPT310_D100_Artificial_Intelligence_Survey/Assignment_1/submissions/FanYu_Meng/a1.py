from aima_python.search import *
import random
import time as timer
import math
import csv

# ______________________________________________________________________________
#EightPuzzle copied and modified from search.py

class EightPuzzle1(Problem):
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

    def calc_manhattan(self, node):
        manhattan = 0
        state = node.state

        board = {
            1: [0, 0], 2: [1, 0], 3: [2, 0],
            4: [0, 1], 5: [1, 1], 6: [2, 1],
            7: [0, 2], 8: [1, 2], 0: [2, 2]
        }
        curr = 0
        for i in state:
            if i == 0:
                curr += 1
            else:
                if curr == 8:
                    curr_loc = board[0]
                else:
                    curr_loc = board[curr+1]
                goal = board[i]
                dx = abs(curr_loc[0] - goal[0])
                dy = abs(curr_loc[1] - goal[1])
                manhattan += dx + dy
                curr += 1
        return manhattan

    def get_max_h(self,node):
        misplaced = self.h(node)
        manhattan = self.calc_manhattan(node)

        return max(misplaced, manhattan)

# ______________________________________________________________________________

# ______________________________________________________________________________
"""
DuckPuzzle modified from EightPuzzle
+--+--+
|  |  |
+--+--+--+--+
|  |  |  |  |
+--+--+--+--+
   |  |  |  |
   +--+--+--+

 1 2
 3 4 5 6   goal state
   7 8 *
"""

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

        index_blank_square = self.find_blank_square(state)

        moves = {
            0:['DOWN', 'RIGHT'], 1:['DOWN', 'LEFT'],
            2:['UP', 'RIGHT'], 3:['UP', 'DOWN', 'LEFT', 'RIGHT'], 4:['DOWN', 'LEFT', 'RIGHT'], 5:['DOWN', 'LEFT'],
                               6:['UP', 'RIGHT'], 7:['UP', 'LEFT', 'RIGHT'], 8:['UP', 'LEFT']
        }

        return moves[index_blank_square]

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        if blank in (0,1,2,3):
            #print(blank)
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        #print(f'action {delta[action]}')
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

    def calc_manhattan(self, node):
        manhattan = 0
        state = node.state

        board = {
            1: [0, 0], 2: [1, 0],
            3: [0, 1], 4: [1, 1], 5: [2, 1], 6: [3, 1],
                       7: [1, 2], 8: [2, 2], 0: [3, 2]
        }
        curr = 0
        for i in state:
            if i == 0:
                curr += 1
            else:
                if curr == 8:
                    curr_loc = board[0]
                else:
                    curr_loc = board[curr+1]
                goal = board[i]
                dx = abs(curr_loc[0] - goal[0])
                dy = abs(curr_loc[1] - goal[1])
                manhattan += dx + dy
                curr += 1
        return manhattan

    def get_max_h(self,node):
        misplaced = self.h(node)
        manhattan = self.calc_manhattan(node)

        return max(misplaced, manhattan)

# ______________________________________________________________________________



def best_first_graph_search1(problem, f, display=False):
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
    node_count = 0
    while frontier:
        node = frontier.pop()
        node_count += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, node_count]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def astar_search1(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""

    h = memoize(h or problem.h, 'h')
    return best_first_graph_search1(problem, lambda n: n.path_cost + h(n), display)


def make_rand_8puzzle():
    puzzle = EightPuzzle1(Problem)
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    for i in range(0,100):
        possible_actions = puzzle.actions(state)
        state = puzzle.result(state, possible_actions[random.randrange(len(possible_actions))])
    return EightPuzzle1(state)

def make_rand_dpuzzle():
    puzzle = DuckPuzzle(Problem)
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    for i in range(0,100):
        possible_actions = puzzle.actions(state)
        state = puzzle.result(state, possible_actions[random.randrange(len(possible_actions))])
    return DuckPuzzle(state)

def display(state):
    new = str(state).replace('0','"*"')
    new = eval(new)
    print(f'{new[0]} {new[1]} {new[2]}')
    print(f'{new[3]} {new[4]} {new[5]}')
    print(f'{new[6]} {new[7]} {new[8]}')

def display_duck(state):
    new = str(state).replace('0','"*"')
    new = eval(new)
    print(f'{new[0]} {new[1]}')
    print(f'{new[2]} {new[3]} {new[4]} {new[5]}')
    print(f'  {new[6]} {new[7]} {new[8]}')
"""
# Eight Puzzle
with open('a1.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Eight Puzzle method', 'time', 'cost', 'total nodes'])
for i in range(10):
    eightpuzz = make_rand_8puzzle()
    display(eightpuzz.initial)

    start_t = timer.time()
    misplaced_result = astar_search1(eightpuzz)
    end_t = timer.time()
    misplaced_time = end_t - start_t
    misplaced_cost = misplaced_result[0].path_cost
    misplaced_nodes = misplaced_result[1]
    print('CPU time for mispalced herustics:                          {:.2f}'.format(misplaced_time))
    print(f'Path length for misplaced herustics:                       {misplaced_cost}')
    print(f'Total nodes removed from frontier for misplaced herustics: {misplaced_nodes}')

    start_t = timer.time()
    manhattan_result = astar_search1(eightpuzz, eightpuzz.calc_manhattan)
    end_t = timer.time()
    manhattan_time = end_t - start_t
    manhattan_cost = manhattan_result[0].path_cost
    manhattan_node = manhattan_result[1]
    print('CPU time for manhattan herustics:                          {:.2f}'.format(manhattan_time))
    print(f'Path length for manhattan herustics:                       {manhattan_cost}')
    print(f'Total nodes removed from frontier for manhattan herustics: {manhattan_node}')

    start_t = timer.time()
    max_result = astar_search1(eightpuzz, eightpuzz.get_max_h)
    end_t = timer.time()
    max_time = end_t - start_t
    max_cost = max_result[0].path_cost
    max_node = max_result[1]
    print('CPU time for max herustics:                          {:.2f}'.format(max_time))
    print(f'Path length for max herustics:                       {max_cost}')
    print(f'Total nodes removed from frontier for max herustics: {max_node}')

    with open('a1.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerows(
            [['misplaced', misplaced_time, misplaced_cost, misplaced_nodes],
            ['manhattan', manhattan_time, manhattan_cost, manhattan_node],
            ['max', max_time, max_cost, max_node],
            [eightpuzz.initial,'-------','-------','-------']]
        )
"""
# Duck Puzzle

with open('a1.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Duck Puzzle method', 'time', 'cost', 'total nodes'])

for i in range(10):
    dpuzzle = make_rand_dpuzzle()
    #dpuzzle = DuckPuzzle((2,3,1,0,4,7,5,8,6))
    display_duck(dpuzzle.initial)
    start_t = timer.time()
    misplaced_result = astar_search1(dpuzzle)
    end_t = timer.time()
    misplaced_time = end_t - start_t
    misplaced_cost = misplaced_result[0].path_cost
    misplaced_nodes = misplaced_result[1]
    print('CPU time for mispalced herustics:                          {:.2f}'.format(misplaced_time))
    print(f'Path length for misplaced herustics:                       {misplaced_cost}')
    print(f'Total nodes removed from frontier for misplaced herustics: {misplaced_nodes}')

    start_t = timer.time()
    manhattan_result = astar_search1(dpuzzle, dpuzzle.calc_manhattan)
    end_t = timer.time()
    manhattan_time = end_t - start_t
    manhattan_cost = manhattan_result[0].path_cost
    manhattan_node = manhattan_result[1]
    print('CPU time for manhattan herustics:                          {:.2f}'.format(manhattan_time))
    print(f'Path length for manhattan herustics:                       {manhattan_cost}')
    print(f'Total nodes removed from frontier for manhattan herustics: {manhattan_node}')

    start_t = timer.time()
    max_result = astar_search1(dpuzzle, dpuzzle.get_max_h)
    end_t = timer.time()
    max_time = end_t - start_t
    max_cost = max_result[0].path_cost
    max_node = max_result[1]
    print('CPU time for max herustics:                          {:.2f}'.format(max_time))
    print(f'Path length for max herustics:                       {max_cost}')
    print(f'Total nodes removed from frontier for max herustics: {max_node}')

    with open('a1.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerows(
            [['misplaced', misplaced_time, misplaced_cost, misplaced_nodes],
            ['manhattan', manhattan_time, manhattan_cost, manhattan_node],
            ['max', max_time, max_cost, max_node],
            [dpuzzle.initial,'-------','-------','-------']]
        )
