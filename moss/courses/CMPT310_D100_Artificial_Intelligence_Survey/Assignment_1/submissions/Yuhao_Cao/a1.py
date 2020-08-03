#!/usr/bin/env python
# coding: utf-8

# In[45]:


import numpy as np


# In[46]:


import time


# In[47]:


from search import *


# In[48]:


# def best_first_graph_search(problem, f, display=False):
#     """Search the nodes with the lowest f scores first.
#     You specify the function f(node) that you want to minimize; for example,
#     if f is a heuristic estimate to the goal, then we have greedy best
#     first search; if f is node.depth then we have breadth-first search.
#     There is a subtlety: the line "f = memoize(f, 'f')" means that the f
#     values will be cached on the nodes as they are computed. So after doing
#     a best first search you can examine the f values of the path returned."""
#     f = memoize(f, 'f')
#     node = Node(problem.initial)
#     frontier = PriorityQueue('min', f)
#     frontier.append(node)
#     explored = set()
#     counter = 0
#     while frontier:
#         node = frontier.pop()
#         counter += 1
#         if problem.goal_test(node.state):
#             if display:
#                 print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
#             path = node.path()
#             print("Total removed nodes is : %d"%counter)
#             print("The solution is :%d)"%len(path))
#             return node
#         explored.add(node.state)
#         for child in node.expand(problem):
#             if child.state not in explored and child not in frontier:
#                 frontier.append(child)
#             elif child in frontier:
#                 if f(child) < frontier[child]:
#                     del frontier[child]
#                     frontier.append(child)
#     return None
#This one is changing from search.py


# In[49]:


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

        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank == 0 or blank == 1:
            delta['DOWN'] = 2 
        if blank == 2 or blank == 3:
            delta['UP'] = -2
#         print(blank, end = " ")
#         print(action, end = " ")
#         print(delta[action], end = " ")
#         print(delta)
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
#         print(display_duck(state))
#         print(display_duck(new_state))

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """
        blank = self.find_blank_square(state)
        check_2x2 = [0,1,2,3]
        index_2x2 = [state.index(1),state.index(2),state.index(3)]
        if index_2x2[0] < 4 and index_2x2[1] < 4 and index_2x2[2] < 4:
            check_2x2.remove(index_2x2[0])
            check_2x2.remove(index_2x2[1])
            check_2x2.remove(index_2x2[2])
            if state[check_2x2[0]] != 0:
                return False
            if state[3] != 0 and state[3] != 1 and state[3] != 2 and state[3] != 4:
                return False          
            inversion = 0
            for i in range(0,len(state)):
                for j in range(i + 1, len(state)):
                    if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                        inversion += 1
            return inversion % 2 == 0
        else:
            return False

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        return sum(s != g  for (s, g) in zip(node.state, self.goal))


# In[50]:


def make_rand_8puzzle_duck():
    a = True
    while a:
        state = tuple(np.random.permutation(9))
        dummy_puzzle = DuckPuzzle(initial=state)
        solve = dummy_puzzle.check_solvability(state)
        if solve == True:
            return state
def make_rand_8puzzle():
    a = True
    while a:
        state = tuple(np.random.permutation(9))
        dummy_puzzle = EightPuzzle(initial=state)
        solve = dummy_puzzle.check_solvability(state)
        if solve == True:
            return state


# In[51]:


def display(state):
    check = 1
    for x in state:
        if x == 0:
            x = "*"
        if check == 3:
            print(x)
            check = 1
        else:
            print(x,end = " ")
            check = check + 1
def display_duck(state):
    check = 1
    for x in state:
        if x == 0:
            x = "*"
        if check == 2 or check == 6 or check == 9:
            print(x)
            check = check + 1
        else:
            if check == 7:
                print(" ",end = " ")
            print(x,end = " ")
            check = check + 1
        


# In[52]:


def manhattan(node):
    goal = {0:[0,0], 1:[0,1], 2:[0,2], 3:[1,0], 4:[1,1], 5:[1,2], 6:[2,0], 7:[2,1], 8:[2,2]}
    temp = node.state
    ind1 = 1
    dit = 0
    for x in range(0,8):
        num = temp.index(ind1)
        ind2 = ind1 -1
        val = abs(goal[ind2][0]-goal[num][0]) + abs(goal[ind2][1]-goal[num][1])
        ind1 += 1
        dit = dit + val
    return dit
def manhattan_duck(node):
    goal = {0:[0,0], 1:[0,1], 2:[1,0], 3:[1,1], 4:[1,2], 5:[1,3], 6:[2,1], 7:[2,2], 8:[2,3]}
    temp = node.state
    ind1 = 1
    dit = 0
    for x in range(0,8):
        num = temp.index(ind1)
        ind2 = ind1 -1
        val = abs(goal[ind2][0]-goal[num][0]) + abs(goal[ind2][1]-goal[num][1])
        ind1 += 1
        dit = dit + val

    return dit


# In[53]:


def my_maxh(node):
    current = EightPuzzle(node.state)
    first = manhattan(node)
    second = current.h(node)
    return max(first,second)
def my_maxh_duck(node):
    puz = DuckPuzzle(initial = node.state)
    return max(puz.h(node),manhattan_duck(node))


# In[ ]:


for x in range (0,10):
    print("---test---%d"%x)
    state = make_rand_8puzzle()
    display(state)
    puzzle = EightPuzzle(initial = state)
    a1 = time.time()
    print(astar_search(puzzle,h = puzzle.h))
    a2 = time.time()
    print(a2-a1)
    b1 = time.time()
    print(astar_search(puzzle,h = manhattan))
    b2 = time.time()
    print(b2-b1)
    d1 = time.time()
    print(astar_search(puzzle,h = my_maxh))
    d2 = time.time()
    print(d2-d1)


# In[ ]:


for x in range (0,10):
    print("---test---%d"%x)
    state = make_rand_8puzzle_duck()
    display_duck(state)
    puzzle = DuckPuzzle(initial = state)
    x1 = time.time()
    print(astar_search(puzzle,h = puzzle.h))
    x2 = time.time()
    print(x2-x1)
    y1 = time.time()
    print(astar_search(puzzle,h = manhattan_duck))
    y2 = time.time()
    print(y2-y1)
    z1 = time.time()
    print(astar_search(puzzle,h = my_maxh_duck))
    z2 = time.time()
    print(z2-z1)


# In[ ]:



