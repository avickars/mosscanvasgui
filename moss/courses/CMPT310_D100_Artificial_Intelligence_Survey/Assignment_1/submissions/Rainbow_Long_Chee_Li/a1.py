# a1.py

from search import *
import random
import time

# dictionary for the EightPuzzle manhattan distance table
tableDictionary = {
    '1': (
    0, 1, 2,
    1, 2, 3,
    2, 3, 4
    ),
    '2': (
    1, 0, 1,
    2, 1, 2,
    3, 2, 3
    ),
    '3': (
    2, 1, 0,
    3, 2, 1,
    4, 3, 2
    ),
    '4': (
    1, 2, 3,
    0, 1, 2,
    1, 2, 3
    ),
    '5': (
    2, 1, 2,
    1, 0, 1,
    2, 1, 2
    ),
    '6': (
    3, 2, 1,
    2, 1, 0,
    3, 2, 1
    ),
    '7': (
    2, 3, 4,
    1, 2, 3,
    0, 1, 2
    ),
    '8': (
    3, 2, 3,
    2, 1, 2,
    1, 0, 1
    ),
    '0': (
    4, 3, 2,
    3, 2, 1,
    2, 1, 0
    )
}

# dictionary for the DuckPuzzle Manhattan distance table:
# -1 represents a blocked tile (inaccessible)
duckDictionary = {
    '1': (
    0, 1, -1, -1,
    1, 2, 3, 4,
    -1, 3, 4, 5
    ),
    '2': (
    1, 0, -1, -1,
    2, 1, 2, 3,
    -1, 2, 3, 4
    ),
    '3': (
    1, 1, -1, -1,
    0, 1, 2, 3,
    -1, 2, 3, 4
    ),
    '4': (
    2, 1, -1, -1,
    1, 0, 1, 2,
    -1, 1, 2, 3
    ),
    '5': (
    3, 2, -1, -1,
    2, 1, 0, 1,
    -1, 2, 1, 2
    ),
    '6': (
    4, 3, -1, -1,
    3, 2, 1, 0,
    -1, 3, 2, 1
    ),
    '7': (
    3, 2, -1, -1,
    2, 1, 2, 3,
    -1, 0, 1, 2
    ),
    '8': (
    4, 3, -1, -1,
    3, 2, 1, 2,
    -1, 1, 0, 1
    ),
    '0': (
    5, 4, -1, -1,
    4, 3, 2, 1,
    -1, 2, 1, 0
    )
}



# QUESTION 3:
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 4x3 board, where one of the
    squares is a blank, and there are tiles (denoted as -1) where the tiles cannot be moved to. 
    A state is represented as a tuple of length 12, where  element at
    index i represents the tile number  at index i (0 if it's an empty square, 
    -1 if it's an unaccessible square) """

    def __init__(self, initial, goal=(1, 2, -1, -1, 3, 4, 5, 6, -1, 7, 8, 0)):
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
        not_left = [0, 4, 9]
        not_right = [1, 7, 11]
        not_up = [0, 1, 6, 7]
        not_down = [4, 9, 10, 11]
        index_blank_square = self.find_blank_square(state)

        if index_blank_square in not_left:
            possible_actions.remove('LEFT')
        if index_blank_square in not_up:
            possible_actions.remove('UP')
        if index_blank_square in not_right:
            possible_actions.remove('RIGHT')
        if index_blank_square in not_down:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    # NOTE: in the may 27 lecture, the prof said we don't need to put in the check_solvability, so...
    #def check_solvability(self, state)

    # since i'm using '-1' to represent blocked tiles, the heuristic will still work as intended
    # as the '-1' should always be in the same spots, and (-1) != (-1) returns 0
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))
            
    # NOTE: in the may 29 lecture, someone mentioned that the default heuristic function includes '0'.
    # Due to this, I also included the '0' in my manhattan
    def manhattan(self, node):
        distanceSum = 0

        for x in range(0, 9):
            index = node.state.index(x)
            table = duckDictionary.get(str(x))
            distance = table[index]
            distanceSum += distance

        return distanceSum

    def max(self, node):
        distanceSum = 0

        for x in range(0, 9):
            index = node.state.index(x)
            table = duckDictionary.get(str(x))
            distance = table[index]
            distanceSum += distance

        manhattan_val = distanceSum
        default_val = sum(s != g for (s, g) in zip(node.state, self.goal))

        if (manhattan_val > default_val):
            return manhattan_val
        return default_val

def rand_duck_puzzle():
    state = (1, 2, -1, -1, 3, 4, 5, 6, -1, 7, 8, 0)
    duck_puzzle = DuckPuzzle(state)
    randInt = random.randint(10, 50)
    previous = ''
    choice = 'FILLER'

    for x in range(randInt):
        # get random choice from possible actions
        allChoices = duck_puzzle.actions(state)
        choice = random.choice(allChoices)

        # mod to account for list size
        if (choice is previous):
            choice = allChoices[ (allChoices.index(previous)+1) % len(allChoices)]

        # account for previous choice (prevent * from moving back to previous spot)
        if (choice is 'DOWN'):
            previous = 'UP'        
        if (choice is 'UP'):
            previous = 'DOWN'  
        if (choice is 'LEFT'):
            previous = 'RIGHT'        
        if (choice is 'RIGHT'):
            previous = 'LEFT'  

        state = duck_puzzle.result(state, choice)

    # did not check for solvability because prof said we don't need it for DuckPuzzle
    # if (duck_puzzle.check_solvability(state) is False):

    duck_puzzle.initial = state

    return duck_puzzle

