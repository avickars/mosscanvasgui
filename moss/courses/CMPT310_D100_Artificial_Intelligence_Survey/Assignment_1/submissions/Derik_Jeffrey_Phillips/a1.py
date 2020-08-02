# a1.py

from search import *

# ...

import random, time

# ----- Duck Puzzle -----

# --- Class Definition ---

class DuckPuzzle(EightPuzzle):
	
	def actions(self, state):
		
		possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
		index_blank_square = self.find_blank_square(state)
		
		if index_blank_square in (0, 2, 6):
			possible_actions.remove('LEFT')
		if index_blank_square in (0, 1, 4, 5):
			possible_actions.remove('UP')
		if index_blank_square in (1, 5, 8):
			possible_actions.remove('RIGHT')
		if index_blank_square in (2, 6, 7, 8):
			possible_actions.remove('DOWN')
		
		return possible_actions
	
	def result(self, state, action):
		
		blank = self.find_blank_square(state)
		new_state = list(state)
		
		delta = {'LEFT': -1, 'RIGHT': 1}
		
		if blank in (0, 1):
			delta['DOWN'] = 2
		elif blank in (2, 3, 4, 5):
			delta['UP'] = -2
			delta['DOWN'] = 3
		elif blank in (6, 7, 8):
			delta['UP'] = -3
	
		neighbour = blank + delta[action]
		new_state[blank], new_state[neighbour] = new_state[neighbour], new_state[blank]
		
		return tuple(new_state)
		
	def check_solvability(self, state):
		return None


# --- Manhattan ---

patterns_duckpuzzle = (
	(0, 1, 1, 2, 3, 4, 3, 4, 5),
	(1, 0, 2, 1, 2, 3, 2, 3, 4),
	(1, 2, 0, 1, 2, 3, 2, 3, 4),
	(2, 1, 1, 0, 1, 2, 1, 2, 3),
	(3, 2, 2, 1, 0, 1, 2, 1, 2),
	(4, 3, 3, 2, 1, 0, 3, 2, 1),
	(3, 2, 2, 1, 2, 3, 0, 1, 2),
	(4, 3, 3, 2, 1, 2, 1, 0, 1),
	(5, 4, 4, 3, 2, 1, 2, 1, 0)
)

def manhattan_duckpuzzle(node):
	sum = 0
	for tile in node.state:
		if (tile) == 0:
			continue
		sum += patterns_duckpuzzle[tile-1][node.state.index(tile)]
	return sum


# --- Max of Manhattan and Misplaced Tile ---

def max_duckpuzzle(node):
	return max(manhattan_duckpuzzle(node), misplaced_tile(node))


# --- Helper Functions ---

def make_random_duckpuzzle():
	state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
	puzzle = DuckPuzzle(state)
	for i in range(random.randrange(1000, 50000)):
		actions = puzzle.actions(state)
		state = puzzle.result(state, actions[random.randrange(len(actions))])
		puzzle = DuckPuzzle(state)
	return puzzle


def display_duckpuzzle(state):
	state = [str(x) for x in state]
	state = [x if x != '0' else '*' for x in state]
	for i in range(9):
		print(state[i] + " ", end="")
		if i == 1:
			print()
		if i == 5:
			print("\n  ", end="")
	print()

		
# ----- search.py Alterations -----

# Altering best first graph search in order to count the number of nodes removed
#   from the frontier.
def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    removed = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, removed
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    removed += 1
                    frontier.append(child)
    return None

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# ----- Eight Puzzle -----

# --- Misplaced Tile ---

def misplaced_tile(node):
	goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
	return sum(s != g for (s, g) in zip(node.state, goal))


# --- Manhattan ---

patterns_8puzzle = (
	(0, 1, 2, 1, 2, 3, 2, 3, 4),
	(1, 0, 1, 2, 1, 2, 3, 2, 3),
	(2, 1, 0, 3, 2, 1, 4, 3, 2),
	(1, 2, 3, 0, 1, 2, 1, 2, 3),
	(2, 1, 2, 1, 0, 1, 2, 1, 2),
	(3, 2, 1, 2, 1, 0, 3, 2, 1),
	(2, 3, 4, 1, 2, 3, 0, 1, 2),
	(3, 2, 3, 2, 1, 2, 1, 0, 1),
	(4, 3, 2, 3, 2, 1, 2, 1, 0)
)

