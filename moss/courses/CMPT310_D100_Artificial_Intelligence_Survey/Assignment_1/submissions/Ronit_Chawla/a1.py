'''
Ronit Chawla 
301329044
rchawla@sfu.ca
Assignment 1, CMPT310, Prof Toby Donaldson

Annotation:
In the file named search.py i have just made one modification to the function named, best_first_graph_search. The modification is made in order to accomodate
total frontiers removed

Citation:
-> Manhattan distance fromula reference from https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game
-> Manhatan distance formula used for the DuckPuzzle was taken from TA's tutorial video 
-> check solvability idea for the Duck puzzle taken from the same tutorial video
-> Duck Puzzle, make_rand_duck_puzzle discussed with friend and some other doubts as well were also discussed in order to make the question three functional


'''

from search import *
import random
import time

############################################################    QUESTION 1   ###############
numbersTuple = (1,2,3,4,5,6,7,8,0)
def make_rand_8puzzle():
    RandomNumbers = random.sample(numbersTuple,9) #makerandom selection without repetirion
    tupleRandomNumbers = tuple(RandomNumbers)
    instanceOne = EightPuzzle(tupleRandomNumbers)
    boolCheck = instanceOne.check_solvability(tupleRandomNumbers)
    #print(boolCheck)
    #print(type(tupleRandomNumbers))
    while(boolCheck == False):
        RandomNumbers = random.sample(numbersTuple,9) #makerandom selection without repetirion
        tupleRandomNumbers = tuple(RandomNumbers)
        instanceOne = EightPuzzle(tupleRandomNumbers)
        boolCheck = instanceOne.check_solvability(tupleRandomNumbers)
    #print(boolCheck)
    return instanceOne

def display(state):
    #print(state)
    tempList=list(state)
    #print(type(tempList))
    count=0
    
    for i in range(0,3):
        for j in range(0,3):
            
            if( tempList[count] == 0):
                print('*',end="   ")
            else:
                print(tempList[count], end="   ")
            count+=1
        print()
            
    #print(state)

##################################################### QUESTION 2 ########################
def ManhattanDist(node):
    tupleState=node.state
    sum=0
    for i in range(0,9):
        if tupleState[i]==0:
            sum+=(abs(int(i/3)-2)+abs(i%3-2))
        sum+= (abs(int(i/3)-int((tupleState[i]-1)/3))+abs(i%3-(tupleState[i]-1)%3))
    return sum

def maxManDist(node):
    inst=EightPuzzle(node.state)
    if(ManhattanDist(node) > inst.h(node)):
        return ManhattanDist(node)
    else:
        return inst.h(node)
    return max(ManhattanDist(node),inst.h(node))

for i in range(0,2):
    puzzle=make_rand_8puzzle()
    print('Random instance '+ str(i+1) + ' of Eight Puzzle')
    display(puzzle.initial)

    startTime = time.time()
    astarResult, nodesRemoved = astar_search(puzzle)
    print(astarResult)
    endTime = time.time() - startTime
    print('Misplaced Tile Heuristic')
    print('Total time taken: '+ str(endTime))
    print('Total nodes removed from frontier: '+str(nodesRemoved))
    print('Total length or # of tiles moved: '+str(len(astarResult.solution())))
    display(astarResult.state)
    print('\n\n')
    
    startTime = time.time()
    astarResult, nodesRemoved = astar_search(puzzle,h=ManhattanDist)
    endTime = time.time() - startTime
    print('Manhattan Distance Heuristic')
    print('Total time taken: '+ str(endTime))
    print('Total nodes removed from frontier: '+str(nodesRemoved))
    print('Total length or # of tiles moved: '+str(len(astarResult.solution())))
    display(astarResult.state)
    print('\n\n')
    
    startTime = time.time()
    astarResult, nodesRemoved = astar_search(puzzle,h=maxManDist)
    endTime = time.time() - startTime
    print('max of the misplaced tile heuristic and the Manhattan distance heuristic')
    print('Total time taken: '+ str(endTime))
    print('Total nodes removed from frontier: '+str(nodesRemoved))
    print('Total length or # of tiles moved: '+str(len(astarResult.solution())))
    display(astarResult.state)

