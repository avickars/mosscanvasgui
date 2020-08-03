#a1.py
from search import *
from random import randint
import time

"""Changes that I made in search.py
def best_first_graph_search(problem, f, display=False):
	f = memoize(f, 'f')
	node = Node(problem.initial)
	frontier = PriorityQueue('min', f)
	frontier.append(node)
	explored = set()
	total_pop = 0 #added
	while frontier:
		node = frontier.pop()
		total_pop += 1 #added
		if problem.goal_test(node.state):
			if display:
				print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
			return node, total_pop #added total_pop
		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				frontier.append(child)
			elif child in frontier:
				if f(child) < frontier[child]:
					del frontier[child]
					frontier.append(child)
	return None, total_pop #added total_pop
"""

# Question 1
# Eight Puzzle

def make_rand_8puzzle():
	state = [0,1,2,3,4,5,6,7,8]

	newState = list(state)

	random.shuffle(newState)

	newEightPuzzle = EightPuzzle(tuple(newState))

	while(newEightPuzzle.check_solvability(newState) == False):
		random.shuffle(newState)
		newEightPuzzle = EightPuzzle(tuple(newState))

	return newEightPuzzle

def display(state):
	for i in range(0,9):
		if state[i] == 0:
			print("*", end='')
			if i % 3 == 2:
				print("\n", end='')
			else:
				print(" ", end='')
		
		else:
			print(state[i], end='')
			if i % 3 == 2:
				print("\n", end='')
			else:
				print(" ", end='')




# Question 2
# References
# https://www.youtube.com/watch?v=GuCzYxHa7iA
# https://www.andrew.cmu.edu/course/15-121/labs/HW-7%20Slide%20Puzzle/lab.html
def manhattan_distance(board):
	currentState = board.state
	index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
	currentSpot = {}
	index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
	distance = 0

	for i in range(len(currentState)):
		currentSpot[currentState[i]] = index[i]

	#not include 0
	for i in range(1,9):
		x = abs(index_goal[i][0] - currentSpot[i][0])
		y = abs(index_goal[i][1] - currentSpot[i][1])
		distance = distance + x + y

	return distance

def max_both(board):
	puzzle = EightPuzzle(board.state)
	return max(manhattan_distance(board), puzzle.h(board))


# This function is called ten times to get the result when we are comparing 
# three different heuristic methods
def running_time_test():
	eight_puzzle = make_rand_8puzzle()
	manh_astar = eight_puzzle
	max_of_both = eight_puzzle

	#misplaced tile heuristic------------
	display(eight_puzzle.initial)
	start_time = time.time()
	result , pop = astar_search(eight_puzzle)
	elapsed_time = time.time() - start_time

	print('*******************************************************')
	print('A* - search using the misplaced tile heuristic')
	print('Length of Solution: ', len(result.solution()))
	print('Total number of nodes removed from frontier: ', pop)
	print('Time Taken to solve: ', elapsed_time ,'s')
	print('-------------------------------------------------------')

	#manhattan distance heuristic-----------
	start_time = time.time()
	result , pop = astar_search(eight_puzzle, h=manhattan_distance)
	elapsed_time = time.time() - start_time

	print('A* - search using Manhattan Distance heuristic')
	print('Length of Solution: ', len(result.solution()))
	print('Total number of nodes removed from frontier: ', pop)
	print('Time Taken to solve: ', elapsed_time ,'s')
	print('-------------------------------------------------------')

	#max of both--------------
	start_time = time.time()
	result , pop = astar_search(eight_puzzle, h=max_both)
	elapsed_time = time.time() - start_time

	print('A* - search using max of misplaced heuristic and manhattan heuristic')
	print('Length of Solution: ', len(result.solution()))
	print('Total number of nodes removed from frontier: ', pop)
	print('Time Taken to solve: ', elapsed_time ,'s')
	print('*******************************************************')


def running_test_8puzzle_ten_time():
	print('************************************')
	print('This is Eight Puzzle.')
	print('************************************')
	for i in range(10):
		print('The' , i+1, 'times')
		running_time_test()

running_test_8puzzle_ten_time()



#____________________________________________________________________________


# Question 3
# Duck puzzle

