# a1.py
#student name : Yu Yang
#student id : 301308290

from search import *
import time
import random
import numpy as np #it is from TA
from collections import *

#reference:
# https://brilliant.org/wiki/a-star-search/
# https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html

# This is the assignment 1 to puzzles and measure time
# changed to display the length of frontier
"""def best_first_graph_search(problem, f, display= False):
    Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned.
    
    #count removed frontier
    removed = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        removed = removed +1
        ##print("node",node)
        if problem.goal_test(node.state):
            ##if display:
            ##print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print("Length of removed from frontier :", removed)
            return node
        explored.add(node.state)
        ##print("explored:",explored)
        for child in node.expand(problem):
            ##print("child",child)
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None
# end of the best_first_graph_search
"""



#Question 1 : Helper Functions
#Function 1 : make_rand_8puzzle()
#TA suggested np.random.permutation
def make_rand_8puzzle():
	state = tuple(np.random.permutation(9))
	puzzle = EightPuzzle(initial = state)
	
	while(True):
		if (puzzle.check_solvability(state)):
			
			
			return puzzle
		else:
			
			state = tuple(np.random.permutation(9))
			puzzle = EightPuzzle(initial = state)
			continue
#reference: https://www.w3schools.com/python/ref_string_format.asp
#Function 2 : display(state) to show current puzzle
def display(state):
	matrix = ""
	for i in range(9):
		if i == 3 or i ==6:
			matrix = matrix + "\n"
		if(state[i]!= 0 ):
			matrix = matrix + format(state[i]) + " "
		else:
			matrix = matrix + "* "

	print(matrix)

#define the cost=0 when using A*
def nullHeristic(puzzle):
    return 1




# Question 2 manhattan distance
def manhattan(puzzle):
	goal = {1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1], 0:[2,2]}
	location = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
	current_location = {}
	distance = 0
	for i in range(9):
		current_location[puzzle.state[i]] = location[i]
	
	for i in range(1,9):
		x = abs(goal[i][0] - current_location[i][0])
		y = abs(goal[i][1] - current_location[i][1])
		distance = distance + x + y

	return distance		

# Question 2 max of the misplaced tile heuristic and the Manhattan distance heuristic
def maxH(puzzle):
	return max(manhattan(puzzle), nullHeristic(puzzle))
	
	
	
	
	
# Question 3 Duck Puzzle Class
# Changes based on Search.py
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

        if (index_blank_square == 0) or (index_blank_square == 2) or (index_blank_square == 6):
            possible_actions.remove('LEFT')
        if (index_blank_square == 0) or (index_blank_square == 1) or (index_blank_square == 4) or (index_blank_square == 5):
            possible_actions.remove('UP')
        if (index_blank_square == 1) or (index_blank_square == 5) or (index_blank_square == 8):
            possible_actions.remove('RIGHT')
        if (index_blank_square == 6) or (index_blank_square == 7) or (index_blank_square == 8):
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
       
        blank = self.find_blank_square(state)
        new_state = list(state)
		
	# changed the delta, index differences will make a delta differences
        if(blank < 3):
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif(blank == 3):
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
    # for 2x2 part, because 0 can only go up and left when it reaches index 3 to
    # switch with 1,2,3,4, so at least 1,2,3 will always be in the 2x2 form.
        """ Checks if the given state is solvable """
        blank = self.find_blank_square(state)
        inversionPart1 = 0 # for 2x2 part
        inversionPart2 = 0 # for 2x3 part
        
        # calculate inversion for Part2 2x3 form
        for i in range(3, 7):
            if(state[i] != 0):
                for j in range(i+1, 8):
                    if(state[i] > state[j] and state[j] != 0):
                        inversionPart2 = inversionPart2 + 1
        
        # calculate inversion for Part1 2x2 form
        if(blank < 4 and state.index(1) < 4 and  state.index(2) < 4 and  state.index(3) < 4 ):
            for i in range(2):
                if(state[i] != 0):
                    for j in range(i+1, 3):
                        if(state[i] > state[j] and state[j] != 0):
                            inversionPart1 = inversionPart1 + 1
                if(blank < 2 and inversionPart1 % 2 == 1):
                    return inversionPart2 % 2 == 0
                elif(blank > 1 and blank < 4 and inversionPart1 % 2 == 0):
                    return inversionPart2 % 2 == 0   
        elif(blank > 3 and state.index(1) < 4 and  state.index(2) < 4 and  state.index(3) < 4 ):
            return inversionPart2 % 2 == 0
        return False

    def h(self, state):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        return sum(s != g for (s, g) in zip(state, self.goal))

