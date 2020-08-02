#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Q1


# In[2]:


import numpy as np


# In[3]:


from search import *


# In[4]:


import time


# In[5]:


def display(state):
    i=0
    while i<9:
        if state[i]==0:
            print("*",state[i+1],state[i+2])
        elif state[i+1]==0:
            print(state[i],"*",state[i+2])
        elif state[i+2]==0:
            print(state[i],state[i+1],"*")
        else :
             print(state[i],state[i+1],state[i+2])
        i=i+3


# In[6]:


def make_rand_8puzzle():
    state = tuple(np.random.permutation(9))
    dummy_puzzle = EightPuzzle(initial = state)
    while (1):
        if dummy_puzzle.check_solvability(state)== True:
            break
        else:
            state = tuple(np.random.permutation(9))
            dummy_puzzle = EightPuzzle(initial = state)
    return dummy_puzzle


# In[7]:


#Q2


# In[8]:


def best_first_graph_search(problem, f, display=False):
    counter=0;
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        counter=counter+1
        if problem.goal_test(node.state):
            print(counter)
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


# In[9]:


start=time.time()
puzzle = make_rand_8puzzle()
node=astar_search(puzzle)
end=time.time()


# In[10]:


print("misplace time: ",end-start)


# In[11]:


print("misplace length: ",len(node.path()))


# In[12]:


def manhattan(node):
    state = node.state
    index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    
    for i in range(len(state)):
        index_state[state[i]] = index[i]
    
    mhd = 0
    
    for i in range(8):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
    
    return mhd


# In[13]:


start=time.time()


# In[14]:


print("manhattan len: ",len(astar_search(puzzle,manhattan(node)).path()))


# In[15]:


end=time.time()


# In[16]:


print("manhattan time: ",end-start)


# In[17]:


def max_heuristic(node):
    tempPuzzle = EightPuzzle(initial= node.state)
    score1 = manhattan(node)
    score2 = tempPuzzle.h(node)
    return max(score1, score2)


# In[18]:


start=time.time()


# In[19]:


print("max_heuristic len: ",len(astar_search(puzzle,max_heuristic(node)).path()))


# In[20]:


end=time.time()


# In[21]:


print("max_heuristic time: ",end-start)


# In[22]:


#Q3


# In[23]:


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

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square ==6:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square ==5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square ==8:
            possible_actions.remove('RIGHT')
        if index_blank_square ==2 or index_blank_square > 5:
            possible_actions.remove('DOWN')
        return possible_actions
    
    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        if blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        if blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)
    
    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal
    
    def check_solvability(self, state):
        top_check = [0,1,2,3]
        one = state.index(1)
        two = state.index(2)
        three = state.index(3)
        
        if one < 4 and two < 4 and three < 4:
            top_check.remove(one)
            top_check.remove(two)
            top_check.remove(three)
            if state[top_check[0]] != 0:
                return False
            if one == 0 and two != 1:
                return False
            elif one == 1 and two != 3:
                return False
            elif one == 2 and two != 0:
                return False
            elif one == 3 and two != 2:
                return False
            
            inversion = 0
            for i in range(3,len(state)):
                for j in range(i + 1, len(state)):
                    if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                        inversion += 1
            return inversion % 2 == 0
        else:
            return False
        
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))



# In[24]:


def display_duck(self):
    while i<9:
        if i == 1:
            print("\n",end='')
        elif i == 5:
            print("\n",end = '  ')
        if self.initial[i] == 0:
            print("*",end = ' ')
        else:
            print(self.initial[i],end = ' ')
        print("\n")


# In[25]:


def make_rand_DuckPuzzle():
    state = tuple(np.random.permutation(9))
    duck_puzzle = DuckPuzzle(initial = state)
    while (1):
        if duck_puzzle.check_solvability(state)== True:
            break
        else:
            state = tuple(np.random.permutation(9))
            duck_puzzle = DuckPuzzle(initial = state)
    return duck_puzzle


# In[26]:


start=time.time()
Dpuzzle = make_rand_DuckPuzzle()
Dnode = astar_search(Dpuzzle)
end = time.time()


# In[27]:


print("DP misplace time: ",end-start)


# In[28]:


print("DP misplace len: ",len(Dnode.path()))


# In[29]:


def Duck_manhattan(node):
    state = node.state
    index_goal = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
    index_state = {}
    index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
    
    for i in range(len(state)):
        index_state[state[i]] = index[i]
    
    mhd = 0
    
    for i in range(8):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
    
    return mhd


# In[30]:


start=time.time()


# In[31]:


print("DP manhattan len: ",len(astar_search(Dpuzzle,Duck_manhattan(Dnode)).path()))


# In[32]:


end=time.time()


# In[33]:


print("DP manhattan time: ",end-start)


# In[34]:


def Duck_max_heuristic(node):
    tempPuzzle = DuckPuzzle(initial= node.state)
    score1 = Duck_manhattan(node)
    score2 = tempPuzzle.h(node)
    return max(score1, score2)


# In[35]:


start=time.time()


# In[36]:


print("DP max_heuristic len: ",len(astar_search(Dpuzzle,Duck_max_heuristic(Dnode)).path()))


# In[37]:


end=time.time()


# In[38]:


print("DP max_heuristic time: ",end-start)


# In[ ]:




