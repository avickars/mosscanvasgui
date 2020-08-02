from search import *
import random
import time



#Quesiton 1:

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    #Counting number of nodes removed from frontier:
    total_removed = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    #Appending very first node "inital state"
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        #counter for total nodes poppes
        total_removed += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, total_removed
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, total_removed


def display(board):
	for index, item in enumerate(board):
		if item == 0:
			if index == 2 or index ==5 or index == 8:
				print("*")
			else:
				print("*", end = " ")
		else:
			if index == 2 or index ==5 or index == 8:
				print(item)
			else:
				print(item, end = " ")

#tuple1 = (3,0,2,1,8,7,4,6,5)
#display(tuple1)


def make_rand_8puzzle():
	#Function for generating 8puzzle
	#First have a list, shuffle then typecast to be tuplethen Eight Puzzle object

	num_list = [0,1,2,3,4,5,6,7,8]
	random.shuffle(num_list)
	puzzle = EightPuzzle(tuple(num_list))

	#Checking if the 8 puzzle is solvable
	while(puzzle.check_solvability(num_list)==False):
		random.shuffle(num_list)
		puzzle = EightPuzzle(tuple(num_list))

	return puzzle



#Question 2: 
 ######################################################################################################################################

#manhatten distance heursitc function

def manhanttan_h(board):
	values = { 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0],5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1], 0:[2,2]}
	origin = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
	current = []
	zero_index = 0
	tuple1 = board.state
	for i in tuple1:
		if tuple1[i] == 0:
			zero_index = i
		current.append(values.get(i))
	total = 0
	for i in range(9):
		for j in range(2):
			total += abs(current[i][j]-origin[i][j])

	#do not account for 0
	for k in range(2):
		total -= abs(current[zero_index][k]-origin[zero_index][k])


	return total

#implemented my own misplaced tile function so that it does not include the "0"
def misplaced_tile(board):
	misplaced = 0
	original = (1,2,3,4,5,6,7,8,0)
	tuple1 = board.state
	for i in tuple1:
		if tuple1[i] !=original[i]:
			misplaced +=1
	#do not account for 0
	if tuple1[8] != original[8]:
		misplaced -= 1
	#print("This is the number of misplaced_tile ", misplaced)

	return misplaced



#Getting the max between default heuristic and manhattan heuristic
def max_both(board):
	return max(manhanttan_h(board),misplaced_tile(board))


def timing_8puzzle():
	puzzle = make_rand_8puzzle()
	#puzzle = EightPuzzle((0, 4, 5, 6, 1, 8, 3, 7, 2)    )
	astar_default = puzzle
	manhattan = puzzle
	max_b = puzzle
    
	print("Results for astar default:")
	start = time.time()
	result_astar, total_nodes = astar_search(astar_default, h =misplaced_tile)
	total_time = time.time() - start
	print(astar_default.initial)
	print(f'Total time (in seconds): {total_time}s')
	print("Total number of tiles moved: ", len(result_astar.solution()))
	print("Total nimber of nodes removed: ", total_nodes)
    



	print("Results for using manhatten:")
	start2 = time.time()
	result_manhattan, total_nodes2 = astar_search(manhattan, h = manhanttan_h)
	total_time2 = time.time() - start2
	print(f'Total time (in seconds): {total_time2}s')
	print("Total number of tiles moved: ", len(result_manhattan.solution()))
	print("Total number of nodes removed: ", total_nodes2)

	print("Results for using max of the two:")
	start3 = time.time()
	result_max, total_nodes3 = astar_search(max_b, h = max_both)
	total_time3 = time.time() - start3
	print(f'Total time (in seconds): {total_time3}s')
	print("Total number of tiles moved: ", len(result_max.solution()))
	print("Total number of nodes removed: ", total_nodes3)




for i in range(1,10):
	print("This is the 8-puzzle, trial ", i )
	timing_8puzzle()


########################################################################################################################################
##Question 3 Duck Puzzle 



##display for duck puzzle



class DuckPuzzle(Problem):


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
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        if index_blank_square == 2:
        	possible_actions.remove("DOWN")
        	possible_actions.remove("LEFT")
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 6:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
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

        if blank == 0 or blank == 1 or blank == 2:
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


def display_duck(board):
	for index, item in enumerate(board):
		if item ==0:
			if index == 0 or index == 2 or index == 3 or index == 4 or index == 7: 
				print("*", end = ' ')
			if index == 1 or index == 5:
				print("*")
			if index == 6:
				print(' ', end = ' ')
				print("*", end = ' ')
			if index == 8:
				print("*")
		else:
			if index == 0 or index == 2 or index == 3 or index == 4 or index == 7: 
				print(item, end = ' ')
			if index == 1 or index == 5:
				print(item)
			if index == 6:
				print(' ', end = ' ')
				print(item, end = ' ')
			if index == 8:
				print(item)

#manhanttan heurisitic for duck puzzle 

def manhanttan_h_duck(board):
	values = { 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1],5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2], 0:[2,3]}
	origin = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
	current = []
	zero_index = 0
	tuple1 = board.state
	for i in tuple1:
		if tuple1[i] == 0:
			zero_index = i
		current.append(values.get(i))
	total = 0
	for i in range(9):
		for j in range(2):
			total += abs(current[i][j]-origin[i][j])

	#do not account for 0
	for k in range(2):
		total -= abs(current[zero_index][k]-origin[zero_index][k])


	return total

###max of both heurisitics

def max_both_duck(board):
	return max(manhanttan_h_duck(board),misplaced_tile(board))

def make_rand_duck():
	#If we start with goal state and continuously make legal moves on it, it will always be a valid duck puzzle, 
	#do not need to check whether or not the state is solvable or not.
	duck = DuckPuzzle((1,2,3,4,5,6,7,8,0))
	initial = (1,2,3,4,5,6,7,8,0)
	for i in range(1000):
		index = duck.find_blank_square(initial)
		#possible actions for current state
		p = duck.actions(initial)
		#out of the list get a random item from the list and perform the action
		move = random.choice(p)
		result = duck.result(initial,move)
		initial = result

	final = DuckPuzzle(initial)
	return final



def timing_duckpuzzle():
	puzzle = make_rand_duck()
	#puzzle = DuckPuzzle((4, 1, 2, 5, 3, 0, 8, 6, 7) )
	astar_default = puzzle
	manhattan = puzzle
	max_b = puzzle
    
	print("Results for astar default:")
	start = time.time()
	result_astar, total_nodes = astar_search(astar_default, h =misplaced_tile)
	total_time = time.time() - start
	print(puzzle.initial)
	print(f'Total time (in seconds): {total_time}s')
	print("Total number of tiles moved: ", len(result_astar.solution()))
	print("Total nimber of nodes removed: ", total_nodes)
    



	print("Results for using manhatten:")
	start2 = time.time()
	result_manhattan, total_nodes2 = astar_search(manhattan, h = manhanttan_h_duck)
	total_time2 = time.time() - start2
	print(f'Total time (in seconds): {total_time2}s')
	print("Total number of tiles moved: ", len(result_manhattan.solution()))
	print("Total number of nodes removed: ", total_nodes2)

	print("Results for using max of the two:")
	start3 = time.time()
	result_max, total_nodes3 = astar_search(max_b, h = max_both_duck)
	total_time3 = time.time() - start3
	print(f'Total time (in seconds): {total_time3}s')
	print("Total number of tiles moved: ", len(result_max.solution()))
	print("Total number of nodes removed: ", total_nodes3)



for i in range(1,10):
	print("This is the duck puzzle, trial ", i )
	timing_duckpuzzle()



