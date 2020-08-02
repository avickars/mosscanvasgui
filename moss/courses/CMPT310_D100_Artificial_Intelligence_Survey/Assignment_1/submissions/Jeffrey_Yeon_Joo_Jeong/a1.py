#a1.py

from search import *
from search import random
import time

####---------------------------------------------
#---CODE TAKEN FROM search.py FOR MODIFICATION---
# Check comments for modified lines of code
####---------------------------------------------

class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """
        I forgot how global variables worked in Python so I referred to

        https://stackoverflow.com/questions/423379/using-global-variables-in-a-function

        for guidance
        """

        #increment tiles moved
        global numberOfTilesMoved
        numberOfTilesMoved = c + 1
        return c + 1

    def value(self, state):
        raise NotImplementedError
        
####---------------------------------------------
#---CODE TAKEN FROM search.py FOR MODIFICATION---
# Check comments for modified lines of code
####---------------------------------------------
class EightPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
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
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def check_solvability(self, state):
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        #brute force checking if it's the goal state. takes noticeably longer
        return sum(s != g for (s, g) in zip(node.state, self.goal))

####---------------------------------------------
#---CODE TAKEN FROM search.py FOR MODIFICATION---
# Check comments for modified lines of code
####---------------------------------------------
def astar_search(problem, h=None, display=False):
    """code taken from search.py for modification"""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

#take the max of the misplaced tile and manhattan heuristic
def astar_search_max(problem, h=None, i=None, display=False):
    """code taken from search.py for modification"""
    h = memoize(h or problem.h, 'h')
    i = memoize(i or problem.i, 'i')

    return best_first_graph_search(problem, lambda n: n.path_cost + max(h(n),i(n)), display) 

def best_first_graph_search(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        #increment removed nodes counter
        global frontierRemoved
        frontierRemoved = frontierRemoved + 1
        #tests if the current state is the goal
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            #add the unexplored state to the frontier if it doesn't exist
            #(basically moving tiles and if the state doesn't exist, add it for examination)
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            #if the state is already explored
            elif child in frontier:
                #if the frontier leads to the goal state, delete it and increment the counter
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)

    return None

####--------------------------------------------------
#-- CODE TAKEN FROM test_search.py FOR MODIFICATION---
####--------------------------------------------------

"""IMPORTANT
Referred to 
http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
for more information on Manhattan Heuristics

Also discussed with other students about Manhattan Distance and according to the textbook
0 is omitted from the Manhattan heuristic as it's not a tile, so 0 is removed from the goal dict
"""
def manhattan(node):
    #defines what the goal state is and their indices.
    state = node.state
    index_goal = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    for i in range(len(state)):
        if state[i] != 0:
            index_state[state[i]] = index[i]

    mhd = 0

    #checks the cost for each index. if the current index is at its correct tile there should be no cost
    #need to minimize this by checking if each index is at its correct location
    for i in range(1,9):
        for j in range(2):
            mhd = abs(index_state[i][j] - index_goal[i][j]) + mhd

    return mhd

def manhattan_duckPuzzle(node):
    #defines what the goal state is and their indices.
    state = node.state
    index_goal = {1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3]]

    for i in range(len(state)):
        if i != 2 and i != 3 and i != 8:
            if state[i] != 0:
                index_state[state[i]] = index[i]

    mhd = 0  

    for i in range(1,9):
        for j in range(2):
            mhd = abs(index_state[i][j] - index_goal[i][j]) + mhd

    return mhd

"""
-----------------------------------------------------------------------------
                        ASSIGNMENT 1 IMPLEMENTATIONS
-----------------------------------------------------------------------------
"""
#------------------ IMPORTANT -------------------
# Adopted the same class format as EightPuzzle from aima-python's search.py
#------------------------------------------------

class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, -1, -1, 3, 4, 5, 6, -1, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    #note to self: construct a 4 x 3 square with "forbidden" spots at indices 2,3,8.
    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 4 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 4:
            possible_actions.remove('UP')
        if index_blank_square % 4 == 3:
            possible_actions.remove('RIGHT')
        if index_blank_square > 7:
            possible_actions.remove('DOWN')

        if index_blank_square == 6:
            possible_actions.remove('UP')
        if index_blank_square == 7:
            possible_actions.remove('UP')
        if index_blank_square == 9:
            possible_actions.remove('LEFT')
        if index_blank_square == 1:
            possible_actions.remove('RIGHT')
        if index_blank_square == 4:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    """
    The puzzle is generated via random moves from a solvable state,
    so it is solvable.
    """
    def check_solvability(self, state):
        return True

    def goal_test(self, state):
        return state == self.goal

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

def make_rand_duckPuzzle():
    """
    Used the prof's recommendations to generate solvable puzzle by starting from
    solved state
    """
    #start from solved state
    newPuzzle = (1, 2, -1, -1, 3, 4, 5, 6, -1, 7, 8, 0)

    #randomly shuffle from solved state so the resulting puzzle is still solvable
    for i in range(500):
        action = DuckPuzzle(newPuzzle).actions(newPuzzle)
        randomMove = random.randint(0,len(action)-1)
        newPuzzle = DuckPuzzle(newPuzzle).result(newPuzzle, action[randomMove])

    return newPuzzle
#----------------------End of DuckPuzzle class-------------------------

def check_number_availability(current_array,number):
    #check if the number is available by seeing if the generated number 
    #is already in the tuple and return true if it isn't
    for i in range(len(current_array)):
        if number == current_array[i]:
            #print("%d is in %s",number,current_array) debug
            return False

    return True

