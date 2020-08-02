# a1.py

#--------------------------------------------------------------------RITVIK SHAH----------------------------------------------------------
#--------------------------------------------------------------------301366819-------------------------------------------------------------

from search import *
import random
import time


goal = (1,2,3,4,5,6,7,8,0) #declared globally so can be used throughout the file
# 1 ------------------------------------------------------------------------ Helper Functions ----------------------------------------------------------------------------------


def make_rand_8puzzle():
    solvable = False #boolean to track status of puzzle
    init_state = [0,1,2,3,4,5,6,7,8] #starting state
    while(solvable == False): #loop shuffles until puzzle is solvable
        random.shuffle(init_state) #shuffle using the random library
        puzzle_state = EightPuzzle(init_state) #generate puzzle

        solvable = puzzle_state.check_solvability(init_state) #check_solvability takes array as argument
    init_state_tuple = tuple(init_state) 
    return init_state_tuple


# A function that prints the Eight Puzzle problem initial state
def display(state):
    for i in range(9):
        if state[i] == 0:
            print("*", end = " ")
        else:
            print(state[i], end = " ")
        if(i + 1) % 3 == 0:
            print(" ")

#arbitrary_puzzle = make_rand_8puzzle()
#puzzle = EightPuzzle(arbitrary_puzzle)
#display(arbitrary_puzzle)

#2 ------------------------------------------------------------------------ Comparing Algorithms-----------------------------------------------------------------------------

#calculate number of misplaced tiles in relation to goal state:
def misplaced_tiles(node):
    return sum(s != 0  and s != g for (s, g) in zip(node.state, goal)) #obtained from search.py


def manhattanHeuristic(node): #primarily inspired by test_search.py
    mhd = 0
    init_state = node.state
    
    #goal state visualization:
    # 1 2 3
    # 4 5 6
    # 7 8 0
    
    # number -> (row,col)
    # 1 -> (0,0)
    # 2 -> (0,1)

    #below is dict implementation of goal state inspired by test_search.py and https://www.csee.umbc.edu/courses/undergraduate/471/spring17/01/code/python/p8.py
    current_state = {}
    goal_state = {1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1], 0:[2,2]}
    index = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    
    for i in range(len(init_state)):
        current_state[init_state[i]] = index[i]

    #zero is not included in range because function does not overestimate
    for i in range(8):
        for j in range(2):
            mhd = abs(goal_state[i][j] - current_state[i][j]) + mhd

    return mhd


# max of misplaced tile and manhattan using python's inbuilt max function:
def max_misplaced_manhattan(node):
    misplacedTiles = misplaced_tiles(node)
    manhattanDistance = manhattanHeuristic(node)
    return max(misplacedTiles,manhattanDistance)

#modified best first seach, inspired from search.py
def modified_bfs(problem, f, display = False):
    f = memoize(f,'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    nodes_removed_frontier = 0
    while frontier:
        node = frontier.pop()
        nodes_removed_frontier += 1 #keep track of nodes removed
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, nodes_removed_frontier]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

#modified astar search inspired from search.py:
def astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return modified_bfs(problem, lambda n: n.path_cost + h(n), display)

#def algorithm_statistics_EP():

for i in range(12):

    init_puzzle = make_rand_8puzzle() #create instance

    puzz = EightPuzzle(init_puzzle) #converts to an object

    display(init_puzzle) #print initial state

    print()

    print("Statistics for misplaced tile: ")
    start_time = time.time()
    result_misplaced = astar_search(puzz, h = misplaced_tiles)
    time_taken = time.time() - start_time

    print('Time Taken: ', time_taken)
    print()
    print('No. of steps taken (length of solution):', result_misplaced[0].path_cost) #path_cost gives length directly compared to solution()
    print()
    print('No. of nodes removed from frontier:', result_misplaced[1])

    print()

    print("Statistics for manhattan heuristic: ")
    start_time = time.time()
    result_manhattan = astar_search(puzz, h = manhattanHeuristic)
    time_taken = time.time() - start_time

    print('Time Taken: ', time_taken)
    print()
    print('No. of steps taken (length of solution):', result_manhattan[0].path_cost) #path_cost gives length directly compared to solution()
    print()
    print('No. of nodes removed from frontier:', result_manhattan[1])

    print()

    print("Statistics for max of misplaced & manhattan: ")
    start_time = time.time()
    result_max = astar_search(puzz, h =  max_misplaced_manhattan)
    time_taken = time.time() - start_time

    print('Time Taken: ', time_taken)
    print()
    print('No. of steps taken (length of solution):', result_max[0].path_cost) #path_cost gives length directly compared to solution()
    print()
    print('No. of nodes removed from frontier:', result_max[1])
    #return

#algorithm_statistics_EP()
#3 -----------------------------------------------------------------------------------------Duck Puzzle-----------------------------------------------------------

