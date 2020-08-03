# Zhong Yu Quan - CMPT 310 Assignment 1
# importing classes from search.py
from search import *
import random
import time

#Modify these variables to change # of times EightPuzzle and DuckPuzzle tests
# are run
eightTestCount = 10
duckTestCount = 10

# Question 1: Helper Functions
def make_rand_8puzzle():
    init = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    random.shuffle(init)
    newPuzzle = EightPuzzle(tuple(init))
    solvable = newPuzzle.check_solvability(init)

    while not solvable:
        random.shuffle(init)
        newPuzzle = EightPuzzle(tuple(init))
        solvable = newPuzzle.check_solvability(init)

    return newPuzzle

def display(state):
    current = list(state)
    currentstr = ['*' if x == 0 else str(x) for x in current]

    #splice list into nested list of 3s
    nested = [currentstr[i:i+3] for i in range(0, len(currentstr), 3)]

    print ('\n'.join(' '.join(map(str, x)) for x in nested))

# Question 2: Comparing Algorithms
#Misplaced tile heuristic function
#Modified to ignore the blank tile in heuristic sum
def misplaced(self, node):
    misplaced = 0
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    current = node.state
    for i in range(len(current)):
        if (current[i] != 0):
            if (current[i] != goal[i]):
                misplaced += 1

    return misplaced

#Manhattan distance heuristic function
#Does not include 0/blank tile in calculating tile distances
def manhattan(self, node):
    state = node.state
    totalDist = 0
    goal_state = {1:[0,0], 2:[1,0], 3:[2,0], 4:[0,1], 5:[1,1], 6:[2,1], 7:[0,2], 8:[1,2], 0:[2,2]}
    arrangement = [[0,0], [1,0], [2,0], [0,1], [1,1], [2,1], [0,2], [1,2], [2,2]]
    current = {}

    #map the values in tuple state to current arrangement
    for i in range(len(state)):
        current[state[i]] = arrangement[i]

    for x in range(1, 9):
        for y in range(2):
            totalDist = totalDist + abs(goal_state[x][y] - current[x][y])

    return totalDist

#Heuristic function to determine max of misplaced tile and manhattan distance
def max_h(self, node):
    a = manhattan(self, node)
    b = misplaced(self, node)

    return max(a, b)

#Assign misplaced tile, manhattan distance and max_h heuristic methods to EightPuzzle
EightPuzzle.misplaced = classmethod(misplaced)
EightPuzzle.manhattan = classmethod(manhattan)
EightPuzzle.max_h = classmethod(max_h)

#Global variable to track removed nodes from frontier
removedCounter = 0

#Search algorithms from search.py
#modified best_first_graph_search to track removed nodes
def best_first_graph_search2(problem, f, display=False):
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
    global removedCounter
    removedCounter = 0
    while frontier:
        node = frontier.pop()
        removedCounter += 1
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

