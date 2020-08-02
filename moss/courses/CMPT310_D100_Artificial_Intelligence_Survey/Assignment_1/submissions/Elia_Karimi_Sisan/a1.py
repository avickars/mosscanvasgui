# a1.py

#Elia Karimi Sisan - 301369976

#Acknowledgments:
#Random Module: https://docs.python.org/3.7/library/random.html
#Python Arrays and Sets: https://www.i-programmer.info/programming/python/3942-arrays-in-python.html?start=1
#Manhattan Distance: http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
#TA: Mohammadmahdi Jahanara

#Testing Note: Script starts with running Q1Test() which is the test for Question One. Please uncomment Q2Test(), and Q3Test() functions for Question Two and Question Three tests respectively from their sections when required.

from search import *
import random
import time

#--------------------------------------------------Question 1: Helper Functions-------------------------------------------------

#Function that returns a new instance of an EightPuzzle problem with a random initial state that is solvable
def make_rand_8puzzle():
    while(True):
        initialState=[i for i in range(9)]
        random.shuffle(initialState)
        randomState = tuple(initialState) #Convert to tuple
        newPuzzle = EightPuzzle(randomState)
        solvabilityFlag = newPuzzle.check_solvability(randomState) #check_solvability called to ensure initial state is solvable
        
        if (solvabilityFlag == True):
            newPuzzle = EightPuzzle(randomState)
            break

return newPuzzle #Returns instance of EightPuzzle problem with solvable random initial state

#Function that takes an 8-puzzle state as input and prints a neat and readable representation of it.
def display(state):
    puzzleState=[i*0 for i in state]
    for i in state:
        puzzleState[i] = state[i]
        if (puzzleState[i] == 0): #If 0 (blank) is present, print "*" character
            puzzleState[i] = "*"

print ('|', puzzleState[0],'|', puzzleState[1],'|', puzzleState[2], '|')
print ('|', puzzleState[3],'|', puzzleState[4],'|', puzzleState[5], '|')
print ('|', puzzleState[6],'|', puzzleState[7],'|', puzzleState[8], '|')

#Testing for Question 1
def Q1Test():
    test = make_rand_8puzzle()
    display(test.initial)

Q1Test()

#------------------------------------------------Question 2: Comparing Algorithms-----------------------------------------------

#Following code (EightPuzzle Class) taken from Search.py in the aima-python code repository
# ______________________________________________________________________________ Begin Aima-Python Code
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

#A*-Search using misplaced tile heuristic
def h(self, node):
    """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """
            
            return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal)) #Exclude 0 (s!=0) because heuristic never overestimates the cost of reaching the goal

#Timer function provided in hints section of the Assignment
def timer(a,b):
    start_time = time.time()
    astar_search(a,b)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')

#A*-Search function modified by taking display out of the parameters
def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

#Best-First Graph Search function modified to output the total number of nodes removed from frontier and
#the length of the solution
def best_first_graph_search(problem, f):
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
    removedNodes = 0 #Variable to hold number of nodes removed from frontier
    
    while frontier:
        node = frontier.pop()
        removedNodes = removedNodes + 1 #Increment total number of nodes removed
        
        if problem.goal_test(node.state):
            print("Total number of nodes removed from the frontier is: ", removedNodes)
            print("Length of the solution is: ",len(node.solution()))
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
# ______________________________________________________________________________ End Aima-Python Code

#A*-Search using manhattan distance heuristic
def manhattanEight(node):
    state = node.state
    index_goal = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1], 0: [2, 2]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    
    for i in range(len(state)):
        index_state[state[i]] = index[i]
    
    mhd = 0 #Total manhattan distance
    dx = 0 #Delta X variable for calculating horizontal movements
    dy = 0 #Delta Y variable for calculating vertical movements
    
    for i in range(9):
        if(i!=0): #Exclude 0 because heuristic never overestimates the cost of reaching the goal
            dx = abs(index_goal[i][0] - index_state[i][0])
            dy = abs(index_goal[i][1] - index_state[i][1])
            mhd = dx + dy + mhd
    
    return mhd

#A*-Search using maximum of misplaced tile heuristic and manhattan distance heuristic
def maxHeuristicEight(node):
    eightPuzz = EightPuzzle(node.state)
    return max(eightPuzz.h(node),manhattanEight(node))

#Testing for Question 2
def Q2Test():
    for i in range(10):
        algorithmTest = make_rand_8puzzle()
        print(algorithmTest.initial)
        display(algorithmTest.initial)
        
        print("------------------------------------------------------------------------------------")
        print("A*-Search using misplaced tile heuristic")
        timer(algorithmTest,algorithmTest.h)
        print("------------------------------------------------------------------------------------")
        
        print("A*-Search using manhattan distance heuristic")
        timer(algorithmTest,manhattanEight)
        print("------------------------------------------------------------------------------------")
        
        print("A*-Search using maximum of misplaced tile heuristic and manhattan distance heuristic")
        timer(algorithmTest,maxHeuristicEight)
        print("------------------------------------------------------------------------------------")

