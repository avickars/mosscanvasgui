# KeBen (Kevin) Chen Su
# 301386066
# a1

from search import *
import time

class EightPuzzle(Problem):

    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 goal, where one of the
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

    def manhattan(self, node):
        "the empty tile '0' is included in the calculation"
        state = node.state
        index_goal = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1], 0: [2, 2]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        x = 0
        y = 0
        for i in range(len(state)):
            index_state[state[i]] = index[i]

        for i in range(9):
            x = abs(index_goal[i][0] - index_state[i][0]) + x
            y = abs(index_goal[i][1] - index_state[i][1]) + y

        return x + y

    def max_heuristics(self, node):
        return max(self.h(node), self.manhattan(node))
# ______________________________________________________________________________________________________________________


def best_first_graph_search(problem, f, display = False):

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
    # added a counter for the number of nodes being pop
    node_count = 0
    while frontier:
        node = frontier.pop()
        node_count = node_count + 1 #update the counter when a node is pop from frontier
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, node.path_cost, node_count]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)

    return None

# ______________________________________________________________________________________________________________________
# Informed (Heuristic) Search


greedy_best_first_graph_search = best_first_graph_search


# Greedy best-first search is accomplished by specifying f(n) = h(n).

def astar_search(problem, h=None, display=True):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def astar_search_manhattan(problem, h=None, display=True):
    """ A*-search using the Max value between Manhattan distance heurisitic and Misplaced tile heuristic"""

    h = memoize(h or problem.manhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def astar_max_heuristic(problem, h=None, display=True):
    """ A*-search using the Manhattan distance heuristic"""

    h = memoize(h or problem.max_heuristics, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
# ______________________________________________________________________________________________________________________


# https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game

def make_rand_8puzzle():

    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(goal)
    new_goal = (goal[0], goal[1], goal[2],
                goal[3], goal[4], goal[5],
                goal[6], goal[7], goal[8])

    state = EightPuzzle(new_goal)

    while not state.check_solvability(state.initial):
        # create a new goal
        goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(goal)
        new_goal = (goal[0], goal[1], goal[2],
                    goal[3], goal[4], goal[5],
                    goal[6], goal[7], goal[8])

        state = EightPuzzle(new_goal)

    return state

def display(state):
    new_display = [0]*9
    for i in range(9):
        new_display[i] = state[i]
        if new_display[i] == 0:
            new_display[i] = '*'
    print(new_display[0], new_display[1], new_display[2])
    print(new_display[3], new_display[4], new_display[5])
    print(new_display[6], new_display[7], new_display[8])
# ______________________________________________________________________________________________________________________________
# DuckPuzzle

class DuckPuzzle(Problem):

    """ The problem of sliding tiles numbered from 1 to 8 on a duck shaped puzzle, where one of the
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
        index_cant_moveup =   (0, 1, 4, 5)
        index_cant_movedown = (2, 6, 7, 8)
        index_cant_moveright = (1, 5, 8)
        index_cant_moveleft =  (0, 2, 6)

        if index_blank_square in index_cant_moveup:
            possible_actions.remove('UP')
        if index_blank_square in index_cant_movedown:
            possible_actions.remove('DOWN')
        if index_blank_square in index_cant_moveright:
            possible_actions.remove('RIGHT')
        if index_blank_square in index_cant_moveleft:
            possible_actions.remove('LEFT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        """0   1
           2   3   4   5
               6   7   8

        there are 2 exceptions for row 1 in the above puzzle, one is going from index 0 to 2 or 2 to 0
        the other exception would be going from 1 to 3 or 3 to 1. Therefore, for row 1 we would have UP:-2 and DOWN: 2
        For row 2, we can only move UP by 2, and there is no restriction for DOWN so we will keep it as DOWN: 3
        For row 3, we have no restriction so we will keep it as UP: -3, DOWN: -3"""

        exception_blanks_row1 = (0, 1)
        exception_blanks_row2 = (2, 3, 4, 5)
        exception_blanks_row3 = (6, 7, 8)
        exception_moves_row1 = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT':1}
        exception_moves_row2 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT':1}
        exception_moves_row3 = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT':1}

        if blank in exception_blanks_row1:
            neighbor = blank + exception_moves_row1[action]
        if blank in exception_blanks_row2:
            neighbor = blank + exception_moves_row2[action]
        if blank in exception_blanks_row3:
            neighbor = blank + exception_moves_row3[action]

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
        "the empty tile '0' is included in the calculation"
        state = node.state
        index_goal = {1: [0, 0], 2: [0, 1],3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2], 0: [2, 3]}
        index_state = {}
        index = [[0, 0], [0, 1],[1, 0], [1, 1], [1, 2], [1, 3],[2, 1], [2, 2], [2, 3]]
        x = 0
        y = 0
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        for i in range(9):
            x = abs(index_goal[i][0] - index_state[i][0]) + x
            y = abs(index_goal[i][1] - index_state[i][1]) + y
        return x + y

    def max_heuristics(self, node):
        return max(self.h(node), self.manhattan(node))
# ________________________________________________________________________________________________________________________________________

def make_rand_duckPuzzle():
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    random_puzzle = goal
    solved_duck_puzzle = DuckPuzzle(goal)

    "Here we will take a goal state and randomize a sequence of actions to make sure the random puzzle is solvable."
    random_range = random.randint(1000, 10000)
    for i in range(random_range):
        actions = solved_duck_puzzle.actions(random_puzzle)
        random_move = random.choice(actions)
        random_puzzle = solved_duck_puzzle.result(random_puzzle, random_move)
    solvable_puzzle = DuckPuzzle(random_puzzle)

    return solvable_puzzle

def displayDuck(state):
    new_display = [0]*9
    for i in range(9):
        new_display[i] = state[i]
        if new_display[i] == 0:
            new_display[i] = '*'
    print(new_display[0], new_display[1])
    print(new_display[2], new_display[3], new_display[4], new_display[5])
    print(" ",            new_display[6], new_display[7], new_display[8])
    
#  _________________________________________________________________________________________________________________________________________________

# Timers:

def astar_timer(state):
    tic = time.time()
    results = astar_search(state)
    toc = time.time()
    elapse_time = toc - tic
    print(f"The elapsed time (in seconds): {elapse_time}'s")
    print("The length of the solution: ", results[1])
    print("The total number of nodes removed from frontier: ", results[2])


def astar_manhattan_timer(state):
    tic = time.time()
    results = astar_search_manhattan(state)
    toc = time.time()
    elapse_time = toc - tic
    print(f"The elapsed time (in seconds): {elapse_time}'s")
    print("The length of the solution: ", results[1])
    print("The total number of nodes removed from frontier: ", results[2])


def astar_max_heuristic_timer(state):
    tic = time.time()
    results = astar_max_heuristic(state)
    toc = time.time()
    elapse_time = toc - tic
    print(f"The elapsed time (in seconds): {elapse_time}'s")
    print("The length of the solution: ", results[1])
    print("The total number of nodes removed from frontier: ", results[2])

# ______________________________________________________________________________________________________________________________

# "8 Puzzle analysis"

print("_________________________________________EIGHT PUZZLE________________________________________________________")
for i in range(10):
    puzzle = make_rand_8puzzle()
    display(puzzle.initial)
    print("Test:", i, " A*-search using the misplaced title heuristics")
    astar_timer(puzzle)
    print('\n')
    print("Test:", i, " A*-search using the Manhattan Distance heuristics")
    astar_manhattan_timer(puzzle)
    print('\n')
    print("Test:", i, " A*-search using the max misplaced and Manhattan heuristics")
    astar_max_heuristic_timer(puzzle)
    print('\n')
print("______________________________________________END_____________________________________________________________")
print('\n')

# "Duck Puzzle analysis"

print("__________________________________________ DUCK PUZZLE________________________________________________________")
for i in range(10):
    duck_puzzle = make_rand_duckPuzzle()
    displayDuck(duck_puzzle.initial)
    print("Test:", i, " A*-search using the misplaced title heuristics")
    astar_timer(duck_puzzle)
    print('\n')
    print("Test:", i, " A*-search using the Manhattan Distance heuristics")
    astar_manhattan_timer(duck_puzzle)
    print('\n')
    print("Test:", i, " A*-search using the max misplaced and Manhattan heuristics")
    astar_max_heuristic_timer(duck_puzzle)
    print('\n')
print("______________________________________________END_____________________________________________________________")
  

   


















