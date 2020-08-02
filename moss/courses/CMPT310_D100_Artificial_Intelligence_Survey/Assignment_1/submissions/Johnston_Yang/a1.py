# a1.py
# By Johnston Yang
# 301282192


#https://stackoverflow.com/questions/1380860/add-variables-to-tuple
# how to work with tuples
#https://www.tutorialspoint.com/python/python_classes_objects.htm
# how classes work in python
#got help from TA
# asked about astar_search function

from search import *
import random as r
import time
import csv


# creates random 8 puzzles that are solvable 
def make_rand_8puzzle():
	solved = False
	while(not solved):
		puzzle = ()
		numbers = [0,1,2,3,4,5,6,7,8]
		for i in range(9):
			num = r.choice(numbers)
			puzzle = puzzle + (num,)
			numbers.remove(num)
		tmp = EightPuzzle(puzzle)
		solved = tmp.check_solvability(puzzle)
	return puzzle

# displays the 8 puzzles to terminal
def display(state):
	num = 1
	for i in state:
		if(i == 0):
			print("* ",end="")
		else:
			print(str(i) + " ",end="")
		if(num % 3 == 0):
			print()
		num += 1
	return state


def astar_search(problem, h=None, display=False):
	"""A* search is best-first graph search with f(n) = g(n)+h(n).
	You need to specify the h function when you call astar_search, or
	else in your Problem subclass."""
	h = memoize(h or problem.h, 'h')
	return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


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
		removed += 1
		if problem.goal_test(node.state):
			if display:
				print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
				print(str(removed) + " Removed nodes from Frontier")
			return (node , removed) # gets the number of removed nodes with removed variable
		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				frontier.append(child)
			elif child in frontier:
				if f(child) < frontier[child]:
					del frontier[child]
					frontier.append(child)
	return None

# adds up the total distance that separates a tile from where the tile is suppose to be
def manhattanHeuristic(node):
	state = node.state
	dist = 0
	state_index = [[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]]
	index_goal = {0: [2, 2], 1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 2], 8: [1, 2]}
	for i in range(len(state)):
		if(state[i] != 0):
			dist = ( abs(state_index[i][0] - index_goal[state[i]][0]) + abs(state_index[i][1] - index_goal[state[i]][1]) ) + dist
	return dist

# calculates the misplaced heuristic 
def h(node):
	goal = (1,2,3,4,5,6,7,8,0)
	return sum(s != g for (s, g) in zip(node.state, goal))

# takes both heuristics and finds the max of the two heuristics
def maxh(node):
	misVal = h(node)
	manVal = manhattanHeuristic(node)
	return max(misVal,manVal)

## code to put data into csv file
# with open('data.csv','a',newline='') as file:
# 	writer = csv.writer(file,delimiter = ',')
	#writer.writerow(["Heuristic","Elapsed Time (s)","Number of Tiles Moved","Number of Nodes Removed from Frontier"])

### code to run the regular eight puzzle
i = 0
while(i != 20):
	puzzle = make_rand_8puzzle()
	display(puzzle)
	thePuzzle = EightPuzzle(puzzle)
	thePuzzle.state = puzzle
	thePuzzle.intial = puzzle

	#misplaced tile
	print("-"*64)
	print("Misplaced Heuristic")
	start_timeM = time.time()
	val,removed = astar_search(thePuzzle,h=h,display=False)
	elapsed_timeM = time.time() - start_timeM
	print("Elapsed Time: " + str(elapsed_timeM)) # how long
	print("Moves to solution: " + str(val.path_cost)) # how many moves
	print(str(removed) + " Removed nodes from Frontier") # number of removed nodes
	print("-"*64)

	#writer.writerow(["Misplaced",elapsed_timeM,val.path_cost,removed])


	#manhattan 
	print("-"*64)
	print("Manhattan Hueristic")
	start_timeM = time.time()
	val,removed = astar_search(thePuzzle,h=manhattanHeuristic,display=False)
	elapsed_timeM = time.time() - start_timeM
	print("Elapsed Time: " + str(elapsed_timeM)) # how long
	print("Moves to solution: " + str(val.path_cost)) # how many moves
	print(str(removed) + " Removed nodes from Frontier") # number of removed nodes
	print("-"*64)

	#writer.writerow(["Manhattan",elapsed_timeM,val.path_cost,removed])
	

	#max of misplaced/manhattan
	print("-"*64)
	print("Max of Misplaced and Manhattan")
	start_timeM = time.time()
	val,removed = astar_search(thePuzzle,h=maxh,display=False)
	elapsed_timeM = time.time() - start_timeM
	print("Elapsed Time: " + str(elapsed_timeM)) # how long
	print("Moves to solution: " + str(val.path_cost)) # how many moves
	print(str(removed) + " Removed nodes from Frontier") # number of removed nodes
	print("-"*64)

	#writer.writerow(["Max of Misplaced and Manhattan",elapsed_timeM,val.path_cost,removed])

	i += 1


class DuckPuzzle(Problem):

	def __init__(self, initial, goal=(1,2,3,4,5,6,7,8,0)):
		super().__init__(initial, goal)


	def find_blank_square(self,state):
		return state.index(0)

	def actions(self, state):

		possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
		index_blank_square = self.find_blank_square(state)

		if(index_blank_square > 5 or index_blank_square == 2):
			possible_actions.remove('DOWN')
			if(index_blank_square == 2 or index_blank_square == 6):
				possible_actions.remove('LEFT')
			if(index_blank_square == 8):
				possible_actions.remove('RIGHT')
		elif( index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5):
			possible_actions.remove('UP')
			if(index_blank_square == 0):
				possible_actions.remove('LEFT')		
			if(index_blank_square == 1 or index_blank_square == 5):
				possible_actions.remove('RIGHT')	
		return possible_actions

	def result(self, state, action):

		blank = self.find_blank_square(state)
		new_state = list(state)

		delta = {'UP': -3, 'DOWN' : 3 ,'LEFT': -1, 'RIGHT': 1}

		if(blank == 0 or blank == 1):
			delta['UP'] = -2
		if(blank == 2 or blank == 3):
			delta['DOWN'] = 2

		neighbour = blank + delta[action]
		new_state[blank], new_state[neighbour] = new_state[neighbour], new_state[blank]

		return tuple(new_state)

	def goal_test(self,state):
		return state == self.goal


