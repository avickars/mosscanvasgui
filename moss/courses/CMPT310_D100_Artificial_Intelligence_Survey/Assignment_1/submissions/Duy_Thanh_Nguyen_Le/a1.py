# a1.py

# https://github.com/aimacode/aima-python

from search import *
import time


# ===================== Question 1: Helper Functions =====================

def make_rand_8puzzle():
    problem=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    eight_puzzle=EightPuzzle_modified(problem)

    num_of_shuffles=random.randint(50, 100)
    for _ in range(num_of_shuffles):
        list_of_actions=(eight_puzzle.actions(problem))
        problem=eight_puzzle.result(problem, random.choice(list_of_actions))

    while not eight_puzzle.check_solvability(problem):
        list_of_actions=(eight_puzzle.actions(problem))
        problem=eight_puzzle.result(problem, random.choice(list_of_actions))

    return EightPuzzle_modified(problem)


def display(state):
    for x in state:
        index=state.index(x) + 1
        if (x == 0):
            x="*"
        if (index % 3 == 0):
            print(x)
        else:
            print(x, "", end="")


# ===================== Question 2: Comparing Algorithms =====================

# modified best_first_graph_search in search.py
def best_first_graph_search_modified(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f=memoize(f, 'f')
    node=Node(problem.initial)
    frontier=PriorityQueue('min', f)
    frontier.append(node)
    explored=set()

    nodesRemoved=0

    while frontier:
        node=frontier.pop()
        nodesRemoved += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and",
                      len(frontier), "paths remain in the frontier")
            return [node, nodesRemoved]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def astar_search_misplaced_tile(problem, h=None, display=False):
    h=memoize(h or problem.h, 'h')
    return best_first_graph_search_modified(problem, lambda n: n.path_cost + h(n), display)


def astar_search_manhattan_distance(problem, h=None, display=False):
    h=memoize(h or problem.mdh, 'mdh')
    return best_first_graph_search_modified(problem, lambda n: n.path_cost + h(n), display)


def astar_search_max(problem, h=None, display=False):
    h=memoize(h or problem.h, 'max_h')
    return best_first_graph_search_modified(problem, lambda n: n.path_cost + h(n), display)


# modified EightPuzzle in search.py
class EightPuzzle_modified(Problem):
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

        possible_actions=['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square=self.find_blank_square(state)

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
        blank=self.find_blank_square(state)
        new_state=list(state)

        delta={'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor=blank + delta[action]
        new_state[blank], new_state[neighbor]=new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion=0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    # modified manhattan in tests/test_search.py
    def mdh(self, node):
        state = node.state
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2],
                      4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]

        distance = 0

        for i in range(9):
            distance = abs(index_goal[i][0] - index_state[i][0]) + \
                      abs(index_goal[i][1] - index_state[i][1]) + distance

        return distance

    def max_h(self, node):
        return max(self.h(node), self.mdh(node))


def compare_8puzzle_algos():
    num_of_tests = 10

    print("\n\n@@@@@@@@   EIGHT PUZZLE   @@@@@@@@")

    for curr_test_num in range(num_of_tests):
        eight_puzzle=make_rand_8puzzle()

        print("\n\n########   TEST #", curr_test_num + 1, "   ########")
        display(make_rand_8puzzle().initial)

        print("\n\n====== A*-search using the misplaced tile heuristic ======")
        start_time=time.time()
        res=astar_search_misplaced_tile(eight_puzzle)
        end_time=time.time()
        print("Total running time in seconds            : ", end_time - start_time)
        print("Length of the solution                   : ", len(res[0].solution()))
        print("Total # of nodes removed from frontier   : ", res[1])

        print("\n====== A*-search using the Manhattan distance heuristic ======")
        start_time=time.time()
        res=astar_search_manhattan_distance(eight_puzzle)
        end_time=time.time()
        print("Total running time in seconds            : ", end_time - start_time)
        print("Length of the solution                   : ", len(res[0].solution()))
        print("Total # of nodes removed from frontier   : ", res[1])

        print("\n====== A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic ======")
        start_time=time.time()
        res=astar_search_max(eight_puzzle)
        end_time=time.time()
        print("Total running time in seconds            : ", end_time - start_time)
        print("Length of the solution                   : ", len(res[0].solution()))
        print("Total # of nodes removed from frontier   : ", res[1])


