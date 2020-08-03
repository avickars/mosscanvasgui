# a1.py
from search import *
import random
import time
import sys
#Question 1

#modified EightPuzzle to have two new functions: manhattan_distance and max_h to calculate new heuristics
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
        mt_h = sum(s != g for (s, g) in zip(node.state, self.goal))
        for (x, y) in zip(node.state, self.goal):
            if x == 0:
                mt_h -= 1
        return mt_h

    def mhn_distance(self, node):
        init_state = node.state #define state
        target = (1, 2, 3, 4, 5, 6, 7, 8, 0) #this is the goal state
        distance = 0 #manhattan distance
        dx = 0 #difference of distance by the row
        dy = 0 #difference of distance by the column
        for k in init_state:
            di = abs(target.index(k) - init_state.index(k)) #find out the difference of index between target state and initial state
            if k != 0: #0 does not account for in calculating manhattan distance
                dx = di % 3
                dy = di // 3
                distance += dx + dy #distance increment
                if di % 3 == 1 and abs(init_state.index(k)%3 - target.index(k)%3) == 2: #special case where in 2-D two indices are diagonal but difference is only 1 in di. 
                    distance += 2 #increment by 2 due to special case
        return distance
    
    def max_h(self, node):
        mis_t_h = self.h(node)
        man_distance = self.mhn_distance(node)
        return max(mis_t_h, man_distance)

#modified EightPuzzle class to DuckPuzzle
#changed actions, result and check_solvability functions
class DuckPuzzle(Problem):
    
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state): #changed possible actions to suit the duck puzzle board.
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        blank = state.index(0)
        if blank == 0 or blank == 1 or blank == 4 or blank == 5:
            possible_actions = ['DOWN', 'LEFT', 'RIGHT']
            if blank == 0:
                possible_actions = ['DOWN', 'RIGHT']
            if blank == 1:
                possible_actions = ['DOWN', 'LEFT']
            if blank == 5:
                possible_actions = ['DOWN', 'LEFT']
        if blank == 2 or blank > 5:
            possible_actions = ['UP', 'LEFT', 'RIGHT']
            if blank == 2:
                possible_actions = ['UP', 'RIGHT']
            if blank == 6:
                possible_actions = ['UP', 'RIGHT']
            if blank == 8:
                possible_actions = ['UP', 'LEFT']
        return possible_actions

    def result(self, state, action): #modified delta values to better suit the duck puzzle board.
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        if blank < 3: #when blank index is 0, 1 or 2, the up neightbor and down neighbor is 2 indicies away from blank
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        if blank == 3: #when blank index is 3, the up neightbor is 2 indicies away
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
        """ Checks if the given state is solvable
        #if sum of (inversion + blank position index) is odd, the the puzzle is solvable
        #divide the duck puzzle into two separate grids. First is a 2x2 with numbers of index 0, 1, 2 and 3 from the duck puzzle index
        #the other is a 2x3 grid with numbers of index 4 to 8 from the duck puzzle index
         if the puzzle is like: 1 2
                                3 4 5 6
                                  7 8 0
                                  
        then 1 2                                    4 5 6
             3 4 forms the 2x2 board and            7 8 0   froms the 2x3 board

        if both boards are solvable at the same time, then the whole duck puzzle is solvable
        """
        blank_index = self.find_blank_square(state)
        index_goal = {1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2], 0: [2, 3]}
        index_state = {}
        index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]
            
        solvable2x2 = False
        solvable2x3 = False
        solvable = False
        dmt2x2 = 0 #determinant for the 2*2 grid
        dmg2x3 = 0 #determinant for the 2*3 grid
        inversion = 0
        if state.index(1) == 0 and state.index(2) == 1 and state.index(3) == 2:    #if 1 2 and 3 are in the first 4 numbers in unsolved state
            if blank_index < 4: #if blank is in the first 4 numbers
                for i in range(4): #calculate the number of inversions
                    for j in range(i + 1, 4):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                dmt2x2 = inversion + index_state[0][0] + index_state[0][1] #locate the position (sum of row and column) of 0 in dictionary and add to inversion
                if dmt2x2 % 2 == 1: #if the determinant is odd
                    solvable2x2 = True
                inversion = 0 #clear inversion
                #determine whether the 2x3 board is solvable
                for r in range(3, 9): #determine the inversion in 2x3 grid
                    for q in range(r + 1, 9):
                        if (state[r] > state[q]) and state[r] != 0 and state[q] != 0:
                            inversion += 1
                dmt2x3 = 2 + inversion
                if dmt2x3 % 2 == 1:
                    solvable2x3 = True
                if solvable2x2 == True and solvable2x3 == True: #if the 2x2 grid and 2x3 grid are both solvable
                    solvable = True #then the whole puzzle is solvable
                else:
                    solvable = False
                return solvable
            else: #same logic applies like the above but this time 0 is not in the 2x2 grid
                if state.index(1) < 3 and state.index(2) < 3 and state.index(3) < 3:
                    for k in range(4):
                        for p in range(k + 1, 4):
                            if (state[k] > state[p]) and state[k] != 0 and state[p] != 0:
                                inversion += 1
                    dmt2x2 = inversion + index_state[0][0] + index_state[0][1]
                    if dmt2x2 % 2 == 1:
                        solvable2x2 = True
                    inversion = 0 #clear inversion
                    for s in range(3, 9):
                        for t in range(s + 1, 9):
                            if (state[s] > state[t]) and state[s] != 0 and state[t] != 0:
                                inversion += 1
                    dmt2x3 = inversion + index_state[0][0] + index_state[0][1]
                    if dmt2x3 % 2 == 1:
                        solvable2x3 = True
                    if solvable2x2 == True and solvable2x3 == True:
                        solvable = True
                    else:
                        solvable = False
                    return solvable
                else:
                    solvable = False
                    return solvable
        else:
            solvable = False
            return solvable

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        mt_h = sum(s != g for (s, g) in zip(node.state, self.goal))
        for (x, y) in zip(node.state, self.goal):
            if x == 0:
                mt_h -= 1
        return mt_h

    def mhn_distance(self, node): #modified test_search.py manhattan distance to suit the duck puzzle board
        state = node.state
        index_goal = {1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2], 0: [2, 3]}
        index_state = {}
        index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhd = 0

        for i in range(1, 9): #i does not include 0 
            for j in range(2):
                    mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

        return mhd
    def max_h(self, node):
        mis_t_h = self.h(node)
        man_distance_duck = self.mhn_distance(node)
        return max(mis_t_h, man_distance_duck)
    
