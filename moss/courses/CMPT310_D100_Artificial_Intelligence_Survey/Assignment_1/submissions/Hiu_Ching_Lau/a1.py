#CMPT310 A1.py
#Name: Lau Hiu Ching
#Student ID: 301220487
#Resources i looked up online
#Explanation of 8 Puzzle  https://www.cs.princeton.edu/courses/archive/spr10/cos226/assignments/8puzzle.html
#Explanation of tuple     https://www.tutorialspoint.com/python3/python_tuples.htm
#Explanation of List  	   https://www.tutorialspoint.com/python3/python_lists.htm
#Manhatten         	   http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
#Manhatten  		   geeksforgeeks.org/sum-manhattan-distances-pairs-points/
#Class Notes  		   https://www2.cs.sfu.ca/CourseCentral/310/tjd/chp3_search.html


from search import *
import random
import time

# The goal of 8 puzzle
goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]

def astar_search(problem, h=None, display=True):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
    
# A*-search using the misplaced tile heuristic (this is the default heuristic in the EightPuzzle class)
def misplace_tile(node):
    return sum([1 if node.state[i] != goal[i] else 0 for i in range(8)])

# A*-search using the Manhattan distance heuristic
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

# A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic
def max_heuristic(node):
    score1 = manhattan(node)
    score2 = misplace_tile(node)
    return max(score1, score2)

#------------------------------------Assignment 1-----------------------------------------#

# Question 1: Helper Functions -- make_rand_8puzzle()
def make_rand_8puzzle():
    tile_number = (0,1,2,3,4,5,6,7,8) #8 tile number and 0 = * the empty space
    l = list(tile_number)
    random.shuffle(l)
    rand_puzzle = EightPuzzle(tuple(l))
    while(not rand_puzzle.check_solvability(tuple(l))):
        rand_puzzle.check_solvability(tuple(l))
        random.shuffle(l)
    display_8Puzzle(tuple(l))
    rand_puzzle = EightPuzzle(tuple(l))
    return rand_puzzle

# Question 1: Helper Functions -- display(state)
def display_8Puzzle(state):
    for i in range(9):
        if i%3 == 2 and state[i] == 0:
            print('*')
        elif state[i] == 0:
            print('*',end = " ")
        elif i%3 == 2:
            print(state[i])
        else:
            print(state[i],end = " ")

#--------------------------Question 2 Compare Algorithms for Eight Puzzle---------------------#

# Question 2: Comparing Algorithms
# The node removed from frontier is counted in best_first_graph_search()
def Q2Compare(EightPuzzle):
    start_time1 = time.time()
    r1 = astar_search(EightPuzzle,manhattan).solution()
    elapsed_time1 = time.time() - start_time1
    print(f'Manhattan: elapsed time (in seconds): {elapsed_time1}s')
    print("Size of solution: ", len(r1) ,)
    print()
    start_time2 = time.time()
    r2 = astar_search(EightPuzzle).solution()
    elapsed_time2 = time.time() - start_time2
    print(f'Misplace_tile: elapsed time (in seconds): {elapsed_time2}s')
    print("Size of solution: ", len(r2))
    print()
    start_time3 = time.time()
    r3 = astar_search(EightPuzzle,max_heuristic).solution()
    elapsed_time3 = time.time() - start_time3
    print(f'Max_heuristic: elapsed time (in seconds): {elapsed_time3}s')
    print("Size of solution: ", len(r3))
    print()
    
#-----------------------------------------------------------------------------------------------#
#Hardcoded cases 
#list_of_cases = [(2,7,5,0,4,1,3,8,6),(1,2,7,0,6,8,4,5,3),(3,8,1,0,2,6,4,5,7),(0,3,5,6,1,8,4,2,7)]
#for i in range(len(list_of_cases)):
#    puzzle = EightPuzzle(list_of_cases[i])
#    display_8Puzzle(list_of_cases[i])
#    Q2Compare(puzzle)

#Random cases (one case)
puzzle = make_rand_8puzzle()
Q2Compare(puzzle)
#-------------------------------------------------------------------------------------------------#

#--------------------------------Question 2 The House-Puzzle-------------------------------------#
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a Duck board, where one of the
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
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        if index_blank_square == 6:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
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
        
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        
        return tuple(new_state)
    
    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """       
        
        return state == self.goal
    
        return inversion % 2 == 0
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """
        return sum(s != g for (s, g) in zip(node.state, self.goal))

