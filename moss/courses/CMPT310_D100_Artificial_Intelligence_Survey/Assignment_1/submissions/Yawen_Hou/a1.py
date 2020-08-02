# a1.py
from search import *
import time
import random

# Question 1
def make_rand_8puzzle(): 
	number_List = [0,1,2,3,4,5,6,7,8]
	while True:
		random.shuffle(number_List)
		initial_State = tuple(number_List)
		new_List = EightPuzzle(initial_State)
		if new_List.check_solvability(initial_State) == True:
			return new_List
		else:
			continue

def display(state):
	index = 0

	for i in range(3):
		for j in range(3):
			if state[index] == 0:
				print("*", end = '')
			else:
				print(state[index], end = '')
			index = index + 1

		print("\n", end = '')

	return


# Question 2

## create n 8_puzzle instances
def create_8puzzle_instances(n):
	instances_List = []
	for i in range(n):
		instances_List.append(make_rand_8puzzle())
	return instances_List

def misplaced_tile_heuristic(node):
	goal_List = [1,2,3,4,5,6,7,8,0]
	goal = tuple(goal_List)
	return sum(s != 0 and s != g for (s, g) in zip(node.state, goal))

def manhattan_heuristic(node):
	node_state = node.state
	index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
	index_state = {}
	index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
	x, y = 0, 0

	for i in range(len(node_state)):
		index_state[node_state[i]] = index[i]

	manhattan = 0

	for i in range(8):
		for j in range(2):
			manhattan = abs(index_goal[i+1][j] - index_state[i+1][j]) + manhattan

	return manhattan

def compute_max_8puzzle(node):
	return max(misplaced_tile_heuristic(node),manhattan_heuristic(node))


# adapted from search.py from https://github.com/aimacode/aima-python
def astar_search(problem, h=None):
	"""A* search is best-first graph search with f(n) = g(n)+h(n).
	You need to specify the h function when you call astar_search, or
	else in your Problem subclass."""
	h = memoize(h or problem.h, 'h')
	return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

# modified and adapted from search.py from https://github.com/aimacode/aima-python
# Added a counter to count the number of nodes popped.
def best_first_graph_search(problem, f):
	"""Search the nodes with the lowest f scores first.
	You specify the function f(node) that you want to minimize; for example,
	if f is a heuristic estimate to the goal, then we have greedy best
	first search; if f is node.depth then we have breadth-first search.
	There is a subtlety: the line "f = memoize(f, 'f')" means that the f
	values will be cached on the nodes as they are computed. So after doing
	a best first search you can examine the f values of the path returned."""
	counter = 0
	f = memoize(f, 'f')
	node = Node(problem.initial)
	frontier = PriorityQueue('min', f)
	frontier.append(node)
	explored = set()
	while frontier:
		node = frontier.pop()
		counter += 1
		if problem.goal_test(node.state):
			return node, counter
		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				frontier.append(child)
			elif child in frontier:
				if f(child) < frontier[child]:
					del frontier[child]
					frontier.append(child)
	return None





def compare_8puzzle():

	# create a list of 10 instances
	problemList = create_8puzzle_instances(10)
	print("8_puzzles to solve are: ")
	for i in range(10):
		print(problemList[i].initial)

	# initialize lists
	ASTARruntime = []
	MANruntime = []
	MAXruntime = []

	ASTARsolutionLength = []
	MANsolutionLength = []
	MAXsolutionLength = []

	ASTARnumNodesRemoved = []
	MANnumNodesRemoved = []
	MAXnumNodesRemoved = []


	# comparing . . .
	print('***********Misplaced tile heuristic***********')
	for i in range(10):
		start_time = time.time()
		res, numNodesRmved = astar_search(problemList[i], misplaced_tile_heuristic)
		elapsed_time = time.time() - start_time
		ASTARruntime.append(elapsed_time)
		ASTARsolutionLength.append(res.path_cost)
		ASTARnumNodesRemoved.append(numNodesRmved)
	print("Misplacended tile heuristic runtime is: ")
	print(ASTARruntime)
	print("Misplaced tile heuristic path cost is: ")
	print(ASTARsolutionLength)
	print("Misplaced tile heuristic number of nodes removed is: ")
	print(ASTARnumNodesRemoved)


	print('\n\n')
	print('***********Manhattan heuristic************')
	for i in range(10):
		start_time = time.time()
		res, numNodesRmved = astar_search(problemList[i], manhattan_heuristic)
		elapsed_time = time.time() - start_time
		MANruntime.append(elapsed_time)
		MANsolutionLength.append(res.path_cost)
		MANnumNodesRemoved.append(numNodesRmved)
	print("Manhattan heuristic runtime is: ")
	print(MANruntime)
	print("Manhattan heuristic path cost is: ")
	print(MANsolutionLength)
	print("Manhattan heuristic number of nodes removed is: ")
	print(MANnumNodesRemoved)

	print('\n\n')
	print('************Max heuristic************')
	for i in range(10):
		start_time = time.time()
		res, numNodesRmved = astar_search(problemList[i], compute_max_8puzzle)
		elapsed_time = time.time() - start_time
		MAXruntime.append(elapsed_time)
		MAXsolutionLength.append(res.path_cost)
		MAXnumNodesRemoved.append(numNodesRmved)
	print("Max heuristic runtime is: ")
	print(MAXruntime)
	print("Max heuristic path cost is: ")
	print(MAXsolutionLength)
	print("Max heuristic number of nodes removed is: ")
	print(MAXnumNodesRemoved)








