from search import EightPuzzle
from search import Problem
import random
from collections import deque
from utils import *
import time

"""
Code from search.py that has been brought here and modified:
    Node class -> has a self.numRemovedFromFrontier member variable to keep track of pop operations from frontier during best_first_graph_search
    best_first_graph_search -> has a small modification to keep number of pop operations and sets numRemovedFromFrontier for root node before returning it
"""
class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        self.numRemovedFromFrontier = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)

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
    popCount = 0
    while frontier:
        node = frontier.pop()
        popCount+=1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            node.numRemovedFromFrontier = popCount
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

"""
helper functions
"""
def make_rand_8puzzle():
    randList = []
    alreadySeen = set()
    
    while (len(alreadySeen) < 9):
        randInt = random.randint(0,8)
        if (randInt not in alreadySeen):
            alreadySeen.add(randInt)
            randList.append(randInt)

    rand_8puzzle = EightPuzzle(tuple(randList))
    return rand_8puzzle

def display(state : tuple):
    counter = 1
    for i in state:
        if (i == 0):
            print("*", end = " ")
        else:
            print(i, end = " ")
        counter += 1
        if (counter == 4):
            print("")
            counter = 1

"""
DuckPuzzle class definition
"""
# changed the possible actions due to new dimensions
# also changed the delta to account for new dimensions
class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if (blank == 3):
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if (blank < 3):
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def check_solvability(self, state):
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

#### helper function to make random duck puzzles -> starts from goal state and takes a random move random times (between 1 to 1 mil)

def make_random_duck_puzzle():
    duckPuzzle = DuckPuzzle(initial = (1,2,3,4,5,6,7,8,0))
    randInt = random.randint(1, 1000000)
    for i in range(randInt):
        poss_actions = duckPuzzle.actions(duckPuzzle.initial)
        duckPuzzle.initial = duckPuzzle.result(duckPuzzle.initial, random.choice(poss_actions))
    return duckPuzzle


"""
some testing code ...
"""

# testEightPuzzle = make_rand_8puzzle()
# testDuckTuple = (1, 2, 3, 0, 4, 6, 7, 5, 8)
# testDuckPuzzle = DuckPuzzle(testDuckTuple)
# print("this is index of 0: "+str(testEightPuzzle.find_blank_square(testEightPuzzle.initial)))
# display(testEightPuzzle.initial)
# if (testEightPuzzle.check_solvability(testEightPuzzle.initial)):
#     res = astar_search(testEightPuzzle)
#     print("this is the result: "+ str(res.path_cost))
#     print("this is the number of elements removed from frontier "+str(res.numRemovedFromFrontier))
# else:
#     print("not solvable")

# if (testEightPuzzle.check_solvability(testEightPuzzle.initial)):
#     res = astar_search(testDuckPuzzle)
#     print("this is the duck puzzle result: "+ str(res.path_cost))
#     print("this is the number of elements removed from frontier "+str(res.numRemovedFromFrontier))
# else:
#     print("not solvable")

"""
definitions for the three heuristics
"""

def default(node): # from the github repo code
        return sum(s != g for (s, g) in zip(node.state, (1,2,3,4,5,6,7,8,0)))

def manhattan(node): # fixed the github repo error -> should be "for i in range(9)" instead of "for i in range(8)"
    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    for i in range(9): # changed this to 9 - it was originally 8 in the code from github repo
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

    return mhd

def maxOfTwo(node):
    mhd = manhattan(node)
    defaultVal = default(node)

    return max(mhd, defaultVal)

""" 
looping 20 times for each heuristic
"""
#### default heuristic
print("\n starting 8 puzzle loops \n")
for i in range(20):
    testEightPuzzle = make_rand_8puzzle()
    print("this is index of 0 for loop ", i, " : ", str(testEightPuzzle.find_blank_square(testEightPuzzle.initial)))
    display(testEightPuzzle.initial)
    if (testEightPuzzle.check_solvability(testEightPuzzle.initial)):
        print("loop: "+str(i))
        #### default heuristic
        t_0 = time.clock() # from tutorial code
        res = astar_search(testEightPuzzle)
        t_1 = time.clock()
        print("this is the result for default: "+ str(res.path_cost))
        print("this is the number of elements removed from frontier: "+str(res.numRemovedFromFrontier))
        print("Time Elasped for default: ", t_1-t_0)
        #### manhattan heuristic
        t_0 = time.clock() # from tutorial code
        res = astar_search(testEightPuzzle, h=manhattan)
        t_1 = time.clock()
        print("this is the result for manhattan: "+ str(res.path_cost))
        print("this is the number of elements removed from frontier: "+str(res.numRemovedFromFrontier))
        print("Time Elasped for manhattan:", t_1-t_0)
        #### best of two
        t_0 = time.clock() # from tutorial code
        res = astar_search(testEightPuzzle, h=maxOfTwo)
        t_1 = time.clock()
        print("this is the result for best of two: "+ str(res.path_cost))
        print("this is the number of elements removed from frontier: "+str(res.numRemovedFromFrontier))
        print("Time Elasped for best of two: ", t_1-t_0)
    else:
        print("loop ", i, " not solvable")

"""
Same three heuristics for DuckPuzzle -> loop 10 times
"""
print("\n starting duck puzzle loops\n")
for i in range(10):
    testDuckPuzzle = make_random_duck_puzzle()
    print("this is index of 0 for loop ", i, " : ", str(testDuckPuzzle.find_blank_square(testDuckPuzzle.initial)))
    #### default
    t_0 = time.clock() # from tutorial code
    res = astar_search(testDuckPuzzle)
    t_1 = time.clock()
    print("this is the result for default: "+ str(res.path_cost))
    print("this is the number of elements removed from frontier: "+str(res.numRemovedFromFrontier))
    print("Time Elasped for default: ", t_1-t_0)
    #### manhattan
    print("this is index of 0 for loop ", i, " : ", str(testDuckPuzzle.find_blank_square(testDuckPuzzle.initial)))
    t_0 = time.clock() # from tutorial code
    res = astar_search(testDuckPuzzle, h=manhattan)
    t_1 = time.clock()
    print("this is the result for manhattan: "+ str(res.path_cost))
    print("this is the number of elements removed from frontier: "+str(res.numRemovedFromFrontier))
    print("Time Elasped for manhattan: ", t_1-t_0)
    #### best of two
    t_0 = time.clock() # from tutorial code
    res = astar_search(testDuckPuzzle, h=maxOfTwo)
    t_1 = time.clock()
    print("this is the result for best of two: "+ str(res.path_cost))
    print("this is the number of elements removed from frontier: "+str(res.numRemovedFromFrontier))
    print("Time Elasped for best of two: ", t_1-t_0)


    






