#a1.py

import random
import time
from search import *
numberOfPuzzle = 10
initState = (1,2,3,4,5,6,7,8,0)
puzzle = []
duckPuzzle = []

#Class of a duck puzzle creates a 9 node puzzle with 2 nodes on top left 4 in the middle and 3 on the bottom right
class DuckPuzzle(Problem):
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

        a1 = (0,2,6)
        a2 = (0,1,4,5)
        a3 = (1,5,8)
        a4 = (2,6,7,8)

        if index_blank_square in a1 :
            possible_actions.remove('LEFT')
        if index_blank_square in a2:
            possible_actions.remove('UP')
        if index_blank_square in a3:
            possible_actions.remove('RIGHT')
        if index_blank_square in a4:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        a1 = (0,1)
        a2 = (2,3,4,5)
        a3 = (6,7,8)


        if blank in a1:
            delta = {'UP': 0, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank in a2:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif blank in a3:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}


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

        return sum(s != g for (s, g) in zip(node.state, self.goal))


# ______________________________________________________________________________

#Makes a random 3x3 puzzle checks if solvable, if not solvable it will retry
def make_rand_8puzzle():
    flag = False
    while flag == False:
        state = random.sample(initState,9)
        puzzle = EightPuzzle(tuple(state))
        flag = puzzle.check_solvability(puzzle.initial)
        if flag == False:
            print("Puzzle Not Solvable Retrying")   
    return puzzle

#Makes a random duck puzzle with 9 spaces. It will only make solvable puzzles since it will only use legal moves from
#the goal state to create the problem state. Idea came from CSSS discord, implemented by me.
def make_rand_duckPuzzle():
    duckPuzzle = DuckPuzzle(tuple(initState))
    state = duckPuzzle.initial
    for i in range (0,100000):
        action = duckPuzzle.actions(state)
        action = action[random.randrange(1,4)%len(action)]
        state = duckPuzzle.result(state,action)
    duckPuzzle.initial = state
    return duckPuzzle

#displays the 3x3 grid puzzle
def display(state):
    count = 0
    for val in state:
        if val == 0:
            val = '*'
        if count != 2:
            print(val, end =' ')
            count += 1
        else:
            print(val, end ='\n')
            count = 0

#displays the duck puzzle
def displayDuck(state):
    count = 0
    for val in state:
        if val == 0:
            val ='*'
        if count == 1:
            print(val, end ='\n')
        elif count == 5:
            print(val, end = '\n  ')
        else:
            print(val, end = ' ')
        count += 1
    print('\n')

