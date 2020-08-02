# a1.py

from search import *
import time
import random


# init a random 8puzzle 
def init_puzzle():
	g = []
	gg = [8,7,6,5,4,3,2,1,0]
	while len(gg) > 0:
		randIndex = random.randint(0,len(gg)-1)
		g .append(gg[randIndex])
		gg.remove(gg[randIndex])
	return tuple(g)


#make an rand 8puzzle
def make_rand_8puzzle():
	s = init_puzzle()
	ep = EightPuzzle(s)
	if ep.check_solvability(ep.initial) == True:
		return s
	else:	
		while ep.check_solvability(ep.initial) == False:
			s = init_puzzle()
			ep = EightPuzzle(s)
		return s


# print puzzle
def display(state):
	g = list(state)
	for i in range(9):
		if g[i] == 0:
			g[i] = "*"

	for i in range(3):	
		print(g[i],end=' ')
	print()
	for i in range(3,6):
		print(g[i],end=' ')
	print()
	for i in range(6,9):
		print(g[i],end=' ')
	print()


def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


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
    con = 0
    while frontier:
        node = frontier.pop()
        con += 1
        if problem.goal_test(node.state):
        	return node,con 
        explored.add(node.state)
        for child in node.expand(problem):
        	if child.state not in explored and child not in frontier:
        		frontier.append(child)
        	elif child in frontier:
        		if f(child) < frontier[child]:
        			del frontier[child]
        			frontier.append(child)
    return None


def manhattan(node):
        state = node.state
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index_state = {}
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        x, y = 0, 0
        
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        
        mhd = 0
        
        for i in range(1,9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        
        return mhd


def MaxA(ep):
	node = Node(ep.initial)
	if ep.h(node) > manhattan(node):
		return True
	else:
		return False


############################################################################################################


def init_HousePuzzle():
	gg = list(init_puzzle())
	g = []
	g.append(gg[0])
	g.append(-1)
	for i in range(1,8):
		g.append(gg[i])
	g.append(-2)
	g.append(gg[8])
	g.append(-3)
	s = tuple(g)
	return s


def make_rand_HousePuzzle():
	s = init_HousePuzzle()
	Hp = HousePuzzle(s)
	if Hp.check_solvability(Hp.initial) == True:
		return s
	else:	
		while Hp.check_solvability(Hp.initial) == False:
			s = init_HousePuzzle()
			Hp = HousePuzzle(s)
		return s


	# print H state
def Hdisplay(state):
	g = list(state)
	for i in range(9):
		if g[i] == 0:
			g[i] = "*"

	for i in range(3):	
		print(g[i], end=" ")
	print()
	for i in range(3,6):
		print(g[i],end=" ")
	print()
	for i in range(6,9):
		print(g[i],end=" ")
	print()
	for i in range(9,12):
		print(g[i],end=" ")
	print()


def Hmanhattan(node):
	state = node.state
	index_goal = {-1:[0,1], -2:[3,0], -3:[3,2], 0:[3,1], 1:[0,0], 2:[0,2], 3:[1,0], 4:[1,1], 5:[1,2], 6:[2,0], 7:[2,1], 8:[2,2]}
	index_state = {}
	index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2], [3,0], [3,1], [3,2]]
	x, y = 0, 0
	for i in range(len(state)):
		index_state[state[i]] = index[i]
	mhd = 0
	for i in range(-3,9):
		for j in range(2):
			mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
	return mhd


def HMaxA(ep):
	node = Node(ep.initial)
	if ep.h(node) > Hmanhattan(node):
		return True
	else:
		return False