# ===================== Question 3: The House-Puzzle =====================
# modified EightPuzzle in search.py
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

        """
        Goal State:
            1 2
            3 4 5 6
              7 8 *

            0:[0,0],    1:[0,1]
            2:[1,0],    3:[1,1],    4:[1,2],    5:[1,3]
                        6:[2,1],    7:[2,2],    8:[2,3]

        Conditions:
            Up action invalid:
                0:[0,0]
                1:[0,1]
                4:[1,2]
                5:[1,3]
            Down action invalid:
                2:[1,0]
                6:[2,1]
                7:[2,2]
                8:[2,3]
            Left action invalid:
                0:[0,0]
                2:[1,0]
                6:[2,1]
            Right action invalid:
                1:[0,1]
                5:[1,3]
                8:[2,3]
        """

        invalid_up_index = [0, 1, 4, 5]
        invalid_down_index = [2, 6, 7, 8]
        invalid_left_index = [0, 2, 6]
        invalid_right_index = [1, 5, 8]

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square in invalid_left_index:
            possible_actions.remove('LEFT')
        if index_blank_square in invalid_up_index:
            possible_actions.remove('UP')
        if index_blank_square in invalid_right_index:
            possible_actions.remove('RIGHT')
        if index_blank_square in invalid_down_index:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        """
        Goal State:
            1 2 3
            4 5 6
            7 8 *

            (1, 2, 3, 4, 5, 6, 7, 8, 0)
             0  1  2  3  4  5  6  7  8   <= index

            Move UP:
                (1, 2, 3, 4, 5, 6, 7, 8, 0) -> (1, 2, 3, 4, 5, 0, 7, 8, 6)
                 0  1  2  3  4  5  6  7  8      0  1  2  3  4  5  6  7  8

                0:(index 8) -> 0:(index 5)

                moving up is a diff of -3
        """

        """
        Goal State:
            1 2
            3 4 5 6
              7 8 *

            (1, 2, 3, 4, 5, 6, 7, 8, 0)

        """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta1 = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        delta2 = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        abnormalIndex = (0, 2, 1, 3)

        if blank in abnormalIndex:
            neighbor = blank + delta1[action]
        else:
            neighbor = blank + delta2[action]

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

    # modified manhattan in tests/test_search.py
    def mdh(self, node):
        state = node.state
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2],
                      4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]

        distance = 0

        for i in range(9):
            distance = abs(index_goal[i][0] - index_state[i][0]) + \
                      abs(index_goal[i][1] - index_state[i][1]) + distance

        return distance

    def max_h(self, node):
        return max(self.h(node), self.mdh(node))


def make_rand_duck_puzzle():
    problem=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    duck_puzzle=DuckPuzzle(problem)

    num_of_shuffles=random.randint(50, 100)
    for _ in range(num_of_shuffles):
        list_of_actions=(duck_puzzle.actions(problem))
        problem=duck_puzzle.result(problem, random.choice(list_of_actions))

    return DuckPuzzle((problem))


def display_duck_puzzle(state):
    """
    Goal State:
        1 2
        3 4 5 6
          7 8 *
    """

    for x in state:
        index=state.index(x)
        if (x == 0):
            x="*"
        if (index == 1):
            print(x, "", "")
        elif (index == 5):
            print(x)
        elif (index == 6):
            print(" ", x, end=" ")
        else:
            print(x, "", end="")


def compare_duck_puzzle_algos():
    num_of_tests = 10

    print("\n\n@@@@@@@@   DUCK PUZZLE   @@@@@@@@")

    for curr_test_num in range(num_of_tests):
        duck_puzzle=make_rand_duck_puzzle()

        print("\n\n########   TEST #", curr_test_num + 1, "   ########")
        display_duck_puzzle(make_rand_duck_puzzle().initial)

        print("\n\n====== A*-search using the misplaced tile heuristic ======")
        start_time=time.time()
        res=astar_search_misplaced_tile(duck_puzzle)
        end_time=time.time()
        print("Total running time in seconds            : ", end_time - start_time)
        print("Length of the solution                   : ", len(res[0].solution()))
        print("Total # of nodes removed from frontier   : ", res[1])

        print("\n====== A*-search using the Manhattan distance heuristic ======")
        start_time=time.time()
        res=astar_search_manhattan_distance(duck_puzzle)
        end_time=time.time()
        print("Total running time in seconds            : ", end_time - start_time)
        print("Length of the solution                   : ", len(res[0].solution()))
        print("Total # of nodes removed from frontier   : ", res[1])

        print("\n====== A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic ======")
        start_time=time.time()
        res=astar_search_max(duck_puzzle)
        end_time=time.time()
        print("Total running time in seconds            : ", end_time - start_time)
        print("Length of the solution                   : ", len(res[0].solution()))
        print("Total # of nodes removed from frontier   : ", res[1])

# ===================== Function Calls =====================


# display(make_rand_8puzzle().initial)
compare_8puzzle_algos()


# display_duck_puzzle(make_rand_duck_puzzle().initial)
compare_duck_puzzle_algos()