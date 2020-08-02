#a1

from search import *
import random
import time

# Functions imported from search.py:
def modified_best_first_graph_search(problem, f, display=False):
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
	frontier_popped = 0
	while frontier:
		node = frontier.pop()
		frontier_popped += 1
		if problem.goal_test(node.state):
			if display:
				print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
			node.frontier_popped = frontier_popped
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

def modified_astar_search(problem, h=None, display=False):
	"""A* search is best-first graph search with f(n) = g(n)+h(n).
	You need to specify the h function when you call astar_search, or
	else in your Problem subclass."""
	h = memoize(h or problem.h, 'h')
	return modified_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# ______________________________________________________________________________

# Question 1: Helper Functions
def make_rand_8puzzle():
	while True:
		initial_state = tuple(random.sample(list(range(0,9)), 9))
		puzzle = EightPuzzle(initial_state)
		solvable = puzzle.check_solvability(initial_state)
		if solvable:
			display(initial_state)
			return puzzle

def display(state):
	count = 0
	for i in state:
		if (count == 3):
			count = 0
			print(' ')
		if i == 0:
			print('*', end=' ')
		else:
			print(i, end=' ')	
		count += 1 
	print(' ')

# Question 2a: Manhattan distance heuristic for 8puzzle
def manhattan_heuristic_8puzzle(node):
	goal = (1,2,3,4,5,6,7,8,0)
	state = node.state
	manhattan_dist = 0
	for i in state:
		if i != 0: # and i != goal[state.index(i)]
			horizontal_dist = abs(state.index(i)%3 - goal.index(i)%3)
			vertical_dist = abs(int(state.index(i)/3) - int(goal.index(i)/3))
			manhattan_dist += (horizontal_dist + vertical_dist)
			# print(i, horizontal_dist, vertical_dist, manhattan_dist)
	return manhattan_dist

# Qusetion 2b: returns max of misplaces_tile_heuristic and manhattan_heuristic for 8 puzzle
def find_max_heuristic_value_8puzzle(node):
	puzzle = EightPuzzle(node.state)
	misplaces_tile_heuristic_value = puzzle.h(node)
	manhattan_heuristic_value = manhattan_heuristic_8puzzle(node)
	return max(misplaces_tile_heuristic_value, manhattan_heuristic_value)

# ______________________________________________________________________________

# Question 3a: DuckPuzzle class
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

		if index_blank_square in [0,1,4,5]:
			possible_actions.remove('UP')
		if index_blank_square in [2,6,7,8]:
			possible_actions.remove('DOWN')
		if index_blank_square in [0,2,6]:
			possible_actions.remove('LEFT')
		if index_blank_square in [2,5,8]:
			possible_actions.remove('RIGHT')

		return possible_actions

	def result(self, state, action):
		""" Given state and action, return a new state that is the result of the action.
		Action is assumed to be a valid action in the state """

		# blank is the index of the blank square
		blank = self.find_blank_square(state)
		new_state = list(state)

		delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}

		if blank in [3]:
			delta['DOWN'] = 3
			delta['UP'] = -2
		if blank in [4,5]:
			delta['DOWN'] = 3
		if blank in [6,7,8]:
			delta['UP'] = -3

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

# Question 3b: Helper Functions for Duck Puzzle
def make_rand_duck_puzzle():
	initial_state = (1,2,3,4,5,6,7,8,0)
	duck_puzzle = DuckPuzzle(initial_state)
	random_unsolved_state = initial_state
	for i in range(random.randint(1, 10000)):
		possible_actions = duck_puzzle.actions(random_unsolved_state)
		random_legal_action = random.choice(possible_actions)
		random_unsolved_state = duck_puzzle.result(random_unsolved_state, random_legal_action)
	display_duck_puzzle(random_unsolved_state)
	return DuckPuzzle(random_unsolved_state)

def display_duck_puzzle(state):
	initial = list(state)
	for i in initial:
		if i == 0:
			initial[initial.index(i)] = '*'
			break
	# 1 2
	# 3 4 5 6
	#   7 8 *
	print(initial[0], initial[1], end='\n') 
	print(initial[2], initial[3], initial[4], initial[5], end='\n  ') 
	print(initial[6], initial[7], initial[8], end='\n') 

