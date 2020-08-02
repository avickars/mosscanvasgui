#ai.py

from search import *
import random
import time

# Question 1:
def make_rand_8_puzzle():
    curr_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    rand_puzzle = EightPuzzle(curr_state)
    
    for i in range(50):
        list_possible_moves = rand_puzzle.actions(curr_state)
        num_of_moves = len(list_possible_moves)
        next_move_index = random.randrange(num_of_moves)
        next_move = list_possible_moves[next_move_index]
        curr_state = rand_puzzle.result(curr_state, next_move)
    
    if rand_puzzle.check_solvability(curr_state):
        return curr_state
    else:
        assert False, ('  State Not Solvable. Program Terminated.')
    
def display(state):
    state_list = list(state)
    state_list = ['*' if x==0 else x for x in state_list]
    state_list = str(state_list).replace(',', '').replace('\'','')
    print('\n\t\t      Solvable Puzzle Example:')
    print('\t\t\t      ',(state_list)[1:6]) 
    print('\t\t\t      ',(state_list)[7:12]) 
    print('\t\t\t      ',(state_list)[13:18])

#------------------------------------------------------------------------------

# Question 2:
def create_10_puzzles():
    puzzles = []
    for i in range(10):
        puzzles.append(make_rand_8_puzzle())
    return puzzles

# adapted from search.py in aima-python to return a counter for 
# popped frontier nodes
def best_first_graph_search(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    popped_counter = 0
    while frontier:
        node = frontier.pop()
        popped_counter += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", 
                      len(frontier),
                     "paths remain in the frontier")
            return node, popped_counter
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

# copied from search.py in aima-python to work with above adapted
# best_first_graph_search
def astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n),
                                  display)

def misplaced_tile_heur_search(puzzles: list):
    print('\n*--------------------Misplaced Tile Heuristic--------------------*\n')

    for i, puzzle in enumerate(puzzles, start=0):
        start_time = time.time()
        result,removed_nodes = astar_search(EightPuzzle(puzzle))
        elapsed_time = time.time() - start_time

        print(f'  Puzzle {i+1}: {puzzle}\n')
        print('  Elapsed run time (in seconds):                     ',
              f'{elapsed_time:.8f}s')
        print('  Length of tiles moved to get to solution:          ',
              f'{len(result.solution())}')
        print('  Total number of nodes removed from frontier:       ',
              f'{removed_nodes}\n')

def manhattan_heur(node: Node):
    # Manhattan Heuristic Function
    curr_state = node.state
    man_dist = 0
    for i, num in enumerate(curr_state, start=0):
        if num == 1:
            one_dist = [0,1,2,1,2,3,2,3,4]
            man_dist += one_dist[i]
        elif num == 2:
            two_dist = [1,0,1,2,1,2,3,2,3]
            man_dist += two_dist[i]
        elif num == 3:
            three_dist = [2,1,0,3,2,1,4,3,2]
            man_dist += three_dist[i]
        elif num == 4:
            four_dist = [1,2,3,0,1,2,1,2,3]
            man_dist += four_dist[i]
        elif num == 5:
            five_dist = [2,1,2,1,0,1,2,1,2]
            man_dist += five_dist[i]
        elif num == 6:
            six_dist = [3,2,1,2,1,0,3,2,1]
            man_dist += six_dist[i]
        elif num == 7:
            seven_dist = [2,3,4,1,2,3,0,1,2]
            man_dist += seven_dist[i]
        elif num == 8:
            eight_dist = [3,2,3,2,1,2,1,0,1]
            man_dist += eight_dist[i]

    return man_dist

def manhattan_heur_search(puzzles: list):
    print('\n*--------------------Manhattan Tile Heuristic--------------------*\n')

    for i, puzzle in enumerate(puzzles, start=0):
        curr_puzzle = EightPuzzle(puzzle)
        start_time = time.time()
        result,removed_nodes = astar_search(curr_puzzle, manhattan_heur)
        elapsed_time = time.time() - start_time
        curr_puzzle
        print(f'  Puzzle {i+1}: {puzzle}\n')
        print('  Elapsed run time (in seconds):                     ',
              f'{elapsed_time:.8f}s')
        print('  Length of tiles moved to get to solution:          ',
              f'{len(result.solution())}')
        print('  Total number of nodes removed from frontier:       ',
              f'{removed_nodes}\n')

def max_misplaced_manhattan_heur(node: Node):
    curr_puzzle = EightPuzzle(node.state)
    return max(curr_puzzle.h(node), manhattan_heur(node))