# Question 3
# The House-Puzzle class

class DuckPuzzle(Problem):

	def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
		""" Define goal state and initialize a problem """

		self.goal = goal
		Problem.__init__(self, initial, goal)

	def find_blank_square(self, state):
		""" Return the index of the blank square in a given state"""

		return state.index(0)


	def actions(self,state):
		""" Return the actions that can be executed in the given state.
		The result would be a list, since there are only four possible actions
		in any given state of the environment """

		possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
		index_blank_square = self.find_blank_square(state)

		if index_blank_square == 0:
			possible_actions.remove('UP')
			possible_actions.remove('LEFT')
		elif index_blank_square == 1:
			possible_actions.remove('UP')
			possible_actions.remove('RIGHT')
		elif index_blank_square == 2:
			possible_actions.remove('DOWN')
			possible_actions.remove('LEFT')
		elif index_blank_square == 4:
			possible_actions.remove('UP')
		elif index_blank_square == 5:
			possible_actions.remove('UP')
			possible_actions.remove('RIGHT')
		elif index_blank_square == 6:
			possible_actions.remove('DOWN')
			possible_actions.remove('LEFT')
		elif index_blank_square == 7:
			possible_actions.remove('DOWN')
		elif index_blank_square == 8:
			possible_actions.remove('DOWN')
			possible_actions.remove("RIGHT")

		return possible_actions

	def result(self, state, action):
		""" Given state and action, return a new state that is the result of the action.
		Action is assumed to be a valid action in the state """

		# blank is the index of the blank square
		blank = self.find_blank_square(state)
		new_state = list(state)

		delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}

		# neighbors
		if (blank == 0 and action == 'DOWN'): 
			neighbor = 2
		elif(blank == 1 and action == 'DOWN'): 
			neighbor = 3
		elif(blank == 2 and action == 'UP'): 
			neighbor = 0
		elif(blank == 3 and action == 'UP'): 
			neighbor = 1
		else: 
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

		return sum(s != 0 and s != g for (s, g) in zip(node.state, self.goal))

#discussed with friend
def make_rand_Duckpuzzle(): 

	state = [1,2,3,4,5,6,7,8,0]
	new = DuckPuzzle(state)
	for i in range(500):
		# random.shuffle(numList)
		# initialState = tuple(numList)
		# new = DuckPuzzle(initialState)
	# new = DuckPuzzle(numList)
	# for i in range(1000):
	# 	actions = new.actions(numList)
	# 	numList = new.result(numList, random.choice(actions))
		# if new.result(numList, random.choice(numList)) == (1,2,3,4,5,6,7,8,0): 
		# 	return new
		# else: 
		# 	continue
		action = new.actions(state)
		rand = np.random.randint(0,len(action))
		state = new.result(state,action[rand])
	new = DuckPuzzle(state)
	return new

def display_Duckpuzzle(state):  #displays the Ypuzzle state in the actual game form

	# print first row
	if state[0] == 0:
		print('*', end = ' ')
	else: 
		print(state[0], end = ' ')

	# print second element
	if state[1] == 0:
		print('*')
	else: 
		print(state[1])
	print('\n',end = '')

	# print second row
	index = 2
	for i in range(4):
		if state[index] == 0:
			print('*', end = ' ')
		else: 
			print(state[index], end = ' ')
		index = index + 1
	print('\n', end = '')
	print(' ', end = ' ')

	# print last row
	index = 6
	for i in range(3):
		if state[index] == 0:
			print('*', end = ' ')
		else: 
			print(state[index], end = ' ')
		index = index + 1

	# # print the last element
	# if state[8] == 0:
	# 	print('  *')
	# else: 
	# 	print('  ' + str(state[8]))
	# return





def create_Duckpuzzle_instance(n): 
	#create n instances of Duckpuzzle
	problemList = []
	for i in range(n):
		problemList.append(make_rand_Duckpuzzle())
	return problemList

def misplaced_tile_heuristic_Duck(node):
	goalList = [1,2,3,4,5,6,7,8,0]
	goal = tuple(goalList)
	return sum(s != 0 and s != g for (s, g) in zip(node.state, goal))

