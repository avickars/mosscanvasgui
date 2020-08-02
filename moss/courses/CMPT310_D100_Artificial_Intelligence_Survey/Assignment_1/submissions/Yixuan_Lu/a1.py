# a1.py
# yixuan lu
# 301336734

from search import *

import random
import time


# learn from course reference book section 3.6.
# https://github.com/aimacode/aima-python/blob/master/search.ipynb
# modify best_first_graph_search in search.py, adding counter to count removed nodes


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
    numRemoved=0    #counter
    while frontier:
        node = frontier.pop()
        numRemoved=numRemoved+1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node,numRemoved
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None,numRemoved      #return num of removed nodes

# remove display to solve TypeError: cannot unpack non-iterable Node object
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


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
        # exclude zero since misplaced will overestimate true cost
        return sum(s != g and s !=0 for (s, g) in zip(node.state, self.goal))


    
#1 helper functions
    
def make_rand_8puzzle():
    my_state=[1,2,3,4,5,6,7,8,0]
    random.shuffle(my_state)
    my_puzzle=EightPuzzle(tuple(my_state))
    while not my_puzzle.check_solvability(my_state):
        random.shuffle(my_state)
        
    my_puzzle=EightPuzzle(tuple(my_state))

    return my_puzzle

def display(state):
    size=9
    for i in range(size):
        if i%3==2:
            if state[i]==0:
                print('*','\n',sep=' ')
            else:
                print(state[i],'\n',sep=' ')
        else:
            if state[i]==0:
                print('*',end=' ')
            else:
                print(state[i],end=' ')

#2 comparing algorithms

# learn from course reference book section 3.6.
# https://github.com/aimacode/aima-python/blob/master/search.ipynb
def manhattan_dis(node):
    current = node.state
    goal_block = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    current_block = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    
    for i in range(len(current)):
        current_block[current[i]] = index[i]
    
    man_dis=0
    
    for i in range(1,9):
        man_dis = abs(current_block[i][0]-goal_block[i][0]) + man_dis # x-axis
        man_dis = abs(current_block[i][1]-goal_block[i][1]) + man_dis # y-axis
    
    return man_dis

def maxHeuristic(node):
    mypuzzle=EightPuzzle(node.state)

    return max(manhattan_dis(node),mypuzzle.h(node))

'''
def man_runningtime(puzzle):

'''
def runningtime():
    mis_puzzle=make_rand_8puzzle()
    man_puzzle=mis_puzzle
    mix_puzzle=mis_puzzle
    display(mis_puzzle.initial)
    start_time = time.time()
    astar_res , numRemoved = astar_search(mis_puzzle)
    elapsed_time = time.time() - start_time
    print('-----------------------------',end='\n')
    print('Using misplaced tile heuristic')
    print('Solution:',astar_res.solution(),sep=' ')
    print('Running time ',elapsed_time,'seconds')
    print('The length of solution ', len(astar_res.solution()))
    print('Total number of removed nodes ', numRemoved)
    start_time = time.time()
    astar_res , numRemoved = astar_search(man_puzzle,manhattan_dis)
    elapsed_time = time.time() - start_time
    print('-----------------------------',end='\n')
    print('Using Manhattan distance heuristic')
    print('Solution:',astar_res.solution(),sep=' ')
    print('Running time ',elapsed_time,'seconds')
    print('The length of solution ', len(astar_res.solution()))
    print('Total number of removed nodes ', numRemoved)
    start_time = time.time()
    astar_res , numRemoved = astar_search(mix_puzzle,maxHeuristic)
    elapsed_time = time.time() - start_time
    print('-----------------------------',end='\n')
    print('Using the max of the misplaced tile heuristic and the Manhattan distance heuristic')
    print('Solution:',astar_res.solution(),sep=' ')
    print('Running time ',elapsed_time,'seconds')
    print('The length of solution ', len(astar_res.solution()))
    print('Total number of removed nodes ', numRemoved)
    
