# a1.py

# ...
# code from "https://github.com/aimacode/aima-python" was used as reference, inspiration and copied
#
import sys
from collections import deque
from utils import *
#
import random
import time
from search import *

# ______________________________________________________________________________
# A* heuristics 

# Copied from search.py  
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

        # to make the function smaller we use h = index_blank_square
        h = index_blank_square

        if h == 0 or h == 2 or h == 6:
            possible_actions.remove('LEFT')
        if h == 0 or h == 1 or h == 4 or h == 5:
            possible_actions.remove('UP')
        if h == 1 or h == 5 or h == 8:
            possible_actions.remove('RIGHT')
        if h == 2 or h == 6 or h == 7 or h == 8:
            possible_actions.remove('DOWN')
        return possible_actions
        
    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """
        
        
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        #print(blank)
        neighbor = blank + delta[action]
        #print("here",len(state))
        
        #print(neighbor)
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

# Creates a simple puzzle for EightPuzzle starting from 0 to 8
def create_puzzle():
    a = 0; b = 1; c = 2
    d = 3; e = 4; f = 5
    g = 6; h = 7; i = 8
    
    state = [a,b,c,d,e,f,g,h,i]
    return state

# Creates a simple puzzle for DuckPuzzle starting from 1 to 0 (1,2,3,4,5,6,7,8,0)
def create_duck_puzzle():
    a = 1; b = 2; c = 3
    d = 4; e = 5; f = 6
    g = 7; h = 8; i = 0
    
    state = [a,b,c,d,e,f,g,h,i]
    return state

# Displays the puzzle for EightPuzzle
def display(state):
    for x in range(1,10): # Iterates from 1 to 9
        if (state[x-1] == 0): # x-1 = from 0 to 8, we want 0 to become a star
            print("*", end =" ")
        elif state[x-1] != 0:
            print(state[x-1], end =" ")
        if (x%3) == 0: # Make a new line every iterations
            print("")
    return state
# Displays the puzzle for DuckPuzzle, more complex because of the added complexity of DuckPuzzle
def display_duck(state):
    i = 0
    for x in range(1,10): # Iterate from 1 to 9
        if x == 7: 
            print(" ", state[x-1], end =" ")
        elif (state[x-1] == 0): # Turn  0 into into a star
            print("*", end =" ")
        elif state[x-1] != 0:
            print(state[x-1], end =" ")
        i += 1
        if i == 2: # We reached two nodes, skip line
            print("")
        elif i == 6: # We reached six nodes, skip line (we would now be at 4 values)
            print(" ")
    print("")
    return state

# Make random puzzle for our EightPuzzle
def make_rand_8puzzle():
    
    state = create_puzzle()
    the_puzzle = EightPuzzle(initial = state)

    i = 0
    shuffle_amount = 1000 # We are shuffling everything 1000 times
    while i < shuffle_amount:
        options = the_puzzle.actions(state) # Where can we move?
        random_number = random.randint(0,len(options)-1) # Random movement based on what we have available
        random_action = options[random_number] # Move in one of the valid directions

        state = the_puzzle.result(state,random_action) # Change state to reflect new movement
        if the_puzzle.check_solvability(state) == False: # Error checker
            print("ERROR")
        i += 1
    return state

    return 


# Make random puzzle for our DuckPuzzle
def make_rand_duckpuzzle():
    
    state = create_duck_puzzle() # Create basic puzzle
    the_puzzle = DuckPuzzle(initial = state) # Initialize

    i = 0
    shuffle_amount = 1000 # We are POSSIBLY shuffling 1000 times
    while i < shuffle_amount:

        random_move = random.randint(0,3) # Pick a random direction to move
        x = 0
        while x <= 8:  
            if(state[x] == 0):
                current_location = x  # we now know where 0 is located
            x += 1
        
        h = current_location #To make the code neater, h = current_location

        #move up, everything but [0,1,4,5] also move valid number of steps
        if random_move == 0 and h != 0 and h != 1 and h != 4 and h != 5:
            if h == 2 or h == 3: # We move more/less steps depending on row we're at
                temp_state = state[h]
                state[h] = state[h-2]
                state[h-2] = temp_state
            if h == 6 or h == 7 or h == 8:
                temp_state = state[h]
                state[h] = state[h-3]
                state[h-3] = temp_state
        #move down, everything but [2,6,7,8] also move valid number of steps
        elif random_move == 1 and h != 2 and h != 6 and h != 7 and h != 8:
            if h == 0 or h == 1:
                temp_state = state[h]
                state[h] = state[h+2]
                state[h+2] = temp_state
            if h == 3 or h == 4 or h == 5: # We move more/less steps depending on row we're at
                temp_state = state[h]
                state[h] = state[h+3]
                state[h+3] = temp_state 
        #move left, everything but [0,2,6] also move valid number of steps
        elif random_move == 2 and h != 0 and h != 2 and h != 6:
            temp_state = state[h]
            state[h] = state[h-1]
            state[h-1] = temp_state
        #move right, everything but [1,5,8] also move valid number of steps
        elif random_move == 3 and h != 1 and h != 5 and h != 8:
            temp_state = state[h]
            state[h] = state[h+1]
            state[h+1] = temp_state
        i += 1
    return tuple(state)

# my_manhattan is the manhattan heuristic
my_max_manhattan = 0 # Hold max value for testing/other possible purposes
def my_manhattan(node):
    goal = (1,2,3,4,5,6,7,8,0)
    global my_max_manhattan
    cost = 0
    state = node.state
    #display(state)

    for j in range(0,8): #Check cost for every piece
        goal_value = goal[j]
        current_value = node.state[j]

        # I thought of this as an integer game where we move-
        # left/up to reduce value, right/down to increase it
        while (current_value != goal_value): 
            if current_value == 0: #Ignore 0
                break
            elif current_value >= goal_value + 3: 
                current_value = current_value - 3 # Move Up
                cost += 1
            elif current_value > goal_value:
                current_value = current_value - 1 # Move Left
                cost += 1
            elif current_value <= goal_value - 3: 
                current_value = current_value + 3 # Move Down
                cost += 1
            elif current_value < goal_value:
                current_value = current_value + 1 # Move Right
                cost += 1

    if my_max_manhattan < cost: # Hold max_manhattan for future use, if needed
        my_max_manhattan = cost
    return cost # Cost is the cost of moving to where we want to go

# my_misplaced is the misplaced tile heuristic
my_max_misplaced = 0
def my_misplaced(node):
    
    global my_max_misplaced
    goal = (1,2,3,4,5,6,7,8,0)
    total_misplaced = 0
    for i in range(0,len(goal)): # From 0 to 8
        current_value = node.state[i] # Current value is equal to node we're looking at
        if current_value == 0:
            pass 
        elif(current_value != goal[i]): # Is this node misplaced?
            total_misplaced += 1 # Since it's misplaced store the value
    if(my_max_misplaced <= total_misplaced):
        my_max_misplaced = total_misplaced

    return total_misplaced

# Max heuristic
def my_max_both(node):
    return max((my_misplaced(node)), (my_manhattan(node))) # Return the max between the two other heuristics
        
# Implemented the same as search.py to get the frontier_pops
frontier_pop_counter = 0
def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    global frontier_pop_counter
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        frontier_pop_counter += 1
        node = frontier.pop()
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

# Implemented the same as search.py to track certain things when testing
def my_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

#  -------------------- BEGIN MAIN ------------------------
os.system('clear') # A clean terminal is a happy terminal

''' This code is used to run the EightPuzzle algorithm
print("Begin Eight--------------------------\n")
i = 0
while i < 10: 
    #state = (5,0,8,4,2,1,7,3,6)


    # THIS IS FOR EIGHTPUZZLE
    state = make_rand_8puzzle() # Make a random puzzle
    the_puzzle = EightPuzzle(initial = state)
    if False == the_puzzle.check_solvability(state): # Check for errors, no longer required
        print("ERROR")

    temp_node = Node(state)

    display(state) # Display Initial state
    
    time1 = time.time()
    misplaced_node = my_astar_search(the_puzzle, my_misplaced) # Run the algorithm for misplaced tile heuristic
    time2 = time.time()
    how_long = time2 - time1 # Determine how long the algorithm took

    # Below is print for results, some aren't as necessary as others
    print("MISPLACED: ", "Path Cost,", misplaced_node.path_cost,\
    ', frontier ', frontier_pop_counter, ', time ', how_long,\
    'max Man', my_max_manhattan, 'max Mis', my_max_misplaced)
    frontier_pop_counter = 0

    time1 = time.time()
    manhattan_node = my_astar_search(the_puzzle, my_manhattan) # Run the algorithm for manhattan heuristic
    time2 = time.time()
    how_long = time2 - time1
    print("MANHATTEN: ","Path Cost,", manhattan_node.path_cost,\
    ', frontier ', frontier_pop_counter, ', time ', how_long,\
    'max Man', my_max_manhattan, 'max Mis', my_max_misplaced)
    frontier_pop_counter = 0

    time1 = time.time()
    max_node = my_astar_search(the_puzzle, my_max_both) # Run the algorithm for max heuristic
    time2 = time.time()
    how_long = time2 - time1
    print("MAX: ","Path Cost,", max_node.path_cost,\
    ', frontier ', frontier_pop_counter, ', time ', how_long,\
    'max Man', my_max_manhattan, 'max Mis', my_max_misplaced)
    frontier_pop_counter = 0 # FORGOT THIS OOPS
    i+=1
    print("\n---------------------------- End Eight")
'''
''' This code is for DuckPuzzle
i = 0
while i < 10: 
    print("Begin Duck --------------------------\n")
    #This is for Duck
    state = make_rand_duckpuzzle() # Make random puzzle for DuckPuzzle

    the_puzzle = DuckPuzzle(initial = state)

    temp_node = Node(state)
    display_duck(state) # Display intial state


    time1 = time.time()
    misplaced_node = my_astar_search(the_puzzle, my_misplaced) # Run the algorithm for misplaced tile heuristic
    time2 = time.time()
    how_long = time2 - time1
    print("MISPLACED: ","Path Cost,", misplaced_node.path_cost,\
    ', frontier ', frontier_pop_counter, ', time ', how_long,\
    'max Man', my_max_manhattan, 'max Mis', my_max_misplaced)
    frontier_pop_counter = 0

    time1 = time.time()
    manhatten_node = my_astar_search(the_puzzle, my_manhattan) # Run the algorithm for manhattan heuristic
    time2 = time.time()
    how_long = time2 - time1
    print("MANHATTEN: ","Path Cost,", manhatten_node.path_cost,\
    ', frontier ', frontier_pop_counter, ', time ', how_long,\
    'max Man', my_max_manhattan, 'max Mis', my_max_misplaced)
    frontier_pop_counter = 0

    time1 = time.time()
    max_node = my_astar_search(the_puzzle, my_max_both) # Run the algorithm for max heuristic
    time2 = time.time()
    how_long = time2 - time1
    print("MAX: ","Path Cost,", max_node.path_cost,\
    ', frontier ', frontier_pop_counter, ', time ', how_long,\
    'max Man', my_max_manhattan, 'max Mis', my_max_misplaced)
    frontier_pop_counter = 0
    i += 1
    print("\n---------------------------- End Duck")
'''
# -------------------------------------- END MAIN