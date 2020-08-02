# a1.py

from search import *
from timeit import default_timer #https://www.programcreek.com/python/example/12982/timeit.default_timer

import random #https://docs.python.org/3/library/random.html

# ...


""" Write a function called make_rand_8puzzle() that returns a new instance of an EightPuzzle problem with a random 
initial state that is solvable. Note that EightPuzzle has a method called check_solvability that you should use t
o help ensure your initial state is solvable. """

#ideas taken from https://github.com/MaxWong03/aima-python/blob/master/a1.py

def make_rand_8puzzle():
    puzzlenumbers = (1, 2, 3, 4, 5, 6, 7, 8, 0)										#state numbers

    temp = puzzlenumbers															#storing these in a temp variable to use for alteration

    puzzleinstance = EightPuzzle(puzzlenumbers) 									#creating a new instance of the EightPuzzle

    for i in range(0,8):
        tempaction = puzzleinstance.actions(temp) 									#from search.py
        action = random.choice(tempaction) 										    #from search.py
        temp = puzzleinstance.result(temp, action)    								#creating a new instance of the EightPuzzle

    puzzleinstance = EightPuzzle(temp)												#create a new instance


    while (puzzleinstance.check_solvability(puzzleinstance.initial) == False):		#from search.py, repeat till solved
	    puzzlenumbers = (1, 2, 3, 4, 5, 6, 7, 8, 0)

	    temp = puzzlenumbers

	    puzzleinstance = EightPuzzle(puzzlenumbers)

	    for i in range(0,8):
	        tempaction = puzzleinstance.actions(temp)
	        action = random.choice(tempaction)
	        temp = puzzleinstance.result(temp, action)

	    print("working on making it solvable")
	    puzzleinstance = EightPuzzle(temp)
    display(temp)
    print("solved")

    return puzzleinstance

"""Write a function called display(state) that takes an 8-puzzle state (i.e. a tuple that is a permutation 
of (0, 1, 2, …, 8)) as input and prints a neat and readable representation of it. 0 is the 
blank, and should be printed as a * character."""

def display(state):																	#idea taken from https://github.com/MaxWong03/aima-python/blob/master/a1.py
    statedisplay = list(state)         														

    for i in range(0, 9):      														
        if statedisplay[i] == 0:
            statedisplay[i] = "*"        														

    state = tuple(statedisplay)                                                     #need to tuple again for changes to register
    print(state[0], state[1], state[2])   											
    print(state[3], state[4], state[5])
    print(state[6], state[7], state[8])



def astar_search(problem, h=None, display=False):									#taken from "search.py"
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def astar_search_manhattan(problem, h=None, display=False):							#taken from "search.py" but updated for heurisitic_manhattan
    h = memoize(h or problem.heuristic_manhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def astar_search_max(problem, h=None, display=False):								#taken from "search.py" but updated for heuristic_max
    h = memoize(h or problem.heuristic_max, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def best_first_graph_search(problem, f, display=False):								#taken from search.py but updated for tilesmoved and nodesremoved
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    tilesmoved = 0;																	#keep count of tiles moved
    nodesremoved = 0;																#keep count of nodes removed

    while frontier:
        node = frontier.pop()

        tilesmoved = tilesmoved + 1

        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")

            print("Length of the Solution (number of tiles moved): ", tilesmoved)
            print("Total number of nodes removed: ", nodesremoved)

            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]

                    nodesremoved = nodesremoved + 1

                    frontier.append(child) 

    return None

class EightPuzzle(Problem):															#taken from "search.py"

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):


        return state.index(0)

    def actions(self, state):


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

        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):


        return state == self.goal

    def check_solvability(self, state):


        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):


        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def heuristic_manhattan(self, node):  											#idea from https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game
        tempstate = node.state
        
        copystate = list(tempstate)
        manstate = 0
        
        for i, item in enumerate(copystate):
            if item:
                prev_row,prev_col = int(i/ 3) , i % 3
                goal_row,goal_col = int(item /3),item % 3
                manstate += abs(prev_row-goal_row) + abs(prev_col - goal_col)
        
        return manstate

    def heuristic_max(self, node):      											#idea from https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game
        tempstate = node.state

        copystate = list(tempstate)
        manstate = 0

        for i, item in enumerate(copystate):
            if item:
                prev_row,prev_col = int(i/ 3) , i % 3
                goal_row,goal_col = int(item /3),item % 3
                manstate += abs(prev_row-goal_row) + abs(prev_col - goal_col)

        finalstate = sum(s != g for (s, g) in zip(copystate, self.goal))

        return max(manstate,finalstate)


