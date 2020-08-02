import sys
from collections import deque
from utils import *
import numpy as np
import time
from search import Problem, Node

# CMPT310-assignment 1
# name: Ruilin Zhang
# student number: 301250939

def make_rand_8puzzle():
    "a new instance of the eight puzzle"
    state = tuple(np.random.permutation(9))
    new_EightPuzzle=EightPuzzle(initial=state) 
    "using solvability function from eightpuzzle in search"
    if new_EightPuzzle.check_solvability(state):
         "solvable eight puzzle"
         return new_EightPuzzle
    else: 
        "not solvable, make a new eight puzzle until solvable"
        return make_rand_8puzzle() 

def make_rand_duckpuzzle():
    "a new instance of the duckpuzzle"
    state = tuple(np.random.permutation(9))
    new_DuckPuzzle=DuckPuzzle(initial=state) 
    "using solvability function from duckpuzzle in search"
    if new_DuckPuzzle.check_solvability(state):
         return new_DuckPuzzle
    else: 
        "not solvable, make a new duckpuzzle until solvable"
        return make_rand_duckpuzzle()

def display(state):
    new_state=list(state)
    for i in range(len(new_state)):
        if new_state[i] == 0:
            new_state[i]="*"

    print(new_state[0],new_state[1],new_state[2])
    print(new_state[3],new_state[4],new_state[5])
    print(new_state[6],new_state[7],new_state[8])

def Manhattan(node):
    #first part of the textbook example code 
    state = node.state
    #index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    # index_state = {}
    # index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    # for i in range(len(state)):
    #     index_state[state[i]] = index[i]
    manDict = 0
    k=0
    for i in range(3):
         for j in range(3):
                value = state[k] #get value from index 0-8
                if(value != 0): #avoid checking blank space (0)
                 X = (value-1)/3 #expected x axis
                 Y = (value-1)%3 #expected y axis
                 x1 = i-X #x distance from current to expected
                 y1 = j-Y #y distance from current to expected
                 k+=1
                 manDict = manDict + abs(x1)+ abs(y1)
    return manDict

def linear(node): #textbook sample code for getting h value of Misplaced Tiles
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    return sum([1 if node.state[i] != goal[i] else 0 for i in range(8)])


def max_heuristic(node): #textbook sample code for checking max value 
    score1 = Manhattan(node)
    score2 = linear(node)
    return max(score1, score2)


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def astar_search_m(problem, h=Manhattan,display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def astar_search_max(problem, h=max_heuristic, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def best_first_graph_search(problem, f, display=False): 
    # modified version shows the length (i.e. number of tiles moved) of the solution 
    # and the total number of nodes that were removed from frontier
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
        if node.depth > 30:
             if problem == make_rand_duckpuzzle():
                 print("30 tiles have been moved, puzzle seems to be unsolvable")
                 return None #terminates search when 20 actions are reached for duck puzzle
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "nodes have been removed from frontier and", len(frontier), "paths remain in the frontier")
                print((node.depth), "is the length (i.e. number of tiles moved) of the solution")
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
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))



class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 2x3 + 2x2 board, where one of the
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

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')

        if index_blank_square == 1:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')

        if index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        
        if index_blank_square == 4:
            possible_actions.remove('UP')

        if index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
    
        if index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')

        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        
        if index_blank_square == 8:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank == 0:
            
            delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        if blank == 1:
            
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        if blank == 2:
            
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        if blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        if blank > 3:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        #avoids check for solvability, and assumes solvable. If not solvable terminates search after 30 depths
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion >= 1 
        

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))



for i in range(10):

        #create 8 puzzle

        eight = make_rand_8puzzle()
        display(eight.initial)

        start_time1 = time.time()

        a1 = astar_search(eight, display=True)

        elapsed_time1 = time.time() - start_time1

        print(f'elapsed time for solving 8 puzzle using the misplaced tile heuristic (in seconds): {elapsed_time1}s')

                
        start_time2 = time.time()

        a2 = astar_search_m(eight, display=True)

        elapsed_time2 = time.time() - start_time2

        print(f'elapsed time for solving 8 puzzle using the Manhattan heuristic (in seconds): {elapsed_time2}s')

                
        start_time3 = time.time()

        a3= astar_search_max(eight, display=True)

        elapsed_time3 = time.time() - start_time3

        print(f'elapsed time for solving 8 puzzle using the max of the misplaced tile heuristic and the Manhattan heuristic (in seconds): {elapsed_time3}s')

        #create duck puzzle

        duck=make_rand_duckpuzzle() 
        display(duck.initial)

        start_time4 = time.time()

        d1= astar_search(duck, display=True)

        elapsed_time4 = time.time() - start_time4

        print(f'elapsed time for solve duck puzzle using the misplaced tile heuristic (in seconds): {elapsed_time4}s')
       
        start_time5 = time.time()

        d2= astar_search_m(duck, display=True)

        elapsed_time5 = time.time() - start_time5

        print(f'elapsed time for solve duck puzzle using the Manhattan heuristic (in seconds): {elapsed_time5}s')

        start_time6 = time.time()

        d3= astar_search_max(duck, display=True)

        elapsed_time6 = time.time() - start_time6

        print(f'elapsed time for solving duck puzzle using the max of the misplaced tile heuristic and the Manhattan heuristic (in seconds): {elapsed_time6}s')


        
    


        
