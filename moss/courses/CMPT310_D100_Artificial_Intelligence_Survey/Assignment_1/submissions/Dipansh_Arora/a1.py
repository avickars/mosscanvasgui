#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


from utils import *


# In[3]:


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
    nodesRemovedcount=0
    while frontier:
        node = frontier.pop()
        nodesRemovedcount = nodesRemovedcount+1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node,nodesRemovedcount
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return node,nodesRemovedcount


# In[4]:


class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


# ______________________________________________________________________________


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)



# In[5]:


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# In[6]:


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
    
    def manhattan(self,node): #return manhattan distance
        current = node.state
        distance = 0
        #goal_state = [[1,2,3],[4,5,6],[7,8,0]]
        current_state = [[current[0],current[1],current[2]],[current[3],current[4],current[5]],[current[6],current[7],current[8]]]
        i=0                
        while i < 3:
            j=0
            while j < 3:

                if current_state[i][j]!=0:
                    sum = 0
                    target_pos_x = (current_state[i][j]-1)//3    #idea of this algorithm taken from https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
                    target_pos_y = (current_state[i][j]-1)%3     #checked and implemented by me
                    sum = abs(target_pos_x - i) + abs(target_pos_y -j)
                    distance = distance + sum

                j = j+1
            i= i+1

        return distance
        


# ______________________________________________________________________________



# In[7]:


class DuckPuzzle(Problem): #changes made in EightPuzzle Class to make a DuckPuzzle class
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
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')    
        if index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')  
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

        if blank == 0:
            delta = {'DOWN': 2, 'RIGHT': 1} 
        if blank == 1:
            delta = {'DOWN': 2,'LEFT': -1}            
        if blank == 2:
            delta = {'UP': -2,'RIGHT': 1}
        if blank == 3:
            delta = {'UP': -2,'LEFT': -1, 'RIGHT':1, 'DOWN':3}
        if blank == 4:
            delta = {'RIGHT': 1,'DOWN': 3,'LEFT':-1}
        if blank == 5:
            delta = {'DOWN': 3,'LEFT': -1}
        if blank == 6:
            delta = {'UP': -3,'RIGHT': 1}
        if blank == 7:
            delta = {'LEFT': -1,'UP': -3,'RIGHT':1}
        if blank == 8:
            delta = {'LEFT': -1,'UP': -3}        
    
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state): #this won't work correctly
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
    
    def manhattan(self,node): #return manhattan distance
        current = node.state
        distance = 0
    
        my_data = list()
        my_data.append((5,4,4,3,2,1,2,1,0))
        my_data.append((0,1,1,2,3,4,3,4,5))
        my_data.append((1,0,2,1,2,3,2,3,4))
        my_data.append((1,2,0,1,2,3,2,3,4))
        my_data.append((2,1,1,0,1,2,1,2,3))
        my_data.append((3,2,2,1,0,1,2,1,2))
        my_data.append((4,3,3,2,1,0,3,2,1))
        my_data.append((3,2,2,1,2,3,0,1,2))
        my_data.append((4,3,3,2,1,2,1,0,1))
        
        i=0
        while i<9:
            curr_el = current[i]
            distance = distance + (my_data[curr_el][i])
            i=i+1
        
        return distance
        


# In[8]:


def astar_search_manhattan(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.manhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# In[9]:


def max_h(mynode):
    myPuzzle=EightPuzzle(mynode.state)
    return max(myPuzzle.manhattan(mynode),myPuzzle.h(mynode))


# In[10]:


def make_rand_8puzzle():
    while True:
        state = tuple(np.random.permutation(9))
        #print(state) #comment it out
        my_puzzle = EightPuzzle(initial = state)
        solvable = my_puzzle.check_solvability(state)
        #print(solvable) #comment it out
        if solvable:
            return my_puzzle
        
    


# In[11]:


def display(state):
    myList = list(state)
    i=0
    while i<=8:
        if myList[i]==0:
            myList[i]= '*'  
        i=i+1
    print(myList[0],myList[1],myList[2])

    print(myList[3],myList[4],myList[5])
    
    print(myList[6],myList[7],myList[8])
            
            


# In[12]:


def make_rand_duckPuzzle():
    while True:
        state = tuple(np.random.permutation(9))
        #print(state) #comment it out
        my_puzzle = DuckPuzzle(initial = state)
        return my_puzzle
        


# In[13]:


def duckDisplay(state):
    myList = list(state)
    i=0
    while i<=8:
        if myList[i]==0:
            myList[i]= '*'  
        i=i+1
    print(myList[0],myList[1],'\n')

    print(myList[2],myList[3],myList[4],myList[5],'\n')
    
    print(' ',myList[6],myList[7],myList[8])


# In[14]:


import time


# In[15]:


puzzle = make_rand_8puzzle()


# In[16]:


print("8 PUZZLES :\n")


# In[17]:


print('A*-search using the misplaced tile heuristic ')
a = time.time()
solvedPuzzle, nodesRemoved = astar_search(puzzle)
b = time.time()
print('Time taken =',(b-a))
numTilesMoved = len(solvedPuzzle.solution())
print('Number of tiles moved =',numTilesMoved)
print('Total number of nodes removed from frontier = ',nodesRemoved)




# In[18]:


print('A*-search using the Manhattan distance heuristic')
a = time.time()
solvedPuzzle, nodesRemoved = astar_search_manhattan(puzzle)
b = time.time()
print('Time taken =',(b-a))
numTilesMoved = len(solvedPuzzle.solution())
print('Number of tiles moved =',numTilesMoved)
print('Total number of nodes removed from frontier = ',nodesRemoved)
#display(solvedPuzzle.state)


# In[19]:


print('A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic')
a = time.time()
solvedPuzzle, nodesRemoved = astar_search(puzzle,h = max_h)
b = time.time()
print('Time taken =',(b-a))
numTilesMoved = len(solvedPuzzle.solution())
print('Number of tiles moved =',numTilesMoved)
print('Total number of nodes removed from frontier = ',nodesRemoved)
#display(solvedPuzzle.state)


# In[20]:


print("DUCK PUZZLES :\n\n")


# In[21]:


duck = make_rand_duckPuzzle()


# In[22]:


print('A*-search using the misplaced tile heuristic ')
a = time.time()
solvedPuzzle, nodesRemoved = astar_search(duck)
b = time.time()
print('Time taken =',(b-a))
numTilesMoved = len(solvedPuzzle.solution())
print('Number of tiles moved =',numTilesMoved)
print('Total number of nodes removed from frontier = ',nodesRemoved)


# In[23]:


print('A*-search using the Manhattan distance heuristic')
a = time.time()
solvedPuzzle, nodesRemoved = astar_search_manhattan(duck)
b = time.time()
print('Time taken =',(b-a))
numTilesMoved = len(solvedPuzzle.solution())
print('Number of tiles moved =',numTilesMoved)
print('Total number of nodes removed from frontier = ',nodesRemoved)


# In[24]:


print('A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic')
a = time.time()
solvedPuzzle, nodesRemoved = astar_search(duck,h = max_h)
b = time.time()
print('Time taken =',(b-a))
numTilesMoved = len(solvedPuzzle.solution())
print('Number of tiles moved =',numTilesMoved)
print('Total number of nodes removed from frontier = ',nodesRemoved)
#display(solvedPuzzle.state)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




