# a1.py
# Albert Cao (301254951)
# 05/23/20

### The "0" tile is counted in all heuristic functions.

# Elapsed time calculation code shamelessly copied from:
# https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
# Randomization code inspired by:
# https://stackoverflow.com/questions/28958391/shuffle-a-tuple-in-python and
# https://docs.python.org/3/library/random.html
# Tuple indexing expertise grabbed from:
# https://www.programiz.com/python-programming/methods/tuple/index

import time
from search import *
from random import shuffle

### Question 1

# make_rand_8puzzle()
def make_rand_8puzzle():
    tiles = tuple(range(9))
    randomized = ()
    solve = False

    while solve == False:
        randomized = random.sample(tiles, len(tiles))  
        puzzle = EightPuzzleExt(tuple(randomized))
        solve = puzzle.check_solvability(randomized)

    return puzzle

# display()
def display(state):
    count = 0
    display_string = ""

    for i in state:
        # Counting iterations of the loop...
        count = count + 1

        # Concatenating to display_string and replacing "0" with "*"...
        if (i == 0):
            display_string = display_string + "*" + " "
        else:
            display_string = display_string + str(i) + " "

        if (count % 3 == 0 and count != 9):
            display_string = display_string + '\n'
    
    print(display_string)
    return display_string 

###

### Question 2

