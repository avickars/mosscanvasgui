from search import *
import time

RANDOM_MOVES = 1000


# Copied code from search.py with changes to best_first_graph_search
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def best_first_graph_search(problem, f, display=False):
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

    removed_nodes = 0

    while frontier:
        node = frontier.pop()
        removed_nodes += 1
        if problem.goal_test(node.state):
            if display:
                print("Nodes removed from frontier:" + str(removed_nodes))
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


# -------------------------------------------------------------------------------------
# Question 1: Helper Functions
# -------------------------------------------------------------------------------------
def make_rand_8puzzle():
    eight_puzzle_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    eight_puzzle = EightPuzzle(eight_puzzle_state)

    for i in range(RANDOM_MOVES):
        moves = eight_puzzle.actions(eight_puzzle.initial)
        num_moves = len(moves)
        final_move = random.randint(0, num_moves - 1)
        new_state = eight_puzzle.result(eight_puzzle.initial, moves[final_move])
        eight_puzzle = EightPuzzle(new_state)

    assert eight_puzzle.check_solvability(eight_puzzle.initial) == True
    return eight_puzzle


def display(state):
    for i in range(9):
        output = state[i]
        if output == 0:
            print("*", end='   ')
        else:
            print(output, end='   ')
        if i == 2 or i == 5:
            print("\n")


# -------------------------------------------------------------------------------------
# Question 2: Comparing Algorithms
# -------------------------------------------------------------------------------------
def manhatten(node):
    state = node.state
    # Implementation taken from class notes suggestions

    tile_0 = [4, 3, 2, 3, 2, 1, 2, 1, 0]
    tile_1 = [0, 1, 2, 1, 2, 3, 2, 3, 4]
    tile_2 = [1, 0, 1, 2, 1, 2, 3, 2, 3]
    tile_3 = [2, 1, 0, 3, 2, 1, 4, 3, 2]
    tile_4 = [1, 2, 3, 0, 1, 2, 1, 2, 3]
    tile_5 = [2, 1, 2, 1, 0, 1, 2, 1, 2]
    tile_6 = [3, 2, 1, 2, 1, 0, 3, 2, 1]
    tile_7 = [2, 3, 4, 1, 2, 3, 0, 1, 2]
    tile_8 = [3, 2, 3, 2, 1, 2, 1, 0, 1]

    tile_list = [tile_0, tile_1, tile_2, tile_3, tile_4, tile_5, tile_6, tile_7, tile_8]
    total_manhatten_distance = 0
    for i in range(9):
        current_tile = state[i]
        manhattan_distance = tile_list[current_tile][i]
        total_manhatten_distance += manhattan_distance

    return total_manhatten_distance


def max_misplaced_manhatten(node):
    eight_puzzle = EightPuzzle(node.state)
    return max(manhatten(node), eight_puzzle.h(node))


# -------------------------------------------------------------------------------------
# Question 3: Duck-Puzzle
# -------------------------------------------------------------------------------------

