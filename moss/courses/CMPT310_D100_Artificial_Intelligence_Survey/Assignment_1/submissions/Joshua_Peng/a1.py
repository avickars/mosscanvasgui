from search import *
import random
import time
#301340929
#Joshua Peng
#Cmpt 310 Assignment 1

#Did research about concepts through these links but all code was written by me unless it was from aima-python
#https://www.andrew.cmu.edu/course/15-121/labs/HW-7%20Slide%20Puzzle/lab.html
#https://blog.goodaudience.com/solving-8-puzzle-using-a-algorithm-7b509c331288
#Also some clarifications about questions was given by TA

#Modified from eightPuzzle
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

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta = {}
        if (blank <= 2):
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        if (blank == 3):
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if (blank >= 4):
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

#modified from aima-python
def astar_search_compare(problem, h=None, m= None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    m = memoize(m or problem.m, 'm')
    return best_first_graph_search_modified(problem, lambda n: max(n.path_cost + h(n), n.path_cost + m(n)), display)

#modified from aima-python
def astar_search_modified(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_modified(problem, lambda n: n.path_cost + h(n), display)

#modified from aima-python
def best_first_graph_search_modified(problem, f, display=False):
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
    prevNode = Node(problem.initial)
    counter = 0
    while frontier:
        node = frontier.pop()
        if (node.path_cost > prevNode.path_cost):
            #print(node.path())
            counter+= 1


            counter -= (node.path_cost - prevNode.path_cost)
        if problem.goal_test(node.state):
            if display:
                print("The number of nodes moved is " + str(len(node.path())-1))
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


#Q1
def make_rand_8puzzle():
    spots = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    eightPuzzle = EightPuzzle(spots)
    for i in range(0,random.randint(101,120)):
        actions = eightPuzzle.actions(spots)
        choice = random.choice(actions)
        spots = eightPuzzle.result(spots, choice)
    eightPuzzle.initial = spots
    return eightPuzzle

def display(state):
    for i in range(0,3):
        if (state[i] == 0):
            print ("*", end= " ")
        else:
            print (state[i], end=" ")
    print()
    for i in range(3,6):
        if (state[i] == 0):
            print ("*", end= " ")
        else:
            print (state[i], end=" ")
    print()
    for i in range (6,9):
        if (state[i] == 0):
            print ("*", end= " ")
        else:
            print (state[i], end=" ")
    print()

#Q2A

def A_Heuristic(eightPuzzle):
    start_time = time.time()
    eightPuzzle.initial = tuple(eightPuzzle.initial)
    astar_search_modified(eightPuzzle,eightPuzzle.h,True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    return

#Q2B
def manHatton(Nodestate):
    initialState = Nodestate.state
    manhattanDistance = 0
    index = 0
    for i in initialState:
        if (i == 0):
            index+=1
        else:
            currentPosX = index//3
            currentPosY = index%3

            goalPosX = (i-1) // 3
            goalPosY = (i-1)%3
            index+=1
            manhattonVal = (abs(currentPosX-goalPosX) + abs(currentPosY - goalPosY))
            manhattanDistance += manhattonVal

    return manhattanDistance

def A_Manhattan_solver(eightPuzzle):
    start_time = time.time()
    eightPuzzle.initial = tuple(eightPuzzle.initial)
    astar_search_modified(eightPuzzle,manHatton,True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    return
#Q2C
def A_Both_solver(eightPuzzle):
    start_time = time.time()
    eightPuzzle.initial = tuple (eightPuzzle.initial)
    astar_search_compare(eightPuzzle,eightPuzzle.h,manHatton, True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')

#Q3 Set Up
def make_rand_duckpuzzle():
    spots = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    duckPuzzle = DuckPuzzle(spots)
    for i in range(0,random.randint(201,220)):
        actions = duckPuzzle.actions(spots)
        choice = random.choice(actions)
        spots = duckPuzzle.result(spots, choice)
    duckPuzzle.initial = spots
    return duckPuzzle


def display_Duck(state):
    for i in range(0,2):
        if (state[i] == 0):
            print ("*", end= " ")
        else:
            print (state[i], end=" ")
    print()
    for i in range(2,6):
        if (state[i] == 0):
            print ("*", end= " ")
        else:
            print (state[i], end=" ")
    print()
    print(" ", end = " ")
    for i in range (6,9):
        if (state[i] == 0):
            print ("*", end= " ")
        else:
            print (state[i], end=" ")
    print()



#Q3A

def Duck_Heuristic(duckPuzzle):
    start_time = time.time()
    duckPuzzle.initial= tuple(duckPuzzle.initial)
    astar_search_modified(duckPuzzle,duckPuzzle.h,True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    return

#Q3B
def Duck_ManHatton(nodeState):
    initialState = nodeState.state
    manhattanDistance = 0

    index = 0
    for i in initialState:
        if (i == 0):
            index+=1
        elif(index <= 3):
            currentPosX = index//2
            currentPosY = index%2

            goalPosX = (i-1) // 2
            goalPosY = (i-1)%2
            index+=1
            manhattonVal = (abs(currentPosX-goalPosX) + abs(currentPosY - goalPosY))
            manhattanDistance += manhattonVal

        else:

            currentPosX = index//3
            currentPosY = (index%3) + 1

            goalPosX = (i-1) // 3
            goalPosY = ((i-1)%3) + 1
            index+=1
            manhattonVal = (abs(currentPosX-goalPosX) + abs(currentPosY - goalPosY))
            manhattanDistance += manhattonVal

    return manhattanDistance

def Duck_Manhattan_Solver(duckPuzzle):
    start_time = time.time()
    duckPuzzle.initial= tuple(duckPuzzle.initial)
    astar_search_modified(duckPuzzle,Duck_ManHatton,True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    return

#Q3C
def A_Duck_Both_solver(DuckPuzzle):
    start_time = time.time()
    eightPuzzle.initial = tuple (eightPuzzle.initial)
    astar_search_compare(DuckPuzzle,DuckPuzzle.h,Duck_ManHatton, True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')


#Main function that initializes all the puzzles

eightPuzzle = make_rand_8puzzle()
eightPuzzle2 = make_rand_8puzzle()
eightPuzzle3 = make_rand_8puzzle()
eightPuzzle4 = make_rand_8puzzle()
eightPuzzle5 = make_rand_8puzzle()
eightPuzzle6 = make_rand_8puzzle()
eightPuzzle7 = make_rand_8puzzle()
eightPuzzle8 = make_rand_8puzzle()
eightPuzzle9 = make_rand_8puzzle()
eightPuzzle10 = make_rand_8puzzle()


duckPuzzle = make_rand_duckpuzzle()
duckPuzzle2 = make_rand_duckpuzzle()
duckPuzzle3 = make_rand_duckpuzzle()
duckPuzzle4 = make_rand_duckpuzzle()
duckPuzzle5 = make_rand_duckpuzzle()
duckPuzzle6 = make_rand_duckpuzzle()
duckPuzzle7 = make_rand_duckpuzzle()
duckPuzzle8 = make_rand_duckpuzzle()
duckPuzzle9 = make_rand_duckpuzzle()
duckPuzzle10 = make_rand_duckpuzzle()

#Running the algorithms and solving the puzzles

print("The current puzzle is: ")
display((eightPuzzle.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
A_Heuristic(eightPuzzle)
#Manhattan approach

print("Solving with Heuristic Approach")
A_Manhattan_solver(eightPuzzle)
#Max value approach
print("Solving with Max Value Approach")
A_Both_solver(eightPuzzle)

print("----------------------------------")

print("The current puzzle is: ")
display((eightPuzzle2.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
A_Heuristic(eightPuzzle2)
#Manhattan approach
print("Solving with Heuristic Approach")
A_Manhattan_solver(eightPuzzle2)
#Max value approach
print("Solving with Max Value Approach")
A_Both_solver(eightPuzzle2)

print("----------------------------------")

print("The current puzzle is: ")
display((eightPuzzle3.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
A_Heuristic(eightPuzzle3)
#Manhattan approach
print("Solving with Heuristic Approach")
A_Manhattan_solver(eightPuzzle3)
#Max value approach
print("Solving with Max Value Approach")
A_Both_solver(eightPuzzle3)

print("----------------------------------")

print("The current puzzle is: ")
display((eightPuzzle4.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
A_Heuristic(eightPuzzle4)
#Manhattan approach
print("Solving with Heuristic Approach")
A_Manhattan_solver(eightPuzzle4)
#Max value approach
print("Solving with Max Value Approach")
A_Both_solver(eightPuzzle4)

print("----------------------------------")

print("The current puzzle is: ")
display((eightPuzzle5.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
A_Heuristic(eightPuzzle5)
#Manhattan approach
print("Solving with Heuristic Approach")
A_Manhattan_solver(eightPuzzle5)
#Max value approach
print("Solving with Max Value Approach")
A_Both_solver(eightPuzzle5)

print("----------------------------------")

print("The current puzzle is: ")
display((eightPuzzle6.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
A_Heuristic(eightPuzzle6)
#Manhattan approach
print("Solving with Heuristic Approach")
A_Manhattan_solver(eightPuzzle6)
#Max value approach
print("Solving with Max Value Approach")
A_Both_solver(eightPuzzle6)

print("----------------------------------")

print("The current puzzle is: ")
display((eightPuzzle7.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
A_Heuristic(eightPuzzle7)
#Manhattan approach
print("Solving with Heuristic Approach")
A_Manhattan_solver(eightPuzzle7)
#Max value approach
print("Solving with Max Value Approach")
A_Both_solver(eightPuzzle7)

print("----------------------------------")

print("The current puzzle is: ")
display((eightPuzzle8.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
A_Heuristic(eightPuzzle8)
#Manhattan approach
print("Solving with Heuristic Approach")
A_Manhattan_solver(eightPuzzle8)
#Max value approach
print("Solving with Max Value Approach")
A_Both_solver(eightPuzzle8)

print("----------------------------------")

print("The current puzzle is: ")
display((eightPuzzle9.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
A_Heuristic(eightPuzzle9)
#Manhattan approach
print("Solving with Heuristic Approach")
A_Manhattan_solver(eightPuzzle9)
#Max value approach
print("Solving with Max Value Approach")
A_Both_solver(eightPuzzle9)

print("----------------------------------")

print("The current puzzle is: ")
display((eightPuzzle10.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
A_Heuristic(eightPuzzle10)
#Manhattan approach
print("Solving with Heuristic Approach")
A_Manhattan_solver(eightPuzzle10)
#Max value approach
print("Solving with Max Value Approach")
A_Both_solver(eightPuzzle10)

print("----------------------------------")


print("The current puzzle is: ")
display_Duck(duckPuzzle.initial)

#Heuristic approach
print("Solving with Heuristic Approach")
Duck_Heuristic(duckPuzzle)
#Manhattan approach
print("Solving with Heuristic Approach")
Duck_Manhattan_Solver(duckPuzzle)
#Max value approach
print("Solving with Max Value Approach")
A_Duck_Both_solver(duckPuzzle)

print("----------------------------------")

print("The current puzzle is: ")
display_Duck((duckPuzzle2.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
Duck_Heuristic(duckPuzzle2)
#Manhattan approach
print("Solving with Heuristic Approach")
Duck_Manhattan_Solver(duckPuzzle2)
#Max value approach
print("Solving with Max Value Approach")
A_Duck_Both_solver(duckPuzzle2)

print("----------------------------------")

print("The current puzzle is: ")
display_Duck((duckPuzzle3.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
Duck_Heuristic(duckPuzzle3)
#Manhattan approach
print("Solving with Heuristic Approach")
Duck_Manhattan_Solver(duckPuzzle3)
#Max value approach
print("Solving with Max Value Approach")
A_Duck_Both_solver(duckPuzzle3)

print("----------------------------------")

print("The current puzzle is: ")
display_Duck((duckPuzzle4.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
Duck_Heuristic(duckPuzzle4)
#Manhattan approach
print("Solving with Heuristic Approach")
Duck_Manhattan_Solver(duckPuzzle4)
#Max value approach
print("Solving with Max Value Approach")
A_Duck_Both_solver(duckPuzzle4)

print("----------------------------------")

print("The current puzzle is: ")
display_Duck((duckPuzzle5.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
Duck_Heuristic(duckPuzzle5)
#Manhattan approach
print("Solving with Heuristic Approach")
Duck_Manhattan_Solver(duckPuzzle5)
#Max value approach
print("Solving with Max Value Approach")
A_Duck_Both_solver(duckPuzzle5)

print("----------------------------------")

print("The current puzzle is: ")
display_Duck((duckPuzzle6.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
Duck_Heuristic(duckPuzzle6)
#Manhattan approach
print("Solving with Heuristic Approach")
Duck_Manhattan_Solver(duckPuzzle6)
#Max value approach
print("Solving with Max Value Approach")
A_Duck_Both_solver(duckPuzzle6)

print("----------------------------------")

print("The current puzzle is: ")
display_Duck((duckPuzzle7.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
Duck_Heuristic(duckPuzzle7)
#Manhattan approach
print("Solving with Heuristic Approach")
Duck_Manhattan_Solver(duckPuzzle7)
#Max value approach
print("Solving with Max Value Approach")
A_Duck_Both_solver(duckPuzzle7)

print("----------------------------------")

print("The current puzzle is: ")
display_Duck((duckPuzzle8.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
Duck_Heuristic(duckPuzzle8)
#Manhattan approach
print("Solving with Heuristic Approach")
Duck_Manhattan_Solver(duckPuzzle8)
#Max value approach
print("Solving with Max Value Approach")
A_Duck_Both_solver(duckPuzzle8)

print("----------------------------------")

print("The current puzzle is: ")
display_Duck((duckPuzzle9.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
Duck_Heuristic(duckPuzzle9)
#Manhattan approach
print("Solving with Heuristic Approach")
Duck_Manhattan_Solver(duckPuzzle9)
#Max value approach
print("Solving with Max Value Approach")
A_Duck_Both_solver(duckPuzzle9)

print("----------------------------------")

print("The current puzzle is: ")
display_Duck((duckPuzzle10.initial))

#Heuristic approach
print("Solving with Heuristic Approach")
Duck_Heuristic(duckPuzzle10)
#Manhattan approach
print("Solving with Heuristic Approach")
Duck_Manhattan_Solver(duckPuzzle10)
#Max value approach
print("Solving with Max Value Approach")
A_Duck_Both_solver(duckPuzzle10)

print("----------------------------------")








