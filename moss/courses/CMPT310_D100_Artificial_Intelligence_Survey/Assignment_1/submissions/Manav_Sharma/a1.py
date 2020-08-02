# a1.py
import time
from search import *
from random import randint
import array as arr


delete_nodes = 0;                # The global variables
frontier_count = 0;
test_nodes = 1;

# _____________________________________________________________________________________________________________
# Q 1

# Making of random instances
def make_rand_8puzzle():

    import random
    State = [0, 1, 2, 3, 4, 5, 6, 7, 8]          # Intial solvable state
    check_solv = False                           # Checker for solavability
    temp_random =0;
    while (check_solv == False):

        random.shuffle(State);                   # random shuffle the states
        EightPuzzle1 = EightPuzzle(tuple(State)) # random tuple state puzzle
        check_solv = EightPuzzle(tuple(State)).check_solvability(tuple(State))  # solvability check

        if (check_solv == True):
            return EightPuzzle1                  # solvable eight puzzle

    return

# This function Creates an array of 10 random
def test_puzzle_create():

    array_puzzle = []
    for i in range(0, 10):
        array_puzzle.append(make_rand_8puzzle())
    return array_puzzle

# This function display the Eight Puzzle problem
def display(state):
    count_i = 0
    for count_i in range(0,9):
        if (state[count_i] == 0):               # '0' is the blank
            print("*", " ", end="")
        else:
            print(state[count_i], " ", end="")
        if ((count_i + 1) % 3 == 0):
            print()
    print()

    return

# _____________________________________________________________________________________________________________
# Q 2: Comparing Algorithms


def manahattan_max(node):            # max of misplaced tile, manhattan distance
    puzzle =  EightPuzzle(node.state)
    return max(manhattan(node) , puzzle.h(node))

def misplacedTiles(node):           # Count no. of misplaced tiles for eight puzzle

    ResultState = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return sum(s != g for (s, g) in zip(node.state, ResultState))

def check_testRunning():
    eight_puzzle = make_rand_8puzzle()
    manhhatan_star = eight_puzzle
    max_temp = eight_puzzle

    display(eight_puzzle.initial)
    start_time = time.time()
    result_astar, total_pop = astar_search(eight_puzzle)
    elapsed_time = time.time() - start_time


def manhattanDistance(node):                    # Manhattan Distance
    state_user = node.state
    goalState = {1: [0, 2], 2: [1, 2], 3: [2, 2], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 0], 8: [1, 0], 0: [2, 0]}
    currentState = {}
    indices = [[0, 2], [1, 2], [2, 2], [0, 1], [1, 1], [2, 1], [0, 0], [1, 0], [2, 0]]
    Temp_dist=1
    for i in range(len(state_user)):
        currentState[state_user[i]] = indices[i]
    manhattanDistance = 0
    for i in range(1, 9):
        for j in range(2):
            manhattanDistance = abs(goalState[i][j] - currentState[i][j]) + manhattanDistance
    return manhattanDistance


# This instance for a node make the max of Misplaced Tiles, Manhattan Distance
def misplaced_manhatten_max(node):

    temp = max(misplacedTiles(node), manhattanDistance(node))
    return temp


# Using A* for computing required values
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return BestGraphSearch_test(problem, lambda n: n.path_cost + h(n), display)

# Test Function for making Max of manhatten and mispalaced
def test_max_both(self, node):

    manhattan_h_test = self.manhattan(node)
    misplaced_h_test = self.h(node)
    return max(manhattan_h_test , misplaced_h_test)

# This Function modifies and test the BGS
def BestGraphSearch_test(problem, f, display=False):
    global delete_nodes
    delete_nodes = 0
    temp_nodes =0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        delete_nodes += 1
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


