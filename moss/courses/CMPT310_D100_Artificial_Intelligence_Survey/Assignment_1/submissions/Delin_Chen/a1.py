# a1.py

import random
import time

from search import *

def best_first_graph_search(problem, f):
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
    global removedFrontier
    removedFrontier = 0
    while frontier:
        node = frontier.pop()
        removedFrontier += 1
        if problem.goal_test(node.state):
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

class EightPuzzle(Problem):
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

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

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

    def manhattan(self, node):
        state = node.state
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index_state = {}
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        distance = 0

        for i in range(len(state)):
            index_state[state[i]] = index[i]
        
        for i in range(9):
           distance += abs(index_goal[i][0] - index_state[i][0]) + abs(index_goal[i][1] - index_state[i][1])
        
        return distance

    def maxHeuristic(self, node):
        """
        Return the max of the misplaced tile heuristic and the Manhattan distance heuristic
        """
        return (max(self.h(node), self.manhattan(node)))

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

def astar_searchMaxHeuristic(problem, h=None):
    # A*-search using the Max value between Manhattan distance heurisitic and Misplaced tile heuristic 

    h = memoize(h or problem.maxHeuristic, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

def astar_searchManhattan(problem, h=None):
    # A*-search using the Manhattan distance heuristic 

    h = memoize(h or problem.manhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))




# ______________________________________________________________________________

def make_rand_8puzzle():
	puzzleNum = list(range(9))
	random.shuffle(puzzleNum)
	puzzle = EightPuzzle(tuple(puzzleNum))
	while (puzzle.check_solvability(puzzle.initial) == False):
		puzzleNum = list(range(9))
		random.shuffle(puzzleNum)
		puzzle = EightPuzzle(tuple(puzzleNum))
	return puzzle

def display(state):
	stateDisplay = list(state)
	for i in range(9):
		if (stateDisplay[i] == 0):
			stateDisplay[i] = "*"
	for i in range(3):
		print(stateDisplay[0+3*i],stateDisplay[1+3*i],stateDisplay[2+3*i])

# puzzle = make_rand_8puzzle()
# display(puzzle.initial)

for i in range(10): 

	puzzle = make_rand_8puzzle()
	display(puzzle.initial)

	#recording the time, pathcost, and #of frontier removed for default heurstic search algorithm
	start = time.time()
	result = astar_search(puzzle)
	end = time.time()
	print ("A*-Search using misplaced tile heuristic")
	print ("Time to solve the problem: ",end-start)
	print ("Path cost: ",result.path_cost)
	print ("# of nodes removed from frontier: ",removedFrontier, "\n")


	#recording the time, pathcost, and #of frontier removed for manhattan algorithm
	startMan = time.time()
	resultMan = astar_searchManhattan(puzzle)
	endMan = time.time()
	print ("A*-Search using Manhattan distance heuristic")
	print ("Time to solve the problem: ",endMan-startMan)
	print ("Path cost: ",resultMan.path_cost)
	print ("# of nodes removed from frontier: ",removedFrontier, "\n")


	#recording the time, pathcost, and #of frontier removed for max herustic
	startMax = time.time()
	resultMax = astar_searchMaxHeuristic(puzzle)
	endMax = time.time()
	print ("A*-Search using the max of misplaced tile heuristic and Manhattan distance heuristic")
	print ("Time to solve the problem: ",endMax-startMax)
	print ("Path cost: ",resultMax.path_cost)
	print ("# of nodes removed from frontier: ",removedFrontier, "\n")






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

        if index_blank_square in (0,2,6):     #tuple that contains squares that can't move left
            possible_actions.remove('LEFT')
        if index_blank_square in (0,1,4,5) :  #tuple that contains squares that can't move up
            possible_actions.remove('UP')    
        if index_blank_square in (1,5,8):     #tuples that contains squares that can't move right 
            possible_actions.remove('RIGHT')  
        if index_blank_square in (2,6,7,8) :  #tuple that contains squares that can't move down
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        """
        The Y shaped borad leads to 2 exceptions:
        
        0 1
        2 3 4 5
          6 7 8
        
        The index changes going up and down should be 2 in these 2 incases
        """

        deltaException = {'UP':-2, 'DOWN':2, 'LEFT':-1, 'RIGHT':1}
        blankException = (0,1)
        delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
        if blank in blankException:
           neighbor = blank + deltaException[action]
        else:
           neighbor = blank + delta[action]
        
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)


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

    def manhattan(self, node):
        state = node.state
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index_state = {}
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        distance = 0

        for i in range(len(state)):
            index_state[state[i]] = index[i]
        
        for i in range(9):
           distance += abs(index_goal[i][0] - index_state[i][0]) + abs(index_goal[i][1] - index_state[i][1])
        
        return distance

    def maxHeuristic(self, node):
        """
        Return the max of the misplaced tile heuristic and the Manhattan distance heuristic
        """
        return (max(self.h(node), self.manhattan(node)))



# ______________________________________________________________________________

def make_rand_dpuzzle():
	puzzleNum = list(range(9))
	random.shuffle(puzzleNum)
	puzzle = EightPuzzle(tuple(puzzleNum))
	while (puzzle.check_solvability(puzzle.initial) == False):
		puzzleNum = list(range(9))
		random.shuffle(puzzleNum)
		puzzle = EightPuzzle(tuple(puzzleNum))
	return puzzle

def displayd(state):
	stateDisplay = list(state)
	for i in range(9):
		if (stateDisplay[i] == 0):
			stateDisplay[i] = "*"
	
	print(stateDisplay[0],stateDisplay[1])
	print(stateDisplay[2],stateDisplay[3],stateDisplay[4],stateDisplay[5])
	print(" ",stateDisplay[6],stateDisplay[7],stateDisplay[8])


for i in range(10): 

	puzzle = make_rand_dpuzzle()
	displayd(puzzle.initial)


	#recording the time, pathcost, and #of frontier removed for default heurstic search algorithm
	start = time.time()
	result = astar_search(puzzle)
	end = time.time()
	print ("A*-Search using misplaced tile heuristic")
	print ("Time to solve the problem: ",end-start)
	print ("Path cost: ",result.path_cost)
	print ("# of nodes removed from frontier: ",removedFrontier, "\n")


	#recording the time, pathcost, and #of frontier removed for manhattan algorithm
	startMan = time.time()
	resultMan = astar_searchManhattan(puzzle)
	endMan = time.time()
	print ("A*-Search using Manhattan distance heuristic")
	print ("Time to solve the problem: ",endMan-startMan)
	print ("Path cost: ",resultMan.path_cost)
	print ("# of nodes removed from frontier: ",removedFrontier, "\n")


	#recording the time, pathcost, and #of frontier removed for max herustic
	startMax = time.time()
	resultMax = astar_searchMaxHeuristic(puzzle)
	endMax = time.time()
	print ("A*-Search using the max of misplaced tile heuristic and Manhattan distance heuristic")
	print ("Time to solve the problem: ",endMax-startMax)
	print ("Path cost: ",resultMax.path_cost)
	print ("# of nodes removed from frontier: ",removedFrontier, "\n")