'''
def man_runningtime(node):
    puzzle=node
    start_time = time.time()
    answer , removed = astar_search(puzzle,mannhattan_dis)
    elapsed_time = time.time() - start_time
    print('-----------------------------',end='\n')
    print('Using Manhattan distance heuristic')
    print('Running time ',elapsed_time,'seconds')
    print('The length of solution ', len(answer.solution()))
    print('Total number of removed nodes ', removed)

def max_runnningtime(node):
    puzzle=node
    start_time = time.time()
    answer , removed = astar_search(puzzle,maxHeuristic)
    elapsed_time = time.time() - start_time
    print('-----------------------------',end='\n')
    print('Using the max of the misplaced tile heuristic and the Manhattan distance heuristic')
    print('Running time ',elapsed_time,'seconds')
    print('The length of solution ', len(answer.solution()))
    print('Total number of removed nodes ', removed)

def solvingPuzzle():
    mis_puzzle=make_rand_8puzzle()
    man_puzzle=mis_puzzle
    mix_puzzle=mis_puzzle
    display(mis_puzzle.initial)
    mis_runningtime(mis_puzzle) #misplaced tile heuristic 
    man_runningtime(man_puzzle) #Manhattan distance heuristic
    max_runnningtime(mix_puzzle)    #max of the misplaced tile heuristic and the Manhattan distance heuristic
'''


times=10
for i in range(times):
    print('-----------------------------',end='\n')
    print(i+1,'time',sep=' ')
    runningtime()

