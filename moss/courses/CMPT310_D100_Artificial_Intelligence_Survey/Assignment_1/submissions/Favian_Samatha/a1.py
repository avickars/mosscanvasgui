# a1.py
# Assignment 1 for CMPT 310
# Created by: Favian (Ian) Samatha
# Date last edited: May 29, 2020
# Student ID: 301328390 
from search import *
import time
import random
#IMPORTANT Note! Running this program right now will generate 15 puzzles of eight puzzle
#and duck puzzles and search through them as well. Uncomment if you want to run your own test cases

#------------------------------ Startof Classes -----------------------------------
#This section is involved with Q2 (the search) and Q3 (the duck pzuzle)

#Rewrote the EightPuzzle Class from search.py
#Created its own A*search method
#Created the Manhattan method
#Altered the h method so that it rejects the 0 position
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
        #Added s!= 0 to not count the zero tiles
        return sum(s != g and s!=0 for (s, g) in zip(node.state, self.goal))
    
    def manh8(self,node):
        #Maps the correct position through indexing
        #Example, correctPos[0] = 2,2 because in a 3x3 matrix, 
        #its index would be [2][2]
        correctPos = [[2,2],[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1]]
        xPos = 0
        yPos = 0
        currentPos = [[0 for i in range(3)] for j in range (3)]
        counter = 0
        #Maps the state to a 3x3 matrix
        for i in range(3):
            for j in range(3):
                currentPos[i][j] = node.state[counter]
                counter = counter+1
        #Checks for every value (exept for zero) the manhattan distance
        for i in range(3):
            for j in range(3):
                if (currentPos[i][j] ==0):
                    continue
                else:
                    temp = currentPos[i][j]
                    xPos = xPos + abs(correctPos[temp][1] - j)
                    yPos = yPos + abs(correctPos[temp][0] - i)
        return yPos + xPos 

    #Created this function so that it would choose the highest h value between
    #the misplaced tile function (h function) and the manhatten distance function
    def maxh8(self,node):
        return max(EightPuzzle.h(self,node),EightPuzzle.manh8(self,node))
    #Added this function in here for simplicity
    def astar_search(problem, h=None, display=False):
        """A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass."""
        h = memoize(h or problem.h, 'h')
        return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