# Print out a readable state of a DuckPuzzle
def display_duck(state):
    #convert state to list to change 0 to *
    newState = list(state)
    zero = newState.index(0)
    newState[zero] = '*'
    state = tuple(newState)
    string = "{state[0]} {state[1]}\n{state[4]} {state[5]} {state[6]} {state[7]}\n  {state[9]} {state[10]} {state[11]}"
    
    print(string.format(state=state))



# QUESTION 1:
# Adjusted EightPuzzle class, added manhattan heuristic
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
            
    # NOTE: in the may 29 lecture, someone mentioned that the default heuristic function includes '0'.
    # Due to this, I also included the '0' in my manhattan
    def manhattan(self, node):
        distanceSum = 0

        for x in range(0, 9):
            index = node.state.index(x)
            table = tableDictionary.get(str(x))
            distance = table[index]
            distanceSum += distance

        return distanceSum

    def max(self, node):
        distanceSum = 0

        for x in range(0, 9):
            index = node.state.index(x)
            table = tableDictionary.get(str(x))
            distance = table[index]
            distanceSum += distance

        manhattan_val = distanceSum
        default_val = sum(s != g for (s, g) in zip(node.state, self.goal))

        if (manhattan_val > default_val):
            return manhattan_val
            
        return default_val


# create and return a random, solvable EightPuzzle 
def make_rand_8puzzle():
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = EightPuzzle(state)
    randInt = random.randint(10, 50)
    previous = ''
    choice = 'FILLER'

    for x in range(randInt):
        # get random choice from possible actions
        allChoices = puzzle.actions(state)
        choice = random.choice(allChoices)

        # mod to account for list size
        if (choice is previous):
            choice = allChoices[ (allChoices.index(previous)+1) % len(allChoices)]

        # account for previous choice (prevent * from moving back to previous spot)
        if (choice is 'DOWN'):
            previous = 'UP'        
        if (choice is 'UP'):
            previous = 'DOWN'  
        if (choice is 'LEFT'):
            previous = 'RIGHT'        
        if (choice is 'RIGHT'):
            previous = 'LEFT'  

        state = puzzle.result(state, choice)

    # shouldn't be triggered ever since we start from a solved board, but here for coverage
    if (puzzle.check_solvability(state) is False):
        return ValueError("Failed to create solvable random EightPuzzle")

    puzzle.initial = state
    return puzzle

# Print out a readable state of an EightPuzzle
def display(state):
    #convert state to list to change 0 to *
    newState = list(state)
    zero = newState.index(0)
    newState[zero] = '*'
    state = tuple(newState)
    string = "{state[0]} {state[1]} {state[2]}\n{state[3]} {state[4]} {state[5]}\n{state[6]} {state[7]} {state[8]}"
    
    print(string.format(state=state))



# QUESTION 2:
# changed to print out info
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
    count = 0
    while frontier:
        node = frontier.pop()
        count += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print("Length of solution: ", node.path_cost)
            print("Total # of Nodes removed from frontier: ", count)
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

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)



# check time for default heuristic
def default_time(rand_puzzle):
    print('\n===== Default heuristic: =====')
    start_time = time.time()

    if (type(rand_puzzle) is DuckPuzzle):
        display_duck(rand_puzzle.initial)
    else:
        display(rand_puzzle.initial)
        print('This may take a while... Please wait.')

    astar_search(rand_puzzle, rand_puzzle.h)

    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s')

# check time for manhattan heuristic
def manhattan_time(rand_puzzle):
    print('\n===== Manhattan heuristic: =====')
    start_time = time.time()

    if (type(rand_puzzle) is DuckPuzzle):
        display_duck(rand_puzzle.initial)
    else:
        display(rand_puzzle.initial)

    astar_search(rand_puzzle, rand_puzzle.manhattan)

    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s')

# check time for max heuristic
def max_time(rand_puzzle):
    print('\n===== Max of default and manhattan heuristic: =====')
    start_time = time.time()

    if (type(rand_puzzle) is DuckPuzzle):
        display_duck(rand_puzzle.initial)
    else:
        display(rand_puzzle.initial)

    astar_search(rand_puzzle, rand_puzzle.max)

    elapsed_time = time.time() - start_time
    print(f'Elapsed time (in seconds): {elapsed_time}s\n')



# used to create 10 random 8 puzzles, and print the results for them
def eight_puzzle_test():
    for x in range(0, 10):
        rand8puzzle = make_rand_8puzzle()

        default_time(rand8puzzle)
        manhattan_time(rand8puzzle)
        max_time(rand8puzzle)

# used to create 10 random duck puzzles, and print the results for them
def duck_puzzle_test():
    for x in range(0, 10):
        randDuckPuzzle = rand_duck_puzzle()

        default_time(randDuckPuzzle)
        manhattan_time(randDuckPuzzle)
        max_time(randDuckPuzzle)



# Run these to run 10 tests for each
eight_puzzle_test()
duck_puzzle_test()