# a1.py
from search import *
import random
import time


# Question1
def make_rand_8puzzle():
    """ return a solvable EightPuzzle object"""
    # create a list and shuffle it
    l = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(l)
    result = EightPuzzle(tuple(l))
    # shuffle the list until result is solvable
    while not result.check_solvability(tuple(l)):
        random.shuffle(l)
        result = EightPuzzle(tuple(l))
    return result


def display(state):
    """ print the state in a 3x3 matrix, replace 0 with '#' """
    for i in range(0, 9):
        if i % 3 == 2:
            print(state[i] if state[i] != 0 else '#')
        else:
            print(state[i] if state[i] != 0 else '#', " ", end="")


# *******************************************

# Question2
# read https://github.com/aimacode/aima-python/blob/master/search.ipynb
# for help with the original manhattan function, max_heuristic function and implementation of astar_search

def best_first_graph_search_modified(problem, f, display=False):
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
    pops = 0
    while frontier:
        node = frontier.pop()
        # count the number of nodes being popped
        pops = pops + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            # return both result and number of pops
            return node, pops
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, pops


def astar_search_modified(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_modified(problem, lambda n: n.path_cost + h(n), display)


def manhattan_eight(node):
    # The right way to calculate manhattan distance http://ai.stanford.edu/~latombe/cs121/2011/slides/D-heuristic-search.pdf
    """ the original version of manhattain function is wrong
    because it takes consider the empty tile (zero)
    to correct this issue, in this version we take consider elements in range [1,8]"""
    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    for j in range(1, 9):
        mhd = abs(index_goal[j][0] - index_state[j][0]) + abs(index_goal[j][1] - index_state[j][1]) + mhd

    return mhd


def max_heuristic_eight(node):
    """score1=result of Manhattan distance heuristic
     score2=result of misplaced tile heuristic"""
    score1 = manhattan_eight(node)
    tempPuzzle = EightPuzzle(node.state)
    score2 = tempPuzzle.h(node)
    return max(score1, score2)


def compare_algorithms_eight():
    puzzle = make_rand_8puzzle()
    display(puzzle.initial)

    print("A*-search using the misplaced tile heuristic")
    start_time = time.time()
    result, pops = astar_search_modified(puzzle)
    end_time = time.time()
    misplaced_solution = result.solution()
    elapsed_time = end_time - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("the length of the solution = ", len(misplaced_solution))
    print("that total number of nodes that were removed = ", pops)

    print("A*-search using the Manhattan distance heuristic")
    start_time = time.time()
    result, pops = astar_search_modified(puzzle, manhattan_eight)
    end_time = time.time()
    manhattan_solution = result.solution()
    elapsed_time = end_time - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("the length of the solution = ", len(manhattan_solution))
    print("that total number of nodes that were removed = ", pops)

    print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic")
    start_time = time.time()
    result, pops = astar_search_modified(puzzle, max_heuristic_eight)
    end_time = time.time()
    both_solution = result.solution()
    elapsed_time = end_time - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("the length of the solution = ", len(both_solution))
    print("that total number of nodes that were removed = ", pops)

    print("**************************************************************")


### Question 3

def displayDuck(state):
    """ print the state in a 3x3 matrix, replace 0 with '#' """
    for i in range(0, 9):
        if i == 0:
            print(state[i] if state[i] != 0 else '#', " ", end="")
        elif i == 1:
            print(state[i] if state[i] != 0 else '#')
        elif i in [2, 3, 4]:
            print(state[i] if state[i] != 0 else '#', " ", end="")
        elif i == 5:
            print(state[i] if state[i] != 0 else '#')
        elif i == 6:
            print("  ", state[i] if state[i] != 0 else '#', " ", end="")
        elif i == 7:
            print(state[i] if state[i] != 0 else '#', " ", end="")
        else:
            print(state[i] if state[i] != 0 else '#')

def manhattan_duck(node):
    # The right way to calculate manhattan distance http://ai.stanford.edu/~latombe/cs121/2011/slides/D-heuristic-search.pdf
    """ the original version of manhattain function is wrong
    because it takes consider the empty tile (zero)
    to correct this issue, in this version we take consider elements in range [1,8]"""
    state = node.state
    index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
    index_state = {}
    index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    for j in range(1, 9):
        mhd = abs(index_goal[j][0] - index_state[j][0]) + abs(index_goal[j][1] - index_state[j][1]) + mhd

    return mhd


def max_heuristic_duck(node):
    """score1=result of Manhattan distance heuristic
     score2=result of misplaced tile heuristic"""
    score1 = manhattan_duck(node)
    tempPuzzle = DuckPuzzle(node.state)
    score2 = tempPuzzle.h(node)
    return max(score1, score2)


class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        elif index_blank_square == 1:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        elif index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif index_blank_square == 4:
            possible_actions.remove('UP')
        elif index_blank_square == 5:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        elif index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif index_blank_square == 7:
            possible_actions.remove('DOWN')
        elif index_blank_square == 8:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank == 0:
            delta = {'RIGHT': 1, 'DOWN': 2}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        elif blank == 1:
            delta = {'LEFT': -1, 'DOWN': 2}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        elif blank == 2:
            delta = {'UP': -2, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        elif blank == 3:
            delta = {'UP': -2, 'LEFT': -1, 'DOWN': 3, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        elif blank == 4:
            delta = {'LEFT': -1, 'DOWN': 3, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        elif blank == 5:
            delta = {'LEFT': -1, 'DOWN': 3}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        elif blank == 6:
            delta = {'UP': -3, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        elif blank == 7:
            delta = {'UP': -3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        elif blank == 8:
            delta = {'UP': -3, 'LEFT': -1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        queue = [state]
        visited = {state}
        while queue:
            curr_state = queue.pop(0)
            if curr_state == self.goal:
                return True
            for action in self.actions(curr_state):
                temp_state = self.result(curr_state, action)
                if temp_state in visited:
                    continue
                queue.append(temp_state)
                visited.add(temp_state)
        return False

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


def make_rand_Dpuzzle():
    """ return a solvable EightPuzzle object"""
    # create a list and shuffle it
    l = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(l)
    result = DuckPuzzle(tuple(l))
    # shuffle the list until result is solvable
    while not result.check_solvability(tuple(l)):
        random.shuffle(l)
        result = DuckPuzzle(tuple(l))
    return result


def compare_algorithms_duck():
    puzzle = make_rand_Dpuzzle()
    displayDuck(puzzle.initial)

    print("A*-search using the misplaced tile heuristic")
    start_time = time.time()
    result, pops = astar_search_modified(puzzle)
    end_time = time.time()
    misplaced_solution = result.solution()
    elapsed_time = end_time - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("the length of the solution = ", len(misplaced_solution))
    print("that total number of nodes that were removed = ", pops)

    print("A*-search using the Manhattan distance heuristic")
    start_time = time.time()
    result, pops = astar_search_modified(puzzle, manhattan_duck)
    end_time = time.time()
    manhattan_solution = result.solution()
    elapsed_time = end_time - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("the length of the solution = ", len(manhattan_solution))
    print("that total number of nodes that were removed = ", pops)

    print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic")
    start_time = time.time()
    result, pops = astar_search_modified(puzzle, max_heuristic_duck)
    end_time = time.time()
    both_solution = result.solution()
    elapsed_time = end_time - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("the length of the solution = ", len(both_solution))
    print("that total number of nodes that were removed = ", pops)

    print("**************************************************************")


print("testing for eight puzzle")
for i in range(0, 10):
    compare_algorithms_eight()
print("\n")
print("testing for duck puzzle")
for i in range(0, 10):
    compare_algorithms_duck()