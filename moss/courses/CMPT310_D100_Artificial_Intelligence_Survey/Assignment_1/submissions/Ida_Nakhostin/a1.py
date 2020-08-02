import csv
import random
import time
from search import *

"""
Note that some of the code in this assignment are adaptations from the code in aima-python and I have provided 
comments on top of the code that adapted and modifies aima-python, any other code is my own work that 
I have written with help of reading python docs on various python features such as random, csv, time, 
enumerators, data structures and so on. I have implemented the misplaced tile and Manhattan distance based on
the books description, therefor I have excluded tile 0 from the calculations in both heuristics to be admissible.
"""

"""
I have coppied the best_first_graph_search from search.py here and and modified it to add a counter for number 
of nodes removed (removed_nodes_count) which the function is now returning, so I can use it for the analytics.
"""
def best_first_graph_search(problem, f, display=False):
    removed_nodes_count = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        removed_nodes_count += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, removed_nodes_count
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, removed_nodes_count


"""
This is the exact same astar_search function as the one in search.py but I had to copy it here so it can call
my modified best_first_graph_search.
"""
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# ------------------------ Q1 -----------------------

def make_rand_8puzzle():
    """Shuffles the eight puzzle tiles and returns an EightPuzzle with a solvable random initial state."""  
    eight_puzzle_tile_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    is_solvable = False
    while not is_solvable:       
        random.shuffle(eight_puzzle_tile_numbers) # shuffles a sequence in place
        is_solvable = EightPuzzle.check_solvability(None, eight_puzzle_tile_numbers)
        
    solvable_state = tuple(eight_puzzle_tile_numbers)

    return EightPuzzle(solvable_state)

def display(state):
    """Displays the state of an EightPuzzle in 3x3.""" 
    for idx, tile in enumerate(state):
        tile = '*' if tile == 0 else tile
        print_end_char = '\n' if (idx + 1) % 3 == 0 else ' '        
        print(tile, end=print_end_char)


# ------------------------ Q2 -----------------------

