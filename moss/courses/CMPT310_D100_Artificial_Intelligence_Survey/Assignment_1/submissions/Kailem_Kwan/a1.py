'''
Assignment 1: Experimenting with the 8-puzzle

Kailem Kwan
301350992
kailemk@sfu.ca

Use solve_all_eight_puzzle(False) to generate a 8-puzzle and solve it with all 3 heuristics.
Use solve_all_duck_puzzle(False) to generate a 8-puzzle and solve it with all 3 heuristics.

'''



# Import datetime for the timer formatting and csv to output our data to a CSV file 
from search import *
import random
import time
import datetime
import csv
import random




# Question 1: Helper Functions



# Returns a new instance of a EightPuzzle problem that is solvable
def make_rand_8puzzle():

	# Repeat this loop until we generate a solvable puzzle
	while(True):

		# Create list that contains 9 unique integers in the range [0-8] and shuffle it
		initial = list(range(0,9))
		random.shuffle(initial)
		initial = tuple(initial)
		# DEBUG: Printing the initial state of the puzzle
		# print(initial)

		# Create the puzzle
		puzzle = EightPuzzle(initial)

		# Return the puzzle if it is solvable
		if(puzzle.check_solvability(initial)):
			return puzzle;



# Takes an 8-puzzle state as an input and prints it as a 3x3 matrix
def display(state):

	# Traverse each index in the tuple and print the value of at that index with a space
	for i in range(3):
		for j in range(3):
			if state[(i * 3) + j] == 0:
				print('*', end = ' ')
			else:
				print(state[(i * 3) + j], end = ' ')
		# Move on to the next line
		print()
	return





# Question 2: Comparing Algorithms



# Modification made to A* search by changing best_first_graph_search to return a tuple
# that includes the complete puzzle and the number of nodes removed from frontier (which
# is one more than the length of the explored list).

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
	while frontier:
		node = frontier.pop()
		if problem.goal_test(node.state):
			if display:
				print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")  
			return tuple([node, len(explored) + 1])
		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				frontier.append(child)
			elif child in frontier:
				if f(child) < frontier[child]:
					del frontier[child]
					frontier.append(child)
	return None



# A* search taken from search.py 
# No changes made to this function, but we need to have this function in this file 
# so that the modifications made to best_first_graph_search() are overridden

def astar_search(problem, h=None, display=False):
	"""A* search is best-first graph search with f(n) = g(n)+h(n).
	You need to specify the h function when you call astar_search, or
	else in your Problem subclass."""
	h = memoize(h or problem.h, 'h')
	return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)



# Function that returns the Manhattan Distance heuristic
def manhattan_distance(node):

	# Stores the minimum number of moves required to move a tile 
	# to its home. The index of the tuple denotes the value of tile we
	# want to compute, and the subindex represents the number of moves 
	# required given a position.
	min_moves = [(4, 3, 2, 3, 2, 1, 2, 1, 0),
				 (0, 1, 2, 1, 2, 3, 2, 3, 4),
				 (1, 0, 1, 2, 1, 2, 3, 2, 3),
				 (2, 1, 0, 3, 2, 1, 4, 3, 2),
				 (1, 2, 3, 0, 1, 2, 1, 2, 3),
				 (2, 1, 2, 1, 0, 1, 2, 1, 2),
				 (3, 2, 1, 2, 1, 0, 3, 2, 1),
				 (2, 3, 4, 1, 2, 3, 0, 1, 2), 
				 (3, 2, 3, 2, 1, 2, 1, 0, 1)]
	return sum(min_moves[node.state[i]][i] for i in range(9))



# Function that returns the maximum of the Manhattan distance heuristic
# and the  misplaced tile heuristic
def max_misplaced_manhattan(node):
	return max(manhattan_distance(node), sum(s != g for (s, g) in zip(node.state, (1,2,3,4,5,6,7,8,0))))



