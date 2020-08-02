#!/usr/bin/env python
# coding: utf-8

# In[83]:


from search import*
import numpy as np
import math
import time

length = 0
n = 0
        
"""Q1"""
def make_rand_8puzzle():
 
    arr = (0,1,2,3,4,5,6,7,8)
    #state= np.random.permutation(9) 
    #eightPuzzle = EightPuzzle(state)
    l = list(arr)
    random.shuffle(l)
    arr = tuple(l)
    eightPuzzle = EightPuzzle(arr)
    
    while(eightPuzzle.check_solvability(arr) != True):
        l = list(arr)
        random.shuffle(l)
        arr = tuple(l)
        eightPuzzle = EightPuzzle(arr)
    
    #display(arr)
 
    return eightPuzzle
    

def display(state):
    j = 0
    for i in range(len(state)):
        if j == 3 or j == 6:
            sys.stdout.write("\n")
        if state[i] == 0:
            sys.stdout.write("*")
        else:
            sys.stdout.write ("%s" % state[i])
        j = j+1
    return None
      """"'''''''''''''''''''''''''''''''''''''''''''''''"""

def my_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)







def calculateManhattan(node):
    count = 0
    current_state = node.state
    
    if current_state[0] is not 1:
        if current_state[1] == 1 or current_state[3] == 1:
            count += 1
        elif current_state[2] == 1 or current_state[4] == 1 or current_state[6] == 1:
            count += 2
        elif current_state[5] == 1 or current_state[7] == 1:
            count += 3
        elif current_state[8] == 1:
            count += 4
            
    if current_state[1] is not 2:
        if current_state[0] == 2 or current_state[2] == 2 or current_state[4] == 2:
            count += 1
        elif current_state[3] == 2 or current_state[5] == 2 or current_state[7] == 2:
            count += 2
        elif current_state[6] == 2 or current_state[8] == 2:
            count += 3
                
    if current_state[2] is not 3:
        if current_state[1] == 3 or current_state[5] == 3:
            count += 1
        elif current_state[0] == 3 or current_state[4] == 3 or current_state[8] == 3:
            count += 2
        elif current_state[3] == 3 or current_state[7] == 3:
            count += 3
        elif current_state[6] == 3:
            count += 4
            
    if current_state[3] is not 4:
        if current_state[0] == 4 or current_state[4] == 4 or current_state[6] == 4:
            count += 1
        elif current_state[1] == 4 or current_state[5] == 4 or current_state[7] == 4:
            count += 2
        elif current_state[2] == 4 or current_state[8] == 4:
            count += 3
      
    if current_state[4] is not 5:
        if current_state[1] == 5 or current_state[3] == 5 or current_state[5] == 5 or current_state[7]:
            count += 1
        elif current_state[0] == 5 or current_state[2] == 5 or current_state[6] == 5 or current_state[8] == 5:
            count += 2
            
    if current_state[5] is not 6:
        if current_state[2] == 6 or current_state[4] == 6 or current_state[8] == 6:
            count += 1
        elif current_state[1] == 6 or current_state[7] == 6 or current_state[3] == 6:
            count += 2
        elif current_state[0] == 6 or current_state[6] == 6:
            count += 3
            
    if current_state[6] is not 7:
        if current_state[3] == 7 or current_state[7] == 7:
            count += 1
        elif current_state[0] == 7 or current_state[8] == 7 or current_state[4] == 7:
            count += 2
        elif current_state[1] == 7 or current_state[5] == 7:
            count += 3
        elif current_state[2] == 7:
            count += 4
            
    if current_state[7] is not 8:
        if current_state[4] == 8 or current_state[6] == 8 or current_state[8] == 8:
            count += 1
        elif current_state[3] == 8 or current_state[5] == 8 or current_state[1] == 8:
            count += 2
        elif current_state[0] == 8 or current_state[2] == 8:
            count += 3
       
    return count
            

def my_best_first_graph_search(problem, f, display=False):
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
        global n 
        n += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
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


def my_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return my_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):                                                                                                                                                                            tial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
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

        if index_blank_square != 1 and index_blank_square // 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or (index_blank_square > 3 and index_blank_square < 6):
            possible_actions.remove('UP')
        if index_blank_square > 2 and (index_blank_square + 1) % 3 == 0:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        if blank > 3:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
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
    
    
    
def display_duck(state):
    j = 0
    for i in range(len(state)):
        if j == 2:
            sys.stdout.write("\n")
        elif j == 6:
            sys.stdout.write("\n ")
        if state[i] == 0:
            sys.stdout.write("*")
        else:
            sys.stdout.write ("%s" % state[i])
        j = j+1
            


# In[84]:


def max_fun(node):
    num1 = calculateManhattan(node)
    num2 = my_linear(node)
    return max(score1, score2)

""""https://github.com/aimacode/aima-python/blob/master/search.ipynb"""
def my_linear(node):
    goal = (1,2,3,4,5,6,7,8,0)
    return sum([1 if node.state[i] != goal[i] else 0 for i in range(8)])


myDuck_Puzzle = DuckPuzzle((1,2,3,5,6,0,7,8,4))

start_time = time.time()

astar_search(myDuck_Puzzle).solution()

elapsed_time = time.time() - start_time

print(elapsed_time)


# In[ ]:




