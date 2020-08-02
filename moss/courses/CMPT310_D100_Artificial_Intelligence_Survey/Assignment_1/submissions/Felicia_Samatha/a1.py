#a1.py 
from search import *
import time

"""README: Running the code will produce 10 EightPuzzles and 10 DuckPuzzles. Please refer to the last two lines to change 
the number of puzzles the code needs to produce or commenting it out."""

""" EightPuzzle Class (differences from .h file): Two functions were added (manhat_h and maxh). 
    In addition, changes were made to the h(self,node) function"""

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
        #Added s!=0: Old h overestimated the hueristic value. Ex: If 8 and 0 were switched, h = 2 rather than 0
        return sum(s != g and s!=0 for (s, g) in zip(node.state, self.goal))

    #Q1: Manhattan Heuristics
    def manhat_h(self, node):
        """Returns the Manhattan heuristic value for a given state.
        manhat_h = |xstart - xdest| + |ystart - ydest|."""

        #Goal state of each number mapped to 3x3 grid 
        correct_pos = { 1:(0,0), 2:(0,1), 3:(0,2), 4:(1,0), 5:(1,1), 6:(1,2), 7:(2,0), 8:(2,1), 0:(2,2)} 
        state_pos = node.state
        num = 0
        test = [[0, 0, 0], [0, 0, 0], [0, 0, 0]] 

        #Put generated puzzle in 3x3
        for i in range(3):
            for j in range (3):
                test[i][j] = state_pos[num]
                num += 1

        #Find number of x and y moves to put piece in correct position and apply formula
        x_sum = 0
        y_sum = 0
        for i in range(3):
            for j in range(3):
                piece = test[i][j]
                #print(piece)
                if( piece != 0):
                    x_sum = x_sum + abs (correct_pos[piece][1] - j)
                    y_sum = y_sum + abs (correct_pos[piece][0] - i)         
        #h = |xstart - xdest| + |ystart - ydest|
        h = x_sum + y_sum
        return h

    #Q1: Finds the maximum between h and manhat_h
    def maxh(self, node):
        manhattan = EightPuzzle.manhat_h(self,node)
        mis_tile = EightPuzzle.h(self,node)
        return max(manhattan, mis_tile)
# ______________________________________________________________________________
""" Two functions for EightPuzzle. First generates a random one, second displays it
in 3x3 format."""

#Q1. Returns a solvable puzzle for EightPuzzle
def make_rand_8puzzle():
    is_solvable = False
    #Continue till solvable
    while not is_solvable:
        #Shuffle to create random initial state
        valid_num = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(valid_num)
        rand_tuple=tuple(valid_num)
        Epuzzle = EightPuzzle(initial = rand_tuple)

        #Check
        is_solvable = (Epuzzle.check_solvability(rand_tuple))
        #print(is_solvable)
    return Epuzzle

#Displays puzzle in 3x3 format
def display(state):
    for i in range(9):
        num = state.initial
        if state.initial[i]== 0:
            print("* ", end='')
        else:
            print("{} ".format(num[i]), end='')
        if ((i+1)%3 == 0):
            print('')
# ______________________________________________________________________________
"""Q3: Changed class of EightPuzzle to correspond with DuckPuzzle.
    The result, actions, and h functions were modified. 
    A manhattan heuristic function (duckMan) and maximum heuristic function (duck_maxh)
    were added.
"""
class DuckPuzzle(Problem):
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
        #For DuckPuzzle, UP21 moves piece up from row 2 to row 1 and DOWN 21 moves from row 1 to 2
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'UP21', 'DOWN12']
        index_star = self.find_blank_square(state)

        #At most left at index 0, 2, 6
        if index_star == 0 or index_star == 2 or index_star == 6:
            possible_actions.remove('LEFT')
        #Up21 only applies to index 2 and 3
        if index_star != 2 and index_star != 3:
            possible_actions.remove('UP21')
        #Can't go up if index at 0-5
        if index_star < 6:
            possible_actions.remove('UP')
        #Can't go right if index at 1, 5, 8
        if index_star == 1 or index_star == 5 or index_star == 8:
            possible_actions.remove('RIGHT')
        #Down12 only applies to row 1 (ndex 0 and 1)
        if index_star > 1:
            possible_actions.remove('DOWN12')
        #Down only works if index at 3, 4, 5
        if index_star > 5 or index_star < 3:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        #For DuckPuzzle, UP21 moves piece up from row 2 to and 1 and DOWN 21 moves it down
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1, 'UP21' : -2, 'DOWN12' : 2}

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

        #Althered (same reason as the one in EightPuzzle)
        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

    #Manhattan heuristic for DuckPuzzle
    def duckMan(self, node):
        """manhat_h function = |xstart - xdest| + |ystart - ydest|."""

        #Goal state of each number mapped to 3x3 grid 
        correct_pos = { 1:(0,0), 2:(0,1), 3:(1,0), 4:(1,1), 5:(1,2), 6:(1,3), 7:(2,1), 8:(2,2), 0:(2,3)}  
        state_pos = node.state
        num = 0
        test = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]] 

        #Put generated puzzle in DuckPuzzle format
        for j in range(2):
            test[0][j] = state_pos[num]
            num += 1
        for j in range(4):
            test [1][j] = state_pos[num]
            num += 1
        for j in range(4):
            if j != 0:
                test [2][j] = state_pos[num]
                num+=1
    
        x_sum = 0
        y_sum = 0
        #Find number of x and y moves to put piece in correct position
        for i in range(3):
            for j in range(4):
                if( (i==0 and j==2) or (i==0 and j==3) or (i==2 and j==0) ):
                    continue
                else:
                    piece = test[i][j]
                    #Exclude 0
                    if( piece != 0):
                        x_sum = x_sum + abs (correct_pos[piece][1] - j)
                        y_sum = y_sum + abs (correct_pos[piece][0] - i)

        #h = |xstart - xdest| + |ystart - ydest|
        h = x_sum + y_sum
        return h

    #Max of heuristics for DuckPuzzle
    def duck_maxh(self, node):
        manhattan = DuckPuzzle.duckMan(self,node)
        mis_tile = DuckPuzzle.h(self,node)
        return max(manhattan, mis_tile)

