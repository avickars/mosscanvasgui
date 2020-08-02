from search import Problem, Node
import sys
from collections import deque
from utils import *
'''
imports Problem and Node Class from search library and libraries that are needed in search (for memoize and so on)
All this program needs is aima-python clone
'''

import random
import time




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

        return sum(s != g and s!=0 for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        state = node.state      
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

        for i in range(len(state)):
            index_state[state[i]] = index[i] 
        dx = 0
        dy = 0

        for i in range(1, len(state)):
                dx += abs(index_state[i][0] - index_goal[i][0])
                dy += abs(index_state[i][1] - index_goal[i][1])   
        return (dx+dy)

    #http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html

    def MaxH(self, node):
            return max(self.h(node), self.manhattan(node))

#----start Q1----
def make_rand_8puzzle():    
    '''
     it uses random library and creates a list that is comprised of number 0-8. 
     It checks whether it is solvable and if it is not solvable, 
     it shuffles the order in the list and check solvability again until it passes the solvability test. 
     Changes List to tuple at the end

     '''
    initial = list(range(0, 9))
    random.shuffle(initial)
    initial_tuple = tuple(initial)
    puzzle = EightPuzzle(initial_tuple)
    while puzzle.check_solvability(initial_tuple) == False:
        random.shuffle(initial)
        initial_tuple = tuple(initial)

    return initial_tuple
 
def display(state):
    llist = list(state)
    llist[llist.index(0)] = "*"
    state = tuple(llist)
    for x in range((len(state)//3)):
        print("{} {} {}".format(state[x*3], state[x*3+1], state[x*3+2]))
    return None

def best_first_graph_search(problem, f, display = False):
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
    popcounter = 0
    while frontier:
        node = frontier.pop()
        popcounter=popcounter+1 
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")

            return [node, node.path_cost, popcounter]   
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    
    return None
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def astar_searchMH(problem, h=None, display=False):
    
    h = memoize(h or problem.manhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
def astar_searchMaxH(problem, h=None, display = False):
    
    h = memoize(h or problem.MaxH, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

#https://brilliant.org/wiki/a-star-search/
#https://blog.goodaudience.com/solving-8-puzzle-using-a-algorithm-7b509c331288



#----start Q3

class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)
    def find_blank_square(self, state):
        return state.index(0)
    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
        if index_blank_square in (0, 2, 6):
            possible_actions.remove('LEFT')
        if index_blank_square in (1, 5,8):
            possible_actions.remove('RIGHT')
        if index_blank_square in (0, 1, 4, 5):
            possible_actions.remove('UP')
        if index_blank_square in (2, 6, 7, 8):
            possible_actions.remove('DOWN')
        return possible_actions
    def result(self, state, action):
        '''
        Same result() to that of 8Puzzles, except for the delta values. 
        The delta values are changed to correspond to the Duckpuzzle patterns.
        '''
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta1 = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        delta2 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        delta3 = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank in (0, 1, 2):
            neighbor = blank + delta1[action]    
        elif blank == 3:
            neighbor = blank + delta2[action]
        else:
            neighbor = blank + delta3[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable
                """ 
        return astar_search(DuckPuzzle(state)) != None


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g and s!= 0 for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        state = node.state
        index_goal={0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
        index_state = {}
        index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2],  [2, 3]]
        for i in range(len(state)):
            index_state[state[i]] = index[i]

        dx = 0
        dy = 0
        for i in range(1, len(state)):
            dx += abs(index_state[i][0] - index_goal[i][0])
            dy += abs(index_state[i][1] - index_goal[i][1])
        return (dx+dy)
    #http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html

    def MaxH(self, node):
        return max(self.h(node), self.manhattan(node))

def displayDuckPuzzle(state):
    llist = list(state)
    llist[llist.index(0)] = "*"
    state = tuple(llist)
    print("{} {}".format(state[0], state[1]))
    print("{} {} {} {}".format(state[2], state[3], state[4], state[5]))
    print("  {} {} {}".format(state[6], state[7],state[8]))
    return None

def make_rand_Duckpuzzle():    
    '''generates the random number like make_rand_8puzzle. 
    However, it calls astar function to make sure that astar does not return 'None'. 
    If it returns None, it means that the tuple is not solvable. 
    By checking solvability in this way, I can check the tuple that is generated by other people.
    Changes list to tuple at the end
    '''
    initial = list(range(0, 9))
    random.shuffle(initial)
    initial_tuple = tuple(initial)
    puzzle = DuckPuzzle(initial_tuple)
    while (puzzle.check_solvability(initial_tuple) == False):
        random.shuffle(initial)
        initial_tuple = tuple(initial)
    return initial_tuple


'''
#Test individual puzzle
a=make_rand_8puzzle()



puzzle = EightPuzzle(a)
if (puzzle.check_solvability(a)==False):
    print("False")
    exit()
display(a)
start_time = time.time()

print("A*")
print("length: ",astar_search(puzzle)[1])
print("Nodes removed from Frontier: ",astar_search(puzzle)[2])
#print("Path Taken: ",astar_searchMH(puzzle)[3])
print("--- %.5f seconds ---" % (time.time() - start_time))
print("---------------------------")

print("Manhattan")
start_time = time.time()
print("length: ",astar_searchMH(puzzle)[1])
print("Nodes removed from Frontier: ",astar_searchMH(puzzle)[2])
#print("Path Taken: ",astar_searchMH(puzzle)[3])
print("--- %.5f seconds ---" % (time.time() - start_time))
print("---------------------------")

print("Max")
start_time = time.time()
print("length: ",astar_searchMaxH(puzzle)[1])
print("Nodes removed from Frontier: ",astar_searchMaxH(puzzle)[2])
#print("Path Taken: ",astar_searchMH(puzzle)[3])
print("--- %.5f seconds ---" % (time.time() - start_time))

a=make_rand_Duckpuzzle()
puzzle = DuckPuzzle(a)
displayDuckPuzzle(a)
if puzzle.check_solvability(a) != True:
    exit()
start_time = time.time()

print("A*")
print("length: ",astar_search(puzzle)[1])
print("Nodes removed from Frontier: ",astar_search(puzzle)[2])
print("--- %.5f seconds ---" % (time.time() - start_time))
print("---------------------------")

print("Manhattan")
start_time = time.time()
print("length: ",astar_searchMH(puzzle)[1])
print("Nodes removed from Frontier: ",astar_searchMH(puzzle)[2])
print("--- %.5f seconds ---" % (time.time() - start_time))
print("---------------------------")

print("Max")
start_time = time.time()
print("length: ",astar_searchMaxH(puzzle)[1])
print("Nodes removed from Frontier: ",astar_searchMaxH(puzzle)[2])
print("--- %.5f seconds ---" % (time.time() - start_time))

'''

print("Test 8Puzzle")
for x in range(10):
    print("-----------test ", x+1, "---------------")
    a = make_rand_8puzzle() 
    puzzle = EightPuzzle(a)
    display(a)
    start_time = time.time()

    print("A*")
    print("length: ",astar_search(puzzle)[1])
    print("Nodes removed from Frontier: ",astar_search(puzzle)[2])
    print("--- %.5f seconds ---" % (time.time() - start_time))
    print("---------------------------")

    print("Manhattan")
    start_time = time.time()
    print("length: ",astar_searchMH(puzzle)[1])
    print("Nodes removed from Frontier: ",astar_searchMH(puzzle)[2])
    print("--- %.5f seconds ---" % (time.time() - start_time))
    print("---------------------------")

    print("Max")
    start_time = time.time()
    print("length: ",astar_searchMaxH(puzzle)[1])
    print("Nodes removed from Frontier: ",astar_searchMaxH(puzzle)[2])
    print("--- %.5f seconds ---" % (time.time() - start_time))

    print("-----------test ", x+1, " Done------------\n\n")

print("Test DuckPuzzle")
for x in range(10):
    print("-----------test ", x+1, "---------------")
    a = make_rand_Duckpuzzle()
    puzzle = DuckPuzzle(a)
    displayDuckPuzzle(a)
    start_time = time.time()

    print("A*")
    print("length: ",astar_search(puzzle)[1])
    print("Nodes removed from Frontier: ",astar_search(puzzle)[2])
    print("--- %.5f seconds ---" % (time.time() - start_time))
    print("---------------------------")

    print("Manhattan")
    start_time = time.time()
    print("length: ",astar_searchMH(puzzle)[1])
    print("Nodes removed from Frontier: ",astar_searchMH(puzzle)[2])
    print("--- %.5f seconds ---" % (time.time() - start_time))
    print("---------------------------")

    print("Max")
    start_time = time.time()
    print("length: ",astar_searchMaxH(puzzle)[1])
    print("Nodes removed from Frontier: ",astar_searchMaxH(puzzle)[2])
    print("--- %.5f seconds ---" % (time.time() - start_time))

    print("-----------test ", x+1, " Done------------\n\n")
