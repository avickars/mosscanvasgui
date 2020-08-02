#CMPT310 assignment 1
#Yoonhong Lee
#2020-05-29

from search import *
import time

#---Part 1--------------------------------------------------------------------------------#
# Class from aima-python/search.py 
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

    def h(self, node): #Updated the return value to exclude the blank tile
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))



def make_rand_8puzzle(): #Helper function to return a solvable eight puzzle
	randomized_state = [0,1,2,3,4,5,6,7,8]
	random.shuffle(randomized_state)
	eight_puzzle = EightPuzzle(tuple(randomized_state))

	while(eight_puzzle.check_solvability(tuple(randomized_state)) == False):
		random.shuffle(randomized_state)
		eight_puzzle = EightPuzzle(tuple(randomized_state))


	return eight_puzzle

def display(state):  #Method to display the puzzle 
	for i in range(len(state)):
		if(state[i] == 0):
			print('*', end=' ')
		else:
			print(state[i], end=' ')

		if(i % 3 == 2):
			print('')

#---Part 2--------------------------------------------------------------------------------#
# function from aima-python/search.py added counter to keep track of the removed nodes
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
    pop_counter = 0
    while frontier:
        node = frontier.pop()
        pop_counter = pop_counter + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, pop_counter
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, pop_counter

# function from aima-python/search.py
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# Manhattan heuristic implementation inspired by https://www.youtube.com/watch?v=GuCzYxHa7iA&t=153s
def manh(node):
	goal_state = [1,2,3,4,5,6,7,8,0]
	distance = 0
	for i in range(len(node.state)):
		if(node.state[i] != 0):
			for j in range(len(goal_state)):
				if(node.state[i] == goal_state[j]):
					ix = i % 3
					iy = i / 3

					jx = j % 3
					jy = j / 3

					distance = abs(ix - jx) + abs(iy - jy) + distance
	return distance

# A method for summarizing all 
# 		the total running time in seconds
# 		the length (i.e. number of tiles moved) of the solution
# 		that total number of nodes that were removed from frontier
def summary(random_puzzles):
	for i in range(len(random_puzzles)):
		print(f'Puzzle #{i + 1}')
		display(random_puzzles[i].initial)

		start_time = time.time()
		node, removed_nodes_count = astar_search(random_puzzles[i])
		elapsed_time = time.time() - start_time
		print('A*-search using the misplaced tile heuristic')
		print(f'elapsed time (in seconds): {elapsed_time}s')
		print(f'the length of the solution: {len(node.solution())}')
		print(f'the total number of nodes that were removed from frontier: {removed_nodes_count}')

		print()

		start_time = time.time()
		node, removed_nodes_count = astar_search(random_puzzles[i], manh)
		elapsed_time = time.time() - start_time
		print('A*-search using the Manhattan distance heuristic ')
		print(f'elapsed time (in seconds): {elapsed_time}s')
		print(f'the length of the solution: {len(node.solution())}')
		print(f'the total number of nodes that were removed from frontier: {removed_nodes_count}')
		print()
		
		def maxMisplacedAndMan(node):
			return max(random_puzzles[i].h(node), manh(node))

		start_time = time.time()
		node, removed_nodes_count = astar_search(random_puzzles[i], maxMisplacedAndMan)
		elapsed_time = time.time() - start_time
		print('A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic')
		print(f'elapsed time (in seconds): {elapsed_time}s')
		print(f'the length of the solution: {len(node.solution())}')
		print(f'the total number of nodes that were removed from frontier: {removed_nodes_count}')

		print()
		print('==================================================================================')

#---Part 3--------------------------------------------------------------------------------#
# Implmentation dervied from EightPuzzle class from aima-python/search.py
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

    def actions(self, state): # Method altered according to the shape of the puzzle
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 5 or index_blank_square == 8 or index_blank_square == 1:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square >= 6:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action): # Method altered according to the shape of the puzzle
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        delta_alt = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        delta_alt1 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        if blank in [0,1]:
        	neighbor = blank + delta_alt[action]
        elif blank in [2,3]:
        	neighbor = blank + delta_alt1[action]
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

    def h(self, node): #Updated the return value to exclude the blank tile
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

 #Method to display the puzzle 