def make_rand_Duck():
	state = tuple(np.random.permutation(9))
	puzzle = DuckPuzzle(initial = state)
	
	while(True):
		if (puzzle.check_solvability(state)):
			return puzzle
		else:
			
			state = tuple(np.random.permutation(9))
			puzzle = DuckPuzzle(initial = state)
			continue

def displayDuck(state):
	matrix = ""
	for i in range(9):
		if i == 2:
			matrix = matrix + "\n"
		if i == 6:
			matrix = matrix + "\n" + "  "
		if(state[i]!= 0 ):
			matrix = matrix + format(state[i]) + " "
		else:
			matrix = matrix + "* "
	print(matrix)
	
#main program
#changes are based on the the function prof. provided
def main():
    print("=============== Eight Puzzle part ===============")
    for i in range(11):
        q1 = make_rand_8puzzle()
        display(q1.initial)
		
# Eight Puzzle (test for A* only) 
# A*-search using the misplaced tile heuristic		
        start_time = time.time()
        result = astar_search(q1,h = nullHeristic)
		
        elapsed_time = time.time() - start_time
        print("--------------Using A* only--------------")
        print("Used ", elapsed_time, " to complete.")
        print("Length of solution: ", len(result.solution()))		
		
# Eight Puzzle (test for manhattan distance)	
# A*-search using the Manhattan distance heuristic
        start_time = time.time()
        result = astar_search(q1,h = manhattan)
		
        elapsed_time = time.time() - start_time
        print("--------------Using manhattan only--------------")
        print("Used ", elapsed_time, " to complete.")
        print("Length of solution: ", len(result.solution()))		

# Eight Puzzle
# A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic		
        start_time = time.time()
        result = astar_search(q1,h = maxH)
		
        elapsed_time = time.time() - start_time
        print("--------------Using max of two searches only--------------")
        print("Used ", elapsed_time, " to complete.")
        print("Length of solution: ", len(result.solution()))

    print("=============== Duck Puzzle part ===============")
    for i in range(11):
        q1 = make_rand_Duck()
        displayDuck(q1.initial)

# Duck Puzzle (test for A* only) 
# A*-search using the misplaced tile heuristic		
        start_time = time.time()
        result = astar_search(q1,h = nullHeristic)
		
        elapsed_time = time.time() - start_time
        print("--------------Using A* only--------------")
        print("Used ", elapsed_time, " to complete.")
        print("Length of solution: ", len(result.solution()))

# Duck Puzzle (test for manhattan distance)	
# A*-search using the Manhattan distance heuristic
        start_time = time.time()
        result = astar_search(q1,h = manhattan)
		
        elapsed_time = time.time() - start_time
        print("--------------Using manhattan only--------------")
        print("Used ", elapsed_time, " to complete.")
        print("Length of solution: ", len(result.solution()))	

# Duck Puzzle
# A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic		
        start_time = time.time()
        result = astar_search(q1,h = maxH)
		
        elapsed_time = time.time() - start_time
        print("--------------Using max of two searches only--------------")
        print("Used ", elapsed_time, " to complete.")
        print("Length of solution: ", len(result.solution()))
		
if __name__ == "__main__":
	main()
   
#End of Qustion 1
