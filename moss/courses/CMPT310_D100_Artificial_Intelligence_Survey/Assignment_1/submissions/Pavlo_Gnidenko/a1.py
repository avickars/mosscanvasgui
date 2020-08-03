# a1.py
from search import *
import random
import time
# ...

# global definitions
goalState = [1, 2, 3, 4, 5, 6, 7, 8, 0]

class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 3:
            return possible_actions

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 1 or index_blank_square == 5:
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
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattanH(self, node):
        total = 0
        for i in range(0,9):
            targetIndex = node.state[i] - 1
            x1 = i % 3
            y1 = (int)(i / 3)
            x2 = targetIndex % 3
            y2 = (int)(targetIndex / 3)
            total = total + abs(x2 - x1) + abs(y2 - y1)
        return total
        
    def maxH(self, node):
        manSum = 0
        for i in range(0,9):
            targetIndex = node.state[i] - 1
            x1 = i % 3
            y1 = (int)(i / 3)
            x2 = targetIndex % 3
            y2 = (int)(targetIndex / 3)
            manSum = manSum + abs(x2 - x1) + abs(y2 - y1)
        hSum = sum(s != g for (s, g) in zip(node.state, self.goal))
        if hSum > manSum:
            total = hSum
        else:
            total = manSum
        return total

class EightPuzzleA1(EightPuzzle):
    def manhattanH(self, node):
        total = 0
        for i in range(0,9):
            targetIndex = node.state[i] - 1
            x1 = i % 3
            y1 = (int)(i / 3)
            x2 = targetIndex % 3
            y2 = (int)(targetIndex / 3)
            total = total + abs(x2 - x1) + abs(y2 - y1)
        return total
    def maxH(self, node):
        manSum = 0
        for i in range(0,9):
            targetIndex = node.state[i] - 1
            x1 = i % 3
            y1 = (int)(i / 3)
            x2 = targetIndex % 3
            y2 = (int)(targetIndex / 3)
            manSum = manSum + abs(x2 - x1) + abs(y2 - y1)
        hSum = sum(s != g for (s, g) in zip(node.state, self.goal))
        if hSum > manSum:
            total = hSum
        else:
            total = manSum
        return total

def best_first_graph_searchCopy(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    nodeDeleted = 0
    explored = set()
    while frontier:
        node = frontier.pop()
        #nodeDeleted += 1
        if problem.goal_test(node.state):
            if display:
                print("Solution length: ", len(explored))
                print("Nodes deleted: ", nodeDeleted)
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                nodeDeleted += 1
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

# solvable DuckPuzzle Problem
def makeRandDuckPuzzle():
    initial = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    index_blank_square = 8
    for i in range(0, 3000):
        new_state = list(initial)
            # find legal moves
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        actionsCount = 4
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
            actionsCount -= 1
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 1 or index_blank_square == 5:
            possible_actions.remove('UP')
            actionsCount -= 1
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
            actionsCount -= 1
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')
            actionsCount -= 1
        # choose a random legal move
        rand = random.randint(0, actionsCount - 1)
        move = possible_actions[rand]
        # make the move
        delta = 0
        if move == 'UP':
            if index_blank_square > 5:
                delta = -3
            else:
                delta = -2
        if move == 'DOWN':
            if index_blank_square < 2:
                delta = 2
            else:
                delta = 3
        if move == 'LEFT':
            delta = -1
        if move == 'RIGHT':
            delta = 1
        neighbor = index_blank_square + delta
        new_state[index_blank_square], new_state[neighbor] = new_state[neighbor], new_state[index_blank_square]
        index_blank_square = neighbor
        initial = tuple(new_state)
    puzzle = DuckPuzzle(initial)
    while puzzle.check_solvability(initial) == False:
        initial = makeRandTuple()
    puzzle.initial = initial
    return puzzle

# fully random 8-puzzle board
def makeRandTuple():
    array = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(array)
    initial = ()
    for i in range(0,9):
        initial = initial + (array[i],)
    return initial

# get a solvable EightPuzzle Problem
def make_rand_8puzzle():
    initial = makeRandTuple()
    puzzle = EightPuzzleA1(initial)
    while puzzle.check_solvability(initial) == False:
        initial = makeRandTuple()
    puzzle.initial = initial
    return puzzle

# print a board state
def display(state):
    iBlank = state.index(0)
    for i in range(0,3):
        if iBlank == 3 * i or iBlank == 3 * i + 1 or iBlank == 3 * i + 2:
            if iBlank % 3 == 0:
                print("*", state[3 * i + 1], state[3 * i + 2])
            if iBlank % 3 == 1:
                print(state[3 * i], "*", state[3 * i + 2])
            if iBlank % 3 == 2:
                print(state[3 * i], state[3 * i + 1], "*")
        else:
            print(state[3 * i], state[3 * i + 1], state[3 * i + 2])
    return

# program start

puzzles1 = []
puzzles2 = []
puzzles3 = []
for i in range(0,10):
    puzzles1.append(make_rand_8puzzle())
    puzzles2.append(make_rand_8puzzle())
    puzzles3.append(make_rand_8puzzle())
print("- - - Solving A* - - -") 
for i in range(0,10):
    print("Puzzle #", i + 1)
    # display(puzzles[i].initial)
    start_time = time.time()
    best_first_graph_searchCopy(puzzles1[i], puzzles1[i].h, True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}')
print("- - - Solving A* man - - -") 
for i in range(0,10):
    print("Puzzle #", i + 1)
    # display(puzzles[i].initial)
    start_time = time.time()
    best_first_graph_searchCopy(puzzles2[i], puzzles2[i].manhattanH, True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}')
print("- - - Solving A* max - - -") 
for i in range(0,10):
    print("Puzzle #", i + 1)
    # display(puzzles[i].initial)
    start_time = time.time()
    best_first_graph_searchCopy(puzzles3[i], puzzles3[i].maxH, True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}')

# Duck solution:

puzzles1 = []
puzzles2 = []
puzzles3 = []
initial = makeRandTuple()
for i in range(0,10):
    puzzles1.append(makeRandDuckPuzzle())
    puzzles2.append(makeRandDuckPuzzle())
    puzzles3.append(makeRandDuckPuzzle())
for i in range(0,10):
    print("Puzzle #", i + 1)
    # display(puzzles[i].initial)
    start_time = time.time()
    best_first_graph_searchCopy(puzzles1[i], puzzles1[i].h, True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}')
print("- - - Solving A* man - - -") 
for i in range(0,10):
    print("Puzzle #", i + 1)
    # display(puzzles[i].initial)
    start_time = time.time()
    best_first_graph_searchCopy(puzzles2[i], puzzles2[i].manhattanH, True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}')
print("- - - Solving A* max - - -") 
for i in range(0,10):
    print("Puzzle #", i + 1)
    # display(puzzles[i].initial)
    start_time = time.time()
    best_first_graph_searchCopy(puzzles3[i], puzzles3[i].maxH, True)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}')