# Function that solves an eight puzzle
# For the Misplaced Tile heuristic, pass puzzle.h as heuristic
# For the Manhattan Distance heuristic, pass manhattan_distance as heuristic
# For max(Misplace Tile, Manhattan Distance), max_misplaced_manhattan as heuristic
def solve_eight_puzzle(puzzle, h):

	# Print the puzzle we are solving with the heuristic type we are using
	heuristic_names = {"h": "Misplaced Tile", "manhattan_distance": "Manhattan Distance", 
					  "max_misplaced_manhattan": "max(Misplaced Tile, Manhattan Distance)"}

	print("Solving the following 8-puzzle with the", heuristic_names[h.__name__], "heuristic:")
	display(puzzle.initial)

	# Start a timer to measure how long it takes to solve the puzzle
	start_time = time.time()

	# Use A* search to solve the puzzle
	a = astar_search(puzzle, h)
	
	# See how long it took to complete the puzzle (and format it to hours:minutes:seconds)
	elapsed_time = (time.time() - start_time)
	elapsed_time = str(datetime.timedelta(seconds = elapsed_time))

	# Print solution data
	print("Time used to solve solve the puzzle:", elapsed_time)
	print("Moves used to complete the puzzle:", a[0].path_cost)
	print("Total number of nodes removed from frontier:", a[1])
	print()

	# Return solution data
	return elapsed_time, a[0].path_cost, a[1]



# Function that solves the puzzle with each of the 3 heuristics
# If write_to_csv is true, then the solution data will be written to a CSV file called a1q3.csv
def solve_all_eight_puzzle(write_to_csv):
	
	# Generate a solvable 8-puzzle
	puzzle = make_rand_8puzzle()

	# write_content stores the data we want to write to the CSV file 
	write_content = [puzzle.initial]

	# Solve the puzzles with each heuristic and store the data in the write_content list
	write_content.extend(solve_eight_puzzle(puzzle, puzzle.h))
	write_content.extend(solve_eight_puzzle(puzzle, manhattan_distance))
	write_content.extend(solve_eight_puzzle(puzzle, max_misplaced_manhattan))

	# Print some lines to create some space between log messages
	print()
	print()
	
	# Write to the CSV file if true
	if(write_to_csv):
		with open("a1q2.csv", mode = 'a') as csv_file:
			writer = csv.writer(csv_file, delimiter = ',', quotechar = '"')
			writer.writerow(write_content)





# Question 3: Duck Puzzle



