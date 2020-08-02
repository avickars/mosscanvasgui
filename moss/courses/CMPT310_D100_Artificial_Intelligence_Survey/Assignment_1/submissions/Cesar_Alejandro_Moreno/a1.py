# a1.py
import time
import math
from random import randrange
from search import *

goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a duck-like board, where one of the
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

        """0 1
		   2 3 4 5
  			 6 7 8"""  		  	
        
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):    	
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        """0 1
           2 3 4 5
             6 7 8"""

        if blank in [0, 1]:        	
        	delta = {'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank in [2, 3]:        	
        	delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif blank in [4, 5]:        	
        	delta = {'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:        	
        	delta = {'UP': -3, 'LEFT': -1, 'RIGHT': 1} # blank in [6, 7, 8]        	
        
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

def print_8puzzle_title():
	print('############################')
	print('# ___ ___            _     #')
	print('#( _ ) _ \\_  _ _____| |___ #')
	print('#/ _ \\  _/ || |_ /_ / / -_)#')
	print('#\\___/_|  \\_,_/__/__|_\\___|#') 
	print('############################')

def print_duckpuzzle_title():
	print('#########################################')
	print('# ___          _   ___            _     #')
	print('#|   \\ _  _ __| |_| _ \\_  _ _____| |___ #')
	print('#| |) | || / _| / /  _/ || |_ /_ / / -_)#')
	print('#|___/ \\_,_\\__|_\\_\\_|  \\_,_/__/__|_\\___|#')
	print('#########################################')        

def display_duckpuzzle(state):
	for position, tile in enumerate(state):
		if position in [1, 5, 8]:
			separator = '\n'
		else:
			separator = ' '

		if position == 6:
			print(' ', end = ' ')

		if tile == 0:
			print('*', end = separator)
		else:
			print(tile, end = separator)

def make_rand_duckpuzzle():	
	solved_puzzle = DuckPuzzle(goal_state)
	number_of_moves = 3000
	
	rand_puzzle = DuckPuzzle(get_random_state(solved_puzzle, number_of_moves))
	
	return rand_puzzle

def make_rand_8puzzle():
	initial_state = goal_state		
	solved_puzzle = EightPuzzle(initial_state)
	number_of_moves = 1000
	
	rand_puzzle = EightPuzzle(get_random_state(solved_puzzle, number_of_moves))	
	
	assert rand_puzzle.check_solvability(rand_puzzle.initial)	

	return rand_puzzle

def get_random_state(puzzle, number_of_moves):
	current_state = puzzle.initial
		
	for i in range(number_of_moves):		
		possible_moves = puzzle.actions(current_state)
		rand_move = possible_moves[randrange(len(possible_moves))]
		current_state = puzzle.result(current_state, rand_move)			

	return current_state

def display(state):
	puzzle_size = 9
	last_tile = puzzle_size - 1	

	for tile in range(puzzle_size):
		if (tile + 1) % 3 == 0:
			separator = '\n'
		else:
			separator = ' '

		if state[tile] == 0:				
			print("*", end = separator)
		else:	
			print(state[tile], end = separator)

def solve_8puzzle(puzzle, solution_moves):
	state = puzzle.initial
	for move in solution_moves:
		state = puzzle.result(state, move)
	
	display(state)
	
	if puzzle.goal_test(state):
		print ("Solved!")
	else:
		print ("Invalid solution!")

def solve_duckpuzzle(puzzle, solution_moves):
	state = puzzle.initial
	for move in solution_moves:
		state = puzzle.result(state, move)
	
	display_duckpuzzle(state)
	
	if puzzle.goal_test(state):
		print ("Solved!")
	else:
		print ("Invalid solution!")

def astar_search(problem, nodes_removed_from_frontier, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""    
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), nodes_removed_from_frontier, display)

def best_first_graph_search(problem, f, nodes_removed_from_frontier, display=False):
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
    while frontier:
        node = frontier.pop()
        nodes_removed_from_frontier[0] += 1                
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
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

def get_duckpuzzle_row(position):
	if position <= 1:
		current_row = 1
	elif position <= 5:
		current_row = 2					
	else:
		current_row = 3

	return current_row
	
def get_duckpuzzle_col(position):
	if position in [0, 2]:
		current_col = 1
	elif position in [1, 3, 6]:
		current_col = 2
	elif position in [4, 7]:
		current_col = 3
	else:
		current_col = 4

	return current_col

def duckpuzzle_manhattan_heuristic(node):
	distance_sum = 0

	for position, tile in enumerate(node.state):
		if tile == 0:
			continue

		current_col = get_duckpuzzle_col(position)
		current_row = get_duckpuzzle_row(position)
		
		goal_col = get_duckpuzzle_col(tile - 1)
		goal_row = get_duckpuzzle_row(tile - 1)
		
		horizontal_distance = abs(current_col - goal_col)
		vertical_distance = abs(current_row - goal_row)	

		distance_sum += horizontal_distance + vertical_distance

	return distance_sum

def manhattan_heuristic(node):
    distance_sum = 0

    for position, tile in enumerate(node.state):
    	if tile == 0:    		
    		continue

    	current_col = position % 3
    	current_row = math.floor(position / 3)

    	goal_col = (tile - 1) % 3
    	goal_row = math.floor((tile - 1) / 3)

    	horizontal_distance = abs(current_col - goal_col)
    	vertical_distance = abs(current_row - goal_row)

    	distance_sum += horizontal_distance + vertical_distance    	  	

    return distance_sum

def misplaced_heuristic(node):
    """ Return the heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles """

    return sum(s != g for (s, g) in zip(node.state, goal_state))    

def max_duckpuzzle_heuristic(node):
	return max(misplaced_heuristic(node), duckpuzzle_manhattan_heuristic(node))

def max_heuristic(node):
	return max(misplaced_heuristic(node), manhattan_heuristic(node))

def run_misplaced_tile_heuristic_seach(puzzle):
	print('\nMisplaced Tile Heuristic Seach')

	nodes_removed_from_frontier = [0]

	start_time = time.time()
	solution_moves = astar_search(puzzle, nodes_removed_from_frontier).solution()
	elapsed_time = time.time() - start_time

	print(f'Elapsed time in seconds: {elapsed_time}s')
	print(f'Lenght: {len(solution_moves)}')	
	print(f'Nodes removed from frontier: {nodes_removed_from_frontier[0]}')
	print ("------------------------------------")

def run_manhattan_heuristic_seach(puzzle, heuristic):
	print('\nManhattan Distance Heuristic Seach')

	nodes_removed_from_frontier = [0]

	start_time = time.time()
	solution_moves = astar_search(puzzle, nodes_removed_from_frontier, heuristic).solution()
	elapsed_time = time.time() - start_time

	print(f'Elapsed time in seconds: {elapsed_time}s')
	print(f'Lenght: {len(solution_moves)}')	
	print(f'Nodes removed from frontier: {nodes_removed_from_frontier[0]}')
	print ("------------------------------------")

def run_max_duckpuzzle_heuristic_search(puzzle):
	print('\nMax Heuristic Seach')

	nodes_removed_from_frontier = [0]

	start_time = time.time()
	solution_moves = astar_search(puzzle, nodes_removed_from_frontier, max_duckpuzzle_heuristic).solution()
	elapsed_time = time.time() - start_time

	print(f'Elapsed time in seconds: {elapsed_time}s')
	print(f'Lenght: {len(solution_moves)}')	
	print(f'Nodes removed from frontier: {nodes_removed_from_frontier[0]}')
	print ("------------------------------------")	

def run_max_heuristic_seach(puzzle):
	print('\nMax Heuristic Seach')

	nodes_removed_from_frontier = [0]

	start_time = time.time()
	solution_moves = astar_search(puzzle, nodes_removed_from_frontier, max_heuristic).solution()
	elapsed_time = time.time() - start_time

	print(f'Elapsed time in seconds: {elapsed_time}s')
	print(f'Lenght: {len(solution_moves)}')	
	print(f'Nodes removed from frontier: {nodes_removed_from_frontier[0]}')
	print ("------------------------------------")

def create_and_solve_8puzzles(number_of_puzzles):
	print_8puzzle_title()	
	for i in range(1, number_of_puzzles + 1):
		print('\n**************************************')
		print(f'Puzzle[{i}]:')
		puzzle_created = make_rand_8puzzle()
		print('\nInitial Board')
		display(puzzle_created.initial)		

		run_misplaced_tile_heuristic_seach(puzzle_created)
		run_manhattan_heuristic_seach(puzzle_created, manhattan_heuristic)
		run_max_heuristic_seach(puzzle_created)		
		print('**************************************\n')

def create_and_solve_duckpuzzles(number_of_puzzles):
	print_duckpuzzle_title()	
	for i in range(1, number_of_puzzles + 1):
		print('\n**************************************')
		print(f'Puzzle[{i}]:')
		puzzle_created = make_rand_duckpuzzle()
		print('\nInitial Board')
		display_duckpuzzle(puzzle_created.initial)		

		run_misplaced_tile_heuristic_seach(puzzle_created)
		run_manhattan_heuristic_seach(puzzle_created, duckpuzzle_manhattan_heuristic)
		run_max_duckpuzzle_heuristic_search(puzzle_created)		
		print('**************************************\n')



create_and_solve_8puzzles(0)
create_and_solve_duckpuzzles(10)