#a1.py
from search import *
import random
import time



# Question 1: Helper Functions ---------------------------------------------------------------------------------------------------------------

def make_rand_8puzzle(): # Returns new state that is solvable

	initial_state = [1,2,3,4,5,6,7,8,0]
	puzzle = EightPuzzle(tuple(initial_state))
	
	random.shuffle(initial_state)
	boolean = True

	while boolean:
		if puzzle.check_solvability(initial_state) == True:
			puzzle = EightPuzzle(tuple(initial_state))
			boolean = False
		else:
			random.shuffle(initial_state)


	return puzzle, tuple(initial_state)
	

def display_eigth(state): # Prints the puzzle board 
	for i in range(9):
		if i != 2 and i != 5 and i != 8:
			if state[i] == 0:
				print("*", end = '')
			else:	
				print(state[i], end = '')
		else:
			if state[i] == 0:
				print("*")
			else:
				print(state[i])


# Testing Question 1
print("Implementing make_rand_8puzzle and display_eigth: \n")
eightpuzzle, initial = make_rand_8puzzle()
display_eigth(initial)


# # Question 2: ---------------------------------------------------------------------------------------------------------------------------------

def best_first_graph_search(problem, f, display=False): # Modified this function's code to show removed nodes
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
    removed = 0 # Counting how many removed nodes
    while frontier:
        node = frontier.pop()
        removed += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print(removed)
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

def mymanhattan(node): # Manhattan heuristic function for Eigth puzzle
	state = node.state
	index_goal = {0: [2,2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
	distance = 0
	indexes = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
	actual_indexes = [0,0,0,0,0,0,0,0,0]

	for x in range(9):
		actual_indexes[state[x]] = indexes[x]

	for y in range(9):
		if state[y] != 0:

			row = actual_indexes[state[y]][0]
			col = actual_indexes[state[y]][1]


			distance += abs(index_goal[state[y]][0]- row) + abs(index_goal[state[y]][1] - col)
	return distance

def max_heuristic(node): # Compares default and mymanhattan and returns the max. (Function taken from aima-python -> search.ipynb)
	 score1 = mymanhattan(node)
	 score2 = h(node)
	 return max(score1, score2)

#  10 Test Cases
print("\n")
for i in range(10): 
	print("Test", i+1, "\n")
	eight_puzzle, instance = make_rand_8puzzle()
	print("Puzzle Board: \n")
	display_eigth(instance)
	print("\n")

	# A* search using default heuristic
	print("Misplaced tiles heuristic -> Pops, Tiles moved and Time \n")
	start_time = time.time()
	print(count(astar_search(eight_puzzle).solution()))
	time_elapsed = time.time() - start_time
	print(str(time_elapsed) + "\n")

	# A* search using Manhattan
	print("Manhattan heuristic -> Pops, Tiles moved and Time \n")
	start_time = time.time()
	print(count(astar_search(eight_puzzle, mymanhattan).solution()))
	time_elapsed = time.time() -start_time
	print(str(time_elapsed) + "\n")


# Quesiton 3: Duck Puzzle -------------------------------------------------------------------------------------------------------------


# NOTE: Unfortunately, I wasn't able to run the code properly  in this question due to a calling the 
# Class/Attribute error in DuckPuzzle at the very end calling A* searches. I do understand it is my own 
# fault.
# I worked on it for a long time but couldn't figure it out, I still did my best to implement and test 
# the questions/functions/algorithms as I could. Sorry for the inconvenience!


class DuckPuzzle(Problem): # Create new Class of DuckPuzzle and implement same functions

    """ The problem of sliding tiles numbered from 1 to 8 on a modified board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state): # Modified for new possible actions that depend on index 
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        # New possible actions 
        no_left_moves = [0,2,6]
        no_up_moves = [0,1,4,5]
        no_down_moves = [2,6,7,8]
        no_right_moves = [1,5,8]

        if index_blank_square in no_left_moves:
            possible_actions.remove('LEFT')
        if index_blank_square in no_up_moves:
            possible_actions.remove('UP')
        if index_blank_square in no_right_moves:
            possible_actions.remove('RIGHT')
        if index_blank_square in no_down_moves:
            possible_actions.remove('DOWN')


        return possible_actions

    def result(self, state, action): # Modified for new dictionary keys that determine action
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        delta_3 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        delta_upper = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}

        if blank < 3:
        	neighbor = blank + delta_upper[action]

        elif blank == 3:
        	neighbor = blank + delta_3[action]

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

        return sum(s != g for (s, g) in zip(node.state, self.goal))


def make_rand_duckpuzzle(): # Creates and returns new state of puzzle
	d_initial_state = [1,2,3,4,5,6,7,8,0]
	duckpuzzle = DuckPuzzle(tuple(d_initial_state))

	random.shuffle(d_initial_state)
	boolean = True

	while boolean:
		if duckpuzzle.check_solvability(d_initial_state) == True:
			duckpuzzle = DuckPuzzle(tuple(d_initial_state))
			boolean = False
		else:
			random.shuffle(d_initial_state)

	return duckpuzzle, tuple(d_initial_state)


def display_duck(state): # Prints the puzzle
	for i in range(9):
		if i != 1 and i != 5 and i != 6 and i!= 8:
			if state[i] == 0:
				print("*", end = '')
			else:	
				print(state[i], end = '')
		elif i == 6:
			if state[i] == 0:
				print(" *", end = '')
			else:	
				print(" ", state[i], end = '')
		else:
			if state[i] == 0:
				print("*")
			else:
				print(state[i])


def mymanhattan_duck(node): # Manhattan heuristic function for Duck Puzzle. 
	state = node.state
	index_goal = {0: [2,3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
	distance = 0
	indexes = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
	actual_indexes = [0,0,0,0,0,0,0,0,0]

	for x in range(9):
		actual_indexes[state[x]] = indexes[x]

	for y in range(9):
		if state[y] != 0:

			row = actual_indexes[state[y]][0]
			col = actual_indexes[state[y]][1]


			distance += abs(index_goal[state[y]][0]- row) + abs(index_goal[state[y]][1] - col)
	return distance

# Testing implementation of duck puzzle
print("Implementing make_rand_duckpuzzle and display_duck: \n")
duckpuzzle, initial_state_duck = make_rand_duckpuzzle()
display_duck(initial_state_duck)

# Generate 10 tests - NOTE this is where my astar_search call showed error!!
for i in range(10): 
	print("Test", i+1, "\n")
	duck_puzzle, instance_duck = make_rand_duckpuzzle()
	print("Puzzle Board: \n")
	display_duck(instance_duck)
	print("\n")

	# A* search using default heuristic
	print("Misplaced tiles heuristic -> Pops, Tiles moved and Time \n")
	start_time = time.time()
	print(count(astar_search(duck_puzzle).solution()))
	time_elapsed = time.time() - start_time
	print(str(time_elapsed) + "\n")

	# A* search using Manhattan
	print("Manhattan heuristic -> Pops, Tiles moved and Time \n")
	start_time = time.time()
	print(count(astar_search(duck_puzzle, mymanhattan_duck).solution()))
	time_elapsed = time.time() -start_time
	print(str(time_elapsed) + "\n")


