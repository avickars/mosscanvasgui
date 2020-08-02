from search import *
import random
import time

# Q1
def make_rand_8puzzle():

    state = [i for i in range(9)]
    random.shuffle(state)
    rand_8puzzle = EightPuzzle(tuple(state))

    while (rand_8puzzle.check_solvability(state) == False):
        random.shuffle(state)
        rand_8puzzle = EightPuzzle(tuple(state))

    return rand_8puzzle


def display(state):
    s = [-1] * 9
    for i in range(0, 9):
        if state[i] == 0:
            s[i] = '*'
        else:
            s[i] = state[i]

    print(s[0], s[1], s[2])
    print(s[3], s[4], s[5])
    print(s[6], s[7], s[8])


# rand_puzzle = make_rand_8puzzle()
# display(rand_puzzle.initial)

def manhattan(node):
    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0
    for i in range(1, 9):
        for j in range(2):
            mhd += abs(index_goal[i][j] - index_state[i][j])

    return mhd


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def best_first_graph_search(problem, f, display=False):
    print("best_first_graph_search")

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
    remove = 0
    while frontier:
        node = frontier.pop()
        remove += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, remove
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, None


# Q2
def max_h_manhattan(node):
    puzzle = EightPuzzle(node.state)
    return max(manhattan(node), puzzle.h(node))


def test_10_8puzzle():
    time1 = []
    moves1 = []
    removes1 = []
    time2 = []
    moves2 = []
    removes2 = []
    time3 = []
    moves3 = []
    removes3 = []

    num_test = 10
    for i in range(num_test):
        rand_puzzle = make_rand_8puzzle()
        display(rand_puzzle.initial)

        print("A* misplaced tile heuristic:")
        start_time = time.time()
        ret, num_moves = astar_search(rand_puzzle)
        elapsed_time = time.time() - start_time
        time1.append(elapsed_time)
        removes1.append(num_moves)
        moves1.append(len(ret.solution()))
        print(time1)
        print(moves1)
        print(removes1)
        print()

        display(rand_puzzle.initial)
        print("A* manhattan heuristic:")
        start_time = time.time()
        ret, num_moves = astar_search(rand_puzzle, h=manhattan)
        elapsed_time = time.time() - start_time
        time2.append(elapsed_time)
        removes2.append(num_moves)
        moves2.append(len(ret.solution()))
        print(time2)
        print(moves2)
        print(removes2)
        print()

        display(rand_puzzle.initial)
        print("A* max of misplaced tile heuristic and manhattan heuristic:")
        start_time = time.time()
        ret, num_moves = astar_search(rand_puzzle, h=max_h_manhattan)
        elapsed_time = time.time() - start_time
        time3.append(elapsed_time)
        removes3.append(num_moves)
        moves3.append(len(ret.solution()))
        print(time3)
        print(moves3)
        print(removes3)
        print()
        print()



# Q3
def manhattan_duck(node):
    state = node.state
    index_goal = {1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2], 0: [2, 3]}
    index_state = {}
    index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    for i in range(1, 9):
        for j in range(2):
            mhd += abs(index_goal[i][j] - index_state[i][j])

    return mhd

def max_h_manhattan_duck(node):
    puzzle = DuckPuzzle(node.state)
    return max(manhattan_duck(node), puzzle.h(node))


class DuckPuzzle(Problem):

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

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square >= 6:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank <= 1:
            delta = {'UP': -10, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank <= 5:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 10, 'LEFT': -1, 'RIGHT': 1}


        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))



def make_rand_duck_puzzle():
    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # default states
    rand_puzzle = DuckPuzzle(tuple(state))
    for i in range(1000000):
        action = random.choice(rand_puzzle.actions(state))
        state = rand_puzzle.result(state, action)
        rand_puzzle = DuckPuzzle(state)

    return rand_puzzle


def display_Duck(state):
    s = [-1] * 9
    for i in range(0, 9):
        if state[i] == 0:
            s[i] = '*'
        else:
            s[i] = state[i]

    print(s[0], s[1])
    print(s[2], s[3], s[4], s[5])
    print(" ", s[6], s[7], s[8])


def test_10_duck_puzzle():
    time1 = []
    moves1 = []
    removes1 = []
    time2 = []
    moves2 = []
    removes2 = []
    time3 = []
    moves3 = []
    removes3 = []

    num_test = 10
    for i in range(num_test):
        rand_puzzle = make_rand_duck_puzzle()

        display_Duck(rand_puzzle.initial)
        print("A* misplaced tile heuristic:")
        start_time = time.time()
        ret, num_moves = astar_search(rand_puzzle)
        elapsed_time = time.time() - start_time
        time1.append(elapsed_time)
        removes1.append(num_moves)
        moves1.append(len(ret.solution()))
        print(time1)
        print(moves1)
        print(removes1)
        print()

        display_Duck(rand_puzzle.initial)
        print("A* manhattan heuristic:")
        start_time = time.time()
        ret, num_moves = astar_search(rand_puzzle, h=manhattan_duck)
        elapsed_time = time.time() - start_time
        time2.append(elapsed_time)
        removes2.append(num_moves)
        moves2.append(len(ret.solution()))
        print(time2)
        print(moves2)
        print(removes2)
        print()

        display_Duck(rand_puzzle.initial)
        print("A* max of misplaced tile heuristic and manhattan heuristic:")
        start_time = time.time()
        ret, num_moves = astar_search(rand_puzzle, h=max_h_manhattan_duck)
        elapsed_time = time.time() - start_time
        time3.append(elapsed_time)
        removes3.append(num_moves)
        moves3.append(len(ret.solution()))
        print(time3)
        print(moves3)
        print(removes3)
        print()
        print()


test_10_8puzzle()
test_10_duck_puzzle()