#a1.py

from search import *
import random
import time

########################################################################

# Question 1: Helper Functions

########################################################################

def make_rand_8puzzle():
    """Return a solvable random Eight Puzzle object"""
    randomList = random.sample(range(0,9), 9)
    newPuzzle = EightPuzzle(tuple(randomList))
    while(not newPuzzle.check_solvability(newPuzzle.initial)):
        randomList = random.sample(range(0,9), 9)
        newPuzzle = EightPuzzle(tuple(randomList))
    return newPuzzle

def particular8puzzle():
    """Return a particular Eight Puzzle object used for testing purposes"""
    state = (4, 7, 1, 8, 6, 0, 5, 3, 2)
    puzzle = EightPuzzle(state)
    return puzzle
    
def display8Puzzle(state):
    """Display the Eight Puzzle in a nice format with 0 represented as * (blank state)"""
    print()
    index = 1
    for i in range(9):
        if(state[i] == 0):
            print('*', end = ' ')
        else:
            print(state[i], end = ' ')
        if(index%3 == 0):
            print()
        index += 1
    print()

########################################################################

# Question 2: Comparing Algorithms

########################################################################

def aStarSearch(puzzle, h1=None, h2=None):
    start_time = time.time()

    # Case for max(h1, h2) function
    if((h1 and h2) is not None):
        node = astar_search_a1(puzzle, h1, h2, True)
    # Case for one heuristic function
    elif(h1 is not None):
        node = astar_search_a1(puzzle, h1, None, True)
    else:
        print("Error at aStarSearch")
        return -1

    elapsed_time = time.time() - start_time

    print("Solution Length:", len(node.path()))
    print(f'elapsed time (in seconds): {elapsed_time}s')

