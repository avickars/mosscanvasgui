# a1.py

from search import *

import random
import time

# Global Variables
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)


# Question 1 ______________________________________________________________________________

def make_rand_8puzzle():
    """ Returns a new instance of an 8-puzzle problem with a random solvable initial state """
    
    state = goal_state
    puzzle = EightPuzzle(state, goal_state)

    # Make a random number of valid moves starting from the solved state
    for _ in range(100, 200):
        valid_moves = puzzle.actions(state)
        move = random.choice(valid_moves)
        state = puzzle.result(state, move)

    # Verify the solvability of the new random state obtained
    if puzzle.check_solvability(state) == False:
        print("Error: Failed to generate a solvable 8-puzzle instance")
        return None

    return EightPuzzle(state)

def display(state):
    """ Prints a human-readable 8-puzzle state """

    curr = list(state)
    index = curr.index(0)
    curr[index] = "*"

    print(curr[0], curr[1], curr[2])
    print(curr[3], curr[4], curr[5])
    print(curr[6], curr[7], curr[8])


# Question 2 ______________________________________________________________________________

def rand_8puzzles(n):
    """ Returns n instances of 8-puzzle problems with solvable random initial states """

    puzzles = []
    for _ in range(n):
        puzzles.append(make_rand_8puzzle())

    return puzzles

# Modified EightPuzzle.h() from search.py
def h_misplaced(node):
    """ Returns the misplaced tile heuristic value for a given state.
    h(n) = number of misplaced tiles """

    h_val = sum(s != g for (s, g) in zip(node.state, goal_state))

    # Exclude the blank tile from the heuristic
    if (node.state.index(0) != goal_state.index(0)):
        h_val -= 1

    return h_val

