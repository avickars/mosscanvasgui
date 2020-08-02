# a1.py

import random
import time

from search import *

# Modified functions from search.py
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def best_first_graph_search(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                #len(explored)+1 represents the number of popped nodes since the last popped node is not added to explored
                print("Number of nodes removed from frontier:", len(explored)+1, "\nNumber of tiles moved (path cost):", node.path_cost)
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

#  Q1 : Helper Functions

# Create a random state, repeat until it is a solvable state
def make_rand_8puzzle():
    initState = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    rand_8puzzle = EightPuzzle(tuple(initState))

    while (True):
        randomState = random.sample(initState, len(initState))
        rand_8puzzle = EightPuzzle(tuple(randomState))

        if (rand_8puzzle.check_solvability(rand_8puzzle.initial)):
            break

    return rand_8puzzle

def display(state):
    state = ["*" if i == 0 else i for i in state]

    for i, num in enumerate(state):
        print(num, end =" ")
        if (i % 3 == 2):
            print()

# Q2 : Comparing Algorithms

# Returns the y coordinate of the tile in a 3-row puzzle
def yCoord(y):
    return int(y / 3)

# Returns the x coordinate of the tile in a 3-column puzzle
def xCoord(x):
    return x % 3

# Used by h2_ManhattanDistance_DuckPuzzle to represent the puzzle in a '4x3' grid indices, x being in 4-columns.
def xCoord_duckpuzzle(x):
    return x % 4

# Misplaced Tile Algorithm:
# This heuristic algorithm does not consider the blank tile.
def h1_MisplacedTile(node):
    sum = 0
    for i, num in enumerate(node.state):
        if (i != num-1 and num != 0):
            sum+=1
    return sum

# Manhattan Distance Algorithm:
# Compute distance from tile A to home tile B with |Ax - Bx| + |Ay - By|
# h(n) is the sum of each tile's distance from home
# Calculate Ax by index % 3, Ay by index / 3, where A is the index in array. B is the num-1 since array index starts at 0
def h2_ManhattanDistance(node):
    sum = 0
    for i, num in enumerate(node.state):
        if (i != num-1 and num != 0):
            sum += abs(xCoord(i) - xCoord((num-1)))
            sum += abs(yCoord(i) - yCoord((num-1)))
    return sum

# Max of Misplaced Tile & Manhattan Distance Algorithm:
def h3_Max(node):
    return max(h1_MisplacedTile(node), h2_ManhattanDistance(node))

def solveProblem(problem, h):
    start_time = time.time()
    print(astar_search(problem, h, True))
    elapsed_time = time.time() - start_time
    print("elapsed time(s) :", elapsed_time, "s\n")

def simulateEightPuzzle(n):
    for x in range(n):
        randPuzzle = make_rand_8puzzle()
        print("Test ", x+1, ": ")
        display(randPuzzle.initial)

        print("\nEightPuzzle[Misplaced Tile Heuristic]")
        solveProblem(randPuzzle, h1_MisplacedTile)

        print("\nEightPuzzle[Manhattan Distance Heuristic]")
        solveProblem(randPuzzle, h2_ManhattanDistance)

        print("\nEightPuzzle[Max(misplaced_tile, manhattan_distance) Heuristic]")
        solveProblem(randPuzzle, h3_Max)

#Q3 : Duck Puzzle Implementation
class DuckPuzzle(Problem):

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

        # (DUCKPUZZLE) - account for the different possible actions in the new puzzle layout
        if index_blank_square in [0, 2, 6]:
            possible_actions.remove('LEFT')
        if index_blank_square in [0, 1, 4, 5]:
            possible_actions.remove('UP')
        if index_blank_square in [1, 5, 8]:
            possible_actions.remove('RIGHT')
        if index_blank_square in [2, 6, 7, 8]:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # (DUCKPUZZLE) certain tiles have different delta values to move the blank square
        if blank in [0, 1, 2]:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

# DUCKPUZZLE HELPER FUNCTIONS

# (DUCKPUZZLE) - Sramble puzzle by starting with the goal state, and perform legal actions on the blank tile randomly up to N times.
# This guarantees that the puzzle is solvable after the scramble
def make_rand_duckpuzzle():
    randomState = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    rand_duckPuzzle = DuckPuzzle(tuple(randomState))
    n = 1000

    for x in range(n):
        actions = rand_duckPuzzle.actions(rand_duckPuzzle.initial)
        move = random.choice(actions)
        rand_duckPuzzle = DuckPuzzle(rand_duckPuzzle.result(rand_duckPuzzle.initial, move))

    return rand_duckPuzzle

def display_duckpuzzle(state):
    state = ["*" if i == 0 else i for i in state]

    for i, num in enumerate(state):
        print(num, end =" ")
        if (i == 1 or i == 8):
            print()
        if (i == 5):
            print("\n", end="  ")

# To calculate manhattan distance for duck puzzle. We can note that the duck puzzle can be represented in a 4x3 grid.
# Convert the indexes to as if it was in a 4x3 grid and then calculate the distance using yCoord() and xCoord_duckpuzzle()
def gridIndex(i):
    if (i > 1 and i < 6):
        return i + 2
    elif (i > 5):
        return i + 3
    else:
        return i

# Similar to how the manhattan was calculated in EightPuzzle, where we get the difference of its x, y coordinates.
# However, to keep it 1D space complexity, we can represent the puzzle in a 4x3 grid and adjust indices accordingly by calling gridIndex().
def h2_ManhattanDistance_DuckPuzzle(node):
    sum = 0
    for i, num in enumerate(node.state):
        if (gridIndex(i) != gridIndex(num-1) and num != 0):
            sum += abs(xCoord_duckpuzzle(gridIndex(i)) - xCoord_duckpuzzle(gridIndex(num-1))) + abs(yCoord(gridIndex(i)) - yCoord(gridIndex(num-1)))
    return sum

def h3_Max_DuckPuzzle(node):
    return max(h1_MisplacedTile(node), h2_ManhattanDistance_DuckPuzzle(node))

def simulateDuckPuzzle(n):
    for x in range(n):
        randPuzzle = make_rand_duckpuzzle()
        print("Test ", x+1, ": ")
        display_duckpuzzle(randPuzzle.initial)

        print("\nDuck Puzzle[Misplaced Tile Heuristic]")
        solveProblem(randPuzzle, h1_MisplacedTile)

        print("\nDuck Puzzle[Manhattan Distance Heuristic]")
        solveProblem(randPuzzle, h2_ManhattanDistance_DuckPuzzle)

        print("\nDuck Puzzle[Max(misplaced_tile, manhattan_distance) Heuristic]")
        solveProblem(randPuzzle, h3_Max_DuckPuzzle)

if __name__ == "__main__":
      numTestCases = 10
      simulateEightPuzzle(numTestCases)
      simulateDuckPuzzle(numTestCases)
