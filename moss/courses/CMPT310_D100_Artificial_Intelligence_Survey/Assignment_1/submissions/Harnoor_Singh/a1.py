# a1.py
from search import *
import time


# Code from search.py

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
    CountRemoved = 0
    while frontier:
        node = frontier.pop()
        CountRemoved = CountRemoved + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            ret = [node, CountRemoved]
            return ret
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

    # This is Some part of Question 2
    def manhattan(self, node):
        state = node.state
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhdHorizontal = 0
        mhdVertical = 0

        for i in range(9):
            mhdHorizontal = abs(index_goal[i][0] - index_state[i][0]) + mhdHorizontal
            mhdVertical = abs(index_goal[i][1] - index_state[i][1]) + mhdVertical
        mhdResult = mhdHorizontal + mhdVertical
        return mhdResult

    def maximumofHeuristics(self, node):

        manhattanHeuristic = self.manhattan(node)
        misplacedHeuristic = self.h(node)
        ret = max(misplacedHeuristic, manhattanHeuristic)
        return ret


"""
Notes:
The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
squares is a blank. A state is represented as a tuple of length 9, where  element at
index i represents the tile number  at index i (0 if it's an empty square) 
"""

"""
Question 1: Helper Functions
Write a function called make_rand_8puzzle() that returns a new instance of an EightPuzzle 
problem with a random initial state that is solvable. Note that EightPuzzle has a method
called check_solvability that you should use to help ensure your initial state is solvable.
Write a function called display(state) that takes an 8-puzzle state 
(i.e. a tuple that is a permutation of (0, 1, 2, …, 8)) as input and prints a neat and readable
representation of it. 0 is the blank, and should be printed as a * character.
For example, if state is (0, 3, 2, 1, 8, 7, 4, 6, 5), then display(state) should print:
* 3 2
1 8 7
4 6 5
"""


def make_rand_8puzzle():
    randomlist = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8], 9)
    randomlist = tuple(randomlist)
    EightP = EightPuzzle(randomlist, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))
    if not EightP.check_solvability(EightP.initial):
        while not EightP.check_solvability(EightP.initial):
            randomlist = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8], 9)
            randomlist = tuple(randomlist)
            EightP = EightPuzzle(randomlist, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))
    return EightP


def display(state):
    state = list(state)
    for i in range(9):
        if state[i] == 0:
            state[i] = "*"
    print(state[0], state[1], state[2])
    print(state[3], state[4], state[5])
    print(state[6], state[7], state[8])


"""
Question 2: Comparing Algorithms
Create 10 (more would be better!) random 8-puzzle instances (using your code from above),
and solve each of them using the algorithms below. Each algorithm should be run on the exact 
same set of problems to make the comparison fair.

For each solved problem, record:
the total running time in seconds
the length (i.e. number of tiles moved) of the solution
that total number of nodes that were removed from frontier
You will probably need to make some modifications to the A* code to get all this data.

Also, be aware that the time it takes to solve random 8-puzzle instances can vary from less than
a second to hundreds of seconds — so solving all these problems might take some time!

The algorithms you should test are:

A*-search using the misplaced tile heuristic (this is the default heuristic in the EightPuzzle class)
A*-search using the Manhattan distance heuristic Please implement your own (correctly working!) 
version of the Manhattan heuristic.
Be careful: there is an incorrect Manhattan distance function in tests/test_search.py. 
So don’t use that!
A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic
Summarize all your data in a single table in a spreadsheet as described below.

Based on your data, which algorithm is the best? Explain how you came to your conclusion.

"""


def Outputs(tym, tilesM, Frontiers_Removed):
    print("Total running time is :", tym)
    print("The length (i.e. number of tiles moved) of the solution :", tilesM)
    print("The total number of nodes that were removed from frontier :", Frontiers_Removed, "\n")


def AlgoComparision():
    for i in range(10):
        EightP = make_rand_8puzzle()
        display(EightP.initial)

        print(" ==> A*-search using the misplaced tile heuristic")
        Begin = time.time()
        ret = astar_search(EightP, EightP.h)
        End = time.time() - Begin
        Outputs(End, ret[0].path_cost, ret[1])

        print(" ==> A*-search using the Manhattan distance heuristic")
        Begin = time.time()
        ret = astar_search(EightP, EightP.manhattan)
        End = time.time() - Begin
        Outputs(End, ret[0].path_cost, ret[1])

        print(" ==> A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic")
        Begin = time.time()
        ret = astar_search(EightP, EightP.maximumofHeuristics)
        End = time.time() - Begin
        Outputs(End, ret[0].path_cost, ret[1])

        print("\n")


