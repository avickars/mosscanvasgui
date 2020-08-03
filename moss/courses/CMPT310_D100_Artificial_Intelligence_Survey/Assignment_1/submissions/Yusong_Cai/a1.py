
#// - new_astar_search function and new_best_first_graph_search is from the search file
#//
#// - got some hints for solvability function from my TA Mahmoud

# I believe that my other function can work for house puzzle and solvability function still has bug...

from search import *
import random
import time


class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """

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

        return sum(s != 0 and s != g for (s, g) in zip(node.state, self.goal))

# _____________________________ _________________________________________________

class housePuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, -1, -1, 3, 4, 5, 6, -1, 7, 8, 0)):
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

        if index_blank_square in [0, 4, 9]:
            possible_actions.remove('LEFT')
        if index_blank_square in [1, 7, 11]:
            possible_actions.remove('RIGHT')
        if index_blank_square in [0, 1, 6, 7]:
            possible_actions.remove('UP')
        if index_blank_square in [4, 9, 10, 11]:
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

        if state[0] == 0:
            if state[1] == 2 and state[4] == 1:
                for i in range(5, 12):
                    for j in range(i + 1, 12):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                return inversion % 2 == 0

        elif state[0] == 0:
            if state[1] == 3 and state[4] == 2:
                for i in range(5, 12):
                    for j in range(i + 1, 12):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                return inversion % 2 == 0

        elif state[0] == 0:
            if state[1] == 1 and state[4] == 3:
                for i in range(5, 12):
                    for j in range(i + 1, 12):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                return inversion % 2 == 0

        elif state[0] == 1:
            if state[1] == 2 and state[4] == 3:
                for i in range(5, 12):
                    for j in range(i + 1, 12):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                return inversion % 2 == 0

        elif state[0] == 1:
            if state[1] == 2 and state[4] == 0:
                for i in range(5, 12):
                    for j in range(i + 1, 12):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                return inversion % 2 == 0

        elif state[0] == 1:
            if state[1] == 0 and state[4] == 3:
                for i in range(5, 12):
                    for j in range(i + 1, 12):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                return inversion % 2 == 0

        elif state[0] == 2:
            if state[1] == 0 and state[4] == 1:
                for i in range(5, 12):
                    for j in range(i + 1, 12):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                return inversion % 2 == 0

        elif state[0] == 2:
            if state[1] == 3 and state[4] == 1:
                for i in range(5, 12):
                    for j in range(i + 1, 12):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                return inversion % 2 == 0

        elif state[0] == 2:
            if state[1] == 3 and state[4] == 0:
                for i in range(5, 12):
                    for j in range(i + 1, 12):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                return inversion % 2 == 0

        elif state[0] == 3:
            if state[1] == 0 and state[4] == 2:
                for i in range(5, 12):
                    for j in range(i + 1, 12):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                return inversion % 2 == 0

        elif state[0] == 3:
            if state[1] == 1 and state[4] == 2:
                for i in range(5, 12):
                    for j in range(i + 1, 12):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                return inversion % 2 == 0

        else:
            if state[1] == 1 and state[4] == 0 and state[0] == 3:
                for i in range(5, 12):
                    for j in range(i + 1, 12):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
                return inversion % 2 == 0


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != 0 and s != g for (s, g) in zip(node.state, self.goal))
# ______________________________________________________________________________


def manhatt_house(node):

    index_arr = {}
    state = node.state
    g_index = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
    index = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3]]

    for m in range(len(state)):
        if state[m] == -1:
            m = m + 1
        else:
            index_arr[state[m]] = index[m]

    manhantt_dis = 0

    for m in range(8):
        for n in range(2):
            manhantt_dis += abs(g_index[m+1][n] - index_arr[m+1][n])

    return manhantt_dis

def manhatt_Eight(node):

    index_arr = {}
    state = node.state
    g_index = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    for m in range(len(state)):
        index_arr[state[m]] = index[m]

    manhantt_dis = 0

    for m in range(8):
        for n in range(2):
            manhantt_dis += abs(g_index[m+1][n] - index_arr[m+1][n])

    return manhantt_dis

def max_method(node):
    e_puzzle = EightPuzzle(node.state)
    return max(manhatt_Eight(node), e_puzzle.h(node))

def max_housePuzzle(node):
    h_puzzle = housePuzzle(node.state)
    return max(manhatt_house(node), h_puzzle.h(node))


def make_rand_8puzzle():
    arr = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    Eight_puzzle = EightPuzzle(tuple(arr))
    while True:
        random.shuffle(arr)
        if Eight_puzzle.check_solvability(tuple(arr)):
            Eight_puzzle.initial = tuple(arr)
            return Eight_puzzle
        else:
            continue

def make_rand_housePuzzle():
    while True:
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        h_puzzle = housePuzzle(tuple(arr))
        random.shuffle(arr)
        arr.insert(2, -1)
        arr.insert(3, -1)
        arr.insert(8, -1)
        if h_puzzle.check_solvability(tuple(arr)):
            h_puzzle.initial = tuple(arr)
            return h_puzzle


def display_8(object):
    for index, item in enumerate(object.initial, start=1):
        if item == 0: item = '*'
        print(item, end=' ' if index % 3 else '\n')

def display_H(object):
    for index, item in enumerate(object.initial, start=1):
        if item == 0: item = '*'
        if item == -1: item = ' '
        print(item, end=' ' if index % 4 else '\n')


def new_astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return new_best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def new_best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    ctr = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        ctr+=1
        if problem.goal_test(node.state):
            return node, ctr
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def eightPuzzle_compare():

    for i in range(10):
        puzzle = make_rand_8puzzle()

        print(puzzle.initial)
        print()

        display_8(puzzle)
        print()


        start_time1 = time.time()
        result1 = new_astar_search(puzzle, puzzle.h)
        elapsed_time1 = time.time() - start_time1

        start_time2 = time.time()
        result2 = new_astar_search(puzzle, h=manhatt_Eight)
        elapsed_time2 = time.time() - start_time2

        start_time3 = time.time()
        result3= new_astar_search(puzzle, h=max_method)
        elapsed_time3 = time.time() - start_time3


        len1 = result1[0].path_cost
        len2 = result2[0].path_cost
        len3 = result3[0].path_cost


        node_num1 = result1[1]
        node_num2 = result2[1]
        node_num3 = result3[1]


        print("The total running time by using misplaced tile heuristic in seconds: ", elapsed_time1)
        print("The length of the solution by using misplaced tile heuristic method: ", len1)
        print("The total number of removed nodes by using misplaced tile heuristic method:", node_num1)
        print()

        print("The total running time by using the Manhattan distance heuristicin in seconds: ", elapsed_time2)
        print("The length of the solution by using the Manhattan distance heuristic method: ", len2)
        print("The total number of removed nodes by using the Manhattan distance heuristic method: ", node_num2)
        print()

        print("The total running time by using the max value method in seconds: ", elapsed_time3)
        print("The length of the solution by using the max value method: ", len3)
        print("The total number of removed nodes by using the max value method: ", node_num3)




def housePuzzle_compare():

    for i in range(2):
        Hpuzzle = make_rand_housePuzzle()

        print(Hpuzzle.initial)
        print()

        display_H(Hpuzzle)
        print()


        start_time4 = time.time()
        result4 = new_astar_search(Hpuzzle)
        elapsed_time4 = time.time() - start_time4

        start_time5 = time.time()
        result5 = new_astar_search(Hpuzzle, h=manhatt_house)
        elapsed_time5 = time.time() - start_time5

        start_time6 = time.time()
        result6 = new_astar_search(Hpuzzle, h=max_housePuzzle)
        elapsed_time6 = time.time() - start_time6

        len4 = result4[0].path_cost
        len5 = result5[0].path_cost
        len6 = result6[0].path_cost

        num_of_pops_4 = result4[1]
        num_of_pops_5 = result5[1]
        num_of_pops_6 = result6[1]


        print("The total running time by using misplaced tile heuristic in seconds: ", elapsed_time4)
        print("The length of the solution by using misplaced tile heuristic method: ", len4)
        print("The total number of removed nodes by using misplaced tile heuristic method: ", num_of_pops_4)
        print()

        print("The total running time by using the Manhattan distance heuristicin in seconds: ", elapsed_time5)
        print("The length of the solution by using the Manhattan distance heuristic method: ", len5)
        print("The total number of removed nodes by using the Manhattan distance heuristic method: ", num_of_pops_5)
        print()

        print("The total running time by using the max value method in seconds: ", elapsed_time6)
        print("The length of the solution by using the max value method: ", len6)
        print("The total number of removed nodes by using the max value method: ", num_of_pops_6)


eightPuzzle_compare()
#housePuzzle_compare()