"""
This misplaced tile heuristic is the same as the "h" function in EightPuzzle except it excludes counting 
empty tile (tile 0) for the heuristic to be admissible
"""
def misplaced_tile_heuristic(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return sum(s != g for (s, g) in zip(node.state, goal) if s)

"""
This code is based on the Manhattan function code in test_search.py but I have changed it to  correct the range 
issue, exclude 0 tile so the heuristic is admissible and have update some of the code logic and variable naming
"""
def eight_puzzle_manhattan_distance_heuristic(node):
    """Calculates the Manhattan distance between goal tiles' postions and the current positions 
    on a 3x3 matrix (grid) for an eight puzzle.
    """  
    state = node.state
    # a dictionary of the eight puzzle tile number and their goal x-y postion
    goal_tiles_x_y = {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 2], 8: [1, 2]}
    state_tiles_x_y = {}
    eight_puzzle_tiles_x_y = ([0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [2, 2])
    manhattan_distance = 0

    for idx, tile in enumerate(state):
        # a dictionary of the current eight puzzle tile number x-y postion
        state_tiles_x_y[tile] = eight_puzzle_tiles_x_y[idx]

    # the range does not include 0 so empty tile is excluded from calculation
    for tile in range(1,9):
        goal_x_y = goal_tiles_x_y[tile]
        state_x_y = state_tiles_x_y[tile]
        manhattan_distance = abs(goal_x_y[0] - state_x_y[0]) + abs(goal_x_y[1] - state_x_y[1]) + manhattan_distance

    return manhattan_distance

def eight_puzzle_max_heuristic(node):
    """Returns the maximum of misplaced tile and Manhattan distance heuristic value for he node in eight puzzle"""   
    state = node.state
    manhattan_distance = eight_puzzle_manhattan_distance_heuristic(node)
    misplaced_tiles_num = misplaced_tile_heuristic(node)

    return max(manhattan_distance, misplaced_tiles_num)


def compare_puzzle_algorithms(random_puzzles, misplaced_tile_h, manhattan_distance_h, max_h, display, filename):
    """Runs A* function on puzzles and creates a csv file that includes the initial 
    state, run time, length and number of nodes removed.

    Runs the A* function using the passed in misplaced tile, Manhattan and max heuristic on 
    every puzzle in random_puzzles list and writes the results into a csv file as well as printing it out.

    Args:
        random_puzzles (list): List of Problem objects to solve using A* function
        misplaced_tile_h (function): The misplaced tile heuristics to used for A* function
        manhattan_distance_h (function): The Manhattan distance heuristics to use for A* function
        max_h (function): The maximum heuristic to use for A* function
        display (function): The function to print the state
        filename (str): The name of the file to create and write the csv results to
    """  
    heuristics = {
        'misplaced': misplaced_tile_h, 
        'manhattan': manhattan_distance_h,
        'max': max_h
    }

    results = [] # stores stat result for all puzzles
    for puzzle in random_puzzles:
        result = {'state': puzzle.initial} # stat result for each puzzle 

        print(f'{puzzle.initial}\n')
        display(puzzle.initial)
        
        for h_name, h in heuristics.items():
            print(f'\n--------------------{h_name}--------------------')
            
            # calculate the run time to solve the puzzle
            start_time = time.time()   
            node, removed_nodes_count = astar_search(puzzle, h=h)
            elapsed_time = round(time.time() - start_time, 6)
            
            print(f'the total running time in seconds:      {elapsed_time}')
            print(f'the solution length (# tiles moved):    {node.path_cost}')
            print(f'total # of nodes removed from frontier: {removed_nodes_count}')
            
            result['{}_run_time'.format(h_name)] = elapsed_time
            result['{}_length'.format(h_name)] = node.path_cost
            result['{}_removed_nodes_count'.format(h_name)] = removed_nodes_count
      
        results.append(result)
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['state', 'misplaced_run_time', 'misplaced_length', 'misplaced_removed_nodes_count',
            'manhattan_run_time', 'manhattan_length', 'manhattan_removed_nodes_count',
            'max_run_time', 'max_length', 'max_removed_nodes_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

# ------------------------ Q3 -----------------------

"""
This code is based on the EightPuzzle class in search.py but I have changed the logic for "actions"
and "result" functions to be correct based on a duck puzzle layout. I have also added a display function.
"""
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 4x3 duck shaped board, where one of the
    squares is a blank and squares [0,2], [0,3] and [3,0] are excluded. A state is represented 
    as a tuple of length 9, where element at index i represents the tile number at 
    index i (0 if it's an empty square) 
    """
    
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment 
        """
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        blank_square_index = self.find_blank_square(state)
      
        # Removing actions that are not possible by any certain tile due to their placement 
        if blank_square_index in [0, 2, 6]:
            possible_actions.remove('LEFT')
        if blank_square_index in [0, 1, 4, 5]:
            possible_actions.remove('UP')
        if blank_square_index in [1, 5, 8]:
            possible_actions.remove('RIGHT')
        if blank_square_index in [2, 6, 7, 8]:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given a state and  an action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state 
        """
        blank_square_index = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        # moving up and down inside the 2x2 duck head changes the index by 2
        if blank_square_index <= 3:
            delta['UP'] = -2    
        if blank_square_index <= 2:
            delta['DOWN'] = 2

        neighbor = blank_square_index + delta[action]
        new_state[blank_square_index], new_state[neighbor] = new_state[neighbor], new_state[blank_square_index]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

    def display(state):
        """Displays the state of the 3x4 duck puzzle with consideration of excluded tiles."""
        tile_idx = 0
        tile = ''
        for x in range(3):
            for y in range(4):
                if [x,y] in [[0, 2], [0, 3], [2, 0]]:
                    tile = ' '
                else:
                    tile = state[tile_idx]
                    tile = '*' if tile == 0 else tile
                    tile_idx += 1
                
                print_end_char = '\n' if y == 3 else ' ' 
                print(tile, end=print_end_char)

    
def make_rand_duck_puzzle(goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    """Scrambles the duck puzzle by making random valid moves starting from the goal 
    state and return the scrambled puzzle
    """    
    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    duck_puzzle = DuckPuzzle(goal)
    for _ in range(100): # making 100 random valid moves
        possible_actions = duck_puzzle.actions(duck_puzzle.initial)
        new_state = duck_puzzle.result(duck_puzzle.initial, random.choice(possible_actions))
        duck_puzzle.initial = new_state
    
    return duck_puzzle

def duck_puzzle_manhattan_distance_heuristic(node):
    """Calculates the manhattan distance for duck puzzle based on 3x4 matrix.
    The coordinates [0,1], [0,2] & [2,0] are excluded tiles.
    """
    state = node.state
    # a dictionary of the duck puzzle tile number and their goal x-y postion
    goal_tiles_x_y = {1: [0, 0], 2: [1, 0], 3: [0, 1], 4: [1, 1], 5: [2, 1], 6: [3, 1], 7: [1, 2], 8: [2, 2]}
    state_tiles_x_y = {}
    duck_puzzle_tiles_x_y = ([0, 0], [1, 0], [0, 1], [1, 1], [2, 1], [3, 1], [1, 2], [2, 2], [3, 2])
    manhattan_distance = 0

    for idx, tile in enumerate(state):
        # a dictionary of the current duck puzzle tile x-y postion
        state_tiles_x_y[tile] = duck_puzzle_tiles_x_y[idx]

     # the range does not include 0 so empty tile is excluded from calculation
    for tile in range(1,9):
        goal_x_y = goal_tiles_x_y[tile]
        state_x_y = state_tiles_x_y[tile]
        manhattan_distance = abs(goal_x_y[0] - state_x_y[0]) + abs(goal_x_y[1] - state_x_y[1]) + manhattan_distance

    return manhattan_distance

def duck_puzzle_max_heuristic(node):
    """Returns the maximum of misplaced tile and Manhattan distance heuristic value for the node in duck puzzle""" 
    state = node.state
    manhattan_distance = duck_puzzle_manhattan_distance_heuristic(node)
    misplaced_tiles_num = misplaced_tile_heuristic(node)

    return max(manhattan_distance, misplaced_tiles_num)


if __name__ == '__main__':
    """ The main function is creating 10 random unique eight puzzles and 10 random 
    unique duck puzzles and is calling the compare_puzzle_algorithms for those puzzle
    """
    print(' ------------------------------------------------ ')
    print('|                   Eight Puzzle                 |')
    print(' ------------------------------------------------ ')
    random_eight_puzzle_states = set()
    random_eight_puzzles = []
    # get 10 random unique eight puzzles
    while len(random_eight_puzzles) < 10:
        eight_puzzle = make_rand_8puzzle()
        if eight_puzzle.initial not in random_eight_puzzle_states:
            random_eight_puzzle_states.add(eight_puzzle.initial)
            random_eight_puzzles.append(eight_puzzle)

    compare_puzzle_algorithms(random_eight_puzzles, misplaced_tile_heuristic, 
                              eight_puzzle_manhattan_distance_heuristic, eight_puzzle_max_heuristic, 
                              display, 'eight_puzzle_stats.csv')
    
    print()
    print(' ----------------------------------------------- ')
    print('|                   Duck Puzzle                 |')
    print(' ----------------------------------------------- ')
    random_duck_puzzles_states = set()
    random_duck_puzzles = []
    # get 10 random unique duck puzzles
    while len(random_duck_puzzles) < 10:
        duck_puzzle = make_rand_duck_puzzle()
        if duck_puzzle.initial not in random_duck_puzzles_states:
            random_duck_puzzles_states.add(duck_puzzle.initial)
            random_duck_puzzles.append(duck_puzzle)

    compare_puzzle_algorithms(random_duck_puzzles, misplaced_tile_heuristic, 
                              duck_puzzle_manhattan_distance_heuristic, duck_puzzle_max_heuristic, 
                              DuckPuzzle.display, 'duck_puzzle_stats.csv')