def generate_tuple(length=9):
    rand_array = []
    #insert first random number between 0 and 8

    """
        referred to https://www.w3schools.com/python/numpy_random.asp
        for review on random number functions
    """
    number = random.randint(0,8)
    rand_array.append(number)

    #construct the array with unique numbers
    if length == 9:
        while len(rand_array) != length:
            while check_number_availability(rand_array, number) == False:
                number = random.randint(0,8)
            rand_array.append(number)
        rand_tuple = tuple(rand_array[0:9]) #construct tuple from array
    else:
        while len(rand_array) != length:
            while check_number_availability(rand_array, number) == False:
                number = random.randint(0,8)

            if len(rand_array) == 2:
                rand_array.append(-1)
            elif len(rand_array) == 3:
                rand_array.append(-1)
            elif len(rand_array) == 8:
                rand_array.append(-1)
            else:
                rand_array.append(number)
        rand_tuple = tuple(rand_array[0:12])

    return rand_tuple

def display(state, type=None):
    # print 8 puzzle
    if type == EightPuzzle:
        for i in range(3):
            current = state[i]
            if current == 0: 
                print("*", end=" ")
            if current != 0:
                print(current, end=" ")

        print("")

        for i in range(3):
            current = state[i+3]
            if current == 0: 
                print("*", end=" ")
            if current != 0:
                print(current, end=" ")

        print("")

        for i in range(3):
            current = state[i+6]
            if current == 0: 
                print("*", end=" ")
            if current != 0:
                print(current, end=" ")

        print("")

    #print duck puzzle
    if type == DuckPuzzle:
        for i in range(4):
            current = state[i]
            if current == 0: 
                print("*", end=" ")
            if current == -1: 
                print(" ", end=" ")
            if current > 0:
                print(current, end=" ")

        print("")

        for i in range(4):
            current = state[i+4]
            if current == 0: 
                print("*", end=" ")
            if current == -1: 
                print(" ", end=" ")
            if current > 0:
                print(current, end=" ")

        print("")

        for i in range(4):
            current = state[i+8]
            if current == 0: 
                print("*", end=" ")
            if current == -1: 
                print(" ", end=" ")
            if current > 0:
                print(current, end=" ")
        print("")

def make_rand_8puzzle():
    #create new initial tuple
    newPuzzle = generate_tuple(9)

    #check solvability first; if unsolvable create a new tuple
    while EightPuzzle(newPuzzle).check_solvability(newPuzzle) == False:
        newPuzzle = generate_tuple(9)

    return newPuzzle

"""
---------------
---------------
#testing-------
---------------
---------------
"""

#global variables


"""
frontierRemoved = 0
numberOfTilesMoved = 0

numberOfTimesToSolve = 5

print("--------------------- Eight Puzzle --------------------")
for i in range(numberOfTimesToSolve):
    puzzle = make_rand_8puzzle()
    display(puzzle, EightPuzzle)

    #A* misplaced tile heuristic
    print("Misplaced tile heuristic:")
    frontierRemoved = 0
    start_time = time.time()
    astar_search(EightPuzzle(puzzle), h=EightPuzzle(puzzle).h)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s')
    print(f'Length: {numberOfTilesMoved} tiles moved')
    print(f'Total nodes removed from frontier: {frontierRemoved} nodes\n')

    #A* Manhattan heuristic
    print("Manhattan heuristic:")
    frontierRemoved = 0
    start_time = time.time()
    astar_search(EightPuzzle(puzzle), h=manhattan)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s')
    print(f'Length: {numberOfTilesMoved} tiles moved')
    print(f'Total nodes removed from frontier: {frontierRemoved} nodes\n')
    
    #A* max of Misplaced H and Manhattan H
    print("Max of Misplaced Tile vs Manhattan heuristic:")
    frontierRemoved = 0
    start_time = time.time()
    astar_search_max(EightPuzzle(puzzle), h=EightPuzzle(puzzle).h, i=manhattan)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s')
    print(f'Length: {numberOfTilesMoved} tiles moved')
    print(f'Total nodes removed from frontier: {frontierRemoved} nodes\n')

print("--------------------- Duck Puzzle --------------------")
#House/Duck puzzle
for i in range(numberOfTimesToSolve):
    puzzle = make_rand_duckPuzzle()
    display(puzzle, DuckPuzzle)

    #A* misplaced tile heuristic
    print("Misplaced tile heuristic:")
    frontierRemoved = 0
    numberOfTilesMoved = 0
    start_time = time.time()
    astar_search(DuckPuzzle(puzzle), h=DuckPuzzle(puzzle).h)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s')
    print(f'Length: {numberOfTilesMoved} tiles moved')
    print(f'Total nodes removed from frontier: {frontierRemoved} nodes\n')

    #A* Manhattan heuristic
    print("Manhattan heuristic:")
    frontierRemoved = 0
    numberOfTilesMoved = 0
    start_time = time.time()
    astar_search(DuckPuzzle(puzzle), h=manhattan_duckPuzzle)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s')
    print(f'Length: {numberOfTilesMoved} tiles moved')
    print(f'Total nodes removed from frontier: {frontierRemoved} nodes\n')

    #A* max of Misplaced H and Manhattan H
    print("Max of Misplaced Tile vs Manhattan heuristic:")
    frontierRemoved = 0
    numberOfTilesMoved = 0
    start_time = time.time()
    astar_search_max(DuckPuzzle(puzzle), h=DuckPuzzle(puzzle).h, i=manhattan_duckPuzzle)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s')
    print(f'Length: {numberOfTilesMoved} tiles moved')
    print(f'Total nodes removed from frontier: {frontierRemoved} nodes\n')

"""
# --