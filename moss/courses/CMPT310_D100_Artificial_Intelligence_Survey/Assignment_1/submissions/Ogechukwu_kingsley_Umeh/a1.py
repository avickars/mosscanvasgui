#
#  a1.py
#  a1
#
#  Created by Ogechukwu Kingsley Umeh on 2020-05-29.
# Copyright © 2020 Ogechukwu Kingsley Umeh. All rights reserved.
#

from random import randint
import time
from search import *

#NOTE!!!

#the following code should have been imported from search.py

#please bare with me because i'm new to python, so i copied the whole class plus the part i editted  from search.py

#changed code from the search class:
#My Manhattan_dist heuristic function for eight puzzle class is at line 86 and 113

#plus i also edited best_first_graph_search at line 211

# my house-puzzle class is on line 113
# ______________________________________________________________________________
# A* heuristics 

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

    def Manhattan_dist_h(self, node):
        state=node.state
        answer=0
        for iterator, item in enumerate(state):
        
            node_x, node_y=int(item/3), (item%3)
            
            index=iterator+1
            if index==9:
                index=0
            goal_x, goal_y=int(index/3), (index%3)
            
            answer+=abs(node_x-goal_x)+abs(node_y-goal_y)
        
        return answer
    
    def max_h(self, node):
        return max(self.Manhattan_dist_h(node), self.h(node))
        

    
# ______________________________________________________________________________

# this class was impleamented in search.py

class HousePuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, "", "", 3, 4, 5, 6, "",  7, 8, 0)):
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

        if (index_blank_square % 4 == 0) or (index_blank_square==9):
            possible_actions.remove('LEFT')
        if (index_blank_square < 4) or (index_blank_square==6) or (index_blank_square==7):
            possible_actions.remove('UP')
        if (index_blank_square % 4 == 3) or (index_blank_square==1):
            possible_actions.remove('RIGHT')
        if (index_blank_square > 7) or (index_blank_square==4):
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal
    
    def make_solvable(self):
        for i in range(150):
            moves=self.actions(self.initial);
            moves_num=len(moves)-1;
            random_move=randint(0, moves_num);
            self.initial=self.result(self.initial, moves[random_move]);


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def Manhattan_dist_h(self, node):
        state=node.state
        answer=0
        for i in range(9):
            value=node.state.index(i);
            node_x, node_y=int(value/3), (value%3)
            
            value=self.goal.index(i)
            goal_x, goal_y=int(value/3), (value%3)
            
            answer+=abs(node_x-goal_x)+abs(node_y-goal_y)
        
        return answer
    
    def max_h(self, node):
        return max(self.Manhattan_dist_h(node), self.h(node))
        

    
# ______________________________________________________________________________



def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    count=0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        count+=1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node,  count, len(node.solution())
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None




# ______________________________________________________________________________






#NOTE!!!

#codes not imported from search.py


#
def make_rand_8puzzle():
    while True:
        state=tuple(np.random.permutation(9))
        puzzle=EightPuzzle(initial=state)
        if puzzle.check_solvability(state)==True:
            return puzzle
         
            
def display(state):
    for i in range(0, 9, 3):
        print('*' if (state[i]==0) else state[i], 
              '*' if (state[i+1]==0) else state[i+1], 
              '*' if(state[2+i]==0)else state[i+2])  
        
        
#creates a list of  8puzzle       
def list_of_8puzzle():
    lst=[make_rand_8puzzle()]
    for i in range(9):
        lst.append(make_rand_8puzzle())
        
    return lst


#creates a list of
def list_of_Hpuzzle():
    state_h=(1, 2, "", "", 3, 4, 5, 6, "",  7, 8, 0)
    m=HousePuzzle(state_h)
    m.make_solvable()
    lst=[m]
    for i in range(9):
        m=HousePuzzle(state_h)
        m.make_solvable()
        lst.append(m)
        print(m.initial)
        
    return lst
        

    

lst=list_of_8puzzle()        
h=list_of_Hpuzzle()

print("\nEightPuzzle - max heuristic")
time1=[]#store time spent
paths1=[]#stores length of solution
frontier1=[]#stores lenthgth of remaining  frontier
# and this same format goes for the remaining code

for i in range(10):
    
    a=time.time()
    A=astar_search(problem=lst[i], h=lst[i].max_h)
    b=time.time()
    print("list[",i,"]: ", lst[i].initial, '   Time: ', b-a, "  count: ", A[1], "Len(solution): ", A[2])
    time1.append(b-a)
    paths1.append(A[1])
    frontier1.append(A[2])
    
    
print("EightPuzzle - Manhattan distance heuristic")

time_mhd=[]
paths_mhd=[]
frontier_mhd=[]


for i in range(10):
    
    a=time.time()
    A=astar_search(problem=lst[i], h=lst[i].Manhattan_dist_h)
    b=time.time()
    print("list[",i,"]: ", lst[i].initial, '   Time: ', b-a, "  count: ", A[1], "Len(solution): ", A[2])
    time1.append(b-a)
    time_mhd.append(b-a)
    paths_mhd.append(A[1])
    frontier_mhd.append(A[2])

    
print("\nEightPuzzle - misplaced tile heuristic")
time_misplaced=[]
paths_misplaced=[]
frontier_misplaced=[]
for i in range(10):
    
    
    a=time.time()
    A=astar_search(problem=lst[i], h=lst[i].h)
    b=time.time()
    print("list[",i,"]: ", lst[i].initial, '   Time: ', b-a, "  count: ", A[1], "Len(solution): ", A[2])
    time_misplaced.append(b-a)
    paths_misplaced.append(A[1])
    frontier_misplaced.append(A[2])
    
print("\nHousePuzzle - max heuristic")
time2=[]
paths2=[]
frontier2=[]

for i in range(10):
    a=time.time()
    A=astar_search(problem=h[i], h=h[i].max_h)
    b=time.time()
    print("list[",i,"]: ", h[i].initial, '   Time: ', b-a, "  count: ", A[1], "Len(solution): ", A[2])
    time2.append(b-a)
    paths2.append(A[1])
    frontier2.append(A[2])
    
    
print("nHousePuzzle - Manhattan distance heuristic")

time_mhd1=[]
paths_mhd1=[]
frontier_mhd1=[]

for i in range(10):
    
    a=time.time()
    A=astar_search(problem=h[i], h=h[i].Manhattan_dist_h)
    b=time.time()
    print("list[",i,"]: ", h[i].initial, '   Time: ', b-a, "  count: ", A[1], "Len(solution): ", A[2])
    time_mhd1.append(b-a)
    paths_mhd1.append(A[1])
    frontier_mhd1.append(A[2])
    
    
print("\nHousePuzzle - misplaced tile heuristic")
    
time_misplaced1=[]
paths_misplaced1=[]
frontier_misplaced1=[]

for i in range(10):
    
    a=time.time()
    A=astar_search(problem=h[i], h=h[i].h)
    b=time.time()
    print("list[",i,"]: ", h[i].initial, '   Time: ', b-a, "  count: ", A[1], "Len(solution): ", A[2])
    time_misplaced1.append(b-a)
    paths_misplaced1.append(A[1])
    frontier_misplaced1.append(A[2])