#Copied the Eight Puzzle class
#I changed the actions method, the misplaced tile/h method and the result method
#I added the manHDuck method, an astar_search method, and a maxDuck method
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
    #Changed this to accomadate the different legal moves in the duck puzzle
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """
        #UP refers to when moving from bottom row to middle row
        #UP2 refers to when moving from middle row to top row
        #DOWN refers to when moving from top row to middle row
        #DOWN2 refers to when moving from middlerow to bottom row
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT','UP2','DOWN2']
        index_b = self.find_blank_square(state)

        if index_b == 0 or index_b == 2 or index_b == 6:
            possible_actions.remove('LEFT')
        if index_b <= 5:
            possible_actions.remove('UP')
        if index_b == 8 or index_b == 5 or  index_b ==1:
            possible_actions.remove('RIGHT')
        if index_b > 1:
            possible_actions.remove('DOWN')
        if index_b !=3 and index_b !=4 and index_b !=5:
            possible_actions.remove('DOWN2')
        if index_b !=2 and index_b != 3:
            possible_actions.remove('UP2')

        return possible_actions
    # Changed values in delta for the duck puzzle
    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN2': 3, 'LEFT': -1, 'RIGHT': 1, 'UP2': -2 , 'DOWN':2}
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
        #I added "and s!=0" so that it does not include the 0 tile
        return sum(s != g and s!=0 for (s, g) in zip(node.state, self.goal))
        

    #Created this
    def manhDuck(self,node):
        #I mapped them to a 3x4 grid and found their distance through indexing
        #Example, correctPos[0] = 2,3 because in the duck puzzle, if it was a 3x4 grid,
        #it would be at position [2][3]
        correctPos = [[2,3],[0,0],[0,1],[1,0],[1,1],[1,2],[1,3],[2,1],[2,2]]
        xPos = 0
        yPos = 0
        currentPos = [[0 for i in range(4)] for j in range (3)]
        counter = 0
        #I re-map the state to a 3x4 matrix. For positions wiht no numbers (like i=0,j=2), I put a 9 for filler
        for i in range(3):
            for j in range(4):
                if (i==0 and j==2) or (i==0 and j==3) or (i==2 and j==0):
                    currentPos[i][j] = 9 #9 is just a filler
                else:
                    currentPos[i][j] = node.state[counter]
                    counter = counter+1

        #I check each value, skipping those that are in "filler positions" and calculate
        #Their current psotion through indexing.
        for i in range(3):
            for j in range(4):
                if (i==0 and j==2) or (i==0 and j==3) or (i==2 and j==0):
                    continue
                else:
                    if (currentPos[i][j] ==0):
                        continue
                    else:
                        temp = currentPos[i][j]
                        xPos = xPos + abs(correctPos[temp][1] - j)
                        yPos = yPos + abs(correctPos[temp][0] - i)
        return (yPos + xPos)
    #Created maxDuck to choose the larges h value from the misplaced tile method and the manhattan distance mehtod
    def maxDuck(self,node):
        return max(DuckPuzzle.h(self,node),DuckPuzzle.manhDuck(self,node))
    #Added this function in here for simplicity
    def astar_search(problem, h=None, display=False):
        """A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass."""
        h = memoize(h or problem.h, 'h')
        return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

#------------------------------End of Classes -----------------------------------


#I added this here so that I can output how many frontieres were removed
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
    #This variable keeps tracked of how many frontiers were popped
    totalFrontier = 0 
    explored = set()
    while frontier:
        node = frontier.pop()
        totalFrontier = totalFrontier+1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [totalFrontier,node]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

#-----------------Next 2 functions are for Q1-----------------
#This function makes a random solvable 8-puzzle
def make_rand_8puzzle():
    #Initialize a list and randomize it
    list_init_state = [1,2,3,4,5,6,7,8,0]
    random.shuffle(list_init_state)
    test = tuple(list_init_state)

    #If it isn't solvable, reo-rder the list and do it again
    while not EightPuzzle(test).check_solvability(test):
        random.shuffle(list_init_state)
        test = tuple(list_init_state)

    puzzle = EightPuzzle(initial=test)
    return puzzle

#This function displays the 8puzzle in a friendly format
def display(state):
    for i in range(9):
        if state.initial[i] == 0:
            print("*",end=" ")
        else:
            print(state.initial[i],end=" ")
        if (i+1)%3==0 :
            print("")

#This function displays the duck puzzle in a friendly format
def displayDuck(state):
    currentPos = [[0 for i in range(4)] for j in range (3)]
    counter = 0
    for i in range(3):
        for j in range(4):
            if (i==0 and j==2) or (i==0 and j==3) or (i==2 and j==0):
                currentPos[i][j] = ""
            else:
                currentPos[i][j] = state.initial[counter]
                counter = counter+1
    for i in range(3):
        for j in range(4):
            if (i==0 and j==2) or (i==0 and j==3):
                    continue
            if (i==2 and j==0):
                print("",end=" ")
            if currentPos[i][j] ==0:
                print("*", end=" ")
            else:
                print(currentPos[i][j],end=" ")
        print("")

#This function makes a random solvable duck puzzle instance
#We know it's solvable because it is randomized by a series of legal moves
#from the goal state
def make_rand_duckPuzzle():
    goal_state = (1,2,3,4,5,6,7,8,0)
    state = goal_state
    counter = 0
    while counter <1000000:
        puzzle = DuckPuzzle(state)
        possibleMoves = puzzle.actions(puzzle.initial)
        rand = random.randint(0,len(possibleMoves)-1)
        state = puzzle.result(puzzle.initial,possibleMoves[rand])
        counter+=1
        
    return puzzle


#This function runs the test for analysis
def start_run(numPuz):
    print("\n!!!! 8-Puzzle Analysis !!!!\n")
    for i in range (numPuz):
        print("Eight Puzzle #",i+1)
        print("\n")
        eightPuz = make_rand_8puzzle()
        display(eightPuz)
        print("\n")
        print("-----A*-Search Using Misplaced Tile Heuristic-----")
        start_time = time.time()
        search = eightPuz.astar_search(display=True)
        end_time = time.time()
        final_time = end_time-start_time
        print("Time:",final_time)
        print("The length of the solution:", search[1].path_cost)
        print("The # of nodes removed from frontier:", search[0])
        
        print("-----A*-Search Using Manhattan Distance Heurisitc-----")
        start_time = time.time()
        search = eightPuz.astar_search(h=eightPuz.manh8,display=True)
        end_time = time.time()
        final_time = end_time-start_time
        print("Time:",final_time)
        print("The length of the solution:", search[1].path_cost)
        print("The # of nodes removed from frontier:", search[0])

        print("-----A*-Search Using Max of Manhattan Distance Heurisitc and Misplaced Tile Heuristic-----")
        start_time = time.time()
        search = eightPuz.astar_search( h=eightPuz.maxh8,display=True)
        end_time = time.time()
        final_time = end_time-start_time
        print("Time:",final_time)
        print("The length of the solution:", search[1].path_cost)
        print("The # of nodes removed from frontier:", search[0])
        print("-----------\n")


    #Duck Puzzle
    print("\n!!!! Duck Puzzle Analysis !!!!\n")

    for i in range (numPuz):
        print("Duck Puzzle #",i+1)
        print("\n")
        duckPuz = make_rand_duckPuzzle()
        
        displayDuck(duckPuz)
        print("")
        print("-----A*-Search Using Misplaced Tile Heuristic-----")
        start_time = time.time()
        search = duckPuz.astar_search(display=True)
        end_time = time.time()
        final_time = end_time-start_time
        print("Time:",final_time)
        print("The length of the solution:", search[1].path_cost)
        print("The # of nodes removed from frontier:", search[0])
        
        print("-----A*-Search Using Manhattan Distance Heurisitc-----")
        start_time = time.time()
        search = duckPuz.astar_search(h=duckPuz.manhDuck,display=True)
        end_time = time.time()
        final_time = end_time-start_time
        print("Time:",final_time)
        print("The length of the solution:", search[1].path_cost)
        print("The # of nodes removed from frontier:", search[0])
        
        print("-----A*-Search Using Max of Manhattan Distance Heurisitc and Misplaced Tile Heuristic-----")
        start_time = time.time()
        search = duckPuz.astar_search(h=duckPuz.maxDuck,display=True)
        end_time = time.time()
        final_time = end_time-start_time
        print("Time:",final_time)
        print("The length of the solution:", search[1].path_cost)
        print("The # of nodes removed from frontier:", search[0])
        print("-----------\n")
#------------------------------ End of Functions


#Main function

#Uncomment this line below if you want to run your own test cases
start_run(15)