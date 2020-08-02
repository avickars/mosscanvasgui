# a1.py

from search import *

# ...

from random import sample, choice
import time

#table was meant to be used for initial manhattan attempt
'''
tables = [(0,1,2,1,2,3,2,3,4),
        (1,0,1,2,1,3,3,2,3),
        (2,1,0,3,2,1,4,3,2),
        (1,2,3,0,1,2,1,2,3),
        (2,1,2,1,0,1,2,1,2),
        (3,2,1,2,1,0,3,2,1),
        (2,3,4,1,2,3,0,1,2),
        (3,2,3,2,1,2,1,0,1)]
'''

#calculates the distance of a particular node to its home position
#student Sukhdeep Parmar (spa111@sfu.ca) helped me develop and understand the calculate function
def calculate(currentPos, goalPos, isEight=True):
    #appropriate grid mapping if the puzzle is an EightPuzzle
    if(isEight==True):
        grid = {
            0:(0,0), 1:(1,0), 2:(2,0),
            3:(0,1), 4:(1,1), 5:(2,1),
            6:(0,2), 7:(1,2), 8:(2,2)
        }

    #appropriate grid mapping if the puzzle is a HousePuzzle
    else:
        grid = {
            0:(0,0), 1:(1,0),
            2:(0,1), 3:(1,1), 4:(2,1), 5:(3,1),
            6:(1,2), 7:(2,2), 8:(3,2)
        }

    #maps inputted values to grid to get values for equation
    x1, y1 = grid.get(currentPos)
    x2, y2 = grid.get(goalPos)
    manhattanNum = abs(x1-x2) + abs(y1-y2)
    return manhattanNum

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

    #initial attempt of calculating the manhattan heuristic but for some reason took way too long    
    '''
    def manhattan(self, node):
        state = self.initial
        manSum = 0
        for i in range(len(state)):
            if(self.initial.index(i)==0):
                continue
            manSum = manSum + tables[self.initial.index(i)-1][i]
        return manSum
    '''

    #adds up all the calculated manahattan distances of each elements in the node state
    #student Sukhdeep Parmar (spa111@sfu.ca) helped me develop and understand the manhattan function
    def manhattan(self, node):
        manSum = 0

        #adds all manahattan distances after calling the calculate function
        #includes 0 tile in the calculations
        for i in range(len(self.goal)):
            manSum = manSum + calculate(node.state.index(i),self.goal.index(i))
        return manSum

#new Problem class
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

        #changed the possible actions that can be performed based on the DuckPuzzle shape
        if index_blank_square  == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square > 5:
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

    #does not work well for DuckPuzzle
    '''
    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0
    '''

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        manSum = 0

        #if the manhattan is being called on a DuckPuzzle
        if(type(self)) == DuckPuzzle:
            for i in range(len(self.goal)):
                manSum = manSum + calculate(node.state.index(i),self.goal.index(i),False)

        #if the manhattan is being called on an EightPuzzle
        else:
            for i in range(len(self.goal)):
                manSum = manSum + calculate(node.state.index(i),self.goal.index(i))
        return manSum

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
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    #counter for nodes popped from frontier
    remFrontier = 0
    while frontier:
        node = frontier.pop()
        remFrontier = remFrontier + 1
        if problem.goal_test(node.state):
            if display:
                #print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                print(f'total number of nodes removed from the frontier: {remFrontier}')
                print(f'length of the solution: {node.path_cost}')
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

#returns a new instance of EightPuzzle with a solvable state
def make_rand_8puzzle():
    start = tuple((0,1,2,3,4,5,6,7,8))

    #shuffle the tuple to randomize the order
    #reference: https://stackoverflow.com/questions/17649875/why-does-random-shuffle-return-none
    shuffled = random.sample(start,len(start))
    solvable8puzz = EightPuzzle(shuffled)

    #if the state is not solvable, shuffle the order
    while(solvable8puzz.check_solvability(shuffled) == 0):
        shuffled = random.sample(shuffled,len(shuffled))

    #convert list to tuple
    solvable8puzz.initial = tuple(shuffled)
    return solvable8puzz

