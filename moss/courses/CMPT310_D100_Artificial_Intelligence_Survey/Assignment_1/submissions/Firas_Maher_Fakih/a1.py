# a1.py
from search import *
import random
import time


# FIRAS FAKIH
# 301347333
# **********************************Implementations USED FROM search.py***************************************
def best_first_graph_search(problem, f, display=False):
    # prints the nodes removed and also searches
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
    removed = 0
    while frontier:
        node = frontier.pop()
        removed += 1
        if problem.goal_test(node.state):
            print("Total Nodes Removed: ", removed)
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


def astarSearch(problem, h=None, display=True):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


    
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
    
#***********************************QUESTION 2 IMPLEMENTATIONS*****************************************
 
    
    def Manhattan(self,node):
        # Manhattan Heuristic
        state = node.state
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index_state = {}
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        i = 0
        while (i < len(state)):
            index_state[state[i]] = index[i]
            i +=1
        
        manhattanx = 0
        manhattany = 0
        i = 0
        while (i < 9):
           manhattanx += abs(index_goal[i][0] - index_state[i][0])
           manhattany += abs(index_goal[i][1] - index_state[i][1])
           i += 1
        
        return (manhattanx + manhattany)
    def MaxH(self,node):
        # max Heuristic
        defaultH = self.h(node)
        manhattanH = self.Manhattan(node)
        return max(defaultH,manhattanH)



# ********************************************Question 1******************************************
def make_rand_8puzzle():
    # Returns a new instance of an EightPuzzle problem
    rSample = tuple(random.sample(range(0,9),9))
    instance1 = EightPuzzle(rSample)
    checker = instance1.check_solvability(instance1.initial)
    while (checker == False):
        rSample= tuple(random.sample(range(0,9),9))
        instance1 = EightPuzzle(rSample)
        checker = instance1.check_solvability(instance1.initial)
    print("SOLVABLE")
    return instance1
       

def display(state):
    # Displays the initial state
    eightP = []
    for i in range(0,len(state)):
        eightP.append(state[i])
        if eightP[i] == 0:
            eightP[i] = "*"
    print (eightP[0],eightP[1],eightP[2],sep=' ')
    print (eightP[3],eightP[4],eightP[5],sep=' ')
    print (eightP[6],eightP[7],eightP[8],sep=' ')

display(make_rand_8puzzle().initial)
# ********************************************Question 2******************************************

# Creating the set of 10 random puzzles

def CreateSetOfPuzzles():
    SetOfPuzzles = []
    for i in range (10):
        SetOfPuzzles.append(make_rand_8puzzle())
    return SetOfPuzzles

# Analysis

SetOfPuzzles = CreateSetOfPuzzles()
print("\n****************EIGHT PUZZLE ANALYSIS**********************\n")
for i in range(len(SetOfPuzzles)):    
    print("\nDefault misplaced tile heuristic")
    start_time = time.time()
    res = astarSearch(SetOfPuzzles[i],SetOfPuzzles[i].h)
    elapsed_time = time.time() - start_time
    print("Path cost is: ", res.path_cost)
    print("Total Time Taken (in seconds) : ", elapsed_time)
        


    print("\nA* Search using Manhattan Distance: ")
    start_time = time.time()
    res = astarSearch(SetOfPuzzles[i],SetOfPuzzles[i].Manhattan)
    elapsed_time = time.time() - start_time
    print("Path cost is: ", res.path_cost)
    print("Total time taken (in seconds) : ", elapsed_time)
        

    print("\nUsing Max(Manhattan, Default): ")
    start_time = time.time()
    res = astarSearch(SetOfPuzzles[i],SetOfPuzzles[i].MaxH)
    elapsed_time = time.time() - start_time
    print("Path cost is: ", res.path_cost)
    print("Total Time Taken (in seconds) : ", elapsed_time)

# *************************Question 3 IMPLEMENTATIONS USED FROM search.py******************************************
def best_first_graph_search0(problem, f, display=False):
    # prints the nodes removed and also searches
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
    removed = 0
    while frontier:
        node = frontier.pop()
        removed += 1
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return [node,removed]


def astarSearch0(problem, h=None, display=True):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search0(problem, lambda n: n.path_cost + h(n), display)






class DuckPuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        self.goal = goal
        Problem.__init__(self,initial,goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        # New set of Rules for Duck Puzzle
        
        NotUp = [1, 2, 5, 6]
        NotDown = [3, 7, 8]
        NotLeft = [1, 3, 7]
        NotRight = [2, 6, 0]

        if index_blank_square in NotLeft:
            possible_actions.remove('LEFT')
        if index_blank_square in NotUp:
            possible_actions.remove('UP')
        if index_blank_square in NotRight:
            possible_actions.remove('RIGHT')
        if index_blank_square in NotDown:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):

        # MODIFIED VERSION OF RESULT

        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # DeltaExcluded is for the nodes that have different variations and exceptions going up and down
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        DeltaExcluded = (2,3,1,4)
        DeltaExcluded0 = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        top = (0,)
        TopExclude0 = {'UP': -6, 'DOWN': 0, 'LEFT': -8, 'RIGHT': 0}

        if blank in DeltaExcluded:
            neighbor = blank + DeltaExcluded0[action]
        elif blank in top:
            neighbor = blank + TopExclude0[action]
        else:
            neighbor = blank + delta[action]

        new_state[blank-1], new_state[neighbor-1] = new_state[neighbor-1], new_state[blank-1]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def Manhattan(self, node):
        # Manhattan heuristic
        
        state = node.state
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index_state = {}
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        i = 0
        while (i < len(state)):
            index_state[state[i]] = index[i]
            i +=1
        
        manhattanx = 0
        manhattany = 0
        i = 0
        while (i < 9):
           manhattanx += abs(index_goal[i][0] - index_state[i][0])
           manhattany += abs(index_goal[i][1] - index_state[i][1])
           i += 1
        
        return (manhattanx + manhattany)

    def MaxH(self,node):
        # max Heuristic
        defaultH = self.h(node)
        manhattanH = self.Manhattan(node)
        return max(defaultH,manhattanH)


def make_rand_Housepuzzle():
    # Makes a random House Puzzle using sample function from random module
    

    rSample = tuple(random.sample(range(0,9),9))
    instance1 = DuckPuzzle(rSample)
    return instance1


def displayHouse(state):
    # Displays a tuple in the format of a House Puzzle
    # Displays 0 as a *

    HouseP = []
    for i in range(0,len(state)):
        HouseP.append(state[i])
        if HouseP[i] == 0:
            HouseP[i] = "*"
    print(HouseP[0], HouseP[1], sep=" ")
    print(HouseP[2], HouseP[3], HouseP[4], HouseP[5], sep=" ")
    print(" ", HouseP[6], HouseP[7], HouseP[8], sep=" ")


displayHouse(make_rand_Housepuzzle().initial)

def CreateSetOfDuckPuzzles():
    SetOfPuzzles = []
    for i in range (10):
        SetOfPuzzles.append(make_rand_Housepuzzle())
    return SetOfPuzzles

# *********************************Question 3 ANALYSIS******************************************

SetOfPuzzles = CreateSetOfDuckPuzzles()
print("\n****************DUCK PUZZLE ANALYSIS**********************\n")
for i in range(len(SetOfPuzzles)): 

    print("\nDefault misplaced tile heuristic")
    start_time = time.time()
    res = astarSearch0(SetOfPuzzles[i],SetOfPuzzles[i].h)
    elapsed_time = time.time() - start_time
    print("Total Nodes Removed: ", res[1])
    print("Path cost is: ", res[0].path_cost)
    print("Total Time Taken (in seconds) : ", elapsed_time)

        


    print("\nA* Search using Manhattan Distance: ")
    start_time = time.time()
    res = astarSearch0(SetOfPuzzles[i],SetOfPuzzles[i].Manhattan)
    elapsed_time = time.time() - start_time
    print("Total Nodes Removed: ", res[1])
    print("Path cost is: ", res[0].path_cost)
    print("Total time taken (in seconds) : ", elapsed_time)
        

    print("\nUsing Max(Manhattan, Default): ")
    start_time = time.time()
    res = astarSearch0(SetOfPuzzles[i],SetOfPuzzles[i].MaxH)
    elapsed_time = time.time() - start_time
    print("Total Nodes Removed: ", res[1])
    print("Path cost is: ", res[0].path_cost)
    print("Total Time Taken (in seconds) : ", elapsed_time)
