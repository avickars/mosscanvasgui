# a1.py
# Name: Taorui(Mac) Liu
# Student number: 301237339

from search import *
from random import *
import time


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
    nodepop = 0
    while frontier:
        node = frontier.pop()
        nodepop = nodepop + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print("total number of nodes that were removed from frontier: " + str(nodepop))
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

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
        h(n) = number of misplaced tiles removed 0 to achieve optimal solution"""
        h = 0
        for i in range(9):
            if(node.state[i] != self.goal[i]):
                if node.state[i] != 0:
                    h = h + 1

        return h
    
    def manhattan(self,node):
        """ Calculating manhanttan value using nested if statements will return dx + dy for all tiles """
        dx = 0
        dy = 0
        for i in range(9):
            if node.state[i] == 1 or node.state[i] == 4 or node.state[i] == 7:
                dx = dx + i % 3
            if node.state[i] == 2 or node.state[i] == 5 or node.state[i] == 8:
                if i == 0 or i == 3 or i == 6 or i == 2 or i == 5 or i ==8:
                    dx = dx + 1
            if node.state[i] == 3 or node.state[i] == 6:
                if i == 0 or i == 3 or i == 6:
                    dx = dx + 2
                if i== 1 or i == 4 or i ==7:
                    dx = dx + 1
        

            if node.state[i] == 1 or node.state[i] == 2 or node.state[i] == 3:
                if i == 3 or i == 4 or i == 5:
                    dy = dy + 1
                if i == 6 or i == 7 or i == 8:
                    dy = dy +2
            if node.state[i] == 4 or node.state[i] == 5 or node.state[i] == 6:
                if i == 0 or i == 1 or i == 2 or i == 6 or i == 7 or i ==8:
                    dy = dy + 1
            if node.state[i] == 7 or node.state[i] == 8:
                if i == 0 or i == 1 or i == 2:
                    dy = dy + 2
                if i== 3 or i == 4 or i ==5:
                    dy = dy + 1

        return dx + dy

    def max_h(self,node):
        hvalue = self.h(node)
        manhattanvalue = self.manhattan(node)

        return max(hvalue,manhattanvalue)

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

        if index_blank_square  == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta = 0
        if blank == 0 or blank == 1:
            if action == 'DOWN':
                delta = 2
        if blank == 0 or blank == 2 or blank == 3 or blank == 4 or blank == 6 or blank == 7:
            if action == 'RIGHT':
                delta = 1
        if blank == 1 or blank == 3 or blank == 4 or blank == 5 or blank == 7 or blank == 8:
            if action == 'LEFT':
                delta = -1
        if blank == 2 or blank == 3:
            if action == 'UP':
                delta = -2
        if blank == 6 or blank == 7 or blank == 8:
            if action == 'UP':
                delta = -3
        if blank == 3 or blank == 4 or blank == 5:
            if action == 'DOWN':
                delta = +3
        
        neighbor = blank + delta
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
        h(n) = number of misplaced tiles removed 0 to achieve optimal solution"""

        h = 0
        for i in range(9):
            if(node.state[i] != self.goal[i]):
                if node.state[i] != 0:
                    h = h + 1

        return h
    
    def manhattan(self,node):
        """ Calculating manhanttan value using nested if statements will return dx + dy for all tiles """
        dx = 0
        dy = 0
        for i in range(9):
            if node.state[i] == 1 or node.state[i] == 3:
                if i == 1 or i == 3 or i == 6:
                    dx = dx + 1
                if i == 4 or i == 7:
                    dx = dx + 2
                if i == 5 or i == 8:
                    dx = dx + 3
            if node.state[i] == 2 or node.state[i] == 4 or node.state[i] == 7:
                if i == 0 or i == 2 or i == 4 or i == 7:
                    dx = dx + 1
                if i == 5 or i == 8:
                    dx = dx + 2
            if node.state[i] == 5 or node.state[i] == 8:
                if i == 0 or i == 2:
                    dx = dx + 2
                if i== 1 or i == 3 or i == 6 or i == 5 or i == 8:
                    dx = dx + 1
            if node.state[i] == 6:
                if i == 4 or i == 7:
                    dx = dx + 1
                if i== 1 or i == 3 or i == 6:
                    dx = dx + 2
                if i== 0 or i == 2:
                    dx = dx + 3
        

            if node.state[i] == 1 or node.state[i] == 2:
                if i == 2 or i == 3 or i == 4 or i == 5:
                    dy = dy + 1
                if i == 6 or i == 7 or i == 8:
                    dy = dy +2
            if node.state[i] == 3 or node.state[i] == 4 or node.state[i] == 5 or node.state[i] == 6:
                if i == 0 or i == 1 or i == 6 or i == 7 or i ==8:
                    dy = dy + 1
            if node.state[i] == 7 or node.state[i] == 8:
                if i == 0 or i == 1:
                    dy = dy + 2
                if i== 3 or i == 4 or i ==5 or i == 6:
                    dy = dy + 1

        return dx + dy

    def max_h(self,node):
        hvalue = self.h(node)
        manhattanvalue = self.manhattan(node)

        return max(hvalue,manhattanvalue)


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def astar_search_Manhattan(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.manhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def astar_search_MaxH(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.max_h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def display(state):
    """Display 8 Puzzle parameter tuple"""
    for i in range(len(state)):
        if i == 2 or i == 5 or i == 8:
            print("*" if state[i] == 0 else state[i], end= "\n")
        else:
            print("*" if state[i] == 0 else state[i], end= " ")

def display_duckpuzzle(state):
    """Display Duck Puzzle parameter tuple"""
    for i in range(len(state)):
        if i == 1 or i == 5 or i == 8:
            print("*" if state[i] == 0 else state[i], end= "\n")
        elif i == 6:
            print("  *" if state[i] == 0 else "  " + str(state[i]), end = " ")
        else:
            print("*" if state[i] == 0 else state[i], end= " ")

def make_rand_8puzzle():
    """Start from goal state then choose a random move number 0 to 1000 and taking random action from action function"""
    state = (1,2,3,4,5,6,7,8,0)
    index = 8
    randomnumber = randint(0,1000)
    for x in range(randomnumber):
        actionlength = len(EightPuzzle(Problem).actions(state))
        randaction = EightPuzzle(Problem).actions(state)[randint(0,actionlength-1)]
        state = EightPuzzle(Problem).result(state,randaction)
    return EightPuzzle(state)

def make_rand_duckpuzzle():
    """Start from goal state then choose a random move number 0 to 1000 and taking random action from action function"""
    state = (1,2,3,4,5,6,7,8,0)
    index = 8
    randomnumber = randint(0,1000)
    for x in range(randomnumber):
        actionlength = len(DuckPuzzle(Problem).actions(state))
        randaction = DuckPuzzle(Problem).actions(state)[randint(0,actionlength-1)]
        state = DuckPuzzle(Problem).result(state,randaction)
    return DuckPuzzle(state)

def test_astar_time():
    print("8 Puzzle:")
    for x in range(10):
        puzzle8 = make_rand_8puzzle()
        print("number: " + str(x+1))
        start_time = time.time()
        display(puzzle8.initial)
        print("H")
        result = astar_search(puzzle8)
        elapsed_time = time.time() - start_time
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print("length of the solution: " + str(result.path_cost))
        start_time = time.time()
        print("Manhattan")
        result = astar_search_Manhattan(puzzle8)
        elapsed_time = time.time() - start_time
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print("length of the solution: " + str(result.path_cost))
        start_time = time.time()
        print("maxH")
        result = astar_search_MaxH(puzzle8)
        elapsed_time = time.time() - start_time
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print("length of the solution: " + str(result.path_cost))

def test_astar_time_duckpuzzle():
    print("Duck Puzzle:")
    for x in range(10):
        print("number: " + str(x+1))
        puzzleduck =  make_rand_duckpuzzle()
        start_time = time.time()
        display_duckpuzzle(puzzleduck.initial)
        print("H")
        result = astar_search(puzzleduck)
        elapsed_time = time.time() - start_time
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print("length of the solution: " + str(result.path_cost))
        start_time = time.time()
        print("Manhattan")
        result = astar_search_Manhattan(puzzleduck)
        elapsed_time = time.time() - start_time
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print("length of the solution: " + str(result.path_cost))
        start_time = time.time()
        print("maxH")
        result = astar_search_MaxH(puzzleduck)
        elapsed_time = time.time() - start_time
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print("length of the solution: " + str(result.path_cost),end="\n")


test_astar_time_duckpuzzle()
test_astar_time()