def duck_puzzle_display(state):
	for i in range(len(state)):
		if(i == 6):
			print(' ', end=' ')

		if(state[i] == 0):
			print('*', end=' ')
		else:
			print(state[i], end=' ')

		if(i == 1 or i == 5 or i == 8):
			print('')

# Manhattan heuristic implementation inspired by https://www.youtube.com/watch?v=GuCzYxHa7iA&t=153s
def manh_duck_puzzle(node):
	goal_state = [1,2,3,4,5,6,7,8,0]
	distance = 0
	for i in range(len(node.state)):
		if(node.state[i] != 0):
			for j in range(len(goal_state)):
				if(node.state[i] == goal_state[j]):
					if i == 0 or i == 1:
						ix = i % 3
						iy = i / 3
					elif i >= 2 and i <= 5:
						ix = i - 2
						iy = 1
					else:
						ix = i - 5
						iy = 2

					if j == 0 or j == 1:
						jx = j % 3
						jy = j / 3
					elif j >= 2 and j <= 5:
						jx = j - 2
						jy = 1
					else:
						jx = j - 5
						jy = 2

					distance = abs(ix - jx) + abs(iy - jy) + distance
	return distance

def make_rand_duck_puzzle(): #Helper function to return a solvable duck puzzle
	randomized_state = (1,2,3,4,5,6,7,8,0)
	duck_puzzle = DuckPuzzle(randomized_state)

	for i in range(500):
		possible_actions = duck_puzzle.actions(duck_puzzle.initial)
		random.shuffle(possible_actions)
		randomized_state = duck_puzzle.result(duck_puzzle.initial, possible_actions[0])
		duck_puzzle = DuckPuzzle(randomized_state)

	return duck_puzzle

# A method for summarizing all 
# 		the total running time in seconds
# 		the length (i.e. number of tiles moved) of the solution
# 		that total number of nodes that were removed from frontier
def summary_duck(random_puzzles):
	for i in range(len(random_puzzles)):
		print(f'Puzzle #{i + 1}')
		duck_puzzle_display(random_puzzles[i].initial)

		start_time = time.time()
		node, removed_nodes_count = astar_search(random_puzzles[i])
		elapsed_time = time.time() - start_time
		print('A*-search using the misplaced tile heuristic')
		print(f'elapsed time (in seconds): {elapsed_time}s')
		print(f'the length of the solution: {len(node.solution())}')
		print(f'the total number of nodes that were removed from frontier: {removed_nodes_count}')
		print()

		start_time = time.time()
		node, removed_nodes_count = astar_search(random_puzzles[i], manh_duck_puzzle)
		elapsed_time = time.time() - start_time
		print('A*-search using the Manhattan distance heuristic ')
		print(f'elapsed time (in seconds): {elapsed_time}s')
		print(f'the length of the solution: {len(node.solution())}')
		print(f'the total number of nodes that were removed from frontier: {removed_nodes_count}')
		print()

		
		def maxMisplacedAndMan(node):
			return max(random_puzzles[i].h(node), manh_duck_puzzle(node))

		start_time = time.time()
		node, removed_nodes_count = astar_search(random_puzzles[i], maxMisplacedAndMan)
		elapsed_time = time.time() - start_time
		print('A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic')
		print(f'elapsed time (in seconds): {elapsed_time}s')
		print(f'the length of the solution: {len(node.solution())}')
		print(f'the total number of nodes that were removed from frontier: {removed_nodes_count}')
		print()
		print('==================================================================================')

def main():
	random_puzzles = []
	for i in range(10):
		random_puzzle = make_rand_8puzzle()
		random_puzzles.append(random_puzzle)

	summary(random_puzzles)

	random_puzzles = []
	for i in range(10):
		random_puzzle = make_rand_duck_puzzle()
		random_puzzles.append(random_puzzle)

	summary_duck(random_puzzles)

if __name__ == '__main__':
	main()