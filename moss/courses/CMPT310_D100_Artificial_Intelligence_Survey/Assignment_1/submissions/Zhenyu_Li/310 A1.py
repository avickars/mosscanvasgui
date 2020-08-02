# a1.py

# Got some help with importing specific libraries and first few lines of codes from TA (Mohammadmahdi) during tutorial
# Learned stuffs like operators, syntax of Python from: https://www.tutorialspoint.com/python/index.htm
# Learned how to output result in a single line by using end from: https://www.geeksforgeeks.org/gfact-50-python-end-parameter-in-print/
# Referenced some general ideas about solving puzzles from: https://github.com/Duo-Lu
# Got some help from peer about check_solvability of class DuckPuzzle. However, I did not come up a result.

from search import *
import numpy as np
import time

#Class / function copied from aima-python search.py

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

        return sum(s != g and s!=0 for (s, g) in zip(node.state, self.goal))
        # blank 




# Question 1: Helper Functions

def make_rand_8puzzle():
    check = False #initially, the puzzle is not solvable.
    while check != True : #Keep generating the puzzle until it is solvable
        ##Code from TA:
        rand_puzzle = tuple(np.random.permutation(9))
        dummy_puzzle = dummy_puzzle = EightPuzzle(initial=rand_puzzle)
        check = dummy_puzzle.check_solvability(rand_puzzle)
        ##
        # print("puzzle is type: ", type(dummy_puzzle))
    return dummy_puzzle #class: __main__.EightPuzzle


def display(state): #state: class tuple
        
    for i in range(0,9):
        if (i+1)%3 == 0: 
            if state[i] == 0:
                print('*')
            else:
                print(state[i])

        else: 
            if state[i] == 0:
                print('*',end=' ')
            else: 
                print(state[i],end=' ')


# randpuzzle = make_rand_8puzzle()
# print(type(randpuzzle.initial)) 
# display(randpuzzle.initial)



# Question 2: Comparing Algorithms

#Class / function copied from aima-python search.py

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f') # g(n) + h(n)
    node = Node(problem.initial) #problem's initial nodes (position)
    frontier = PriorityQueue('min', f)
    frontier.append(node) #append initial nodes into frontier 
    explored = set()
    removed = 0 #count the nodes poped

    while frontier:
        node = frontier.pop()
        removed = removed +1
        if problem.goal_test(node.state): #if it reaches the goal state
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, removed 
        explored.add(node.state)
        for child in node.expand(problem): #in the list of nodes reachable in one step
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, removed


# Greedy best-first search is accomplished by specifying f(n) = h(n).
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


#Referenced the manhattan from In[40] : https://github.com/aimacode/aima-python/blob/master/search.ipynb
def Manhattan_heuristic(node):
    state = node.state
    goal_position = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    current_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    
    
    for i in range(len(state)):
        current_state[state[i]] = index[i]
    
    manhattan_distance = 0 #initially, it is 0
    
    for i in range(8):
        for j in range(2):
            manhattan_distance = manhattan_distance + abs(goal_position[i][j] - current_state[i][j])
    
    return manhattan_distance

def max_heuristic(node):
    return max(EightPuzzle(node.state).h(node), Manhattan_heuristic(node))