#modified astar search method to use custom bestgraphsearch that tracks removed nodes
def astar_search1(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search1(problem, lambda n: n.path_cost + h(n), display)

#modified best first graph search to track the number of popped nodes
def best_first_graph_search1(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    nodesRemoved = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        nodesRemoved += 1
        if problem.goal_test(node.state):
            if display:
                print("Total nodes removed from frontier including goal =", nodesRemoved)
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

#This is for misplaced heuristic but it ignores 0 space hence not using the default
def misplacedHeuristic(node):
    count = 1
    heuristic = 0
    for val in node.state:
        if (val != count) and (val != 0):
            heuristic += 1
        count += 1

    return heuristic

#Calculates the max heuristic value of misplaced and manhattan heuritisics for 3x3 puzzle
def MaxHeuristic(problem):
    count = 1
    heuristic = 0
    for val in problem:
        if (val != count) and (val != 0):
            heuristic += 1
        count += 1
    x = 0
    y = 0
    manSum = 0
    for val in problem:
        if val != 0:
            dy = (y - (int((val-1)/3)))
            dx = (x - (val-1)%3)
            manSum += abs(dx) + abs(dy)
        if x != 2:
            x+= 1
        else:
            x = 0
            y+=1
    if heuristic > manSum:
        return 1
    else:
        return 0

#Calculates the max heuristic value of misplaced and manhattan heuritisics for duck puzzle
def MaxHeuristicDuck(problem):
    count = 1
    heuristic = 0
    for val in problem:
        if (val != count) and (val != 0):
            heuristic += 1
        count += 1
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    a1 = (1,2,3,0)
    a2 = (4,5,6,7,8,0)
    manSum = 0
    for val in problem:
        if val != 0:
            if val in a1:
                dy = (y1-(int((val-1)/2)))
                dx = (x1-((val-1)%2))
                manSum += abs(dx) + abs(dy)
            elif val in a2:
                dy = (y2-(int((val-4)/3)))
                dx = (x2-((val-4)%3))
                manSum += abs(dx) + abs(dy)
        if val in a1:
            if (val == 0) and (y1 == 1) and (x1==1) and (x2==2):
                y2+=1
                x2=0
            elif (val in a1) and (y1 == 1) and (x1==1):
                x2 += 1
            elif(x1==1):
                y1 +=1
                x1 =0
            else:
                x1 +=1
        elif val in a2:
            if (x2== 2):
                y2+= 1
                x2= 0
            else:
                x2+=1
    if heuristic > manSum:
        return 1
    else:
        return 0

#Calculates the heuristic value of manhattan distance for duck puzzle assumes 2x2 puzzle and 2x3 puzzle with a shared middle
def ManhattanSumCalcDuck(node):
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    a1 = (1,2,3,0)
    a2 = (4,5,6,7,8,0)
    manSum = 0
    for val in node.state:
        if val != 0:
            if val in a1:
                dy = (y1-(int((val-1)/2)))
                dx = (x1-((val-1)%2))
                manSum += abs(dx) + abs(dy)
            elif val in a2:
                dy = (y2-(int((val-4)/3)))
                dx = (x2-((val-4)%3))
                manSum += abs(dx) + abs(dy)
        if val in a1:
            if (val == 0) and (y1 == 1) and (x1==1) and (x2==2):
                y2+=1
                x2=0
            elif (val in a1) and (y1 == 1) and (x1==1):
                x2 += 1
            elif(x1==1):
                y1 +=1
                x1 =0
            else:
                x1 +=1
        elif val in a2:
            if (x2== 2):
                y2+= 1
                x2= 0
            else:
                x2+=1
    return manSum

#Calculates the heuristic value of manhattan distance for 3x3 puzzle
def ManhattanSumCalc(node):
    x = 0
    y = 0
    manSum = 0
    for val in node.state:
        if val != 0:
            dy = (y - (int((val-1)/3)))
            dx = (x - (val-1)%3)
            manSum += abs(dx) + abs(dy)
        if x != 2:
            x+= 1
        else:
            x = 0
            y+=1

    return manSum


#Calculates time it takes for a star max to run
#Accepts a puzzle and an optional duck paramater to put it in duck mode
def calculateAStarMax(puzzle, duck = False):
    h = None
    maxH = 0
    print('Maximum Heuristic\n')
    timeStart = time.time()
    if duck == False:
        maxH = MaxHeuristic(puzzle.initial)
        if maxH == 1:
            h = misplacedHeuristic
        else:
            h = ManhattanSumCalc
    else:
        maxH = MaxHeuristicDuck(puzzle.initial)
        if maxH == 1:
            h = misplacedHeuristic
        else:
            h = ManhattanSumCalcDuck

    tilesMoved = astar_search1(puzzle, h,True).solution()
    timeEnd = time.time()
    timeTotal = timeEnd - timeStart
    print('Total Moves =',len(tilesMoved))
    print('Total Time = %.5f Seconds \n' %  timeTotal)

#Calculates time it takes for a star manhattan to run
#Accepts a puzzle and an optional duck paramater to put it in duck mode
def calculateAStarManhattan(puzzle, duck = False):  
    h= ManhattanSumCalc 
    print('Manhattan Distance Heuristic\n')
    if duck == True:
        h = ManhattanSumCalcDuck
    timeStart = time.time()
    tilesMoved = astar_search1(puzzle, h,True).solution()
    timeEnd = time.time()
    timeTotal = timeEnd - timeStart
    print('Total Moves =',len(tilesMoved))
    print('Total Time = %.5f Seconds \n' %  timeTotal)

#Calculates time it takes for a star misplaced to run
#Accepts a puzzle and an optional duck paramater to put it in duck mode       
def calculateAStarMisplaced(puzzle, duck=False): 
    if duck == False:
        print('Puzzle Grids\n')
        display(puzzle.initial)
    else:
        print('Duck Grid\n')
        displayDuck(puzzle.initial)
    print('\nMisplaced Tile Heuristic\n')
    timeStart = time.time()
    tilesMoved = astar_search1(puzzle, misplacedHeuristic,True).solution()
    timeEnd = time.time()
    timeTotal = timeEnd - timeStart
    print('Total Moves =',len(tilesMoved))
    print('Total Time = %.5f Seconds \n' %  timeTotal)


#builds 3x3 and duck puzzles. numberOfPuzzle sets how many will be created
print('Creating', numberOfPuzzle ,'3x3 Eight Puzzle(s) and Nine Space Duck Puzzle(s).')
for i in range (0,numberOfPuzzle):
    puzzle.append(make_rand_8puzzle())
    duckPuzzle.append(make_rand_duckPuzzle())
print('Finished Creating 3x3 Eight Puzzles and Nine Space Duck Puzzle(s).')
#Solves duck puzzles using various algorithms
for duck in duckPuzzle:
    calculateAStarMisplaced(duck, True)
    calculateAStarManhattan(duck, True)
    calculateAStarMax(duck, True)

#Solves 3x3 puzzles using various algorithms
for puz in puzzle:
    calculateAStarMisplaced(puz)
    calculateAStarManhattan(puz)
    calculateAStarMax(puz)

    



