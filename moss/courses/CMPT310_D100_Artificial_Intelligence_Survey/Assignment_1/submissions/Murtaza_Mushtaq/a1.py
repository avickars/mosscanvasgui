# a1.py

from search import *
import sys
import time
import random
# ...

# Before running this piece of code, set the number of puzzles to analyse in eight and duck shapes
numOfTestPuzzles = 1 # This decides the number of random puzzles to analyse in both Eight and Duck shapes

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
    numOfRemovedNodes = 0
    explored = set()
    while frontier:
        node = frontier.pop()
        numOfRemovedNodes = numOfRemovedNodes + 1
        if problem.goal_test(node.state):
            if display:
                #print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                print("Number of nodes removed " + str(numOfRemovedNodes))
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
    
    # Answer to part of Question 2
    def man_algo(self, node):
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
    
    def maxh_algo(self, node):
        return max(self.h(node), self.man_algo(node))
    # ...

# Answer to Question 1
def make_rand_8puzzle():
    puzzleSolvable = 0
    newPuzzleInstance = None
    while(puzzleSolvable == 0):
        newPuzzleTupleInstance = tuple(random.sample(range(0, 9), 9))
        newPuzzleInstance = EightPuzzle(newPuzzleTupleInstance, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))
        puzzleSolvable = newPuzzleInstance.check_solvability(newPuzzleInstance.initial)
    return newPuzzleInstance

def display(state):
    puzzleInListForm = list(state)
    for i in range(9):
        if(puzzleInListForm[i] == 0):
            puzzleInListForm[i] = "*"
    print(puzzleInListForm[0], puzzleInListForm[1], puzzleInListForm[2])
    print(puzzleInListForm[3], puzzleInListForm[4], puzzleInListForm[5])
    print(puzzleInListForm[6], puzzleInListForm[7], puzzleInListForm[8])
# ...

# Answer to Question 2
print("---------------")
print("Solving Eight Puzzle")
testPuzzlesList = []
for i in range(numOfTestPuzzles):
    newTestPuzzleIndividual = make_rand_8puzzle()
    testPuzzlesList.append(newTestPuzzleIndividual)
for i in range(numOfTestPuzzles):
    print("Initial look of puzzle #" + str(i+1))
    display(testPuzzlesList[i].initial)
    print("Using default algo")
    timerStartTime = time.time()
    target = astar_search(testPuzzlesList[i], testPuzzlesList[i].h, True)
    timeTaken = time.time() - timerStartTime
    print("Time taken is: " + str(timeTaken) + "s and number of tiles moved are: " + str(target.path_cost))
    print("Using man algo")
    timerStartTime = time.time()
    target = astar_search(testPuzzlesList[i], testPuzzlesList[i].man_algo, True)
    timeTaken = time.time() - timerStartTime
    print("Time taken is: " + str(timeTaken) + "s and number of tiles moved are: " + str(target.path_cost))
    print("Using maxh algo")
    timerStartTime = time.time()
    target = astar_search(testPuzzlesList[i], testPuzzlesList[i].maxh_algo, True)
    timeTaken = time.time() - timerStartTime
    print("Time taken is: " + str(timeTaken) + "s and number of tiles moved are: " + str(target.path_cost))
    print("Final look of puzzle #" + str(i+1))
    display(target.state)
    print("--------")
print(str(numOfTestPuzzles) + " EIGHT PUZZLE(S) SOLVED")
# ...

# Answer to Question 3
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board shaped like a left facing duck,
    where one of the squares is a blank. A state is represented as a tuple of length 9, where  element at
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
        if((index_blank_square == 0) or (index_blank_square == 4) or (index_blank_square == 9)):
            possible_actions.remove('LEFT')
        if((index_blank_square == 0) or (index_blank_square == 1) or (index_blank_square == 6) or (index_blank_square == 7)):
            possible_actions.remove('UP')
        if((index_blank_square == 1) or (index_blank_square == 7) or (index_blank_square == 11)):
            possible_actions.remove('RIGHT')
        if((index_blank_square == 4) or (index_blank_square == 9) or (index_blank_square == 10) or (index_blank_square == 11)):
            possible_actions.remove('DOWN')
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1} # delta for UP and DOWN have changed to accomodate a 4x3 grid
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
    
    def man_algo(self, node):
        state = node.state
        index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]} # coordinates have changed
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3]] # now accomodates a 4x3 grid
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        mhd = 0
        for i in range(9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        return mhd
    
    def maxh_algo(self, node):
        return max(self.h(node), self.man_algo(node))

def make_rand_Duckpuzzle():
    newPuzzleTupleInstance = tuple(random.sample(range(0, 9), 9))
    someNewPuzzleTupleInstance = (newPuzzleTupleInstance[0], newPuzzleTupleInstance[1], " ", " ", newPuzzleTupleInstance[2], newPuzzleTupleInstance[3], newPuzzleTupleInstance[4], newPuzzleTupleInstance[5], " ", newPuzzleTupleInstance[6], newPuzzleTupleInstance[7], newPuzzleTupleInstance[8])
    newPuzzleTupleInstance = someNewPuzzleTupleInstance
    newPuzzleInstance = DuckPuzzle(newPuzzleTupleInstance, goal=(1, 2, " ", " ", 3, 4, 5, 6, " ", 7, 8, 0))
    return newPuzzleInstance

def displayDuck(state):
    puzzleInListForm = list(state)
    for i in range(12):
        if(puzzleInListForm[i] == 0):
            puzzleInListForm[i] = "*"
    print(puzzleInListForm[0], puzzleInListForm[1], puzzleInListForm[2], puzzleInListForm[3])
    print(puzzleInListForm[4], puzzleInListForm[5], puzzleInListForm[6], puzzleInListForm[7])
    print(puzzleInListForm[8], puzzleInListForm[9], puzzleInListForm[10], puzzleInListForm[11])

print("---------------")
print("Solving Duck Puzzle")
for i in range(numOfTestPuzzles):
    target = None
    duckTotalTimeTaken = 0
    testPuzzle = None
    while(target == None):
        testPuzzle = make_rand_Duckpuzzle()
        duckTimeStart = time.time()       
        target = astar_search(testPuzzle, testPuzzle.h, True)
        duckTotalTimeTaken = time.time() - duckTimeStart
    print("Initial look of puzzle #" + str(i+1))
    displayDuck(testPuzzle.initial)
    print("Using default algo")
    print("Time taken is: " + str(duckTotalTimeTaken) + "s and number of tiles moved are: " + str(target.path_cost))
    print("Using man algo")
    duckTimeStart = time.time()
    target = astar_search(testPuzzle, testPuzzle.man_algo, True)
    duckTotalTimeTaken = time.time() - duckTimeStart
    print("Time taken is: " + str(duckTotalTimeTaken) + "s and number of tiles moved are: " + str(target.path_cost))
    print("Using maxh algo")
    duckTimeStart = time.time()
    target = astar_search(testPuzzle, testPuzzle.maxh_algo, True)
    duckTotalTimeTaken = time.time() - duckTimeStart
    print("Time taken is: " + str(duckTotalTimeTaken) + "s and number of tiles moved are: " + str(target.path_cost))
    print("Final look of puzzle #" + str(i+1))
    displayDuck(target.state)
    print("--------")
print(str(numOfTestPuzzles) + " DUCK PUZZLE(S) SOLVED")
# ...