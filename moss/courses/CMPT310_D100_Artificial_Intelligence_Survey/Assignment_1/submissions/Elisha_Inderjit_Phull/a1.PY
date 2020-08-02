# a1.py

from search import *
import numpy as np
import random 
import time 

# -----------------------------------------------------------------------------------------------------------------------------
# Question 1: Helper Functions 

# make_rand_8puzzle().
# returns a new instance of an EightPuzzle problem with a random initial state that is solvable. 
# Note that EightPuzzle has a method called check_solvability, which is used to check if initial state is solvable.
def make_rand_8puzzle(): 
    initalstate = tuple(np.random.permutation(9))

    p1 = EightPuzzle(initial=initalstate)

    while p1.check_solvability(initalstate) == False: 
        initalstate = tuple(np.random.permutation(9))
    
    p1.initial = initalstate
    return p1


# display(state, EIGHTPUZZLE). 
# Inputs:
# takes any 8-puzzle state (i.e. a tuple that is a permutation of (0, 1, 2, …, 8))
# and boolean true if you want the EightPuzzle GameBoard display.  
# returns: readable representation of gameboard of a EightPuzzle(3-by-3) or DuckPuzzle(3-by-4).
# 0 is the blank is printed as a * character.
def display(state, EIGHTPUZZLE):

    state = list(state)

    if EIGHTPUZZLE == True: 
        for i, tile in enumerate(state, start=1):
            if tile == 0:
                tile = '*'
            print(tile, end=' ' if i % 3 else '\n')
    else: 
        for i, tile in enumerate(state, start=0):
            if tile == 0:
               tile = '*'
            if i == 0:
                print(tile, end=' ')
            if i == 1:
                print(tile, end='\n')
            if i == 2:
                print(tile, end=' ')
            if i == 3:
                print(tile, end=' ')
            if i == 4:
                print(tile, end=' ')
            if i == 5:
                print(tile, end='\n  ')
            if i == 6:
                print(tile, end=' ')
            if i == 7:
                print(tile, end=' ')
            if i == 8:
                print(tile, end='\n')
        
# -----------------------------------------------------------------------------------------------------------------------------

# Question 2: Solving the EightPuzzle Problem using Search Algo -- Compare Algo - based on:
# 1.total running time (s), 
# 2.length of solution/#tiles moves==actions-represented as branches. Each tile move has equal weight, so we can use g(x) of the goalnode//goal state to directly get the number of moves from rootnode/initial to goalnode/state
# 2.length of solution/#tiles moves==height of tree represented from goalstate to node in the explored set: count nodes added to explored set minus 2. 
# 3.total#ofnodes removed from frontier-count the pops--represents the number of nodes searched, ie., total solution space)