def make_rand_8puzzle():
    order_list = tuple(range(9))
    perm = tuple(random.sample(order_list, len(order_list)))
    return perm
def make_rand_duckPuzzle():
    order_list = tuple(range(9))
    perm = tuple(random.sample(order_list, len(order_list)))
    return perm
state = make_rand_8puzzle() #define state
puzzle = EightPuzzle(Problem) #class
solvable = puzzle.check_solvability(state) #returns true or false

while solvable == False: #make a conditional loop
    if solvable == False:
        state = make_rand_8puzzle()
        solvable = puzzle.check_solvability(state)
        print("unsolvable puzzle, redoing...")
    else:
        break

def display(state):
    for i in tuple(range(9)):
        if(i%3==0):
            print("")
        if(state[i]==0):
            print("*", end = " ")
        else:
            print(state[i], end = " ")
display(state)
print("\nstate is: ", state, "\n")
#This is duck display function
def display_duck(state):
    for i in tuple(range(9)):
        if i == 2:
            print("")
        if i == 6:
            print("")
            print(" ", end = " ")
        if state[i] == 0:
            print("*", end = " ")
        else:
            print(state[i], end = " ")
duck_state = make_rand_duckPuzzle()
duck_puzzle = DuckPuzzle(Problem)
duck_solvable = duck_puzzle.check_solvability(duck_state)
while duck_solvable == False:
    if duck_solvable == False:
        duck_state = make_rand_duckPuzzle()
        duck_solvable = duck_puzzle.check_solvability(duck_state)
        #print("unsolvable duck puzzle, redoing...")
    else:
        break
print("\nthis is Duck Puzzle: ")
display_duck(duck_state)

#Question 2

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display=True) #changing display to True to guide in if display in best first search

def astar_search_manhattan(problem, h = None, display= False):
    h = problem.mhn_distance
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display = True)
def astar_search_max(problem, h = None, display = False):
    h= problem.max_h
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display = True)

def best_first_graph_search(problem, f, display=True):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    numFrontRemoved = 0 #set up a counter to count how many node have been removed from frontier
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        numFrontRemoved += 1 #increment on every node poped from frontier
        if problem.goal_test(node.state):
            if display:
                print()
                print()
                #print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                print("\nhere is the total number of nodes removed from frontier: ", numFrontRemoved) #print the number of nodes removed from frontier
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

puzzleCount=1
print("\nHere are the 10 puzzles for question 2:")
while 0<1:
    if solvable == False: 
        state = make_rand_8puzzle()
        solvable = puzzle.check_solvability(state)
    else:
        print("\npuzzle#", puzzleCount)
        display(state)
        puzzleCount += 1
        newEightPuzzle = EightPuzzle(state)

        #misplaced
        print("\ncalculating solution with A* search using misplaced tiles heuristic...")
        start_time = time.time() #start timer
        stepsToSolve = astar_search(newEightPuzzle).solution() #store the steps to solve the puzzle in a list variable
        finish_time = time.time()-start_time #calculates time elapsed in seconds
        print("\nthis is the solution using the misplaced tile heuristic: ", stepsToSolve)
        countSteps = len(stepsToSolve) #count number of stpes using len
        print("\nthis is the length of solution: ", countSteps) 
        print("\nthis puzzle took", finish_time, "seconds using the misplaced tile heuristic")
        print()

        #manhattan
        print("\ncalculating solution with A* search using Manhattan distance heuristic...")
        start_time_man = time.time() #start timer for manhattan distance
        man_solve = astar_search_manhattan(newEightPuzzle).solution()
        finish_time_man = time.time() - start_time_man
        print("\nthis is the solution using the manhattan distance heuristic: ", man_solve)
        print("\nthis is the length of the solution using manhattan distance heuristic: ", len(man_solve))
        print("\nthis puzzle took", finish_time_man, "seconds using the manhattan distance heuristic")
        print()

        #max
        print("\ncalculating solution with A* search using max heuristic...")
        start_time_max = time.time() #start timer for max
        max_solve = astar_search_max(newEightPuzzle).solution()
        finish_time_max = time.time() - start_time_max
        print("\nthis is the solution using max heuristic between the two: ", max_solve)
        print("\nthis is the length of the solution using max heuristic: ", len(max_solve))
        print("\nthis puzzle took", finish_time_max, "seconds using the max heuristic")

        
        state = make_rand_8puzzle() #make a new puzzle
        solvable = puzzle.check_solvability(state) #check solvability of new puzzle
        if puzzleCount == 11:
            break



#Question 3
print("\nHere are the 10 duck puzzles:")
duck_puzzleCount = 1
while 0 < 1:
    if duck_solvable == False:
        duck_state = make_rand_duckPuzzle()
        duck_solvable = duck_puzzle.check_solvability(duck_state)
    else:
        print("\nDuck puzzle #", duck_puzzleCount)
        display_duck(duck_state)
        duck_puzzleCount += 1
        newDuckPuzzle = DuckPuzzle(duck_state)
        
        #misplaced tiles
        print("\ncalculating solution of Duck Puzzle with A* search using misplaced tiles heuristic...")
        start_duck_time = time.time()
        duck_misplaced = astar_search(newDuckPuzzle).solution()
        finish_duck_time = time.time() - start_duck_time
        print("\nthis is the solution of Duck Puzzle with A* search using misplaced tiles heuristic: ", duck_misplaced)
        
        print("\nthis Duck Puzzle took", finish_duck_time, "seconds using the misplaced tile heuristic")
        print("\nthis is the length of solution: ", len(duck_misplaced))
        print()
        
        #manhattan
        print("\ncalculating solution of Duck Puzzle with A* search using manhattan distance heuristic...")
        start_duck_man = time.time()
        duck_manhattan = astar_search_manhattan(newDuckPuzzle).solution()
        finish_duck_man = time.time() - start_duck_man
        print("\nthis is the solution of Duck Puzzle with A* search using manhattan distance heuristic...", duck_manhattan)
        print("\nthis is the length of solution: ", len(duck_manhattan))
        print("\nthis puzzle took", finish_duck_man, "seconds using manhattan distance heuristic")
        print()

        #max
        print("\ncalculating solution of Duck Puzzle with A* search using max heuristic...")
        start_duck_max = time.time()
        duck_max = astar_search_max(newDuckPuzzle).solution()
        finish_duck_max = time.time() - start_duck_max
        print("\nthis is the solution of Duck Puzzle with A* search using max heuristic", duck_max)
        print("\nthis is the length of solution: ", len(duck_max))
        print("\nthis puzzle took", finish_duck_max, "seconds using max heuristic")
    duck_state = make_rand_duckPuzzle() #generate new puzzle
    duck_solvable = duck_puzzle.check_solvability(duck_state)
    if duck_puzzleCount == 11:
        break