import numpy as np
from search import *
import time
# ADDED REMOVED NODE COUNT AND LENGTH OF SOLUTION
# TODO: NEED TO CHANGE search.py on best_first_graph_search function
def best_first_graph_search2(problem, f, display=False):
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
        count = count + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print("Length of the solution", len(node.solution()))
            print("Removed Node Count:", count)
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

# Question 1: Helper Function
def make_rand_8puzzle():
    state = tuple(np.random.permutation([1,2,3,4,5,6,7,8,0]))
    puzzle = EightPuzzle(initial=state)
    if puzzle.check_solvability(state):
        return puzzle
    else:
        return make_rand_8puzzle()

def display(state):
    print_state = tuple([x if x != 0 else "*" for x in state])
    print("%s %s %s" % print_state[0:3])
    print("%s %s %s" % print_state[3:6])
    print("%s %s %s" % print_state[6:9])





# Question 2: Eight Puzzle
puzzles = [make_rand_8puzzle() for i in range(10)]
for puzzle in puzzles:
    print(puzzle.initial)

# MANHATTAN DISTANCE HEURISTIC FUNCTION
# inspired from manhattan function in tests/test_search.py
def manhattan_distance(node):
    state = node.state
    goal = (1,2,3,4,5,6,7,8,0)
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    index_state = {}
    index_goal = {}

    for i in range(len(index)):
        index_state[state[i]] = index[i]
        index_goal[goal[i]] = index[i]

    distance = 0

    for i in range(9):
        goal_x, goal_y = index_goal[i]
        state_x, state_y = index_state[i]
        delta_x = goal_x - state_x
        delta_y = goal_y - state_y
        distance = abs(delta_x) + abs(delta_y) + distance

    return distance

# MAX OF MISPLACED TILE HEURISTIC AND MANHATTAN DISTANCE HEURISTIC FUNCTION
misplaced_tile_heuristic = EightPuzzle(initial=None).h
def max_heuristic(node):
    manhattan_score = manhattan_distance(node)
    misplaced_score = misplaced_tile_heuristic(node)
    return max(manhattan_score, misplaced_score)

# MISPLACED TILE HEURISTIC SEARCH
for puzzle in puzzles:
    start_time = time.time()
    astar_search(puzzle)
    end_time = time.time()
    print("Time taken:", end_time - start_time)

# MISPLACED TILE HEURISTIC SEARCH
for puzzle in puzzles:
    start_time = time.time()
    astar_search(puzzle, h=manhattan_distance)
    end_time = time.time()
    print("Time taken:", end_time - start_time)

# MAX OF MISPLACED TILE HEURISTIC AND MANHATTAN DISTANCE HEURISTIC SEARCH
for puzzle in puzzles:
    start_time = time.time()
    astar_search(puzzle, h=max_heuristic)
    end_time = time.time()
    print("Time taken:", end_time - start_time)





# QUESTION 3: Duck Puzzle
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a Duck Puzzle Board, where one of the
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

        if index_blank_square in [0, 2, 6]:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or index_blank_square > 3 and index_blank_square < 6:
            possible_actions.remove('UP')
        if index_blank_square in [1, 5, 8]:
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

        delta = {'LEFT': -1, 'RIGHT': 1}
        if blank > 5:
            delta = {**delta, "UP": -3}
        elif blank > 1:
            delta = {**delta, "UP": -2, "DOWN": 3}
        else:
            delta = {**delta, "DOWN": 2}
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

def make_rand_duck_puzzle():
    goal_state = (1,2,3,4,5,6,7,8,0)
    goal_puzzle = DuckPuzzle(initial=goal_state)
    for i in range(100000):
        pos_actions = goal_puzzle.actions(goal_state)
        action = random.choice(pos_actions)
        goal_state = goal_puzzle.result(goal_state, action)
    puzzle = DuckPuzzle(initial=goal_state)
    return puzzle

def display_duck_puzzle(state):
    print_state = tuple([x if x != 0 else "*" for x in state])
    print("%s %s" % print_state[0:2])
    print("%s %s %s %s" % print_state[2:6])
    print("  %s %s %s" % print_state[6:9])

duck_puzzles = [make_rand_duck_puzzle() for i in range(10)]

for puzzle in duck_puzzles:
    print(puzzle.initial)

# MISPLACED TILE HEURISTIC FUNCTION
for puzzle in duck_puzzles:
    start_time = time.time()
    astar_search(puzzle)
    end_time = time.time()
    print("Time taken:", end_time - start_time)

# MISPLACED TILE HEURISTIC FUNCTION
for puzzle in duck_puzzles:
    start_time = time.time()
    astar_search(puzzle, h=manhattan_distance)
    end_time = time.time()
    print("Time taken:", end_time - start_time)

# MAX OF MISPLACED TILE HEURISTIC AND MANHATTAN DISTANCE HEURISTIC FUNCTION
for puzzle in duck_puzzles:
    start_time = time.time()
    astar_search(puzzle, h=max_heuristic)
    end_time = time.time()
    print("Time taken:", end_time - start_time)