def max_misplaced_manhattan_search(puzzles: list):
    print('\n*------------Max Misplaced & Manhattan Tile Heuristic------------*\n')

    for i, puzzle in enumerate(puzzles, start=0):
        curr_puzzle = EightPuzzle(puzzle)
        start_time = time.time()
        result,removed_nodes = astar_search(curr_puzzle, 
                                            max_misplaced_manhattan_heur)
        elapsed_time = time.time() - start_time
        print(f'  Puzzle {i+1}: {puzzle}\n')
        print('  Elapsed run time (in seconds):                     ',
              f'{elapsed_time:.8f}s')
        print('  Length of tiles moved to get to solution:          ',
              f'{len(result.solution())}')
        print('  Total number of nodes removed from frontier:       ',
              f'{removed_nodes}\n')

#------------------------------------------------------------------------------

# Question 3:
def make_rand_duck_puzzle():
    initial_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    rand_puzzle = DuckPuzzle(initial_state)
    moves_taken = []
    previous_state = initial_state
    for i in range(50):
        
        list_possible_moves = rand_puzzle.actions(previous_state)
        num_of_moves = len(list_possible_moves)
        next_move_index = random.randrange(num_of_moves)
        next_move = list_possible_moves[next_move_index]
        moves_taken.append(next_move)
        changed_state = rand_puzzle.result(previous_state, next_move)
        previous_state = changed_state
 
    if rand_puzzle.check_solvability(changed_state, moves_taken):
        return changed_state
    else:
        assert False,("  State Not Solvable. Program Terminated.")
 
def display_duck(state):
    state_list = list(state)
    state_list = ['*' if x==0 else x for x in state_list]
    state_list = str(state_list).replace(',', '').replace('\'','')
    print('\n\t\t      Solvable Puzzle Example:')
    print('\t\t\t   ',(state_list)[1:4]) 
    print('\t\t\t   ',(state_list)[5:12]) 
    print('\t\t\t        '+ (state_list)[13:18])

def create_10_ducks():
    puzzles = []
    for i in range(10):
        puzzles.append(make_rand_duck_puzzle())
    return puzzles

def misplaced_tile_heur_search_duck(puzzles: list):
    print('\n*------------Misplaced Tile Heuristic - Duck Edition-------------*\n')

    for i, puzzle in enumerate(puzzles, start=0):
        start_time = time.time()
        result,removed_nodes = astar_search(DuckPuzzle(puzzle))
        elapsed_time = time.time() - start_time
        print(f'  Puzzle {i+1}: {puzzle}\n')
        print('  Elapsed run time (in seconds):                     ',
              f'{elapsed_time:.8f}s')
        print('  Length of tiles moved to get to solution:          ',
              f'{len(result.solution())}')
        print('  Total number of nodes removed from frontier:       ',
              f'{removed_nodes}\n')

def manhattan_heur_duck(node: Node):
    # Manhattan Heuristic Function Duck Edition
    curr_state = node.state
    man_dist = 0
    for i, num in enumerate(curr_state, start=0):
        if num == 1:
            one_dist = [0,1,1,2,3,4,3,4,5]
            man_dist += one_dist[i]
        elif num == 2:
            two_dist = [1,0,2,1,2,3,2,3,4]
            man_dist += two_dist[i]
        elif num == 3:
            three_dist = [1,2,0,1,2,3,2,3,4]
            man_dist += three_dist[i]
        elif num == 4:
            four_dist = [2,1,1,0,1,2,1,2,3]
            man_dist += four_dist[i]
        elif num == 5:
            five_dist = [3,2,2,1,0,1,2,1,2]
            man_dist += five_dist[i]
        elif num == 6:
            six_dist = [4,3,3,2,1,0,3,2,1]
            man_dist += six_dist[i]
        elif num == 7:
            seven_dist = [3,2,2,1,2,3,0,1,2]
            man_dist += seven_dist[i]
        elif num == 8:
            eight_dist = [4,3,3,2,1,2,1,0,1]
            man_dist += eight_dist[i]

    return man_dist

def manhattan_heur_search_duck(puzzles: list):
    print('\n*-------------Manhattan Tile Heuristic - Duck Edition------------*\n')

    for i, puzzle in enumerate(puzzles, start=0):
        curr_puzzle = DuckPuzzle(puzzle)
        start_time = time.time()
        result,removed_nodes = astar_search(curr_puzzle, manhattan_heur_duck)
        elapsed_time = time.time() - start_time
        curr_puzzle
        print(f'  Puzzle {i+1}: {puzzle}\n')
        print('  Elapsed run time (in seconds):                     ',
              f'{elapsed_time:.8f}s')
        print('  Length of tiles moved to get to solution:          ',
              f'{len(result.solution())}')
        print('  Total number of nodes removed from frontier:       ',
              f'{removed_nodes}\n')

def max_misplaced_manhattan_heur_duck(node: Node):
    curr_puzzle = DuckPuzzle(node.state)
    return max(curr_puzzle.h(node), manhattan_heur(node))