'''
times=0
print("times ", times+1)
eight_puz = make_rand_8puzzle()
man_puz = eight_puz
max_of_both = eight_puz

    #misplaced tile heuristic-----------------------------------
display(eight_puz.initial)
start_time = time.time()
answer , removed = astar_search(eight_puz)
elapsed_time = time.time() - start_time

print('A*-search using the misplaced tile heuristic')
print('Time Taken : ',elapsed_time,'s')
print('Length of Solution : ', len(answer.solution()))
print('Total # of nodes removed from frontier : ', removed)


'''
#3 the house_puzzle
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x4 board. Tile cannot be place
        on [0][2],[0][3],[2][0]"""

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
        
        if index_blank_square==0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')

        if index_blank_square==1:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
            
        if index_blank_square==2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        # 3 has no restriction
        
        if index_blank_square==4:
            possible_actions.remove('UP')

        if index_blank_square==5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')

        if index_blank_square==6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')

        if index_blank_square==7:
            possible_actions.remove('DOWN')

        if index_blank_square==8:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')
            
        
        
            
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)


        if blank==0 or blank==1 or blank==2:
            delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank==3 or blank==4 or blank==5:
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
        """ Checks if the given state is solvable """
        # since I dont know how to check solvability for all random duckpuzzle, I only check puzzle with particular cases
        # let first four tiles 0,1,2,3 be in state 0 to 3 and goal is state[0]=1, state[1]=2, state[2]=3, state[3]=0
        # Then we can focus on the remaining 2*3 gameboard with 4 to 8 and 0, if 2*2 is solvable
        #-----------------------------------
        # checking 2*2
        
        if state[0]+state[1]+state[2]+state[3]!=6:
            return False
       
        flag=False
        if state[0]==1:
            if state[1]==2 and state[2]==3:
                flag=True
            elif state[1]==0 and state[2]==3:
                flag=True
                
        elif state[0]==2:
            if state[1]==3 and state[2]==1:
                flag=True
            elif state[1]==3 and state[2]==1:
                flag=True
            elif state[1]==0 and state[2]==1:
                flag=True

        elif state[0]==3:
            if state[1]==1 and state[2]==2:
                flag=True
            elif state[1]==1 and state[2]==0:
                flag=True
            elif state[1]==0 and state[2]==2:
                flag=True


        elif state[0]==0:
            if state[1]==1 and state[2]==3:
                flag=True
            elif state[1]==3 and state[2]==2:
                flag=True
            elif state[1]==2 and state[2]==1:
                flag=True

            
        if flag==False:
            return False
        '''
        inversion_f = 0
        for i in range(4):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion_f += 1
        if inversion_f % 2==1:
            return False
        '''
        # checking 2*3
        inversion_s = 0
        for i in range(3,len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion_s += 1
        return inversion_s % 2==0


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        # exclude zero since misplaced will overestimate true cost
        return sum(s != g and s!=0 for (s, g) in zip(node.state, self.goal))
    
def make_rand_dpuzzle():
    my_state=[1,2,3,4,5,6,7,8,0]
    random.shuffle(my_state)
    my_puzzle=DuckPuzzle(tuple(my_state))
    while not my_puzzle.check_solvability(my_state):
        random.shuffle(my_state)
        
    my_puzzle=DuckPuzzle(tuple(my_state))

    return my_puzzle

def display_dp(state):
    for i in range(2):
        if state[i]==0:
            print('*',end=' ')
        else:
            print(state[i],end=' ')
    print('\n')
    for i in range(4):
        if state[i+2]==0:
            print('*',end=' ')
        else:
            print(state[i+2],end=' ')
    print('\n')
    print(' ',end=' ')
    for i in range(3):
        if state[i+6]==0:
            print('*',end=' ')
        else:
            print(state[i+6],end=' ')
    print('\n')
    
# learn from course reference book section 3.6.
# https://github.com/aimacode/aima-python/blob/master/search.ipynb
def manhattan_dis_dp(node):
    current = node.state
    goal_block = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
    current_block = {}
    index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
    
    for i in range(len(current)):
        current_block[current[i]] = index[i]
    
    man_dis=0
    
    for i in range(1,9):
        man_dis = abs(current_block[i][0]-goal_block[i][0]) + man_dis # x-axis
        man_dis = abs(current_block[i][1]-goal_block[i][1]) + man_dis # y-axis
    
    return man_dis

def maxHeuristic_dp(node):
    mypuzzle=DuckPuzzle(node.state)

    return max(manhattan_dis_dp(node),mypuzzle.h(node))

def runningtime_dp():
    mis_puzzle=make_rand_dpuzzle()
    man_puzzle=mis_puzzle
    mix_puzzle=mis_puzzle
    display_dp(mis_puzzle.initial)
    start_time = time.time()
    astar_res , numRemoved = astar_search(mis_puzzle)
    elapsed_time = time.time() - start_time
    print('-----------------------------',end='\n')
    print('Using misplaced tile heuristic')
    print('Solution:',astar_res.solution(),sep=' ')
    print('Running time ',elapsed_time,'seconds')
    print('The length of solution ', len(astar_res.solution()))
    print('Total number of removed nodes ', numRemoved)
    start_time = time.time()
    astar_res , numRemoved = astar_search(man_puzzle,manhattan_dis_dp)
    elapsed_time = time.time() - start_time
    print('-----------------------------',end='\n')
    print('Using Manhattan distance heuristic')
    print('Solution:',astar_res.solution(),sep=' ')
    print('Running time ',elapsed_time,'seconds')
    print('The length of solution ', len(astar_res.solution()))
    print('Total number of removed nodes ', numRemoved)
    start_time = time.time()
    astar_res , numRemoved = astar_search(mix_puzzle,maxHeuristic_dp)
    elapsed_time = time.time() - start_time
    print('-----------------------------',end='\n')
    print('Using the max of the misplaced tile heuristic and the Manhattan distance heuristic')
    print('Solution:',astar_res.solution(),sep=' ')
    print('Running time ',elapsed_time,'seconds')
    print('The length of solution ', len(astar_res.solution()))
    print('Total number of removed nodes ', numRemoved)
times=10
for i in range(times):
    print('\n')
    print('-----------------------------',end='\n')
    print('Duck Puzzle',end='\n')
    print('-----------------------------',end='\n')
    print(i+1,'time',sep=' ')
    print('\n')
    runningtime_dp()

