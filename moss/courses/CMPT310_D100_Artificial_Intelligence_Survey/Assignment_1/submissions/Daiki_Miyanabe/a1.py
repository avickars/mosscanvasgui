# a1.py

from search import *

# Written by Daiki Miyanabe (dmiyanab@sfu.ca)
# Helped by tutorial session by TA:  Mohammadmahdi Jahanara,
# Other resources: 
# Printing without new line: https://careerkarma.com/blog/python-print-without-new-line/
# original codes form aima-python
import time


#part 1
def make_rand_8puzzle():
    #returns new instance of EightPuzzle
    state = tuple(np.random.permutation(9))
    temp_puzzle =EightPuzzle(initial=state)
    
    while not temp_puzzle.check_solvability(state):
        state = tuple(np.random.permutation(9))
        temp_puzzle =EightPuzzle(initial=state)
        
    return temp_puzzle  

def display(state):
    #displays 8 puzzle state, blank is displayed as *
    
    if state and len(state) == 9:
        for row in range(3): #iterate rows
            for col in range(3): #iterate columns
                if state[3*row + col] == 0: #if blank
                    print('*', end=' ')
                else:
                    print(state[3*row + col], end=' ')
            print('\n')
    else:
        print('State is empty or not in correct format')

        
#extra
def get_solvable_state():
    state = tuple(np.random.permutation(9))
    temp_puzzle =EightPuzzle(initial=state)
    
    while not temp_puzzle.check_solvability(state):
        state = tuple(np.random.permutation(9))
        temp_puzzle =EightPuzzle(initial=state)
        
    return state
    
#Part 2
#original from aima-python search.py
def best_first_graph_search_modified(problem, f, display=False):
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
    
    removedFromFrontier = 0 #added by dmiyanab
    lengthOfSolution = 0;#added by dmiyanab
    
    while frontier:
        node = frontier.pop()
        removedFromFrontier += 1#added by dmiyanab
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                print("Number of nodes removed form Frontier:", removedFromFrontier, ' Length:', node.depth)#added by dmiyanab
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

