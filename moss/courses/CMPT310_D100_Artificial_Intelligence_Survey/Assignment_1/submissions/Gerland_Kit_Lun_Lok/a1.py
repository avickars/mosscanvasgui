# a1.py

from search import *
import time
import math

#

def run_Puzzle(puzzle, h):
   start_time = time.time()
   node = puzzle.astar_search(h, True)
   end_time = time.time()
   run_time = end_time - start_time
   print(f'Elapsed time (in seconds): {run_time}', end = '\n\n')
   print('Solution: ', node.solution(), end = '\n\n')
   print('Path: ', node.path(), end = '\n\n')
   print('Path length: ', len(node.path()), end = '\n\n')

def make_rand_8puzzle():
    while True: 
        intial_puzzle = (1,2,3,4,5,6,7,8,0)
        rand_8puzzle = Eight_Puzzle(intial_puzzle) 
        
        for x in range(500):
            solvable_puzzle = False
            possible_action = rand_8puzzle.actions(intial_puzzle)
            counter = 0
            while(solvable_puzzle == False):
                random.randint(0,len(possible_action))
                next_state = rand_8puzzle.result(intial_puzzle, possible_action[random.randint(0,len(possible_action)-1)])
                if(rand_8puzzle.check_solvability(next_state) or counter >= 15): #Counter prevents infinite loop
                    intial_puzzle = next_state
                    solvable_puzzle = True
                    break
                counter + 1
        print('Randomly generated 8 Puzzle:')
        print(intial_puzzle)
        return Eight_Puzzle(intial_puzzle)

def make_rand_DuckPuzzle():
    while True: 
        puzzle_state = (1,2,3,4,5,6,7,8,0)
        rand_Duckpuzzle = DuckPuzzle(puzzle_state) 
        
        for x in range(500):  
            possible_action = rand_Duckpuzzle.actions(puzzle_state)
            random.randint(0,len(possible_action))
            puzzle_state = rand_Duckpuzzle.result(puzzle_state, possible_action[random.randint(0,len(possible_action)-1)])
        print('Randomly generated Duck Puzzle:')
        print(puzzle_state)
        return DuckPuzzle(puzzle_state)


def display(state):
    for x in range(len(state)):
        if (x+1) % 3 == 0:
            if int(state[x]) == 0:
                print('*')
            else:
                print(state[x])

        else:
            if int(state[x]) == 0:
                print('*', end = '')
            else:
                print(state[x], end = '')

def displayDuck(state):
    print('+-+-+')
    for x in range(len(state)):
        print('|', end = '')
        if x == 1 or x == 5 or x == 8:
            if int(state[x]) == 0:
                print('*', end = '|\n')
            else:
                print(state[x], end = '|\n')
            if x == 8: 
                print('  +-+-+-+')
            else: 
                print('+-+-+-+-+')
                if x == 5:
                    print('  ',end = '')
        else:
            if int(state[x]) == 0:
                print('*', end = '')
            else:
                print(state[x], end = '')
    
def best_first_graph_search_updated(problem, f, display=False):
    # Adapted from search.py #
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    removed = 0
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        removed = removed + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                print(f'Number of nodes removed: {removed}')
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    removed = removed + 1
                    frontier.append(child)
    return None 


class Eight_Puzzle(EightPuzzle):
    # Adapted and inheriented from EightPuzzle class of Search.py
    # Override h function and add in Manhattan and Max heuristic functions

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        #print('Using modified h heuristic')
        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

    def manhattan_h(self, node):
        h_value = 0
        position_map = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        for (s, g) in zip(node.state, self.goal):
            if s != g:
                if s != 0: #Do not include 0/* tile in calculation
                    position_s = position_map[node.state.index(s)]
                    position_g = position_map[self.goal.index(s)]
                    h_value = h_value + abs(position_s[0] - position_g[0]) + abs(position_s[1] - position_g[1]) 
        #print(f'Mahattan Distance is: {h_value}')
        return h_value

    def max_heuristic(self,node):
        return max(self.h(node), self.manhattan_h(node))

    def astar_search(self, h=None, display=False):
    # Adapted from search.py 
        h = memoize(h or self.h, 'h')
        return best_first_graph_search_updated(self, lambda n: n.path_cost + h(n), display)

class DuckPuzzle(Problem):
    # Class adapted from the EightPuzzle Class in Search.py
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

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': 0, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}

        if 0 <= blank <= 1:
            delta['DOWN'] = 2

        if 2 <= blank <= 3:
            delta['UP'] = -2
        
        if 3 <= blank <= 5:
            delta['DOWN'] = 3
        
        if 6 <= blank <= 8:
            delta['UP'] = -3

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h_duck(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

    def manhattan_h_duck(self, node):
        h_value = 0
        position_map = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
        for (s, g) in zip(node.state, self.goal):
            if s != g:
                if s != 0: #Do not include 0/* tile in calculation
                    position_s = position_map[node.state.index(s)]
                    position_g = position_map[self.goal.index(s)]
                    h_value = h_value + abs(position_s[0] - position_g[0])  # y-axis distance
                    h_value = h_value + abs(position_s[1] - position_g[1])  # x-axis distance
        #print(f'Mahattan Distance is: {h_value}')
        return h_value

    def max_heuristic_duck(self,node):
        return max(self.h_duck(node), self.manhattan_h_duck(node))

    def astar_search(self, h=None, display=False):
    # Adapted from search.py 
        print('Using new astar_search')
        h = memoize(h or self.h_duck, 'h')
        return best_first_graph_search_updated(self, lambda n: n.path_cost + h(n), display)


#########################################################
# Driver Code 

print('######################################################')
print('#      Assignment I - Experimenting with 8 Puzzle    #')
print('#               CMPT 310 - SUMMER 2020               #')
print('#               Gerland Lok; 301260310               #')
print('######################################################\n')

enable_8Puzzle = True
enable_duck = True

if enable_8Puzzle:
    print('======================================================')
    print('=              Running 8 Puzzle Tests                =')
    print('======================================================\n')
    for i in range(10):
        print('######################################################')
        print(f'#                      TEST {i+1}                       #')
        print('######################################################\n', end = '\n')
        puzzle1 = make_rand_8puzzle()
        print()
        display(puzzle1.initial)
        print('---------------Misplaced Tile Heuristic---------------')
        run_Puzzle(puzzle1, puzzle1.h)
        print('------------------------------------------------------\n')

        print('-----------------Manhattan Heuristic------------------')
        run_Puzzle(puzzle1, puzzle1.manhattan_h)
        print('------------------------------------------------------\n')
        
        print('--------------------Max Heuristic---------------------')
        run_Puzzle(puzzle1, puzzle1.max_heuristic)
        print('------------------------------------------------------\n')

if enable_duck:
    print('======================================================')
    print('=              Running Duck Puzzle Tests             =')
    print('======================================================\n')
    for i in range(10):
        print('######################################################')
        print(f'#                      TEST {i+1}                       #')
        print('######################################################\n', end = '\n')
        puzzle1 = make_rand_DuckPuzzle()
        print()
        displayDuck(puzzle1.initial)
        print('---------------Misplaced Tile Heuristic---------------')
        run_Puzzle(puzzle1, puzzle1.h_duck)
        print('------------------------------------------------------\n')

        print('-----------------Manhattan Heuristic------------------')
        run_Puzzle(puzzle1, puzzle1.manhattan_h_duck)
        print('------------------------------------------------------\n')
        
        print('--------------------Max Heuristic---------------------')
        run_Puzzle(puzzle1, puzzle1.max_heuristic_duck)
        print('------------------------------------------------------\n')