#modified astar_search to use modified best_first_graph_search2
def astar_search2(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search2(problem, lambda n: n.path_cost + h(n), display)

#Functions to print A* search performance with misplaced tile, manhattan distance, and max of both heuristics
def EightPuzzle_Misplaced(EightPuzzle):
    start_time = time.time()
    node = astar_search2(EightPuzzle, EightPuzzle.misplaced)
    elapsed_time = time.time() - start_time
    print("Misplaced tile heuristic test")
    print("Elapsed Time: ", elapsed_time, " seconds")
    print("Length of solution (# tile moves): ", len(node.solution()))
    print("Total number of nodes removed from frontier: ", removedCounter)

def EightPuzzle_Manhattan(EightPuzzle):
    start_time = time.time()
    node = astar_search2(EightPuzzle, EightPuzzle.manhattan)
    elapsed_time = time.time() - start_time
    print("Manhattan distance heuristic test")
    print("Elapsed Time: ", elapsed_time, " seconds")
    print("Length of solution (# tile moves): ", len(node.solution()))
    print("Total number of nodes removed from frontier: ", removedCounter)

def EightPuzzle_Max(EightPuzzle):
    start_time = time.time()
    node = astar_search2(EightPuzzle, EightPuzzle.max_h)
    elapsed_time = time.time() - start_time
    print("Max_h heuristic test")
    print("Elapsed Time: ", elapsed_time, " seconds")
    print("Length of solution (# tile moves): ", len(node.solution()))
    print("Total number of nodes removed from frontier: ", removedCounter)

#Test function to run 3 search types for a random eight puzzle
def EightPuzzleTest():
    test = make_rand_8puzzle()
    display(test.initial)
    print("")
    print("Solvable?", test.check_solvability(test.initial))
    EightPuzzle_Misplaced(test)
    EightPuzzle_Manhattan(test)
    EightPuzzle_Max(test)
    print("")

#run variable number of instances of EightPuzzleTest
for i in range(eightTestCount):
    print("Eight Puzzle Test #", i + 1)
    EightPuzzleTest()
    i += 1

# Question 3: The House-Puzzle
# DuckPuzzle implementation
class DuckPuzzle(Problem):
# +--+--+
# |  |  |
# +--+--+--+--+
# |  |  |  |  |
# +--+--+--+--+
#    |  |  |  |
#    +--+--+--+

    #DuckPuzzle constructor defining goal state and initializing problem
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    #Return index of blank square
    def find_blank_square(self, state):
        return state.index(0)

    #Return legal actions
    def actions(self, state):
        possible = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index = self.find_blank_square(state)

        if index in (0, 1, 4, 5):
            possible.remove('UP')
        if index in (1, 5, 8):
            possible.remove('RIGHT')
        if index in (2, 6, 7, 8):
            possible.remove('DOWN')
        if index in (0, 2, 6):
            possible.remove('LEFT')

        return possible

    #Return result state given an action and an initial state
    #Assume only valid actions occur
    def result(self, state, action):
        index = self.find_blank_square(state)
        result_state = list(state)

        if index < 2:
            delta = {'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif index < 6:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'LEFT': -1, 'RIGHT': 1}

        pair = index + delta[action]
        result_state[index], result_state[pair] = result_state[pair], result_state[index]

        return tuple(result_state)

    #Return if state is goal state for problem
    def goal_test(self,state):
        return state == self.goal

    #Misplaced tile heuristic
    #Uses 0 as a misplacable tile
    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

    #Modified misplaced tile heuristic
    #Does not include the blank tile in heuristic for admissibility
    def misplaced(self, node):
        misplaced = 0
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        current = node.state
        for i in range(len(current)):
            if (current[i] != 0):
                if (current[i] != goal[i]):
                    misplaced += 1

        return misplaced

    #Manhattan distance heuristic
    #Does not include the blank tile in heuristic for admissibility
    def manhattan(self, node):
        state = node.state
        totalDist = 0
        goal_state = {1: [0, 0], 2: [1, 0], 3: [0, 1], 4: [1, 1], 5: [2, 1], 6: [3, 1], 7: [1, 2], 8: [2, 2], 0: [3, 2]}
        arrangement = [[0, 0], [1, 0], [0, 1], [1, 1], [2, 1], [3, 1], [1, 2], [2, 2], [3, 2]]
        current = {}

        #map the values in tuple state to current arrangement
        for i in range(len(state)):
            current[state[i]] = arrangement[i]

        for x in range(1, 9):
            for y in range(2):
                totalDist = totalDist + abs(goal_state[x][y] - current[x][y])

        return totalDist

    #Max heuristic between manhattan distance and misplaced tile
    def max_h(self, node):
        a = misplaced(self, node)
        b = manhattan(self, node)

        return max(a, b)

# Helper functions for Duck Puzzle
def make_rand_duckpuzzle():
    shuffleState = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    newPuzzle = DuckPuzzle(tuple(shuffleState))
    for i in range(200):
        move = random.choice(newPuzzle.actions(shuffleState))
        tempState = newPuzzle.result(shuffleState, move)
        shuffleState = tempState
        i += 1
    newPuzzle = DuckPuzzle(shuffleState)
    return newPuzzle

def display_duckpuzzle(state):
    current = list(state)
    currentstr = ['*' if x == 0 else str(x) for x in current]
    print (currentstr[0], " ", currentstr[1])
    print (currentstr[2], " ", currentstr[3], " ", currentstr[4], " ", currentstr[5])
    print ("   ", currentstr[6], " ", currentstr[7], " ", currentstr[8])

#Functions to print A* search performance with misplaced tile, manhattan distance, and max of both heuristics
def DuckPuzzle_Misplaced(DuckPuzzle):
    start_time = time.time()
    node = astar_search2(DuckPuzzle, DuckPuzzle.misplaced)
    elapsed_time = time.time() - start_time
    print("Misplaced tile heuristic test")
    print("Elapsed Time: ", elapsed_time, " seconds")
    print("Length of solution (# tile moves): ", len(node.solution()))
    print("Total number of nodes removed from frontier: ", removedCounter)

def DuckPuzzle_Manhattan(DuckPuzzle):
    start_time = time.time()
    node = astar_search2(DuckPuzzle, DuckPuzzle.manhattan)
    elapsed_time = time.time() - start_time
    print("Manhattan distance heuristic test")
    print("Elapsed Time: ", elapsed_time, " seconds")
    print("Length of solution (# tile moves): ", len(node.solution()))
    print("Total number of nodes removed from frontier: ", removedCounter)

def DuckPuzzle_Max(DuckPuzzle):
    start_time = time.time()
    node = astar_search2(DuckPuzzle, DuckPuzzle.max_h)
    elapsed_time = time.time() - start_time
    print("Max_h heuristic test")
    print("Elapsed Time: ", elapsed_time, " seconds")
    print("Length of solution (# tile moves): ", len(node.solution()))
    print("Total number of nodes removed from frontier: ", removedCounter)

#Test function to run 3 search types for a random duck puzzle
def DuckPuzzleTest():
    test = make_rand_duckpuzzle()
    display_duckpuzzle(test.initial)
    print("")
    DuckPuzzle_Misplaced(test)
    DuckPuzzle_Manhattan(test)
    DuckPuzzle_Max(test)
    print("")

#run variable number of instances of DuckPuzzleTest
for i in range(duckTestCount):
    print("Duck Puzzle Test #", i + 1)
    DuckPuzzleTest()
    i += 1