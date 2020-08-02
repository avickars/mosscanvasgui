#a1.py
import sys
#Please change the path, the follow path is Linhan's own path
sys.path.insert(0, 'C:\\Users\\john\\aima-python')
from search import *
import random
import time


#Question1: returns a new instance of an EightPuzzle problem with a random initial state that is solvable.
def make_rand_8puzzle():
    solvability = 0
    temp = list(range(0,9))

    while solvability == 0:    
        random.shuffle(temp)
        temp_puzzle = EightPuzzle(tuple(temp))
        solvability = temp_puzzle.check_solvability(tuple(temp))
        if solvability == 1:
            return temp_puzzle
    
    
    
#Question1: takes an 8-puzzle state as input and prints a neat and readable representation of it.
def  display(state):
    temp = list(state)
    for i in range(len(temp)):
        if temp[i] == 0:
            temp[i] = '*'
    print(temp[0], temp[1], temp[2])
    print(temp[3], temp[4], temp[5])
    print(temp[6], temp[7], temp[8])
    
    
#Question2: search using the Manhattan distance heuristic of 8-puzzle
def manhattan(node):
    init = node.state
    manDict = 0
    for i,item in enumerate(init):
        if item != 0:
            prow,pcol = int(i/ 3) , i % 3
            grow,gcol = int((item - 1) /3),(item - 1) % 3
            manDict += abs(prow-grow) + abs(pcol - gcol)
    
    return manDict


#Question2: the misplaced tile heuristic of 8-puzzle
def linear(node):
    return sum(s != g for (s, g) in zip(node.state, (1,2,3,4,5,6,7,8,0)))


#sQuestion2:The max of the misplaced tile heuristic and the Manhattan distance heuristic of 8-puzzle
def max_heuristic(node):
    score1 = manhattan(node)
    score2 = linear(node)
    return max(score1, score2)



def new_astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return new_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)



def new_best_first_graph_search(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    count = 0
    while frontier:
        node = frontier.pop()
        count+=1
        if problem.goal_test(node.state):
            print("The number of removed nodes: ",count) #print the number of removed nodes
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



#Test of 8-puzzle

#puzzle = EightPuzzle(tuple([0,7,6,2,1,3,4,5,8]))
puzzle = make_rand_8puzzle()
print("8-Puzzle:")
display(puzzle.initial)
print("Please wait...")
start_time = time.time()
#node = new_astar_search(puzzle) #The misplaced tile
node = new_astar_search(puzzle, manhattan) #the Manhattan distance
#node = new_astar_search(puzzle, max_heuristic) #The max of the misplaced tile heuristic and the Manhattan distance heuristic

elapsed_time = time.time() - start_time

print("elapsed time (in seconds):", elapsed_time, 's')

print("Solution: ",node.solution())
print("Solution path: ",node.path())
print("length of solution: ",len(node.path()) - 1)



# ______________________________________________________________________________

#Question3: class of Duck-puzzle
#Set -1 as the external space(the space cannot reach) in a 3*4 table
#Showed displays as the following:
#1   2  -1  -1
#3   4   5   6
#-1  7   8   0
class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, -1, -1, 3, 4, 5, 6, -1, 7, 8, 0)):
        super().__init__(initial, goal)
        
        
    def find_blank_square(self, state):
        return state.index(0)
    
    
    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        elif index_blank_square == 1:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        elif index_blank_square == 4:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif index_blank_square == 6:
            possible_actions.remove('UP')
        elif index_blank_square == 7:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        elif index_blank_square == 9:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif index_blank_square == 10:
            possible_actions.remove('DOWN')
        elif index_blank_square == 11:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')
        
        return possible_actions
    
    
    def result(self, state, action):
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        
        if blank < 4:
            delta = {'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
        elif blank >=4 and blank <= 7:
            delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
        elif blank > 7:
            delta = {'UP': -4,'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)
    
    
    def goal_test(self, state):
        return state == self.goal
    

    #No check_solvability in DuckPuzzle
    
        
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, (1, 2, -1, -1, 3, 4, 5, 6, -1, 7, 8, 0)))
 # ______________________________________________________________________________   



#Question3: Search using the Manhattan distance heuristic of Duck-puzzle
def dmanhattan(node):
    init = node.state
    manDict = 0
    for i,item in enumerate(init):
        if item != 0 and item != -1:
            prow,pcol = int(i/ 4) , i % 4
            if item == 1:
                grow,gcol = 0,0
            elif item == 2:
                grow,gcol = 0,1
            elif item == 3:
                grow,gcol = 1,0
            elif item == 4:
                grow,gcol = 1,1
            elif item == 5:
                grow,gcol = 1,2
            elif item == 6:
                grow,gcol = 1,3
            elif item == 7:
                grow,gcol = 2,1
            elif item == 8:
                grow,gcol = 2,2
                
            manDict += abs(prow-grow) + abs(pcol - gcol)
    
    return manDict



#Question3: The misplaced tile heuristic of Duck-puzzle
def dlinear(node):
    return sum(s != g for (s, g) in zip(node.state, (1, 2, -1, -1, 3, 4, 5, 6, -1, 7, 8, 0)))



#Question3: The max of the misplaced tile heuristic and the Manhattan distance heuristic of Duck-puzzle
def dmax_heuristic(node):
    score1 = dmanhattan(node)
    score2 = dlinear(node)
    return max(score1, score2)


#Test of Duck-puzzle
puzzle = DuckPuzzle(tuple([2,0,-1,-1,1,3,8,4,-1,7,5,6]))
print("\nDuck-Puzzle:")
start_time = time.time()
#node = new_astar_search(puzzle) #The misplaced tile
node = new_astar_search(puzzle, dmanhattan) #The Manhattan distance
#node = new_astar_search(puzzle, dmax_heuristic) #The max of the misplaced tile heuristic and the Manhattan distance heuristic

elapsed_time = time.time() - start_time

print("elapsed time (in seconds):", elapsed_time, 's')

print("Solution: ",node.solution()) 
print("Solution path: ",node.path())
print("length of solution: ",len(node.path()) - 1)


