
from search import *
import random
import math
import time

def make_rand_8puzzle():
	state = (1,2,3,4,5,6,7,8,0)
	newPuzzle = EightPuzzle(state)
	shuffleCounter = 150

	for x in range(0,shuffleCounter):
		moves = newPuzzle.actions(state)
		move = random.choice(moves)
		state = newPuzzle.result(state,move)
	return EightPuzzle(state)


def display(state):
	listState = list(state)
	listState[state.index(0)] = '*'
	for x in listState:
		if listState.index(x) == 2 or listState.index(x) == 5 or listState.index(x) == 8:
			print(x)
		else:
			print(x,end=" ")

goal=[1,2,3,4,5,6,7,8,0]

def linear(node):
    return sum([1 if node.state[i] != goal[i] else 0 for i in range(8)])

def manhattan(node):
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

def sqrt_manhattan(node):
    state = node.state
    index_goal = {0:[2,2], 1:[0,0], 2:[1,0], 3:[2,0], 4:[0,1], 5:[1,1], 6:[2,1], 7:[0,2], 8:[1,2]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    x, y = 0, 0
    
    for i in range(len(state)):
        index_state[state[i]] = index[i]
    
    mhd = 0
    
    for i in range(8):
        for j in range(2):
            mhd = (index_goal[i][j] - index_state[i][j])**2 + mhd
    
    return math.sqrt(mhd)

def h(node):
	return sum(s != g for (s, g) in zip(node.state, goal))

def max_heuristic(node):
    score1 = manhattan(node)
    score2 = h(node)
    return max(score1, score2)



def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    popCounter = 0 
    delCounter = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        popCounter += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print("Number of nodes popped:",popCounter)
            print("Number of nodes removed:", delCounter)
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    delCounter += 1
                    frontier.append(child)
    return None

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def testEight(name,f,puzzle):
	print(name)
	start_time = time.time()
	solution = astar_search(puzzle,f).solution()
	elapsed_time = time.time() - start_time
	print("numbers of tiles moved:",len(solution))
	print("time taken:",elapsed_time)
	print("solution:",solution)

def runTestEight():

	for i in range(10):		
		print()
		print("Test ",i+1, ":")
		puzzleMade = make_rand_8puzzle()
		display(puzzleMade.initial)
		testEight("linear",puzzleMade.h,puzzleMade)
		testEight("manhattan",manhattan,puzzleMade)
		testEight("max heuristic",max_heuristic,puzzleMade)	


runTestEight()

class DuckPuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    	super().__init__(initial, goal)	

    def find_blank_square(self, state):
        return state.index(0)
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square in (0,1,4,5):
        	possible_actions.remove("UP")

        if index_blank_square in (2,6,7,8):
        	possible_actions.remove("DOWN")

        if index_blank_square in (0,2,6):
        	possible_actions.remove("LEFT")

        if index_blank_square in (1,5,8):
        	possible_actions.remove("RIGHT")

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        deltaBody = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        deltaHead = {'UP': -2,'DOWN': 2,'LEFT': -1,'RIGHT': 1}
        deltaMiddle = {'UP': -2,'DOWN': 3,'LEFT': -1,'RIGHT': 1}
        if blank < 3:
        	neighbor = blank + deltaHead[action]
        elif blank == 3:
        	neighbor = blank + deltaMiddle[action]
        else:
        	neighbor = blank + deltaBody[action]


        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

def make_rand_duckPuzzle():
	state = (1,2,3,4,5,6,7,8,0)
	newPuzzle = DuckPuzzle(state)
	shuffleCounter = 150

	for x in range(0,shuffleCounter):
		moves = newPuzzle.actions(state)
		move = random.choice(moves)
		state = newPuzzle.result(state,move)
	return DuckPuzzle(state)

def displayDuck(state):
	listState = list(state)
	listState[state.index(0)] = '*'
	for x in listState:
		if listState.index(x) == 1 or listState.index(x) == 5 or listState.index(x) == 8:
			print(x)
		elif listState.index(x) == 6:
			print(" ",x,end=" ")
		else:
			print(x,end=" ")	



def linear_duck(node):
    return sum([1 if node.state[i] != goal[i] else 0 for i in range(8)])

def manhattan_duck(node):
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

def sqrt_manhattan_duck(node):
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
            mhd = (index_goal[i][j] - index_state[i][j])**2 + mhd
    
    return math.sqrt(mhd)

def max_heuristic_duck(node):
    score1 = manhattan_duck(node)
    score2 = h(node)
    return max(score1, score2)

def testDuck(name,f,puzzle):
	print(name)
	start_time = time.time()
	solution = astar_search(puzzle,f).solution()
	elapsed_time = time.time() - start_time
	print("numbers of tiles moved:",len(solution))
	print("time taken:",elapsed_time)
	print("solution:",solution)

def runTestDuck():

	for i in range(10):
		print()
		print("Test ",i+1,":")
		puzzleMade = make_rand_duckPuzzle()
		displayDuck(puzzleMade.initial)
		testDuck("linear_duck",puzzleMade.h,puzzleMade)
		testDuck("manhattan_duck",manhattan_duck,puzzleMade)
		testDuck("max max_heuristic_duck",max_heuristic_duck,puzzleMade)

runTestDuck()