def astar_search1(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')

    return best_first_graph_search1(problem, lambda n: n.path_cost + h(n), display)


def best_first_graph_search1(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    count_totalsearch = 0
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    
    while frontier:
        node = frontier.pop()   #returns the node at front with smallest value. 
        count_totalsearch = count_totalsearch + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print("Was the Goal State Returned?: ", node)
            print("What is the value of f(goalnode)?", f(node))
            print("#oftile moves: g(x)=PathCost of Goal Node to Intial State", node.path_cost)
            print(node.path())
            return count_totalsearch, node.path_cost
        explored.add(node.state)
        # print("NODE ADDED TO EXPLORED: ?", node)
        # print("NODE ADDED TO EXPLORED f(node)?", f(node))
        # print("NODE ADDED TO EXPLORED g(node)", node.path_cost)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None



def algo1(obj): 
#   ALGO1: A*-search using the misplaced tile heuristic (this is the default heuristic in the EightPuzzle class)
    start_time = time.time()
    result = astar_search1(problem=obj) #setting function as an argument
    RUNTIME = time.time() - start_time
    print("\tTotal Running Time (s): ", RUNTIME)
    print("\tTotal Solution Space (Total # of Nodes Removed from Frontier): ", result[0])
    print("\tLength of/#tiles moves for the Successful solution: ", result[1])


def algo2(obj, h1):
    #   ALGO2: A*-search using the Manhattan distance heuristic Please implement your own (correctly working!) version of the Manhattan heuristic.
    # Be careful: there is an incorrect Manhattan distance function in tests/test_search.py. So don’t use that!
    start_time = time.time()
    result = astar_search1(problem=obj, h=h1) #setting function as an argument
    RUNTIME = time.time() - start_time
    print("\tTotal Running Time (s): ", RUNTIME)
    print("\tTotal Solution Space (Total # of Nodes Removed from Frontier): ", result[0])
    print("\tLength of/#tiles moves for the Successful solution: ", result[1])


def algo3(obj, h1):
    #   # ALGO3: A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic of the initial state
    # for each node/state, find which one is the max.  
    misplacedtile = obj.h(node=Node(obj.initial))
    manh_h = h1(n=Node(obj.initial))

    if misplacedtile > manh_h:
        print("Misplaced is Larger!")
        algo1(obj=obj)
    else:
        print("Manhattan is Larger!")
        algo2(obj=obj, h1=h1)

#----------------------------------------------------------------------------------------------------------------------------------------------------------

def manh(n):
    """returns the heuristic value for a given state using the Manhattan Distance heuristic function 
    h(n)= sum of the difference beween tiles in correct position to current position.
    Each tile's location is represented in 2D coordinate plane in the form (row, coloumn), 
    where row and coloumn represent the rows and coloumns of the nxm matrix gameboard."""
    state = n.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]  #gameboard size of size [n,m]

    index_state = {} #represent the list instead of their tile values, but via their index location
    for i in range(len(state)):
        index_state[state[i]] = index[i]    #index_state will return a m-by-n table of the same size of index/gameboard. 
                                            # index_state places the [r,c] position of each tile into the tile-value index of index_state = location in table where [r,c] stored
    mhd = 0
    for i in range(len(state)):
        for j in range(2):  #represents the the 2D coordinate geometry or (r,c) of the table
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
    
    #print("h include 0: ", mhd)
    return mhd


def manh_rmv0Tile(n):
    """disregards the tile 0 as a tile. returns the heuristic value for a given state using the Manhattan Distance heuristic function 
    h(n)= sum of the difference beween tiles in correct position to current position.
    Each tile's location is represented in 2D coordinate plane in the form (row, coloumn), 
    where row and coloumn represent the rows and coloumns of the nxm matrix gameboard."""
    state = n.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]  #gameboard size of size [n,m]

    index_state = {} #represent the list instead of their tile values, but via their index location
    for i in range(len(state)):
        index_state[state[i]] = index[i]    #index_state will return a m-by-n table of the same size of index/gameboard.  index_state places the [r,c] position of each tile of the state into the tile-value index of index_state = location in table where [r,c] stored

    mhd = 0
    for i in range(len(state)):
        if i != 0:
            for j in range(2):  #represents the the 2D coordinate geometry or (r,c) of the table
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        
    #print("h (do not include 0) ", mhd)
    return mhd


def executeEightPuzzleProblemSolution():
    # Create 10 random 8-puzzle instances
    p1 = EightPuzzle(initial=(6, 2, 0, 1, 8, 4, 5, 3, 7))
    p2 = EightPuzzle(initial=(2, 1, 8, 4, 3, 5, 7, 0, 6))
    p3 = EightPuzzle(initial=(1, 2, 8, 7, 5, 3, 6, 4, 0))
    p4 = EightPuzzle(initial=(3, 4, 0, 6, 2, 5, 7, 1, 8))
    p5 = EightPuzzle(initial=(1, 3, 2, 0, 7, 5, 4, 8, 6))
    p6 = EightPuzzle(initial=(7, 6, 1, 8, 5, 2, 3, 4, 0))
    p7 = EightPuzzle(initial=(6, 7, 5, 1, 0, 4, 3, 8, 2))
    p8 = EightPuzzle(initial=(3, 8, 2, 1, 5, 7, 4, 6, 0))
    p9 = EightPuzzle(initial=(8, 6, 0, 5, 7, 3, 1, 2, 4))
    p10 = EightPuzzle(initial=(0, 1, 7, 2, 8, 4, 5, 6, 3))

    ProblemList = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]


    for obj in ProblemList:
        print("Inital State:")
        display(obj.initial, EIGHTPUZZLE=True)

        print("A*-search using the misplaced tile heuristic.")
        algo1(obj)

        print("A*-search using Manhattan distance heuristic.")
        algo2(obj, h1=manh)

        print("A*-search using max{misplaced, Manhattan} heuristic.")
        algo3(obj, h1=manh) #pass manh just in case manhattan is the one that is better than misplaced 

        print("\n")

