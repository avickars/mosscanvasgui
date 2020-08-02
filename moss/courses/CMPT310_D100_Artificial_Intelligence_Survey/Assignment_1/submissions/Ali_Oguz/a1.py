# a1.py

import sys
from collections import deque
from utils import *

import random
import time

"""
This Part Contains Changes I Made On The search.py . 
I have removed import from search as I copied each function I used from search.py as most of them are changed.


"""
class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


# ______________________________________________________________________________


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)


def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""

    #This is the frontier pop count
    #A function to  return this value has been implemented on line 424
    global frontierPopCount
    frontierPopCount = 0

    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        frontierPopCount = frontierPopCount + 1
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



def frontierPopCountReturn():
    return frontierPopCount


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

#Astar search with Manhattan Distance Heuristic Value
def astar_search_man(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.manD, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

#Astar search with max of misplaced tile heuristic and Manhattan Distance Heuristic Value
def astar_search_max(problem, h=None, display= False):
    h1 = problem.h(Node(problem.initial))
    h2 = problem.manD(Node(problem.initial))
    if h1 > h2:
        return astar_search(problem)
    else:
        return astar_search_man(problem)

# ______________________________________________________________________________
# A* heuristics 

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

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manD(self, node):
        """ Return the heuristic value for a given state. Manhattan Distance heuristic function used is 
        h(n) = sum of each tiles Manhattan Distance """

        # Idea of lookup table is taken from lecture
        distLookTable = []
        for i in range(0,9):
            distLookTable.append(list([]))
            for j in range(0,9):
                rowDiff = abs(i%3 - j%3)
                colDiff = abs(int(i/3) - int(j/3))
                totalDiff = rowDiff + colDiff
                distLookTable[(i)].append(totalDiff)
       
        tempState = list(node.state)
        manDistances = []
        manDistanceTotal = 0
        for i in range(0,9):
            if int(tempState[i]) == 0:
                tempDist = distLookTable[i][8]
            else:
                tempDist = distLookTable[i][int(tempState[i])-1]
            manDistances.append(tempDist)
            manDistanceTotal = manDistanceTotal + tempDist

        return manDistanceTotal

        #return sum(s != g for (s, g) in zip(node.state, self.goal))


#Edited EightPuzzle class for creating DuckPuzzle class 
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

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        if (index_blank_square == 1) or (index_blank_square == 5):
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        if (index_blank_square == 2) or (index_blank_square == 6):
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        #position 3 does not have any illegal move
        #if index_blank_square == 3:
        if index_blank_square == 4:
            possible_actions.remove('UP')
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
        if (blank >= 2) and (blank <= 5):
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif blank > 5:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': 0, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
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

    def manD(self, node):


        # Idea of lookup table is taken from lecture
        distLookTable = []
        for i in range(0,9):
            distLookTable.append(list([]))
            if i <= 1:
                rowI = 0
                colI = i
            elif 1 < i < 5:
                rowI = 1
                colI = i - 2
            else:
                rowI = 2
                colI = i - 6
                colI = colI + 1 # because last row is shifted to the left

            for j in range(0,9):
                if j <= 1:
                    rowJ = 0
                    colJ = j
                elif 1 < j < 5:
                    rowJ = 1
                    colJ = j - 2
                else:
                    rowJ = 2
                    colJ = i - 6
                    colJ = colJ + 1 # because last row is shifted to the left

                rowDiff = abs(rowI - rowJ)
                colDiff = abs(colI - colJ)
                totalDiff = rowDiff + colDiff
                distLookTable[(i)].append(totalDiff)
       
        tempState = list(node.state)
        manDistances = []
        manDistanceTotal = 0
        for i in range(0,9):
            if int(tempState[i]) == 0:
                tempDist = distLookTable[i][8]
            else:
                tempDist = distLookTable[i][int(tempState[i])-1]
            manDistances.append(tempDist)
            manDistanceTotal = manDistanceTotal + tempDist

        return manDistanceTotal

        #return sum(s != g for (s, g) in zip(node.state, self.goal))

"""
End of copied part of search.py
"""

def display(state):
    print(str(state[0]) + " " +str(state[1]) + " " + str(state[2]) + "\n" +  str(state[3]) + " " + str(state[4]) + " " + str(state[5]) + "\n" + str(state[6]) + " " + str(state[7]) + " " + str(state[8]) + "\n")

def displayDuck(state):
    print(str(state[0]) + " " +str(state[1]) + "\n" + str(state[2]) + " " +  str(state[3]) + " " + str(state[4]) + " " + str(state[5]) + "\n  " + str(state[6]) + " " + str(state[7]) + " " + str(state[8]) + "\n")    

def reverseMove(string):
    if string ==  'LEFT':
        return 'RIGHT'
    elif string == 'RIGHT':
        return 'LEFT'
    elif string == 'UP' :
        return 'DOWN'
    elif string == 'DOWN' :
        return 'UP'
    else:
        raise ValueError("Wrong input for reverseMove")


def make_rand_8puzzle():
    initState = (1,2,3,4,5,6,7,8,0)
    puzzleState= (1,2,3,4,5,6,7,8,0)
    ePuzzle = EightPuzzle(puzzleState,initState)
    posActions= ePuzzle.actions(puzzleState)
    shuffleMoveCount = random.randrange(20,50)
    x = 0
    while x < shuffleMoveCount :
        newAction = random.choice(posActions)
        puzzleState = ePuzzle.result(puzzleState, newAction)
        posActions= ePuzzle.actions(puzzleState)
        posActions.remove(reverseMove(newAction))
        x = x + 1
    return EightPuzzle(puzzleState,initState)


def make_rand_DuckPuzzle():
    initState = (1,2,3,4,5,6,7,8,0)
    puzzleState= (1,2,3,4,5,6,7,8,0)
    ePuzzle = DuckPuzzle(puzzleState,initState)
    posActions= ePuzzle.actions(puzzleState)
    shuffleMoveCount = random.randrange(20,50)
    x = 0
    while x < shuffleMoveCount :
        newAction = random.choice(posActions)
        puzzleState = ePuzzle.result(puzzleState, newAction)
        posActions= ePuzzle.actions(puzzleState)
        posActions.remove(reverseMove(newAction))
        x = x + 1
    return DuckPuzzle(puzzleState,initState)




#I will make graphs with 10 different random puzzles
puzzle = []
for i in range(0,10):
	puzzle.append(make_rand_8puzzle())
	print("Randomized puzzle number "+ str(i) +" : \n")
	display(puzzle[i].initial)
	print("Solvability of puzzle number "+ str(i) + " : " + str(bool(puzzle[i].check_solvability(puzzle[i].initial))) + "\n")




#Testing for A* search algortihm with misplaced tile heuristic 
timerA = []
resultA= []
popCountA= []
for i in range(0,10):
	timerA.append(time.time())
	resultA.append(astar_search(puzzle[i]))
	timerA[i]= time.time() - timerA[i]
	popCountA.append(frontierPopCountReturn())

	

#Testing for A* search algortihm with Manhattan Distance heuristic 
timerB = []
resultB= []
popCountB= []
for i in range(0,10):
	timerB.append(time.time())
	resultB.append(astar_search_man(puzzle[i]))
	timerB[i]= time.time() - timerB[i]
	popCountB.append(frontierPopCountReturn())

#Testing for A* search algortihm with max of misplaced tile heuristic and Manhattan Distance heuristic
timerC = []
resultC= []
popCountC= []
for i in range(0,10):
	timerC.append(time.time())
	resultC.append(astar_search_man(puzzle[i]))
	timerC[i]= time.time() - timerC[i]
	popCountC.append(frontierPopCountReturn())

print("info table for EightPuzzle")
print("A = A* with misplaced tile heuristic")
print("B = A* with Manhattan Distance heuristic")
print("C = A* with max of misplaced tile heuristic and Manhattan Distance heuristic")
print("Result table	|	len A 	|	len B 	| 	len C 	|	time A 	|	time B 	| 	time C 	|	pop A 	|	pop B 	| 	pop C 	|")
for i in range(0,10):
	print("Puzzle number "+ str(i) +" |\t" + str(len(resultA[i].solution())) + "\t|\t" + str(len(resultB[i].solution())) + "\t|\t" + str(len(resultC[i].solution())) + "\t|\t" + str(timerA[i])  + "|\t" + str(timerB[i])  + "|\t" + str(timerC[i])  + "|\t" +  str(popCountA[i]) + "\t|\t"+  str(popCountB[i]) + "\t|\t"+  str(popCountC[i]) + "\t|\t"  )


#I will make graphs with 10 different random puzzles
dPuzzle = []
for i in range(0,10):
	dPuzzle.append(make_rand_DuckPuzzle())
	print("Randomized puzzle number "+ str(i) +" : \n")
	displayDuck(dPuzzle[i].initial)


#Testing for A* search algortihm with misplaced tile heuristic 
timerDuckA = []
resultDuckA= []
popCountDuckA= []
for i in range(0,10):
	timerDuckA.append(time.time())
	resultDuckA.append(astar_search(dPuzzle[i]))
	timerDuckA[i]= time.time() - timerDuckA[i]
	popCountDuckA.append(frontierPopCountReturn())

	

#Testing for A* search algortihm with Manhattan Distance heuristic 
timerDuckB = []
resultDuckB= []
popCountDuckB= []
for i in range(0,10):
	timerDuckB.append(time.time())
	resultDuckB.append(astar_search_man(dPuzzle[i]))
	timerDuckB[i]= time.time() - timerDuckB[i]
	popCountDuckB.append(frontierPopCountReturn())

#Testing for A* search algortihm with max of misplaced tile heuristic and Manhattan Distance heuristic
timerDuckC = []
resultDuckC= []
popCountDuckC= []
for i in range(0,10):
	timerDuckC.append(time.time())
	resultDuckC.append(astar_search_man(dPuzzle[i]))
	timerDuckC[i]= time.time() - timerDuckC[i]
	popCountDuckC.append(frontierPopCountReturn())

print("info table for DuckPuzzle")
print("A = A* with misplaced tile heuristic")
print("B = A* with Manhattan Distance heuristic")
print("C = A* with max of misplaced tile heuristic and Manhattan Distance heuristic")
print("Result table	|	len A 	|	len B 	| 	len C 	|	time A 	|	time B 	| 	time C 	|	pop A 	|	pop B 	| 	pop C 	|")
for i in range(0,10):
	print("Puzzle number "+ str(i) +" |\t" + str(len(resultDuckA[i].solution())) + "\t|\t" + str(len(resultDuckB[i].solution())) + "\t|\t" + str(len(resultDuckC[i].solution())) + "\t|\t" + str(timerDuckA[i])  + "|\t" + str(timerDuckB[i])  + "|\t" + str(timerDuckC[i])  + "|\t" +  str(popCountDuckA[i]) + "\t|\t"+  str(popCountDuckB[i]) + "\t|\t"+  str(popCountDuckC[i]) + "\t|\t"  )