#original from aima-python search.py
def astar_search_modified(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_modified(problem, lambda n: n.path_cost + h(n), display)

#original from aima-python search.py, default heuristic, calculate number of missplaced tiles
def h_misplaced_max(node):
    """ Return the heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles """
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return max(s != g for (s, g) in zip(node.state, goal))


#part 2
def h_manhattan(node):
    manh_distance = 0
    
    #calculate heuristic using total Manhattan distance for the whole panel in a state
    if node.state and len(node.state) == 9:
        for row in range(3):
            for col in range(3):
                manh_distance += h_manhattan_cell(node.state[3*row+col] ,row, col)
        node.state
    else:
        print('node.state undefined or size is not 9')
    
    return manh_distance
        
def h_manhattan_cell(value, row, col):
    #calculate Manhattan distance for specific cell
    if not (value >=0 and row >=0 and col >=0):
        #validate imputs
        print('value, row or col undefined')
    else:
        #calculate position of solution for this cell
        if value == 0:
            rowSol = 2
            colSol = 2
        else:
            rowSol = (value-1)//3
            colSol = (value-1)%3
    
        #distance = offset in x + offset in y 
        distance = abs(row - rowSol) + abs(col - colSol)
        return distance
    
def h_manhattan_combined(node):
    #calculate heuristic using both the Manhattan distance and the number of missplaced tiles
    h_manh = h_manhattan(node)
    h_misplaced = h_misplaced_max(node)
    return h_misplaced +h_manh


#part 3
#original from aima-python modified by dmiyanab

class DuckPuzzle (Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):#changed
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """
        
        '''
         Goal state
         1 2
         3 4 5 6   
           7 8 *
        '''

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        if index_blank_square == 1:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        #if index_blank_square == 3:
            #no restriction
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')


        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        #changed
        if blank <=1:
            delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank <=3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif blank <=5:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif blank <=8:
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
        check_inversion =  inversion% 2 == 0
        
        # edited: specific for duck_puzzle 
        # due to the design of the puzzle numbers 1-3 can only rotate within position 0-3
        # similarly, numbers 5-8 can only rotate within position 3-8
        if state[0] > 3 or state[1] > 3 or state[2] > 3:
            #position 0~2 cannot have any number other than 0,1,2 in duck_puzzle
            check_state = False
        elif (state[4] <= 3 and state[4] != 0) or (state[5] <= 3 and state[5] != 0)  or (state[6] <= 3 and state[6] != 0)  or (state[7] <= 3 and state[7] != 0) or (state[8] <= 3 and state[8] != 0):
            #position 4~8 cannot have any number other than 4,5,6,7,8 in duck_puzzle
            check_state = False
        else: 
            check_state = True
        
        
        return check_inversion and check_state

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

def make_rand_duckpuzzle():
    #returns new instance of EightPuzzle
    state = tuple(np.random.permutation(9))
    temp_puzzle =DuckPuzzle(initial=state)
    
    while not temp_puzzle.check_solvability(state):
        state = tuple(np.random.permutation(9))
        temp_puzzle =DuckPuzzle(initial=state)
        
    return temp_puzzle  



#test part 1
def a1_test_part1():
    print('Testing Part 1')
    print('display(state):')
    a = make_rand_8puzzle()
    state = get_solvable_state()
    display(state)
    print('actual tuple in state:')
    print(state)

#test part 2
def a1_test_part2():
    print('Testing Part 2')
    for x in range(21):
        puzzle = make_rand_8puzzle()
        print('*******Iteration:', x ,'********')
        display(puzzle.initial)


        print('=======starting Default h=======')
        start_time = time.time()
        astar_search_modified(puzzle, display=True)
        elapsed_time = time.time() - start_time
        print(f'Default: elapsed time (in seconds): {elapsed_time}s')


        print('=======starting Manhattan h=======')
        start_time = time.time()
        astar_search_modified(puzzle, display=True, h=h_manhattan)
        elapsed_time = time.time() - start_time
        print(f'Manhattan: elapsed time (in seconds): {elapsed_time}s')

        print('=======starting Combined h=======')
        start_time = time.time()
        astar_search_modified(puzzle, display=True, h=h_manhattan_combined)
        elapsed_time = time.time() - start_time
        print(f'Combined: elapsed time (in seconds): {elapsed_time}s')

        print('\n')
    print('End Test Part 2')
    
def a1_test_part3():
    #test
    print('Testing Part 3')
    state = (3, 1, 2, 0, 6, 8, 7, 5, 4)
    DUCK_puzzle =DuckPuzzle(initial=state)
    print(DUCK_puzzle.check_solvability(state))

    print('=======starting Default h=======')
    start_time = time.time()
    astar_search_modified(DUCK_puzzle, display=True)
    elapsed_time = time.time() - start_time
    print(f'Default: elapsed time (in seconds): {elapsed_time}s')
    
    print('=======starting Manhattan h=======')
    start_time = time.time()
    astar_search_modified(DUCK_puzzle, display=True, h=h_manhattan)
    elapsed_time = time.time() - start_time
    print(f'Manhattan: elapsed time (in seconds): {elapsed_time}s')
    
    
    print('=======starting Combined h=======')
    start_time = time.time()
    astar_search_modified(DUCK_puzzle, display=True, h=h_manhattan_combined)
    elapsed_time = time.time() - start_time
    print(f'Combined: elapsed time (in seconds): {elapsed_time}s')
    print('End Test Part 3')

    for x in range(11):
        DUCK_puzzle = make_rand_duckpuzzle()
        print('*******Iteration:', x ,'********')
        display(DUCK_puzzle.initial)


        print('=======starting Default h=======')
        start_time = time.time()
        astar_search_modified(DUCK_puzzle, display=True)
        elapsed_time = time.time() - start_time
        print(f'Default: elapsed time (in seconds): {elapsed_time}s')


        print('=======starting Manhattan h=======')
        start_time = time.time()
        astar_search_modified(DUCK_puzzle, display=True, h=h_manhattan)
        elapsed_time = time.time() - start_time
        print(f'Manhattan: elapsed time (in seconds): {elapsed_time}s')

        print('=======starting Combined h=======')
        start_time = time.time()
        astar_search_modified(DUCK_puzzle, display=True, h=h_manhattan_combined)
        elapsed_time = time.time() - start_time
        print(f'Combined: elapsed time (in seconds): {elapsed_time}s')

        print('\n')
    