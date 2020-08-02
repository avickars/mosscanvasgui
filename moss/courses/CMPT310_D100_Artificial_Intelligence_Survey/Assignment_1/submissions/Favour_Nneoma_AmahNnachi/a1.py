# a1.py

from search import *
import random
import time

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
    removedNode = 0
    while frontier:
        node = frontier.pop()
        removedNode +=1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node , removedNode
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None , removedNode


def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        # Don't include zero. The heuristic function never ever overestimate the true cost
        # but the default one does

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))


#Question 1

#returns a new instance of an EightPuzzle problem
#generate a list then check if its solvable
def make_rand_8puzzle():
	randlist = [0,1,2,3,4,5,6,7,8]
	
	random.shuffle(randlist)
	
	#tuple(seq) Converts a list into tuple.
	#create the instance of EightPuzzle
	EightPuzzleTuple = EightPuzzle(tuple(randlist))


	while EightPuzzleTuple.check_solvability(randlist) == False:
		random.shuffle(randlist) #shuffle again
		
		EightPuzzleTuple = EightPuzzle(tuple(randlist))
	return EightPuzzleTuple



def display(state):
	#state is a tuple 
	for start in range(0,9) : #1st row
		if start%3 == 0 and start != 0:
			if state[start] == 0 :
				print("\n", end= "" )
				print ("*" , end= " ")
			else : 
				print("\n", end= "" )
				print (state[start], end = " ")
		else:
			if state[start] == 0 :
				print ("*" , end= " ")
			else : 
				print (state[start], end = " ")


#Question 2
#Create 20 random 8-puzzle instances


def manhattanDistanceHeuristic(node):

	state = node.state
	x_value,y_value = 0, 0
	index =[[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
	goal_state ={ 0: [2,2], 1: [0,0], 2: [0,1], 3: [0,2], 4: [1,0], 5: [1,1], 6: [1,2], 7: [2,0], 8: [2,1] }

	size = len(state)
	new_state = {}
	for new_index in range(size):
		new_state[state[new_index]] = index[new_index]
	
	manhattan_distance = 0

	for n in range(1,9):
		for m in range(0,2):
			manhattan_distance += abs(goal_state[n][m] - new_state[n][m]) 
	return manhattan_distance



#A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic
def maxFunction(node):
	#state is a tuple
	nodeState = node.state
	tempObj = EightPuzzle(nodeState)
	operand1= tempObj.h(node)
	operand2= manhattanDistanceHeuristic(node)
	 
	return max(operand1, operand2)





#make a for loop that 20 instances the following
for num in range(0,20):

	lengthOfSolution = 0;
	initial_8puzzle = make_rand_8puzzle() #store a random 8-puzzle instance in initial_8puzzle variable 
	Astar_8puzzle = initial_8puzzle
	manhattan_8puzzle = initial_8puzzle

	print("The initial state of the puzzle is: ")

	display(initial_8puzzle.initial)

	print("\nMisplaced tile heuristic")
	start_time = time.time()
	result, sumOfRemoved = astar_search(Astar_8puzzle)# specify the h function and display 
	elapsed_time = time.time() - start_time
	print(f'\nThe total running time for Misplaced tile heuristic in seconds is: {elapsed_time}s')
	lengthOfResult = len(result.solution())
	print('\nThe length of the solution is : ', lengthOfResult)
	print('\nThe total number of nodes that were removed from frontier: ', sumOfRemoved )


	print("\nManhattan Distance heuristic")
	start_time = time.time()
	result , sumOfRemoved = astar_search(manhattan_8puzzle, h = manhattanDistanceHeuristic)
	elapsed_time = time.time() - start_time
	print(f'\nThe total running time for Manhattan Distance heuristic in seconds is : {elapsed_time}s')
	lengthOfResult = len(result.solution())
	print('\nThe length of the solution is : ', lengthOfResult)
	print('\nThe total number of nodes that were removed from frontier: ' , sumOfRemoved)


	print("\nMax of Misplaced tile heuristic AND Manhattan distance")
	start_time = time.time()
	result , sumOfRemoved = astar_search(initial_8puzzle, h = maxFunction)
	elapsed_time = time.time() - start_time
	print(f'\nThe total running time for  max of the misplaced tile heuristic and the Manhattan distance in seconds is : {elapsed_time}s')
	lengthOfResult = len(result.solution())
	print('\nThe length of the solution is : ', lengthOfResult)
	print('\nThe total number of nodes that were removed from frontier: ' , sumOfRemoved)
#Question 3 : The House-Puzzle


