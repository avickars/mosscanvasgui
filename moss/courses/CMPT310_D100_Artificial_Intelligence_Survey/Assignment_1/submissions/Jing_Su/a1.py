import random
from search import*
import time

#################
#				#
#   QUESTION 1	#
#				#
#################
def make_rand_8puzzle():
	"""Generate a sequence representing random solvable 3*3 puzzletiles"""
	randomlist=random.sample(range(0,9),9)
	randomt=tuple(randomlist)
	e=EightPuzzle(randomt)
	while e.check_solvability(randomt)==0:
		randomt=tuple(random.sample(range(0,9),9))
		e=EightPuzzle(randomt)

	return randomt

def display(state):
	for idx,val in enumerate(state):

		if val==0:
			print('*',end="")
		else:
			print(val,end="")
		if idx%3==2:
			print('\n',end="")
		else:
			print(' ',end="")	



#########################################
#										#
#   DUCK_PUZZLE VERSION OF QUESTION 1	#
#										#
#########################################

def make_rand_8puzzle_duck():
	"""Generate a sequence representing random solvable 8 duck puzzle, The method
	used here is startring from the goal and then making random moves to it, so 
	the solvability is guaranteed"""
	randomt = (1,2,3,4,5,6,7,8,0)
	duckpuzzle = DuckPuzzle(randomt)
	scope = random.randint(0,100)
	for i in range(scope):
		randomt = duckpuzzle.result(randomt,random.choice(duckpuzzle.actions(randomt)))
	return randomt



def display_duck(state):
	for idx,val in enumerate(state):
	        if idx==6:
	            print('  ',end="")
	        if val==0:
	            print('*',end="")
	        else :
	            print(val,end="")
	        if idx==1 or idx==5 or idx ==8:
	            print('\n',end="")
	        else:
	            print(' ',end="")
	"""Display the sequence representing 8 duck puzzle as they are in a real duck board"""
	
     


#########################################
#										#
#  MODIFIED A* SEARCH FOR QUESTION 2,3	#
#										#
#########################################

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
	removed = 0
	while frontier:
		node = frontier.pop()
		removed = removed +1
		if problem.goal_test(node.state):
			if display:
				print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
				
			return node, removed
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




#############################################################
#															#
#   8_PUZZLE CLASS(Manhattan and max function added 		#
#					as member function)  					#
#															#
#############################################################

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

	def manhattan(self,node):
		sum=0
		for idx,val in enumerate(node.state):
			if val!=0:
				"""We don't include 0 since if there is just last move to make to achive the goal
				,manhattan sum will be two(one for the blank and one for its final neighbor),
				which overestimates the cost(it should be less than 1), so the admissibility
				is not maintained"""
				step=(val-idx-1)
				
				move=((abs(step))%3) +int((abs(step))/3)
				if idx==2 or idx==5:
					if step==1 or step==4:
						move = move+2
				if idx==3 or idx==6:
					if step==-1 or step==-4:
						move = move +2
			   
				sum = sum + move
		return sum
# ____
	def maxh(self,node):
		return max(self.h(node),self.manhattan(node))


#########################################
#										#
#   DUCK_PUZZLE CLASS  QUESTION 3		#
#										#
#########################################


class DuckPuzzle(Problem):
	""" The problem of sliding tiles numbered from 1 to 8 on a duck board, where one of the
	squares is a blank. A state is represented as a tuple of length 9, where  element at
	index i represents the tile number  at index i (0 if it's an empty square) """
	def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)): 
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

		if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
			possible_actions.remove('LEFT')
		if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
			possible_actions.remove('UP')
		if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
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

		delta = {'LEFT': -1, 'RIGHT': 1}
		neighbor = blank
		if action == 'UP':
			if blank == 2 or blank == 3:
				neighbor = blank -2
			else:
				neighbor = blank -3
		elif action == 'DOWN':
			if blank < 2:
				neighbor = blank + 2
			else:
				neighbor = blank + 3
		else:
			neighbor = blank + delta[action]

		
		new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

		return tuple(new_state)

	def goal_test(self, state):
		""" Given a state, return True if state is a goal state or False, otherwise """

		return state == self.goal

	

	def h(self, node):
		""" Return the heuristic value for a given state. Default heuristic function used is 
		h(n) = number of misplaced tiles """

		return sum(s != g for (s, g) in zip(node.state, self.goal))

	def manhattan(self,node):
		sum=0
		match=[0, 0, 1, 4, 5, 6, 7, 9, 10, 11]
		for idx,val in enumerate(node.state):
			"""We don't include 0 since if there is just last move to make to achive the goal
				,manhattan sum will be two(one for the blank and one for its final neighbor),
				which overestimates the cost(it should be less than 1), so the admissibility
				is not maintained"""
			if val!= 0:
				move = abs((match[idx+1]%4) - (match[val]%4)) + abs(int(match[idx+1]/4) - int(match[val]/4))
				   
				sum = sum + move
		return sum

	def maxh(self,node):
		return max(self.h(node),self.manhattan(node))

