# a1.py
#
# Gabriel Stang 
# 301384654
#
# Assumptions / Execution Information:
# - I ran this file in the aima-python folder cloned from github, using debian, and with python 3.7.3
# - I am using the goal state as defined by the aima-python code and not the textbook 
#
# Sources:
# - https://www.w3schools.com/python/python_lambda.asp -> for lambda syntax
# - https://www.geeksforgeeks.org/currying-function-in-python/ -> for how to implement curried function in python.
# - 

import random, time  # from standard library

from search import *


# *************************************************************************** #
# Question 1:

def make_rand_8puzzle(swaps=1000):
	"""Returns a new instance of an EightPuzzle problem with a random initial 
	   state that is solvable"""

	# init puzzle	
	state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
	puzzle = EightPuzzle(state)
	
	# do n legal moves <where n=swaps>
	for i in range(0, swaps):
		action = random.choice(puzzle.actions(state))  # pick random possible action
		state = puzzle.result(state, action)  # apply the possible action

	puzzle.initial = state  # update the action

	# do error check before returning
	if puzzle.check_solvability(state):
		return puzzle
	else:
		print("ERROR: random puzzle generated was unsolvable.")
		return None


def display(state):
	puzzle_size = 3
	for i in range(0, len(state), puzzle_size):
		for j in range(0, puzzle_size):  # prints rows
			val = state[i + j] 
			end_char = '\n' if j == puzzle_size - 1 else ' ' 
			print( "*" if val == 0 else val, end=end_char ) 

def q1_tests():
	# run tests
	print("q1 tests - testing make_rand_8puzzle() and display(state)")
	
	for i in range(0, 2):
		print( "########## test {} ##########".format(i) )
		puzzle = make_rand_8puzzle() 
		
		print( "random puzzle:" )
		print( puzzle.initial )
		print( "", end="\n" )

		print( "puzzle displayed:" )
		display( puzzle.initial )
		print( "", end="\n" )
	
	print("done q1 tests --------------------------- \n")


# *************************************************************************** #
# Question 2:
#
# Terminology: 
# 	mt -> misplaced tile heuristic
#	md -> manhattan distance heuristic
#	max -> max of mt and md


def astar_search_modified(problem, h=None, display=False):
	"""A* search is best-first graph search with f(n) = g(n)+h(n).
	You need to specify the h function when you call astar_search, or
	else in your Problem subclass.
	
	This function has been modified to return different information about the 
	search"""    
	h = memoize(h or problem.h, 'h')
	
	start_time = time.time()
	search_data = best_first_graph_search_modified(problem, lambda n: n.path_cost + h(n), display)	
	if search_data == None: # This only happens if the search fails
		print("ERROR: search failed")
		return None
	elapsed_time = time.time() - start_time
		
	return (elapsed_time, search_data[0], search_data[1])

def best_first_graph_search_modified(problem, f, display=False):
	"""Search the nodes with the lowest f scores first.
	You specify the function f(node) that you want to minimize; for example,
	if f is a heuristic estimate to the goal, then we have greedy best
	first search; if f is node.depth then we have breadth-first search.
	There is a subtlety: the line "f = memoize(f, 'f')" means that the f
	values will be cached on the nodes as they are computed. So after doing
	a best first search you can examine the f values of the path returned.

	This function has been modified to return different information about the 
	search."""
	frontier_nodes_popped = 0  # for tracking when nodes are popped

	f = memoize(f, 'f')
	node = Node(problem.initial)
	frontier = PriorityQueue('min', f)
	frontier.append(node)
	explored = set()
	while frontier:
		node = frontier.pop()
		frontier_nodes_popped += 1
		if problem.goal_test(node.state):
			if display:
				print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
			return (frontier_nodes_popped, node.path_cost)	# returns the length of the path and the frontier nodes popped
		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				frontier.append(child)
			elif child in frontier:
				if f(child) < frontier[child]:
					del frontier[child]
					frontier.append(child)
	return None

	