# This Function used different algorithyms to solve random instance
def comparingAlgorithmsEightPuzzle():

    Track_couneter = 15;
    count_puzzle = 10;
    array_puzzle = []

    for i in range(0, count_puzzle):
        array_puzzle.append(make_rand_8puzzle())

    # Array for track of time
    asearch_misplaced_time = []
    asearch_manhatten_time = []
    asearch_max_time = []
    global delete_nodes

    print("The Outcomes from running the MISPLACED TILES HEURISTIC are:")
    for i in range(0, count_puzzle):
        IntialTime = time.time()
        Result = astar_search(array_puzzle[i], h=misplacedTiles).solution()
        FinalTime = time.time()
        asearch_misplaced_time.append(FinalTime - IntialTime)
        print()
        print("Current Initial Puzzle State is: ", array_puzzle[i].initial)
        print("Current Puzzle Goal State is: ", array_puzzle[i].goal)
        print("Current Puzzle Solution is:", Result)
        print(i, ".\tTime Taken: ", asearch_misplaced_time[i])
        print("\tLength of the Solution:", len(Result))
        print("\tNumber of nodes removed from the frontier:", delete_nodes)
        print()

 #______________________________________________________________________________________________________________________

    print("The outcomes from running the MANHATTAN DISTANCE HEURISTIC are :")
    for i in range(0, count_puzzle):
        IntialTime = time.time()
        Result = astar_search(array_puzzle[i], h=manhattanDistance).solution()
        FinalTime = time.time()
        asearch_manhatten_time.append(FinalTime - IntialTime)
        print()
        print("Current Initial Puzzle State is: ", array_puzzle[i].initial)
        print("Current Puzzle Goal State is: ", array_puzzle[i].goal)
        print("Current Puzzle Solution is:", Result)
        print(i, ".\tTime Taken: ", asearch_manhatten_time[i])
        print("\tLength of the Solution:", len(Result))
        print("\tNumber of nodes removed from the frontier:", delete_nodes)
        print()

#________________________________________________________________________________________________________________________

    print("The outcomes of running the max(MISPLACED TILES HEURISTIC, MANHATTAN DISTANCE HEURISTIC):")
    for i in range(0, count_puzzle):
        IntialTime = time.time()
        Result = astar_search(array_puzzle[i], h=misplaced_manhatten_max).solution()
        FinalTime = time.time()
        asearch_max_time.append(FinalTime - IntialTime)
        print()
        print("Current Initial Puzzle State is: ", array_puzzle[i].initial)
        print("Current Puzzle Goal State is: ", array_puzzle[i].goal)
        print("Current Puzzle Solution is:", Result)
        print(i, ".\tTime Taken: ", asearch_max_time[i])
        print("\tLength of the Solution:", len(Result))
        print("\tNumber of nodes removed from the frontier:", delete_nodes)
        print()

    return

# _____________________________________________________________________________________________________________
# Q 3

# Declaring a Duck Puzzle class which inherits from the Problem class
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a house shaped board, where one of the
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
        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')

        if index_blank_square == 1:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')

        if index_blank_square == 2:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')

        if index_blank_square == 4:
            possible_actions.remove('UP')

        if index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')

        if index_blank_square == 6:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')

        if index_blank_square == 7:
            possible_actions.remove('DOWN')

        if index_blank_square == 8:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
        if blank == 0:
            delta = {'DOWN': 2, 'RIGHT': 1}
        if blank == 1:
            delta = {'DOWN': 2, 'LEFT': -1}
        if blank == 2:
            delta = {'UP': -2, 'RIGHT': 1}
        if blank == 3:
            delta = {'DOWN': 3, 'UP': -2, 'LEFT': -1, 'RIGHT': 1}
        if blank == 4:
            delta = {'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank == 5:
            delta = {'LEFT': -1, 'DOWN': 3}
        if blank == 6:
            delta = {'UP': -3, 'RIGHT': 1}
        if blank == 7:
            delta = {'UP': -3, 'LEFT': -1, 'RIGHT': 1}
        if blank == 8:
            delta = {'UP': -3, 'LEFT': -1}

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

# This Function generates the heuristic for h(n)
def Tiles_misplaced_PuzzleDuck(node):
    goalState = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return sum(s != g for (s, g) in zip(node.state, goalState))

# This Function generates the Manhattan distance from the node
def Distance_manhattan_PuzzleDuck(node):
    inputState = node.state
    goalState = {1: [1, 2], 2: [0, 1], 3: [1, 1], 4: [2, 1], 5: [3, 1], 6: [0, 0], 7: [1, 0], 8: [2, 0], 0: [3, 0]}
    currentState = {}
    indices = [[1, 2], [0, 1], [1, 1], [2, 1], [3, 1], [0, 0], [1, 0], [2, 0], [3, 0]]
    for i in range(len(inputState)):
        currentState[inputState[i]] = indices[i]
    manhattanDistance = 0
    for i in range(1, 9):
        for j in range(2):
            manhattanDistance = abs(goalState[i][j] - currentState[i][j]) + manhattanDistance
    return manhattanDistance

# This Function used for testing thr random array geneartion of duck puzzle
def temp_rand_testDuck():
    import random

    state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(state)

    Eight_D_obj = DPuzzle(tuple(state))
    while (Eight_D_obj.check_solvability(state) == False):
        random.shuffle(state)

        Eight_D_obj = DPuzzle(tuple(state))

    return Eight_D_obj

#  This Function make the max of both algorithyms
def Max_DuckPuzzle(node):

    return max(Tiles_misplaced_PuzzleDuck(node), Distance_manhattan_PuzzleDuck(node))


# A function that generates random instances of the House Puzzle problem
def make_rand_DuckPuzzle():
    puzzle = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0));
    currentNode = Node(puzzle.initial)
    for i in range(1000):
        possibleMoves = puzzle.actions(currentNode.state)
        selectedMove = randint(0, len(possibleMoves) - 1)
        currentNode.state = puzzle.result(currentNode.state, possibleMoves[selectedMove])
    finalPuzzle = DuckPuzzle(currentNode.state)
    return finalPuzzle


