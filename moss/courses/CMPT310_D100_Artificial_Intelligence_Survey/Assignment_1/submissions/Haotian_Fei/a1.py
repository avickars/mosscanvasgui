# a1.py

from search import *
from random import shuffle, sample
import time

# Precomputed manhattan distance
eight_puzzle_distance_table = [
    4,3,2,3,2,1,2,1,0,
    0,1,2,1,2,3,2,3,4,
    1,0,1,2,1,2,3,2,3,
    2,1,0,3,2,1,4,3,2,
    1,2,3,0,1,2,1,2,3,
    2,1,2,1,0,1,2,1,2,
    3,2,1,2,1,0,3,2,1,
    2,3,4,1,2,3,0,1,2,
    3,2,3,2,1,2,1,0,1,
]

duck_puzzle_distance_table = [
    5,4,4,3,2,1,2,1,0,
    0,1,1,2,3,4,3,4,5,
    1,0,2,1,2,3,2,3,4,
    1,2,0,1,2,3,2,3,4,
    2,1,1,0,1,2,1,2,3,
    3,2,2,1,0,1,2,1,2,
    4,3,3,2,1,0,3,2,1,
    3,2,2,1,2,3,0,1,2,
    4,3,3,2,1,2,1,0,1
]

# For test use
eight_puzzle_instance = [
    EightPuzzle(tuple([1,8,2,0,4,3,7,6,5])),
    EightPuzzle(tuple([8,1,3,4,0,2,7,6,5]))
]

# Duck Puzzle related

class DuckPuzzle(Problem):
    possible_destination = [
        [1, 2],
        [0, 3],
        [0, 3],
        [1, 2, 4, 6],
        [3, 5, 7],
        [4, 8],
        [3, 7],
        [4, 6, 8],
        [5, 7]
    ]
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        index_blank_square = self.find_blank_square(state)

        return DuckPuzzle.possible_destination[index_blank_square]

    def result(self, state, destination):
        blank = self.find_blank_square(state)
        new_state = list(state)
        new_state[blank], new_state[destination] = new_state[destination], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

def generate_solvable_duck_puzzles():
    initial_state = (1,2,3,4,5,6,7,8,0)
    problem = DuckPuzzle(initial_state, (0,0,0,0,0,0,0,0,0))
    solvable_puzzles = set()
    frontier = [initial_state]

    while frontier:
        node = frontier.pop()
        if node not in solvable_puzzles:
            solvable_puzzles.add(node)

            for action in problem.actions(node):
                frontier.append(problem.result(node, action))

    return list(solvable_puzzles)

def manhattan_distance_duck_puzzle(node):
    result = 0
    for index, val in enumerate(node.state):
        result += duck_puzzle_distance_table[val * 9 + index]
    return result

def solve_duck_puzzles(k):
    solvable_puzzles = generate_solvable_duck_puzzles()
    random_puzzles = sample(solvable_puzzles, k)
    for ramdom_puzzle in random_puzzles:
        display(ramdom_puzzle)
        random_problem = DuckPuzzle(ramdom_puzzle)
        astar_default(random_problem)
        astar_manhattan(random_problem, manhattan_distance_duck_puzzle)
        astar_max(random_problem, manhattan_distance_duck_puzzle)


# Eight Puzzle Related

def make_rand_8puzzle():
    state = list(range(0,9))
    check_instance = EightPuzzle(tuple(state))

    while True:
        shuffle(state)
        if check_instance.check_solvability(state):
            return EightPuzzle(tuple(state))

def manhattan_distance_eight_puzzle(node):
    result = 0
    for index, val in enumerate(node.state):
        result += eight_puzzle_distance_table[val * 9 + index]
    return result

def solve_eight_puzzles(k):
    random_problems = [make_rand_8puzzle() for _ in range(0, k)]
    for random_problem in random_problems:
        display(random_problem.initial)
        astar_default(random_problem)
        astar_manhattan(random_problem, manhattan_distance_eight_puzzle)
        astar_max(random_problem, manhattan_distance_eight_puzzle)



# General utilities
def display(state):
    index = 0
    display_string = ""

    while index < 9:
        next_target = str(state[index])
        if state[index] == 0:
            next_target = '*'

        if index %3 == 2 and index != 8:
            display_string += next_target + '\n'
        elif index == 8:
            display_string += next_target
        else:
            display_string += next_target + ' '

        index += 1

    print(display_string)

def solver_timer_wrapper(test_func):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        final_state = test_func(*args)
        running_time = time.time() - start_time

        print(f'running time (in seconds): {running_time}s')
        if final_state:
            print(f'depth: {final_state.depth}')
        else:
            print('this instance isn\'t solvable')
    return wrapper

@solver_timer_wrapper
def astar_default(problem):
    return astar_search(problem, None, True)

@solver_timer_wrapper
def astar_manhattan(problem, manhattan_distance):
    return astar_search(problem, manhattan_distance, True)

@solver_timer_wrapper
def astar_max(problem, manhattan_distance):
    return astar_search(problem, lambda n: max(manhattan_distance(n), problem.h(n)), True)

# if __name__ == "__main__":
#     solve_duck_puzzles(10)