def Duckh(node):
	goal = (1,2,3,4,5,6,7,8,0)
	return sum(s != g for (s, g) in zip(node.state, goal))

def DuckManhattan(node):
	state = node.state
	dist = 0
	state_index = [[0,0],[1,0],[0,1],[1,1],[2,1],[3,1],[1,2],[2,2],[3,2]]
	index_goal = {0: [3, 2], 1: [0, 0], 2: [1, 0], 3: [0, 1], 4: [1, 1], 5: [2, 1], 6: [3, 1], 7: [1, 2], 8: [2, 2]}
	for i in range(len(state)):
		if(state[i] != 0):
			dist = ( abs(state_index[i][0] - index_goal[state[i]][0]) + abs(state_index[i][1] - index_goal[state[i]][1]) ) + dist
	return dist

def maxDuckh(node):
	misplaced = Duckh(node)
	manhattan = DuckManhattan(node)
	return max(misplaced,manhattan)


def make_duck_puzzle():
	puzzle = [1,2,3,4,5,6,7,8,0]
	moves = 0
	while(moves != 1000):
		for zeroPos in range(len(puzzle)):
			if (puzzle[zeroPos] == 0): # checks for position of zero
				if(zeroPos == 8): # position of zero
					switchPos = r.choice([5,7]) # positions that can be switched
					if (switchPos == 5):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos] # performs the swap 
					elif(switchPos == 7):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
				elif(zeroPos == 5):
					switchPos = r.choice([4,8])
					if(switchPos == 4):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
					elif(switchPos == 8):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
				elif(zeroPos == 7):
					switchPos = r.choice([4,6,8])
					if(switchPos == 4):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
					elif(switchPos == 6):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
					elif(switchPos == 8):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
				elif(zeroPos == 4):
					switchPos = r.choice([3,5,7])
					if(switchPos == 3):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
					elif(switchPos == 5):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
					elif(switchPos == 7):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
				elif(zeroPos == 6):
					switchPos = r.choice([3,7])
					if(switchPos == 3):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
					elif(switchPos == 7):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
				elif(zeroPos == 3):
					switchPos = r.choice([1,2,4,6])
					if(switchPos == 1):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
					elif(switchPos == 2):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
					elif(switchPos == 4):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
					elif(switchPos == 6):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
				elif(zeroPos == 1):
					switchPos = r.choice([0,3])
					if(switchPos == 3):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
					elif(switchPos == 0):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
				elif(zeroPos == 2):
					switchPos = r.choice([0,3])
					if(switchPos == 3):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
					elif(switchPos == 0):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
				elif(zeroPos == 0):
					switchPos = r.choice([1,2,])
					if(switchPos == 1):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
					elif(switchPos == 2):
						puzzle[switchPos], puzzle [zeroPos] = puzzle[zeroPos], puzzle[switchPos]
		moves += 1
	return tuple(puzzle)


### code to write data into csv file
# with open('housepuzzle.csv','a',newline='') as hpfile:
# 	writer = csv.writer(hpfile,delimiter=',')

	
### code to run the duck puzzle
i = 0
while(i != 20):
	puzzle = make_duck_puzzle()
	
	thePuzzle = DuckPuzzle(puzzle)
	thePuzzle.state = puzzle
	thePuzzle.intial = puzzle
	print(puzzle)

	#misplaced tile
	print("-"*64)
	print("Misplaced Heuristic")	
	start_timeM = time.time()
	val,removed = astar_search(thePuzzle,h=Duckh,display=False)
	elapsed_timeM = time.time() - start_timeM
	print("Elapsed Time: " + str(elapsed_timeM)) # how long
	print("Moves to solution: " + str(val.path_cost)) # how many moves
	print(str(removed) + " Removed nodes from Frontier") # number of removed nodes
	print("-"*64)

	#writer.writerow(["Misplaced",elapsed_timeM,val.path_cost,removed])

	#manhattan
	print("-"*64)
	print("Manhattan Heuristic")
	start_timeM = time.time()
	val,removed = astar_search(thePuzzle,h=DuckManhattan,display=False)
	elapsed_timeM = time.time() - start_timeM
	print("Elapsed Time: " + str(elapsed_timeM)) # how long
	print("Moves to solution: " + str(val.path_cost)) # how many moves
	print(str(removed) + " Removed nodes from Frontier") # number of removed nodes
	print("-"*64)

	#writer.writerow(["Manhattan",elapsed_timeM,val.path_cost,removed])

	# max of manhattan and misplaced
	print("-"*64)
	print("Max of Manhattan and Misplaced Heuristic")
	print(puzzle)
	start_timeM = time.time()
	val,removed = astar_search(thePuzzle,h=maxDuckh,display=False)
	elapsed_timeM = time.time() - start_timeM
	print("Elapsed Time: " + str(elapsed_timeM)) # how long
	print("Moves to solution: " + str(val.path_cost)) # how many moves
	print(str(removed) + " Removed nodes from Frontier") # number of removed nodes
	print("-"*64)

	#writer.writerow(["Max of Misplaced and Manhattan",elapsed_timeM,val.path_cost,removed])

	i += 1
