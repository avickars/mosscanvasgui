# a1.py

from search import *
import random
import time

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
    
    def h2(self, node):
        """ Return the heuristic value for a given state."""

        # Manhattan Heuristic Function
        xgoal = 0
        ygoal = 0
        heuristic = 0
        mystate = node.state
        for i, val in enumerate(mystate):
            xval = abs(i%3)
            yval = abs(i//3)
            if val == 1:
                xgoal += abs(xval)
                ygoal += abs(yval)
            if val == 2:
                xgoal += abs(xval - 1)
                ygoal += abs(yval)
            if val == 3:
                xgoal += abs(xval - 2)
                ygoal += abs(yval)
            if val == 4:
                xgoal += abs(xval)
                ygoal += abs(yval - 1)
            if val == 5:
                xgoal += abs(xval - 1)
                ygoal += abs(yval - 1)
            if val == 6:
                xgoal += abs(xval - 2)
                ygoal += abs(yval - 1)
            if val == 7:
                xgoal += abs(xval)
                ygoal += abs(yval - 2)
            if val == 8:
                xgoal += abs(xval - 1)
                ygoal += abs(yval - 2)
            # we add 0 in our manhattan distance because the misplaced tile heuristic has a value for 0
            if val == 0:
                xgoal += abs(xval - 2)
                ygoal += abs(yval - 2)

            heuristic = xgoal + ygoal

        return heuristic

    def h3 (self, node):
        # returns the max of the manhattan distance and misplaced tile heuristics

        return max(self.h(node), self.h2(node))

class DuckPuzzle(Problem):
    # The problem of the classic Eight Puzzle but the board is skewed into the shape of a duck

    def __init__(self, initial, goal=(1, 2, 10, 10, 3, 4, 5, 6, 10, 7, 8, 0)):
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

        # removes LEFT if blank square is on the very left or if there is a out of bounds to the left
        # out of bounds is indicated by the value 10
        if index_blank_square % 4 == 0 or index_blank_square == 9:
            possible_actions.remove('LEFT')
        # removes UP if blank square is at the very top or if there is an out of bounds above
        if index_blank_square < 3 or index_blank_square == 6 or index_blank_square == 7:
            possible_actions.remove('UP')
        # removes RIGHT if blank square is on the very right or if there is an out of bounds to the right
        if index_blank_square % 4 == 3 or index_blank_square == 1:
            possible_actions.remove('RIGHT')
        # removes DOWN if the blank square is at the very bottom or if there is an out of bounds to the right
        if index_blank_square > 7 or index_blank_square == 4:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
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
    
    def h2(self, node):
        """ Return the heuristic value for a given state."""

        # Manhattan Heuristic Function
        xgoal = 0
        ygoal = 0
        heuristic = 0
        mystate = node.state
        # goes through the tuple and for each index it takes the absolute value of the difference
        # between where the value currently is and where it should be
        for i, val in enumerate(mystate):
            xval = abs(i%3)
            yval = abs(i//3)
            if val == 1:
                xgoal += abs(xval)
                ygoal += abs(yval)
            if val == 2:
                xgoal += abs(xval - 1)
                ygoal += abs(yval)
            if val == 3:
                xgoal += abs(xval)
                ygoal += abs(yval - 1)
            if val == 4:
                xgoal += abs(xval - 1)
                ygoal += abs(yval - 1)
            if val == 5:
                xgoal += abs(xval - 2)
                ygoal += abs(yval - 1)
            if val == 6:
                xgoal += abs(xval - 3)
                ygoal += abs(yval - 1)
            if val == 7:
                xgoal += abs(xval - 1)
                ygoal += abs(yval - 2)
            if val == 8:
                xgoal += abs(xval - 2)
                ygoal += abs(yval - 2)
            if val == 0:
                xgoal += abs(xval - 3)
                ygoal += abs(yval - 2)

            heuristic = xgoal + ygoal

        return heuristic

    def h3 (self, node):
        # returns the max of the manhattan distance and misplaced tile heuristics

        return max(self.h(node), self.h2(node))

def make_rand_8puzzle():
    # takes a solved puzzle and makes random amount of randomized moves
    array = ( 1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = EightPuzzle(array)

    shufflecount = random.randint(10,60)
    count = 0

    while count < shufflecount:
        action = puzzle.actions(array)
        random_action = random.randint(0,len(action) - 1)
        array = puzzle.result(array, action[random_action])
        count += 1
    display(array)
    return EightPuzzle(array)

def make_rand_duckpuzzle():
    array = (1, 2, 10, 10, 3, 4, 5, 6, 10, 7, 8, 0)
    puzzle = DuckPuzzle(array)

    shufflecount = random.randint(10,30)
    count = 0

    while count < shufflecount:
        action = puzzle.actions(array)
        random_action = random.randint(0,len(action) - 1)
        array = puzzle.result(array, action[random_action])
        count += 1
    duckdisplay(array)
    return DuckPuzzle(array)


def display(state):
    displaystate = list(state)

    for i, val in enumerate(state):
        if val == 0:
            displaystate[i] = "*"
        else:
            displaystate[i] = str(state[i])

   
    line1 = (str(displaystate[0]) + " " + str(displaystate[1]) + " " + str(displaystate[2]))
    line2 = (str(displaystate[3]) + " " + str(displaystate[4]) + " " + str(displaystate[5]))
    line3 = (str(displaystate[6]) + " " + str(displaystate[7]) + " " + str(displaystate[8]))
 
    print(line1)
    print(line2)
    print(line3)

def duckdisplay(state):
    displaystate = list(state)

    for i, val in enumerate(state):
        if val == 0:
            displaystate[i] = "*"
        elif val == 10:
            displaystate[i] = " "
        else:
            displaystate[i] = str(state[i])

   
    line1 = (str(displaystate[0]) + " " + str(displaystate[1]) + " " + str(displaystate[2]) + " " + str(displaystate[3]))
    line2 = (str(displaystate[4]) + " " + str(displaystate[5]) + " " + str(displaystate[6]) + " " + str(displaystate[7]))
    line3 = (str(displaystate[8]) + " " + str(displaystate[9]) + " " + str(displaystate[10]) + " " + str(displaystate[11]))
 
    print(line1)
    print(line2)
    print(line3)

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    removedfront = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        removedfront += 1
        if problem.goal_test(node.state):
            print(str(node.path_cost) + " number of tiles moved")
            print(str(removedfront) + " number of nodes removed from frontier")
            print(node)
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
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
    start_time = time.time()

    h = memoize(h or problem.h, 'h')
    bfgs = best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')

    return bfgs

print("EightPuzzle")
puzzle1 = make_rand_8puzzle()
astar_search(puzzle1, puzzle1.h)
print(" ")
astar_search(puzzle1, puzzle1.h2)
print(" ")
astar_search(puzzle1, puzzle1.h3)
print(" ")

print("DuckPuzzle")
puzzle2 = make_rand_duckpuzzle()
astar_search(puzzle1, puzzle1.h)
print(" ")
astar_search(puzzle1, puzzle1.h2)
print(" ")
astar_search(puzzle1, puzzle1.h3)

# ...