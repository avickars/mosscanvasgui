# a1.py Jim Randa 301298943

from search import *
import random
import time

###############################################
##          FUNCTIONS FROM AIMA              ##
###############################################


def my_astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return my_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def my_best_first_graph_search(problem, f, display=False):
    count = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        count+=1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node,count
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, count

#DOES NOT INCLUDE 0
def Misplaced(node):
    i = sum((s != g and s != 0) for (s, g) in zip(node.state, (1,2,3,4,5,6,7,8,0)))
    #print(i)
    return i



###############################################
##          EIGHT PUZZLE FUNCTIONS           ##
###############################################

def make_rand_8puzzle():
    currentState = (1,2,3,4,5,6,7,8,0)
    EP = EightPuzzle(initial=currentState)
    
    solvable = False
    
    while not solvable:
        for i in range(100):
    	    possibleActions = EP.actions(currentState)
    	    actionToTake = possibleActions[random.randint(0,len(possibleActions) -1)]
    	    currentState = EP.result(state=currentState, action=actionToTake)
        solvable = EP.check_solvability(currentState)

    randomEP = EightPuzzle(initial = currentState)
    return randomEP

def display(state):
    string = ""
    for i in range(len(state)):
        if i % 3 == 0:
            string += "\n"
        if state[i] == 0:
            string += "* "
        else:
            string += str(state[i]) + " "
        
    print(string)

#Manhattan heuristic function
def MH(Node):
    total = 0

    for i in range(1,9):
        currentIndex = Node.state.index(i)
        goalIndex = (1,2,3,4,5,6,7,8,0).index(i)
        total += Manhatten(currentIndex, goalIndex)
    #print(total)
    return total 

def Manhatten(currentIndex, goalIndex):
    if(currentIndex == 0):
        return (0,1,2,1,2,3,2,3,4)[goalIndex]
    elif(currentIndex==1):
        return (1,0,1,2,1,2,3,2,3)[goalIndex]
    elif(currentIndex==2):
        return (2,1,0,3,2,1,4,3,2)[goalIndex]
    elif(currentIndex==3):
        return (1,2,3,0,1,2,1,2,3)[goalIndex]
    elif(currentIndex==4):
        return (2,1,2,1,0,1,2,1,2)[goalIndex]
    elif(currentIndex==5):
        return (3,2,1,2,1,0,3,2,1)[goalIndex]
    elif(currentIndex==6):
        return (2,3,4,1,2,3,0,1,2)[goalIndex]
    elif(currentIndex==7):
        return (3,2,3,2,1,2,1,0,1)[goalIndex]
    elif(currentIndex==8):
        return (4,3,2,3,2,1,2,1,0)[goalIndex]

#Max of misplaced / manhattan
def Max(Node):
    defaultH = Misplaced(Node)
    Manhatten = MH(Node)
    return max(defaultH, Manhatten)

Puzzles = []

for i in range(10):
    Puzzles.append(make_rand_8puzzle())

AlgorithmTests = (("Misplaced Tile (Not including 0)", Misplaced), ("Manhatten", MH), ("Max", Max))

for puzzle in Puzzles:
    display(puzzle.initial)
    for Algorithm in AlgorithmTests:  
        print("Solving with " + Algorithm[0])
        start_time = time.time()
        info, totalPopped = my_astar_search(puzzle, Algorithm[1])
        elapsed_time = time.time() - start_time
        print("Solved in " + str(info.depth) + " moves")
        print("Nodes removed from frontier: " + str(totalPopped))
        print(f'elapsed time (in seconds): {elapsed_time}s')




print("######################################\n##     DUCK PUZZLES NOW         ##\n######################################")

###############################################
##          DUCK PUZZLE CODE BELOW           ##
###############################################


class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1,2,3,4,5,6,7,8,0)):
        super().__init__(initial, goal)
        
    def find_blank_square(self,state):
        return state.index(0)
        
    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        ibs = self.find_blank_square(state)
        
        if (ibs in (0,1,4,5)):
            possible_actions.remove('UP')
        if (ibs in (2,6,7,8)):
            possible_actions.remove('DOWN')
        if (ibs in (0,2,6)):
            possible_actions.remove('LEFT')
        if (ibs in (1,5,8)):
            possible_actions.remove('RIGHT')   
            
        return possible_actions
          
    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        if (blank in (0,1,2)):
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif (blank == 3):
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)


def make_rand_duckpuzzle():
    currentState = (1,2,3,4,5,6,7,8,0)
    DP = DuckPuzzle(initial=currentState)
    
    for i in range(1000):
        possibleActions = DP.actions(currentState)
        actionToTake = possibleActions[random.randint(0,len(possibleActions) -1)]
        currentState = DP.result(state=currentState, action=actionToTake)

    randomDP = DuckPuzzle(initial = currentState)
    return randomDP

def displayDuck(state):
    print(str(state[0]) + " " + str(state[1]) + "\n" + str(state[2]) + " " + str(state[3]) + " " + str(state[4]) + " " + str(state[5]) + "\n  " + str(state[6]) + " " + str(state[7]) + " " + str(state[8]))


def DMH(Node):
    total = 0

    for i in range(1,9):
        currentIndex = Node.state.index(i)
        goalIndex = (1,2,3,4,5,6,7,8,0).index(i)
        total += DuckManhattan(currentIndex, goalIndex)
    #print(total)
    return total

def DuckManhattan(currentIndex, goalIndex):
    if(currentIndex == 0):
        return (0,1,1,2,3,4,3,4,5)[goalIndex]
    elif(currentIndex==1):
        return (1,0,2,1,2,3,2,3,4)[goalIndex]
    elif(currentIndex==2):
        return (1,2,0,1,2,3,2,3,4)[goalIndex]
    elif(currentIndex==3):
        return (2,1,1,0,1,2,1,2,3)[goalIndex]
    elif(currentIndex==4):
        return (3,2,2,1,0,1,2,1,2)[goalIndex]
    elif(currentIndex==5):
        return (4,3,3,2,1,0,3,2,1)[goalIndex]
    elif(currentIndex==6):
        return (3,2,2,1,2,3,0,1,2)[goalIndex]
    elif(currentIndex==7):
        return (4,3,3,2,1,2,1,0,1)[goalIndex]
    elif(currentIndex==8):
        return (5,4,4,3,2,1,2,1,0)[goalIndex]

def DuckMax(Node):
    defaultH = Misplaced(Node)
    Manhatten = DMH(Node)
    return max(defaultH, Manhatten)



DuckPuzzles = []
for i in range(10):
    DuckPuzzles.append(make_rand_duckpuzzle())
    
AlgorithmTests = (("Misplaced Tile (Not including 0)", Misplaced), ("Manhatten", DMH), ("Max", DuckMax))

for puzzle in DuckPuzzles:
    print("")
    displayDuck(puzzle.initial)
    for Algorithm in AlgorithmTests:  
        print("Solving with " + Algorithm[0])
        start_time = time.time()
        info, totalPopped = my_astar_search(puzzle, Algorithm[1])
        elapsed_time = time.time() - start_time
        print("Solved in " + str(info.depth) + " moves")
        print("Nodes removed from frontier: " + str(totalPopped))
        print(f'elapsed time (in seconds): {elapsed_time}s')


