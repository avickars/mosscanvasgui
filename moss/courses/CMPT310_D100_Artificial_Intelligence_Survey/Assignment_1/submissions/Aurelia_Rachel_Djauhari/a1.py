#CMPT 310 a1.py
#Experimenting with the 8-puzzle
#referenced a lot of python documentation at docs.python.org
#referenced information on python functions etc from www.w3schools.com/python and tutorialspoint.com as well

from search import *
import random
import time

#from textbook github code search.py--------------------------

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

    #Added Manhattan Distance Heuristic Function and Max of Misplaced Tile and Manhattan Distance Heuristic Function

    def manhattan(self, node):
        xDistance = 0
        yDistance = 0
        manhattanDistance = 0
        goalIndex = [[2,2], [0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1]] #0,1,2,3,4,5,6,7,8

        #get indicies from node state
        nodeState = node.state
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]] #1,2,3,4,5,6,7,8,0
        nodeIndex = {}

        #reordering nodeState in nodeIndex to be in the order 0,1,2,3,4,5,6,7,8 and simultaneously
        #assigning the index corresponding to its nodeState position
        for i in range(len(nodeState)):
            nodeIndex[nodeState[i]] = index[i]

        #find the difference in indices for x and y and add them up
        for i in range(9):
            xDistance = xDistance + abs(goalIndex[i][0] - nodeIndex[i][0])
            yDistance = yDistance + abs(goalIndex[i][1] - nodeIndex[i][1])

        manhattanDistance = xDistance + yDistance

        return manhattanDistance

    def max(self, node):
        maximum = 0

        maximum = max(self.h(node), self.manhattan(node))

        return maximum

    #----------------------------------------------------------end of changes to original textbook code

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    nodesRemoved = 0 #added this variable to keep track of nodes being removed from the frontier
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        #pop means nodes are being removed from frontier
        nodesRemoved += 1 #add 1 to number of nodes removed
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, nodesRemoved] #return also the number of nodes removed from frontier
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

#----------------------------------------------------------end of code changed from github textbook code


#Question 1 -- Helper Functions
def make_rand_8puzzle():
    #returns a new instance of an EightPuzzle problem with a random initial state that is solvable

    board = (range(9)) #(0,1,2,3,4,5,6,7,8)

    #store shuffled board while original board stays the same
    initialState = random.sample(board, len(board))

    #instance of the EightPuzzle w the randomly generated initialState
    newPuzzle = EightPuzzle(tuple(initialState))

    #check for solvability and keep generating initialState while check_solvability == False
    while (newPuzzle.check_solvability(newPuzzle.initial) == False):
        initialState = random.sample(board, len(board))
        newPuzzle = EightPuzzle(tuple(initialState))

    return newPuzzle

def display(state):
    #takes an 8-puzzle state and prints it

    displayState = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for index in range(9):
        if (state[index] == 0):
             displayState[index] = '*' #changing 0 to display as '*'
        else:
             displayState[index] = state[index]

    #print in format: 1 2 3
    #		      4 5 6
    #		      7 8 * 

    print(displayState[0], displayState[1], displayState[2])
    print(displayState[3], displayState[4], displayState[5])
    print(displayState[6], displayState[7], displayState[8])


#Question 2 -- Comparing Algorithms

#A*-search heuristics-------------------------

#taken from github textbook code and left unchanged--------------------
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
#----------------------------------------------------------------------

#Manhattan distance heuristic
def astar_search_manhattan(problem, h=None, display=False):
    h = memoize(h or problem.manhattan, 'h')

    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

#Max of misplaced tile and manhattan distance heuristic
def astar_search_max(problem, h=None, display=False):
    h = memoize(h or problem.max, 'h')

    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

#---------------------------------------------

for iterations in range(10):

    #create instance of random 8-puzzle
    newPuzzle = make_rand_8puzzle()

    #display what the random 8-puzzle looks like before solving
    display(newPuzzle.initial)

    #A*-search using misplaced tile heuristic (default in 8-puzzle class)
    startTime1 = time.time() #returns time in seconds since the epoch (the point where the time starts)
    search = astar_search(newPuzzle)
    endTime1 = time.time()
    duration1 = endTime1 - startTime1

    #cost of path is the number of tiles moved from state1 to state2, in this case, initial to goal
    #can get path_cost from Problem class
    length1 = search[0].path_cost

    #removedNodes value from index 1 of array returned from the best_first_graph_search
    nodesRemoved1 = search[1]

    print("Total running time in seconds: ", duration1)
    print("Length of the solution: ", length1)
    print("Number of nodes that were removed from the frontier: ", nodesRemoved1)

    #A*-search using the manhattan distance heuristic
    startTime2 = time.time()
    searchManhattan = astar_search_manhattan(newPuzzle)
    endTime2 = time.time()
    duration2 = endTime2 - startTime2

    length2 = searchManhattan[0].path_cost

    nodesRemoved2 = searchManhattan[1]

    print("Total running time in seconds: ", duration2)
    print("Length of the solution: ", length2)
    print("Number of nodes that were removed from the frontier: ", nodesRemoved2)

    #A*-search using the max of the misplaced tile heuristic and the manhattan distance heuristic
    startTime3 = time.time()
    searchMax = astar_search_max(newPuzzle)
    endTime3 = time.time()
    duration3 = endTime3 - startTime3

    length3 = searchMax[0].path_cost

    nodesRemoved3 = searchMax[1]

    print("Total running time in seconds: ", duration3)
    print("Length of the solution: ", length3)
    print("NUmber of nodes that were removed from the frontier: ", nodesRemoved3)

