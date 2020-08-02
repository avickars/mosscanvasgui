#a1.py
from search import * #imports all of code from the search.py file
import random #imports the "random" module in python 
import time # import time.time() function
import math #importing math functions for abs()


# NOTE i received giudence from TA Mohammad during tutorial sections 

#generating a random 8 puzzle by shuffling the tiles 
def make_rand_8puzzle():

	initialPuzzle = [1, 2, 3, 4, 5, 6, 7, 8, 0]
	
	#possible moves at each position 
	indx0 = [1, 3]
	indx1 = [0, 2, 4]
	indx2 = [1, 5]
	indx3 = [0, 4, 6]
	indx4 = [1, 3, 5, 7]
	indx5 = [2, 4, 8]
	indx6 = [3, 7]
	indx7 = [4, 6, 8]
	indx8 = [5, 7]

	#current index of the 0 (blank tile)
	currentIndex = 8

	#itirations of random swapping 
	for i in range(1000):
		
		if currentIndex == 0:
			swapIndex = random.choice(indx0)
		elif currentIndex == 1:
			swapIndex = random.choice(indx1)
		elif currentIndex == 2:
			swapIndex = random.choice(indx2)
		elif currentIndex == 3:
			swapIndex = random.choice(indx3)
		elif currentIndex == 4:
			swapIndex = random.choice(indx4)
		elif currentIndex == 5:
			swapIndex = random.choice(indx5)
		elif currentIndex == 6:
			swapIndex = random.choice(indx6)
		elif currentIndex == 7:
			swapIndex = random.choice(indx7)
		elif currentIndex == 8:
			swapIndex = random.choice(indx8)
		else:
			print("something is wrong...")

		temp = initialPuzzle[currentIndex]
		initialPuzzle[currentIndex] = initialPuzzle[swapIndex]
		initialPuzzle[swapIndex] = temp

		currentIndex = swapIndex

	scrambledPuzzle = tuple(initialPuzzle)

	newEightPuzzle = EightPuzzle(scrambledPuzzle) #new instance of a EightPuzzle object

	solveable = newEightPuzzle.check_solvability(newEightPuzzle.initial) #sets the boolean solveable to the return of check_solvability 

	

	#returns instance of EightPuzzle object with a solveable initial state

	if solveable == True: 
		return newEightPuzzle

	#in case it is not solveable 
	return "something is wrong..."



# q1 helper function for displaying the 3x3 grid
def display(state):

	for i in range(3): # basically for(int i = 0; i < 3; i++)
		for j in range(3):
			if state[i * 3 + j] == 0:
				print("* ", end = '') 
			else:
				print(str(state[i*3 + j]) + " ", end = '') # str() changes int to string, + does the concatenatoin 
		print('')		


#manhattan h function to calcualte the manhattan distance
def manhattan(node):
	state = node.state
	index_goal = {1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1], 0:[2,2]}
	index_state = {}
	index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]


	for i in range(len(state)):
		index_state[state[i]] = index[i]

	mhx = 0
	mhy = 0


	for i in range(1, 9):
		xDiff = 0
		yDiff = 0
		yDiff = abs(index_goal[i][0] - index_state[i][0]) #first [] is not the index of the dictionay, but the key, the index of the key doesnt matter
		xDiff = abs(index_goal[i][1] - index_state[i][1])
		mhx = xDiff + mhx
		mhy = yDiff + mhy

	return mhx + mhy


#slighted edited mixplaced h to not include 0 in the misplaced tile count
def h_1(node):
	""" Return the heuristic value for a given state. Default heuristic function used is 
	h(n) = number of misplaced tiles """

	return sum(s != g and s != 0 for (s, g) in zip(node.state, (1, 2, 3, 4, 5, 6, 7, 8, 0)))


# max between the original and manhattan function 
def max_h_manhattan(node):

	h_max = h_1(node)
	mahattan_max = manhattan(node)

	return(max(h_max, mahattan_max))



#edited astar_search algorithm to use the best_first_graph_serach_edited function
def astar_search_edited(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_edited(problem, lambda n: n.path_cost + h(n), display)


#edited to return the number of nodes removed
def best_first_graph_search_edited(problem, f, display=False):
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
    nodes_removed = 0
    while frontier:
        node = frontier.pop()
        nodes_removed = nodes_removed + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, nodes_removed]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None














##################################################################################################################################
######################################################### DUCK PUZZLE ############################################################


#duck puzzle class, slightly modified from the 8 puzzle
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


    # edited for the leagal actions at a given index
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')

        elif index_blank_square == 1:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')

        elif index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')

        #ALL MOVES POSSIBLE for index 3

        elif index_blank_square == 4:
            possible_actions.remove('UP')

        elif index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')

        elif index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')

        elif index_blank_square == 7:
            possible_actions.remove('DOWN')

        elif index_blank_square == 8:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')

        return possible_actions


    #limits for the legal moves and gives result of the action 
    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)


        if blank == 0:
            delta = {'UP': 0, 'DOWN': 2, 'LEFT': 0, 'RIGHT': 1}

        elif blank == 1:
            delta = {'UP': 0, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 0}

        elif blank == 2:
            delta = {'UP': -2, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}

        elif blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        elif blank == 4:
            delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        elif blank == 5:
            delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 0}

        elif blank == 6:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}

        elif blank == 7:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}

        elif blank == 8:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 0}

        
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



