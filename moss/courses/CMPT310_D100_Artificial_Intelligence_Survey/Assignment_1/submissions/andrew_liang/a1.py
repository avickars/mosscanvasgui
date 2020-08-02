# a1.py
from search import *
import time


class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
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
        """0 1
           2 3 4 5
             6 7 8      index table"""
        #  remove actions base on index table above
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')

        if index_blank_square == 0 or index_blank_square == 1 \
                or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')

        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')

        if index_blank_square == 2 or index_blank_square == 6 \
                or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        temp_up = 0
        temp_down = 0
        #   action up for 6,7,8
        if blank == 6 or blank == 7 or blank == 8:
            temp_up = -3
        #   action up for 2,3
        if blank == 2 or blank == 3:
            temp_up = -2

        #   action down for 3,4,5
        if blank == 3 or blank == 4 or blank == 5:
            temp_down = 3
        #   action down for 0,1
        if blank == 0 or blank == 1:
            temp_down = 2

        delta = {'UP': temp_up, 'DOWN': temp_down, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def h2(self, node):
        """ Return the heuristic value for a given state. this new heuristic function used is
        h(n) =  Manhattan distance from current state to goal state"""

        goal_coordinates = {0: [2, 3], 1: [0, 0], 2: [0, 1],
                            3: [1, 0], 4: [1, 1], 5: [1, 2],
                            6: [1, 3], 7: [2, 1], 8: [2, 2]}

        manhatton_distance = 0
        current_position = 1
        # abjust the current position so the loop start from 1:[0][0] to 8:[2][2]
        for current_item in node.state:
            goal_x, goal_y = goal_coordinates[current_item]
            current_x, current_y = goal_coordinates[current_position]

            manhatton_distance += abs(current_x - goal_x) + abs(current_y - goal_y)

            if current_position != 8:  # stop at index 8
                current_position += 1

        # finish the final 0[2][2] which has skipped above
        goal_x, goal_y = goal_coordinates[node.state[8]]  # final state object
        current_x, current_y = goal_coordinates[0]  # 0[2][2]
        manhatton_distance += abs(current_x - goal_x) + abs(current_y - goal_y)

        return manhatton_distance

    def h3(self, node):
        """ Return the heuristic value for a given state. this new heuristic function used is
        h(n) =  Manhattan distance from current state to goal state + misplaced tile heuristic """

        goal = {0, 1, 2, 3, 4, 5, 6, 7, 8}
        manhatton_distance = h2(node)
        return manhatton_distance + sum(s != g for (s, g) in zip(node.state, goal))


def make_rand_duckpuzzle(init_state):
    state = init_state
    puzzle = DuckPuzzle(tuple(init_state))
    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    actions = []
    #  move the duck puzzle with random action
    for _ in range(1000000):
        actions.append(random.choice(possible_actions))

    for action in actions:
        if action in puzzle.actions(state):
            state = list(puzzle.result(state, action))

    return tuple(state)  # return the new state


# display duck puzzle
def display_duckpuzzle(state):
    length = len(state)
    for i in range(length):
        if state[i] == 0:
            print("*", end=' ')  # print * when 0
        else:
            print(state[i], end=' ')

        if i == 1:  # break line after 2nd element
            print()
        if i == 5:  # break line after 2nd element
            print()
            print(end='  ')
        if i == 8:  # break line after 2nd element
            print()


# h1
def solve_duck_h1(puzzle):
    """Solves the puzzle using a*_search with h1"""
    return astar_search(puzzle, h=puzzle.h, display=True).solution()


# h2
def solve_duck_h2(puzzle):
    """Solves the puzzle using a*_search with h2"""
    return astar_search(puzzle, h=puzzle.h2, display=True).solution()


# h3
def solve_duck_h3(puzzle):
    """Solves the puzzle using a*_search with h3"""
    return astar_search(puzzle, h=puzzle.h3, display=True).solution()


def make_rand_8puzzle(init_state):
    puzzle = EightPuzzle(tuple(init_state))
    switch = False  # true when solvable
    numbers = list(init_state)  # put initial state into list
    new_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # new state

    while not switch:
        k = 0
        while len(numbers) > 0:
            temp_num = random.randint(0, len(numbers) - 1)  # get a random index
            new_state[k] = numbers[temp_num]  # append
            k += 1  # next index
            numbers.remove(numbers[temp_num])  # remove index appended

        if puzzle.check_solvability(new_state):  # is solvable
            switch = True
        else:
            # print("false")  #  test
            numbers = list(init_state)  # put initial state into list
    return new_state  # return the new state


# display 8 puzzle
def display(state):
    length = len(state)
    for i in range(length):
        if state[i] == 0:
            print("*", end=' ')  # print * when 0
        else:
            print(state[i], end=' ')

        if (i + 1) % 3 == 0:  # break line every 3 line
            print()


# h1
def solve_h1(puzzle):
    """Solves the puzzle using a*_search with h1"""
    return astar_search(puzzle, display=True).solution()


# h2
def solve_h2(puzzle):
    """Solves the puzzle using a*_search with h2"""
    return astar_search(puzzle, h=h2, display=True).solution()


def h2(node):
    """ Return the heuristic value for a given state. this new heuristic function used is
    h(n) =  Manhattan distance from current state to goal state"""

    goal_coordinates = {0: [2, 2], 1: [0, 0], 2: [0, 1],
                        3: [0, 2], 4: [1, 0], 5: [1, 1],
                        6: [1, 2], 7: [2, 0], 8: [2, 1]}

    manhatton_distance = 0
    current_position = 1
    # abjust the current position so the loop start from 1:[0][0] to 8:[2][1]
    for current_item in node.state:
        goal_x, goal_y = goal_coordinates[current_item]
        current_x, current_y = goal_coordinates[current_position]

        manhatton_distance += abs(current_x - goal_x) + abs(current_y - goal_y)

        if current_position != 8:  # stop at index 8
            current_position += 1

    # finish the final 0[2][2] which has skipped above
    goal_x, goal_y = goal_coordinates[node.state[8]]  # final state object
    current_x, current_y = goal_coordinates[0]  # 0[2][2]
    manhatton_distance += abs(current_x - goal_x) + abs(current_y - goal_y)

    return manhatton_distance


# h3
def solve_h3(puzzle):
    """Solves the puzzle using a*_search with h3"""
    return astar_search(puzzle, h=h3, display=True).solution()


def h3(node):
    """ Return the heuristic value for a given state. this new heuristic function used is
    h(n) =  Manhattan distance from current state to goal state + misplaced tile heuristic """

    goal = {0, 1, 2, 3, 4, 5, 6, 7, 8}
    manhatton_distance = h2(node)
    return manhatton_distance + sum(s != g for (s, g) in zip(node.state, goal))


def run_3_algo_8_puzzle(state):
    display(state)
    puzzle_1 = EightPuzzle(tuple(state))

    start_time = time.time()
    solution_h1_1 = solve_h1(puzzle_1)
    elapsed_time = time.time() - start_time
    print(solution_h1_1)
    print("number of tiles moved", len(solution_h1_1))
    print(f'elapsed time (in seconds): {elapsed_time}s')

    start_time = time.time()
    solution_h2_1 = solve_h2(puzzle_1)
    elapsed_time = time.time() - start_time
    print(solution_h2_1)
    print("number of tiles moved", len(solution_h2_1))
    print(f'elapsed time (in seconds): {elapsed_time}s')

    start_time = time.time()
    solution_h3_1 = solve_h3(puzzle_1)
    elapsed_time = time.time() - start_time
    print(solution_h3_1)
    print("number of tiles moved: ", len(solution_h3_1))
    print(f'elapsed time (in seconds): {elapsed_time}s')


def run_3_algo_duck_puzzle(state):
    display_duckpuzzle(state)
    puzzle_1 = DuckPuzzle(tuple(state))

    start_time = time.time()
    solution_h1_1 = solve_duck_h1(puzzle_1)
    elapsed_time = time.time() - start_time
    #print(solution_h1_1)
    print("number of tiles moved", len(solution_h1_1))
    print(f'elapsed time (in seconds): {elapsed_time}s')

    start_time = time.time()
    solution_h2_1 = solve_duck_h2(puzzle_1)
    elapsed_time = time.time() - start_time
    #print(solution_h2_1)
    print("number of tiles moved", len(solution_h2_1))
    print(f'elapsed time (in seconds): {elapsed_time}s')

    start_time = time.time()
    solution_h3_1 = solve_duck_h3(puzzle_1)
    elapsed_time = time.time() - start_time
    #print(solution_h3_1)
    print("number of tiles moved: ", len(solution_h3_1))
    print(f'elapsed time (in seconds): {elapsed_time}s')


def initial_main():  # main

    init_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    duck_state_1 = make_rand_duckpuzzle(init_state)
    duck_state_2 = make_rand_duckpuzzle(init_state)
    duck_state_3 = make_rand_duckpuzzle(init_state)
    duck_state_4 = make_rand_duckpuzzle(init_state)
    duck_state_5 = make_rand_duckpuzzle(init_state)
    duck_state_6 = make_rand_duckpuzzle(init_state)
    duck_state_7 = make_rand_duckpuzzle(init_state)
    duck_state_8 = make_rand_duckpuzzle(init_state)
    duck_state_9 = make_rand_duckpuzzle(init_state)
    duck_state_10 = make_rand_duckpuzzle(init_state)

    print("1st state duck")
    print("_______________________________________________________________________", '\n')
    run_3_algo_duck_puzzle(duck_state_1)
    print("2nd state duck")
    print("_______________________________________________________________________", '\n')
    run_3_algo_duck_puzzle(duck_state_2)
    print("3rd state duck")
    print("_______________________________________________________________________", '\n')
    run_3_algo_duck_puzzle(duck_state_3)
    print("4th state duck")
    print("_______________________________________________________________________", '\n')
    run_3_algo_duck_puzzle(duck_state_4)
    print("5th state duck")
    print("_______________________________________________________________________", '\n')
    run_3_algo_duck_puzzle(duck_state_5)
    print("6th state duck")
    print("_______________________________________________________________________", '\n')
    run_3_algo_duck_puzzle(duck_state_6)
    print("7th state duck")
    print("_______________________________________________________________________", '\n')
    run_3_algo_duck_puzzle(duck_state_7)
    print("8th state duck")
    print("_______________________________________________________________________", '\n')
    run_3_algo_duck_puzzle(duck_state_8)
    print("9th state duck")
    print("_______________________________________________________________________", '\n')
    run_3_algo_duck_puzzle(duck_state_9)
    print("10th state duck")
    print("_______________________________________________________________________", '\n')
    run_3_algo_8_puzzle(duck_state_10)

    """state_1 = make_rand_8puzzle(init_state)
    state_2 = make_rand_8puzzle(init_state)
    state_3 = make_rand_8puzzle(init_state)
    state_4 = make_rand_8puzzle(init_state)
    state_5 = make_rand_8puzzle(init_state)
    state_6 = make_rand_8puzzle(init_state)
    state_7 = make_rand_8puzzle(init_state)
    state_8 = make_rand_8puzzle(init_state)
    state_9 = make_rand_8puzzle(init_state)
    state_10 = make_rand_8puzzle(init_state)"""

    """print("1st state")
    print("_______________________________________________________________________", '\n')
    run_3_algo_8_puzzle(state_1)
    print("2nd state")
    print("_______________________________________________________________________", '\n')
    run_3_algo_8_puzzle(state_2)
    print("3rd state")
    print("_______________________________________________________________________", '\n')
    run_3_algo_8_puzzle(state_3)
    print("4th state")
    print("_______________________________________________________________________", '\n')
    run_3_algo_8_puzzle(state_4)
    print("5th state")
    print("_______________________________________________________________________", '\n')
    run_3_algo_8_puzzle(state_5)
    print("6th state")
    print("_______________________________________________________________________", '\n')
    run_3_algo_8_puzzle(state_6)
    print("7th state")
    print("_______________________________________________________________________", '\n')
    run_3_algo_8_puzzle(state_7)
    print("8th state")
    print("_______________________________________________________________________", '\n')
    run_3_algo_8_puzzle(state_8)
    print("9th state")
    print("_______________________________________________________________________", '\n')
    run_3_algo_8_puzzle(state_9)
    print("10th state")
    print("_______________________________________________________________________", '\n')
    run_3_algo_8_puzzle(state_10)"""


initial_main()  # main