class HousePuzzle(Problem):

    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board,
    where one of the squares is a blank. A state is represented as a tuple of length 12,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """
 
    def __init__(self, initial, goal=(1,2,-1,-2,3,4,5,6,-3,7,8,0)):
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

        if index_blank_square == 0:
        	possible_actions.remove('UP')
        	possible_actions.remove('LEFT')
        if (index_blank_square == 1) | (index_blank_square == 7):
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if (index_blank_square == 4) | (index_blank_square == 9):
        	possible_actions.remove('DOWN')
        	possible_actions.remove('LEFT')
        if index_blank_square == 6:
        	possible_actions.remove('UP')
        if index_blank_square == 10:
        	possible_actions.remove('DOWN')
        if index_blank_square == 11:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

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
        l = []
        ll = [0,1,2,3,4,5,6,7,8]
        ll[0] = state[0]
        ll[1] = state[1]
        ll[2] = state[4]
        ll[3] = state[5]
        ll[4] = state[6]
        ll[5] = state[7]
        ll[6] = state[9]
        ll[7] = state[10]
        ll[8] = state[11]
        if i in range(len(ll)):
            for j in range(i+1, len(ll)):
                if(ll[i] > ll[j]) and ll[i] != 0 and ll[j] != 0:
                    inversion += 1
        return inversion % 2 == 0
    
    def h(self, node):
        """Return the heuristic value for a given state. Default heuristic function used is h(n) = number of misplaced tiles """
    	return sum(s != g for (s, g) in zip(node.state, self.goal))


#main
#8-puzzle

# A*-search using the misplaced tile heuristic 
print ("=======================================================================")
print ("8_PUzzle Misplaced Tile Heuristic")

ep = EightPuzzle(make_rand_8puzzle())

start_time = time.time()								    # running time
Misplace_node = astar_search(ep, ep.h)
elapsed_time = time.time() - start_time
print(f'time: {elapsed_time}')
time1 = elapsed_time
print ("Length: ", Misplace_node[0].path_cost)				# Length

print ("Remove: ", Misplace_node[1])						# Number of removed f


#A*-search using Manhattan distance hueristic
print ("=======================================================================")
print ("8_PUzzle Manhattan Tile Heuristic")

start_time = time.time()									# running time
Manhattan_node = astar_search(ep, manhattan)
elapsed_time = time.time() - start_time
print(f'time: {elapsed_time}')
time2 = elapsed_time
print ("The Length: ", Manhattan_node[0].path_cost)			# Length

print ("Remove: ", Manhattan_node[1])						# Number of removed 


#A*-search using max of the misplaced tile heristic and the Manhattan distance heurstic 
print ("=======================================================================")
print ("8_PUzzle Max of Misplaced Tile Hueristic and Manhattan Tile Hueristic")

if MaxA(ep) == True:
	start_time = time.time()									# running time
	Misplace_node = astar_search(ep, ep.h)
	elapsed_time = time.time() - start_time
	print(f'time: {elapsed_time}')

	print ("Length: ", Misplace_node[0].path_cost)				# Length

	print ("Remove: ", Misplace_node[1])						# Number of removed 
else:
	start_time = time.time()									# unning time
	Manhattan_node = astar_search(ep, manhattan)
	elapsed_time = time.time() - start_time
	print(f'time: {elapsed_time}')

	print ("The Length: ", Manhattan_node[0].path_cost)			# Length

	print ("Remove: ", Manhattan_node[1])						# Number of removed 



#HousePuzzle

#A*-search using Manhattan distance hueristic
print ("=======================================================================")
print ("H_Puzzle Misplaced Tile Heuristic")

Hp = HousePuzzle(make_rand_HousePuzzle())
start_time = time.time()									# running time
HMisplace_node = astar_search(Hp, Hp.h)
elapsed_time = time.time() - start_time
print(f'time: {elapsed_time}')
print ("Length: ", HMisplace_node[0].path_cost)				# Length
print ("Remove: ", HMisplace_node[1])						# Number of removed 

#A*-search using Manhattan distance hueristic
print ("=======================================================================")
print ("H_PUzzle Manhattan Tile Heuristic")

start_time = time.time()										# running time
HManhattan_node = astar_search(Hp, Hmanhattan)
elapsed_time = time.time() - start_time
print(f'time: {elapsed_time}')
time2 = elapsed_time
print ("The Length: ", HManhattan_node[0].path_cost)			# Length

print ("Remove: ", HManhattan_node[1])							# Number of removed 

#A*-search using max of the misplaced tile heristic and the Manhattan distance heurstic 
print ("=======================================================================")
print ("H_PUzzle Max of Misplaced Tile Hueristic and Manhattan Tile Hueristic")

if HMaxA(Hp) == True:
	start_time = time.time()									#  running time
	Misplace_node = astar_search(Hp, Hp.h)
	elapsed_time = time.time() - start_time
	print (f'time: {elapsed_time}')

	print ("Length: ", HMisplace_node[0].path_cost)				# Length

	print ("Remove: ", HMisplace_node[1])						# Number of removed 
else:
	start_time = time.time()									# running time
	Manhattan_node = astar_search(Hp, Hmanhattan)
	elapsed_time = time.time() - start_time
	print(f'time: {elapsed_time}')

	print ("The Length: ", HManhattan_node[0].path_cost)		# Length

	print ("Remove: ", HManhattan_node[1])						# Number of removed




















# ...