executeEightPuzzleProblemSolution()

def compareAdmissibilityHeuristicEIGHT():
    p3 = EightPuzzle(initial=(1, 2, 8, 7, 5, 3, 6, 4, 0))
    print("A*-search using Manhattan distance heuristic. EIGHT PUZZLE")
    algo2(obj=p3, h1=manh)
    print("A*-search using Manhattan distance heuristic. 0 is not a Tile. EIGHT PUZZLE")
    algo2(obj=p3, h1=manh_rmv0Tile)

# -----------------------------------------------------------------------------------------------------------------------------

# Question 3: Solving the Duck Puzzle Problem using Search Algo -- Compare Algo - based on:
# Implement a new Problem class called DuckPuzzle that is the same as the 8-puzzle, 
# except the board has this shape (that looks a bit like a duck facing to the left)

def manh_DUCK(n):
    """returns the heuristic value for a given state using the Manhattan Distance heuristic function 
    h(n)= sum of the difference beween tiles in correct position to current position.
    Each tile's location is represented in 2D coordinate plane in the form (row, coloumn), 
    where row and coloumn represent the rows and coloumns of the nxm matrix gameboard. """

    state = n.state
    index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
    index = [[0, 0], [0, 1], [1,0], [1,1], [1, 2], [1,3], [2, 1], [2, 2], [2,3]]  #gameboard size of size [n,m]

    index_state = {} #represent the list instead of their tile values, but via their index location
    for i in range(len(state)):
        index_state[state[i]] = index[i]    #index_state is an m-by-n table of the same size of index/gameboard.  
                                            # index_state places the [r,c] position of each tile  into the tile-value index of index_state = location in table where [r,c] stored

    mhd = 0
    for i in range(len(state)):
        for j in range(2):  #represents the the 2D coordinate geometry or (r,c) of the table
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
    
    #print("h include 0: ", mhd)
    return mhd


def manh_DUCK_rm0Tile(n):
    """disregards tile 0 as a tile. returns the heuristic value for a given state using the Manhattan Distance heuristic function 
    h(n)= sum of the difference beween tiles in correct position to current position.
    Each tile's location is represented in 2D coordinate plane in the form (row, coloumn), 
    where row and coloumn represent the rows and coloumns of the nxm matrix gameboard. """

    state = n.state

    index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
    index = [[0, 0], [0, 1], [1,0], [1,1], [1, 2], [1,3], [2, 1], [2, 2], [2,3]]  #gameboard size of size [n,m]

    index_state = {} #represent the list instead of their tile values, but via their index location
    for i in range(len(state)):
        index_state[state[i]] = index[i]    #index_state is an m-by-n table of the same size of index/gameboard.  
                                            # index_state places the [r,c] position of each tile  into the tile-value index of index_state = location in table where [r,c] stored

    mhd = 0
    for i in range(len(state)):
        if i != 0:
            for j in range(2):  #represents the the 2D coordinate geometry or (r,c) of the table
                    mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
    #print("h dont include 0: ", mhd)
    return mhd




