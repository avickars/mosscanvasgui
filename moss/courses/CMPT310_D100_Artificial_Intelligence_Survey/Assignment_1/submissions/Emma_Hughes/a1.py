# a1.py
# Emma Hughes 301320199 eha38@sfu.ca

from search import *
import random
import time
import copy

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

#####################
# EightPuzzle Stuff #
#####################
class myEightPuzzle(EightPuzzle):
    def display(self, state):
        i = 0
        for x in state:
            if (i % 3 == 2): # If end of line
                if x == 0:
                    print("*")
                else:
                    print(x)
            else:  # If not end of line
                if x == 0:
                    print("*", end=" ")
                else:
                    print(x, end=" ")
            i += 1

        return None


    # http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
    def manhattan_algorithm(self, node):
        score = 0
        i = 0
        for x in node.state: # For each tile in current state
            j = 0
            for y in self.goal: # For each tile in goal state
                if x == y: # Find match
                    score += abs((i / 3) - (j / 3)) + abs((i % 3) - (j % 3)) # Row difference + Column difference
                j += 1
            i += 1

        return score


    def max_algorithm(self, node):
        return max(self.manhattan_algorithm(node), self.h(node))

# End of myEightPuzzle class


def make_rand_8puzzle():
    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    random.shuffle(state)
    while not myEightPuzzle(state).check_solvability(state):
        random.shuffle(state)

    return myEightPuzzle(tuple(state))


def my_astar_search(problem, h=None, display=False): # Taken from search.py
    h = memoize(h or problem.h, 'h')
    return my_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def my_best_first_graph_search(problem, f, display=False): # Taken from search.py
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    nodes_removed = 0

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")

            print("Node path cost: " + str(node.path_cost))
            print("Total # of nodes removed: " + str(nodes_removed))

            return node

        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)

                    nodes_removed += 1
    return None


##############
# Duck Stuff #
##############
class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)


    def find_blank_square(self, state):
        return state.index(0)


    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions


    def calc_delta(self, state):
        index_blank_square = self.find_blank_square(state)

        delta = {
            0: {'DOWN': 2,  'RIGHT': 1},
            1: {'DOWN': 2,  'LEFT':  -1},
            2: {'UP': -2,   'RIGHT': 1},
            3: {'UP': -2,   'DOWN': 3,  'LEFT': -1, 'RIGHT': 1},

            4: {'DOWN': 3,  'LEFT': -1, 'RIGHT': 1},
            5: {'DOWN': 3,  'LEFT': -1},
            6: {'UP': -3,   'RIGHT': 1},
            7: {'UP': -3,   'LEFT': -1, 'RIGHT': 1},
            8: {'UP': -3,   'LEFT': -1}
        }

        return delta.get(index_blank_square)


    def result(self, state, action):
        blank = self.find_blank_square(state) # Index of the blank square
        new_state = list(state)

        delta = self.calc_delta(state)

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)


    def goal_test(self, state):
        return state == self.goal

    def display(self, state):
        i = 0
        for x in state:
            if x == 0: x = '*'

            if i == 0: print(x, end=" ")
            if i == 1: print(x, end="    \n")
            if i == 2 or i == 3 or i == 4: print(x, end=" ")
            if i == 5: print(x, end="\n  ")
            if i == 6 or i == 7: print(x, end=" ")
            if i == 8: print(x)

            i += 1
            if x == '*': x = 0
            

        return None


    def h(self, node): # Taken from search.py
        return sum(s != g for (s, g) in zip(node.state, self.goal))


    def manhattan_algorithm(self, node): 
        score = 0
        i = 0
        for x in node.state: # For each tile in current state
            if i == 2: # TODO Oh man
                i = 4
            elif i == 8:
                i = 9

            j = 0
            for y in self.goal: # For each tile in goal state
                if i == 2: # TODO Oh man
                    i = 4
                elif i == 8:
                    i = 9

                if x == y: # Find match
                    score += abs((i / 3) - (j / 3)) + abs((i % 4) - (j % 4)) # Row difference + Column difference
                j += 1
            i += 1

        return score


    def max_algorithm(self, node):
        return max(self.manhattan_algorithm(node), self.h(node)) # Ret max of manhattan and h algorithms

# End of DuckPuzzle class


def make_rand_duck_puzzle():
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = DuckPuzzle(state)

    for i in range(1000):
        act = puzzle.actions(state)
        random.shuffle(act)

        state = puzzle.result(state, act[0])

    return DuckPuzzle(tuple(state))


##################
# Main Functions #
##################
def test_algorithms(puzzle):
    # Run misplaced tile algorithm
    start = time.time()
    my_astar_search(puzzle, puzzle.h)
    elapsed = time.time() - start
    print("Time taken for misplaced tile algorithm: " + str(elapsed) + "\n")

    # Run Manhattan distance algorithm
    start = time.time()
    my_astar_search(puzzle, puzzle.manhattan_algorithm)
    elapsed = time.time() - start
    print("Time taken for Manhattan distance algorithm: " + str(elapsed) + "\n")

    # Run combo algorithm
    start = time.time()
    my_astar_search(puzzle, puzzle.max_algorithm)
    elapsed = time.time() - start
    print("Time taken for max: " + str(elapsed) + "\n")


def run_8puzzle():
    puzzle0 = make_rand_8puzzle()
    puzzle1 = make_rand_8puzzle()
    puzzle2 = make_rand_8puzzle()
    puzzle3 = make_rand_8puzzle()
    puzzle4 = make_rand_8puzzle()
    puzzle5 = make_rand_8puzzle()
    puzzle6 = make_rand_8puzzle()
    puzzle7 = make_rand_8puzzle()
    puzzle8 = make_rand_8puzzle()
    puzzle9 = make_rand_8puzzle()

    puzzle_array = [puzzle0, puzzle1, puzzle2, puzzle3, puzzle4, 
                    puzzle5, puzzle6, puzzle7, puzzle8, puzzle9]

    print("8PUZZLE", end="\n---------------")
    for i in range(len(puzzle_array)):
        print("\nTest " + str(i) + ":")  # Display Test name
        puzzle_array[i].display(puzzle_array[i].initial)  # Display initial state
        test_algorithms(puzzle_array[i])

    print("FINISHED 8PUZZLE!")

    return None

# RUN THIS
def run_duck():
    puzzle0 = make_rand_duck_puzzle()
    puzzle1 = make_rand_duck_puzzle()
    puzzle2 = make_rand_duck_puzzle()
    puzzle3 = make_rand_duck_puzzle()
    puzzle4 = make_rand_duck_puzzle()
    puzzle5 = make_rand_duck_puzzle()
    puzzle6 = make_rand_duck_puzzle()
    puzzle7 = make_rand_duck_puzzle()
    puzzle8 = make_rand_duck_puzzle()
    puzzle9 = make_rand_duck_puzzle()

    puzzle_array = [puzzle0, puzzle1, puzzle2, puzzle3, puzzle4, 
                    puzzle5, puzzle6, puzzle7, puzzle8, puzzle9]

    print("DUCK", end="\n---------------")
    for i in range(len(puzzle_array)):
        print("\nTest " + str(i) + ":") # Display Test name
        puzzle_array[i].display(puzzle_array[i].initial) # Display initial state
        test_algorithms(puzzle_array[i])

    print("FINISHED QUACK!")

    return None