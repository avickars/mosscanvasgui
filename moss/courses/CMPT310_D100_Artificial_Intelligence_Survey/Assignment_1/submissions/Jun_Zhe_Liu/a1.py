from search import *
from random import randrange
from enum import Enum
import time
# generate list of randomized permutation of 0 to 9. this list must represent a solvable EightPuzzle


def make_rand_8puzzle(scramble_move_count=500):
    current_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    rand_puzzle = EightPuzzle(current_state)
    for moves in range(scramble_move_count):
        allowed_actions = rand_puzzle.actions(current_state)
        action = allowed_actions[randrange(len(allowed_actions))]
        current_state = rand_puzzle.result(current_state, action)
    return current_state


def display(state):
    for i in range(9):
        if state[i] == 0:
            print("* ", end='')
        else:
            print("{} ".format(state[i]), end='')
        if i % 3 == 2:
            print('\n', end='')


def misplaced_metric(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return sum(s != g for (s, g) in zip(node.state, goal))


def max_manhattan_misplaced(node):
    return max(manhattan_metric(node), misplaced_metric(node))


def manhattan_metric(node):
    metric_sum = 0
    # index: current position
    # val: calculate offset
    for tile_index, val in enumerate(node.state, start=0):
        if val != 0:
            target_index = val - 1
            target_x = target_index % 3
            target_y = target_index // 3 # integer division
            tile_x = tile_index % 3
            tile_y = tile_index // 3
            metric_sum += abs(tile_x - target_x) + abs(tile_y - target_y)
    return metric_sum


class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions.remove('UP')
            possible_actions.remove('LEFT')
        if index_blank_square == 1:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        # all moves possible for index 3
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        blank_pos = self.find_blank_square(state)
        new_state = list(state)
        delta = 999  # throw through out of index if error in condition checking
        if action == 'LEFT':
            delta = -1
        elif action == 'RIGHT':
            delta = 1
        elif action == 'UP':
            if 2 <= blank_pos < 4:
                delta = -2
            elif 6 <= blank_pos < 9:
                delta = -3
        elif action == 'DOWN':
            if 0 <= blank_pos < 2:
                delta = 2
            elif 3 <= blank_pos < 6:
                delta = 3

        neighbor = blank_pos + delta
        new_state[blank_pos], new_state[neighbor] = new_state[neighbor], new_state[blank_pos]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    # skip check_solvability


def make_rand_duck_puzzle(scramble_move_count=100):
    current_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    rand_puzzle = DuckPuzzle(current_state)
    for moves in range(scramble_move_count):
        allowed_actions = rand_puzzle.actions(current_state)
        action = allowed_actions[randrange(len(allowed_actions))]
        current_state = rand_puzzle.result(current_state, action)
    return current_state

# ignore these
#
# def duck_manhattan_metric(node):
#     metric_sum = 0
#
#     # treat puzzle like 4x3 for dx and dy calculation
#     for tile_index, val in enumerate(node.state, start=0):
#         target_position = -1
#         if 0 < val <= 2:
#             target_position = val - 1
#         if 2 < val <= 6:
#             target_position = val + 1
#         if val > 7:
#             target_position = val + 2
#
#         if val != 0:
#             target_x = target_position % 4
#             target_y = target_position // 3  # integer division
#             tile_x = tile_index % 4
#             tile_y = tile_index // 3
#             metric_sum += abs(tile_x - target_x) + abs(tile_y - target_y)
#     return metric_sum
#
#
# def duck_misplaced_metric(node):
#     goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
#     return sum(s != g for (s, g) in zip(node.state, goal))
#
#
# def duck_max_manhattan_misplaced(node):
#     return max(duck_manhattan_metric(node), duck_misplaced_metric(node))

class PuzzleType(Enum):
    EIGHT_PUZZLE = 1
    DUCK_PUZZLE = 2


def test_puzzle(puzzle_set, heuristic_fn, puzzle_type):
    result_statistics = []  # list of maps
    for puzzle in puzzle_set:
        puzzle_instance = None
        if puzzle_type == PuzzleType.EIGHT_PUZZLE:
            puzzle_instance = EightPuzzle(puzzle)
        elif puzzle_type == PuzzleType.DUCK_PUZZLE:
            puzzle_instance = DuckPuzzle(puzzle)

        start_time = time.time()
        result = astar_search(puzzle_instance, heuristic_fn)  # do not show statistics from search.py
        elapsed_time = time.time() - start_time

        if result is None:
            raise Exception("Solution for puzzle not found")  # if puzzle is invalid
        else:
            statistic = {'time': elapsed_time, 'solution_length': len(result.solution()), 'pop_count': result.pop_count}
            result_statistics.append(statistic)
    return result_statistics


rand_eight_puzzles = []
for i in range(10):
    rand_eight_puzzles.append(make_rand_8puzzle())

rand_duck_puzzles = []
for i in range(10):
    rand_duck_puzzles.append(make_rand_duck_puzzle())


def format_results(results):
    print("puzzle\ttime\tsolution\tpop_count")
    for index, result in enumerate(results, start=1):

        print("{},\t{:.6f},\t{},\t\t\t{}".
              format(index,
                     round(result['time'], 6),
                     result['solution_length'],
                     result['pop_count']
                     ))


def main():
    for eight_puzzle in rand_eight_puzzles:
        display(eight_puzzle)
        print()

    misplaced_test_results_eight = test_puzzle(rand_eight_puzzles, misplaced_metric, PuzzleType.EIGHT_PUZZLE)
    manhattan_test_results_eight = test_puzzle(rand_eight_puzzles, manhattan_metric, PuzzleType.EIGHT_PUZZLE)
    max_test_results_eight = test_puzzle(rand_eight_puzzles, max_manhattan_misplaced, PuzzleType.EIGHT_PUZZLE)
    format_results(misplaced_test_results_eight)
    format_results(manhattan_test_results_eight)
    format_results(max_test_results_eight)

    for duck_puzzle in rand_duck_puzzles:
        display(duck_puzzle)
        print()

    misplaced_test_results_duck = test_puzzle(rand_duck_puzzles, misplaced_metric, PuzzleType.DUCK_PUZZLE)
    manhattan_test_results_duck = test_puzzle(rand_duck_puzzles, manhattan_metric, PuzzleType.DUCK_PUZZLE)
    max_test_results_duck = test_puzzle(rand_duck_puzzles, max_manhattan_misplaced, PuzzleType.DUCK_PUZZLE)
    format_results(misplaced_test_results_duck)
    format_results(manhattan_test_results_duck)
    format_results(max_test_results_duck)


main()
