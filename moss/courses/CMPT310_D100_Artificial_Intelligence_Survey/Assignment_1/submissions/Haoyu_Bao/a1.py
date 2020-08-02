#!/usr/bin/env python
# coding: utf-8

# In[160]:


# a1.py


# In[161]:


from search import *
import random
import time


# In[162]:


def make_rand_8puzzle(): 
    arr=[0,1,2,3,4,5,6,7,8]
    puzzle = EightPuzzle(tuple(arr))
    while True:
        random.shuffle(arr)
        if puzzle.check_solvability(tuple(arr)):
            break
    puzzle.initial = tuple(arr)
    return puzzle


# In[163]:


def display(state):
    i = 0

    for i in range(0,9):
        if state[i] == 0:
            print('*' , end = '')
            if (i+1) % 3 == 0:
                print('\n' , end = '')
            else:
                print(' ', end = '')
        else:
            print(state[i] , end = '')
            if (i+1) % 3 == 0:
                print('\n' , end = '')
            else:
                print(' ', end = '')


# In[164]:


def manhattan(node):
    state = node.state
    index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    x, y = 0, 0
        
    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0
    for i in range(8):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        
    return mhd


# In[165]:


def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


# In[180]:


def best_first_graph_search(problem, f):
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
    count=0
    while frontier:
        node = frontier.pop()
        count+=1
        if problem.goal_test(node.state):
            return node, count
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, None


# In[181]:


def max_heuristic(node):
    puzzle = EightPuzzle(node.state)
    return max(puzzle.h(node), manhattan(node))


# In[182]:


def part2():
    print('8-puzzle')
    for i in range(1,11):
        puzzle = make_rand_8puzzle()
        print(f'({i})')
        display(puzzle.initial)
    
        print('Misplaced Tile Heuristic')
        start_time = time.time()
        node, num = astar_search(puzzle, puzzle.h)
        elapsed_time = time.time() - start_time
        print(f'elapsed time (in seconds): {elapsed_time}')
        print(f'length of solution: {node.path_cost}')
        print(f'nodes removed: {num}\n')

        print('Manhattan Heuristic')
        start_time = time.time()
        node, num = astar_search(puzzle, manhattan)
        elapsed_time = time.time() - start_time
        print(f'elapsed time (in seconds): {elapsed_time}')
        print(f'length of solution: {node.path_cost}')
        print(f'nodes removed: {num}\n')

        print('Max Heuristic')
        start_time = time.time()
        node, num = astar_search(puzzle, max_heuristic)
        elapsed_time = time.time() - start_time
        print(f'elapsed time (in seconds): {elapsed_time}')
        print(f'length of solution: {node.path_cost}')
        print(f'nodes removed: {num}\n')


# In[183]:


def display_Duck(state):
    for i in range(9):
        if state[i] == 0: #Print * when it is 0
            print('*', end = '')
            if i == 1 or i == 8:
                print('\n', end = '') #Change end variable to keep the line
            elif i == 5:
                print('\n', ' ', end = '')
            else:
                print(' ', end = '')
        else:
            print(state[i], end = '')
            if i == 1 or i == 8:
                print('\n', end = '')
            elif i == 5:
                print('\n', ' ', end = '')
            else:
                print(' ', end = '')


# In[184]:


def make_rand_Duckpuzzle():
    state = [1,2,3,4,5,6,7,8,0]
    blank = 8
    for i in range(random.randint(10000,50000)):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        if blank % 2 == 0 and blank != 4 and blank  != 8:
            possible_actions.remove('LEFT')
        if blank  < 2 or (blank  > 3 and blank  < 6):
            possible_actions.remove('UP')
        if blank  % 4 == 1 or blank  == 8:
            possible_actions.remove('RIGHT')
        if blank  > 5 or blank  == 2:
            possible_actions.remove('DOWN')  
        action = random.sample(possible_actions, 1)[0]
        if blank == 2 or blank == 3 or blank == 4 or blank == 5:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            state[blank], state[neighbor] = state[neighbor], state[blank]
        if blank < 2:
            delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            state[blank], state[neighbor] = state[neighbor], state[blank]
        if blank > 5: 
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            state[blank], state[neighbor] = state[neighbor], state[blank]
        blank = neighbor
        
    goal_puzzle = DuckPuzzle(tuple(state)) 
            
    return goal_puzzle


# In[185]:


def mhd_Duck(start, end):
    """ Given two index start and end, calculate the distance from start to end"""
    
    if start == end:
        return 0
    if start > end:
        return mhd_Duck(end, start)
    if end == 1:
        return 4
    elif end == 8:
        return 1 + mhd_Duck(start,6)
    elif end-start == 3:
        return 1
    elif end-start and (start+end)%3 != 0:
        return 1       
    elif end == 4:
        return 1 + mhd_Duck(start,3)
    elif end == 3:
        return 2
    else:
        return 1 + mhd_Duck(start,end-3)


# In[186]:


def manhattan_Duck(node):
    puzzle = DuckPuzzle(node.state)
    return max(puzzle.h(node), manhattan_Duck(node))


# In[187]:


def max_heuristic_Duck(node):
    puzzle = DuckPuzzle(node.state)
    return max(puzzle.h(node), manhattan_Duck(node))


# In[188]:


class DuckPuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)
    
    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)
    
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
            
        if index_blank_square % 2 == 0 and index_blank_square != 4 and index_blank_square != 8:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or (index_blank_square > 3 and index_blank_square < 6):
            possible_actions.remove('UP')
        if index_blank_square % 4 == 1 or index_blank_square == 8:
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
        
        if blank == 2 or blank ==3 or blank ==4 or blank ==5: 
            delta = {'UP':-2, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank < 2:
            delta = {'UP':-3, 'DOWN':2, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank > 5:
            delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
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


# In[191]:


def part3():
    print('Duck-puzzle')
    for i in range(1,11):
        puzzle = make_rand_Duckpuzzle()
        print(f'({i})')
        display_Duck(puzzle.initial)
    
        print('Misplaced Tile Heuristic')
        start_time = time.time()
        node, num = astar_search(puzzle, puzzle.h)
        elapsed_time = time.time() - start_time
        print(f'elapsed time (in seconds): {elapsed_time}')
        print(f'length of solution: {node.path_cost}')
        print(f'nodes removed: {num}\n')
        
  
    

        
        

        print('Manhattan Heuristic')
        start_time = time.time()
        node, num = astar_search(puzzle, manhattan_Duck)
        elapsed_time = time.time() - start_time
        print(f'elapsed time (in seconds): {elapsed_time}')
        print(f'length of solution: {node.path_cost}')
        print(f'nodes removed: {num}\n')

        print('Max Heuristic')
        start_time = time.time()
        node, num = astar_search(puzzle, max_heuristic_Duck)
        elapsed_time = time.time() - start_time
        print(f'elapsed time (in seconds): {elapsed_time}')
        print(f'length of solution: {node.path_cost}')
        print(f'nodes removed: {num}\n')      


# In[192]:


part3()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




