# a1.py

from search import *

import time


 # Question 1: Helper Functions
def make_rand_8puzzle():
	# state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
	# l = random.sample(state, 9)
	# rand_state = tuple(l)
	# eight_puzzle = EightPuzzle(rand_state)
	# if not eight_puzzle.check_solvability(rand_state):
	# 	make_rand_8puzzle()

	# return eight_puzzle

	eight_puzzle = EightPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))

	state =(1, 2, 3, 4, 5, 6, 7, 8, 0)
	rand_iteration = random.randint(2,10000)
	for x in range(1,rand_iteration):
		possible_actions = eight_puzzle.actions(state)

		rand_action = random.choice(possible_actions)
		rand_state = eight_puzzle.result(state,rand_action)
		state = rand_state
	if not eight_puzzle.check_solvability(rand_state):
		make_rand_8puzzle()
	eight_puzzle = EightPuzzle(rand_state)
	return eight_puzzle


def display(state):
	eightpuzzle = EightPuzzle(state)
	blank_index = eightpuzzle.find_blank_square(state)
	list_state = list(state)
	list_state[blank_index] = '*'

	for i in range(0 , len(list_state), 3):
		print(list_state[i], end = " "),
		print(list_state[i+1], end = " "),
		print(list_state[i+2])

# Question 2: Comparing Algorithms
def new_best_first_graph_search(problem, f):
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
    remove = 0
    while frontier:
        node = frontier.pop()
        remove = remove + 1
        if problem.goal_test(node.state):
            return node , remove
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def new_astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return new_best_first_graph_search(problem, lambda n: n.path_cost + h(n))

def Manhattan_distance(node):
	state = node.state
	goal_state = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
	problem_state = {}
	index = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
	for i in range(len(state)):
		problem_state[state[i]] = index[i]
	
	Manhattan = 0
	for j in range(1,9):
			Manhattan = abs(goal_state[j][0] - problem_state[j][0]) + abs(goal_state[j][1] - problem_state[j][1]) + Manhattan

	return Manhattan

def max_ManhattanOrMisplaced_heuristic(node):
	Manhattan = Manhattan_distance(node)

	x = EightPuzzle(node.state)
	heuristic = x.h(node)

	return max(Manhattan , heuristic)

# Question 3: The House-Puzzle

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

        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions = ['RIGHT','DOWN2']
        if index_blank_square == 1 :
            possible_actions = ['LEFT','DOWN2']
        if index_blank_square == 2:
            possible_actions = ['UP2','RIGHT']
        if index_blank_square == 3 :
            possible_actions = ['UP2', 'DOWN3', 'LEFT', 'RIGHT']
        if index_blank_square == 4:
            possible_actions = ['DOWN3', 'LEFT', 'RIGHT']
        if index_blank_square == 5 :
            possible_actions = ['LEFT','DOWN3']
        if index_blank_square == 6:
            possible_actions = ['UP3','RIGHT']
        if index_blank_square == 7 :
            possible_actions = ['UP3', 'LEFT', 'RIGHT']
        if index_blank_square == 8 :
            possible_actions = ['LEFT','UP3']

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP2': -2, 'UP3': -3, 'DOWN2': 2, 'DOWN3': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """
        if state.index(1) > 3 | state.index(2) > 3 | state.index(3) > 3:
        	return False
        if state.index(4) < 3 | state.index(5) < 3 | state.index(6) < 3 | state.index(7) < 3 | state.index(8) < 3:
        	return False

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
def make_rand_Duckpuzzle():
	# state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
	# l = random.sample(state, 9)
	# rand_state = tuple(l)
	# duck_puzzle = DuckPuzzle(rand_state)
	# if duck_puzzle.check_solvability(rand_state) == False:
	# 	make_rand_Duckpuzzle()

	# return duck_puzzle
	duck_puzzle = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))

	state =(1, 2, 3, 4, 5, 6, 7, 8, 0)
	rand_iteration = random.randint(2,100000)
	for x in range(1,rand_iteration):
		possible_actions = duck_puzzle.actions(state)

		rand_action = random.choice(possible_actions)
		rand_state = duck_puzzle.result(state,rand_action)
		state = rand_state
	duck_puzzle = DuckPuzzle(rand_state)
	if duck_puzzle.check_solvability(rand_state) == False:
		make_rand_Duckpuzzle()
	return duck_puzzle