# astar() - copied from search.py and modified.
def astar(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return best_first(problem, lambda n: n.path_cost + h(n), display)

# best_first() - copied from search.py and modified.
def best_first(problem, f, display=False):
    start_time = time.time()
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    removed = 0
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        removed = removed + 1
        if problem.goal_test(node.state):
            if display:
                print("Total running time in seconds: ", (time.time() - start_time), " s")
                print("Length (i.e., number of tiles moved) of the solution: ", node.depth)
                print("Total number of nodes that were removed from frontier: ", removed)
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

# EightPuzzleExt subclass.
class EightPuzzleExt(EightPuzzle): 

    # manh() - a Manhattan heuristic function.
    def manh(self, node):
        # Total moves estimated by the Manhattan heuristic.
        man_dist = 0

        # Manhattan Heuristic Function
        for i in node.state:
            x1, x2, y1, y2, = 0, 0, 0, 0
            curr_pos = node.state.index(i)
            goal_pos = self.goal.index(i)

            # Calculating coordinates of current tile position...
            if curr_pos == 0:
                x1 = 1
                y1 = 1
            elif curr_pos == 1:
                x1 = 2
                y1 = 1
            elif curr_pos == 2:
                x1 = 3
                y1 = 1
            elif curr_pos == 3:
                x1 = 1
                y1 = 2
            elif curr_pos == 4:
                x1 = 2
                y1 = 2
            elif curr_pos == 5:
                x1 = 3
                y1 = 2
            elif curr_pos == 6:
                x1 = 1
                y1 = 3
            elif curr_pos == 7:
                x1 = 2
                y1 = 3
            elif curr_pos == 8:
                x1 = 3
                y1 = 3

            # Calculating coordinates of goal tile position...
            if goal_pos == 0:
                x2 = 1
                y2 = 1
            elif goal_pos == 1:
                x2 = 2
                y2 = 1
            elif goal_pos == 2:
                x2 = 3
                y2 = 1
            elif goal_pos == 3:
                x2 = 1
                y2 = 2
            elif goal_pos == 4:
                x2 = 2
                y2 = 2
            elif goal_pos == 5:
                x2 = 3
                y2 = 2
            elif goal_pos == 6:
                x2 = 1
                y2 = 3
            elif goal_pos == 7:
                x2 = 2
                y2 = 3
            elif goal_pos == 8:
                x2 = 3
                y2 = 3
            
            # Copied from the existing Manhattan algorithm...
            tile_dist = abs(x2 - x1) + abs(y2 - y1)
            man_dist = man_dist + tile_dist

        return man_dist

    def maxh(self, node):
        return max(self.h(node), self.manh(node))

###

### Question 3

# DuckPuzzle subclass.
class DuckPuzzle(Problem): 
    
    # Constructor.
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    # find_blank_square()
    def find_blank_square(self, state):
        return state.index(0)

    # actions()
    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 2 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    # goal_test()
    def goal_test(self, state):
        return state == self.goal

    # result()
    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    # h()
    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

    # manh() - a Manhattan heuristic function.
    def manh(self, node):
        # Total moves estimated by the Manhattan heuristic.
        man_dist = 0

        # Manhattan Heuristic Function
        for i in node.state:
            x1, x2, y1, y2, = 0, 0, 0, 0
            curr_pos = node.state.index(i)
            goal_pos = self.goal.index(i)

            # Calculating coordinates of current tile position...
            if curr_pos == 0:
                x1 = 1
                y1 = 1
            elif curr_pos == 1:
                x1 = 2
                y1 = 1
            elif curr_pos == 2:
                x1 = 1
                y1 = 2
            elif curr_pos == 3:
                x1 = 2
                y1 = 2
            elif curr_pos == 4:
                x1 = 3
                y1 = 2
            elif curr_pos == 5:
                x1 = 4
                y1 = 2
            elif curr_pos == 6:
                x1 = 2
                y1 = 3
            elif curr_pos == 7:
                x1 = 3
                y1 = 3
            elif curr_pos == 8:
                x1 = 4
                y1 = 3

            # Calculating coordinates of goal tile position...
            if goal_pos == 0:
                x1 = 1
                y1 = 1
            elif goal_pos == 1:
                x1 = 2
                y1 = 1
            elif goal_pos == 2:
                x1 = 1
                y1 = 2
            elif goal_pos == 3:
                x1 = 2
                y1 = 2
            elif goal_pos == 4:
                x1 = 3
                y1 = 2
            elif goal_pos == 5:
                x1 = 4
                y1 = 2
            elif goal_pos == 6:
                x1 = 2
                y1 = 3
            elif goal_pos == 7:
                x1 = 3
                y1 = 3
            elif goal_pos == 8:
                x1 = 4
                y1 = 3
            
            # Copied from the existing Manhattan algorithm...
            tile_dist = abs(x2 - x1) + abs(y2 - y1)
            man_dist = man_dist + tile_dist

        return man_dist

    def maxh(self, node):
        return max(self.h(node), self.manh(node))

# make_rand_duck_puzzle()
def make_rand_duck_puzzle():
    tiles = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = DuckPuzzle(tiles)
    outcome = puzzle.initial
    actions = puzzle.actions(puzzle.initial)
    count = 0

    while count < 1000:
        random_index = random.choice(list(range(len(actions))))
        outcome = puzzle.result(outcome, actions[random_index])
        actions = puzzle.actions(outcome)

        count = count + 1

    return DuckPuzzle(outcome)

# duck_display()
def duck_display(state):
    count = 0
    display_string = ""

    for i in state:
        # Counting iterations of the loop...
        count = count + 1

        # Concatenating to display_string and replacing "0" with "*"...
        if (i == 0):
            i = "*"

        if (count == 2 or count == 6):
            display_string = display_string + str(i) + " " + "\n"
        elif (count == 7):
            display_string = display_string + "  " + str(i) + " "
        else:
            display_string = display_string + str(i) + " "
    
    print(display_string)
    return display_string 

###

def main():
    ### Question 2

    # Comparing Algorithms
    for i in range(10):
        print("------------------------------------------")
        print("                 Puzzle ", i + 1)
        print("------------------------------------------")

        puzzle = make_rand_8puzzle()
        print()
        display(puzzle.initial)
        print()

        # Misplaced Tile Heuristic
        print("###############")
        print("Misplaced Tile:")
        print("###############")
        astar(puzzle, puzzle.h, True)
        print()

        # Manhattan Heuristic
        print("###############")
        print("Manhattan:")
        print("###############")
        astar(puzzle, puzzle.manh, True)
        print()

        # Max Heuristic
        print("###############")
        print("Max:")
        print("###############")
        astar(puzzle, puzzle.maxh, True)
        print()

    ###

    ### Question 3

    # Comparing Algorithms
    for i in range(10):
        print("------------------------------------------")
        print("                 Puzzle ", i + 1)
        print("------------------------------------------")

        duck_puzzle = make_rand_duck_puzzle()
        print()
        duck_display(duck_puzzle.initial)
        print()

        # Misplaced Tile Heuristic
        print("###############")
        print("Misplaced Tile:")
        print("###############")
        astar(duck_puzzle, duck_puzzle.h, True)
        print()

        # Manhattan Heuristic
        print("###############")
        print("Manhattan:")
        print("###############")
        astar(duck_puzzle, duck_puzzle.manh, True)
        print()

        # Max Heuristic
        print("###############")
        print("Max:")
        print("###############")
        astar(duck_puzzle, duck_puzzle.maxh, True)
        print()
    
    ###

if (__name__ == "__main__"):
    main()