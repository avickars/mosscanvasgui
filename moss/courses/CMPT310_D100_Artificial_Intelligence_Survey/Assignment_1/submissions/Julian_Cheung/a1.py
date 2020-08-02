# a1.py
from search import *
import time

#--------------------------------- q1 ---------------------------------
def make_rand_8puzzle(state):
    # state=tuple(random.sample(range(9), 9))
    # state= (1,2,3,4,0,5,6,7,8)
    # state = (7,2,4,5,0,6,8,3,1)
    puzzle = EightPuzzle(state)
    
    while not puzzle.check_solvability(state):
        state=tuple(random.sample(range(9), 9))
        puzzle = EightPuzzle(state)
    
    print(state)
    display(state)
    print(puzzle.check_solvability(state))

    return puzzle

def display(state):
    state=list(state)
    for i in range(len(state)):
        if state[i] == 0:
            state[i] = '*'

    print(*state[0:3], sep=' ')
    print(*state[3:6], sep=' ')
    print(*state[6:9], sep=' ')

#--------------------------------- q2 ---------------------------------
#misplaced tile heuristic
def misplaced_tile(problem):
    # problem = make_rand_8puzzle()
    res = astar_search(problem, problem.h, True)
    print("Length of solution: " , res.path_cost)


#manhattan distance heurisitic function
#node.state is a tuple
def manhattan_distance_heuristic(node):
    current_state = node.state
    distance = 0

    for i in range(0, 9):
        current = current_state[i]
        if current != i+1 and current != 0:
            prev_row = int(i/3)
            prev_col = i%3
            goal_row = int(current/3)
            goal_col = current%3
            distance += abs(prev_row-goal_row) + abs(prev_col - goal_col)

    return distance

#manhattan distance heurisitic result
def manhattan_distance_result(problem):
    # problem = make_rand_8puzzle()
    res = astar_search(problem, manhattan_distance_heuristic, True)
    print("Length of solution: " , res.path_cost)

#max of misplaced tile heurisitic and manhattan distance heurisitic
def max_heuristic(problem):
    misplaced_res = astar_search(problem, problem.h, True)
    manhattan_res = astar_search(problem, manhattan_distance_heuristic, True)
    res = max(misplaced_res, manhattan_res)
    print("Length of solution: " , res.path_cost)
    return res


def q2(problem):
    start_time = time.time()
    misplaced_tile(problem)
    elapsed_time = time.time() - start_time
    print(f'misplaced tile heuristic elapsed time (in seconds): {elapsed_time}s')

    start_time = time.time()
    manhattan_distance_result(problem)
    elapsed_time = time.time() - start_time
    print(f'manhattan distance heuristic elapsed time (in seconds): {elapsed_time}s')

    start_time = time.time()
    max_heuristic(problem)
    elapsed_time = time.time() - start_time
    print(f'max of misplaced tile heuristic and manhattan distance heuristic elapsed time (in seconds): {elapsed_time}s')
    # print('max of misplaced tile heuristic and manhattan distance heuristic', max_heuristic(problem))

    
#--------------------------------- q3 ---------------------------------
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

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
        remove_left = [0, 2, 6]
        remove_right = [1, 5, 8]
        remove_up = [0, 1, 4, 5]
        remove_down = [2, 6, 7, 8]

        if index_blank_square in remove_left:
            possible_actions.remove('LEFT')
        if index_blank_square in remove_up:
            possible_actions.remove('UP')
        if index_blank_square in remove_right:
            possible_actions.remove('RIGHT')
        if index_blank_square in remove_down:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta = {'LEFT': -1, 'RIGHT': 1}

        if blank < 2:
            delta['DOWN'] = 2
        else:
            delta['DOWN'] = 3
        
        if blank > 5:
            delta['UP'] = -3
        else:
            delta['UP'] = -2

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

def randomize_duck_puzzle(problem):

    state = problem.initial
    possible_actions = problem.actions(state)
    random_action = possible_actions[random.randint(0, len(possible_actions)-1)]
    return problem.result(state, random_action)
    # print(random_action)


def display_q3(state):
    state=list(state)
    for i in range(len(state)):
        if state[i] == 0:
            state[i] = '*'

    print(*state[0:2], sep=' ')
    print(*state[2:6], sep=' ')
    print(" " , *state[6:9], sep=' ')



# q2 execute
# for i in range(10):
#     state = tuple(random.sample(range(9), 9))
#     problem = make_rand_8puzzle(state)
#     q2(problem)
#     print('-----------------')


# q3 execute
state= (1,2,3,4,5,6,7,8,0)

duck_puzzle = DuckPuzzle(state)


for j in range(10):
    #random duck puzzle
    for i in range(1500):
        state = randomize_duck_puzzle(duck_puzzle)
        duck_puzzle = DuckPuzzle(state)
    display_q3(state)

    q2(duck_puzzle)
    print('-----------------')