def solving_puzzle (problem_puzzle):

    #Learned how to calculate running time from TA's tutorial
    #Misplaced tile heuristic:
    starting_time_misplaced = time.time()
    misplaced_sol, misplaced_tile = astar_search(problem_puzzle)
    ending_time_misplaced = time.time()

    # print (misplaced_sol) 
    print ("By using the misplaced tile heuristic, the result is: ")
    display (misplaced_sol.state) #solution state
    running_time_misplaced = ending_time_misplaced - starting_time_misplaced
    print ("The running time of A*-search using the misplaced tile heuristic: ", running_time_misplaced)
    print ("The length of the solution: ", len(misplaced_sol.solution()))
    print ("The totoal number of nodes that were removed from frontier: ", misplaced_tile)
    print ("\n")

    #Manhattan distance heuristic:
    starting_time_Manhattan = time.time()
    Manhattan_sol, Manhattan_tile = astar_search(problem_puzzle, h = Manhattan_heuristic)
    ending_time_Manhattan = time.time()

    print ("By using the Manhattan distance heuristic, The result is: ")
    display (Manhattan_sol.state) #solution state
    running_time_Manhattan = ending_time_Manhattan - starting_time_Manhattan
    print ("The running time of A*-search using the Manhattan distance heuristic: ", running_time_Manhattan)
    print ("The length of the solution: ", len(Manhattan_sol.solution()))
    print ("The totoal number of nodes that were removed from frontier: ", Manhattan_tile)
    print ("\n")

    #Max of the misplaced tile heuristic and the Manhattan distance heuristic
    starting_time_Max = time.time()
    Max_sol, Max_tile = astar_search(problem_puzzle, h = max_heuristic)
    ending_time_Max = time.time()

    print ("By using the Max of both methods, The result is: ")
    display (Manhattan_sol.state) #solution state
    running_time_Max = ending_time_Max - starting_time_Max
    print ("The running time of A*-search using the Max of the misplaced tile heuristic and Manhattan distance heuristic: ", running_time_Max)
    print ("The length of the solution: ", len(Max_sol.solution()))
    print ("The totoal number of nodes that were removed from frontier: ", Max_tile)
    print ("\n")


#Creating 10 (more would be better!) random 8-puzzle instances
for x in range(0,16):
    random_puzzle = make_rand_8puzzle()
    # random_puzzle = EightPuzzle(tuple(dummy_puzzle))
    print ("The initial state of No.", x+1, "random 8-puzzle: ")
    display(random_puzzle.initial) #initial state of the puzzle
    print ("\n")
    solving_puzzle (random_puzzle)
    
    # print (type(dummy_puzzle))



#Question 3: The House-Puzzle

#modified the class EightPuzzle from Search.py
class DuckPuzzle(Problem):
    #Think about having the board that each block is indexed from 0 to 8 from the first row to the third row.
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

        # remove blank tile possible_actions under certain circumstances: 
        # modification: 
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        
        return possible_actions


    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # changing the index of tile. Tiles in different row may have different delta
        if blank == 0 or blank == 1: #row 1
            if blank == 0:
                delta = {'UP': 0, 'DOWN': 2, 'LEFT': 0, 'RIGHT': 1} #0
            else:
                delta = {'UP': 0, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 0} #1
        elif blank == 2 or blank == 3 or blank == 4 or blank == 5: #row 2
            if blank == 2:
                delta = {'UP': -2, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1} #2
            elif blank == 3:
                delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1} #3
            elif blank == 4:
                delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1} #4
            else:
                delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 0} #5
        else:
            if blank == 6:
                delta = {'UP': -3, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1} #6
            elif blank == 7:
                delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1} #7
            else:
                delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 0} #8

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)


    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal


    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        #Can't really figure out what to do here

        return True

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g and s!=0 for (s, g) in zip(node.state, self.goal))


def make_rand_duckpuzzle():
    check = False #initially, the puzzle is not solvable.
    while check != True : #Keep generating the puzzle until it is solvable
        ##Code from TA:
        rand_puzzle = tuple(np.random.permutation(9)) #one solution tuple([3,0,2,1,7,6,4,8,5])
        dummy_puzzle = dummy_puzzle = DuckPuzzle(initial=rand_puzzle)
        check = dummy_puzzle.check_solvability(rand_puzzle)
        ##
        # print("puzzle is type: ", type(dummy_puzzle))
    # print (type(dummy_puzzle))
    # display_duck(dummy_puzzle.initial)
    return dummy_puzzle #class: __main__.EightPuzzle


