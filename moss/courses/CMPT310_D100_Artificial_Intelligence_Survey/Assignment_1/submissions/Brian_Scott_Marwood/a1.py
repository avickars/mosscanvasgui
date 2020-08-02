# a1.py
#Brian Marwood
from search import *
from datetime import datetime, timedelta 
import os

###      Helper functions
def printTimedAlgo(puzzle, methodType):
    start_time = datetime.now()
    mod_astar_search(puzzle, methodType)
    timeTaken = (datetime.now() - start_time).total_seconds()
    print("*** %s seconds ***" % timeTaken + "\n")

# random.shuffle from https://docs.python.org/3/library/random.html#random.shuffle
def make_rand_8puzzle():
    myStates = [0, 3, 2, 1, 8, 7, 4, 6, 5]
    solvable = False
    currState = None
    eightPzl = None 
    while not solvable:
        random.shuffle(myStates)
        currState = tuple(myStates)
        eightPzl = EightPuzzle(currState)
        solvable = eightPzl.check_solvability(currState)
    
    return eightPzl
        
#  how to print on same line from https://www.geeksforgeeks.org/print-without-newline-python/
def display8Pzl(self, state):
    maxLine = 3
    for var in state:
        if maxLine <= 0 :
            maxLine = 3
            print()

        if var == 0 :
            print("*", end = ' ')
        else :
            print(var, end = ' ')
        maxLine-=1

    print()

#######         Algorithms          #######

#based of the theory from https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
def manhattan_distance(self, node):
    firstRun = True
    score = 0
    MovementCost = 1 #always 1 b/c using the simple case
    for curTile in node.state:
        goalTile = self.goal[self.goal.index(curTile)] #finds the current Tile within the goalTile
        x1 = node.state.index(curTile)
        x2 = self.goal.index(curTile)
        y1 = node.state.index(goalTile)
        y2 = self.goal.index(goalTile)

        dx = abs(x1 - x2)       #coordinate index's
        dy = abs(y1 - y2)
        heuristicDistance = dx + dy
        score += MovementCost * heuristicDistance
    return score
    
def max_heuristic(self, node):
    return max(self.h(node), manhattan_distance(self, node))


def mod_astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return mod_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

#from search.py and modified to show path cost and removed notes
#Thanks to Sukhdeep Parmar for explaining how to think about getting Tiles moved/Removed and how it applied
#specifically to the manhattan search algo
def mod_best_first_graph_search(problem, f, display=False):
    nodesRemoved = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")

            #print the other required info prior to returning the finished puzzle
            print("Tiles moved: " + str(node.path_cost))
            print("Nodes Removed: " + str(nodesRemoved))
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            # print(node)
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    nodesRemoved += 1
                    frontier.append(child)

    return None


############            Run CompareAlgo to Compare 10 different 8puzzles                ############
def compare8PzlAlgo():
    i = 0
    while i < 10:
        puzzle = make_rand_8puzzle()
        display8Pzl(puzzle, puzzle.initial)
        start_time = datetime.now()
        print("Running Misplaced Tile Heuristic")
        printTimedAlgo(puzzle, puzzle.h)
        print("Running Manhattan Heuristic")
        printTimedAlgo(puzzle,lambda n: manhattan_distance(puzzle, n) )
        print("Running Max Heuristic")
        printTimedAlgo(puzzle, lambda n: max_heuristic(puzzle, n))
        i +=1
    return None


####################################     Duck Puzzle      ####################################

#based off of EightPuzzle from search.py
class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    #actions are modified here to fit within the scope of the duck puzzle rather then a classic 3x3
    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        #remove the actions that are not permitted per index
        if index_blank_square < 2: #line 1
            possible_actions.remove('UP')
            if index_blank_square == 0:
                possible_actions.remove('LEFT')
            else:
                possible_actions.remove('RIGHT')
        elif index_blank_square < 6: #line 2
            if (index_blank_square == 2):
                possible_actions.remove('LEFT')
                possible_actions.remove('DOWN')
            if (index_blank_square >= 4):
                possible_actions.remove('UP')
            if (index_blank_square == 5):
                possible_actions.remove('RIGHT')
        else: #line 3
            possible_actions.remove('DOWN')
            if index_blank_square == 6:
                possible_actions.remove('LEFT')
            if index_blank_square == 8:
                possible_actions.remove('RIGHT')
        return possible_actions

    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)
        up = 0
        down = 0
        #change which row your in to determine the differences in up/down in the lines
        if blank < 2: #line 1
            down = 2
        elif blank < 6: #line 2
            up = -2
            down = 3
        else: #line 3
           up = -3

        delta = {'UP': up, 'DOWN': down, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))


def displayduckPzl(self, state):
    lines = [2,4,3]
    lineRunner = 0
    lineIndexer = 0
    for var in state:
        if  lineRunner >= lines[lineIndexer] :
            if(lineIndexer <= len(lines)):
                lineIndexer += 1;
            lineRunner = 0
            print()
            if(lineIndexer == 2):
                print(" ", end = ' ')

        if var == 0 :
            print("*", end = ' ')
        else :
            print(var, end = ' ')
        lineRunner+=1

    print()

def make_rand_duckPuzzle():
    myStates = [0, 3,
                2, 1, 8, 7,
                   4, 6, 5]
    duckPuzzle = None 
    duckPuzzle = DuckPuzzle(tuple(myStates))

    #as stated in the assignment checking solvibility is not an option, therefore we back shuffle it 
    #as a human would
    return shuffle_duck(duckPuzzle)

#shuffles the board anywhere from 1-1000 times to get a modified but solvable board
def shuffle_duck(duckPuzzle):

    shuffles = random.randint(1, 100000) 
    newState = duckPuzzle.initial
    for shuffle in range(shuffles):
        actions = duckPuzzle.actions(newState) #get the actions for the current state
        random.shuffle(actions) #shuffle the actions and use the first one 
        newState = duckPuzzle.result(newState, actions[0])    
    return DuckPuzzle(newState)

def compareDuckPzlAlgo():
    i = 0
    while i < 10:
        puzzle = make_rand_duckPuzzle()
        displayduckPzl(puzzle, puzzle.initial)
        start_time = datetime.now()
        print("Running Misplaced Tile Heuristic")
        printTimedAlgo(puzzle, puzzle.h)
        print("Running Manhattan Heuristic")
        printTimedAlgo(puzzle,lambda n: manhattan_distance(puzzle, n) )
        print("Running Max Heuristic")
        printTimedAlgo(puzzle, lambda n: max_heuristic(puzzle, n))
        i +=1
    return None

"""
THIS IS WHERE YOU CAN CHOOSE TO RUN EITHER PUZZLE/BOTH
"""
compare8PzlAlgo()
compareDuckPzlAlgo()