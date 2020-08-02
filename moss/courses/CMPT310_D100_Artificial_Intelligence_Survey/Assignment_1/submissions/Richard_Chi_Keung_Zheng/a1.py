# a1.py
# By: Richard Zheng (301289827)

# Notes:
# - The functions best_first_graph_search and astar_search were copied over from search.py since I needed to modify them to meet the assignment requirements
# - EightPuzzle class was copied over from search.py to modify the default heuristic (misplaced tile) to not include the blank tile (the 0) in its calculations, as that is how the textbook defines it
# - The DuckPuzzle Class is a modified version of the EightPuzzle, which was copied over from search.py
# - My implementation of the Manhattan Distance heuristic uses the same idea as the manhattan function found in tests/test_search.py and search.ipynb files
#   - It uses a list of tuples to indicate the positions for each tiles, so for the EightPuzzle I used a 3x3 grid, while for the DuckPuzzle, I used a 4x3 grid
#   - There are two different functions for manhattan heuristics and max heuristics for EightPuzzle and DuckPuzzle due to the differences in the representation of the grids
# - There are some links in regards to where I looked up code snippets or learned of certain functions or methods to get things done
# - For the running times, I rounded them to 5 decimal points, as that seems to be enough decimal points to compare the heuristics thoroughly

from search import *
import random # Using this library to shuffle a list and generate random numbers within a range, referenced: https://docs.python.org/3/library/random.html
import time
import statistics # This is used for finding means and medians as referenced here: https://docs.python.org/3/library/statistics.html

# First two functions are for question 1 of assignment 1
def make_rand_8puzzle():
    list8 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    solvable = False
    puzzle = EightPuzzle((1,2,3,4,5,6,7,8,0))

    while (not solvable):
        random.shuffle(list8)
        random_tuple = tuple(list8) # Converting list to a tuple: https://www.geeksforgeeks.org/tuples-in-python/ (Referenced the "Converting list to a Tuple" section)

        if (puzzle.check_solvability(random_tuple)):
            solvable = True
            puzzle.initial = random_tuple
            return puzzle

def display(state):
    for x in range (0, 9, 3):
        if (state[x] == 0):
            print("*  {}  {}".format(state[x+1], state[x+2]))
        elif (state[x+1] == 0):
            print("{}  *  {}".format(state[x], state[x+2]))
        elif (state[x+2] == 0):
            print("{}  {}  *".format(state[x], state[x+1]))
        else:
            print("{}  {}  {}".format(state[x], state[x+1], state[x+2]))

# This implementation starts from the goal state and randomly makes 1000 valid moves to shuffle the puzzle
# This will always generate a solvable puzzle, so the check_solvability function was unused and unmodified for my DuckPuzzle implementation
def make_rand_duckPuzzle():
    shuffles = 1000
    movesMade = 0
    puzzle = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))
    puzzle.state = puzzle.initial

    while (movesMade < shuffles):
        possibleMoves = puzzle.actions(puzzle.state)
        moveToMake = random.randrange(0, len(possibleMoves))
        puzzle.state = puzzle.result(puzzle.state, possibleMoves[moveToMake])
        movesMade += 1

    return DuckPuzzle(puzzle.state)

# Separate display function from the one above, as the DuckPuzzle has a unique shape
def displayDuck(state):
    itemsPerRow = [2, 4, 3]
    index = 0
    for x in range(len(itemsPerRow)):
        if x == 2:
            print("   ", end='')
        for y in range(itemsPerRow[x]):
            if state[index + y] == 0:
                print("*  ", end='')
            else:
                print(state[index + y], " ", end='')
        print("")
        index += itemsPerRow[x]


# Modified to return the number of nodes removed from frontier
# Returns a tuple with the second attribute in the tuple being that counter
# Learned of way to return multiple values here: https://www.geeksforgeeks.org/g-fact-41-multiple-return-values-in-python/
def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    removed = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        removed+=1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, removed # Returning a tuple
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, removed

# Modified the best_first_graph_search function, so had to put this here too
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# ______________________________________________________________________________
# A* heuristics 

# The idea / concept that I used was adopted from manhattan function found in the tests/test_search.py and search.ipynb files
# Can be found here: https://github.com/aimacode/aima-python/blob/master/search.ipynb or https://github.com/aimacode/aima-python/blob/master/tests/test_search.py
def manhattanHeuristic(node):
    distance = 0

    goal_index = [(2,2), (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1)]
    initial_index = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

    for i in range(9):
        currentTile = node.state[i]
        # Skip the blank tile (value 0 in the tuple)
        if (currentTile == 0):
            continue
        currentIndex = initial_index[i]
        desiredIndex = goal_index[currentTile]
        distance = abs(desiredIndex[0] - currentIndex[0]) + abs(desiredIndex[1] - currentIndex[1]) + distance

    return distance

