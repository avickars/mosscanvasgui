from search import *
from random import shuffle
import time
# import json

# Default misplaced heuristics without 0 for admissible heuristic
def hEight(node):
		""" Return the heuristic value for a given state. Default heuristic function used is 
		h(n) = number of misplaced tiles """
		# don't include 0 as misplaced, otherwise not admissible
		return sum(s != g and s!= 0 for (s, g) in zip(node.state, EightPuzzle(node.state).goal))

def hDuck(node):
		""" Return the heuristic value for a given state. Default heuristic function used is 
		h(n) = number of misplaced tiles """
		# don't include 0 as misplaced, otherwise not admissible
		return sum(s != g and s!= 0 for (s, g) in zip(node.state, DuckPuzzle(node.state).goal))

# Modified from search.py
def astar_search(problem, h=None, display=False):
	"""A* search is best-first graph search with f(n) = g(n)+h(n).
	You need to specify the h function when you call astar_search, or
	else in your Problem subclass."""
	h = memoize(h or problem.h, 'h')
	return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# Modified from search.py
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
		removed = removed + 1
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
	return None, removed

#_____________________________________________________________________________
# Question 1: Helper Functions
def make_rand_8puzzle():
	initState = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	shuffle(initState)
	state = EightPuzzle(tuple(initState))
	while (not state.check_solvability(initState)):
		shuffle(initState)
	state = EightPuzzle(tuple(initState))
	display(initState)
	return state

def display(state):
	for i, var in enumerate(state, start=1):
		if (var != 0):
			print(var, end=" ")
		else:
			print("*", end=" ")
		if (i % 3 == 0):
			print()
	print()

#_____________________________________________________________________________
# Question 2
def manhattan(node):
	state = node.state
	index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
	index_state = {}
	index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

	for i in range(len(state)):
		index_state[state[i]] = index[i]

	mhd = 0

	for i in range(1, 9):
		for j in range(2):
			mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd 
	return mhd

def manhattan_max(node):
	puzzle =  EightPuzzle(node.state)
	return max(manhattan(node), hEight(node))	

result = {}
def get8Puzzle():
	res = []
	for i in range(0, 10):
		state = make_rand_8puzzle()
		out = {}
		out["Trial"] = i+1
		out["State"] = str(state.initial)
		start_time = time.time()
		node, removed = astar_search(state, hEight, display=False)
		elapsed_time = time.time() - start_time
		out["length_h"] = len(node.solution())
		out["removed_h"] = removed
		out["h_time"] = elapsed_time
		start_time = time.time()
		node, removed = astar_search(state, manhattan, display=False)
		elapsed_time = time.time() - start_time
		out["length_manhattan"] = len(node.solution())
		out["removed_manhattan"] = removed
		out["time_manhattan"] = elapsed_time
		start_time = time.time()
		node, removed = astar_search(state, manhattan_max, display=False)
		elapsed_time = time.time() - start_time
		out["length_manhattan_max"] = len(node.solution())
		out["removed_manhattan_max"] = removed
		out["time_manhattan_max"] = elapsed_time
		res.append(out)
	return res
#_____________________________________________________________________________
# For Question 3, modified from search.py's EightPuzzle class
class DuckPuzzle(Problem):
	""" The problem of sliding tiles numbered from 1 to 8 on a duck board, where one of the
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
		if index_blank_square == 1 or index_blank_square == 5:
			possible_actions.remove('UP')
			possible_actions.remove('RIGHT')
		if index_blank_square == 2 or index_blank_square == 6:
			possible_actions.remove('LEFT')
			possible_actions.remove('DOWN')
		if index_blank_square == 4:
			possible_actions.remove('UP')
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

		if blank == 1:
			delta = {'UP': 0, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 0}
			neighbor = blank + delta[action]
			new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
		if blank == 2:
			delta = {'UP': -2, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}
			neighbor = blank + delta[action]
			new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
		if blank == 3:
			delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
			neighbor = blank + delta[action]
			new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
		if blank == 4:
			delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
			neighbor = blank + delta[action]
			new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
		if blank == 5:
			delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 0}
			neighbor = blank + delta[action]
			new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
		if blank == 6:
			delta = {'UP': -3, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}
			neighbor = blank + delta[action]
			new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
		if blank == 7:
			delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
			neighbor = blank + delta[action]
			new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
		if blank == 8:
			delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 0}
			neighbor = blank + delta[action]
			new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
		if blank == 0:
			delta = {'UP': 0, 'DOWN': 2, 'LEFT': 0, 'RIGHT': 1}
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

#_____________________________________________________________________________
# Question 3
def make_rand_Duckpuzzle():
	goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
	duck = DuckPuzzle(tuple(goal))
	for i in range(0, 10000): # Guaranteed solvability, starts from goal
		action = duck.actions(goal)
		goal = duck.result(goal, random.choice(action))
	duck = DuckPuzzle(tuple(goal))
	displayDuck(goal)
	return duck

def displayDuck(state):
	for i, var in enumerate(state, start=1):
		if (i <= 2):
			if (var == 0):
				print("*", end=" ")
			else:
				print(var, end=" ")
			if (i == 2):
				print()
		elif (i > 6):
			if (i == 7):
				print(end="  ")
			if (var == 0):
				print("*", end=" ")
			else:
				print(var, end=" ")
		else:
			if (var == 0):
				print("*", end=" ")
			else:
				print(var, end=" ")
			if (i == 6):
				print()
	print("\n")

def manhattanDuck(node):
	state = node.state
	index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
	index_state = {}
	index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]

	for i in range(len(state)):
		index_state[state[i]] = index[i]

	mhd = 0

	for i in range(1, 9):
		for j in range(2):
			mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd 
	return mhd

def manhattan_maxDuck(node):
	puzzle =  DuckPuzzle(node.state)
	return max(manhattanDuck(node), hDuck(node))

# ______________________________________________________________________________
# Question 3
def getDuckPuzzle():
	res = []
	for i in range(0, 10):
		state = make_rand_Duckpuzzle()
		out = {}
		out["Trial"] = i+1
		out["State"] = str(state.initial)
		start_time = time.time()
		node, removed = astar_search(state, hDuck, display=False)
		elapsed_time = time.time() - start_time
		out["length_h"] = len(node.solution())
		out["removed_h"] = removed
		out["h_time"] = elapsed_time
		start_time = time.time()
		node, removed = astar_search(state, manhattanDuck, display=False)
		elapsed_time = time.time() - start_time
		out["length_manhattanDuck"] = len(node.solution())
		out["removed_manhattanDuck"] = removed
		out["time_manhattanDuck"] = elapsed_time
		start_time = time.time()
		node, removed = astar_search(state, manhattan_maxDuck, display=False)
		elapsed_time = time.time() - start_time
		out["length_manhattan_maxDuck"] = len(node.solution())
		out["removed_manhattan_maxDuck"] = removed
		out["time_manhattan_maxDuck"] = elapsed_time
		res.append(out)
	return res

# ______________________________________________________________________________

def main():
	result["Eight_Puzzle"] = get8Puzzle()
	result["Duck_Puzzle"] = getDuckPuzzle()
	
	# use JSON to convert to CSV
	# with open('a1.json', 'w') as fp:
	# 	json.dump(result, fp) 
	# print(result)

if __name__ == "__main__":
	main()