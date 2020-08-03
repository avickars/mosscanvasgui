from search import *
from random import randint
import time

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


    def manhattan(self, node):
        state = node.state
        index_goal = {1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index_state = {}
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        
        index_state.pop(0)
        mhd = 0
        
        for i in range(1, 8):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        
        return mhd

    def max_heuristic(self, node):
        return max(self.manhattan(node), self.h(node))


# ______________________________________________________________________________

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

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        # If the tile is in the first row. Moving it down won't change the index by 3, but by 2
        if blank == 0 or blank == 1 or blank == 2 or blank == 3:
            delta['UP'] = -2
            delta['DOWN'] = 2

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


    def manhattan(self, node):
        state = node.state
        index_goal = {1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
        index_state = {}
        index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
        
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        
        # Pop the zero (*) tile after mapping all tiles as we'll know which tile holds the zero tile after assignment
        index_state.pop(0)

        mhd = 0
    
        for i in range(1, 8):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        
        return mhd

    def max_heuristic(self, node):
        return max(self.manhattan(node), self.h(node))

# ______________________________________________________________________________

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
    expanded = [] # add a list to hold nodes explored
    while frontier:
        node = frontier.pop()
        expanded.append(node)
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, expanded]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def display(state):
    for i in state:
        if state.index(i) == 3 or state.index(i) == 6:
            print("\n")
        if i == 0:
            print("* ", end="")
        else: print(f"{i} ", end="")


def display_duck_puzzle(state):
    for i in state:
        if state.index(i) == 2:
            print("\n")
        if state.index(i) == 6:
            print("\n")
            print("  ", end="")
        if i == 0:
            print("* ", end="")
        else: print(f"{i} ", end="")

def make_rand_8puzzle():
    initial_state = [i for i in range(1,9)]
    initial_state.append(0)
    eight_puzzle = EightPuzzle(tuple(initial_state))

    for i in range(0,100):
        actions = eight_puzzle.actions(eight_puzzle.initial)
        result = actions[randint(0, len(actions)-1)]
        eight_puzzle.initial = eight_puzzle.result(eight_puzzle.initial, result)

    return eight_puzzle


def make_rand_duckpuzzle():
    state = [i for i in range(1,9)]
    state.append(0)

    helper = DuckPuzzle(tuple(state))

    for i in range(0,100):
        actions = helper.actions(helper.initial)
        result = actions[randint(0, len(actions)-1)]
        helper.initial = helper.result(helper.initial, result)

    return helper


def runTest(puzzle, heuristic=1):
    start_time = time.time()
    if heuristic == 1:
        print("Misplaced Tile Heuristic")
        result, node_count = astar_search(puzzle)
    elif heuristic == 2:
        print("Manhattan Heuristic")
        result, node_count = astar_search(puzzle, puzzle.manhattan)
    elif heuristic == 3:
        print("Max of the Misplaced Tile Heuristic and the Manhattan Distance Heuristic")
        result, node_count = astar_search(puzzle, puzzle.max_heuristic)
    
    print(f"Elapsed Time (s): {time.time() - start_time}")
    print(f"Num of Steps: {len(result.solution())}")
    print(f"Nodes Removed from Frontier: {len(node_count)}\n\n")

def runDuckTest(puzzle, heuristic=1):
    start_time = time.time()
    if heuristic == 1:
        print("Misplaced Tile Heuristic")
        result, node_count = astar_search(puzzle)
    elif heuristic == 2:
        print("Manhattan Heuristic")
        result, node_count = astar_search(puzzle, puzzle.manhattan)
    elif heuristic == 3:
        print("Max of the Misplaced Tile Heuristic and the Manhattan Distance Heuristic")
        result, node_count = astar_search(puzzle, puzzle.max_heuristic)
    
    print(f"Elapsed Time (s): {time.time() - start_time}")
    print(f"Num of Steps: {len(result.solution())}")
    print(f"Nodes Removed from Frontier: {len(node_count)}\n\n")


def run_8_puzzle_test():
    for i in range(10):
        print(f"Test {i + 1} ---------------------------")
        puzzle = make_rand_8puzzle()
        runTest(puzzle)
        runTest(puzzle, 2)
        runTest(puzzle, 3)

def run_duck_puzzle_tests():
    for i in range(10):
        print(f"Test {i + 1} ---------------------------")
        puzzle = make_rand_duckpuzzle()
        print("\n")
        runTest(puzzle)
        runTest(puzzle, 2)
        runTest(puzzle, 3)

# print("-------------------------------")
# print("-------------------------------")
# print("8-Puzzle Tests")
# print("-------------------------------")
# print("-------------------------------")
# run_8_puzzle_test()
# print("-------------------------------")
# print("-------------------------------")
# print("Duck Puzzle Tests")
# print("-------------------------------")
# print("-------------------------------")
# run_duck_puzzle_tests()

