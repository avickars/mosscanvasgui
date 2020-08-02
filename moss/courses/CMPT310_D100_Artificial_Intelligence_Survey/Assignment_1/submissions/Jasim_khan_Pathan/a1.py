from search import *
import sys
import random
import time

#From search.py:

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

    # Question 2 (In-class Functions):

    def manhattanDistHeuristic(self, node):

        state = node.state
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        mhd = 0
        for i in range(9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        return mhd

    def maximumValue(self, node):

        return max((self.manhattanDistHeuristic(node)), (self.h(node)))

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
    count = 0
    while frontier:
        node = frontier.pop()
        count += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, count]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


#Question 1:

def make_rand_8puzzle():

    randomlist = random.sample(range(0, 9), 9)
    pTuple = tuple(randomlist)

    puzzle = EightPuzzle(pTuple, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))

    while puzzle.check_solvability(puzzle.initial) is False :
        randomlist = random.sample(range(0, 9), 9)
        pTuple = tuple(randomlist)
        puzzle.initial = pTuple

    return puzzle

def display(state):
    output = list(state)
    for a in range(9):
        if output[a] == 0:
            output[a] = "*"
    print('\n',output[0], output[1], output[2], '\n', output[3], output[4], output[5], '\n', output[6], output[7], output[8])

#Question 2 (Generating and checking 10 puzzles):

for i in range(10):

    print (" Puzzle No: ", i+1, '\n')
    puzzle = make_rand_8puzzle()
    print (" Original Puzzle")
    display(puzzle.initial)

    print ('\n',"Misplaced Tile Heuristic Stats",'\n')
    start_time = time.time()
    func = astar_search(puzzle, puzzle.h)
    run_time = time.time() - start_time
    print(" Run time (s) = ", run_time)
    print(" Length = ", func[0].path_cost)
    print(" Number of nodes removed = ",func[1])

    print('\n',"Manhattan Distance Heuristic Stats", '\n')
    start_time = time.time()
    func = astar_search(puzzle, puzzle.manhattanDistHeuristic)
    run_time = time.time() - start_time
    print(" Run time (s) = ",run_time)
    print(" Length = ",func[0].path_cost)
    print(" Number of nodes removed = ",func[1])

    print('\n',"Maximum Value between Manhattan Distance Heuristic and Misplaced Tile Heuristic ", '\n')
    start_time = time.time()
    func = astar_search(puzzle, puzzle.maximumValue)
    run_time = time.time() - start_time
    print(" Run time (s) = ",run_time)
    print(" Length = ",func[0].path_cost)
    print(" Number of nodes removed = ",func[1])

#Question 3:

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

        impossibleLeft = [0, 2, 6];
        if index_blank_square in impossibleLeft:
            possible_actions.remove('LEFT')
        impossibleUP = [0, 1, 4, 5];
        if index_blank_square in impossibleUP:
            possible_actions.remove('UP')
        impossibleRight = [1, 5, 8];
        if index_blank_square in impossibleRight:
            possible_actions.remove('RIGHT')
        impossibleDown = [2,6,7,8];
        if index_blank_square in impossibleDown:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        case1Val = (0,1,2)
        case2Val = (3,)
        case1 = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        case2 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        case3 = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        if blank in case1Val:
            neighbor = blank + case1[action]
        elif blank in case2Val:
            neighbor = blank + case2[action]
        else:
            neighbor = blank + case3[action]

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

    def manhattanDistHeuristic(self, node):
        state = node.state
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        mhd = 0
        for i in range(9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        return mhd


    def maximumValue(self, node):
        return max((self.manhattanDistHeuristic(node)), (self.h(node)))

def make_rand_Duckpuzzle():

    randomlist = random.sample(range(0, 9), 9)
    pTuple = tuple(randomlist)

    puzzle = DuckPuzzle(pTuple, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))

    while puzzle.check_solvability(puzzle.initial) is False :
        randomlist = random.sample(range(0, 9), 9)
        pTuple = tuple(randomlist)
        puzzle.initial = pTuple

    return puzzle

def Duckdisplay(state):
    output = list(state)
    for a in range(9):
        if output[a] == 0:
            output[a] = "*"
    print('\n',output[0], output[1], '\n', output[2], output[3], output[4], output[5], '\n'," ", output[6], output[7], output[8])

for i in range(10):

    print (" Puzzle No: ", i+1, '\n')
    puzzle = make_rand_Duckpuzzle()
    print (" Original Puzzle")
    Duckdisplay(puzzle.initial)

    print ('\n',"Misplaced Tile Heuristic Stats",'\n')
    start_time = time.time()
    func = astar_search(puzzle, puzzle.h)
    run_time = time.time() - start_time
    while func is None :
        puzzle = make_rand_Duckpuzzle()
        start_time = time.time()
        func = astar_search(puzzle, puzzle.h)
        run_time = time.time() - start_time
    print(" Run time (s) = ", run_time)
    print(" Length = ", func[0].path_cost)
    print(" Number of nodes removed = ",func[1])

    print('\n',"Manhattan Distance Heuristic Stats", '\n')
    start_time = time.time()
    func = astar_search(puzzle, puzzle.manhattanDistHeuristic)
    run_time = time.time() - start_time
    print(" Run time (s) = ",run_time)
    print(" Length = ",func[0].path_cost)
    print(" Number of nodes removed = ",func[1])

    print('\n',"Maximum Value between Manhattan Distance Heuristic and Misplaced Tile Heuristic ", '\n')
    start_time = time.time()
    func = astar_search(puzzle, puzzle.maximumValue)
    run_time = time.time() - start_time
    print(" Run time (s) = ",run_time)
    print(" Length = ",func[0].path_cost)
    print(" Number of nodes removed = ",func[1])