# A function that prints the House Puzzle problem initial state
def display_DuckPuzzle(state):
    print()
    print('   ', state[0])
    print(state[1], ' ', state[2], ' ', state[3], ' ', state[4])
    print(state[5], ' ', state[6], ' ', state[7], ' ', state[8])
    print()
    return


# A function to create random instances of House Puzzle and using diffrent heuristics to solve them
def comparingAlgorithmsDuckPuzzle():

    count_puzzle1 = 10;
    arrayPuzzle = []
    count_puzzle2 = 15;
    count_puzzle3 = 9;

    for i in range(0, count_puzzle1):                       # Array with random instance
        arrayPuzzle.append(make_rand_DuckPuzzle())

    asearch_misplacestile_time = []
    asearch_manhattendist_time = []
    asearch_max_timetak = []

    global delete_nodes
    print("The outcomes from running the MISPLACED TILES HEURISTIC are :")
    for i in range(0, count_puzzle1):
        temp1_max=0;
        intial_time = time.time()
        solution = astar_search(arrayPuzzle[i], h=Tiles_misplaced_PuzzleDuck).solution()
        final_time = time.time()
        asearch_misplacestile_time.append(final_time - intial_time)
        print()
        print("Current Initial Puzzle State is: ", arrayPuzzle[i].initial)
        print("Current Puzzle Goal State is: ", arrayPuzzle[i].goal)
        print("Current Puzzle Solution is:", solution)
        print(i, ".\tTime Taken: ", asearch_misplacestile_time[i])
        print("\tLength of the Solution:", len(solution))
        print("\tNumber of nodes removed from the frontier:", delete_nodes)
        print()

# ---------------------------------------------------------------------------------------------------------------------

    print("The outcomes from running the MANHATTAN DISTANCE HEURISTIC:")
    for i in range(0, count_puzzle1):
        temp2_max=0;
        intial_time = time.time()
        solution = astar_search(arrayPuzzle[i], h=Distance_manhattan_PuzzleDuck).solution()
        final_time = time.time()
        asearch_manhattendist_time.append(final_time - intial_time)
        print()
        print("Current Initial Puzzle State is: ", arrayPuzzle[i].initial)
        print("Current Puzzle Goal State is: ", arrayPuzzle[i].goal)
        print("Current Puzzle Solution is:", solution)
        print(i, ".\tTime Taken: ", asearch_manhattendist_time[i])
        print("\tLength of the Solution:", len(solution))
        print("\tNumber of nodes removed from the frontier:", delete_nodes)
        print()
#-----------------------------------------------------------------------------------------------------------------------

    print( "The outcomes from running the max(MISPLACED TILES HEURISTIC, MANHATTAN DISTANCE HEURISTIC) are :")
    for i in range(0, count_puzzle1):
        temp3_max=0;
        intial_time = time.time()
        solution = astar_search(arrayPuzzle[i], h=Max_DuckPuzzle).solution()
        final_time = time.time()
        asearch_max_timetak.append(final_time - intial_time)
        print()
        print("Current Initial Puzzle State is: ", arrayPuzzle[i].initial)
        print("Current Puzzle Goal State is: ", arrayPuzzle[i].goal)
        print("Current Puzzle Solution is:", solution)
        print(i, ".\tTime Taken: ", asearch_max_timetak[i])
        print("\tLength of the Solution:", len(solution))
        print("\tNumber of nodes removed from the frontier:", delete_nodes)
        print()

    return


def runProgram():
    comparingAlgorithmsEightPuzzle()
    comparingAlgorithmsDuckPuzzle()
    return


runProgram()