# Question 3c: Manhattan distance heuristic for Duck puzzle
def manhattan_heuristic_duck_puzzle(node):
	# vertical and horizontal positions of goal state
	# 00 01
	# 10 11 12 13
	#    21 22 23
	goal = (1,2,3,4,5,6,7,8,0)
	state = node.state
	goal_position_matrix = [ [0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3] ]
	manhattan_dist = 0
	for i in state:
		if i != 0: # and i != goal[state.index(i)]
			positon_of_i = goal_position_matrix[state.index(i)]
			goal_position_of_i = goal_position_matrix[goal.index(i)]
			horizontal_dist = abs(positon_of_i[1] - goal_position_of_i[1])
			vertical_dist = abs(positon_of_i[0] - goal_position_of_i[0])
			manhattan_dist += (horizontal_dist + vertical_dist)
			# print(i, horizontal_dist, vertical_dist, manhattan_dist)
	return manhattan_dist

# Qusetion 3d: returns max of misplaces_tile_heuristic and manhattan_heuristic for duck puzzle
def find_max_heuristic_value_duck_puzzle(node):
	puzzle = DuckPuzzle(node.state)
	misplaces_tile_heuristic_value = puzzle.h(node)
	manhattan_heuristic_value = manhattan_heuristic_duck_puzzle(node)
	return max(misplaces_tile_heuristic_value, manhattan_heuristic_value)

# ______________________________________________________________________________

# main function to generate data
if __name__ == '__main__':

	# 8puzzle
	for x in range(10):
		puzzle = make_rand_8puzzle()

		print('Using misplaced tiles heuristic:')
		start_time = time.time()
		solved_node = modified_astar_search(puzzle)
		elapsed_time = time.time() - start_time
		print(f'elapsed time (in seconds): {elapsed_time}s')
		print(f'path_cost: {solved_node.path_cost}')
		print(f'frontier_popped: {solved_node.frontier_popped}')

		print('Using manhattan distance heuristic:')
		start_time = time.time()
		solved_node = modified_astar_search(puzzle, manhattan_heuristic_8puzzle)
		elapsed_time = time.time() - start_time
		print(f'elapsed time (in seconds): {elapsed_time}s')
		print(f'path_cost: {solved_node.path_cost}')
		print(f'frontier_popped: {solved_node.frontier_popped}', end='\n')


		print('Using max heuristic:')
		start_time = time.time()
		solved_node = modified_astar_search(puzzle, find_max_heuristic_value_8puzzle)
		elapsed_time = time.time() - start_time
		print(f'elapsed time (in seconds): {elapsed_time}s')
		print(f'path_cost: {solved_node.path_cost}')
		print(f'frontier_popped: {solved_node.frontier_popped}', end='\n')
		print(' ')

	print('8puzzle done\n\n')

	# Duck puzzle
	for x in range(10):
		puzzle = make_rand_duck_puzzle()

		print('Using misplaced tiles heuristic:')
		start_time = time.time()
		solved_node = modified_astar_search(puzzle)
		elapsed_time = time.time() - start_time
		print(f'elapsed time (in seconds): {elapsed_time}s')
		print(f'path_cost: {solved_node.path_cost}')
		print(f'frontier_popped: {solved_node.frontier_popped}')

		print('Using manhattan distance heuristic:')
		start_time = time.time()
		solved_node = modified_astar_search(puzzle, manhattan_heuristic_duck_puzzle)
		elapsed_time = time.time() - start_time
		print(f'elapsed time (in seconds): {elapsed_time}s')
		print(f'path_cost: {solved_node.path_cost}')
		print(f'frontier_popped: {solved_node.frontier_popped}')

		print('Using max heuristic:')
		start_time = time.time()
		solved_node = modified_astar_search(puzzle, find_max_heuristic_value_duck_puzzle)
		elapsed_time = time.time() - start_time
		print(f'elapsed time (in seconds): {elapsed_time}s')
		print(f'path_cost: {solved_node.path_cost}')
		print(f'frontier_popped: {solved_node.frontier_popped}', end='\n')
		print(' ')

	print('DuckPuzzle done\n\n')

# ______________________________________________________________________________


