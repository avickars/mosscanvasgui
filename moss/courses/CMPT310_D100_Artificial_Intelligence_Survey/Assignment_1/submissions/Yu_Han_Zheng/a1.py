# a1.py

from search import *
import time
import numpy as np

# ...
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
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print(f"Total number of nodes removed from frontier: {len(explored)+1}")
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

def make_rand_8puzzle():
    puzzle = EightPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))
    moveNum = random.randint(0, 100)
    initial = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    for i in range(moveNum):
        actionList = puzzle.actions(initial)
        action = random.choice(actionList)
        initial = puzzle.result(initial, action)
    # Since only legal moves were used to obtain the scrambled state, there is no need to call check_solvability().
    return EightPuzzle(initial)

def display(state):
    state = list(state)
    state[state.index(0)] = '*'
    for i in range(0, len(state), 3): #https://stackoverflow.com/questions/9475241/split-string-every-nth-character
        print(*state[i:i+3], sep=" ") #https://kite.com/python/answers/how-to-print-a-list-without-brackets-in-python

def manhattan(node):
    precomputedTable = {0: (0, 1, 2, 1, 2, 3, 2, 3, 4),  # The pre-computed tables were taken from the course notes.
                        1: (1, 0, 1, 2, 1, 2, 3, 2, 3),
                        2: (2, 1, 0, 3, 2, 1, 4, 3, 2),
                        3: (1, 2, 3, 0, 1, 2, 1, 2, 3),
                        4: (2, 1, 2, 1, 0, 1, 2, 1, 2),
                        5: (3, 2, 1, 2, 1, 0, 3, 2, 1),
                        6: (2, 3, 4, 1, 2, 3, 0, 1, 2),
                        7: (3, 2, 3, 2, 1, 2, 1, 0, 1),
                        8: (4, 3, 2, 3, 2, 1, 2, 1, 0)}
    score = 0
    for tile in range(1, 9): # Do not count blank square.
        tilePos = node.state.index(tile)  # Find the index of the tile.
        table = precomputedTable[tilePos] # Select the table indexed by tile position.
        solvedPos = (1, 2, 3, 4, 5, 6, 7, 8, 0).index(tile)  # Find the index of where the tile should be.
        score += table[solvedPos]
    #print(node.state)
    #print(f"man score {score}")
    return score

def max_h_manhattan(node):
    return max(puzzle.h(node), manhattan(node))

def solve_puzzle(puzzle, h = None):
    start_time = time.time()
    res = astar_search(puzzle, h=h, display=False) # Returns a node object.
    elapsed_time = time.time() - start_time
    print(f"Running time: {elapsed_time}")
    print(f"Number of tiles moved (length) of the solution: {res.path_cost}") # Can also be obtained with len(res.solution())
'''
# Make and solve one puzzle.
#puzzle = make_rand_8puzzle()
#puzzle = EightPuzzle((6,5,2,3,7,1,8,4,0), (1, 2, 3, 4, 5, 6, 7, 8, 0))
display(puzzle.initial)
h = puzzle.h
print("\nMisplaced Tiles")
solve_puzzle(puzzle, puzzle.h)
print("\nManhattan")
solve_puzzle(puzzle, manhattan)
print("\nMax")
solve_puzzle(puzzle, max_h_manhattan)
'''

for i in range(0,10): # Make and solve ten puzzles.
    puzzle = make_rand_8puzzle()
    display(puzzle.initial)
    print("\nMisplaced Tiles")
    solve_puzzle(puzzle, puzzle.h)
    print("\nManhattan")
    solve_puzzle(puzzle, manhattan)
    print("\nMax")
    solve_puzzle(puzzle, max_h_manhattan)


######### Duck Puzzle ##########
class DuckPuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, '_', '_', 3, 4, 5, 6, '_', 7, 8, 0)):
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

        if index_blank_square % 4 == 0 or index_blank_square == 9:
            possible_actions.remove('LEFT')
        if index_blank_square < 4 or index_blank_square == 6 or index_blank_square == 7:
            possible_actions.remove('UP')
        if index_blank_square % 4 == 3 or index_blank_square == 1:
            possible_actions.remove('RIGHT')
        if index_blank_square > 7 or index_blank_square == 4:
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

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """
        return sum(s != g for (s, g) in zip(node.state, self.goal))

def make_rand_duckpuzzle():
    puzzle = DuckPuzzle((1, 2, '_', '_', 3, 4, 5, 6, '_', 7, 8, 0))
    moveNum = random.randint(0, 100)
    initial = (1, 2, '_', '_', 3, 4, 5, 6, '_', 7, 8, 0)
    for i in range(moveNum):
        actionList = puzzle.actions(initial)
        action = random.choice(actionList)
        initial = puzzle.result(initial, action)
    # Since only legal moves were used to obtain the scrambled state, there is no need to call check_solvability().
    return DuckPuzzle(initial)

def displayDuck(state):
    state = list(state)
    state[state.index(0)] = '*'
    state = np.array(state)
    idx = np.where(state == '_')[0]
    state[idx] = ' '
    for i in range(0, len(state), 4): #https://stackoverflow.com/questions/9475241/split-string-every-nth-character
        print(*state[i:i+4], sep=" ")

def manhattanD(node):
    precomputedTable = {0: (0, 1, '_', '_', 1, 2, 3, 4, '_', 3, 4, 5),  # The pre-computed tables were manually created.
                        1: (1, 0, '_', '_', 2, 1, 2, 3, '_', 2, 3, 4),
                        4: (1, 2, '_', '_', 0, 1, 2, 3, '_', 2, 3, 4),
                        5: (2, 1, '_', '_', 1, 0, 1, 2, '_', 1, 2, 3),
                        6: (3, 2, '_', '_', 2, 1, 0, 1, '_', 2, 1, 2),
                        7: (4, 3, '_', '_', 3, 2, 1, 0, '_', 3, 2, 1),
                        9: (3, 2, '_', '_', 2, 1, 2, 3, '_', 0, 1, 2),
                        10: (4, 3, '_', '_', 3, 2, 1, 2, '_', 1, 0, 1),
                        11: (5, 4, '_', '_', 4, 3, 2, 1, '_', 2, 1, 0)}
    score = 0
    for tile in range(1, 9): # Do not count blank square.
        tilePos = node.state.index(tile)  # Find the index of the tile.
        table = precomputedTable[tilePos] # Select the table indexed by tile position.
        solvedPos = (1, 2, '_', '_', 3, 4, 5, 6, '_', 7, 8, 0).index(tile)  # Find the index of where the tile should be.
        score += table[solvedPos]
    #print(node.state)
    #print(f"man score {score}")
    return score

def max_h_manhattanD(node):
    return max(duckPuzzle.h(node), manhattanD(node))

for i in range(0,10): # Make and solve ten puzzles.
    #duckPuzzle = DuckPuzzle((2, 3, '_', '_', 1, 7, 0, 8, '_', 6, 4, 5))
    duckPuzzle = make_rand_duckpuzzle()
    displayDuck(duckPuzzle.initial)
    print("\nMisplaced Tiles")
    solve_puzzle(duckPuzzle, duckPuzzle.h)
    print("\nManhattan")
    solve_puzzle(duckPuzzle, manhattanD)
    print("\nMax")
    solve_puzzle(duckPuzzle, max_h_manhattanD)