# This is different from the above manhattan distance function because the indices are based on a 4x3 grid instead for a duck puzzle
def manhattanHeuristicForDuck(node):
    distance = 0

    # For DuckPuzzle, I treated the board as a 4x3 grid, but with some of the spots being invalid
    goal_index = [(2,3), (0,0), (0,1), (1,0), (1,1), (1,2), (1,3), (2,1), (2,2)]
    initial_index = [(0,0), (0,1), (1,0), (1,1), (1,2), (1,3), (2,1), (2,2), (2,3)]

    for i in range(9):
        currentTile = node.state[i]
        # Skip the blank tile (value 0 in the tuple)
        if (currentTile == 0):
            continue
        currentIndex = initial_index[i]
        desiredIndex = goal_index[currentTile]
        distance = abs(desiredIndex[0] - currentIndex[0]) + abs(desiredIndex[1] - currentIndex[1]) + distance

    return distance


# Had to place this here for maxHeuristic to call
def misplacedHeuristic(node):
    goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    # Added a check for 0 to ensure that the blank tile isn't included in the sum
    return sum((s != g and s != 0) for (s, g) in zip(node.state, goal))


def maxHeuristic(node):
    manhattan = manhattanHeuristic(node)
    misplaced = misplacedHeuristic(node)

    return max(manhattan, misplaced)

# Separate function for the duck puzzle, as the duck puzzle uses a different manhattan distance function
def maxHeuristicForDuck(node):
    manhattan = manhattanHeuristicForDuck(node)
    misplaced = misplacedHeuristic(node)

    return max(manhattan, misplaced)


# This is copied over from search.py because I had to edit the default Misplaced Tile Heuristic to exclude the blank tile from its calculation
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

        # Edited to exclude the blank tile
        return sum((s != g and s != 0) for (s, g) in zip(node.state, self.goal))