def max_misplaced_manhattan_search_duck(puzzles: list):
    print('\n*-----Max Misplaced & Manhattan Tile Heuristic - Duck Edition----*\n')

    for i, puzzle in enumerate(puzzles, start=0):
        curr_puzzle = DuckPuzzle(puzzle)
        start_time = time.time()
        result,removed_nodes = astar_search(curr_puzzle, 
                                            max_misplaced_manhattan_heur_duck)
        elapsed_time = time.time() - start_time
        print(f'  Puzzle {i+1}: {puzzle}\n')
        print('  Elapsed run time (in seconds):                     ',
              f'{elapsed_time:.8f}s')
        print('  Length of tiles moved to get to solution:          ',
              f'{len(result.solution())}')
        print('  Total number of nodes removed from frontier:       ',
              f'{removed_nodes}\n')

class DuckPuzzle(Problem):
    """ Apparently this looks like a duck:
   +--+--+
   |  |  |
   +--+--+--+--+
   |  |  |  |  |
   +--+--+--+--+
      |  |  |  |
      +--+--+--+
1 2
3 4 5 6 
  7 8 *    : goal state"""

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

        # 1 2       --> 0 1      (indices)
        # 3 4 5 6       2 3 4 5
        #   7 8 *         6 7 8
        #Rules for above
        if index_blank_square == 0 or index_blank_square == 2 or \
            index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or \
            index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or \
            index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square == 6 or \
            index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        #these dictionary values are indicies to add
        # We know
        # 0 1      (indices)   
        # 2 3 4 5                            
        #   6 7 8                      

        if blank == 0 or blank == 1:
            top_row = {'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + top_row[action] 
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
            return tuple(new_state)
        elif blank == 2:
            middle_row = {'UP': -2, 'RIGHT': 1}
            neighbor = blank + middle_row[action] 
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
            return tuple(new_state)
        elif blank == 3:
            middle_row = {'UP': -2, 'DOWN': 3, 'LEFT': -1,'RIGHT': 1}
            neighbor = blank + middle_row[action] 
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
            return tuple(new_state)
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1} 
            neighbor = blank + delta[action] 
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
            return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

    def check_solvability(self, state, moves: list):
        """ Checks if the given state is solvable """
        # state is the puzzle we are trying to see is solvable
        # moves is the list of moves we used to get to the state

        curr_state = state
        # reverses all the moves because we are working from the goal
        reversed_moves = moves[::-1]

        # now we have to get the opposite of the moves
        opposite_moves = []
        for i in range(50):
          # use a dictionary
          delta = {'UP':'DOWN', 'DOWN': 'UP', 'LEFT':'RIGHT', 'RIGHT':'LEFT'}
          # gets the current move
          curr_move = reversed_moves[i]
          # accesses the dictionary
          opposite_moves.append(delta[curr_move])   
        
        #set the previous_state the the goal state to start off with  
        previous_state = curr_state
        for i in range(50):
            #gets the next move from the backwards/opposite list
            next_move = opposite_moves[i]
            #changes the state by using result
            changed_state = self.result(previous_state, next_move)
            #sets the previous state as the new state
            previous_state = changed_state
        if changed_state != self.goal:
            print(f'did not work: {changed_state}, {self.goal}')
        return changed_state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

def main():
   # Question 1: Helper Functions
    print(' \t\t-----------------------------------')
    print(' \t\t* Helper Functions - Eight Puzzle *')
    print(' \t\t-----------------------------------')
    random_puzzle = make_rand_8_puzzle()
    display(random_puzzle)

   # Question 2: 8-Puzzle
    print(' \n\t\t----------------------------------')
    print(' \t\t*   Heuristics - Eight Puzzle    *')
    print(' \t\t----------------------------------')
    puzzles = create_10_puzzles()
    misplaced_tile_heur_search(puzzles)
    manhattan_heur_search(puzzles)
    max_misplaced_manhattan_search(puzzles)

    # Question 3: DuckPuzzle
    # These are recreated Question 1 problems for the DuckPuzzle 
    print('\n \t\t-----------------------------------')
    print(' \t\t* Helper Functions - Duck Puzzle  *')
    print(' \t\t-----------------------------------')
    random_duck = make_rand_duck_puzzle()
    display_duck(random_duck)

    #These are recreated Question 2 problems for the DuckPuzzle
    print(' \n\t\t----------------------------------')
    print(' \t\t*   Heuristics - Duck Puzzle     *')
    print(' \t\t----------------------------------')
    puzzles = create_10_ducks()
    misplaced_tile_heur_search_duck(puzzles)
    manhattan_heur_search_duck(puzzles)
    max_misplaced_manhattan_search_duck(puzzles)

if __name__ == "__main__":
    main()