# Helper function : make_rand_duckpuzzle()
def make_rand_duckpuzzle():
    tile_number = (1,2,3,4,5,6,7,8,0)
    l = list(tile_number)
    move_tile = random.randint(10,20)
    empty_location = 0
    last_move = ''
    reverse_move = ''
    rand_puzzle = DuckPuzzle(tuple(l))
    for i in range(move_tile):
    	blank = rand_puzzle.find_blank_square(tuple(l))
    	possible_action = rand_puzzle.actions(tuple(l))
    	#forbidding the tile to move front and back and not going anywhere
    	if last_move == 'DOWN': reverse_move = 'UP'
    	elif last_move == 'UP': reverse_move = 'DOWN'
    	elif last_move == 'LEFT': reverse_move = 'RIGHT'
    	else: reverse_move = 'LEFT'
    	
    	rand = random.randint(0,len(possible_action)-1)
    	#if the random move is the revese of the last move. do random again.
    	while reverse_move == possible_action[rand]:
    	  rand = random.randint(0,len(possible_action)-1)
    	if blank < 2 and possible_action[rand] == 'DOWN': 
    	  l[blank],l[blank+2] = l[blank+2],l[blank] #cases for moving down 
    	if blank > 2 and possible_action[rand] == 'DOWN': 
    	  l[blank],l[blank+3] = l[blank+3],l[blank] #cases for moving down 
    	if blank < 4 and possible_action[rand] == 'UP': 
    	  l[blank],l[blank-2] = l[blank-2],l[blank] #cases for moving up 
    	if blank > 4 and possible_action[rand] == 'UP': 
    	  l[blank],l[blank-3] = l[blank-3],l[blank] #cases for moving up 
    	if (blank != 0 and blank != 2 and blank != 6) and possible_action[rand] == 'LEFT': 
    	  l[blank],l[blank-1] = l[blank-1],l[blank] #cases for moving left 
    	if (blank != 1 and blank != 5 and blank != 8) and possible_action[rand] == 'RIGHT':
    	  l[blank],l[blank+1] = l[blank+1],l[blank] #cases for moving left 
    	last_move = possible_action[rand]
    	#display_duckPuzzle(tuple(l)) check functions
    display_duckPuzzle(tuple(l))
    rand_puzzle = DuckPuzzle(tuple(l))
    return rand_puzzle

# Helper function : displayduck()
def display_duckPuzzle(state):
    for i in range(9):
        if i == 6 and state[i] == 0:
            print(" ",'*',end=" ")
        elif i == 6 :
            print(" ",state[i],end=" ")
        elif(i == 1 or i == 5 or i == 8) and state[i] == 0:
            print('*')
        elif state[i] == 0:
            print('*',end = " ")
        elif (i == 1 or i == 5 or i == 8) :
            print(state[i])
        else:
            print(state[i],end = " ")

# Comparing Algorithms    a = make_rand_duckpuzzle()
def Q3Compare(DuckPuzzle):
    start_time1 = time.time()
    r1 = astar_search(DuckPuzzle,manhattan).solution()
    elapsed_time1 = time.time() - start_time1
    print(f'Manhattan: elapsed time (in seconds): {elapsed_time1}s')
    print("Size of solution: ", len(r1))
    print()
    start_time2 = time.time()
    r2 = astar_search(DuckPuzzle).solution()
    elapsed_time2 = time.time() - start_time2
    print(f'Mistiled: elapsed time (in seconds): {elapsed_time2}s')
    print("Size of solution: ", len(r2))
    print()
    start_time3 = time.time()
    r3 = astar_search(DuckPuzzle,max_heuristic).solution()
    elapsed_time3 = time.time() - start_time3
    print(f'Max_heuristic: elapsed time (in seconds): {elapsed_time3}s')
    print("Size of solution: ", len(r3))
    print()
    
#-----------------------------------------------------------------------------------------------#
#Hardcoded cases 
#list_of_cases = [(8,5,3,0,2,7,4,1,6),(7,0,8,4,2,6,5,3,1),(7,6,3,1,5,0,4,2,8),(7,0,2,6,1,5,3,8,4)]
#for i in range(len(list_of_cases)):
#    puzzle = DuckPuzzle(list_of_cases[i])
#    display_duckPuzzle(list_of_cases[i])
#    Q3Compare(puzzle)

#Random cases (one case)
puzzle = make_rand_duckpuzzle()
Q3Compare(puzzle)
#-------------------------------------------------------------------------------------------------#
