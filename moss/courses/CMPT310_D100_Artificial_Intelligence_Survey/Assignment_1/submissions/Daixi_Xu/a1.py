from search import *
import random
import sys
import time

#______________________________________________________________________________
# Functions modified from search.py

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    popped = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        popped = popped + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                print("Number of nodes that were removed from frontier is: " + str(popped))
                print("Number of tiles moved is: " + str(len(explored)))
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

# ______________________________________________________________________________


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# ______________________________________________________________________________
# A* heuristics 


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

    def h_manhattanDistance(self, node):
        """Added heuristic function with h(n) = manhattan distance"""
        # 1D to 2D array
        curr_state = []
        temp = node.state 
        for i in range(len(temp)):
            if i % 3 == 0:
                curr_state.append(temp[i:(i + 3)])
        goal_state = []
        temp = self.goal 
        for i in range(len(temp)):
            if i % 3 == 0:
                goal_state.append(temp[i:(i + 3)])
        mDistance = 0
        goal_row = 0 
        goal_col = 0
        curr_row = 0 
        curr_col = 0
        for i in node.state:
            for row in range(3):
                for col in range(3): 
                    if(i == goal_state[row][col]):
                        # where the number is supposed to be
                        goal_row = row 
                        goal_col = col
                    if(i == curr_state[row][col]):
                        curr_row = row 
                        curr_col = col
            mDistance = mDistance + (abs(goal_row - curr_row) + abs(goal_col - curr_col))
        return mDistance

# ______________________________________________________________________________


# Question 1
def make_rand_8puzzle():
	while(1):
		num_range = [0, 1, 2, 3, 4, 5, 6, 7, 8]
		random.shuffle(num_range)
		initial_state = tuple(num_range)
		new_8puzzle = EightPuzzle(initial_state)
		# check if the initial state is solvable
		if (new_8puzzle.check_solvability(initial_state)):
			return new_8puzzle

def display(state): 
	temp = []
	for i in range(len(state)):
		if state[i] == 0:
			temp.append('*')
		else:
			temp.append(state[i])
	state_divided = []
	for i in range(len(temp)):
		if i % 3 == 0:
			state_divided.append(temp[i:(i + 3)])
	for i in state_divided:
		# reference: https://stackoverflow.com/questions/13550423/python-printing-without-commas/43177870
		print(' '.join(map(str, i)))

# ______________________________________________________________________________


# Question 2

def maxHeuristic(puzzle):
	hScore = astar_search(puzzle, puzzle.h, False)
	MDScore = astar_search(puzzle, puzzle.h_manhattanDistance, False)
	if (hScore > MDScore):
		return "Misplaced Tiles"
	return "Manhattan Distance"

hTime = []
MDTime = []
maxTime = []

for i in range(10):
	new_8puzzle = make_rand_8puzzle()

	start = time.time()
	astar_search(new_8puzzle, new_8puzzle.h, True)
	duration_h = time.time() - start
	hTime.append(duration_h) 

	start = time.time()
	astar_search(new_8puzzle, new_8puzzle.h_manhattanDistance, True)
	duration_md = time.time() - start 
	MDTime.append(duration_md) 

	res = maxHeuristic(new_8puzzle)
	if (res == "Misplaced Tiles"):
		maxTime.append(duration_h)
	maxTime.append(duration_md)

print(hTime)
print(MDTime)
print(maxTime)

# ______________________________________________________________________________


# Question 3
class HousePuzzle(Problem):
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

        if index_blank_square in [0, 2, 6]:
            possible_actions.remove('LEFT')
        if index_blank_square in [0, 1, 4, 5]:
            possible_actions.remove('UP')
        if index_blank_square in [1, 5, 8]:
            possible_actions.remove('RIGHT')
        if index_blank_square in [2, 6, 7, 8]:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if (0 <= blank <= 2):
        	delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif (blank == 3):
        	delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif (4 <= blank <= 8):
        	delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h_manhattanDistance(self, node):
        """Added heuristic function with h(n) = manhattan distance"""

        # Solving this problem by imagining the puzzle to be 4 * 3 
        curr_state = list(node.state)
        curr_state.insert(2, -1) # insert -1 for added spots
        curr_state.insert(3, -1)
        curr_state.insert(8, -1)

        goal_state = list(self.goal)
        goal_state.insert(2, -1) # insert -1 for added spots
        goal_state.insert(3, -1)
        goal_state.insert(8, -1)

        # 2D arrays 
        curr_temp = []
        goal_temp = []

        for i in range(len(curr_state)):
        	if i % 4 == 0:
        		curr_temp.append(curr_state[i:(i + 4)])

        for i in range(len(goal_state)):
        	if i % 4 == 0:
        		goal_temp.append(goal_state[i:(i + 4)])

        mDistance = 0
        goal_row = 0 
        goal_col = 0
        curr_row = 0 
        curr_col = 0

        for i in curr_state:
            for row in range(3):
                for col in range(4): 
                    if(i == goal_temp[row][col]):
                        # where the number is supposed to be
                        goal_row = row 
                        goal_col = col
                    if(i == curr_temp[row][col]):
                        curr_row = row 
                        curr_col = col
            mDistance = mDistance + (abs(goal_row - curr_row) + abs(goal_col - curr_col))
        return mDistance


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

# ______________________________________________________________________________


def make_rand_housePuzzle():
	"""A function that returns a random house puzzle"""
	puzzle = HousePuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0)) # start with the goal state for solvability of the puzzle 
	actions = []
	result = tuple()
	for i in range(1000): # randomize by randomly moving the tiles 1000 times
		actions = puzzle.actions(puzzle.initial) # return should be a list of actions
		result = puzzle.result(puzzle.initial, random.choice(actions))
		puzzle.initial = result
	return puzzle


hTime = []
MDTime = [] 
maxTime = []
for i in range(10):
	puzzle = make_rand_housePuzzle()
	start = time.time()
	astar_search(puzzle, puzzle.h, True)
	duration_h = time.time() - start 
	hTime.append(duration_h)
	start = time.time()
	astar_search(puzzle, puzzle.h_manhattanDistance, True)
	duration_md = time.time() - start
	MDTime.append(duration_md)

	res = maxHeuristic(puzzle)
	if (res == "Misplaced Tiles"):
		maxTime.append(duration_h)
	maxTime.append(duration_md)


print(hTime)
print(MDTime)
print(maxTime)