#Question 3 -- The House-Puzzle (Duck-Puzzle)
class DuckPuzzle(Problem):

    def __init__(self, initial, goal=(1,2,3,4,5,6,7,8,0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        removeRight = [1, 5, 8]
        removeLeft = [0, 2, 6]
        removeDown = [2, 6, 7, 8]
        removeUp = [0, 1, 4, 5]

        if index_blank_square in removeLeft:
            possible_actions.remove('LEFT')
        if index_blank_square in removeRight:
            possible_actions.remove('RIGHT')
        if index_blank_square in removeUp:
            possible_actions.remove('UP')
        if index_blank_square in removeDown:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        #blank is index of blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1} #regular way
        deltaException = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1} #for 1->3 and back and 2->4 and back
        blankException = (1, 3, 2, 4)

        if blank in blankException:
            neighbor = blank + deltaException[action]
        else:
            neighbor = blank + delta[action]

        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        xDistance = 0
        yDistance = 0
        manhattanDistance = 0
        goalIndex = [[2,2], [0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1]] #0,1,2,3,4,5,6,7>

        #get indicies from node state
        nodeState = node.state
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]] #1,2,3,4,5,6,7,8,0
        nodeIndex = {}

        #reordering nodeState in nodeIndex to be in the order 0,1,2,3,4,5,6,7,8 and simultaneously
        #assigning the index corresponding to its nodeState position
        for i in range(len(nodeState)):
            nodeIndex[nodeState[i]] = index[i]

        #find the difference in indices for x and y and add them up
        for i in range(9):
            xDistance = xDistance + abs(goalIndex[i][0] - nodeIndex[i][0])
            yDistance = yDistance + abs(goalIndex[i][1] - nodeIndex[i][1])

        manhattanDistance = xDistance + yDistance

        return manhattanDistance

    def max(self, node):
        maximum = 0

        maximum = max(self.h(node), self.manhattan(node))

        return maximum


def make_rand_duckpuzzle():

    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    newPuzzle = DuckPuzzle(tuple(goal))

    for slides in range(100):
        possibleActions = newPuzzle.actions(newPuzzle.initial)
        randIndex = random.randint(0, len(possibleActions) - 1)
        newPuzzle.initial = newPuzzle.result(newPuzzle.initial, possibleActions[randIndex])

    return newPuzzle

def display_duckpuzzle(state):
    #takes a duck puzzle  state and prints it

    displayState = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for index in range(9):
        if (state[index] == 0):
             displayState[index] = '*' #changing 0 to display as '*'
        else:
             displayState[index] = state[index]

    #print in format: 1 2
    #                 3 4 5 6
    #                   7 8 * 

    print(displayState[0], displayState[1])
    print(displayState[2], displayState[3], displayState[4], displayState[5])
    print(" ", displayState[6], displayState[7], displayState[8])


for iterations in range(10):

    #create instance of random duck-puzzle
    newPuzzleDuck = make_rand_duckpuzzle()

    #display what the random duck-puzzle looks like before solving
    display_duckpuzzle(newPuzzleDuck.initial)

    #A*-search using misplaced tile heuristic
    startTime1Duck = time.time() #returns time in seconds since the epoch (the point where the time star>
    searchDuck = astar_search(newPuzzleDuck)
    endTime1Duck = time.time()
    duration1Duck = endTime1Duck - startTime1Duck

    #cost of path is the number of tiles moved from state1 to state2, in this case, initial to goal
    #can get path_cost from Problem class
    length1Duck = searchDuck[0].path_cost

    #removedNodes value from index 1 of array returned from the best_first_graph_search
    nodesRemoved1Duck = searchDuck[1]

    print("Total running time in seconds: ", duration1Duck)
    print("Length of the solution: ", length1Duck)
    print("Number of nodes that were removed from the frontier: ", nodesRemoved1Duck)

    #A*-search using the manhattan distance heuristic
    startTime2Duck = time.time()
    searchManhattanDuck = astar_search_manhattan(newPuzzleDuck)
    endTime2Duck = time.time()
    duration2Duck = endTime2Duck - startTime2Duck

    length2Duck = searchManhattanDuck[0].path_cost

    nodesRemoved2Duck = searchManhattanDuck[1]

    print("Total running time in seconds: ", duration2Duck)
    print("Length of the solution: ", length2Duck)
    print("Number of nodes that were removed from the frontier: ", nodesRemoved2Duck)

    #A*-search using the max of the misplaced tile heuristic and the manhattan distance heuristic
    startTime3Duck = time.time()
    searchMaxDuck = astar_search_max(newPuzzleDuck)
    endTime3Duck = time.time()
    duration3Duck = endTime3Duck - startTime3Duck

    length3Duck = searchMaxDuck[0].path_cost

    nodesRemoved3Duck = searchMaxDuck[1]

    print("Total running time in seconds: ", duration3Duck)
    print("Length of the solution: ", length3Duck)
    print("Number of nodes that were removed from the frontier: ", nodesRemoved3Duck)