################################## QUESTION 3 ############################


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

        if index_blank_square  == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        else:
            if index_blank_square == 1:
                possible_actions.remove('UP')
                possible_actions.remove('RIGHT')
            if index_blank_square == 2:
                possible_actions.remove('LEFT')
                possible_actions.remove('DOWN')
            if index_blank_square == 4:
                possible_actions.remove('UP')
            if index_blank_square == 5:
                possible_actions.remove('RIGHT')
                possible_actions.remove('UP')
            if index_blank_square  == 6:
                possible_actions.remove('LEFT')
                possible_actions.remove('DOWN')
            if index_blank_square  == 7:
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

        if blank == 0:
            delta = {'DOWN': 2, 'RIGHT': 1}
        else:
            if blank == 1:
                delta = {'DOWN': 2,'LEFT': -1}
            if blank == 2:
                delta = {'UP': -2,'RIGHT': 1}
            if blank == 3:
                delta = {'UP': -2,'LEFT': -1, 'RIGHT':1, 'DOWN':3}
            if blank == 4:
                delta = {'RIGHT': 1,'DOWN': 3,'LEFT':-1}
            if blank == 5:
                delta = {'DOWN': 3,'LEFT': -1}
            if blank == 6:
                delta = {'UP': -3,'RIGHT': 1}
            if blank == 7:
                delta = {'UP': -3,'LEFT': -1,'RIGHT':1}
            if blank == 8:
                delta = {'UP': -3,'LEFT': -1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal
############################ Helper functions #####################
goalState = (1,2,3,4,5,6,7,8,0)
def make_rand_duckPuzzle():
    # instance of house puzzle in goal state - so we know its solvable
    puzzleEnd = DuckPuzzle(goalState)
    node = Node(puzzleEnd.initial)
    for i in range (20):
        for j in range(10):
            actions = puzzleEnd.actions(node.state)
            randomMoves  = random.randint(0,len(actions)-1)
            node.state = puzzleEnd.result(node.state, actions[randomMoves])
    return (DuckPuzzle(node.state))

def displayDuck(state):
    tempList=list(state)
    #print(type(tempList))
    #print(tempList)
    countBreak=0
    count=0
    for j in range(0,9):
        if(countBreak == 6):
            print('    ',end="")  
        if( tempList[count] == 0):
            print('*',end="   ")
        else:
            print(tempList[count], end="   ")
        count+=1
        countBreak+=1
        if(countBreak == 2):
            print()
        if(countBreak == 6):
            print()
        if(countBreak == 9):
            print()


############################## calculating distance helper functions
countFrontiersRemoved = 0

def astar_search_duck(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_duck(problem, lambda n: n.path_cost + h(n), display)

def best_first_graph_search_duck(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""

    global countFrontiersRemoved 
    countFrontiersRemoved = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        countFrontiersRemoved+=1
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

def misplaced_tiles(node):
    return sum(s != g for (s, g) in zip(node.state, goalState))


def manhattan_duck(node):
        state = node.state
        # indeces arrangement on goal sate 
        index_goal = {0: [2, 2], 8: [2, 1], 7: [2, 0], 6: [1, 3], 5: [1, 2], 4: [1, 1], 3: [1, 0], 2: [0, 1], 1: [0, 0]}
        index_state = {}
        index = [[0, 0], [0, 1], [1,0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2]]
        # indeces arrangement on the given state
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        mhd = 0
        # iterating 1 to 8, ignoring 0 (since it is a empty space)
        for i in range(1,9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        return mhd


def max_duck(node):
    return max(misplaced_tiles(node), manhattan_duck(node))

for i in range (0,2):
    print("\n\n\n \n\nRandom instance "+ str(i+1) + " of Duck Puzzle")
    puzzle=make_rand_duckPuzzle()
    displayDuck(puzzle.initial)
    ###########################################

    print("\nMisplaced Heuristic")
    
    start = time.time()
    solution = astar_search_duck(puzzle,h=misplaced_tiles)
    end = time.time() - start
    print("\nTotal Time: ", end)
    #print("Length of solution   : ",len(solution))
    print("Total Nodes, frontiers, Removed: ", countFrontiersRemoved)
    
    print("Total tiles moved: ",len(solution.solution()))
    displayDuck(solution.state)
    print(solution)
    ###########################################
    print("\nManhattan Distance Heuristic")
    
    start = time.time()
    solution = astar_search_duck(puzzle, h = manhattan_duck)
    end = time.time() - start
    print("\nTotal Time: ", end)
    #print("Length of solution   : ",len(solution))
    print("Total Nodes, frontiers, Removed: ", countFrontiersRemoved)
    
    print("Total tiles moved: ",len(solution.solution()))
    displayDuck(solution.state)
    print(solution)
    ###########################################

    print("\nMax Distance Heuristic")
    start = time.time()
    solution = astar_search_duck(puzzle, h = max_duck)
    end = time.time() - start
    print("\nTotal Time: ", end)
    #print("Length of solution   : ",len(solution))
    print("Total Nodes, frontiers, Removed: ", countFrontiersRemoved)
    
    print("Total tiles moved: ",len(solution.solution()))
    displayDuck(solution.state)
    print(solution)
    