class DuckPuzzle(Problem):
	""" The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
	squares is a blank. A state is represented as a tuple of length 9, where  element at
	index i represents the tile number  at index i (0 if it's an empty square) """

	def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
		""" Define goal state and initialize a problem """
		super().__init__(initial, goal)

	def find_blank_square(self, state):
		return state.index(0)

	def actions(self, state):
		possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
		index_blank_square = self.find_blank_square(state)

		if index_blank_square == 0:
			possible_actions.remove('LEFT')
			possible_actions.remove('UP')
		if index_blank_square == 1:
			possible_actions.remove('UP')
			possible_actions.remove('RIGHT')
		if index_blank_square == 2:
			possible_actions.remove('LEFT')
			possible_actions.remove('DOWN')
		if index_blank_square == 4:
			possible_actions.remove('UP')
		if index_blank_square == 5:
			possible_actions.remove('UP')
			possible_actions.remove('RIGHT')
		if index_blank_square == 6:
			possible_actions.remove('LEFT')
			possible_actions.remove('DOWN')
		if index_blank_square == 7:
			possible_actions.remove('DOWN')
		if index_blank_square == 8:
			possible_actions.remove('RIGHT')
			possible_actions.remove('DOWN')

		return possible_actions

	def result(self, state, action):
		""" Given state and action, return a new state that is the result of the action.
		Action is assumed to be a valid action in the state """

		# blank is the index of the blank square
		blank = self.find_blank_square(state)
		new_state = list(state)
		if blank < 3:
			delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
			neighbor = blank + delta[action]
			new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
		if blank == 3:
			delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
			neighbor = blank + delta[action]
			new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
		if blank == 4 or blank == 5 or blank == 6 or blank == 7 or blank == 8:
			delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
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
	
	def display(self):
		for i in range(9):
			if self.initial[i] == 0:
				print("*", end = '')
				if i == 1:
					print("\n", end = '')
				elif i == 5:
					print("\n", end = '  ')
				else:
					print(" ", end='')

			else:
				print(self.initial[i], end='')
				if i == 1:
					print("\n", end = '')
				elif i == 5:
					print("\n", end = '  ')
				else:
					print(" ", end='')
		print("\n")


# Randomly move node/index from the goal state to make the duck puzzle sovable
# By doing this method we do not need to check for sovable of the puzzle
# by calling check_solvability() function.
def make_rand_dpuzzle():
	puzzle = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0));

	currentNode = Node(puzzle.initial)

	for i in range(1000):
		possibleMoves = puzzle.actions(currentNode.state)
		selectedMove = randint(0, len(possibleMoves) - 1)
		currentNode.state = puzzle.result(currentNode.state, possibleMoves[selectedMove])

	finalPuzzle = DuckPuzzle(currentNode.state)
	finalPuzzle.display()

	return finalPuzzle


def manhattan_distance_duck(board):
	currentState = board.state
	index_goal = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
	currentSpot = {}
	index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
	distance = 0

	for i in range(len(currentState)):
		currentSpot[currentState[i]] = index[i]

	for i in range(1,9):
		x = abs(index_goal[i][0] - currentSpot[i][0])
		y = abs(index_goal[i][1] - currentSpot[i][1])
		distance = distance + x + y

	return distance


def max_both_duck(board):
	puzzle = EightPuzzle(board.state)
	return max(manhattan_distance_duck(board), puzzle.h(board))


print('************************************')
print("Part 3. This is the Duck Puzzle \n")
print('************************************')

# This function is called ten times to get the result when we are comparing 
# three different heuristic methods 
def running_time_test_duckpuzzle():
	duck_puzzle = make_rand_dpuzzle()
	manh_astar = duck_puzzle
	max_of_both = duck_puzzle

	#misplaced tile heuristic-----------
	start_time = time.time()
	result , pop = astar_search(duck_puzzle)
	elapsed_time = time.time() - start_time

	print('*******************************************************')
	print('A* - search using the misplaced tile heuristic')
	print('Length of Solution: ', len(result.solution()))
	print('Total number of nodes removed from frontier: ', pop)
	print('Time Taken to solve: ', elapsed_time ,'s')
	print('------------------------------------------------------')

	#manhattan distance heuristic-----------

	start_time = time.time()
	result , pop = astar_search(duck_puzzle, h=manhattan_distance_duck)
	elapsed_time = time.time() - start_time

	print('A* - search using Manhattan Distance heuristic')
	print('Length of Solution: ', len(result.solution()))
	print('Total number of nodes removed from frontier: ', pop)
	print('Time Taken to solve: ', elapsed_time ,'s')
	print('------------------------------------------------------')

	#max of both---------------------
	start_time = time.time()
	result , pop = astar_search(duck_puzzle, h=max_both_duck)
	elapsed_time = time.time() - start_time

	print('A* - search using max of misplaced heuristic and manhattan heuristic')
	print('Length of Solution: ', len(result.solution()))
	print('Total number of nodes removed from frontier: ', pop)
	print('Time Taken to solve: ', elapsed_time ,'s')
	print('*******************************************************')



def running_test_duckPuzzle_ten_times():
	for i in range(10):
		print('The' , i+1, 'times')
		running_time_test_duckpuzzle()

running_test_duckPuzzle_ten_times()