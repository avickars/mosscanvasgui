# a1.py

#acknowledgement:
#	stackoverflow
#	w3school
#	geeksforgeeks
#	classmate
#	google
# 	partial code copied and modified from search.py

import math
import random
import time
from search import *

# ...
#===EIGHT===========================================================================================

def my_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return my_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def my_best_first_graph_search(problem, f, display=False):
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
			print('Eight | Nodes removed from frontier:', len(explored)+1)
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

def eight():

	puzzle = make_rand_8puzzle()
	print('Eight Puzzle')
	display(puzzle.initial)

	print()

	print('Misplaced Tile Heuristic:')	
	start_time = time.time()
	solutionLinear = my_astar_search(puzzle, h).solution()
	elapsed_time = time.time() - start_time
	print(f'Eight | Elapsed time (seconds): {elapsed_time}s')
	print('Eight | Length of the solution:', len(solutionLinear))
	print()

	print('Manhattan Distance Heuristic:')
	mhd_start_time = time.time()
	solutionManhattan = my_astar_search(puzzle, my_manhattan).solution()
	mhd_elapsed_time = time.time() - mhd_start_time
	print(f'Eight | Elapsed time (seconds): {mhd_elapsed_time}s')
	print('Eight | Length of the solution:', len(solutionManhattan))
	#print(solutionManhattan)
	print()

	print('Max Heuristic:')
	max_heuristic_start_time = time.time()
	solutionMaxHeuristic = my_astar_search(puzzle, max_heuristic).solution()
	max_heuristic_elapsed_time = time.time() - max_heuristic_start_time
	print(f'Eight | Elapsed time (seconds): {max_heuristic_elapsed_time}s')
	print('Eight | Length of the solution:', len(solutionMaxHeuristic))
	print()

def make_rand_8puzzle():
	goal = (1,2,3,4,5,6,7,8,0)
	e = EightPuzzle(goal)

	numShuffle = 100
	generated_puzzle = goal
	i = 0
	while i < numShuffle or not goal:
		possibleAction = e.actions(generated_puzzle)
		randAction = random.randint(0,len(possibleAction)-1)
		generated_puzzle = e.result(generated_puzzle, possibleAction[randAction])
		i+=1

	return EightPuzzle(generated_puzzle)

def display(state):

	#generate 3x3 matrix initialized at 0
	row = col = 3
	matrix = [[0 for i in range(row)] for j in range(col)]

	#insert list into matrix, replace 0 with *
	k = 0
	for i in range(row):
		for j in range(col):
			if state[k] == 0:
				matrix[i][j] = '*'
				k += 1
			else:
				matrix[i][j] = state[k]
				k += 1

	#display matrix out in grid form
	for i in matrix:	#row in matrix
		for j in i:		#elements per row
			print(j, end = " ")
		print()

goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
# def linear(node):
# 	return sum([1 if node.state[i] != goal[i] else 0 for i in range(8)])

def h(node):
    """ Return the heuristic value for a given state. 
    Default heuristic function used is h(n) = number of misplaced tiles """

    return sum(s != g for (s, g) in zip(node.state, goal))

def my_manhattan(node):
	state = node.state
	index_goal = {0:[2,2], 1:[0,0], 2:[1,0], 3:[2,0], 4:[0,1], 5:[1,1], 6:[2,1], 7:[0,2], 8:[1,2]}
	index_state = {}
	index = [[0,0], [1,0], [2,0], [0,1], [1,1], [2,1], [0,2], [1,2], [2,2]]
	x, y = 0, 0

	for i in range(len(state)):
		index_state[state[i]] = index[i]

	mhd = 0
	
	for i in range(8):
		for j in range(2):
			mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
	
	return mhd

def max_heuristic(node):
    manhattan = my_manhattan(node)
    misplaced_tiles = h(node)
    return max(manhattan, misplaced_tiles)


#===DUCK===========================================================================================

def duck_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return duck_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def duck_best_first_graph_search(problem, f, display=False):
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
			print('Duck | Nodes removed from frontier:', len(explored)+1)
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

        if index_blank_square == 0:
            possible_actions.remove('UP')
            possible_actions.remove('LEFT')
        if index_blank_square in (1,5):
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')     
        if index_blank_square in (2,6):
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 4:
            possible_actions.remove('UP')
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

        if blank in (0,1,2):
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        if blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}           
        if blank in (4,5,6,7,8):
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

def duck():
	puzzle = make_rand_duckpuzzle()
	print('Duck Puzzle')
	displayDuck(puzzle.initial)

	print('Misplaced Tile Heuristic:')
	start_time = time.time()
	solutionLinear = duck_astar_search(puzzle).solution()
	elapsed_time = time.time() - start_time
	print(f'Duck | Elapsed time (seconds): {elapsed_time}s')
	print('Duck | Length of the solution:', len(solutionLinear))
	#print(solutionLinear)
	print()

	print('Manhattan Distance Heuristic:')
	second_test_start_time = time.time()
	solutionManhattan = duck_astar_search(puzzle, duck_manhattan).solution()
	second_test_elapsed_time = time.time() - second_test_start_time
	print(f'Duck | Elapsed time (seconds): {second_test_elapsed_time}s')
	print('Duck | Length of the solution:', len(solutionManhattan))
	#print(solutionManhattan)
	print()

	print('Max Heuristic:')
	third_test_start_time = time.time()
	solutionMaxHeuristic = duck_astar_search(puzzle, duck_max_heuristic).solution()
	third_test_elapsed_time = time.time() - third_test_start_time
	print(f'Duck | Elapsed time (seconds): {third_test_elapsed_time}s')
	print('Duck | Length of the solution:', len(solutionMaxHeuristic))
	#print(solutionMaxHeuristic)
	print()

def make_rand_duckpuzzle():
	goal = (1,2,3,4,5,6,7,8,0)
	d = DuckPuzzle(goal)

	numShuffle = 100
	generated_puzzle = goal
	i = 0
	while i < numShuffle or not goal:
		possibleAction = d.actions(generated_puzzle)
		randAction = random.randint(0,len(possibleAction)-1)
		generated_puzzle = d.result(generated_puzzle, possibleAction[randAction])
		i+=1

	return DuckPuzzle(generated_puzzle)

def displayDuck(state):

	temp_list = list(state)
	temp_list[state.index(0)] = '*'

	for index, item in enumerate(temp_list):
		if index == 1:
			print(item, end = '\n')
		elif index == 5:
			print(item, end = '\n')
		elif index == 6:
			print('  ' + str(item), end = ' ')
		else:
			print(item, end = ' ')
	print()
	print()

def duck_manhattan(node):
	state = node.state
	index_goal = {0:[3,2], 1:[0,0], 2:[1,0], 3:[0,1], 4:[1,1], 5:[2,1], 6:[3,1], 7:[1,2], 8:[2,2]}
	index_state = {}
	index = [[0,0], [1,0], [0,1], [1,1], [2,1], [3,1], [1,2], [2,2], [3,2]]
	x, y = 0, 0

	for i in range(len(state)):
		index_state[state[i]] = index[i]

	mhd = 0

	for i in range(8):
		for j in range(2):
			mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

	return mhd

def duck_max_heuristic(node):
    manhattan = duck_manhattan(node)
    misplaced_tiles = h(node)
    return max(manhattan, misplaced_tiles)

def test():
	#loop x number of tests
	numTest = 10
	for i in range(numTest):
		print('================')
		print('=====Test ' + str(i+1) + '=====')
		print('================')
		eight() #generate 8puzzle, solve, print results
		duck() #generate duck puzzle, solve, print results

test()