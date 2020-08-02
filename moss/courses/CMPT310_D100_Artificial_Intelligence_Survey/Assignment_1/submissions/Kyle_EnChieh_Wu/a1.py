from search import *
import random
import time

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# x     Things that were changed in search.py but brought here      x
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# The functions from search.py now have "New" appended to their function names in a1.py
# For example best_first_graph_search() is now best_first_graph_searchNew()

# eightpuzzle class had to be brought over since misplaced needed to be changed so that it would not count the zero tile


class EightPuzzleNew(Problem):
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

        # if the tile is misplaced AND if the tile is not zero since we do not count the zero tile
        return sum((s != g and s!=0) for (s, g) in zip(node.state, self.goal))


# ______________________________________________________________________________

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

        noUp = (0, 1, 4, 5)
        noRight = (2, 5, 8)
        noDown = (2, 6, 7, 8)
        noLeft = (0, 2, 6)

        if index_blank_square in noLeft:
            possible_actions.remove('LEFT')
        if index_blank_square in noUp:
            possible_actions.remove('UP')
        if index_blank_square in noRight:
            possible_actions.remove('RIGHT')
        if index_blank_square in noDown:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if(blank < 3): delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif(blank > 3): delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif(blank == 3): delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    # mix up the tiles
    def shuffle(self, state=None):
        new_state = list(self.initial)
        for i in range(10000):
            actionsList = self.actions(new_state)
            new_state = self.result(new_state, actionsList[random.randint(0, len(actionsList) - 1)])
        self.initial = tuple(new_state)

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        # if the tile is misplaced AND if the tile is not zero since we do not count the zero tile
        return sum((s != g and s != 0) for (s, g) in zip(node.state, self.goal))


# _______________________________________________________________________________________________


def best_first_graph_searchNew(problem, f, display=False):
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
    frontierCount = 0
    while frontier:
        node = frontier.pop()
        frontierCount += 1
        if problem.goal_test(node.state):
            if display:
                print("Length of solution: ", len(node.solution()),
                      "\nNumber of nodes removed from frontier: ", frontierCount)
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

# _______________________________________________________________________________________________


