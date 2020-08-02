import numpy as np
import time
import random

from search import *

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

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))
    
    def h_manhattan(self, node):
        sum = 0
        for (i, piece) in zip(node.state, self.goal):
            x1 = int(i/3)
            y1 = i%3
            x2 = int(piece/3)
            y2 = piece%3
            sum += abs(x2 - x1) + abs(y2 - y1)

        return int(sum)
    
    def h_max(self, node):
        h_def = self.h(node) # Default heuristic function
        h_man = self.h_manhattan(node)
        return max(h_def, h_man)

def astar_search_copy(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_copy(problem, lambda n: n.path_cost + h(n), display)

def astar_search_manhattan(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h_manhattan, 'h')
    return best_first_graph_search_copy(problem, lambda n: n.path_cost + h(n), display)

def astar_search_max(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h_max, 'h')
    return best_first_graph_search_copy(problem, lambda n: n.path_cost + h(n), display)

def best_first_graph_search_copy(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    
    nodes_removed = 0 # number of nodes removed from the frontier
    
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        nodes_removed += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, nodes_removed
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def make_rand_8puzzle():
    running = True
    while(running):
        state = tuple(np.random.permutation(9))
        puzzle = EightPuzzle(initial = state)
        if puzzle.check_solvability(state) == True:
            running = False
            return puzzle

def display(state):
    for i, piece in enumerate(state, 1):
        if piece == 0:
            print("*", end= ' ' if i % 3 else "\n")
        else:
            print(piece, end= ' ' if i % 3 else "\n")

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

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if (index_blank_square < 2) or ((3 < index_blank_square) and index_blank_square < 6) :
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square  == 2 or index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        if blank < 2:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        if blank > 5:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank > 1 and blank < 6:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            
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
    
    def h_manhattan(self, node):
        sum = 0
        for (i, piece) in zip(node.state, self.goal):
            x1 = int(i/3)
            y1 = i%3
            x2 = int(piece/3)
            y2 = piece%3
            sum += abs(x2 - x1) + abs(y2 - y1)

        return int(sum)
    
    def h_max(self, node):
        h_def = self.h(node) # Default heuristic function
        h_man = self.h_manhattan(node)
        return max(h_def, h_man)

def make_rand_duck_puzzle():
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = DuckPuzzle(initial = state)
    new_state = state
    for i in range(100):
        action_list = puzzle.actions(new_state)
        action = random.choice(action_list)
        new_state = puzzle.result(new_state, action)
        
    puzzle.initial = new_state
    return puzzle
	
def display_duck(state):
    for i, piece in enumerate(state, 1):
        if i == 2:
            if piece == 0:
                print("*", end= "\n")
            else:
                print(piece, end= "\n")
        if i == 6:
            if piece == 0:
                print("*", end= "\n  ")
            else:
                print(piece, end= "\n  ")
        if i != 2 and i != 6:
            if piece == 0:
                print("*", end= ' ')
            else:
                print(piece, end= ' ')

# ----------Testing Puzzles----------

print("Statistics for 8 puzzle problem:\n")

for i in range(10):
        puzzle = make_rand_8puzzle()
    
        start_time = time.time()
        solution = astar_search_copy(puzzle)
        elapsed_time = time.time() - start_time
    
        print("-----Default heuristic-----\n")
        print("Total running time (in seconds): ", elapsed_time)
        print("Length of solution: ", len(solution[0].path())) 
        print("Number of nodes removed from frontier: ", solution[1])
        print("\n")
        
        start_time = time.time()
        solution = astar_search_manhattan(puzzle)
        elapsed_time = time.time() - start_time
        
        print("-----Manhattan heuristic-----\n")
        print("Total running time (in seconds): ", elapsed_time)
        print("Length of solution: ", len(solution[0].path())) 
        print("Number of nodes removed from frontier: ", solution[1])
        print("\n")
        
        start_time = time.time()
        solution = astar_search_max(puzzle)
        elapsed_time = time.time() - start_time
        
        print("-----Max heuristic-----\n")
        print("Total running time (in seconds): ", elapsed_time)
        print("Length of solution: ", len(solution[0].path())) 
        print("Number of nodes removed from frontier: ", solution[1])
        print("\n")

print("Statistics for duck puzzle problem:\n")

for i in range(10):
        puzzle = make_rand_duck_puzzle()
    
        start_time = time.time()
        solution = astar_search_copy(puzzle)
        elapsed_time = time.time() - start_time
    
        print("-----Default heuristic-----\n")
        print("Total running time (in seconds): ", elapsed_time)
        print("Length of solution: ", len(solution[0].path())) 
        print("Number of nodes removed from frontier: ", solution[1])
        print("\n")
                
        start_time = time.time()
        solution = astar_search_manhattan(puzzle)
        elapsed_time = time.time() - start_time
        
        print("-----Manhattan heuristic-----\n")
        print("Total running time (in seconds): ", elapsed_time)
        print("Length of solution: ", len(solution[0].path())) 
        print("Number of nodes removed from frontier: ", solution[1])
        print("\n")
        
        start_time = time.time()
        solution = astar_search_max(puzzle)
        elapsed_time = time.time() - start_time
        
        print("-----Max heuristic-----\n")
        print("Total running time (in seconds): ", elapsed_time)
        print("Length of solution: ", len(solution[0].path())) 
        print("Number of nodes removed from frontier: ", solution[1])
        print("\n")