#***********Please Uncomment the following line to test Question 2***********
#Q2Test()

#-------------------------------------------------Question 3: The House Puzzle--------------------------------------------------

#Following code (DuckPuzzle Class) taken from Search.py in the aima-python code repository and modified for
#the DuckPuzzle Problem

# ______________________________________________________________________________ Begin Aima-Python Code
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
    
    #Function changed to reflect possible moves given current index of the Blank Square of the DuckPuzzle
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
            The result would be a list, since there are only four possible actions
            in any given state of the environment """
        
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
        
        if index_blank_square == 0:
            possible_actions.remove('UP')
            possible_actions.remove('LEFT')
        if index_blank_square == 1 or index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')
        
        return possible_actions
    
    #Function changed to return a new state given current index of the Blank Square of the DuckPuzzle
    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
            Action is assumed to be a valid action in the state """
        
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        if blank == 0 or blank == 1 or blank == 2:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        if blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank == 4 or blank == 5 or blank == 6 or blank == 7 or blank == 8:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        
        return tuple(new_state)
    
    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        
        return state == self.goal
    
    #Not used for DuckPuzzle as I merely only made random moves from the goal state for the initial of the puzzle,
    #hence it is always solvable
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
        
        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal)) #Exclude 0 (s!=0) because heuristic never overestimates the cost of reaching the goal
# ______________________________________________________________________________ End Aima-Python Code

#Function that returns a new instance of an DuckPuzzle problem with a random initial state that is solvable.
def make_rand_duckpuzzle():
    goalState=[1,2,3,4,5,6,7,8,0]
    randomState = tuple(goalState)
    duckPuzzle = DuckPuzzle(randomState)
    
    #Start from goal state and randomly make n moves, where n is a random integer in [50,5000]
    for i in range(random.randint(50,5000)):
        actions = duckPuzzle.actions(duckPuzzle.initial)
        randMove = random.randint(0,len(actions)-1)
        randomState = duckPuzzle.result(duckPuzzle.initial, actions[randMove])
        duckPuzzle = DuckPuzzle(randomState)
    
    return duckPuzzle #Returns instance of DuckPuzzle problem with solvable random initial state

#Function that takes a DuckPuzzle state as input and prints a neat and readable representation of it.
def displayDuck(state):
    puzzleState=[i*0 for i in state]
    for i in state:
        puzzleState[i] = state[i]
        if (puzzleState[i] == 0): #If 0 is present, print "*" character
            puzzleState[i] = "*"

print (puzzleState[0], puzzleState[1])
print (puzzleState[2], puzzleState[3],puzzleState[4],puzzleState[5])
print (' ', puzzleState[6], puzzleState[7], puzzleState[8])

#A*-Search using manhattan distance heuristic
def manhattanDuck(node):
    state = node.state
    index_goal = {1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2], 0: [2, 3]}
    index_state = {}
    index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]
    
    for i in range(len(state)):
        index_state[state[i]] = index[i]
    
    mhd = 0 #Total manhattan distance
    dx = 0 #Delta X variable for calculating horizontal movements
    dy = 0 #Delta Y variable for calculating vertical movements
    
    for i in range(9):
        if(i!=0): #Exclude 0 because heuristic never overestimates the cost of reaching the goal
            dx = abs(index_goal[i][0] - index_state[i][0])
            dy = abs(index_goal[i][1] - index_state[i][1])
            mhd = dx + dy + mhd
    
    return mhd

#A*-Search using maximum of misplaced tile heuristic and manhattan distance heuristic
def maxHeuristicDuck(node):
    duckPuzz = DuckPuzzle(node.state)
    return max(duckPuzz.h(node),manhattanDuck(node))

#Testing for Question 3
def Q3Test():
    for i in range(10):
        duckTest = make_rand_duckpuzzle()
        print(duckTest.initial)
        displayDuck(duckTest.initial)
        
        
        print("------------------------------------------------------------------------------------")
        print("A*-Search using misplaced tile heuristic")
        timer(duckTest,duckTest.h)
        print("------------------------------------------------------------------------------------")
        
        print("A*-Search using manhattan distance heuristic")
        timer(duckTest,manhattanDuck)
        print("------------------------------------------------------------------------------------")
        
        print("A*-Search using maximum of misplaced tile heuristic and manhattan distance heuristic")
        timer(duckTest,maxHeuristicDuck)
        print("------------------------------------------------------------------------------------")

#***********Please Uncomment the following line to test Question 3***********
#Q3Test()