def astar_searchNew(problem, h=None, display=False, maxFlag=False, manhattanTemp=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    if(maxFlag): return best_first_graph_searchNew(problem, lambda n: n.path_cost + (h(n) if h(n)>manhattanTemp(n) else manhattanTemp(n)), display)
    return best_first_graph_searchNew(problem, lambda n: n.path_cost + h(n), display)

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# x                     Question 1                                  x
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


def make_rand_8puzzle():
    tempList = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    tempList = tuple(random.sample(tempList, 9))
    tempEightPuzzle = EightPuzzleNew(tempList)
    tempEightPuzzle.check_solvability(tempList)

    while(tempEightPuzzle.check_solvability(tempList) == False):
        tempList = tuple(random.sample(tempList, 9))
        tempEightPuzzle = EightPuzzleNew(tempList)

    return tempEightPuzzle


def displayEight(state):
    state = list(state)
    index = state.index(0)
    state[index] = "*"
    for i in range(3):
        j = i*3
        print(str(state[j]) + " " + str(state[j+1]) + " " + str(state[j+2]))

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# x                     Question 2                                  x
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


def manhattanEight(node):
    distances = (
        # do not count 0, so all the values are zero

        # 0
        (0, 0, 0,
         0, 0, 0,
         0, 0, 0),
        # (4, 3, 2,
        #  3, 2, 1,
        #  2, 1, 0),

        # 1
        (0, 1, 2,
         1, 2, 3,
         2, 3, 4),

        # 2
        (1, 0, 1,
         2, 1, 2,
         3, 2, 3),

        # 3
        (2, 1, 0,
         3, 2, 1,
         4, 3, 2),

        # 4
        (1, 2, 3,
         0, 1, 2,
         1, 2, 3),

        # 5
        (2, 1, 2,
         1, 0, 1,
         2, 1, 2),

        # 6
        (3, 2, 1,
         2, 1, 0,
         3, 2, 1),

        # 7
        (2, 3, 4,
         1, 2, 3,
         0, 1, 2),

        # 8
        (3, 2, 3,
         2, 1, 2,
         1, 0, 1),

    )

    total = 0

    for i in range(9):
        total += distances[node.state[i]][i]

    return total


def aStar(obj):
    print("\nMisplaced")
    print("------------------------")
    startTime = time.time()
    astar_searchNew(obj, None, True)
    endTime = time.time()
    print("Completed in:", endTime-startTime, "seconds")


def aStarMan(obj, manhattanTemp):
    print("\nManhattan")
    print("------------------------")
    startTime = time.time()
    astar_searchNew(obj, manhattanTemp, True)
    endTime = time.time()
    print("Completed in:", endTime-startTime, "seconds")


def aStarMax(obj, manhattanTemp):
    print("\nMax")
    print("------------------------")
    startTime = time.time()
    astar_searchNew(obj, None, True, True, manhattanTemp)
    endTime = time.time()
    print("Completed in:", endTime-startTime, "seconds")


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# x                     Question 3                                  x
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# a lot of functions were reused for duck-puzzle from 8-puzzle
def make_rand_duckpuzzle():
    tempList = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    tempDuckPuzzle = DuckPuzzle(tempList)

    return tempDuckPuzzle


def displayDuck(state):
    state = list(state)
    index = state.index(0)
    state[index] = "*"
    print(str(state[0]) + " " + str(state[1]))
    print(str(state[2]) + " " + str(state[3]) + " " + str(state[4]) + " " + str(state[5]))
    print(" " + " " + str(state[6]) + " " + str(state[7]) + " " + str(state[8]))


def manhattanDuck(node):
    distances = (

        # (5, 4,
        #  4, 3, 2, 1,
        #     2, 1, 0),

        # 0
        (0, 0,
         0, 0, 0, 0,
            0, 0, 0),

        # 1
        (0, 1,
         1, 2, 3, 4,
            3, 4, 5),

        # 2
        (1, 0,
         2, 1, 2, 3,
            2, 3, 4),

        # 3
        (1, 2,
         0, 1, 2, 3,
            2, 3, 4),

        # 4
        (2, 1,
         1, 0, 1, 2,
            1, 2, 3),

        # 5
        (3, 2,
         2, 1, 0, 1,
            2, 1, 2),

        # 6
        (4, 3,
         3, 2, 1, 0,
            3, 2, 1),

        # 7
        (3, 2,
         2, 1, 2, 3,
            0, 1, 2),

        # 8
        (4, 3,
         3, 2, 1, 2,
            1, 0, 1),

    )

    total = 0

    for i in range(9):
        total += distances[node.state[i]][i]

    return total


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# x     Two loops to run both 8-puzzle as well as duck-puzzle       x
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
print("\n\n\nxxxxxxxxxxxxxxxxxx\nxxx Question 2 xxx\nxxxxxxxxxxxxxxxxxx\n")
eightObjList = []
for i in range(10):
    print("\n")
    print("Test number: ", i+1)

    eightObjList.append(make_rand_8puzzle())
    displayEight(eightObjList[i].initial)
    aStar(eightObjList[i])
    aStarMan(eightObjList[i], manhattanEight)
    aStarMax(eightObjList[i], manhattanEight)

print("\n\nxxxxxxxxxxxxxxxxxx\nxxx Question 3 xxx\nxxxxxxxxxxxxxxxxxx\n")
duckObjList = []
for i in range(10):
    print("\n")

    print("Test number: ", i+1)

    duckObjList.append(make_rand_duckpuzzle())
    duckObjList[i].shuffle()
    displayDuck(duckObjList[i].initial)
    aStar(duckObjList[i])
    aStarMan(duckObjList[i], manhattanDuck)
    aStarMax(duckObjList[i], manhattanDuck)
print('\n')
