# a1.py

from search import * 
import random
import time

# referred to https://www.w3schools.com/python/python_tuples.asp


def make_rand_8puzzle():
    int_list = [i for i in range(9)]
    random.shuffle(int_list)
    puzzle = EightPuzzle(tuple(int_list))
    while not puzzle.check_solvability(puzzle.initial):
        random.shuffle(int_list)
        puzzle = EightPuzzle(tuple(int_list))

    return puzzle


def display(state):
    result = ""
    for i in range(9):
        if state[i] == 0:
            result += '*'
        else:
            result += str(state[i])
        if i in [2, 5]:
            result += '\n'
        else:
            result += ' '

    print(result)


def astar_search(problem, h=None):
    h=memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))
    

# modified best_first_graph search from search.py
def best_first_graph_search(problem, h=None):
    h = memoize(h or problem.h, 'h')
    node = Node(problem.initial)
    num_nodes_removed = 0
    frontier = PriorityQueue('min', h)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        num_nodes_removed += 1
        if problem.goal_test(node.state):
            return len(node.path()), num_nodes_removed
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if h(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, None


def show_problemset_stats(problemset, display_func=display):
    """displays the search stats of a set of given problems using three different
    heuristics: misplaced-tile, manhattan-distance, and the max of these."""
    for problem in problemset:
        print()
        display_func(problem.initial)
        show_search_stats(problem, "MISPLACED TILE")
        show_search_stats(problem, "MANHATTAN DISTANCE", problem.manhattan_distance)
        show_search_stats(problem, "MAX OF HEURISTICS", problem.max_h)


def show_search_stats(problem, header, h=None):
    """shows the time, length of solution, and # nodes removed from
    the frontier during the astar search of a problem using a give heuristic"""
    divider = '-' * len(header)
    print(divider + '\n' + header + '\n' + divider)
    solution_length = 0
    nodes_removed = 0
    start_time = time.time()
    
    sol_length, num_nodes_removed = astar_search(problem, h)
    elapsed_time = time.time() - start_time
    print("Run time: " + str(elapsed_time) + "s")
    print("Number of tiles moved: " + str(sol_length))
    print("Number of nodes removed from frontier: " + str(num_nodes_removed))


def manhattan_distance(self, node):
    """Gets the sum of manhattan distance of all tiles in the puzzle"""
    return 0


def max_h(self, node):
    return max(self.h, self.manhattan_distance)


# test for eight puzzle
EightPuzzle.manhattan_distance = manhattan_distance
EightPuzzle.max_h = max_h
print("----------------------\n" +
      "| EIGHT PUZZLE TESTS |\n" +
      "----------------------")
puzzle_list = []
for i in range(10):
    puzzle_list.append(make_rand_8puzzle()) 

show_problemset_stats(puzzle_list)
print()


class DuckPuzzle(EightPuzzle):
    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square < 2 or 3 < index_blank_square < 6:
            possible_actions.remove('UP')
        if index_blank_square == 2 or index_blank_square > 5:
            possible_actions.remove('DOWN')
        if index_blank_square in [1, 5, 8]:
            possible_actions.remove('RIGHT')
        if index_blank_square in [0, 2, 6]:
            possible_actions.remove('LEFT')

        return possible_actions

    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)

        up_delta = -2
        down_delta = 2
        if blank > 5:
            up_delta = -3
        elif blank > 2:
            down_delta = 3

        delta = {'UP': up_delta, 'DOWN': down_delta, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank],  new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def manhattan_distance(self, node):
        return 0
    

def make_rand_duckpuzzle():
    """ Creates a random duck puzzle by scrambling from its solved state. 
    As a result, instances of duck puzzle created by this function 
    will always be solvable"""
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    state = goal
    puzzle = DuckPuzzle(goal)
    num_shuffles = 1000
    previous_action = None
    for i in range(num_shuffles):
        actions = puzzle.actions(state)
        # make sure puzzle doesn't go back to the previous state
        if i > 0:
            actions.remove(get_undo_action(previous_action))
        action = random.choice(actions)
        state = puzzle.result(state, action)
        previous_action = action

    return DuckPuzzle(state)


def get_undo_action(action):
    if action == 'UP':
        return 'DOWN'
    elif action == 'DOWN':
        return 'UP'
    elif action == 'RIGHT':
        return 'LEFT'
    elif action == 'LEFT':
        return 'RIGHT'
    
    return None


def display_duckpuzzle(state):
    result = ""
    for i in range(9):
        if i == 6:
            result += "  "
        if state[i] == 0:
            result += '*'
        else:
            result += str(state[i])
        if i in [1, 5]:
            result += '\n'
        else:
            result += ' '
        
    print(result)


# "Duck Puzzle" tests
DuckPuzzle.max_h = max_h
print("---------------------\n" +
      "| DUCK PUZZLE TESTS |\n" +
      "---------------------")
puzzle_list = []
for i in range(10):
    puzzle_list.append(make_rand_duckpuzzle()) 

show_problemset_stats(puzzle_list, display_duckpuzzle)
