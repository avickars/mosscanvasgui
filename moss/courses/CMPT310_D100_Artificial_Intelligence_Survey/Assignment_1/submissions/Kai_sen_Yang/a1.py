#!/usr/bin/env python
# coding: utf-8

# In[153]:


from search import *
import random
import time


# In[193]:


# Q1: Helper FUnctions


# In[194]:


def make_rand_8puzzle():
    ini_state = [0,1,2,3,4,5,6,7,8]
    random.shuffle(ini_state)
    goal_puzzle = EightPuzzle(tuple(ini_state)) #S. D. Sewal, GeeksforGeeks, https://www.geeksforgeeks.org/python-convert-a-list-into-a-tuple/
    #Check the solvability
    while(goal_puzzle.check_solvability(ini_state) == False):
        random.shuffle(ini_state)
        goal_puzzle = EightPuzzle(tuple(ini_state)) #Reorder the list and convert it into the tuple
        
    return goal_puzzle


# In[195]:


def display(state):
    for i in range(9):
        if state[i] == 0: #Print * when it is 0
            print('*', end = '')
            if i == 2 | i == 5:
                print('\n', end = '') #Change end variable to keep the line
            else:
                print(' ', end = '')
        else:
            print(state[i], end = '')
            if i == 2 | i == 5:
                print('\n', end = '')
            else:
                print(' ', end = '')


# In[196]:


# Q2: Comparing Algorithms


# In[197]:


#Modify best_first_graph_search to get the total number of nodes that were removed from frontier
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
    pop_num = 0
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        pop_num += 1 #Calculate the number of nodes that were removed from frontier
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, pop_num
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, pop_num

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# In[198]:


#Firstly define my own Manhattan distance heuristic function
def Manh_dis(node):
    obj_state = node.state #Call the definition of class Node
    goal = {1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1], 0:[2,2]} #Create the goal borad dictionary
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]] # Create an empty board to store position
    ini_state = {} # Create initialization dictionary to store node.state
    
    for i in range(9):
        ini_state[obj_state[i]] = index[i]
    
    distance = 0 #initialize the distance
    for i in range(1, 9): # Excluede zero
        for j in range(0, 1):
            distance += abs(goal[i][j] - ini_state[i][j])
    
    return distance


# In[199]:


#Secondly define function to find the maximum
def max_of(node):
    ini_puzzle = EightPuzzle(node.state)
    return max(ini_puzzle.h(node), Manh_dis(node))


# In[200]:


# To print time results to compare
def EightPuzzle_Test():
    test = make_rand_8puzzle()
    display(test.initial)
    
    start_time = time.time()
    goal, num_pop = astar_search(test)
    elapsed_time = time.time() - start_time
    print('Misplaced Tile Heuristic')
    print('The length of solution is' , len(goal.solution()))
    print('the total number of nodes that were removed from frontier is' , num_pop)
    print('The elapsed time: ',elapsed_time)
    
    amah = test
    start_time_mah = time.time()
    goal_mah, num_pop_mah = astar_search(amah, h = Manh_dis)
    elapsed_time_mah = time.time() - start_time_mah
    print('Manhattan Heuristic')
    print('The length of solution is' , len(goal_mah.solution()))
    print('the total number of nodes that were removed from frontier is'  , num_pop_mah)
    print('The elapsed time: ',elapsed_time_mah)

    amax = test
    start_time_max = time.time()
    goal_max, num_pop_max = astar_search(amax, h = max_of)
    elapsed_time_max = time.time() - start_time_max
    print('Max of Both')
    print('The length of solution is' , len(goal_max.solution()))
    print('the total number of nodes that were removed from frontier is'  , num_pop_max)
    print('The elapsed time: ',elapsed_time_max)


# In[85]:


#Create 10 random 8-puzzle instances
for i in range(1,11):
    print('Test ',i, ':')
    EightPuzzle_Test()


# In[ ]:


# The House-Puzzle


# In[201]:


#Modify EightPuzzle class to fit the requirements of house puzzle
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

        if blank < 2:
            delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank > 1 or blank < 6:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank > 5: 
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


# In[202]:


def Duck_Manh_dis(node):
    obj_state = node.state #Call the definition of class Node
    goal = {1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2], 0:[2,3]} #Create the goal borad dictionary
    index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]] # Create an empty board to store position
    ini_state = {} # Create initialization dictionary to store node.state
    for i in range(9):
        ini_state[obj_state[i]] = index[i]
    
    distance = 0 #initialize the distance
    for i in range(1, 9): # Excluede zero
        for j in range(0, 1):
            distance += abs(goal[i][j] - ini_state[i][j])
    
    return distance


# In[203]:


#Secondly define function to find the maximum
def Duck_max_of(node):
    ini_puzzle = EightPuzzle(node.state)
    return max(ini_puzzle.h(node), Manh_dis(node))


# In[280]:


#Since it cannot use check_solvability function, make_rand_Duckpuzzle will create a random puzzle from the correct duck-puzzle
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


# In[281]:


def display_Duckpuzzle(state):
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


# In[282]:


def DuckPuzzle_Test():
    test_duck = make_rand_Duckpuzzle()
    display_Duckpuzzle(test_duck.initial)
    start_time = time.time()
    goal, num_pop = astar_search(test_duck)
    elapsed_time = time.time() - start_time
    print('Misplaced Tile Heuristic')
    print('The length of solution is' , len(goal.solution()))
    print('the total number of nodes that were removed from frontier is' , num_pop)
    print('The elapsed time: ',elapsed_time)
    
    amah = test_duck
    start_time_mah = time.time()
    goal_mah, num_pop_mah = astar_search(amah, h = Duck_Manh_dis)
    elapsed_time_mah = time.time() - start_time_mah
    print('Manhattan Heuristic')
    print('The length of solution is' , len(goal_mah.solution()))
    print('the total number of nodes that were removed from frontier is'  , num_pop_mah)
    print('The elapsed time: ',elapsed_time_mah)

    amax = test_duck
    start_time_max = time.time()
    goal_max, num_pop_max = astar_search(amax, h = Duck_max_of)
    elapsed_time_max = time.time() - start_time_max
    print('Max of Both')
    print('The length of solution is' , len(goal_max.solution()))
    print('the total number of nodes that were removed from frontier is'  , num_pop_max)
    print('The elapsed time: ',elapsed_time_max)


# In[283]:


#Create 10 random Duck-puzzle instances
for i in range(1,11):
    print('Test ',i, ':')
    DuckPuzzle_Test()

