#!/home/epolovina/anaconda3/bin/python3

import time
from search import *
from random import shuffle, choice
# import json

res = {}
def generate_state():
    state = [0,1,2,3,4,5,6,7,8]
    shuffle(state)
    return state

def make_rand_8puzzle():
    '''
    Write a function called make_rand_8puzzle() that returns a new instance of 
    an EightPuzzle problem with a random initial state that is solvable. Note 
    that EightPuzzle has a method called check_solvability that you should use 
    to help ensure your initial state is solvable.
    '''
    
    state = generate_state()
    ep = EightPuzzle(tuple(state))

    while not ep.check_solvability(state):
        state = generate_state()

    display(state)
    return EightPuzzle(tuple(state))

def misplacedTile(node):
    """ Return the heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles """
    goal = EightPuzzle(node.state).goal
    return sum(s != g and s != 0 for (s, g) in zip(node.state, goal))

def misplacedTileDuck(node):
    """ Return the heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles """

    goal = DuckPuzzle(node.state).goal
    return sum(s != g and s != 0 for (s, g) in zip(node.state, goal))

def display(state):
    '''
    Write a function called display(state) that takes an 8-puzzle state (i.e. 
    a tuple that is a permutation of (0, 1, 2, …, 8)) as input and prints a 
    neat and readable representation of it. 0 is the blank, and should be 
    printed as a * character.
    '''

    for idx, val in enumerate(state, start=1):
        if val != 0:
            print(val, end=" ")
        else:
            print("*", end=" ")
        if not idx % 3:
            print()

def manhattan(node):
    # Adapted and fixed from tests/test_search.py
    state = node.state
    index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    for i in range(1,9): # from 1-9 so that we do not count the 0
        for j in range(2):
            mhd = abs(index_state[i][j] - index_goal[i][j]) + mhd

    return mhd

def manhattanDuck(node):
    # Adapted and fixed from tests/test_search.py
    state = node.state
    index_goal = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
    index_state = {}
    index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    for i in range(1,9): # do not count the 0
        for j in range(2):
            mhd = abs(index_state[i][j] - index_goal[i][j]) + mhd

    return mhd

def max_tile_manhattan(node):
    h_result = misplacedTile(node)
    manhattan_result = manhattan(node)
    return max(h_result, manhattan_result)

def max_tile_manhattan_duck(node):
    h_result = misplacedTileDuck(node)
    manhattan_result = manhattanDuck(node)
    return max(h_result, manhattan_result)


def compare_algorithms(trial):
    eight_puzzle = make_rand_8puzzle()

    dataDict = { "trial":trial } # save it to a dict later for analysis

    print()
    print("**************** MISPLACED TILE ***************")
    start = time.time()
    res, solution = astar_search(eight_puzzle,h=misplacedTile, display=True)
    print("Length of solution is: ", len(res.solution()))
    print("Removed from the frontier is: ", (solution))
    end = time.time()
    print("Elapsed time (s): ", end-start)
    dataDict["state_h"] = str(eight_puzzle.initial)
    dataDict["length_h"] =  len(res.solution())
    dataDict["removed_h"] =  solution
    dataDict["time_h"] = end-start
    print()

    print("**************** MANHATTAN **************** ")
    start = time.time()
    res, solution = astar_search(eight_puzzle, h=manhattan, display=True)
    print("Length of solution is: ", len(res.solution()))
    print("Removed from the frontier: ", (solution))
    end = time.time()
    print("Elapsed time (s): ", end-start)
    dataDict["length_man"] =  len(res.solution())
    dataDict["removed_man"] =  solution
    dataDict["time_man"] = end-start
    print()

    print("**************** MAX OF MISPLACED AND MANHATTAN **************** ")
    start = time.time()
    res, solution = astar_search(eight_puzzle, h=max_tile_manhattan, display=True)
    print("Length of solution is: ", len(res.solution()))
    print("Removed from the frontier is: ", (solution))
    end = time.time()
    print("Elapsed time (s): ", end-start)
    dataDict["length_max"] =  len(res.solution())
    dataDict["removed_max"] =  solution
    dataDict["time_max"] = end-start
    print()
    return dataDict


