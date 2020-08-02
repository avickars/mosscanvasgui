# a1.py

from search import *

# ...
import time

#Code from aima-python-------------------------------------------------------------
# EightPuzzle class copied from search.py (aima-code) and modified
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
    
    def h2(self, node):
        """ Return the heuristic value for a given state. 
        Manhattan distance heuristic used """

        #print(node.state)
        #print(self.goal)
        
        #logic adapted from http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
        sumOfDistances = 0;
        for i in range(len(node.state)):
            #print('i:',i) 
            
            indexOfTileInGoalArray = self.goal.index(node.state[i])
            #print('indexOfTileInGoalArray:',indexOfTileInGoalArray) 
            
            distInFlatArray = abs(i-indexOfTileInGoalArray)
            #print('distInFlatArray:',distInFlatArray) 
            
            #we can move up/down and change the index by 3 in 1 move
            realDist = (distInFlatArray//3) + distInFlatArray%3;
            #print('realDist:',realDist) 
            
            sumOfDistances+=realDist;
        #print(sumOfDistances)
        #print("")
        #time.sleep(100)
            
        return sumOfDistances

    def h3(self, node):
        """ Return the heuristic value for a given state. 
        The max of Manhattan distance heuristic and number of misplaced tiles
        is used """

        numOfMisplacedTiles = sum(s != g for (s, g) in zip(node.state, self.goal))
        
        sumOfDistances = 0;
        for i in range(len(node.state)):            
            indexOfTileInGoalArray = self.goal.index(node.state[i])
            distInFlatArray = abs(i-indexOfTileInGoalArray)
            #we can move up/down and change the index by 3 in 1 move
            realDist = (distInFlatArray//3) + distInFlatArray%3;
            sumOfDistances+=realDist;
        
        return max(numOfMisplacedTiles,sumOfDistances)

        
# best_first_graph_search copied from search.py (aima-code) and modified
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
    numPoppedFromFrontier = 0
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        #count popped nodes
        numPoppedFromFrontier+=1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                
            print('#nodes removed from frontier:',numPoppedFromFrontier) 
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
                   
    print('#nodes removed from frontier:',numPoppedFromFrontier) 
    return None

# astar_search copied from search.py (aima-code) and modified
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


#Q2---------------------------------------------------------
def make_rand_8puzzle() -> EightPuzzle:
    #create a Eightpuzzle with a random initial state
    initialState = list((1, 2, 3, 4, 5, 6, 7, 8, 0))
    random.shuffle(initialState)
    newEightPuzzle = EightPuzzle(tuple(initialState))
    #display(initialState)
    
    #shuffle inplace until our initial state is solvable
    while (newEightPuzzle.check_solvability(initialState) == False):
        random.shuffle(initialState)
        newEightPuzzle = EightPuzzle(tuple(initialState))
        #display(initialState)
        
    return newEightPuzzle

def display(state):
    for i in range(9):
        if(state[i] == 0):
            #print * instead of 0
            print("* ",end="")
        else:
            print("%d " % state[i],end="")
        if((i+1)%3==0):
            #print linebreak
            print("")

#create 10 random 8-puzzle instances
EightPuzzleList = []
for i in range(10):
    EightPuzzleList.append(make_rand_8puzzle())

print("Q2-EightPuzzle Tests:")
for elem in EightPuzzleList:
    print(elem.initial)
    print("")
    
    #A* using misplaced tile heuristic
    startTime = time.time()
    node = astar_search(elem, h=elem.h)  
    deltaTime = time.time()-startTime

    print('Time in seconds(A* misplaced tile heuristic):', deltaTime)
    print('Length of Solution:', len(node.solution()))
    print('Solution:', node.solution())  
    print('Path:', node.path())
    print("")


    #A* using Manhattan distance heuristic
    startTime = time.time()
    node = astar_search(elem, h=elem.h2)  
    deltaTime = time.time()-startTime

    print('Time in seconds(A* Manhattan distance):', deltaTime)
    print('Length of Solution:', len(node.solution()))
    print('Solution:', node.solution())  
    print('Path:', node.path())
    print("")


    #A* using the max of misplaced tile and Manhattan distance heuristics
    startTime = time.time()
    node = astar_search(elem, h=elem.h3)  
    deltaTime = time.time()-startTime

    print('Time in seconds(A*  max of h1 and h2):', deltaTime)
    print('Length of Solution:', len(node.solution()))
    print('Solution:', node.solution())  
    print('Path:', node.path())

    print("")
    print("")


for i in range(0):
    #test example from textbook pg 103
    initial=(7,2,4,5,0,6,8,3,1)
    goal=(0,1,2,3,4,5,6,7,8)        
    
    problem_instance = EightPuzzle(initial, goal) 
    node = astar_search(problem_instance, h=problem_instance.h2)
    print('Length of Solution:', len(node.solution()))
    print('Solution:', node.solution())  
    print('Path:', node.path())















#Q3---------------------------------------------------------
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
            possible_actions = ['DOWN', 'RIGHT']
        elif index_blank_square == 1:
            possible_actions = ['DOWN', 'LEFT']
        elif index_blank_square == 2:
            possible_actions = ['UP','RIGHT']
        elif index_blank_square == 3:
            possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        elif index_blank_square == 4:
            possible_actions = ['DOWN', 'LEFT', 'RIGHT']            
        elif index_blank_square == 5:
            possible_actions = ['DOWN', 'LEFT']
        elif index_blank_square == 6:
            possible_actions = ['UP', 'RIGHT']
        elif index_blank_square == 7:
            possible_actions = ['UP', 'LEFT', 'RIGHT']
        elif index_blank_square == 8:
            possible_actions = ['UP','LEFT']  
        else:
            #unhandled state size
            raise NotImplementedError
            
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank <= 2:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
             
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """
        raise NotImplementedError

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def h2(self, node):
        """ Return the heuristic value for a given state. 
        Manhattan distance heuristic used """

        #print(node.state)
        #print(self.goal)
        
        #logic adapted from http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
        sumOfDistances = 0;
        for i in range(len(node.state)):
           # print('i:',i) 
            
            indexOfTileInGoalArray = self.goal.index(node.state[i])
            #print('indexOfTileInGoalArray:',indexOfTileInGoalArray) 
            
            distInFlatArray = abs(i-indexOfTileInGoalArray)
            #print('distInFlatArray:',distInFlatArray) 
            
            #we can move up/down and change the index by 3 in 1 move
            #technically we may only change the index by 2 
            #when moving down from or up to the first row
            #However this logic still underestimates the distance and is still valid.
            #placing the puzzle on a cartesian grid would make this more consistent
            realDist = (distInFlatArray//3) + distInFlatArray%3;
            #print('realDist:',realDist) 
            
            sumOfDistances+=realDist;
        #print(sumOfDistances)
        #print("")
        #time.sleep(100)
            
        return sumOfDistances

    def h3(self, node):
        """ Return the heuristic value for a given state. 
        The max of Manhattan distance heuristic and number of misplaced tiles
        is used """

        numOfMisplacedTiles = sum(s != g for (s, g) in zip(node.state, self.goal))
        
        sumOfDistances = 0;
        for i in range(len(node.state)):            
            indexOfTileInGoalArray = self.goal.index(node.state[i])
            distInFlatArray = abs(i-indexOfTileInGoalArray)
            #we can move up/down and change the index by 3 in 1 move
            realDist = (distInFlatArray//3) + distInFlatArray%3;
            sumOfDistances+=realDist;
        
        return max(numOfMisplacedTiles,sumOfDistances)




def make_rand_duckpuzzle() -> DuckPuzzle:
    #create a Eightpuzzle with a valid initial state
    initialState = list((1, 2, 3, 4, 5, 6, 7, 8, 0))
    newDuckPuzzle = DuckPuzzle(tuple(initialState))
    #display_duckpuzzle(initialState)
    
    #make random valid moves to create a valid initial state
    InitialShuffleAmount = 3000 #random.randint(500,2000)
    for i in range(InitialShuffleAmount):
        actionToDo = random.choice(newDuckPuzzle.actions(initialState))
        #print(actionToDo)
        initialState = newDuckPuzzle.result(initialState,actionToDo)
        newDuckPuzzle = DuckPuzzle(tuple(initialState))
        #display_duckpuzzle(newDuckPuzzle.initial)
        
    return newDuckPuzzle

def display_duckpuzzle(state):
    for i in range(9):
        if(state[i] == 0):
            #print * instead of 0
            print("* ",end="")
        else:
            print("%d " % state[i],end="")
        if(i==1 or i==5 or i==8):
            #print linebreak
            print("")
        if(i==5):
            print("  ",end="")
            
            
            
#create 10 random duck-puzzle instances
DuckPuzzleList = []
for i in range(10):
    DuckPuzzleList.append(make_rand_duckpuzzle())

print("Q3-DuckPuzzle Tests")
for elem in DuckPuzzleList:
    print(elem.initial)
    print("")
    
    #A* using misplaced tile heuristic
    startTime = time.time()
    node = astar_search(elem, h=elem.h)  
    deltaTime = time.time()-startTime

    print('Time in seconds(A* misplaced tile heuristic):', deltaTime)
    print('Length of Solution:', len(node.solution()))
    print('Solution:', node.solution())  
    print('Path:', node.path())
    print("")


    #A* using Manhattan distance heuristic
    startTime = time.time()
    node = astar_search(elem, h=elem.h2)  
    deltaTime = time.time()-startTime

    print('Time in seconds(A* Manhattan distance):', deltaTime)
    print('Length of Solution:', len(node.solution()))
    print('Solution:', node.solution())  
    print('Path:', node.path())
    print("")


    #A* using the max of misplaced tile and Manhattan distance heuristics
    startTime = time.time()
    node = astar_search(elem, h=elem.h3)  
    deltaTime = time.time()-startTime

    print('Time in seconds(A*  max of h1 and h2):', deltaTime)
    print('Length of Solution:', len(node.solution()))
    print('Solution:', node.solution())  
    print('Path:', node.path())

    print("")







