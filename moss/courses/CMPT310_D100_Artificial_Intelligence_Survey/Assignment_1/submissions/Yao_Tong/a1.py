from search import *
import numpy as np
import time

'''
****************************   what I changed in search.py     *********************************

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
    counter = 0
    
    while frontier:
        node = frontier.pop()
        counter += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, counter
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

'''

class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square in [0, 2, 6]:
            possible_actions.remove('LEFT')
        if index_blank_square in [0, 1, 4, 5]:
            possible_actions.remove('UP')
        if index_blank_square in [1, 5, 8]:
            possible_actions.remove('RIGHT')
        if index_blank_square in [2, 6, 7, 8]:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank in [2, 3]:
            delta['UP'] = -2
        if blank in [0, 1]:
            delta['DOWN'] = 2

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """
        for i in [0, 1, 2]:
            if state[i] not in [1, 2, 3]:
                return 0
        
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

def make_rand_8puzzle():
    state = tuple(np.random.permutation(9))
    puzzle = EightPuzzle(initial=state)
    if puzzle.check_solvability(state) != 0:
        return state
    else:
        return make_rand_8puzzle()

def make_rand_duckpuzzle():
    state = tuple(np.random.permutation(9))
    puzzle = DuckPuzzle(initial=state)
    if puzzle.check_solvability(state) != 0:
        return state
    else:
        return make_rand_duckpuzzle()

def display(state):
    for i in range(9):
        if state[i] != 0:
            if i % 3 == 2:
                print(state[i], end="\n")
            else:
                print(state[i], end=" ")
        else:
            if i % 3 == 2:
                print("*", end="\n")
            else:
                print("*", end=" ")

def tup2list(state):
    tup = [None] * 12
    j = 0
    for i in range(12):
        if i not in [2, 3, 8]:
            tup[i] = state[j]
            j += 1
        else:
            pass
    return tuple(tup)

def display_duck(state):
    tup = tup2list(state)
    i = 0
    for x in range(3):
        for y in range(4):
            if tup[i] != 0 and tup[i] != None:
                print(tup[i], end=" ")
                i += 1
            elif tup[i] == None:
                print(" ", end= " ")
                i += 1
            else:
                print("*", end=" ")
                i += 1
        print("\n")



def man_h(node):
    x, y, i, h = 0, 0, 0, 0
    for x in range(3):
        for y in range(3):
            if node.state[i] != 0:
                h += abs(int((node.state[i]-1)/3) - x) + abs(int((node.state[i]-1)%3) - y)
                i += 1
            else:
                h += abs(2-x) + abs(2-y)
                i += 1
    return h

def max_h(node):
    manh = man_h(node)
    puzzle = EightPuzzle(initial=node.state)
    defh = puzzle.h(node)
    if manh >= defh:
        return manh
    else:
        return defh

def misplaced(puzzle):
    start_time = time.time()
    node, counter = astar_search(puzzle, h=puzzle.h)
    elapsed_time = time.time() - start_time
    print("************ misplaced ***************")
    print("the length of the solution: ", node.path_cost)
    print("Nodes removed from frontier: ", counter)
    print(f'elapsed time (in seconds): {elapsed_time}s')

def manhantan(puzzle):
    start_time = time.time()
    node, counter = astar_search(puzzle, h=man_h)
    elapsed_time = time.time() - start_time
    print("************ manhantan ***************")
    print("the length of the solution: ", node.path_cost)
    print("Nodes removed from frontier: ", counter)
    print(f'elapsed time (in seconds): {elapsed_time}s')

def maxh(puzzle):
    start_time = time.time()
    node, counter = astar_search(puzzle, h=max_h)
    elapsed_time = time.time() - start_time
    print("*************** max *****************")
    print("the length of the solution: ", node.path_cost)
    print("Nodes removed from frontier: ", counter)
    print(f'elapsed time (in seconds): {elapsed_time}s')


def main_puzzle():
   for i in range(10):
        state = make_rand_8puzzle()
        display(state)
        puzzle = EightPuzzle(initial=state)
        misplaced(puzzle)
        manhantan(puzzle)
        maxh(puzzle)

def main_duck():
    for i in range(10):
        state = make_rand_duckpuzzle()
        display_duck(state)
        puzzle = DuckPuzzle(initial=state)
        misplaced(puzzle)
        manhantan(puzzle)
        maxh(puzzle)
