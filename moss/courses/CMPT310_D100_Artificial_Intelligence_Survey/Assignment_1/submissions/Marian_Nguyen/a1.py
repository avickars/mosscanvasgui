# a1.py
# Name: Marian Nguyen
# Student number: 301312581

import random
import time
from search import Problem, Node, memoize, PriorityQueue

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
    # added nodes removed 
    nodeRemoved = 0
    while frontier:
        node = frontier.pop()
        nodeRemoved += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, nodeRemoved]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
        
    return None

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
        return sum(s != g for (s, g) in zip(node.state, self.goal)) - 1

    def manhattanDistance(self, node):
        state = node.state

        goal = {1:[0,2], 2:[1,2], 3:[2,2], 4:[0,1],5:[1,1],6:[2,1], 7:[0,0], 8:[1,0],0:[2,0]}
        index_state = {}
        index = [[0,2], [1,2], [2,2], [0,1], [1,1], [2,1], [0,0], [1,0], [2,0]]
        dist = 0

        for i in range(len(state)):
            index_state[state[i]] = index[i]
        
        for i in range(8):
           dist += (abs(goal[i][0] - index_state[i][0])) + (abs(goal[i][1] - index_state[i][1]))
        return (dist)
    
    def maxHeuristic(self, node):
        return (max(self.h(node), self.manhattanDistance(node)))
class DuckPuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        self.goal = goal
        Problem.__init__(self, initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        # indexes grouped together according to the illegal moves
        noUp = (0,1,4,5)
        noDown = (2,6,7,8)
        noLeft = (0,2,6)
        noRight = (1,5,8)

        if index_blank_square in noUp:
            possible_actions.remove('UP')
        if index_blank_square in noDown:
            possible_actions.remove('DOWN')
        if index_blank_square in noLeft:
            possible_actions.remove('LEFT')
        if index_blank_square in noRight:
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # indexes that only need two up or down to get to their wanted destination taken into account
        deltaOther = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        blankOther = (0,1,2,3)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank in blankOther:
            neighbor = blank + deltaOther[action]
        else:
            neighbor = blank + delta[action]

        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    # subtracting 1 to remove the 0
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        return sum(s != g for (s, g) in zip(node.state, self.goal)) - 1

    def manhattanDistance(self, node):
        state = node.state
        # the indexes of the goal location depending on the tile not including zero
        goal = {1:[0,2], 2:[1,2], 3:[0,1], 4:[1,1],5:[2,1],6:[3,1], 7:[1,0], 8:[2,0], 0:[3,0]}
        index_state = {}
    
        index = [[0,2], [1,2], [0,1], [1,1], [2,1], [3,1], [1,0], [2,0], [3,0]]
        dist = 0

        for i in range(len(state)):
            index_state[state[i]] = index[i]
        # manhattan calculation 
        for i in range(8):
           dist += (abs(goal[i][0] - index_state[i][0])) + (abs(goal[i][1] - index_state[i][1]))
        return (dist)
    
    def maxHeuristic(self, node):
        return (max(self.h(node), self.manhattanDistance(node)))

def make_rand_8puzzle():
    puzzleBlock = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    solvabilityCheck = False
    while not solvabilityCheck:
        # shuffling the numbers in the puzzle block to create random puzzles
        random.shuffle(puzzleBlock)
        puzzleTuple = tuple(puzzleBlock)
        fullPuzzle = EightPuzzle(puzzleTuple)
        solvabilityCheck = fullPuzzle.check_solvability(puzzleTuple)
    
    fullPuzzle = EightPuzzle(puzzleTuple)

    return fullPuzzle

def display(state):
    stateDisplay = [0,0,0,0,0,0,0,0,0]
    # displaying eight puzzle
    for x in range(9):
        stateDisplay[x] = state[x]
        if (stateDisplay[x] == 0):
            stateDisplay[x] = "*"
    print(stateDisplay[0],stateDisplay[1],stateDisplay[2])
    print(stateDisplay[3],stateDisplay[4],stateDisplay[5])
    print(stateDisplay[6],stateDisplay[7],stateDisplay[8])

def make_rand_Duckpuzzle():
    puzzleBlock = [2, 3, 0, 1, 7, 5, 4, 6, 8]
    duck_puzzle = DuckPuzzle(puzzleBlock)
    i = random.randint(1, 500000)
    
    # create randoms instances using goal state and legal actions
    for j in range(i): 
        possible_actions = duck_puzzle.actions(puzzleBlock)
        k = random.randint(0, len(possible_actions) - 1)
        puzzleBlock = duck_puzzle.result(puzzleBlock, possible_actions[k])
    
    duck_puzzle = DuckPuzzle(puzzleBlock)

    return duck_puzzle

def displayDuckPuzzle(state):
    stateDisplay = [0,0,0,0,0,0,0,0,0]

    # displaying duck puzzle 
    for x in range(9):
        stateDisplay[x] = state[x]
        if (stateDisplay[x] == 0):
            stateDisplay[x] = "*"
    print(stateDisplay[0],stateDisplay[1], " ", " ")
    print(stateDisplay[2],stateDisplay[3],stateDisplay[4],stateDisplay[5])
    print(" ", stateDisplay[6],stateDisplay[7],stateDisplay[8])

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def astar_searchManhattan(problem, h=None):
    h = memoize(h or problem.manhattanDistance, 'h')

    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

def astar_searchMaxHeuristic(problem, h=None):
    h = memoize(h or problem.maxHeuristic, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


print ("*************************************")
print("START OF ANALYSIS")
print ("*************************************""\n")

# running interations in groups of 5
for i in range(5):
    puzzle = make_rand_8puzzle()
    display(puzzle.initial)
    print("\n")
    print("8-Puzzle Analysis using Misplaced Tile")
    start_time = time.time()
    result = astar_search(puzzle)
    total_time = time.time() - start_time
    print(f'total time (in seconds): {total_time}s')
    print("the length of the solution: ", result[0].path_cost)
    print ("# of nodes removed from frontier is: ",result[1], "\n")

    print("8-Puzzle Analysis using Manhattan Distance Heuristic")
    start_time_Man = time.time()
    result_Man = astar_searchManhattan(puzzle)
    total_time_Man = time.time() - start_time_Man
    print(f'total time (in seconds): {total_time_Man}s')
    print("the length of the solution: ", result_Man[0].path_cost)
    print ("# of nodes removed from frontier is: ",result_Man[1], "\n")

    print("8-Puzzle Analysis using Max Heuristic")
    start_time_Max = time.time()
    result_Max = astar_searchMaxHeuristic(puzzle)
    total_time_Max = time.time() - start_time_Max
    print(f'total time (in seconds): {total_time_Max}s')
    print("the length of the solution: ", result_Max[0].path_cost)
    print ("# of nodes removed from frontier is: ",result_Max[1], "\n")
    print("********************************************")

for i in range(5):
    
    duck_start_time = time.time()
    duck_puzzle = make_rand_Duckpuzzle()
    duck_result = astar_search(duck_puzzle)
    duck_total_time = time.time() - duck_start_time
    displayDuckPuzzle(duck_puzzle.initial)
    print("\n")
    print("Duck-Puzzle Analysis using Misplaced Tile")
    print(f'total time (in seconds): {duck_total_time}s')
    print("the length of the solution: ", duck_result[0].path_cost)
    print ("# of nodes removed from frontier is: ",duck_result[1], "\n")

    print("Duck-Puzzle Analysis using Manhattan Distance Heuristic")
    duck_start_time_Man = time.time()
    duck_result_Man = astar_searchManhattan(duck_puzzle)
    duck_total_time_Man = time.time() - duck_start_time_Man
    print(f'total time (in seconds): {duck_total_time_Man}s')
    print("the length of the solution: ", duck_result_Man[0].path_cost)
    print ("# of nodes removed from frontier is: ",duck_result_Man[1], "\n")

    print("Duck-Puzzle Analysis using Max Heuristic")
    duck_start_time_Max = time.time()
    duck_result_Max = astar_searchMaxHeuristic(duck_puzzle)
    duck_total_time_Max = time.time() - duck_start_time_Max
    print(f'total time (in seconds): {duck_total_time_Max}s')
    print("the length of the solution: ", duck_result_Max[0].path_cost)
    print ("# of nodes removed from frontier is: ",duck_result_Max[1], "\n")
    print("********************************************")

print ("*************************************")
print("END OF ANALYSIS""\n")
print ("*************************************")