#returns a new instance of DuckPuzzle with a solvable state
def make_rand_Dpuzzle():
    #make the initial state the goal state
    start = tuple((1,2,3,4,5,6,7,8,0))
    solvableDpuzz = DuckPuzzle(start)

    #choose random actions to reverese the goal state into some random solvable state
    for i in range(75):
        actionList = solvableDpuzz.actions(solvableDpuzz.initial)

        #pick a random action from the list of possible actions
        #https://stackoverflow.com/questions/306400/how-to-randomly-select-an-item-from-a-list      
        randAct = random.choice(actionList)
        solvableDpuzz.initial = solvableDpuzz.result(solvableDpuzz.initial,randAct)
    return solvableDpuzz

#prints the state of an EightPuzzle 
#set isEight to False to print the state of a DuckPuzzle
def display(state, isEight=True):
    #create a 3x3 2-dimensional list
    #https://stackoverflow.com/questions/6667201/how-to-define-a-two-dimensional-array-in-python
    width = 3
    height = 3
    Matrix = [[0 for x in range(width)] for y in range(height)]
    counter = 0

    #fill in the 2-dimensional list with the state elements
    for i in range(0,3):
        for j in range(0,3):
            #0 should be represented as *
            if (state[counter] == 0):
                Matrix[i][j] = '*'
                counter = counter + 1
            else:
                Matrix[i][j] = state[counter]
                counter = counter + 1

    #display if the state belongs to an EightPuzzle
    if(isEight==True):
        #print elements of the 2-dimesional array (3 per line)
        print(Matrix[0][0], Matrix[0][1], Matrix[0][2])
        print(Matrix[1][0], Matrix[1][1], Matrix[1][2])
        print(Matrix[2][0], Matrix[2][1], Matrix[2][2])

    #display if the state belongs to HousePuzzle
    else:
        print(Matrix[0][0], Matrix[0][1])
        print(Matrix[0][2], Matrix[1][0], Matrix[1][1], Matrix[1][2])
        print(' ', Matrix[2][0], Matrix[2][1], Matrix[2][2])


#create 10 EightPuzzle instances
puzzleList8 = [make_rand_8puzzle(),
            make_rand_8puzzle(),
            make_rand_8puzzle(),
            make_rand_8puzzle(),
            make_rand_8puzzle(),
            make_rand_8puzzle(),
            make_rand_8puzzle(),
            make_rand_8puzzle(),
            make_rand_8puzzle(),
            make_rand_8puzzle()]

#create 10 DuckPuzzle instances
puzzleListD = [make_rand_Dpuzzle(),
            make_rand_Dpuzzle(),
            make_rand_Dpuzzle(),
            make_rand_Dpuzzle(),
            make_rand_Dpuzzle(),
            make_rand_Dpuzzle(),
            make_rand_Dpuzzle(),
            make_rand_Dpuzzle(),
            make_rand_Dpuzzle(),
            make_rand_Dpuzzle()]

#EightPuzzle using misplaced heurisitic
for i in range(10):
    display(puzzleList8[i].initial)
    start_time = time.time()
    astar_search(puzzleList8[i],puzzleList8[i].h,True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time: {elapsed_time} seconds')

#EightPuzzle using manhattan heurisitic
for i in range(10):
    display(puzzleList8[i].initial)
    start_time = time.time()
    astar_search(puzzleList8[i],puzzleList8[i].manhattan,True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time: {elapsed_time} seconds')

#EightPuzzle using max heurisitic
for i in range(10):
    display(puzzleList8[i].initial)
    start_time = time.time()
    astar_search(puzzleList8[i],lambda n: max(puzzleList8[i].h(n),puzzleList8[i].manhattan(n)),True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time: {elapsed_time} seconds')

#DuckPuzzle using misplaced heurisitic
for i in range(10):
    display(puzzleListD[i].initial,False)
    start_time = time.time()
    astar_search(puzzleListD[i],puzzleListD[i].h,True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time: {elapsed_time} seconds')

#DuckPuzzle using manhattan heurisitic
for i in range(10):
    display(puzzleListD[i].initial,False)
    start_time = time.time()
    astar_search(puzzleListD[i],puzzleListD[i].manhattan,True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time: {elapsed_time} seconds')

#DuckPuzzle using max heurisitic
for i in range(10):
    display(puzzleListD[i].initial,False)
    start_time = time.time()
    astar_search(puzzleListD[i],lambda n: max(puzzleListD[i].h(n),puzzleListD[i].manhattan(n)),True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time: {elapsed_time} seconds')