def h_manhattan(node):
    """ Returns the Manhattan distance heuristic value for a given state.
    h(n) = total Manhattan distance b/w tiles in current versus goal state """

    mhd = 0

    # Exclude the blank tile from the heuristic
    state = list(goal_state)
    state.remove(0)
    for i in state:
        curr = node.state.index(i)
        goal = goal_state.index(i)

        # Distance along X-axis
        mhd += abs((curr % 3) - (goal % 3))

        # Distance along Y-axis
        mhd += abs((curr // 3) - (goal // 3))

    return mhd

def h_max(node):
    """ Returns the max of the misplaced tile heuristic and the Manhattan distance heuristic.
    h(n) = max(misplaced tile heuristic value, Manhattan distance heuristic value)"""

    return max(h_misplaced(node), h_manhattan(node))

# Modified astar_search from search.py
def modified_astar_search(problem, h = None, display = False, benchmark = False):
    """ A* search is best-first graph search with f(n) = g(n) + h(n). You need to specify
    the h function when you call astar_search, or else in your Problem subclass. """

    h = memoize(h or problem.h, 'h')

    if benchmark:
        start = time.time()
        solution = modified_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display, benchmark)
        end = time.time()
        elapsed = end - start

        print(f'Time: {elapsed}s')
        print(f'Length: {len(solution.solution())} moves')
        return solution
    else:
        return modified_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# Modified best_first_graph_search from search.py
def modified_best_first_graph_search(problem, f, display = False, benchmark = False):
    """ Search the nodes with the lowest f scores first. You specify the function f(node)
    that you want to minimize; for example, if f is a heuristic estimate to the goal,
    then we have greedy best first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f values will be
    cached on the nodes as they are computed. So after doing a best first search you can
    examine the f values of the path returned """

    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    popped = 0
    while frontier:
        node = frontier.pop()
        popped += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            if benchmark:
                print(f'Popped: {popped} nodes')
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

def solve_8puzzles(puzzles, print_solution = True, benchmarking = False):
    for x in puzzles:
        print("\n------------------------------------------------------------------------------------")
        print("8-Puzzle", puzzles.index(x) + 1)
        print("------------------------------------------------------------------------------------\n")

        # Display the initial state of the puzzle
        display(x.initial)

        # A*-search using the misplaced tile heuristic (default)
        print("\nMisplaced Tile Heuristic: ---------------------------")
        mpt_sol = modified_astar_search(x, h_misplaced, benchmark = benchmarking).solution()
        if print_solution:
            print(mpt_sol)

        # A*-search using the Manhattan distance heuristic
        print("\nManhattan Distance Heuristic: -----------------------")
        mhd_sol = modified_astar_search(x, h_manhattan, benchmark = benchmarking).solution()
        if print_solution:
            print(mhd_sol)

        # A*-search using the max of the misplaced tile heuristic and Manhattan distance heuristic
        print("\nMax Heuristic ---------------------------------------")
        max_sol = modified_astar_search(x, h_max, benchmark = benchmarking).solution()
        if print_solution:
            print(max_sol)


# Question 3 ______________________________________________________________________________

def make_rand_duck_puzzle():
    """ Returns a new instance of a Duck puzzle problem with a random solvable initial state """
    
    state = goal_state
    puzzle = DuckPuzzle(state, goal_state)

    # Make a random number of valid moves starting from the solved state
    for _ in range(100, 200):
        valid_moves = puzzle.actions(state)
        move = random.choice(valid_moves)
        state = puzzle.result(state, move)

    return DuckPuzzle(state)

def rand_duck_puzzles(n):
    """ Returns n instances of duck puzzle problems with solvable random initial states """

    puzzles = []
    for _ in range(n):
        puzzles.append(make_rand_duck_puzzle())

    return puzzles

class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a duck shaped board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number at index i (0 if it's an empty square)

    Indices of the state tuple correspond to the following positions (this is not the goal state):
    +---+---+
    | 0 | 1 |
    +---+---+---+---+
    | 2 | 3 | 4 | 5 |
    +---+---+---+---+
        | 6 | 7 | 8 |
        +---+---+---+

    """

    def __init__(self, initial, goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)):
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

        if index_blank_square in [0, 1, 4, 5]:
            possible_actions.remove('UP')
        if index_blank_square in [2, 6, 7, 8]:
            possible_actions.remove('DOWN')
        if index_blank_square in [0, 2, 6]:
            possible_actions.remove('LEFT')
        if index_blank_square in [1, 5, 8]:
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h_misplaced(self, node):
        """ Returns the misplaced tile heuristic value for a given state.
        h(n) = number of misplaced tiles """

        h_val = sum(s != g for (s, g) in zip(node.state, self.goal))

        # Exclude the blank tile from the heuristic
        if (node.state.index(0) != self.goal.index(0)):
            h_val -= 1

        return h_val

    # Adapted from manhattan() in test_search.py
    def h_manhattan(self, node):
        """ Returns the Manhattan distance heuristic value for a given state.
        h(n) = total Manhattan distance b/w tiles in current versus goal state """

        state = node.state
        index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]
        
        index_goal = {}
        for i in range(len(self.goal)):
            index_goal[self.goal[i]] = index[i]

        index_state = {}
        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhd = 0

        # Exclude the blank tile from the heuristic
        for i in range(1, len(self.goal)):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

        return mhd

    def h_max(self, node):
        """ Returns the max of the misplaced tile heuristic and the Manhattan distance heuristic.
        h(n) = max(misplaced tile heuristic value, Manhattan distance heuristic value)"""

        return max(self.h_misplaced(node), self.h_manhattan(node))

    def display(self, state):
        """ Print a human-readable Duck puzzle state """

        curr = list(state)
        index = curr.index(0)
        curr[index] = "*"

        print(curr[0], curr[1])
        print(curr[2], curr[3], curr[4], curr[5])
        print(" ", curr[6], curr[7], curr[8])

def solve_duck_puzzles(puzzles, print_solution = True, benchmarking = False):
    for x in puzzles:
        print("\n------------------------------------------------------------------------------------")
        print("Duck Puzzle", puzzles.index(x))
        print("------------------------------------------------------------------------------------\n")

        # Display the initial state of the puzzle
        x.display(x.initial)

        # A*-search using the misplaced tile heuristic (default)
        print("\nMisplaced Tile Heuristic: ---------------------------")
        mpt_sol = modified_astar_search(x, x.h_misplaced, benchmark = benchmarking).solution()
        if print_solution:
            print(mpt_sol)

        # A*-search using the Manhattan distance heuristic
        print("\nManhattan Distance Heuristic: -----------------------")
        mhd_sol = modified_astar_search(x, x.h_manhattan, benchmark = benchmarking).solution()
        if print_solution:
            print(mhd_sol)

        # A*-search using the max of the misplaced tile heuristic and Manhattan distance heuristic
        print("\nMax Heuristic ---------------------------------------")
        max_sol = modified_astar_search(x, x.h_max, benchmark = benchmarking).solution()
        if print_solution:
            print(max_sol)


# Main functions __________________________________________________________________________

def main():
    # Create 10 random solvable 8-puzzles and duck puzzles
    eight_puzzles = rand_8puzzles(10)
    duck_puzzles = rand_duck_puzzles(10)

    # Solve and display the solutions
    solve_8puzzles(eight_puzzles, print_solution = False, benchmarking = True)
    solve_duck_puzzles(duck_puzzles, print_solution = False, benchmarking = True)

if __name__ == "__main__":
    main()