#-----------------------------------------FOR DUCK PUZZLE I TRIED TO MODIFY & IMPLEMENT AS MANY OF THE METHODS AS I COULD-----------------------------------------
# ----------------------------------------HOWEVER, SINCE I COULD NOT FIGURE OUT ONE METHOD, I COULD NOT GET IT TO WORK--------------------------------------------

# inspired from the EightPuzzle class in search.py)
class duck_puzzle():
    def __init__(self, initial, goal=(1,2,3,4,5,6,7,8,0)):
        super().__init__(initial,goal)

    def find_blank_square(self,state):
        return state.index(0)

    #actiions that can be executed in a given state:
    def actions(self,state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        #0 1
        #2 3 4 5  ==> 0, 2 and 6 cannot move left because it goes off the board
        #  6 7 8

        #change actions because of different structure of duck puzzle:

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')

        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')

        if index_blank_square == 2 or index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions


    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)

        #change in index:

        if blank == 3:
            delta = {'UP': -2, 'DOWN' : 3, 'LEFT' : -1, 'RIGHT' :1}

        elif blank < 3:
            delta = {'UP': -2, 'DOWN' : 3, 'LEFT' : -1, 'RIGHT' :1}
        
        else:
            delta = {'UP': -3, 'DOWN' : 3, 'LEFT' : -1, 'RIGHT' :1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)
        
    def goal_test(self,state):
        return state == self.goal

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

def random_duckpuzzle():
    # we can avoid creating a new check_solvability function by creating a puzzle
    #based on the possible actions
    puzzle_instance = duck_puzzle((0,1,2,3,4,5,6,7,8))
    current = Node(puzzle_instance.initial)

    return current



#the heuristic functions below were coped from aboved and modified:
#calculate number of misplaced tiles in relation to goal state:
def misplaced_tiles(node):
    goal = (1,2,3,4,5,6,7,8,9,0)
    return sum(s != g for (s, g) in zip(node.state, goal)) #obtained from search.py


def manhattanHeuristic(node): #primarily inspired by test_search.py
    mhd = 0
    init_state = node.state
    
    #goal state visualization:
        #0 1
        #2 3 4 5  
        #  6 7 8
    
    # number -> (row,col)
    # 0 -> (0,0)
    # 1 -> (0,1)

    #below is dict implementation of goal state inspired by test_search.py and https://www.csee.umbc.edu/courses/undergraduate/471/spring17/01/code/python/p8.py
    current_state = {}
    goal_state = {0:[0,0], 1:[0,1], 2:[2,0], 3:[2,1], 4:[2,2], 5:[2,3], 6:[3,1], 7:[3,2], 8:[3,3]}
    index = [[0,0],[0,1],[2,0],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]]
    
    for i in range(len(init_state)):
        current_state[init_state[i]] = index[i]

    #zero is not included in range because function does not overestimate
    for i in range(8):
        for j in range(2):
            mhd = abs(goal_state[i][j] - current_state[i][j]) + mhd

    return mhd


# max of misplaced tile and manhattan:
def max_misplaced_manhattan(node):
    misplacedTiles = misplaced_tiles(node)
    manhattanDistance = manhattanHeuristic(node)
    return max(misplacedTiles,manhattanDistance)


def algorithm_statistics_DP():

    for i in range(12):

        init_puzzle = random_duckpuzzle() #create instance

        puzz = duck_puzzle(init_puzzle) #converts to an object


        print()

        print("Statistics for misplaced tile: ")
        start_time = time.time()
        result_misplaced = astar_search(puzz, h = misplaced_tiles)
        time_taken = time.time() - start_time

        print('Time Taken: ', time_taken)
        print()
        print('No. of steps taken (length of solution):', result_misplaced[0].path_cost) #path_cost gives length directly compared to solution()
        print()
        print('No. of nodes removed from frontier:', result_misplaced[1])

        print()

        print("Statistics for manhattan heuristic: ")
        start_time = time.time()
        result_manhattan = astar_search(puzz, h = manhattanHeuristic)
        time_taken = time.time() - start_time

        print('Time Taken: ', time_taken)
        print()
        print('No. of steps taken (length of solution):', result_manhattan[0].path_cost) #path_cost gives length directly compared to solution()
        print()
        print('No. of nodes removed from frontier:', result_manhattan[1])

        print()

        print("Statistics for max of misplaced & manhattan: ")
        start_time = time.time()
        result_max = astar_search(puzz, h =  max_misplaced_manhattan)
        time_taken = time.time() - start_time

        print('Time Taken: ', time_taken)
        print()
        print('No. of steps taken (length of solution):', result_max[0].path_cost) #path_cost gives length directly compared to solution()
        print()
        print('No. of nodes removed from frontier:', result_max[1])

        return


#algorithm_statistics_DP()