# Puzzle that is similar to the 8-puzzle but in the shape:
# 1 2
# 3 4 5 6
#   7 8 0
class DuckPuzzle(Problem):

	# Most of the following methods are the same as the 8-puzzle implementations, with minor tweaks
	def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
		""" Define goal state and initialize a problem """
		super().__init__(initial, goal)

	def find_blank_square(self, state):
	# Return the index of the blank square in a given state


		return state.index(0)

	def actions(self, state):
		""" Return the actions that can be executed in the given state.
		The result would be a list, since there are only four possible actions
		in any given state of the environment """

		possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
		index_blank_square = self.find_blank_square(state)

		# Lists that contain the boundaries of the puzzle represented as an index of the puzzle
		left_limit = [0, 2, 6]
		up_limit = [0, 1, 4, 5]
		right_limit = [1, 5, 8]
		down_limit = [2, 6, 7, 8]

		# If the blank square is in an index in the boundary list, 
		# remove that action from the list of available actions
		if index_blank_square in left_limit:
			possible_actions.remove('LEFT')
		if index_blank_square in up_limit:
			possible_actions.remove('UP')
		if index_blank_square in right_limit:
			possible_actions.remove('RIGHT')
		if index_blank_square in down_limit:
			possible_actions.remove('DOWN')

		return possible_actions

	def result(self, state, action):
		""" Given state and action, return a new state that is the result of the action.
		Action is assumed to be a valid action in the state """

		# blank is the index of the blank square
		blank = self.find_blank_square(state)
		new_state = list(state)

		# Assign the dictionary we want to use based on the position of the blank square
		if blank <= 2:
			delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
		elif blank == 3:
			delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
		else:
			delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

		neighbor = blank + delta[action]
		new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

		return tuple(new_state)

	def goal_test(self, state):
		""" Given a state, return True if state is a goal state or False, otherwise """

		return state == self.goal

	def make_rand_duck():

		# Create the goal state and shuffle it
		puzzle = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))
		state = puzzle.initial

		for i in range(10000):
			actions = puzzle.actions(state)
			state = puzzle.result(state, random.choice(actions))

		puzzle = DuckPuzzle(state)
		return puzzle

	# Prints out the duck puzzle
	def display_duck(self, state):
		for i in range(2):
			if(state[i] == 0):
				print('*', end = ' ')
			else:
				print(state[i], end = ' ')
		print()
		for i in range(4):
			if(state[i + 2] == 0):
				print('*', end = ' ')
			else:
				print(state[i + 2], end = ' ')
		print()
		print(' ', end = ' ')
		for i in range(3):
			if(state[i + 6] == 0):
				print('*', end = ' ')
			else:
				print(state[i + 6], end = ' ')
		print()


	# The EightPuzzle.h method. Unchanged from the 8-puzzle implementation
	def misplaced_tile(self, node):
		""" Return the heuristic value for a given state. Default heuristic function used is 
		h(n) = number of misplaced tiles """

		return sum(s != g for (s, g) in zip(node.state, self.goal))

	def manhattan_distance(self, node):
		# Stores the minimum number of moves required to move a tile 
		# to its home. The index of the tuple denotes the value of tile we
		# want to compute, and the subindex represents the number of moves 
		# required given a position.
		min_moves = [(5, 4, 4, 3, 2, 1, 2, 1, 0),
					 (0, 1, 1, 2, 3, 4, 3, 4, 5),
					 (1, 0, 2, 1, 2, 3, 2, 3, 4),
					 (1, 2, 0, 1, 2, 3, 2, 3, 4),
					 (2, 1, 1, 0, 1, 2, 1, 2, 3),
					 (3, 2, 2, 1, 0, 1, 2, 1, 2),
					 (4, 3, 3, 2, 1, 0, 3, 2, 1),
					 (3, 2, 2, 1, 2, 3, 0, 1, 2),
					 (4, 3, 3, 2, 1, 2, 1, 0, 1)]
		return sum(min_moves[node.state[i]][i] for i in range(9))



	# Function that returns the maximum of the Manhattan distance heuristic
	# and the  misplaced tile heuristic
	def max_misplaced_manhattan(self, node):
		return max(self.manhattan_distance(node), self.misplaced_tile(node))



	# Function that solves a duck puzzle
	# For the Misplaced Tile heuristic, pass self.misplaced_tile as heuristic
	# For the Manhattan Distance heuristic, pass self.manhattan_distance as heuristic
	# For max(Misplace Tile, Manhattan Distance), pass self.max_misplaced_manhattan as heuristic
	def solve_duck_puzzle(self, h):

		# Print the puzzle we are solving with the heuristic type we are using
		heuristic_names = {"misplaced_tile": "Misplaced Tile", "manhattan_distance": "Manhattan Distance", 
						  "max_misplaced_manhattan": "max(Misplaced Tile, Manhattan Distance)"}

		print("Solving the following duck puzzle with the", heuristic_names[h.__name__], "heuristic:")
		self.display_duck(self.initial)

		# Start a timer to measure how long it takes to solve the puzzle
		start_time = time.time()

		# Use A* search to solve the puzzle
		a = astar_search(self, h)
		
		# See how long it took to complete the puzzle
		elapsed_time = (time.time() - start_time)

		# Format the time to hours:minutes:seconds
		elapsed_time = str(datetime.timedelta(seconds = elapsed_time))

		# Print solution data
		print("Time used to solve solve the puzzle:", elapsed_time)
		print("Moves used to complete the puzzle:", a[0].path_cost)
		print("Total number of nodes removed from frontier:", a[1])
		print()

		# Return solution data
		return elapsed_time, a[0].path_cost, a[1]



# Function that solves the puzzle with each of the 3 heuristics
# If write_to_csv is true, then the solution data will be written to a CSV file called a1q3.csv
def solve_all_duck_puzzle(write_to_csv):
		
	# Generate a solvable 8-puzzle
	puzzle = DuckPuzzle.make_rand_duck()

	# write_content stores the data we want to write to the CSV file 
	write_content = [puzzle.initial]

	# Solve the puzzles with each heuristic and store the data in the write_content list
	write_content.extend(puzzle.solve_duck_puzzle(puzzle.misplaced_tile))
	write_content.extend(puzzle.solve_duck_puzzle(puzzle.manhattan_distance))
	write_content.extend(puzzle.solve_duck_puzzle(puzzle.max_misplaced_manhattan))

	# Print some lines to create some space between log messages
	print()
	print()
		
	# Write to the CSV file if true
	if(write_to_csv):
		with open("a1q3.csv", mode = 'a') as csv_file:
			writer = csv.writer(csv_file, delimiter = ',', quotechar = '"')
			writer.writerow(write_content)






#
# Program starts here
#




# Generates and solves 8-puzzles with each heuristic
'''
for i in range(5):
	solve_all_eight_puzzle(False)
'''

# Generates and solves duck puzzles with each heuristic

for i in range(100):
	solve_all_duck_puzzle(False)