# Class for the third part of the assignment, the code is a modified version of the EightPuzzle class found in search.py
# The modified functions were actions, results, and h (excluding the blank tile in the heuristic calculation)
# The check_solvability function is unused and unmodified
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 duck shaped board, where one of the
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

        # Modified the possible actions based on index of the blank square
        if index_blank_square % 2 == 0 and index_blank_square != 4 and index_blank_square != 8: # Checking for index 0, 2, and 6
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5: # Checking for index 0, 1, 4, and 5
            possible_actions.remove('UP')
        if (index_blank_square % 3 == 2 and index_blank_square != 2) or index_blank_square == 1: # Checking for index 1,5, and 8
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square > 5: # Checking for index 2, 6, 7, and 8
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # Modified the changes in the index based on the moves made on a specific row of the puzzle
        firstRow = [0, 1]
        secondRow = [2, 3, 4, 5]
        thirdRow = [6, 7, 8]

        if blank in firstRow:
            delta = {'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank in secondRow:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    # This function is unused and won't work correctly on a duck puzzle
    # This was left unmodified, as to generate a random duck puzzle, I started from the goal state and made random moves to shuffle the puzzle
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

        # Exclude the blank tile (0) in the calculation
        return sum((s != g and s != 0) for (s, g) in zip(node.state, self.goal))

# This function was implemented to reduce repetitiveness, as the same code will need to be used for both the EightPuzzle and DuckPuzzle
# Function for running A* Search with the 3 heuristics one after the other
# Can be used for EightPuzzle or DuckPuzzle, but the default parameter puzzleType will be set to run the EightPuzzle
# Also has a fourth optional parameter to display statistics (min, max, average, median) if desired, and is set to False by default
def runAlgorithms(puzzles, numberOfPuzzles, puzzleType="Eight", displayStatistics=False):

    # The lists used to capture the data for each algorithm, which will be later used for printing out statistics if parameter set to True
    misplacedTimes = []
    manhattanTimes = []
    maxHeuristicTimes = []

    misplacedSolutionLengths = []
    manhattanSolutionLengths = []
    maxHeuristicSolutionLengths = []

    misplacedNodesRemoved = []
    manhattanNodesRemoved = []
    maxHeuristicNodesRemoved = []

    print("Running A* Search with Misplaced Tile Heuristic...")
    for i in range (numberOfPuzzles):
        print("Solving puzzle {}:".format(i+1))
        if puzzleType == "Eight":
            display(puzzles[i].initial)
            print("")
        else:
            displayDuck(puzzles[i].initial)
            print("")
        start_time = time.time()
        astar_results = astar_search(puzzles[i])
        astar_solution = astar_results[0].solution()
        misplacedTimes.append(round(time.time() - start_time, 5))
        misplacedSolutionLengths.append(len(astar_solution))
        misplacedNodesRemoved.append(astar_results[1])
        print("Running time in seconds: {}".format(misplacedTimes[i]))
        print("Length of solution: {}".format(misplacedSolutionLengths[i]))
        print("Number of Nodes removed from Frontier: {}\n".format(misplacedNodesRemoved[i]))

    # Printing a dotted line to make it easier to spot when another algorithm is starting to run
    print("------------------------------------------------------------------------------------------------------------\n")
    print("Running A* Search with Manhattan Distance Heuristic...")
    for i in range (numberOfPuzzles):
        print("Solving puzzle {}:".format(i+1))
        if puzzleType == "Eight":
            display(puzzles[i].initial)
            print("")
        else:
            displayDuck(puzzles[i].initial)
            print("")
        if (puzzleType == "Eight"):
            start_time = time.time()
            astar_results = astar_search(puzzles[i], manhattanHeuristic)
        else:
            start_time = time.time()
            astar_results = astar_search(puzzles[i], manhattanHeuristicForDuck)
        astar_solution = astar_results[0].solution()
        manhattanTimes.append(round(time.time() - start_time, 5))
        manhattanSolutionLengths.append(len(astar_solution))
        manhattanNodesRemoved.append(astar_results[1])
        print("Running time in seconds: {}".format(manhattanTimes[i]))
        print("Length of solution: {}".format(manhattanSolutionLengths[i]))
        print("Number of Nodes removed from Frontier: {}\n".format(manhattanNodesRemoved[i]))

    # Printing a dotted line to make it easier to spot when another algorithm is starting to run
    print("------------------------------------------------------------------------------------------------------------\n")
    print("Running A* Search with Max Heuristic...")
    for i in range (numberOfPuzzles):
        print("Solving puzzle {}:".format(i+1))
        if puzzleType == "Eight":
            display(puzzles[i].initial)
            print("")
        else:
            displayDuck(puzzles[i].initial)
            print("")
        start_time = time.time()
        if (puzzleType == "Eight"):
            start_time = time.time()
            astar_results = astar_search(puzzles[i], maxHeuristic)
        else:
            start_time = time.time()
            astar_results = astar_search(puzzles[i], maxHeuristicForDuck)
        astar_solution = astar_results[0].solution()
        maxHeuristicTimes.append(round(time.time() - start_time, 5))
        maxHeuristicSolutionLengths.append(len(astar_solution))
        maxHeuristicNodesRemoved.append(astar_results[1])
        print("Running time in seconds: {}".format(maxHeuristicTimes[i]))
        print("Length of solution: {}".format(maxHeuristicSolutionLengths[i]))
        print("Number of Nodes removed from Frontier: {}\n".format(maxHeuristicNodesRemoved[i]))

    if displayStatistics:

        print("Minimum running time when using Misplaced Tile Heuristic: {}".format(min(misplacedTimes)))
        print("Maximum running time when using Misplaced Tile Heuristic: {}".format(max(misplacedTimes)))
        print("Average running time when using Misplaced Tile Heuristic: {}".format(statistics.mean(misplacedTimes)))
        print("Median running time when using Misplaced Tile Heuristic: {}\n".format(statistics.median(misplacedTimes)))

        print("Minimum running time when using Manhattan Distance Heuristic: {}".format(min(manhattanTimes)))
        print("Maximum running time when using Manhattan Distance Heuristic: {}".format(max(manhattanTimes)))
        print("Average running time when using Manhattan Distance Heuristic: {}".format(statistics.mean(manhattanTimes)))
        print("Median running time when using Manhattan Distance Heuristic: {}\n".format(statistics.median(manhattanTimes)))

        print("Minimum running time when using Max Heuristic: {}".format(min(maxHeuristicTimes)))
        print("Maximum running time when using Max Heuristic: {}".format(max(maxHeuristicTimes)))
        print("Average running time when using Max Heuristic: {}".format(statistics.mean(maxHeuristicTimes)))
        print("Median running time when using Max Heuristic: {}\n".format(statistics.median(maxHeuristicTimes)))

        print("Minimum solution length when using Misplaced Tile Heuristic: {}".format(min(misplacedSolutionLengths)))
        print("Maximum solution length when using Misplaced Tile Heuristic: {}".format(max(misplacedSolutionLengths)))
        print("Average solution length when using Misplaced Tile Heuristic: {}".format(statistics.mean(misplacedSolutionLengths)))
        print("Median solution length when using Misplaced Tile Heuristic: {}\n".format(statistics.median(misplacedSolutionLengths)))

        print("Minimum solution length when using Manhattan Distance Heuristic: {}".format(min(manhattanSolutionLengths)))
        print("Maximum solution length when using Manhattan Distance Heuristic: {}".format(max(manhattanSolutionLengths)))
        print("Average solution length when using Manhattan Distance Heuristic: {}".format(statistics.mean(manhattanSolutionLengths)))
        print("Median solution length when using Manhattan Distance Heuristic: {}\n".format(statistics.median(manhattanSolutionLengths)))

        print("Minimum solution length when using Max Heuristic: {}".format(min(maxHeuristicSolutionLengths)))
        print("Maximum solution length when using Max Heuristic: {}".format(max(maxHeuristicSolutionLengths)))
        print("Average solution length when using Max Heuristic: {}".format(statistics.mean(maxHeuristicSolutionLengths)))
        print("Median solution length when using Max Heuristic: {}\n".format(statistics.median(maxHeuristicSolutionLengths)))

        print("Minimum number of nodes removed from frontier when using Misplaced Tile Heuristic: {}".format(min(misplacedNodesRemoved)))
        print("Maximum number of nodes removed from frontier when using Misplaced Tile Heuristic: {}".format(max(misplacedNodesRemoved)))
        print("Average number of nodes removed from frontier when using Misplaced Tile Heuristic: {}".format(statistics.mean(misplacedNodesRemoved)))
        print("Median number of nodes removed from frontier when using Misplaced Tile Heuristic: {}\n".format(statistics.median(misplacedNodesRemoved)))

        print("Minimum number of nodes removed from frontier when using Manhattan Distance Heuristic: {}".format(min(manhattanNodesRemoved)))
        print("Maximum number of nodes removed from frontier when using Manhattan Distance Heuristic: {}".format(max(manhattanNodesRemoved)))
        print("Average number of nodes removed from frontier when using Manhattan Distance Heuristic: {}".format(statistics.mean(maxHeuristicNodesRemoved)))
        print("Median number of nodes removed from frontier when using Manhattan Distance Heuristic: {}\n".format(statistics.median(maxHeuristicNodesRemoved)))

        print("Minimum number of nodes removed from frontier when using Max Heuristic: {}".format(min(maxHeuristicNodesRemoved)))
        print("Maximum number of nodes removed from frontier when using Max Heuristic: {}".format(max(maxHeuristicNodesRemoved)))
        print("Average number of nodes removed from frontier when using Max Heuristic: {}".format(statistics.mean(maxHeuristicNodesRemoved)))
        print("Median number of nodes removed from frontier when using Max Heuristic: {}\n".format(statistics.median(maxHeuristicNodesRemoved)))

# --------------------------------------------------------------- Main ---------------------------------------------------------------------------------------------

numberOfPuzzles = 10
displayStatistics = False

# For Question 2
# Comment out this block if not running algorithms on EightPuzzles
puzzles = []
print("Generating EightPuzzles...\n")

for i in range(numberOfPuzzles):
    print("Puzzle {}:".format(i+1))
    puzzles.append(make_rand_8puzzle())
    display(puzzles[i].initial)
    print("")

print("Solving EightPuzzles using A* search with the three heuristics...\n")
runAlgorithms(puzzles, numberOfPuzzles, "Eight", displayStatistics)

# For Question 3
# Comment out this block if not running algorithms on DuckPuzzles
puzzles = [] # Clearing list in case of having to run the two different kinds of puzzles back to back, referenced: https://www.geeksforgeeks.org/different-ways-to-clear-a-list-in-python/
print("Generating DuckPuzzles...\n")

for i in range(numberOfPuzzles):
    print("Puzzle {}:".format(i+1))
    puzzles.append(make_rand_duckPuzzle())
    displayDuck(puzzles[i].initial)
    print("")

print("Solving DuckPuzzles using A* search with the three heuristics...\n")
runAlgorithms(puzzles, numberOfPuzzles, "Duck", displayStatistics)