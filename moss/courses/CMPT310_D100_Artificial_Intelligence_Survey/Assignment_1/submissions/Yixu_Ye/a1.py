# a1.py
from search import *
import random
import time

# Q1
'''***************************************************************************************************************'''


def make_rand_8puzzle():
    list_random = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    available = False
    while not available:
        random.shuffle(list_random)
        t = tuple(list_random)
        e = EightPuzzle(t)
        if e.check_solvability(t):
            available = True
    print(t)
    display(tuple(list_random))
    # display_duck_puzzle(tuple(list_random))
    return tuple(list_random)


def display(state):
    list_data = list(state)
    s = ""
    count_next_line = 1
    for num in list_data:
        if num == 0:
            s += "* "
        else:
            s += str(num) + " "
        if count_next_line % 3 == 0:
            s += "\n"
        count_next_line += 1
    print(s)


# Q2

'''***************************************************************************************************************'''
'''count the total number of nodes removed from frontier'''


def best_first_graph_search_removed_count(problem, f, display=False):
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
            # return node
            break
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    # return None
    return count


def astar_search_count(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_removed_count(problem, lambda n: n.path_cost + h(n), display)


# https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game


def manhattan_distance_h(node):
    man_dis = 0
    init_list = list(node.state)
    goal_list = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    for index, number in enumerate(init_list):
        goal_ind = goal_list.index(number)
        # don't compute MD for element 0
        if number != 0:
            man_dis += abs(int(index / 3) - int(goal_ind / 3)) + abs((index % 3) - (goal_ind % 3))
    return man_dis


def max_h(node):
    # must create a new object based on the node
    # to call the h function
    return max(manhattan_distance_h(node), EightPuzzle(node).h(node))


# Q3
'''***************************************************************************************************************'''


class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square <= 1 or 4 <= index_blank_square <= 5:
            possible_actions.remove('UP')
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square % 4 == 1 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square >= 6 or index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    # https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
    # If the grid width is odd, then the number of inversions in a solvable situation is even.
    # If the grid width is even, and the blank is on an even row counting from the bottom
    # (second - last, fourth - last etc), then the number of inversions in a solvable situation is odd.
    # If the grid width is even, and the blank is on an odd row counting from the bottom
    # (last, third - last, fifth - last etc), then the number of inversions in a solvable situation is even.

    def check_solvability(self, state):
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
                Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        if 0 <= blank <= 1:
            delta = {'UP': 3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
            # print("first")
        elif 2 <= blank <= 5:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            # print("second")
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            # print("third")
        neighbor = blank + delta[action]
        # print(neighbor)
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


# we do not change the check_solvility
def make_rand_duck_puzzle():
    # automatically make a solved puzzle, using random move from the goal backward to
    # original to avoid changing the solvaility
    list_goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    list_duck = DuckPuzzle(list_goal)
    for num in range(1500):
        list_action = list_duck.actions(list_goal)
        list_goal = list_duck.result(list_goal, random.choice(list_action))
    return list_goal


def display_duck_puzzle(state):
    list_data = list(state)
    s = ""
    count_next_line = 1
    for num in list_data:
        if num == 0:
            s += "* "
        else:
            s += str(num) + " "

        if count_next_line == 2 or count_next_line == 6 or count_next_line == 9:
            s += "\n"
        if count_next_line == 6:
            s += "  "
        count_next_line += 1
    print(s)


# Manhattan distance

# Definition: The distance between two points measured along axes at right angles.
# In a plane with p1 at (x1, y1) and p2 at (x2, y2), it is |x1 - x2| + |y1 - y2|
def manhattan_distance_h_duck(node):
    man_dis = 0
    init_list = list(node.state)
    # display_duck_puzzle(init_list)
    points_location = [[0, 0], [1, 0],
                       [0, 1], [1, 1], [2, 1], [3, 1],
                       [1, 2], [2, 2], [3, 2]]
    init_points_position = {}
    goal_points_location = {}

    for i in range(9):
        init_points_position[init_list[i]] = points_location[i]
        if i == 8:
            goal_points_location[0] = points_location[8]
            break
        goal_points_location[i + 1] = points_location[i]

    for i in range(1, 9):
        man_dis = abs(init_points_position[i][0] - goal_points_location[i][0]) + \
                  abs(init_points_position[i][1] - goal_points_location[i][1]) + man_dis
    return man_dis


def max_h_duck(node):
    # must create a new object based on the node
    # to call the h function
    return max(manhattan_distance_h_duck(node), DuckPuzzle(node).h(node))


# testing part

'''***************************************************************************************************************'''


def test_eight_puzzle():
    for i in range(20):
        print(f"case {i + 1} *********************************")
        misplaced_state = EightPuzzle(make_rand_8puzzle())
        max_state = misplaced_state
        manhattan_state = misplaced_state
        # print(misplaced_state)
        print("A* search using misplaced")
        start_time = time.time()
        count = astar_search_count(misplaced_state)
        result = astar_search(misplaced_state)
        elapsed_time = round(time.time() - start_time, 4)
        print(f'misplaced elapsed time (in seconds): {elapsed_time}s')
        print(f'The length of solution: {len(result.solution())}')
        print(f'total number of nodes that were removed from frontier: {count}')

        print("A* search using Manhattan ")
        start_time = time.time()
        count = astar_search_count(manhattan_state, h=manhattan_distance_h)
        result = astar_search(manhattan_state, h=manhattan_distance_h)
        elapsed_time = round(time.time() - start_time, 4)
        print(f'Manhattan elapsed time (in seconds): {elapsed_time}s')
        print(f'The length of solution: {len(result.solution())}')
        print(f'total number of nodes that were removed from frontier: {count}')

        print("A* search using max ")
        start_time = time.time()
        count = astar_search_count(max_state, h=max_h)
        result = astar_search(max_state, h=max_h)
        elapsed_time = round(time.time() - start_time, 4)
        print(f'max elapsed time (in seconds): {elapsed_time}s')
        print(f'The length of solution: {len(result.solution())}')
        print(f'total number of nodes that were removed from frontier: {count}')


def test_duck_puzzle():
    for i in range(20):
        print(f"case {i + 1} *********************************")
        misplaced_state = DuckPuzzle(make_rand_duck_puzzle())
        max_state = misplaced_state
        manhattan_state = misplaced_state

        print("A* search using misplaced")
        start_time = time.time()
        count = astar_search_count(misplaced_state)
        result = astar_search(misplaced_state)
        elapsed_time = round(time.time() - start_time, 4)
        print(f'misplaced elapsed time (in seconds): {elapsed_time}s')
        print(f'The length of solution: {len(result.solution())}')
        print(f'total number of nodes that were removed from frontier: {count}')

        print("A* search using Manhattan ")
        start_time = time.time()
        count = astar_search_count(manhattan_state, h=manhattan_distance_h_duck)
        result = astar_search(manhattan_state, h=manhattan_distance_h_duck)
        elapsed_time = round(time.time() - start_time, 4)
        print(f'Manhattan elapsed time (in seconds): {elapsed_time}s')
        print(f'The length of solution: {len(result.solution())}')
        print(f'total number of nodes that were removed from frontier: {count}')

        print("A* search using max ")
        start_time = time.time()
        count = astar_search_count(max_state, h=max_h_duck)
        result = astar_search(max_state, h=max_h_duck)
        elapsed_time = round(time.time() - start_time, 4)
        print(f'max elapsed time (in seconds): {elapsed_time}s')
        print(f'The length of solution: {len(result.solution())}')
        print(f'total number of nodes that were removed from frontier: {count}')


# test the eight puzzle
test_eight_puzzle()
# test the duck puzzle
test_duck_puzzle()
