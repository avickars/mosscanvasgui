# a1.py
#Nathan Kee 301328767 nkee@sfu.ca May 29
import random
import time
from search import *

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
            print("Total Number of Nodes Removed from Frontier: " , count)
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
                    #count += 1


    return None

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


# ______________________________________________________________________________


def ManhattanHeuristic(node):
    Problem = node.state
    #Problem = Node(Problem )
    #listGoal = [[1,2,3],[4,5,6],[7,8,0]]
    goalDict = {1:(0,0), 2:(0,1), 3:(0,2), 4:(1,0), 5:(1,1), 6:(1,2), 7:(2,0), 8:(2,1), 0:(2,2)}
    inputConvert = [[90,90,90],[90,90,90],[90,90,90]]
    origCounter = 0
    manhattanCounter = 0
    for i in range(3):
        for j in range(3):
            inputConvert[i][j] = Problem[origCounter]
            origCounter +=1
    for k in range(3):
        for l in range(3):
            currentValue = inputConvert[k][l]
            manhattanCounter += abs(goalDict[currentValue][0] - k) + abs(goalDict[currentValue][1]-l)
        #print("converted:", listConverted[i][j])
        #print("Goal: ", listGoal[i][j])
    #print(manhattanCounter)
    return manhattanCounter

def ManhattanHeuristicMax(Problem):
    #Problem = Node(Problem )
    #listGoal = [[1,2,3],[4,5,6],[7,8,0]]
    goalDict = {1:(0,0), 2:(0,1), 3:(0,2), 4:(1,0), 5:(1,1), 6:(1,2), 7:(2,0), 8:(2,1), 0:(2,2)}
    inputConvert = [[90,90,90],[90,90,90],[90,90,90]]
    origCounter = 0
    manhattanCounter = 0
    for i in range(3):
        for j in range(3):
            inputConvert[i][j] = Problem[origCounter]
            origCounter +=1
    for k in range(3):
        for l in range(3):
            currentValue = inputConvert[k][l]
            manhattanCounter += abs(goalDict[currentValue][0] - k) + abs(goalDict[currentValue][1]-l)
        #print("converted:", listConverted[i][j])
        #print("Goal: ", listGoal[i][j])
    #print(manhattanCounter)
    return manhattanCounter



# def ManhattanHeuristicNode(node):
#     goalDict = {1:(0,0), 2:(0,1), 3:(0,2), 4:(1,0), 5:(1,1), 6:(1,2), 7:(2,0), 8:(2,1), 0:(2,2)}
#     print(node.state[1])

def MisplacedTileMax(Problem):
    count = 0
    if (Problem[8] != 0):
        count = 1
    for i in range(7):
        if (Problem[i] != i+1):
            count += 1
    return count

def make_rand_8puzzle():
    x = 0
    numberList = (0,1,2,3,4,5,6,7,8)
    shuffled = random.sample(numberList, len(numberList))
    newPuzzle = EightPuzzle(shuffled)
    while(True):
        if (newPuzzle.check_solvability(shuffled) == True):
            print(shuffled, "SOLVABLE CHECK - SUCCESS \n")
            return shuffled
        else:
            print(shuffled, "SOLVABLE CHECK -  FAIL - RESHUFFLING")
            shuffled = random.sample(numberList, len(numberList))
            newPuzzle = EightPuzzle(shuffled)



def display(state):
  statelen = len(state)
  stateList = list(state)
  for i in range(statelen):
    if stateList[i] == 0:
      stateList[i] = "*"
  print("Displaying Puzzle Grid: \n")
  for j in range(0,8,3):
    print("|", (stateList[j]) , (stateList[j+1]) , (stateList[j+2]), "|", "\n")
  for k in range(statelen):
    if stateList[k] == "*":
      stateList[k] = 0
    state = tuple(stateList)
  return


#add counter at del frontier[child] in best_first_graph_search
def astar_search(problem, h=None, display=True):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)



for i in range(10):
    print("----------------")
    print("Puzzle NUMBER ", i+1, "\n")
    randomPuzzle = make_rand_8puzzle()
    #randomPuzzle = (3, 4, 1, 2, 0, 6, 8, 7, 5)
    #randomPuzzle = (4,7,1,8,6,0,5,3,2)
    TuplerandomPuzzle = EightPuzzle(tuple(randomPuzzle))
    ManhattanMax = ManhattanHeuristicMax(randomPuzzle)
    MisplacedMax = MisplacedTileMax(randomPuzzle)
    maxCalculate = max(ManhattanMax, MisplacedMax)
    display(randomPuzzle)
    print("----------MISPLACED TILE HEURISTIC----------")
    startTime = time.time()
    astarresult = astar_search(TuplerandomPuzzle)
    print("This Puzzle took %s seconds to solve" % (time.time() - startTime))
    print("Puzzle Solution Length: ", astarresult.path_cost, "\n")
    #manhattanResult = astar_search(TuplerandomPuzzle, ManhattanHeuristic)
    print("----------MANHATTAN DISTANCE HEURISTIC----------")
    manstartTime = time.time()
    manastarresult = astar_search(TuplerandomPuzzle, ManhattanHeuristic)
    print("This Puzzle took %s seconds to solve" % (time.time() - manstartTime))
    print("Puzzle Solution Length: ", manastarresult.path_cost, "\n")
    print("----------MAX CALCULATED HEURISTIC----------")
    if (maxCalculate == ManhattanMax):
        print("The Maximum Heuristic is The Manhattan Distance Heuristic")
        manstartTime = time.time()
        manastarresult = astar_search(TuplerandomPuzzle, ManhattanHeuristic)
        print("This Puzzle took %s seconds to solve" % (time.time() - manstartTime))
        print("Puzzle Solution Length: ", manastarresult.path_cost, "\n")
    else:
        print("The Maximum Heuristic is The Misplaced Tile Heuristic")
        startTime = time.time()
        astarresult = astar_search(TuplerandomPuzzle)
        print("This Puzzle took %s seconds to solve" % (time.time() - startTime))
        print("Puzzle Solution Length: ", astarresult.path_cost, "\n")



    #ManhattanHeuristic(randomPuzzle)
    #ManhattanHeuristicNode(randomPuzzle)
    #define new heuristic (hsomething) within the EightPuzzle class. Then create the heuristic to count how many steps away each puzzle is and add it up. This is for the Manhattan heuristic. Add up the total number of moves needed for all the tiles to be moved to the right place. Then run search using the new def.Modify the search above to use the new heuristic.

    #Finish working on cost paths
    #Make the Manhattan version and take the max


    #for house, make it do some number of random moves. THEN run the solve and get the stats
