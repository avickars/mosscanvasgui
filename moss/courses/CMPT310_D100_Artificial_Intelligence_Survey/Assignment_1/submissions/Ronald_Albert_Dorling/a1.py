# a1.py

from search import *
from random import *
import time

# Make random EightPuzzle by performing 100 random moves from goal state
def make_rand_8puzzle():
    state = (1,2,3,4,5,6,7,8,0)
    puzzle = EightPuzzle(state)

    for x in range(0, 100):
        actions = puzzle.actions(state)
        randomIndex = randint(0, len(actions) - 1)
        randomAction = puzzle.actions(state)[randomIndex]
        state = puzzle.result(state, randomAction)

    return state

# Make random DuckPuzzle by performing 50 random moves from goal states
# The puzzle would not solve in reasonable amount of time when using 100
def make_rand_duck_puzzle():
    state = (1,2,3,4,5,6,7,8,0)
    puzzle = DuckPuzzle(state)

    for x in range(0, 50):
        actions = puzzle.actions(state)
        randomIndex = randint(0, len(actions) - 1)
        randomAction = puzzle.actions(state)[randomIndex]
        state = puzzle.result(state, randomAction)

    return state

# Display the state of an EightPuzzle
def display(state):
    line = ''
    count = 0

    for tile in state:
        count += 1
        if tile == 0:
            tile = '*'
        line += str(tile) + ' '
        if count % 3 == 0:
            print(line)
            line = ''

    print()

# Print the desired stats from solving the puzzles
def print_stats(stats):
    output = 'removed: ' + str(stats['removed']) + ', '
    output += 'length: ' + str(stats['length']) + ', '
    output += 'time: ' + str(stats['time'])
    print(output)

# Method taken from aima.python with the addition of stats
def my_astar_search(problem, stats, h=None, display=False):
    h = memoize(h or problem.h, 'h')

    return my_best_first_graph_search(problem, stats, lambda n: n.path_cost + h(n), display)