def compare_algorithms_duck(trial):
    duck = make_rand_duck_puzzle()

    dataDict = { "trial":trial }

    print()
    print("**************** MISPLACED TILE ***************")
    start = time.time()
    res, solution = astar_search(duck, h=misplacedTileDuck, display=True)
    print("Length of solution is: ", len(res.solution()))
    print("Removed from the frontier is: ", (solution))
    end = time.time()
    print("Elapsed time (s): ", end-start)
    dataDict["state_h"] = str(duck.initial)
    dataDict["length_h"] =  len(res.solution())
    dataDict["removed_h"] =  solution
    dataDict["time_h"] = end-start
    print()

    print("**************** MANHATTAN **************** ")
    start = time.time()
    res, solution = astar_search(duck, h=manhattanDuck, display=True)
    print("Length of solution is: ", len(res.solution()))
    print("Removed from the frontier: ", (solution))
    end = time.time()
    print("Elapsed time (s): ", end-start)
    dataDict["length_man"] =  len(res.solution())
    dataDict["removed_man"] =  solution
    dataDict["time_man"] = end-start
    print()

    print("**************** MAX OF MISPLACED AND MANHATTAN **************** ")
    start = time.time()
    res, solution = astar_search(duck, h=max_tile_manhattan_duck, display=True)
    print("Length of solution is: ", len(res.solution()))
    print("Removed from the frontier is: ", (solution))
    end = time.time()
    print("Elapsed time (s): ", end-start)
    dataDict["length_max"] =  len(res.solution())
    dataDict["removed_max"] =  solution
    dataDict["time_max"] = end-start
    print()
    return dataDict # return dict of data points


# Question 3
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)
        self.goal = goal

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        if index_blank_square == 1:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        if index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank == 0:
            delta = {'UP': 0, 'DOWN': 2, 'LEFT': 0, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 1:
            delta = {'UP': 0, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 0}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 2:
            delta = {'UP': -2, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 4:
            delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 5:
            delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 0}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 6:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 7:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 8:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 0}
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

        return sum(s != g and s!=0 for (s, g) in zip(node.state, self.goal))

def displayDuck(state):
    '''
    Write a function called display(state) that takes an 8-puzzle state (i.e. 
    a tuple that is a permutation of (0, 1, 2, …, 8)) as input and prints a 
    neat and readable representation of it. 0 is the blank, and should be 
    printed as a * character.
    '''
    
    state = ["*" if i==0 else i for i in state]

    print(state[0], state[1]) 
    print(state[2], state[3], state[4], state[5])
    print(" ", state[6], state[7], state[8])    

def make_rand_duck_puzzle():
    
    initial_state = [1,2,3,4,5,6,7,8,0]
    ep = DuckPuzzle(tuple(initial_state))

    actions = ep.actions(initial_state)
    state = ep.result(initial_state, choice(actions))

    for i in range(2000):
        state = ep.result(state, choice(actions))
        actions = ep.actions(state)

    displayDuck(state)
    return DuckPuzzle(tuple(state))

def run_Eight_n_times(n):
    out = []
    for i in range(0,n):
        print()
        print("Running trial # " + str(i+1))
        out.append(compare_algorithms(i+1))
    res["8Puzzle"] = out

def run_duck_n_times(n):
    out = []
    for i in range(0,n):
        print()
        print("Running trial # " + str(i+1))
        out.append(compare_algorithms_duck(i+1))
    res["duck"] = out


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
    frontier_pop_count = 0
    while frontier:
        node = frontier.pop()
        frontier_pop_count += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, frontier_pop_count
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, frontier_pop_count

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# def create_json():
#     with open("a1.json", "w+") as f:
#         f.write(json.dumps(res, indent=4))
#         f.close()

if __name__ == "__main__":
    run_Eight_n_times(10)
    run_duck_n_times(10)
    # create_json()