# ______________________________________________________________________________
"""Functions to make a random DuckPuzzle that's solvable and to display it in 
its format."""

def make_rand_DuckPuz():
    """Random puzzle generator for DuckPuzzle. Generated by moving valid moves
from goal state """
    goal_puzzle = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    #Number of times to scramble
    scramble_num = 10000

    while (scramble_num > 0):
        perform = DuckPuzzle.actions(DuckPuzzle(tuple(goal_puzzle)), goal_puzzle)
        random.shuffle(perform)
        goal_puzzle = DuckPuzzle.result(DuckPuzzle(tuple(goal_puzzle)), goal_puzzle, perform[0])
        scramble_num -= 1
        rand_puzzle = DuckPuzzle(initial = tuple(goal_puzzle))
    return rand_puzzle


def Duckdisplay(state):  
    for i in range(9):
        num = state.initial
        if (i == 6):
            print(" ", end = ' ')
        if state.initial[i] == 0:
            print("* ", end='')
        else:
            print("{} ".format(num[i]), end='')
        if (i == 1 or i == 5 ):
            print('')   
# ______________________________________________________________________________

"""Search functions from search.py, added a counter for nodes removed"""

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    nodes_removed = 0

    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        #Counter for nodes removed
        nodes_removed += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                #print("Nodes removed from frontier:", nodes_removed)
            return [node, nodes_removed]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# ______________________________________________________________________________
"""Two functions to run the two puzzles as many times as desired. Outputs the puzzle in 
    proper format, time, length of solution and nodes popped """

#Q1 and 2: EightPuzzles, specify how many puzzles to make
def runEPuzzles(amount):
    """ Runs EightPuzzles ten times"""

    for i in range(amount):
        print("EIGHTPUZZLE NUMBER:", i+1)
        puz1 = make_rand_8puzzle()
        #puz1 = EightPuzzle(initial=(8,0,7,2,5,1,3,6,4))
        display(puz1)

        #Astar search with misplaced tile (MPT)
        start = time.time()
        solve_puz = astar_search(puz1, h = puz1.h,display=False)
        end = time.time()
        print("Using misplaced tile, it took", end-start, "seconds to complete the puzzle.")
        solution_length = (solve_puz[0].path_cost)
        print("MPT: total length of the soltuion is:", solution_length)
        print("Nodes removed from frontier:", solve_puz[1])
        print("\n")

        #Astar search with Manhattan
        start = time.time()
        solve_puz = astar_search(puz1, h = puz1.manhat_h,display=False)
        end = time.time()
        print("Using manhattan, it took", end-start, "seconds to complete the puzzle.")
        solution_length1 = (solve_puz[0].path_cost)
        print("Manhattan, total length of the solution is:", solution_length1)
        print("Nodes removed from frontier:", solve_puz[1])
        print("\n")

        #Astar search with max of Manhattan and misplaced tile
        start = time.time()
        solve_puz = astar_search(puz1, h = puz1.maxh, display=False)
        end = time.time()
        print("Using max, it took", end-start, "seconds to complete the puzzle.")
        solution_length2 = (solve_puz[0].path_cost)
        print("Max, total length of the soltuion is:", solution_length2)
        print("Nodes removed from frontier:", solve_puz[1])

#Q3: Duck Puzzles
def runDpuzzles(amount):
    for i in range(amount):
        print("DUCKPUZZLE NUMBER:", i+1)
        Dpuzzle = make_rand_DuckPuz()
        #Dpuzzle = DuckPuzzle(initial=(1,2,3,4,5,0,6,7,8))
        Duckdisplay(Dpuzzle)
        print("\n")

        #Misplaced Tiles (MPT)
        start = time.time()
        solve_Dpuzzle = astar_search(Dpuzzle, h=Dpuzzle.h, display=False)
        end = time.time()
        print("Using, MPT, it took", end-start, "seconds to complete the puzzle.")
        Dsolution_length = (solve_Dpuzzle[0].path_cost)
        print("Max, total length of the solution is:", Dsolution_length)
        print("Nodes removed from frontier:", solve_Dpuzzle[1])
        print("\n")

        #Manhattan
        start = time.time()
        solve_Dpuzzle = astar_search(Dpuzzle, h=Dpuzzle.duckMan, display=False)
        end = time.time()
        print("Using, Manhattan, it took", end-start, "seconds to complete the puzzle.")
        Dsolution_length = (solve_Dpuzzle[0].path_cost)
        print("Max, total length of the solution is:", Dsolution_length)
        print("Nodes removed from frontier:", solve_Dpuzzle[1])
        print("\n")

        #Max
        start = time.time()
        solve_Dpuzzle = astar_search(Dpuzzle, h=Dpuzzle.duck_maxh, display=False)
        end = time.time()
        print("Using, the max, it took", end-start, "seconds to complete the puzzle.")
        Dsolution_length = (solve_Dpuzzle[0].path_cost)
        print("Max, total length of the solution is:", Dsolution_length)
        print("Nodes removed from frontier:", solve_Dpuzzle[1])

# ______________________________________________________________________________
#Main
#Uncomment the functions if you would like to implement your own test code

#Create EightPuzzles: runEpuzzles(amount)
runEPuzzles(10)
#Create DuckPUzzles: runDpuzzles(amount)
runDpuzzles(10)