#########################################
#										#
#   COMPARISON OF THREE ALGORITHMS		#
#			FOR 8 PUZZLE				#
#										#
#########################################

#create 10 random puzzles
instance = []
for i in range(10):
	ini_state = make_rand_8puzzle()
	instance.append(ini_state)


##############TEST FOR MISPLACED TILES###############
print("---------------EIGHT PUZZLE TEST FOR MISPLACED TILES-------------")
for ini_state in instance:
	display(ini_state)
	start_time = time.time()
	eight_puzzle = EightPuzzle(ini_state)
	node,removed = astar_search(eight_puzzle,eight_puzzle.h, 1)
	elapsed_time=time.time() - start_time
	print(f'elapsed time(in seconds):{elapsed_time}s')
	path = node.path()
	length = len(path)-1
	print(f'tile length: {length}')
	print(f'nodes removed:{removed}\n')

print("---------------EIGHT PUZZLE TEST FOR MANHATTAN-------------")
##############TEST FOR MANHATTAN TILES###############
for ini_state in instance:
	display(ini_state)
	start_time = time.time()
	eight_puzzle = EightPuzzle(ini_state)
	node,removed = astar_search(eight_puzzle,eight_puzzle.manhattan, 1)
	elapsed_time=time.time() - start_time
	print(f'elapsed time(in seconds):{elapsed_time}s')
	path = node.path()
	length = len(path)-1
	print(f'tile length: {length}')
	print(f'nodes removed:{removed}\n')

print("---------------EIGHT PUZZLE TEST FOR MAXH-------------")
##############TEST FOR MAX###############
for ini_state in instance:
	display(ini_state)
	start_time = time.time()
	eight_puzzle = EightPuzzle(ini_state)
	node,removed = astar_search(eight_puzzle,eight_puzzle.maxh, 1)
	elapsed_time=time.time() - start_time
	print(f'elapsed time(in seconds):{elapsed_time}s')
	path = node.path()
	length = len(path)-1
	print(f'tile length: {length}')
	print(f'nodes removed:{removed}\n')

#########################################
#										#
#   COMPARISON OF THREE ALGORITHMS		#
#			FOR DUCK PUZZLE				#
#										#
#########################################

#create 10 random puzzles
instance = []
for i in range(10):
	ini_state = make_rand_8puzzle_duck()
	instance.append(ini_state)

print("---------------DUCK PUZZLE TEST FOR MISPLACED TILES-------------")
##############TEST FOR MISPLACED TILES###############
for ini_state in instance:
	display_duck(ini_state)
	start_time = time.time()
	duck_puzzle = DuckPuzzle(ini_state)
	node,removed = astar_search(duck_puzzle,duck_puzzle.h, 1)
	elapsed_time=time.time() - start_time
	print(f'elapsed time(in seconds):{elapsed_time}s')
	path = node.path()
	length = len(path)-1
	print(f'tile length: {length}')
	print(f'nodes removed:{removed}\n')

print("---------------DUCK PUZZLE TEST FOR MANHATTAN-------------")
##############TEST FOR MANHATTAN TILES###############
for ini_state in instance:
	display_duck(ini_state)
	start_time = time.time()
	duck_puzzle = DuckPuzzle(ini_state)
	node,removed = astar_search(duck_puzzle,duck_puzzle.manhattan, 1)
	elapsed_time=time.time() - start_time
	print(f'elapsed time(in seconds):{elapsed_time}s')
	path = node.path()
	length = len(path)-1
	print(f'tile length: {length}')
	print(f'nodes removed:{removed}\n')

print("---------------DUCK PUZZLE TEST FOR MAXH-------------")
##############TEST FOR MAX###############
for ini_state in instance:
	display_duck(ini_state)
	start_time = time.time()
	duck_puzzle = DuckPuzzle(ini_state)
	node,removed = astar_search(duck_puzzle,duck_puzzle.maxh, 1)
	elapsed_time=time.time() - start_time
	print(f'elapsed time(in seconds):{elapsed_time}s')
	path = node.path()
	length = len(path)-1
	print(f'tile length: {length}')
	print(f'nodes removed:{removed}\n')