def manhattan_8puzzle(node):
	sum = 0
	for tile in node.state:
		if (tile) == 0:
			continue
		sum += patterns_8puzzle[tile-1][node.state.index(tile)]
	return sum


# --- Max of Manhattan and Misplaced Tile ---

def max_8puzzle(node):
	return max(manhattan_8puzzle(node), misplaced_tile(node))


# --- Helper Functions ---

# ------------------------------- ANSWER TO QUESTION 1 ------------------------------- #

def make_rand_8puzzle():
	"""Returns a new instance of EightPuzzle with a random initial state that is solvable."""
	goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
	initial = tuple(random.sample(goal, k=len(goal)))
	puzzle = EightPuzzle(initial, goal)
	while (not puzzle.check_solvability(initial)):
		initial = tuple(random.sample(goal, k=len(goal)))
		puzzle = EightPuzzle(initial, goal)
	return puzzle
	
def display(state):
	"""Takes an 8-puzzle state (i.e. a tuple that is a permutation of numbers 0 to 8) as input
	and prints a neat and readable representation of it. 0 is the blank tile and is 
	represented by the * character."""
	for i in range(9):
		if state[i] != 0:
			print(str(state[i]) + " ", end="")
		else:
			print("* ", end="")
		if i % 3 == 2:
			print()


# --- Initialization and Solve ---

puzzle = make_rand_8puzzle()
display(puzzle.initial)
print()

# Solve with misplaced tile heuristic:
print("Misplaced Tile Solve:")
tic = time.perf_counter()
node, removed = astar_search(puzzle)
toc = time.perf_counter()
print("\tTime taken: ", format(toc - tic, ".4f"))
print("\tLength of solution:", len(node.solution()))
print("\tNodes removed from frontier: ", removed)
print()

# Solve with manhattan heuristic:
print("Manhattan Solve:")
tic = time.perf_counter()
node, removed = astar_search(puzzle, h=manhattan_8puzzle)
toc = time.perf_counter()
print("\tTime taken: ", format(toc - tic, ".4f"))
print("\tLength of solution:", len(node.solution()))
print("\tNodes removed from frontier: ", removed)
print()

# Solve with max of manhattan and misplaced tile heuristics:
print("Max Solve:")
tic = time.perf_counter()
node, removed = astar_search(puzzle, h=max_8puzzle)
toc = time.perf_counter()
print("\tTime taken: ", format(toc - tic, ".4f"))
print("\tLength of solution:", len(node.solution()))
print("\tNodes removed from frontier: ", removed)
print()



puzzle = make_random_duckpuzzle()
display_duckpuzzle(puzzle.initial)
print()

# Solve with misplaced tile heuristic:
print("Misplaced Tile Solve:")
tic = time.perf_counter()
node, removed = astar_search(puzzle)
toc = time.perf_counter()
print("\tTime taken: ", format(toc - tic, ".4f"))
print("\tLength of solution:", len(node.solution()))
print("\tNodes removed from frontier: ", removed)
print()

# Solve with manhattan heuristic:
print("Manhattan Solve:")
tic = time.perf_counter()
node, removed = astar_search(puzzle, h=manhattan_duckpuzzle)
toc = time.perf_counter()
print("\tTime taken: ", format(toc - tic, ".4f"))
print("\tLength of solution:", len(node.solution()))
print("\tNodes removed from frontier: ", removed)
print()

# Solve with max of manhattan and misplaced tile heuristics:
print("Max Solve:")
tic = time.perf_counter()
node, removed = astar_search(puzzle, h=max_duckpuzzle)
toc = time.perf_counter()
print("\tTime taken: ", format(toc - tic, ".4f"))
print("\tLength of solution:", len(node.solution()))
print("\tNodes removed from frontier: ", removed)