def manhattan_distance_heuristic(eight_puzzle):
	""" Calculates the manhattan distance of a state compared with the goal state."""

	# Currying this function so I can pass it to astar_search()
	def inner(node):
		sum = 0
		current_state = node.state
		goal_state = eight_puzzle.goal	

		# I ignore the zero tile in order for this heuristic to be admissible.
		for i in range(1, len(current_state)):
			hdif = abs( i % 3 - goal_state.index(current_state[i]) % 3 )
			vdif = abs( i // 3 - goal_state.index(current_state[i]) // 3 )
			sum += hdif + vdif
		
		return sum

	return inner

# Am ignoring the zero tile in order for the heuristic to be admissible.
def mt_heuristic_fixed(puzzle):
	
	def inner(node):
		return sum(s != g and s != 0 and g != 0 for (s, g) in zip(node.state, puzzle.goal))
	
	return inner	

def max_heuristic(eight_puzzle):
	"""Combines the misplaced tile heuristic and the manhattan distance heuristic."""

	# Currying to make this function passable
	def inner(node): 
		return max( mt_heuristic_fixed(eight_puzzle)(node), manhattan_distance_heuristic(eight_puzzle)(node) ) 

	return inner


def q2_analysis():
	print("start q2 analysis")
		
	# make 10 puzzle instances.  NOTE: you can pass 30 to make_rand_8puzzle() to speed up tests.
	puzzle_list = [make_rand_8puzzle() for i in range(0, 10)]  
	puzzle_data = []  # this is a list of dictionaries holding test data 
 
	for puzzle in puzzle_list:
		data = {}
		
		# solve and fill data
		mt_data = astar_search_modified(puzzle, mt_heuristic_fixed(puzzle))
		md_data = astar_search_modified(puzzle, manhattan_distance_heuristic(puzzle))
		max_data = astar_search_modified(puzzle, max_heuristic(puzzle))

		data["a*mt time"] 				= mt_data[0]  # in s
		data["a*mt frontier popped"] 	= mt_data[1]
		data["a*mt len"] 				= mt_data[2]
		
		data["a*md time"] 				= md_data[0]
		data["a*md frontier popped"] 	= md_data[1]
		data["a*md len"] 				= md_data[2]
		
		data["a*max time"] 				= max_data[0]
		data["a*max frontier popped"] 	= max_data[1]
		data["a*max len"] 				= max_data[2]
		
		puzzle_data.append(data)
		print( "." )  # to show progress when solutions take a long time

	print("analysis results:")
	print("a*mt time", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*mt time"]), end=",")
	print("", end="\n")
	print("a*md time", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*md time"]), end=",")
	print("", end="\n")
	print("a*max time", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*max time"]), end=",")
	print("", end="\n")
	print("a*mt frontier popped", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*mt frontier popped"]), end=",")
	print("", end="\n")
	print("a*md frontier popped", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*md frontier popped"]), end=",")
	print("", end="\n")
	print("a*max frontier popped", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*max frontier popped"]), end=",")
	print("", end="\n")
	print("a*mt len", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*mt len"]), end=",")
	print("", end="\n")
	print("a*md len", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*mt len"]), end=",")
	print("", end="\n")
	print("a*max len", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*mt len"]), end=",")
	print("", end="\n")
	print("done analysis \n")

def q2_tests():
	# run tests
	print("q2 tests - testing solving and search methods")
	
	for i in range(0, 2):
		print( "########## test {} ##########".format(i) )
		puzzle = make_rand_8puzzle(40) 

		print( "puzzle initial state:" )
		display( puzzle.initial )
		print( "", end="\n" )

		print( "solving puzzle using mt heuristic:" )
		display( astar_search(puzzle, mt_heuristic_fixed(puzzle)).state )
		time, _, sol_len = astar_search_modified(puzzle, puzzle.h)
		print( "time = {}, solution length = {} \n".format(time, sol_len) ) 
			
		print( "solving puzzle using md heuristic:" )
		display( astar_search(puzzle, manhattan_distance_heuristic(puzzle)).state )
		time, _, sol_len = astar_search_modified(puzzle,  manhattan_distance_heuristic(puzzle))
		print( "time = {}, solution length = {} \n".format(time, sol_len) ) 
			
		print( "solving puzzle using max heuristic:" )
		display( astar_search(puzzle, max_heuristic(puzzle)).state )
		time, _, sol_len = astar_search_modified(puzzle, max_heuristic(puzzle))
		print( "time = {}, solution length = {} \n".format(time, sol_len) ) 
		
	print("done q2 tests --------------------------- \n")


# *************************************************************************** #
# Question 3:

class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 2x2 intersecting 
	a 3x2 board with one tile. A state is represented as ... 

	The board & goal state looks like this:
		
        [1][2]
		[3][4][5][6]
		   [7][8][*]	
	
	"""

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)


    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)
    
    def actions(self, state):
        """ Returns which actions can be executed at any state. This function
		defines most of the shape of the puzzle. """

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
        Action is assumed to be a valid action in the state. """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

		# The only difference is the up and down mappings.
        delta = {
			'UP': -2 if blank == 2 or blank == 3 else -3, 
			'DOWN': 2 if blank == 0 or blank == 1 else 3, 
			'LEFT': -1, 
			'RIGHT': 1
		}
		
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal
    
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return mt_heuristic_fixed(self)(node)    

# Nearly the same as 8puzzle version
def make_rand_duck_puzzle(swaps=1000):
    """Returns a new instance of an EightPuzzle problem with a random initial 
    state that is solvable"""

    # init puzzle	
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = DuckPuzzle(state)
	
    # do n legal moves <where n=swaps>
    for i in range(0, swaps):
        action = random.choice(puzzle.actions(state))  # pick random possible action
        state = puzzle.result(state, action)  # apply the possible action

    puzzle.initial = state  # update the action
	
	# do error check before returning
    return puzzle

def display_duck_puzzle(state):
    state_cpy = ["*" if v == 0 else v for v in state] # change 0 into *
    print( "{} {}".format(state_cpy[0], state_cpy[1]) )
    print( "{} {} {} {}".format(state_cpy[2], state_cpy[3], state_cpy[4], state_cpy[5]) )
    print( "{} {} {} {}".format(" ", state_cpy[6], state_cpy[7], state_cpy[8]) )

def manhattan_distance_heuristic_duck_puzzle(duck_puzzle):
	""" Calculates the manhattan distance of a state compared with the goal 
	state for a duck_puzzle."""

	# Currying this function so I can pass it to astar_search()
	def inner(node):
		sum = 0
		current_state = node.state
		goal_state = duck_puzzle.goal	

        # Am ignoring the zero tile in order for the heuristic to be admissible.
		for i in range(1, len(current_state)):
			# these map indicies to their positions on the duck grid.
			xpos_map = {0:0, 1:1, 2:0, 3:1, 4:2, 5:3, 6:1, 7:2, 8:3} 
			get_ypos = lambda i: (0 if i < 2 else (2 if i > 5 else 1)) 
			
			current_x = xpos_map[i]
			goal_x = xpos_map[ goal_state.index(current_state[i]) ]

			current_y = get_ypos(i) 
			goal_y = get_ypos( goal_state.index(current_state[i]) ) 
			
			hdif = abs( current_x - goal_x )
			vdif = abs( current_y - goal_y )
			sum += hdif + vdif
		
		return sum

	return inner

def max_heuristic_duck_puzzle(duck_puzzle):
	"""Combines the misplaced tile heuristic and the manhattan distance heuristic."""

	# Currying to make this function passable
	def inner(node): 
		return max( duck_puzzle.h(node), manhattan_distance_heuristic_duck_puzzle(duck_puzzle)(node) ) 

	return inner


def q3_analysis():
	print("start q3 analysis - duck puzzle")
		
	# make 10 puzzle instances.  	
	puzzle_list = [make_rand_duck_puzzle() for i in range(0, 10)]  
	puzzle_data = []  # this is a list of dictionaries holding test data 
 
	for puzzle in puzzle_list:
		data = {}
		
		# solve and fill data
		mt_data = astar_search_modified(puzzle, puzzle.h)
		md_data = astar_search_modified(puzzle, manhattan_distance_heuristic_duck_puzzle(puzzle))
		max_data = astar_search_modified(puzzle, max_heuristic_duck_puzzle(puzzle))

		data["a*mt time"] 				= mt_data[0]  # in s
		data["a*mt frontier popped"] 	= mt_data[1]
		data["a*mt len"] 				= mt_data[2]
		
		data["a*md time"] 				= md_data[0]
		data["a*md frontier popped"] 	= md_data[1]
		data["a*md len"] 				= md_data[2]
		
		data["a*max time"] 				= max_data[0]
		data["a*max frontier popped"] 	= max_data[1]
		data["a*max len"] 				= max_data[2]
		
		puzzle_data.append(data)
		print( "." ) 
	
	# output csv data
	print("analysis results:")
	print("a*mt time", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*mt time"]), end=",")
	print("", end="\n")
	print("a*md time", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*md time"]), end=",")
	print("", end="\n")
	print("a*max time", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*max time"]), end=",")
	print("", end="\n")
	print("a*mt frontier popped", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*mt frontier popped"]), end=",")
	print("", end="\n")
	print("a*md frontier popped", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*md frontier popped"]), end=",")
	print("", end="\n")
	print("a*max frontier popped", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*max frontier popped"]), end=",")
	print("", end="\n")
	print("a*mt len", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*mt len"]), end=",")
	print("", end="\n")
	print("a*md len", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*mt len"]), end=",")
	print("", end="\n")
	print("a*max len", end=",")
	for dat in puzzle_data:
		print("{}".format(dat["a*mt len"]), end=",")
	print("", end="\n")
	print("done analysis \n")

def q3_tests():
	# run tests
	print("q3 tests - testing solving and search methods with duck puzzle")
	
	for i in range(0, 2):
		print( "########## test {} ##########".format(i) )
		puzzle = make_rand_duck_puzzle() 

		print( "puzzle initial state:" )
		display_duck_puzzle( puzzle.initial )
		print( "", end="\n" )

		print( "solving puzzle using mt heuristic:" )
		display_duck_puzzle( astar_search(puzzle, puzzle.h).state )
		time, _, sol_len = astar_search_modified(puzzle, puzzle.h)
		print( "time = {}, solution length = {} \n".format(time, sol_len) ) 
			
		print( "solving puzzle using md heuristic:" )
		display_duck_puzzle( astar_search(puzzle, manhattan_distance_heuristic_duck_puzzle(puzzle)).state )
		time, _, sol_len = astar_search_modified(puzzle,  manhattan_distance_heuristic_duck_puzzle(puzzle))
		print( "time = {}, solution length = {} \n".format(time, sol_len) ) 
			
		print( "solving puzzle using max heuristic:" )
		display_duck_puzzle( astar_search(puzzle, max_heuristic_duck_puzzle(puzzle)).state )
		time, _, sol_len = astar_search_modified(puzzle, max_heuristic_duck_puzzle(puzzle))
		print( "time = {}, solution length = {} \n".format(time, sol_len) ) 
		
	print("done q3 tests --------------------------- \n")


# *************************************************************************** #


if __name__ == "__main__":
	q1_tests()	
	q2_tests()	
	q3_tests()	
	
	q2_analysis()	
	q3_analysis()
	