print("============================================")
print("============================================")
print("=============EIGHT PUZZLE===================")
print("============================================")
print("============================================")

eighttest = list()                                                                       #This list will be used for the heuristics

print("Test: 1")
test1 = make_rand_8puzzle()
eighttest.append(test1)
print("\n")

print("Test: 2")
test2 = make_rand_8puzzle()
eighttest.append(test2)
print("\n")

print("Test: 3")
test3 = make_rand_8puzzle()
eighttest.append(test3)
print("\n")

print("Test: 4")
test4 = make_rand_8puzzle()
eighttest.append(test4)
print("\n")

print("Test: 5")
test5 = make_rand_8puzzle()
eighttest.append(test5)
print("\n")

print("Test: 6")
test6 = make_rand_8puzzle()
eighttest.append(test6)
print("\n")

print("Test: 7")
test7 = make_rand_8puzzle()
eighttest.append(test7)
print("\n")

print("Test: 8")
test8 = make_rand_8puzzle()
eighttest.append(test8)
print("\n")

print("Test: 9")
test9 = make_rand_8puzzle()
eighttest.append(test9)
print("\n")

print("Test: 10")
test10 = make_rand_8puzzle()
eighttest.append(test10)
print("\n")


print("HEURISTIC")
print("============================================")
print("============================================")

eighttestlist = 1

for i in eighttest:
    print("Test:", eighttestlist)
    starttime = default_timer()

    astar_search(i)

    endtime = default_timer()

    eighttestlist+=1

    print("Time in seconds: ", endtime - starttime)
    print("\n")


print("MANHATTAN HEURISTIC")
print("============================================")
print("============================================")

eighttestlist = 1

for i in eighttest:
    print("Test:", eighttestlist)
    starttime = default_timer()

    astar_search_manhattan(i)

    endtime = default_timer()

    eighttestlist+=1

    print("Time in seconds: ", endtime - starttime)
    print("\n")


print("MAX HEURISTIC")
print("============================================")
print("============================================")

eighttestlist = 1

for i in eighttest:
    print("Test:", eighttestlist)
    starttime = default_timer()

    astar_search_max(i)

    endtime = default_timer()

    eighttestlist+=1

    print("Time in seconds: ", endtime - starttime)
    print("\n")

print("Eight tests are all done!")
print("============================================")
print("============================================")
print("============================================")

print("\n")



# All DuckPuzzle content here
def make_rand_duckpuzzle():
    puzzlenumbers = (1, 2, 3, 4, 5, 6, 7, 8, 0)                                     #state numbers

    temp = puzzlenumbers                                                            #storing these in a temp variable to use for alteration

    puzzleinstance = DuckPuzzle(puzzlenumbers)                                     #creating a new instance of the EightPuzzle

    for i in range(0,8):
        tempaction = puzzleinstance.actions(temp)                                  #from search.py
        action = random.choice(tempaction)                                         #from search.py
        temp = puzzleinstance.result(temp, action)                                 #creating a new instance of the EightPuzzle

    puzzleinstance = DuckPuzzle(temp)                                              #create a new instance


    while (puzzleinstance.check_solvability(puzzleinstance.initial) == False):      #from search.py, repeat till solved
        puzzlenumbers = (1, 2, 3, 4, 5, 6, 7, 8, 0)

        temp = puzzlenumbers

        puzzleinstance = DuckPuzzle(puzzlenumbers)

        for i in range(0,8):
            tempaction = puzzleinstance.actions(temp)
            action = random.choice(tempaction)
            temp = puzzleinstance.result(temp, action)

        print("working on making it solvable")
        display(temp)
        puzzleinstance = DuckPuzzle(temp)
    display(temp)
    print("solved")

    return puzzleinstance


def display(state):                                                                 #idea taken from https://github.com/MaxWong03/aima-python/blob/master/a1.py
    statedisplay = list(state)                                                                 

    for i in range(0, 9):                                                           
        if statedisplay[i] == 0:
            statedisplay[i] = "*"                                                                

    state = tuple(statedisplay)                                                     #need to tuple again for changes to register
    print(state[0], state[1], " ")                                             
    print(state[2], state[3], state[4], state[5])
    print(" ", state[6], state[7], state[8])



