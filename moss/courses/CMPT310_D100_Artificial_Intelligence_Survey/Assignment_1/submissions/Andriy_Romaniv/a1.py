from search import *
from random import *
import time

# ______________________________________________________________________________ Start of Duck Puzzle Class

class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a duck shape board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number at index i (0 if it's an empty square) 
    
    Goal State:
    1 2 
    3 4 5 6
      7 8  * 
    """

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
        
        #positions that have restricted number of moves
        restricted_up = [0, 1, 4, 5]
        restricted_down = [2, 6, 7, 8]
        restricted_left = [0, 2, 6]
        restricted_right = [1, 5, 8]

        if index_blank_square in restricted_up:
            possible_actions.remove('UP')
        if index_blank_square in restricted_down:
            possible_actions.remove('DOWN')
        if index_blank_square in restricted_left:
            possible_actions.remove('LEFT')
        if index_blank_square in restricted_right:
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        #positions that have modified vertical moves 
        duck_head = [0, 1, 2]
        duck_neck = [3]

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        
        if blank in duck_head:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}

        if blank in duck_neck:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


# ______________________________________________________________________________ End of Duck Puzzle Class

# ______________________________________________________________________________ Start of Eight Puzzle support methods

def make_rand_8puzzle():
    """
	Returns solvable 8 puzzle problem. This method is using check_solvability() to ensure correctness of the puzzle.
	""" 
    tupleValues = []

    while True:
        for i in range(9):
            value = randint(0,8)
            while value in tupleValues:
                value = randint(0,8)
            tupleValues.append(value)

        valuesT = (tupleValues[0], tupleValues[1], tupleValues[2], tupleValues[3], tupleValues[4], tupleValues[5], tupleValues[6], tupleValues[7], tupleValues[8])
        puzzle = EightPuzzle(valuesT)

        if puzzle.check_solvability(puzzle.initial):
            break
        tupleValues.clear() 

    return puzzle


def display(state):
    """
	Displays 8 puzzle instance in a readable form:
    1 2 3
    4 5 6
    7 8 *
	""" 
    dispValues = []
    for i in range(9):
        if state[i] == 0:
            dispValues.append("*")
        else:
            dispValues.append(state[i])

    print (dispValues[0], dispValues[1], dispValues[2])
    print (dispValues[3], dispValues[4], dispValues[5])
    print (dispValues[6], dispValues[7], dispValues[8], "\n")

# ______________________________________________________________________________ End of Eight Puzzle support methods

# ______________________________________________________________________________ Start of Duck Puzzle support methods


def make_rand_duck_puzzle():
    """
	Returns solvable duck puzzle problem. This method starts with a goal state and makes 200 random moves. This ensures correctness of the puzzle.
	""" 
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = DuckPuzzle(state)

    for i in range(200):
        actions = puzzle.actions(state)
        j = randint(0, len(actions)-1)
        state = puzzle.result(state, actions[j])
        puzzle = DuckPuzzle(state)
    
    return puzzle

def displayDuck(state):
    """
    Displays duck puzzle instance in a readable form:
    1 2
    3 4 5 6
      7 8 *
    """ 
    dispValues = []

    for i in range(9):
        if state[i] == 0:
            dispValues.append("*")
        else:
            dispValues.append(state[i])

    print (dispValues[0], dispValues[1])
    print (dispValues[2], dispValues[3], dispValues[4], dispValues[5])
    print (" ",dispValues[6], dispValues[7], dispValues[8], "\n")
    
# ______________________________________________________________________________ End of Duck Puzzle support methods

# ______________________________________________________________________________ Start of sthared search methods  

def h(node):
    """ Return the heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles """
    goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    return sum(s != g and s !=0 for (s, g) in zip(node.state, goal))

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned.
    
    Method was taken from "\search.py and modified to return the number of
    nodes that were removed from frontier"
    """
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    count = 0
    while frontier:
        node = frontier.pop()
        #increment a counter of the number of nodes that were removed from frontie
        count = count + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return (node, count)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

# ______________________________________________________________________________ End of shared search methods

# ______________________________________________________________________________ Start of Eight Puzzle heuristic implementation   

def manhattan_EightPuzzle(node):
    """
    Manhattan heuristic value is calculated as a sum of all manhattan distandes for the given state,
    comparing to the goal state.
    Basic logic of this method was sourced from "/test_search.py", but the manhattan sum formula was modified
    """
    state = node.state
    index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        
    for i in range(len(state)):
        index_state[state[i]] = index[i]
    
    manhattan_sum = 0
        
    for i in range(1, 9):
            manhattan_sum += abs(index_state[i][0] - index_goal[i][0]) + abs(index_state[i][1] - index_goal[i][1])
            
    return manhattan_sum

def maxHeuristic_EightPuzzle(node):
    """
    Return the mmaximum value between misplaced heuristic and manhattan heurisitic
    """
    return (max(h(node), manhattan_EightPuzzle(node)))

def astar_search_manhattan_EightPuzzle(problem, h=None, display=False):
    """
    A*-search using value of manhattan heurisitic 
    """
    h = memoize(h or manhattan_EightPuzzle, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def astar_search_max_heuristic_EightPuzzle(problem, h=None):
    """
    A*-search using maximum value between misplaced heuristic and manhattan heurisitic 
    """
    h = memoize(h or maxHeuristic_EightPuzzle, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


# ______________________________________________________________________________ End of Eight Puzzle heuristic implementation 

# ______________________________________________________________________________ Start of Duck Puzzle heuristic implementation

def manhattan_DuckPuzzle(node):
    """
    Manhattan heuristic value is calculated as a sum of all manhattan distandes for the given state,
    comparing to the goal state.
    Basic logic of this method was sourced from "/test_search.py", but the manhattan sum formula was modified
    """
    state = node.state
    index_goal = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
    index_state = {}
    index = [[0,0], [0,1], [1, 0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
        
    for i in range(len(state)):
        index_state[state[i]] = index[i]
    
    manhattan_sum = 0
        
    for i in range(1, 9):
        manhattan_sum = manhattan_sum + abs(index_state[i][0] - index_goal[i][0]) + abs(index_state[i][1] - index_goal[i][1])
        
    return manhattan_sum

def maxHeuristic_DuckPuzzle(node):
    """
    Return the mmaximum value between misplaced heuristic and manhattan heurisitic
    """
    return (max(h(node), manhattan_DuckPuzzle(node)))

def astar_search_manhattan_DuckPuzzle(problem, h=None, display=False):
    """
    A*-search using value of manhattan heurisitic 
    """
    h = memoize(h or manhattan_DuckPuzzle, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def astar_search_max_heuristic_DuckPuzzle(problem, h=None):
    """
    A*-search using maximum value between misplaced heuristic and manhattan heurisitic 
    """

    h = memoize(h or maxHeuristic_DuckPuzzle, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

# ______________________________________________________________________________ End of Duck Puzzle heuristic implementation 

# ______________________________________________________________________________ Start of Duck Puzzle analysis


print ("Comparing Algorithms for Duck-puzzle issues:", "\n")

for i in range(10):
    print ("Start of analysis for instance #" + str(i+1), "\n")
    puzzle = make_rand_duck_puzzle()
    displayDuck(puzzle.initial)

    start_time = time.time()
    result = astar_search_manhattan_DuckPuzzle(puzzle)
    run_time = time.time() - start_time

    print ("A* using the Manhattan distance heuristic")
    print ("Path cost: ", result[0].path_cost)
    print ("Nodes removed: ", result[1])
    print ("Run time: ", run_time, "\n")

    start_time = time.time()
    result = astar_search(puzzle)
    run_time = time.time() - start_time

    print ("A* using the misplaced tile heuristic")
    print ("Path cost: ", result[0].path_cost)
    print ("Nodes removed: ", result[1])
    print ("Run time: ", run_time, "\n")

    start_time = time.time()
    result = astar_search_max_heuristic_DuckPuzzle(puzzle)
    run_time = time.time() - start_time

    print ("A* using the max heuristic")
    print ("Path cost: ", result[0].path_cost)
    print ("Nodes removed: ", result[1])
    print ("Run time: ", run_time, "\n")


    print ("End of analysis for instance #" + str(i+1), "\n")
    print("-------------------------------------------", "\n")

# ______________________________________________________________________________ End of Duck Puzzle analysis 

# ______________________________________________________________________________ Start of Eight Puzzle analysis

    
print ("Comparing Algorithms for 8-puzzle issues:", "\n")

for i in range(10):
    print ("Start of analysis for instance #" + str(i+1), "\n")
    puzzle = make_rand_8puzzle()
    display(puzzle.initial)

    start_time = time.time()
    result = astar_search_manhattan_EightPuzzle(puzzle)
    run_time = time.time() - start_time

    print ("A* using the Manhattan distance heuristic")
    print ("Path cost: ", result[0].path_cost)
    print ("Nodes removed: ", result[1])
    print ("Run time: ", run_time, "\n")

    start_time = time.time()
    result = astar_search(puzzle)
    run_time = time.time() - start_time

    print ("A* using the misplaced tile heuristic")
    print ("Path cost: ", result[0].path_cost)
    print ("Nodes removed: ", result[1])
    print ("Run time: ", run_time, "\n")

    start_time = time.time()
    result = astar_search_max_heuristic_EightPuzzle(puzzle)
    run_time = time.time() - start_time

    print ("A* using the max heuristic")
    print ("Path cost: ", result[0].path_cost)
    print ("Nodes removed: ", result[1])
    print ("Run time: ", run_time, "\n")

    print ("End of analysis for instance #" + str(i+1), "\n")
    print("-------------------------------------------", "\n")

# ______________________________________________________________________________ End of Eight Puzzle analysis
