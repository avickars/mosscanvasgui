# a1.py

from search import *
import time
import random
random.seed()

def fixed_misplaced(node):
    displaced = 0
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    for i in range(9):
        if node.state[i] != goal[i]:
            displaced += 1
    # Removing zero from the heuristic
    if node.state.index(0) != 8:
        displaced -= 1
    return displaced


def manhattan(node):
    # Realized you don't include the empty tile from https://en.wikipedia.org/wiki/Admissible_heuristic
    mDistance = 0
    for i in range(9):
        if node.state[i] != 0:
            # difference mod 3 to get the vertical distance
            mDistance += abs(((node.state[i] - 1) % 3) - (i % 3))
            # difference in floor division to get the horizontal distance
            mDistance += abs(((node.state[i] - 1) // 3) - (i//3))
    return mDistance


def hybrid(node):
    # it was easier to implement the misplaced tile algorithm than figure out how to call it from here
    displaced = 0
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    for i in range(9):
        if node.state[i] != goal[i]:
            displaced += 1
    # Removing zero from the heuristic
    if node.state.index(0) != 8:
        displaced -= 1
    return max(displaced, manhattan(node))


def duck_manhattan(node):
    mDistance = 0
    goal = {1: (0, 0), 2: (0, 1), 3: (1, 0), 4: (1, 1), 5: (1, 2), 6: (1, 3), 7: (2, 0), 8: (2, 1), 0: (2, 2)}
    index = 0
    board = (2, 4, 3)
    for i in range(len(board)):
        for j in range(board[i]):
            if node.state[index] != 0:
                mDistance += abs(goal[node.state[index]][0] - i) + abs(goal[node.state[index]][1] - j)
                index += 1
    return mDistance


def duck_hybrid(node):
    displaced = 0
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    for i in range(9):
        if node.state[i] != goal[i]:
            displaced += 1
    # Removing zero from the heuristic
    if node.state.index(0) != 8:
        displaced -= 1
    return max(displaced, duck_manhattan(node))


# I assume by nodes removed the requirements mean nodes deleted, not nodes popped
def best_first_graph_search_modified(problem, f, display=False):
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
    nodes_removed = 0
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, nodes_removed
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    # as in the ones deleted here
                    del frontier[child]
                    nodes_removed += 1
                    frontier.append(child)
    return None


# modified to use the search algorithm that returns nodes removed
def astar_search_modified(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_modified(problem, lambda n: n.path_cost + h(n), display)


def make_basic_8puzzle():
    oneStepOff = (1, 2, 3, 4, 5, 6, 7, 0, 8)
    result = EightPuzzle(oneStepOff)
    return result


def make_rand_8puzzle():
    # Start with a known unsolvable state to initialize the while loop. The unsolvable state below was found at
    # https://www.cs.princeton.edu/courses/archive/fall12/cos226/assignments/8puzzle.html
    stateTuple = (1, 2, 3, 4, 5, 6, 8, 7, 0)
    result = EightPuzzle(stateTuple)
    while result.check_solvability(stateTuple) != 1:
        # removing a random index from one list and appending to the other ensures no duplicates
        numberList = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        stateList = []
        while len(numberList) > 0:
            index = random.randint(0, len(numberList) - 1)
            stateList.append(numberList[index])
            numberList.pop(index)
        stateTuple = tuple(stateList)
    result.initial = stateTuple
    return result


def display(state):
    board = ""
    for x in range(9):
        if state[x] == 0:
            board += "* "
        else:
            board += format(state[x]) + " "
        if x % 3 == 2:
            board += "\n"
    print(board)


class DuckPuzzle(Problem):
    # Reused and modified some of the code from the 8 puzzle class
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
        
        # indices at which the specified moves are invalid
        no_UP = (0, 1, 4, 5)
        no_DOWN = (2, 6, 7, 8)
        no_LEFT = (0, 2, 6)
        no_RIGHT = (1, 5, 8)

        for i in no_UP:
            if index_blank_square == i:
                possible_actions.remove('UP')
        for i in no_DOWN:
            if index_blank_square == i:
                possible_actions.remove('DOWN')
        for i in no_LEFT:
            if index_blank_square == i:
                possible_actions.remove('LEFT')
        for i in no_RIGHT:
            if index_blank_square == i:
                possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        # Special cases for top left of the board
        if blank < 2:
            delta['DOWN'] = 2
        if blank < 4:
            delta['UP'] = -2
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """
        displaced = 0
        goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        for i in range(9):
            if node.state[i] != goal[i]:
                displaced += 1
        # Removing zero from the heuristic
        if node.state.index(0) != 8:
            displaced -= 1
        return displaced


def make_rand_duck_puzzle():
    # start from the goal state and just make random valid moves
    # idea from some guy in the Comp Sci student society discord
    new = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))
    for i in range(1000):
        moves = new.actions(new.initial)
        randChoice = random.randint(0, len(moves) - 1)
        new.initial = new.result(new.initial, moves[randChoice])
    return new


print("Creating 8 puzzles")
puzzleList = []
for i in range(10):
    puzzleList.append(make_rand_8puzzle())

misplacedNodeList = []
misplacedTimes = []

manhattanNodeList = []
manhattanTimes = []

hybridNodeList = []
hybridTimes = []

stringToPrint = ""

print("Data is printed in the format time, path length, nodes removed\n")
print("Computing misplaced tile data")
for i in range(10):
    startTime = time.time()
    misplacedNodeList.append(astar_search_modified(puzzleList[i], fixed_misplaced))
    endTime = time.time()
    misplacedTimes.append(endTime - startTime)

print("Printing misplaced tile data")
for i in range(10):
    stringToPrint = str(misplacedTimes[i]) + ", "
    stringToPrint += str(misplacedNodeList[i][0].path_cost) + ", "
    stringToPrint += str(misplacedNodeList[i][1])
    print(stringToPrint)

print("\nComputing Manhattan distance data")
for i in range(10):
    startTime = time.time()
    manhattanNodeList.append(astar_search_modified(puzzleList[i], manhattan))
    endTime = time.time()
    manhattanTimes.append(endTime - startTime)

print("Printing Manhattan distance data")
for i in range(10):
    stringToPrint = str(manhattanTimes[i]) + ", "
    stringToPrint += str(manhattanNodeList[i][0].path_cost) + ", "
    stringToPrint += str(manhattanNodeList[i][1])
    print(stringToPrint)

print("\nComputing hybrid data")
for i in range(10):
    startTime = time.time()
    hybridNodeList.append(astar_search_modified(puzzleList[i], hybrid))
    endTime = time.time()
    hybridTimes.append(endTime - startTime)

print("Printing hybrid data")
for i in range(10):
    stringToPrint = str(hybridTimes[i]) + ", "
    stringToPrint += str(hybridNodeList[i][0].path_cost) + ", "
    stringToPrint += str(hybridNodeList[i][1])
    print(stringToPrint)

print("\nCreating Duck puzzles")
duckPuzzleList = []
for i in range(10):
    duckPuzzleList.append(make_rand_duck_puzzle())

duckMisplacedNodeList = []
duckMisplacedTimes = []

duckManhattanNodeList = []
duckManhattanTimes = []

duckHybridNodeList = []
duckHybridTimes = []

print("\nComputing duck misplaced tile data")
for i in range(10):
    startTime = time.time()
    duckMisplacedNodeList.append(astar_search_modified(duckPuzzleList[i]))
    endTime = time.time()
    duckMisplacedTimes.append(endTime - startTime)

print("Printing duck misplaced tile data")
for i in range(10):
    stringToPrint = str(duckMisplacedTimes[i]) + ", "
    stringToPrint += str(duckMisplacedNodeList[i][0].path_cost) + ", "
    stringToPrint += str(duckMisplacedNodeList[i][1])
    print(stringToPrint)

print("\nComputing duck Manhattan distance data")
for i in range(10):
    startTime = time.time()
    duckManhattanNodeList.append(astar_search_modified(duckPuzzleList[i], duck_manhattan))
    endTime = time.time()
    duckManhattanTimes.append(endTime - startTime)

print("Printing duck Manhattan distance data")
for i in range(10):
    stringToPrint = str(duckManhattanTimes[i]) + ", "
    stringToPrint += str(duckManhattanNodeList[i][0].path_cost) + ", "
    stringToPrint += str(duckManhattanNodeList[i][1])
    print(stringToPrint)

print("\nComputing duck hybrid data")
for i in range(10):
    startTime = time.time()
    duckHybridNodeList.append(astar_search_modified(duckPuzzleList[i], duck_hybrid))
    endTime = time.time()
    duckHybridTimes.append(endTime - startTime)

print("Printing duck hybrid data")
for i in range(10):
    stringToPrint = str(duckHybridTimes[i]) + ", "
    stringToPrint += str(duckHybridNodeList[i][0].path_cost) + ", "
    stringToPrint += str(duckHybridNodeList[i][1])
    print(stringToPrint)

print("done")