def astar_search_a1(problem, h1=None, h2=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""

    # Case for max(h1, h2) function
    if((h1 and h2) is not None):
        return best_first_graph_search_a1(problem, lambda n: n.path_cost + max(h1(n), h2(n)), display)
    # Case for one heuristic function
    elif(h1 is not None):
        return best_first_graph_search_a1(problem, lambda n: n.path_cost + h1(n), display)
    else:
        print("Error at astar_search_a1")
        return -1

def best_first_graph_search_a1(problem, f, display=False):
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
                print("Number of nodes removed:", len(explored)+1)
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

def eightPuzzleMisplacedTile_h(node):
    """ Return the Misplaced Tile heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles. Copied from search.py, this heuristic ignores the (0) blank tile case
    This is so the heuristic is admissible and it does not overestimate"""
    goalState = (1, 2, 3, 4, 5, 6 , 7, 8, 0)
    return sum((s != g and s != 0) for (s, g) in zip(node.state, goalState))

def eightPuzzleManhattan_h(node):
    """ Return the Manhattan distance sum for a given state. """
    coordinates = {1:(0,0), 2:(1,0), 3:(2,0),
                    4:(0,1), 5:(1,1), 6:(2,1),
                    7:(0,2), 8:(1,2), 9:(2,2)}
    manhattanDistanceSum = 0
    index = 1
    for i in node.state:
        if(i != 0):
            x_goal = coordinates.get(index)[0]
            x_state = coordinates.get(i)[0]
            y_goal = coordinates.get(index)[1]
            y_state = coordinates.get(i)[1]
            manhattanDistanceSum += abs(x_goal - x_state) + abs(y_goal - y_state)
        index += 1
    return manhattanDistanceSum

def make_and_solve_8puzzle():
    "Make and solve one Eight Puzzle"
    puzzle = make_rand_8puzzle()
    display8Puzzle(puzzle.initial)
    aStarSearch(puzzle, eightPuzzleMisplacedTile_h)
    print()
    aStarSearch(puzzle, eightPuzzleManhattan_h)
    print()
    aStarSearch(puzzle, eightPuzzleMisplacedTile_h, eightPuzzleManhattan_h)
    return 0

########################################################################

# Question 3: The Duck Puzzle

########################################################################

class DuckPuzzle(Problem):
    def __init__(self, initial=(1, 2, 3, 4, 5, 6, 7, 8, 0), goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)
    
    def display(self, state):
        """Display given state of the Duck Puzzle"""
        index = 0
        for i in state:
            if(index == 2):
                print('\n' + str(i), end = ' ')
            elif (index == 6):
                print('\n  ' + str(i), end = ' ')
            else:
                print(str(i), end = ' ')
            index += 1
        print()
        return True

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if(index_blank_square == 0 or 
           index_blank_square == 1 or
           index_blank_square == 4 or
           index_blank_square == 5):
            possible_actions.remove('UP')
        if(index_blank_square == 2 or
           index_blank_square == 6 or
           index_blank_square == 7 or
           index_blank_square == 8):
            possible_actions.remove('DOWN')
        if(index_blank_square == 0 or
           index_blank_square == 2 or
           index_blank_square == 6):
            possible_actions.remove('LEFT')
        if(index_blank_square == 1 or
           index_blank_square == 5 or
           index_blank_square == 8):
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': 0, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}

        if(blank == 6 or blank == 7 or blank == 8):
            delta['UP'] = -3
        elif(blank == 2):
            delta['UP'] = -2
        elif(blank == 3):
            delta['UP'] = -3
            delta['DOWN'] = 3
        elif(blank == 0 or
             blank == 1 ):
            delta['DOWN'] = 2
        elif(blank == (4 or 5)):
            delta['DOWN'] = 3

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def misplacedTile_h(self, node):
        """ Return the Misplaced Tile heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles. Copied from search.py, this heuristic ignores the (0) blank tile case.
        This is so the heuristic is admissible and it does not overestimate"""

        return sum((s != g and s != 0) for (s, g) in zip(node.state, self.goal))

    def manhattanDistance_h(self, node):
        coordinates = {1:(0,0), 2:(1,0), 
                   3:(0,1), 4:(1,1), 5:(2,1), 6:(3,1),
                            7:(2,1), 8:(2,2), 9:(3,2)}
        manhattanDistanceSum = 0
        index = 1
        for i in node.state:
            if(i != 0):
                x_goal = coordinates.get(index)[0]
                x_state = coordinates.get(i)[0]
                y_goal = coordinates.get(index)[1]
                y_state = coordinates.get(i)[1]
                manhattanDistanceSum += abs(x_goal - x_state) + abs(y_goal - y_state)
            index += 1
        return manhattanDistanceSum

def displayDuckPuzzle(state):
    """Display the Duck Puzzle in a nice format with 0 represented as * (blank state)"""
    index = 0
    for i in state:
        if(index == 2):
            print('\n' + str(i), end = ' ')
        elif (index == 6):
            print('\n  ' + str(i), end = ' ')
        else:
            print(str(i), end = ' ')
        index += 1
    print("\n")
    return True

def randomizeDuckPuzzle(puzzle):
    """ Randomizes an intial generated Duck Puzzle by making a random choice (1, 100000) of legal movements"""
    node = Node(puzzle.initial)
    
    # runForTime = 60
    # t_end = time.time() + runForTime

    iterations = random.randint(1, 100000)

    for i in range(iterations):
        possible_actions = puzzle.actions(node.state)
        action = random.choice(possible_actions)
        newState = puzzle.result(node.state, action)
        puzzle = DuckPuzzle(newState)
        node = Node(puzzle.initial)
    
    return puzzle
    
def make_and_solve_DuckPuzzle():
    "Make and solve one Duck Puzzle"
    puzzle = DuckPuzzle()
    puzzle = randomizeDuckPuzzle(puzzle)
    puzzle.display(puzzle.initial)
    aStarSearch(puzzle, puzzle.misplacedTile_h)
    print()
    aStarSearch(puzzle, puzzle.manhattanDistance_h)
    print()
    aStarSearch(puzzle, puzzle.misplacedTile_h, puzzle.manhattanDistance_h)
    return 0

def main():
    print("Eight Puzzle:")
    print("-------------------------------------------------------------------------------------\n")
    for i in range(20):
        print(str(i+1)+".")
        make_and_solve_8puzzle()
        print()
    print("Duck Puzzle:")
    print("-------------------------------------------------------------------------------------\n")
    for i in range(20):
        print(str(i+1)+".")
        make_and_solve_DuckPuzzle()
        print()
    return 0

main()