def display_duck(state): #state: class tuple
        
    for i in range(0,2):
        if state[i] == 0:
            if i == 0:
                print('*', end=' ')
            else:
                print('*')
        else:
            if i == 0:
                print(state[i], end=' ')
            else:
                print(state[i])


    for i in range(2,6):
        if state[i] == 0:
            if i == 5:
                print('*')
            else:
                print('*', end=' ')
        else:
            if i == 5:
                print(state[i])
            else:
                print(state[i], end=' ')
   
    print(' ', end=' ')

    for i in range(6,9):
        if state[i] == 0:
            print('*', end=' ')
        else:
            print(state[i], end=' ')


def Duck_Manhattan_heuristic(node):
    state = node.state
    #Think of the board as a 4x4 matrix where [0,3] [0,4] [2,0] are not available for tile
    goal_position = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
    current_state = {}
    index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
    
    
    for i in range(len(state)):
        current_state[state[i]] = index[i]
    
    manhattan_distance = 0 #initially, it is 0
    
    for i in range(8):
        for j in range(2):
            manhattan_distance = manhattan_distance + abs(goal_position[i][j] - current_state[i][j])
    
    return manhattan_distance

def max_heuristic_Duck(node):
    return max(DuckPuzzle(node.state).h(node), Duck_Manhattan_heuristic(node))


def solving_duck_puzzle (problem_puzzle):

    #Learned how to calculate running time from TA's tutorial
    #Misplaced tile heuristic:
    starting_time_misplaced = time.time()
    misplaced_sol, misplaced_tile = astar_search(problem_puzzle)
    ending_time_misplaced = time.time()

    # print (misplaced_sol) 
    print ("By using the misplaced tile heuristic, the result is: ")
    display_duck (misplaced_sol.state) #solution state
    running_time_misplaced = ending_time_misplaced - starting_time_misplaced
    print ("The running time of A*-search using the misplaced tile heuristic: ", running_time_misplaced)
    print ("The length of the solution: ", len(misplaced_sol.solution()))
    print ("The totoal number of nodes that were removed from frontier: ", misplaced_tile)
    print ("\n")


    #Manhattan distance heuristic:
    starting_time_Manhattan = time.time()
    Manhattan_sol, Manhattan_tile = astar_search(problem_puzzle, h = Duck_Manhattan_heuristic)
    ending_time_Manhattan = time.time()

    print ("By using the Manhattan distance heuristic, The result is: ")
    display_duck (Manhattan_sol.state) #solution state
    running_time_Manhattan = ending_time_Manhattan - starting_time_Manhattan
    print ("The running time of A*-search using the Manhattan distance heuristic: ", running_time_Manhattan)
    print ("The length of the solution: ", len(Manhattan_sol.solution()))
    print ("The totoal number of nodes that were removed from frontier: ", Manhattan_tile)
    print ("\n")


    #Max of the misplaced tile heuristic and the Manhattan distance heuristic
    starting_time_Max = time.time()
    Max_sol, Max_tile = astar_search(problem_puzzle, h = max_heuristic_Duck)
    ending_time_Max = time.time()

    print ("By using the Max of both methods, The result is: ")
    display_duck (Manhattan_sol.state) #solution state
    running_time_Max = ending_time_Max - starting_time_Max
    print ("The running time of A*-search using the Max of the misplaced tile heuristic and Manhattan distance heuristic: ", running_time_Max)
    print ("The length of the solution: ", len(Max_sol.solution()))
    print ("The totoal number of nodes that were removed from frontier: ", Max_tile)
    print ("\n")


#Creating 10 (more would be better!) random Duck-puzzle instances
for x in range(0,11):
    random_puzzle = make_rand_duckpuzzle()
    print ("The initial state of No.", x+1, "random Duck puzzle: ")
    display_duck(random_puzzle.initial) #initial state of the puzzle
    print ("\n")
    # print(type(random_Duck_puzzle))
    solving_duck_puzzle (random_puzzle)
    # misplaced_sol, misplaced_tile = astar_search(random_Duck_puzzle)
    # print(type(misplaced_tile))
    # print (misplaced_tile)
    # print(type(misplaced_sol))

# 2x2 3x3 share the same block , each has a solution