# Method taken from aima.python with the addition of stats
def my_best_first_graph_search(problem, stats, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        stats['removed'] += 1
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            stats['length'] = len(explored)
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

# Extend the EightPuzzle class to include two new heuristics
class ExtendedEightPuzzle(EightPuzzle):
    def __init__(self, initial):
        super().__init__(initial)

    def manhattan_distance(self, node):
        manhattan_distance = 0
        index = 0
        for tile in node.state:
            # Don't count distance for 0 because we are trying to get the other
            # tiles into the correct position and once this is achieved, 0 will
            # be in the correct position as a byproduct
            if (tile != 0):
                # Add number of rows this tile is away from its goal position
                manhattan_distance += abs(index // 3 - (tile - 1) // 3)
                # Add number of columns this tile is away from its goal position
                manhattan_distance += abs(index % 3 - (tile - 1) % 3)
            index += 1
        return manhattan_distance

    def max_heuristic(self, node):
        return max(self.h(node), self.manhattan_distance(node))

# Note that EighPuzzle of aima-python was the basis for the code in this class
# Required changes were made, but other functions are left unchanged
class DuckPuzzle(Problem):
    """ This puzzle has the same rules as the 8-puzzle,
        Except instead of a 3x3 board,
        The board has the following shape: 1 2
                                           3 4 5 6
                                             7 8 *
    """
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        # Exhaustive list of possible moves; this adds to how slow it performs
        if (index_blank_square == 0):
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif (index_blank_square == 1):
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        elif (index_blank_square == 2):
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
        elif (index_blank_square == 4):
            possible_actions.remove('UP')
        elif (index_blank_square == 5):
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        elif (index_blank_square == 6):
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
        elif (index_blank_square == 7):
            possible_actions.remove('DOWN')
        elif (index_blank_square == 8):
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        index_blank_square = self.find_blank_square(state)
        new_state = list(state)

        # Going between rows 0 & 1 is 2 indices
        # Going between rows 1 & 2 is 3 indices
        if index_blank_square < 6:
            delta_up = -2 # Row 1 to row 0
        else:
            delta_up = -3 # Row 2 to row 1

        if index_blank_square < 2:
            delta_down = 2 # Row 0 to row 1
        else:
            delta_down = 3 # Row 1 to row 2

        delta = {'UP': delta_up, 'DOWN': delta_down, 'LEFT': -1, 'RIGHT': 1}
        neighbor = index_blank_square + delta[action]
        new_state[index_blank_square], new_state[neighbor] = new_state[neighbor], new_state[index_blank_square]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

    # Get the row of the puzzle for a given index
    def get_row(self, index):
        if index < 3:
            return 0
        if index < 6:
            return 1
        return 2

    # Get the column of the puzzle for a given index
    def get_col(self, index):
        if index == 0 or index == 2:
            return 0
        if index == 4 or index == 7:
            return 2
        if index == 5 or index == 8:
            return 3
        return 1 # Check for col 1 last because it has 3 indices


    def manhattan_distance(self, node):
        manhattan_distance = 0
        index = 0;
        for tile in node.state:
            if tile != 0:
                # Same principle as EightPuzzle, count how many rows and columns
                # The tiles are from their correct position
                manhattan_distance += abs(self.get_col(index) - self.get_col(tile - 1))
                manhattan_distance += abs(self.get_row(index) - self.get_row(tile - 1))
            index += 1
        return manhattan_distance

    def max_heuristic(self, node):
        return max(self.h(node), self.manhattan_distance(node))



        return sum(s != g for (s, g) in zip(node.state, self.goal))

# Compare the EightPuzzle using the 3 Heuristics noted above

# Set the random states to be the same set used for each algorithm
random_states = []
for x in range(0, 10):
    random_states.append(make_rand_8puzzle())

print('---- Stats using misplaced tile heuristic ----')
for state in random_states:
    stats = {'length': 0, 'removed': 0, 'time': time.time()}
    puzzle = ExtendedEightPuzzle(state)
    my_astar_search(puzzle, stats, puzzle.h)
    stats['time'] = time.time() - stats['time']
    print_stats(stats)
print()

print('---- Stats using manhattan distance heuristic ----')
for state in random_states:
    stats = {'length': 0, 'removed': 0, 'time': time.time()}
    puzzle = ExtendedEightPuzzle(state)
    my_astar_search(puzzle, stats, puzzle.manhattan_distance)
    stats['time'] = time.time() - stats['time']
    print_stats(stats)
print()

print('---- Stats using max of both heuristics ----')
for state in random_states:
    stats = {'length': 0, 'removed': 0, 'time': time.time()}
    puzzle = ExtendedEightPuzzle(state)
    my_astar_search(puzzle, stats, puzzle.max_heuristic)
    stats['time'] = time.time() - stats['time']
    print_stats(stats)
print()

# Perform the same process for the DuckPuzzle
random_states = []
for x in range(0, 10):
    random_states.append(make_rand_duck_puzzle())

print('---- Stats using misplaced tile heuristic ----')
for state in random_states:
    stats = {'length': 0, 'removed': 0, 'time': time.time()}
    puzzle = DuckPuzzle(state)
    my_astar_search(puzzle, stats, puzzle.h)
    stats['time'] = time.time() - stats['time']
    print_stats(stats)
print()

print('---- Stats using manhattan distance heuristic ----')
for state in random_states:
    stats = {'length': 0, 'removed': 0, 'time': time.time()}
    puzzle = DuckPuzzle(state)
    my_astar_search(puzzle, stats, puzzle.manhattan_distance)
    stats['time'] = time.time() - stats['time']
    print_stats(stats)
print()

print('---- Stats using max of both heuristics ----')
for state in random_states:
    stats = {'length': 0, 'removed': 0, 'time': time.time()}
    puzzle = DuckPuzzle(state)
    my_astar_search(puzzle, stats, puzzle.max_heuristic)
    stats['time'] = time.time() - stats['time']
    print_stats(stats)
print()