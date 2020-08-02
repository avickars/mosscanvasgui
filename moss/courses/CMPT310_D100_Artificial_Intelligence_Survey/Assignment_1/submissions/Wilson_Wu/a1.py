# a1.py
# WILSON WU
# 301350197
# CMPT 310 ASSIGNMENT #1

from search import Problem
from search import Graph
from search import SimpleProblemSolvingAgentProgram
#from search import astar_search
from search import Node
import time
import random
from utils import *

#

#FUNCTIONS MODIFIED FROM A1.PY

def best_first_graph_search(problem, f, display=False):
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
    counter = 0
    pathLength = 0
    while frontier:
        node = frontier.pop()
        counter = counter + 1
        #print(node.state)
        if problem.goal_test(node.state):
            if display:
                print("Paths expanded: ",len(explored))
                print("Paths remaining in Frontier: ",len(frontier))
                print("Number of nodes removed from Frontier: " ,counter)
                for x in node.path():
                    pathLength = pathLength + 1
                print("The number of tiles moved: ",pathLength-1)
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

def astar_search_new(problem, h=None, display=True):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
   
   
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


class DuckPuzzle(Problem):
    tile0=[0,0,0,0,0,0,0,0,0]
    #tile0=[4,3,2,3,2,1,2,1,0]
    tile1=[0,1,2,1,2,3,2,3,4]
    tile2=[1,0,1,2,1,2,3,2,3]
    tile3=[2,1,0,3,2,1,4,3,2]
    tile4=[1,2,3,0,1,2,1,2,3]
    tile5=[2,1,2,1,0,1,2,1,2]
    tile6=[3,2,1,2,1,0,3,2,1]
    tile7=[2,3,4,1,2,3,0,1,2]
    tile8=[3,2,3,2,1,2,1,0,1]
        
    tiles = [tile0, tile1,tile2,tile3,tile4,tile5,tile6,tile7,tile8]
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    #*(HELPER FUNCTION)*
    def make_rand_duck_puzzle():
        list = [1,2,3,4,5,6,7,8,0]
        newPuzzle = DuckPuzzle(list)
        newNum = random.randint(50,100)
        
        for i in range(0, newNum):
            possibleActions = newPuzzle.actions(list)
            randomAction = random.randint(0,len(possibleActions)-1)
            list = newPuzzle.result(list,possibleActions[randomAction])
            newPuzzle = DuckPuzzle(list)
        list1 = list
        list2 = list
        newPuzzle = DuckPuzzle(list)
        newPuzzle1 = DuckPuzzle(list1)
        newPuzzle2 = DuckPuzzle(list2)
        print("---------------------------------------------------------------")
        duckDisplay(list)
        print("New Solvable Duck Puzzle Created.",newNum," shuffles were used")
        manhattanDuck(list,newPuzzle)
        misplacedDuck(list1, newPuzzle1)
        maxDuck(list2,newPuzzle2)
        print("---------------------------------------------------------------")


    def hardCodedDuck():

        #newPuzzleList = (2,3,1,7,0,8,6,4,5)
        newPuzzleList= (1, 2, 3, 5, 6, 0, 4, 7, 8)
        newPuzzle = DuckPuzzle(newPuzzleList)
        duckDisplay(newPuzzleList)
        manhattan(newPuzzleList,newPuzzle)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self,state):
        actions = []
        index_blank_square = self.find_blank_square(state)
        if  index_blank_square == 0:
            actions = ('RIGHT','DOWN')
        elif  index_blank_square == 1:
            actions=('DOWN','LEFT')
        elif index_blank_square == 2:
             actions=('UP','RIGHT')
        elif index_blank_square == 3:
            actions=('UP','DOWN','LEFT','RIGHT')
        elif index_blank_square == 4:
            actions=('DOWN','LEFT','RIGHT')
        elif index_blank_square == 5:
            actions=('DOWN','LEFT')
        elif  index_blank_square == 6:
            actions=('UP','RIGHT')
        elif index_blank_square == 7:
            actions=('UP','RIGHT','LEFT')
        elif  index_blank_square == 8:
            actions=('UP','LEFT')
        return actions

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        if blank == 0:
            delta = {'UP': 0, 'DOWN': +2, 'LEFT': 0, 'RIGHT': 1}
        elif blank == 1:
            delta = {'UP': 0, 'DOWN': +2, 'LEFT': -1, 'RIGHT': 0}
        elif blank == 2:
            delta = {'UP': -2, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 3:
            delta = {'UP': -2, 'DOWN': +3, 'LEFT': -1, 'RIGHT': 1} 
        elif blank == 4:
            delta = {'UP': 0, 'DOWN': +3, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 5:
            delta = {'UP': 0, 'DOWN': +3, 'LEFT': -1, 'RIGHT': 0}
        elif blank ==6:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}
        elif blank ==7:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
        elif blank ==8:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 0}
        neighbor = blank + delta[action]

        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        #duckDisplay(new_state)
        return tuple(new_state)