def Duck_display(state):
	duckpuzzle = DuckPuzzle(state)
	blank_index = duckpuzzle.find_blank_square(state)
	list_state = list(state)
	list_state[blank_index] = '*'
	list_state = tuple(list_state)

	print('%s %s\n%s %s %s %s\n  %s %s %s' % list_state)

def Duck_Manhattan_distance(node):
	state = node.state
	goal_state = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
	problem_state = {}
	index = [[0,0],[0,1],[1,0],[1,1],[1,2],[1,3],[2,1],[2,2],[2,3]]
	for i in range(len(state)):
		problem_state[state[i]] = index[i]
	
	Manhattan = 0
	for j in range(1,9):
			Manhattan = abs(goal_state[j][0] - problem_state[j][0]) + abs(goal_state[j][1] - problem_state[j][1]) + Manhattan

	return Manhattan

def max_Duck_Manhattan_heuristic(node):
	Duck_Manhattan = Duck_Manhattan_distance(node)

	x = DuckPuzzle(node.state)
	heuristic = x.h(node)

	return max(Duck_Manhattan , heuristic)


def main():
	#8-puzzle
	for i in range(1,11):
		x = make_rand_8puzzle()
		print()
		display(x.initial)
		print('----------------------------')
		print("8-puzzle using misplaced tile heuristic")
		start_time = time.time()

		remove_node , remove_count = new_astar_search(x)

		elapsed_time = time.time() - start_time
		print(len(remove_node.solution()))
		print(remove_count)
		print(f'elapsed time (in seconds): {elapsed_time}s')
		
		print('----------------------------')
		print("8-puzzle using Manhattan distance heuristic")
		start_time = time.time()

		remove_node , remove_count = new_astar_search(x,Manhattan_distance)

		elapsed_time = time.time() - start_time
		print(len(remove_node.solution()))
		print(remove_count)
		print(f'elapsed time (in seconds): {elapsed_time}s')

		print('----------------------------')
		print("8-puzzle using max of misplaced tile heuristic  and Manhattan distance heuristic")
		start_time = time.time()

		remove_node , remove_count = new_astar_search(x,max_ManhattanOrMisplaced_heuristic)

		elapsed_time = time.time() - start_time
		print(len(remove_node.solution()))
		print(remove_count)
		print(f'elapsed time (in seconds): {elapsed_time}s')

	print("#######################################")
	#DuckPuzzle
	for i in range(1,11):
		x = make_rand_Duckpuzzle()
		print()
		Duck_display(x.initial)
		print('----------------------------')
		print("Duckpuzzle using misplaced tile heuristic")
		start_time = time.time()

		remove_node , remove_count = new_astar_search(x)

		elapsed_time = time.time() - start_time
		print(len(remove_node.solution()))
		print(remove_count)
		print(f'elapsed time (in seconds): {elapsed_time}s')
		
		print('----------------------------')
		print("Duckpuzzle using Manhattan distance heuristic")
		start_time = time.time()

		remove_node , remove_count = new_astar_search(x,Duck_Manhattan_distance)

		elapsed_time = time.time() - start_time
		print(len(remove_node.solution()))
		print(remove_count)
		print(f'elapsed time (in seconds): {elapsed_time}s')

		print('----------------------------')
		print("Duckpuzzle using max of misplaced tile heuristic  and Manhattan distance heuristic")
		start_time = time.time()

		remove_node , remove_count = new_astar_search(x,max_Duck_Manhattan_heuristic)

		elapsed_time = time.time() - start_time
		print(len(remove_node.solution()))
		print(remove_count)
		print(f'elapsed time (in seconds): {elapsed_time}s')
	

if __name__ == "__main__":
	main()