class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x4 board, where one of the
    squares is a blank and 3 are invalid positions. 
    A state is represented as a tuple of length 12, where  element at
    index i represents the tile number  at index i (0 if it's an empty square, and Negative values if an invalid square) """

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

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
        if index_blank_square == 2:
            possible_actions.remove('LEFT')
        if index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square < 2:
            possible_actions.remove('UP')
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions.remove('RIGHT')
        if index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')
        if index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions #returns a set of possible actions


    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state) #returns state.idnex(0) what is the index of the element containging 0
        #if the neightbour is one of the invalid positions of the board, then canot move there - validity of action is done in actions method
        if blank == 0:
            if action == 'UP':
                neighbor = blank 
            if action == 'LEFT':
                neighbor = blank
            if action == 'RIGHT':
                neighbor = blank + 1
            if action == 'DOWN':
                neighbor = blank + 2
        if blank == 1:
            if action == 'UP':
                neighbor = blank
            if action == 'RIGHT':
                neighbor = blank
            if action == 'LEFT':
                neighbor = blank - 1
            if action == 'DOWN':
                neighbor = blank + 2
        if blank == 2:
            if action == 'DOWN':
                neighbor = blank 
            if action == 'LEFT':
                neighbor = blank
            if action == 'UP':
                neighbor = blank - 2
            if action == 'RIGHT':
                neighbor = blank + 1
        if blank == 3:
            if action == 'DOWN': 
                neighbor = blank + 3
            if action == 'LEFT':
                neighbor = blank - 1
            if action == 'UP':
                neighbor = blank - 2
            if action == 'RIGHT':
                neighbor = blank + 1
        if blank == 4:
            if action == 'DOWN': 
                neighbor = blank + 3
            if action == 'LEFT':
                neighbor = blank - 1
            if action == 'UP':
                neighbor = blank
            if action == 'RIGHT':
                neighbor = blank + 1
        if blank == 5:
            if action == 'DOWN': 
                neighbor = blank + 3
            if action == 'LEFT':
                neighbor = blank - 1
            if action == 'UP':
                neighbor = blank
            if action == 'RIGHT':
                neighbor = blank 
        if blank == 6:
            if action == 'DOWN': 
                neighbor = blank
            if action == 'LEFT':
                neighbor = blank
            if action == 'UP':
                neighbor = blank -3
            if action == 'RIGHT':
                neighbor = blank + 1
        if blank == 7:
            if action == 'DOWN': 
                neighbor = blank
            if action == 'LEFT':
                neighbor = blank - 1
            if action == 'UP':
                neighbor = blank - 3
            if action == 'RIGHT':
                neighbor = blank + 1
        if blank == 8:
            if action == 'DOWN': 
                neighbor = blank
            if action == 'LEFT':
                neighbor = blank - 1
            if action == 'UP':
                neighbor = blank - 3
            if action == 'RIGHT':
                neighbor = blank 

        new_state = list(state)
    
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank] #swap with neighbour, ie., this is observed as the tile moving into a blank position

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

#END of DuckPuzzle class. 



def executeDuckProblemSolution():
    #Generate instances - by shuffling from the goalstate. For comparison, used the identical intitial states from EightPuzzle
    d1 = DuckPuzzle(initial=(1, 2, 0, 3, 5, 7, 4, 8, 6))
    d2 = DuckPuzzle(initial=(2, 3, 1, 4, 0, 8, 5, 7, 6))
    d3 = DuckPuzzle(initial=(3, 0, 2, 1, 5, 7, 6, 4, 8))

    d4 = DuckPuzzle(initial=(1, 2, 3, 7, 4, 6, 5, 8, 0))

    d5 = DuckPuzzle(initial=(3, 1, 0, 2, 4, 8, 7, 6, 5))
    d6 = DuckPuzzle(initial=(2, 3, 1, 4, 6, 0, 7, 5, 8))
    d7 = DuckPuzzle(initial=(3, 1, 2, 5, 8, 0, 4, 6, 7))
    d8 = DuckPuzzle(initial=(1, 2, 3, 4, 5, 6, 7, 8, 0))
    d9 = DuckPuzzle(initial=(2, 3, 1, 4, 6, 5, 0, 8, 7))
    d10 = DuckPuzzle(initial=(2, 3, 1, 5, 8, 7, 4, 6, 0))

    DuckProblemList = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10]

    for obj in DuckProblemList:
        print("Inital State:")
        display(obj.initial, EIGHTPUZZLE=False)

        print("A*-search using the misplaced tile heuristic.")
        algo1(obj=obj)

        print("A*-search using Manhattan distance heuristic.")
        algo2(obj=obj, h1=manh_DUCK)

        print("A*-search using max{misplaced, Manhattan} heuristic.")
        algo3(obj=obj, h1=manh_DUCK)

        print("\n")



def compareAdmissibilityHeuristicDuck():
    p3 = DuckPuzzle(initial=(1, 2, 0, 3, 5, 7, 4, 8, 6))
    print("A*-search using Manhattan distance heuristic. 0 is a Tile. DUCKPUZZLE")
    algo2(obj=p3, h1=manh_DUCK)
    print("A*-search using Manhattan distance heuristic. 0 is not a Tile. DUCKPUZZLE")
    algo2(obj=p3, h1=manh_DUCK_rm0Tile)