"""
Question 3: The House-Puzzle
(Duck-puzzle) Implement a new Problem class called DuckPuzzle that is the same as the 8-puzzle, except the board has
 this shape (that looks a bit like a duck facing to the left):

+--+--+
|  |  |
+--+--+--+--+
|  |  |  |  |
+--+--+--+--+
   |  |  |  |
   +--+--+--+

 1 2
 3 4 5 6   goal state
   7 8 *
Tiles slide into the blank (the *) as in the regular 8-puzzle, but now the board has a different shape which changes 
the possible moves.

As in the previous question, test this problem using the same approach, and the same algorithms, as in the previous
 problem.

Be careful generating random instances: the check_solvability function from the EightPuzzle probably doesn’t work 
with this board!

Based on your results, how does the Duck-puzzle compare to the 8-puzzle: is it easier, harder, or about the same 
difficulty?
"""


class DuckPuzzle(Problem):
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

        if index_blank_square in (0, 2, 6):
            possible_actions.remove('LEFT')
        if index_blank_square in (0, 1, 4, 5):
            possible_actions.remove('UP')
        if index_blank_square in (1, 8, 5):
            possible_actions.remove('RIGHT')
        if index_blank_square in (2, 6, 7, 8):
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        deltaNew = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        delta3 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank in (0, 1, 2):
            neighbor = blank + deltaNew[action]
        elif blank in (3,):
            neighbor = blank + delta3[action]
        else:
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
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhdHorizontal = 0
        mhdVertical = 0

        for i in range(9):
            mhdHorizontal = abs(index_goal[i][0] - index_state[i][0]) + mhdHorizontal
            mhdVertical = abs(index_goal[i][1] - index_state[i][1]) + mhdVertical
        mhdResult = mhdHorizontal + mhdVertical
        return mhdResult

    def maximumofHeuristics(self, node):

        manhattanHeuristic = self.manhattan(node)
        misplacedHeuristic = self.h(node)
        ret = max(misplacedHeuristic, manhattanHeuristic)
        return ret

def make_rand_DuckPuzzle():
    randomlist = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8], 9)
    randomlist = tuple(randomlist)
    DuckP = DuckPuzzle(randomlist, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))

    if not DuckP.check_solvability(DuckP.initial):
        while not DuckP.check_solvability(DuckP.initial):
            randomlist = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8], 9)
            randomlist = tuple(randomlist)
            DuckP = EightPuzzle(randomlist, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))

    return DuckP


def displayDuck(state):
    state = list(state)
    for i in range(9):
        if state[i] == 0:
            state[i] = "*"
    print(state[0], state[1])
    print(state[2], state[3], state[4], state[5])
    print(" ", state[6], state[7], state[8])

def OutputsDuck(tym, tilesM, Frontiers_Removed):
    print("Total running time is :", tym)
    print("The length (i.e. number of tiles moved) of the solution :", tilesM)
    print("The total number of nodes that were removed from frontier :", Frontiers_Removed, "\n")


def AlgoComparisionDuck():
    for i in range(10):
        DuckP = make_rand_DuckPuzzle()
        ctr=0
        Begin = time.time()
        ret = astar_search(DuckP, DuckP.h)
        End2 = 0
        Begin2 = 0
        while ret is None:
            print("Still Genrating")
            DuckP = make_rand_DuckPuzzle()
            Begin2 = time.time()
            ctr = 1
            ret = astar_search(DuckP, DuckP.h)
            End2 = time.time() - Begin2
        End = time.time() - Begin
        displayDuck(DuckP.initial)
        print(" ==> A*-search using the misplaced tile heuristic")
        if ctr == 0:
            Outputs(End, ret[0].path_cost, ret[1])
        else:
            Outputs(End2, ret[0].path_cost, ret[1])

        print(" ==> A*-search using the Manhattan distance heuristic")
        Begin = time.time()
        ret = astar_search(DuckP, DuckP.manhattan)
        End = time.time() - Begin
        Outputs(End, ret[0].path_cost, ret[1])

        print(" ==> A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic")
        Begin = time.time()
        ret = astar_search(DuckP, DuckP.maximumofHeuristics)
        End = time.time() - Begin
        Outputs(End, ret[0].path_cost, ret[1])

        print("\n")

Input=(1,2,3)
print("Enter your option: \n1.Compare all the Algorithms for 8 Puzzle \n2.Compare all the Algorithms for Duck Puzzle\n3.Exit")
i=int(input("Enter Your Option : "))
while i in Input:
    if i == 1:
        print("1.Comparing all the Algorithms for 8 Puzzle")
        AlgoComparision()
    elif i == 2:
        print("2. Comparing all the Algorithms for Duck Puzzle")
        AlgoComparisionDuck()
    else:
        exit()
    print( "Enter your option: \n1.Compare all the Algorithms for 8 Puzzle \n2.Compare all the Algorithms for Duck Puzzle\n3.Exit")
    i=int(input("Enter Your Option"))