class DuckPuzzle(Problem):
    # Code modified from default implementation of EightPuzzle
    def __init__(self, inital, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(inital, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
        restricted_actions_left = [0, 2, 6]
        restricted_actions_up = [0, 1, 4, 5]
        restricted_actions_right = [1, 5, 8]
        restricted_actions_down = [2, 6, 7, 8]

        if index_blank_square in restricted_actions_left:
            possible_actions.remove('LEFT')
        if index_blank_square in restricted_actions_up:
            possible_actions.remove('UP')
        if index_blank_square in restricted_actions_right:
            possible_actions.remove('RIGHT')
        if index_blank_square in restricted_actions_down:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)

        if action == "UP":
            if blank == 2 or blank == 3:
                neighbor = blank - 2
            else:
                neighbor = blank - 3

        elif action == "DOWN":
            if 3 <= blank <= 6:
                neighbor = blank + 3
            else:
                neighbor = blank + 2

        elif action == "LEFT":
            neighbor = blank - 1

        elif action == "RIGHT":
            neighbor = blank + 1

        # Swap blank and neighbor
        new_state[blank] = new_state[neighbor]
        new_state[neighbor] = 0
        return tuple(new_state)

    def value(self, state):
        pass

    def display(self):
        state = self.initial
        for i in range(9):
            output = state[i]
            if output == 0:
                print("*", end='   ')
            else:
                print(output, end='   ')
            if i == 1 or i == 5:
                print("\n")
                if i == 5:
                    print('    ', end='')

    def h(self, node):
        state = node.state
        goal = self.goal
        misplaced = 0
        for i in range(9):
            if state[i] != goal[i] and state[i] != 0:
                misplaced += 1
        return misplaced


def make_rand_duck_puzzle():
    duck_puzzle_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    duck_puzzle = DuckPuzzle(duck_puzzle_state)

    for i in range(RANDOM_MOVES):
        moves = duck_puzzle.actions(duck_puzzle.initial)
        num_moves = len(moves)
        final_move = random.randint(0, num_moves - 1)
        new_state = duck_puzzle.result(duck_puzzle.initial, moves[final_move])
        duck_puzzle = DuckPuzzle(new_state)

    return duck_puzzle


def manhatten_duck(node):
    state = node.state
    # Implementation taken from class notes suggestions

    tile_0 = [5, 4, 4, 3, 2, 1, 2, 1, 0]
    tile_1 = [0, 1, 1, 2, 3, 4, 3, 4, 5]
    tile_2 = [1, 0, 2, 1, 2, 3, 2, 3, 4]
    tile_3 = [1, 2, 0, 1, 2, 3, 2, 3, 4]
    tile_4 = [2, 1, 1, 0, 1, 2, 1, 2, 3]
    tile_5 = [3, 2, 2, 1, 0, 1, 2, 1, 2]
    tile_6 = [4, 3, 3, 2, 1, 0, 3, 2, 1]
    tile_7 = [3, 2, 2, 1, 2, 3, 0, 1, 2]
    tile_8 = [4, 3, 3, 2, 1, 2, 1, 0, 1]

    tile_list = [tile_0, tile_1, tile_2, tile_3, tile_4, tile_5, tile_6, tile_7, tile_8]
    total_manhatten_distance = 0
    for i in range(9):
        current_tile = state[i]
        manhattan_distance = tile_list[current_tile][i]
        total_manhatten_distance += manhattan_distance

    return total_manhatten_distance


def max_misplaced_manhatten_duck(node):
    duck_puzzle = DuckPuzzle(node.state)
    return max(duck_puzzle.h(node), manhatten_duck(node))


# -------------------------------------------------------------------------------------
# Testing functions
# -------------------------------------------------------------------------------------
def astar_time_search(problem, h):
    print("Search started")
    start_time = time.time()
    # Altered astar_boolean to display # removed nodes
    solution = astar_search(problem, h=h, display=True).solution()
    elapsed_time = time.time() - start_time
    print("Elapsed time: " + str(elapsed_time))
    print("Solution length: " + str(len(solution)))
    print(solution)


def test_duck_puzzle(duck_test_list):
    for i in range(10):
        puzzle_state = duck_test_list[i]
        duck_puzzle = DuckPuzzle(puzzle_state)
        # duck_puzzle.display()
        print("Testing p" + str(i + 1))
        # astar_time_search(duck_puzzle, duck_puzzle.h)
        astar_time_search(duck_puzzle, manhatten_duck)
        # astar_time_search(duck_puzzle, max_misplaced_manhatten_duck)
        print("\n")


def test_eight_puzzle(test_list):
    for i in range(len(test_list)):
        # display(eight_puzzle)
        puzzle_state = test_list[i]
        eight_puzzle = EightPuzzle(puzzle_state)
        print("Testing p" + str(i + 1))
        # astar_time_search(eight_puzzle, eight_puzzle.h)
        # astar_time_search(eight_puzzle, manhatten)
        astar_time_search(eight_puzzle, max_misplaced_manhatten)
        print("\n")


def main():
    # Test case puzzles:
    p1 = (2, 6, 8, 5, 0, 4, 7, 3, 1)
    p2 = (0, 2, 7, 8, 1, 5, 4, 3, 6)
    p3 = (8, 7, 1, 5, 6, 4, 0, 3, 2)
    p4 = (3, 1, 6, 2, 4, 8, 7, 5, 0)
    p5 = (0, 6, 8, 4, 5, 7, 1, 2, 3)
    p6 = (2, 6, 0, 8, 5, 3, 1, 4, 7)
    p7 = (6, 3, 0, 4, 1, 5, 2, 7, 8)
    p8 = (5, 2, 3, 1, 0, 6, 8, 7, 4)
    p9 = (8, 3, 2, 7, 5, 4, 6, 1, 0)
    p10 = (0, 3, 5, 1, 6, 8, 4, 7, 2)

    test_list = (p1, p2, p3, p4, p5, p6, p7, p8, p9, p10)

    # test_eight_puzzle(test_list)

    # Test duck puzzles:
    dp1 = (2, 3, 0, 1, 6, 5, 7, 4, 8)
    dp2 = (3, 0, 2, 1, 4, 6, 8, 7, 5)
    dp3 = (1, 0, 3, 2, 5, 8, 6, 7, 4)
    dp4 = (1, 2, 3, 4, 7, 6, 0, 8, 5)
    dp5 = (2, 3, 0, 1, 5, 4, 8, 7, 6)
    dp6 = (2, 3, 0, 1, 7, 5, 6, 8, 4)
    dp7 = (2, 3, 1, 4, 7, 5, 0, 6, 8)
    dp8 = (2, 3, 1, 6, 7, 5, 0, 8, 4)
    dp9 = (3, 1, 2, 5, 8, 7, 0, 4, 6)
    dp10 = (3, 1, 2, 6, 4, 7, 8, 5, 0)

    duck_test_list = (dp1, dp2, dp3, dp4, dp5, dp6, dp7, dp8, dp9, dp10)

    test_duck_puzzle(duck_test_list)


if __name__ == '__main__':
    main()
