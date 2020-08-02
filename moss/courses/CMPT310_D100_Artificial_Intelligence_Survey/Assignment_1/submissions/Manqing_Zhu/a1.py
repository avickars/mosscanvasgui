# a1.py

from search import *
from random import shuffle
import time

# Return a randomly-generated, solvable 8Puzzle problem instance
def make_rand_8puzzle():
    initial = list(range(9))
    shuffle(initial)
    puzzle = EightPuzzle(tuple(initial))
    if(puzzle.check_solvability(puzzle.initial) == False):
        puzzle.initial = tuple(swap_first_two_nonzero(initial))
    assert puzzle.check_solvability(puzzle.initial) == True, "initial state is unsolvable"
    return puzzle

# Return a new list with the first two non-zero elements swapped
def swap_first_two_nonzero(target_list):
    for i in range(len(target_list)):
        if(target_list[i] == 0):
            continue
        for j in range(i+1, len(target_list)):
            if(target_list[j] == 0):
                continue
            target_list[i], target_list[j] = target_list[j], target_list[i]
            return target_list
    return []

# print a state in the readable form
def display(state):
    assert len(state) == 9, "invalid input to display(state): the length of state should be 9"
    for i in range(len(state)):
        if(state[i] == 0):
            print('*', end='')
        else:
            print(state[i], end='')
        
        if(i % 3 == 2):
            print('')
        else:
            print(' ', end='')

NUM_OF_PUZZLE_INSTANCES = 30

# Return the Manhattan distance heuristic
def manhattan_heuristic(node, hashMap):
    sum = 0
    for i in range(len(node.state)):
        x_state = i % 3
        y_state = i // 3
        x_goal = hashMap[node.state[i]] % 3
        y_goal = hashMap[node.state[i]] // 3
        sum += abs(x_state - x_goal) + abs(y_state - y_goal)
    return sum

# Return the max of the misplaced tile heuristic and the Manhattan distance heuristic
def best_heuristic(node, hashMap, h):
    default = h(node)
    manhattan = manhattan_heuristic(node, hashMap)
    return max(default, manhattan)

# Run A* search using different heuristic value, print statistic info
def algo_statistic(description, puzzle, heuristic_func):
    print(description)
    start_time = time.time()
    # the number of nodes removed from Frontier = the number of path expanded + 1
    node = astar_search(puzzle, heuristic_func, True)
    elapsed_time = time.time() - start_time
    if(node != None):
        print(f'elapsed time (in seconds): {elapsed_time}s')
        print('the length of solution is', node.path_cost)
    else:
        print("unsolvable")
    return node

def compare_algo():
    puzzle_list = []
    for i in range(NUM_OF_PUZZLE_INSTANCES):
        puzzle_list.append(make_rand_8puzzle())
    
    goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    goalHash = {}
    for i in range(len(goal)):
        goalHash[goal[i]] = i

    
    for i in range(len(puzzle_list)):
        print(f'puzzle no.{i+1}')
        display(puzzle_list[i].initial)

        algo_statistic("the misplaced tile heuristic:", puzzle_list[i], None)
        algo_statistic("the Manhattan distance heuristic:",
                       puzzle_list[i], lambda n: manhattan_heuristic(n, goalHash))
        algo_statistic("the best heuristic:", puzzle_list[i], 
        lambda n: best_heuristic(n, goalHash, puzzle_list[i].h))

#=============================================================================================

class DuckPuzzle(EightPuzzle):
    """ The problem of sliding tiles numbered from 1 to 8 on a duck board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square < 2 or (index_blank_square > 3 and index_blank_square < 6):
            possible_actions.remove('UP')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if(blank < 2):
            delta['DOWN'] = 2
        elif(blank < 6):
            delta['UP'] = -2

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

# Return a randomly-generated DuckPuzzle problem instance
def make_rand_duck():
    initial = list(range(9))
    shuffle(initial)
    puzzle = DuckPuzzle(tuple(initial))
    return puzzle

# print a state of DuckPuzzle in the readable form
def display_duck(state):
    assert len(state) == 9, "invalid input to display(state): the length of state should be 9"
    for i in range(len(state)):
        if(i == 6):
            print('  ', end='')

        if(state[i] == 0):
            print('*', end='')
        else:
            print(state[i], end='')

        if(i == 1 or i == 5 or i == 8):
            print('')
        else:
            print(' ', end='')

def get_duck_x(idx):
    x = 0
    if(idx < 2):
        x = idx
    elif(idx < 6):
        x = idx - 2
    else:
        x = idx - 5
    return x

def get_duck_y(idx):
    y = 0
    if(idx > 1):
        y += 1
    if(idx > 5):
        y += 1
    return y

# Return the Manhattan distance heuristic
def duck_manhattan_heuristic(node, hashMap):
    sum = 0
    for i in range(len(node.state)):
        x_state = get_duck_x(i)
        y_state = get_duck_y(i)
        x_goal = get_duck_x(hashMap[node.state[i]])
        y_goal = get_duck_y(hashMap[node.state[i]])
        sum += abs(x_state - x_goal) + abs(y_state - y_goal)
    return sum

# Return the max of the misplaced tile heuristic and the Manhattan distance heuristic
def duck_best_heuristic(node, hashMap, h):
    default = h(node)
    manhattan = duck_manhattan_heuristic(node, hashMap)
    return max(default, manhattan)

def duck_compare_algo():
    goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    goalHash = {}
    for i in range(len(goal)):
        goalHash[goal[i]] = i
    
    count = 0
    while(count != NUM_OF_PUZZLE_INSTANCES):
        puzzle = make_rand_duck()

        node = algo_statistic("the misplaced tile heuristic:", puzzle, None)
        if node != None:
            print(f'duck puzzle no.{count+1}')
            display_duck(puzzle.initial)
            algo_statistic("the Manhattan distance heuristic:", puzzle,
                           lambda n: duck_manhattan_heuristic(n, goalHash))
            algo_statistic("the best heuristic:", puzzle,
                       lambda n: duck_best_heuristic(n, goalHash, puzzle.h))
            count += 1

if __name__ == "__main__":
    compare_algo()
    duck_compare_algo()