def astar_search(problem, h=None, display=False):                                   #taken from "search.py"

    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def astar_search_manhattan(problem, h=None, display=False):                         #taken from "search.py" but updated for heurisitic_manhattan

    h = memoize(h or problem.heuristic_manhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def astar_search_max(problem, h=None, display=False):                               #taken from "search.py" but updated for heuristic_max

    h = memoize(h or problem.heuristic_max, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def best_first_graph_search(problem, f, display=False):                             #taken from search.py but updated for tilesmoved and nodesremoved

    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    tilesmoved = 0;                                                                 #keep count of tiles moved
    nodesremoved = 0;                                                               #keep count of nodes removed

    while frontier:
        node = frontier.pop()

        tilesmoved = tilesmoved + 1

        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")

            print("Length of the Solution (number of tiles moved): ", tilesmoved)
            print("Total number of nodes removed: ", nodesremoved)

            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    nodesremoved = nodesremoved + 1
                    frontier.append(child) 

    return None

class DuckPuzzle(Problem):                                                         #ideas from https://github.com/MaxWong03/aima-python/blob/master/a1.py


    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):

        return state.index(0)

    def actions(self, state):


        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        cantMoveUp = (1,2,5,6) #tuple that contains squares that can't move up
        cantMoveDown = (3,6,7,8) #tuple that contains squares that can't move down
        cantMoveLeft = (1,3,7) #tuple that contains squares that can't move left
        cantMoveRight = (2,6,8) #tuples that contains squares that can't move right 

        if index_blank_square in cantMoveLeft:
            possible_actions.remove('LEFT')
        if index_blank_square in cantMoveUp:
            possible_actions.remove('UP')
        if index_blank_square in cantMoveRight:
            possible_actions.remove('RIGHT')
        if index_blank_square in cantMoveDown:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):


        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):


        return state == self.goal

    def check_solvability(self, state):


        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):


        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def heuristic_manhattan(self, node):                                            #idea from https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game
        tempstate = node.state
        
        copystate = list(tempstate)
        manstate = 0
        
        for i, item in enumerate(copystate):
            if item:
                prev_row,prev_col = int(i/ 3) , i % 3
                goal_row,goal_col = int(item /3),item % 3
                manstate += abs(prev_row-goal_row) + abs(prev_col - goal_col)
        
        return manstate

    def heuristic_max(self, node):                                                  #idea from https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game
        tempstate = node.state

        copystate = list(tempstate)
        manstate = 0

        for i, item in enumerate(copystate):
            if item:
                prev_row,prev_col = int(i/ 3) , i % 3
                goal_row,goal_col = int(item /3),item % 3
                manstate += abs(prev_row-goal_row) + abs(prev_col - goal_col)

        finalstate = sum(s != g for (s, g) in zip(copystate, self.goal))

        return max(manstate,finalstate)



ducktest = list()																		#This list will be used for the heuristics

print("============================================")
print("============================================")
print("=============DUCK PUZZLE====================")
print("============================================")
print("============================================")

print("Test: 1")
test1 = make_rand_duckpuzzle()
ducktest.append(test1)
print("\n")

print("Test: 2")
test2 = make_rand_duckpuzzle()
ducktest.append(test2)
print("\n")

print("Test: 3")
test3 = make_rand_duckpuzzle()
ducktest.append(test3)
print("\n")

print("Test: 4")
test4 = make_rand_duckpuzzle()
ducktest.append(test4)
print("\n")

print("Test: 5")
test5 = make_rand_duckpuzzle()
ducktest.append(test5)
print("\n")

print("Test: 6")
test6 = make_rand_duckpuzzle()
ducktest.append(test6)
print("\n")

print("Test: 7")
test7 = make_rand_duckpuzzle()
ducktest.append(test7)
print("\n")

print("Test: 8")
test8 = make_rand_duckpuzzle()
ducktest.append(test8)
print("\n")

print("Test: 9")
test9 = make_rand_duckpuzzle()
ducktest.append(test9)
print("\n")

print("Test: 10")
test10 = make_rand_duckpuzzle()
ducktest.append(test10)
print("\n")


print("HEURISTIC")
print("============================================")
print("============================================")

ducktestlist = 1

for i in ducktest:
    print("Test:", ducktestlist)
    starttime = default_timer()

    astar_search(i)

    endtime = default_timer()

    ducktestlist+=1

    print("Time in seconds: ", endtime - starttime)
    print("\n")


print("MANHATTAN HEURISTIC")
print("============================================")
print("============================================")

ducktestlist = 1

for i in ducktest:
    print("Test:", ducktestlist)
    starttime = default_timer()

    astar_search_manhattan(i)

    endtime = default_timer()

    ducktestlist+=1

    print("Time in seconds: ", endtime - starttime)
    print("\n")


print("MAX HEURISTIC")
print("============================================")
print("============================================")

ducktestlist = 1

for i in ducktest:
    print("Test:", ducktestlist)
    starttime = default_timer()

    astar_search_max(i)

    endtime = default_timer()

    ducktestlist+=1

    print("Time in seconds: ", endtime - starttime)
    print("\n")


print("Duck tests are all done!")