def manhattan_heuristic_Duck(node): 
	
	state = node.state
	index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
	index_state = {}
	index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]
	x, y = 0, 0

	for i in range(len(state)):

		index_state[state[i]] = index[i]

	manhattan = 0

	for i in range(8):
		for j in range(2):
			mhd = abs(index_goal[i+1][j] - index_state[i+1][j]) + manhattan

	return manhattan

def max_Duckpuzzle(node): 
	#max heuristic function that takes the max h value from the first two functions
	return max(manhattan_heuristic_Duck(node), misplaced_tile_heuristic_Duck(node))

# # adapted from search.py from https://github.com/aimacode/aima-python
# def astar_search(problem, h=None):
# 	"""A* search is best-first graph search with f(n) = g(n)+h(n).
# 	You need to specify the h function when you call astar_search, or
# 	else in your Problem subclass."""
# 	h = memoize(h or problem.h, 'h')
# 	return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

# # modified and adapted from search.py from https://github.com/aimacode/aima-python
# # Added a counter to count the number of nodes popped.
# def best_first_graph_search(problem, f):
# 	"""Search the nodes with the lowest f scores first.
# 	You specify the function f(node) that you want to minimize; for example,
# 	if f is a heuristic estimate to the goal, then we have greedy best
# 	first search; if f is node.depth then we have breadth-first search.
# 	There is a subtlety: the line "f = memoize(f, 'f')" means that the f
# 	values will be cached on the nodes as they are computed. So after doing
# 	a best first search you can examine the f values of the path returned."""
# 	counter = 0
# 	f = memoize(f, 'f')
# 	node = Node(problem.initial)
# 	frontier = PriorityQueue('min', f)
# 	frontier.append(node)
# 	explored = set()
# 	while frontier:
# 		node = frontier.pop()
# 		counter += 1
# 		if problem.goal_test(node.state):
# 			return node, counter
# 		explored.add(node.state)
# 		for child in node.expand(problem):
# 			if child.state not in explored and child not in frontier:
# 				frontier.append(child)
# 			elif child in frontier:
# 				if f(child) < frontier[child]:
# 					del frontier[child]
# 					frontier.append(child)
# 	return None


def compare_Duckpuzzle():

	#create a list of 10 instances
	problemList = create_Duckpuzzle_instance(10)
	print("House_puzzles to solve are: ")
	for i in range(10):
		print(problemList[i].initial)

	#initialize lists to store results
	ASTARruntime = []
	MANruntime = []
	MAXruntime = []

	ASTARsolutionLength = []
	MANsolutionLength = []
	MAXsolutionLength = []

	ASTARnumNodesRemoved = []
	MANnumNodesRemoved = []
	MAXnumNodesRemoved = []

	#comparing . . .
	print('**********Misplaced tile heuristic**********')
	for i in range(10):
		start_time = time.time()
		res, numNodesRmved = astar_search(problemList[i],misplaced_tile_heuristic_Duck)
		elapsed_time = time.time() - start_time
		ASTARruntime.append(elapsed_time)
		ASTARsolutionLength.append(res.path_cost)
		ASTARnumNodesRemoved.append(numNodesRmved)
	print("Misplaced tile heuristic runtime is: ")
	print(ASTARruntime)
	print("Misplaced tile heuristic path cost is: ")
	print(ASTARsolutionLength)
	print("Misplaced tile heuristic number of nodes removed is: ")
	print(ASTARnumNodesRemoved)


	print('\n\n')
	print('**********Manhattan heuristic**********')
	for i in range(10):
		start_time = time.time()
		res, numNodesRmved = astar_search(problemList[i], manhattan_heuristic_Duck)
		elapsed_time = time.time() - start_time
		MANruntime.append(elapsed_time)
		MANsolutionLength.append(res.path_cost)
		MANnumNodesRemoved.append(numNodesRmved)
	print("Manhattan heuristic runtime is: ")
	print(MANruntime)
	print("Manhattan heuristic path cost is: ")
	print(MANsolutionLength)
	print("Manhattan heuristic number of nodes removed is: ")
	print(MANnumNodesRemoved)

	print('\n\n')
	print('**********Max heuristic**********')
	for i in range(10):
		start_time = time.time()
		res, numNodesRmved = astar_search(problemList[i], max_Duckpuzzle)
		elapsed_time = time.time() - start_time
		MAXruntime.append(elapsed_time)
		MAXsolutionLength.append(res.path_cost)
		MAXnumNodesRemoved.append(numNodesRmved)
	print("Max heuristic runtime is: ")
	print(MAXruntime)
	print("Max heuristic path cost is: ")
	print(MAXsolutionLength)
	print("Max heuristic number of nodes removed is: ")
	print(MAXnumNodesRemoved)






# def main():
if __name__ == '__main__':
	print("-----------FOR 8-PUZZLE: -------------\n")
	compare_8puzzle()
	print("\n\n")
	print("-----------FOR House_PUZZLE: ------------\n")
	compare_Duckpuzzle()

# 	return

# if __name__ == '__main__':
# 	main()