#generates a random duck puzzle by shuffling the board with legal moves
def make_rand_duck_puzzle():
	
	#same as the 8 puzzle, 
	initialPuzzle = [1, 2, 3, 4, 5, 6, 7, 8, 0]

	
	#possible moves at each position, different for the moves availabe in 8 puzzle 
	indx0 = [1, 2]
	indx1 = [0, 3]
	indx2 = [0, 3]
	indx3 = [1, 2, 4, 6]
	indx4 = [3, 5, 7]
	indx5 = [4, 8]
	indx6 = [3, 7]
	indx7 = [4, 6, 8]
	indx8 = [5, 7]

	#current index of the 0 (blank tile)
	currentIndex = 8

	# itirations of random swapping 
	for i in range(1000):
		
		if currentIndex == 0:
			swapIndex = random.choice(indx0)
		elif currentIndex == 1:
			swapIndex = random.choice(indx1)
		elif currentIndex == 2:
			swapIndex = random.choice(indx2)
		elif currentIndex == 3:
			swapIndex = random.choice(indx3)
		elif currentIndex == 4:
			swapIndex = random.choice(indx4)
		elif currentIndex == 5:
			swapIndex = random.choice(indx5)
		elif currentIndex == 6:
			swapIndex = random.choice(indx6)
		elif currentIndex == 7:
			swapIndex = random.choice(indx7)
		elif currentIndex == 8:
			swapIndex = random.choice(indx8)
		else:
			print("something is wrong...")

		temp = initialPuzzle[currentIndex]
		initialPuzzle[currentIndex] = initialPuzzle[swapIndex]
		initialPuzzle[swapIndex] = temp

		currentIndex = swapIndex

	scrambledPuzzle = tuple(initialPuzzle)

	newDuckPuzzle = DuckPuzzle(scrambledPuzzle) #new instance of a DuckPuzzle object

	#returns instance of DuckPuzzle object with a solveable initial state
	return newDuckPuzzle







################################################# DATA COLLECTION ##########################################################
############################################################################################################################



#looping through instances of EightPuzzle object for data collection 

for i in range(1, 11): 

	
	testPuzzle1 = make_rand_8puzzle()
	#testPuzzle1 = EightPuzzle((1,2,3,4,5,6,0,7,8))
	#testPuzzle1 = EightPuzzle((5,0,8,4,2,1,7,3,6))
	

	puzzleStart = testPuzzle1.initial
	testPuzzle2 = EightPuzzle(puzzleStart)
	testPuzzle3 = EightPuzzle(puzzleStart)
	print("EightPuzzle")
	print("Puzzle #", i)
	display(puzzleStart)


	############### misplaced h ###############
	start_time = time.time()
	nodes = astar_search_edited(testPuzzle1, h=h_1)
	end_time = time.time()
	elapsed_time = end_time - start_time


	print("Misplaced Heuristic")
	print("Elapsed time (seconds): " + str(elapsed_time))
	print("Path cost: " , nodes[0].path_cost)
	print("Total number of nodes removed: ", nodes[1])
	print("")




	############### manhattan h ###############
	start_time = time.time()
	nodes = astar_search_edited(testPuzzle2, h=manhattan)
	end_time = time.time()
	elapsed_time = end_time - start_time


	print("Manhattan Heuristic")
	print("Elapsed time (seconds): " + str(elapsed_time))
	print("Path cost: " , nodes[0].path_cost)
	print("Total number of nodes removed: ", nodes[1])
	print("")




	############### max h ###############
	start_time = time.time()
	nodes = astar_search_edited(testPuzzle3, h=max_h_manhattan)
	end_time = time.time()
	elapsed_time = end_time - start_time


	print("Max Heuristic")
	print("Elapsed time (seconds): " + str(elapsed_time))
	print("Path cost: " , nodes[0].path_cost)
	print("Total number of nodes removed: ", nodes[1])
	print("")





#looping through instances of DuckPuzzle object for data collection 

for i in range(1, 11): 

	
	testPuzzle1 = make_rand_duck_puzzle()

	puzzleStart = testPuzzle1.initial
	testPuzzle2 = DuckPuzzle(puzzleStart)
	testPuzzle3 = DuckPuzzle(puzzleStart)
	print("DuckPuzzle")
	print("Puzzle #", i)
	display(puzzleStart)


	############### misplaced h ###############
	start_time = time.time()
	nodes = astar_search_edited(testPuzzle1, h=h_1)
	end_time = time.time()
	elapsed_time = end_time - start_time


	print("Misplaced Heuristic")
	print("Elapsed time (seconds): " + str(elapsed_time))
	print("Path cost: " , nodes[0].path_cost)
	print("Total number of nodes removed: ", nodes[1])
	print("")




	############### manhattan h ###############
	start_time = time.time()
	nodes = astar_search_edited(testPuzzle2, h=manhattan)
	end_time = time.time()
	elapsed_time = end_time - start_time


	print("Manhattan Heuristic")
	print("Elapsed time (seconds): " + str(elapsed_time))
	print("Path cost: " , nodes[0].path_cost)
	print("Total number of nodes removed: ", nodes[1])
	print("")




	############### max h ###############
	start_time = time.time()
	nodes = astar_search_edited(testPuzzle3, h=max_h_manhattan)
	end_time = time.time()
	elapsed_time = end_time - start_time


	print("Max Heuristic")
	print("Elapsed time (seconds): " + str(elapsed_time))
	print("Path cost: " , nodes[0].path_cost)
	print("Total number of nodes removed: ", nodes[1])
	print("")