#HEURISTIC FUNCTIONS FOR DUCK
    
    #MISPLACED
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))
    
    #MANHATTAN
    def h1(self, node):
        sum = 0
        counter = 0
        for x in node.state:
            sum = sum + DuckPuzzle.tiles[x][counter]
            counter=counter+1
        return sum
    
    #MAX
    def h2(self,node):
        misplaced = sum(s != g for (s, g) in zip(node.state, self.goal))
        counter = 0
        manhat = 0
        for x in node.state:
            manhat = manhat + EightPuzzle.tiles[x][counter]
            counter=counter+1
        if manhat>misplaced:
            return manhat
        else:
            return misplaced

       

class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """
    tile0 = [0,0,0,0,0,0,0,0,0]
    #tile0=[4,3,2,3,2,1,2,1,0]
    tile1=[0,1,2,1,2,3,2,3,4]
    tile2=[1,0,1,2,1,2,3,2,3]
    tile3=[2,1,0,3,2,1,4,3,2]
    tile4=[1,2,3,0,1,2,1,2,3]
    tile5=[2,1,2,1,0,1,2,1,2]
    tile6=[3,2,1,2,1,0,3,2,1]
    tile7=[2,3,4,1,2,3,0,1,2]
    tile8=[3,2,3,2,1,2,1,0,1]
        
    tiles = [tile0, tile1,tile2,tile3,tile4,tile5,tile6,tile7,tile8]
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

    #HEURISTIC FUNCTIONS FOR 8PUZZLE

    #MISPLACED
    def h1(self, node):

        sum = 0
        counter = 0
        for x in node.state:
            sum = sum + EightPuzzle.tiles[x][counter]
            counter=counter+1
        return sum

    #MANHATTAN
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        sum = 0
        for (s,g) in zip(node.state, self.goal):
            if(s!=g or s!=0):
                 sum = sum + 1

        return sum

    #MAX
    def h2(self,node):
        misplaced = sum(s != g for (s, g) in zip(node.state, self.goal))
        counter = 0
        manhat = 0
        for x in node.state:
            manhat = manhat + EightPuzzle.tiles[x][counter]
            counter=counter+1
        if manhat>misplaced:
            return manhat
        else:
            return misplaced







#DISPLAY FUNCTIONS *(HELPER FUNCTION)*

def display(puzzleTuple):
    state = list(puzzleTuple)
    for x in state:
        if state[x]==0:
            state[x] = '*'
            break
    print(state[0], state[1], state[2])
    print(state[3], state[4], state[5])
    print(state[6], state[7], state[8])
    print('\n')

def duckDisplay(puzzleTuple):
    state = list(puzzleTuple)
    for x in state:
        if state[x]==0:
            state[x] = '*'
            break
    print(state[0], state[1])
    print(state[2], state[3], state[4],state[5])
    print(' ',state[6], state[7], state[8])
    print('\n')

#CREATING 8 PUZZLE

# *(HELPER FUNCTION)*
def shuffle_8puzzle():
        list = [1,2,3,4,5,6,7,8,0]
        newPuzzle = EightPuzzle(list)
        newNum = random.randint(25,50)
        
        for i in range(0, newNum):
            possibleActions = newPuzzle.actions(list)
            randomAction = random.randint(0,len(possibleActions)-1)
            list = newPuzzle.result(list,possibleActions[randomAction])
            newPuzzle = EightPuzzle(list)
        list1 = list
        list2 = list
        newPuzzle = EightPuzzle(list)
        newPuzzle1 = EightPuzzle(list1)
        newPuzzle2 = EightPuzzle(list2)
        print("---------------------------------------------------------------")
        display(list)
        
        print("New Solvable Eight Puzzle Created.",newNum," shuffles were used")
        manhattan(list,newPuzzle)
        misplaced(list1, newPuzzle1)
        max(list2,newPuzzle2)   
        print("---------------------------------------------------------------")

# This function is not used. It is orignally used with fully-random created puzzles but those take too long to solve.
def createPuzzleSolvable():
    newPuzzleList = make_rand_8puzzle()
    newPuzzleList1 = newPuzzleList
    newPuzzle = EightPuzzle(newPuzzleList) 
    newPuzzle1 = EightPuzzle(newPuzzleList) 
    newPuzzle2 = EightPuzzle(newPuzzleList) 
    while newPuzzle.check_solvability(newPuzzleList)==False:
        newPuzzleList = make_rand_8puzzle()
        newPuzzle = EightPuzzle(newPuzzleList)
        newPuzzle1 = EightPuzzle(newPuzzleList)
        newPuzzle2 = EightPuzzle(newPuzzleList) 
    newPuzzleList1 = newPuzzleList
    newPuzzleList2 = newPuzzleList
    print("SOLVABLE: ",newPuzzle.check_solvability(newPuzzleList))
    display(newPuzzleList)
    manhattan(newPuzzleList1, newPuzzle1)
    misplaced(newPuzzleList, newPuzzle)
    max(newPuzzleList2,newPuzzle2)

# This function is not used. It creates a randomized 8 puzzle.
def make_rand_8puzzle():
    list = []
    newNum = random.randint(0,8)
    while len(list) < 9:
        bool = False
        for x in list:
            if x == newNum:
                bool = True
  
        if(bool == False):
            list.append(newNum)
                 
        newNum = random.randint(0,8)
    newTuple = tuple(list)  
    return newTuple


def createHardCodedPuzzle():
    newPuzzleList = (1,2,3,4,5,6,7,0,8)
    newPuzzle=EightPuzzle(newPuzzleList)
    display(newPuzzleList)
    manhattan(newPuzzleList, newPuzzle)

#ALGORITHMS FOR 8 PUZZLE

def misplaced(newPuzzleList, newPuzzle):
    print("-----MISPLACED 8-----")
    start_time = time.time()
    astar_search_new(newPuzzle)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s FOR MISPLACED')



def manhattan(newPuzzleList, newPuzzle1):
    print("-----MANHATTAN 8-----")
    start_time = time.time()
    astar_search_new(newPuzzle1,newPuzzle1.h1)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s for MANHATTAN')


def max(newPuzzleList, newPuzzle2):
    print("-----MAX8 -----")
    start_time = time.time()
    astar_search_new(newPuzzle2,newPuzzle2.h2)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s for MAX')


#ALGORITHMS FOR DUCK PUZZLE

def misplacedDuck(newPuzzleList, newPuzzle):
    print("-----MISPLACED DUCK-----")
    start_time = time.time()
    astar_search_new(newPuzzle)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s FOR MISPLACED')

def manhattanDuck(newPuzzleList, newPuzzle1):
    print("-----MANHATTAN DUCK-----")
    start_time = time.time()
    astar_search_new(newPuzzle1,newPuzzle1.h1)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s for MANHATTAN')

def maxDuck(newPuzzleList, newPuzzle2):
    print("-----MAX DUCK-----")
    start_time = time.time()
    astar_search_new(newPuzzle2,newPuzzle2.h2)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s for MAX')



#DRIVER

#hardDuck = DuckPuzzle.hardCodedDuck()

newDuck1 = DuckPuzzle.make_rand_duck_puzzle()
newDuck2 = DuckPuzzle.make_rand_duck_puzzle()
newDuck3 = DuckPuzzle.make_rand_duck_puzzle()
newDuck4 = DuckPuzzle.make_rand_duck_puzzle()
newDuck5 = DuckPuzzle.make_rand_duck_puzzle()
newDuck6 = DuckPuzzle.make_rand_duck_puzzle()
newDuck7= DuckPuzzle.make_rand_duck_puzzle()
newDuck8= DuckPuzzle.make_rand_duck_puzzle()
newDuck9 = DuckPuzzle.make_rand_duck_puzzle()
newDuck0 = DuckPuzzle.make_rand_duck_puzzle()

#hardPuzzle = createHardCodedPuzzle()
puzzle1 = shuffle_8puzzle()
puzzle2 = shuffle_8puzzle()
puzzle3 = shuffle_8puzzle()
puzzle4 = shuffle_8puzzle()
puzzle5 = shuffle_8puzzle()
puzzle6 = shuffle_8puzzle()
puzzle7 = shuffle_8puzzle()
puzzle8 = shuffle_8puzzle()
puzzle9 = shuffle_8puzzle()
puzzle10 = shuffle_8puzzle()













