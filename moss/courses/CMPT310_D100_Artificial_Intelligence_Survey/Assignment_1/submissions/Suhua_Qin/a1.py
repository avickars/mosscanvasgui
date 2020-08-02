# a1.py
# author: April Qin

from search import *
from random import shuffle

import time
import xlsxwriter


# This program can default generate a random 8puzzle and a random duck puzzle
# and solve them. Some puzzles might take too long to solve, please kill the program
# and re-run in those cases.


# ----------------------------------------------------------
# ----------functions COPIED FROM search.py + my modifications-----------
# ----------------------------------------------------------

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
    removedNodes = 0
    while frontier:
        node = frontier.pop()
        removedNodes += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and",
                      len(frontier), "paths remain in the frontier")
            return [node, removedNodes]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return [None,None]

def astar_search(problem, h='tile', display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    if h == 'tile':
        h = memoize(problem.h, 'h')
    if h == 'manhattan':
        h = memoize(problem.Manhattan_h, 'h')
    if h == 'max':
        h = memoize(problem.max_h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# ______________________________________________________________________________
# A* heuristics

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

        # note the actions that the white cannot take if it's at the index in the list
        remove_Up = [0, 1, 4, 5]
        remove_down = [2, 6, 7, 8]
        remove_left  = [0, 2, 6]
        remove_right = [1, 5, 8]
        
        if index_blank_square in remove_left:
            possible_actions.remove('LEFT')
        if index_blank_square in remove_Up:
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

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
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

    def Manhattan_h(self, node):
        horizontal_distance = 0
        vertical_distance = 0
        goal_positions = {1: (0,0), 2: (0,1), 3: (1,0), 4: (1,1), 5: (1,2), 6: (1,3), 7: (2,1), 8: (2,2), 0: (2,3)}
        for (s, g) in zip(node.state, self.goal):
            if s != g and s != 0:
                current_position = goal_positions[g]
                correct_position = goal_positions[s]  

                horizontal_distance += abs(correct_position[0] - current_position[0]) 
                vertical_distance += abs(correct_position[1] - current_position[1]) 

        return horizontal_distance + vertical_distance

    def max_h(self, node):
        misplaced_distance = self.h(node)
        manhattan_distance = self.Manhattan_h(node)
        return max(misplaced_distance, manhattan_distance)

# ______________________________________________________________________________



# ______________________________________________________________________________
# A* heuristics

class EightPuzzle(Problem):
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

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
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
        # print('state: ', node.state, 'goals: ', self.goal)

        # print([s != g for (s, g) in zip(node.state, self.goal)])

        # this will generate a count of mismatched pairs between the current state with
        # the goal
        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def Manhattan_h(self, node):
        horizontal_distance = 0
        vertical_distance = 0
        for (s, g) in zip(node.state, self.goal):
            if s != g:
                # since g is the goal state, if s != g, means s is misplaced.
                # think the puzzle as a 3*3 grid
                # [(g-1)//3][(g-1)%3] is the misplaced location of s
                # [(s-1)//3][(s-1)%3] is the desired location for s
                # btw, // is the operator for floor division
                # 0 at goal state is at location [2][2]
                g_row = g_col = s_row = s_col = 2
                if g != 0:
                    g_row = (g-1) // 3
                    g_col = (g-1) % 3
                if s != 0:
                    s_row = (s-1) // 3
                    s_col = (s-1) % 3
                    horizontal_distance += abs(g_row - s_row)
                    vertical_distance += abs(g_col - s_col)
        return horizontal_distance + vertical_distance

    def max_h(self, node):
        misplaced_distance = self.h(node)
        manhattan_distance = self.Manhattan_h(node)
        return max(misplaced_distance, manhattan_distance)

# ______________________________________________________________________________



# ----------------------------------------------------------
# -----------create excel-----------------------------------------------
# ----------------------------------------------------------
# ----------------------------------------------------------

def create_excel(name):
    return xlsxwriter.Workbook(name)

def create_sheet(workbook, name):
    return workbook.add_worksheet(name)

def close_excel(workbook):
    workbook.close()

def write_headers(worksheet, headers):
    col = 0
    row = 0
    for item in headers:
        worksheet.write(row, col, item)
        row += 1

def write_data(worksheet, data):
    row=0
    col=data[0]
    for value in data:
        worksheet.write(row, col, str(value))
        row += 1

def swap(array, index1, index2):
    temp = array[index1]
    array[index1] = array[index2]
    array[index2] = temp


# ----------------------------------------------------------
# ----------DUCK PUZZLE------------------------------------------------
# ----------------------------------------------------------
# ----------------------------------------------------------


def display_duckpuzzle(state):
    '''
        print state of an duck puzzle
    '''
    values = []
    
    for data in state:
        data = '*' if data == 0 else data
        values.append(data)
    print(values[0],values[1], " ")
    print(values[2],values[3], values[4], values[5])
    print(" ",values[6], values[7], values[8])


def make_random_duckPuzzle(swaps=2):
    initial_state =[1, 2, 3, 4, 5, 6, 7, 8, 0]

    for x in range(swaps):
        index1 = random.randint(0,8)
        index2 = random.randint(0,8)
        swap(initial_state, index1, index2)

    return DuckPuzzle(initial=tuple(initial_state))



# ----------------------------------------------------------
# -------------8 PUZZLE---------------------------------------------
# ----------------------------------------------------------
# ----------------------------------------------------------


def display_8puzzle(state):
    '''
        print state of an eight puzzle
    '''
    for i in range(len(state)):
        data = '*' if state[i] == 0 else state[i]
        if i > 0 and (i+1) % 3 ==0:
            print(data)
        else:
            print(data, end=" ")

def make_rand_8puzzle(swaps=2):
    '''
        create an eight puzzle with random initial state
    '''
    solvable = False
    puzzle = False
    initial_state =[1, 2, 3, 4, 5, 6, 7, 8, 0]
    
    while not solvable:
        # make swaps
        for x in range(swaps):
            index1 = random.randint(0,8)
            index2 = random.randint(0,8)
            swap(initial_state, index1, index2)
        #  create puzzle and check solvability
        puzzle = EightPuzzle(initial=tuple(initial_state))
        if puzzle.check_solvability(tuple(initial_state)):
            solvable = True

    return puzzle


# ----------------------------------------------------------
# ----------PUZZLE SOLVER------------------------------------------------
# ----------------------------------------------------------
# ----------------------------------------------------------

def astar_puzzle_solver(problem, heuristic='tile'):
    print('\n ***  ', heuristic, ' ***  ')
    start_time = time.time()
    result, removedNodes = astar_search(problem, heuristic, display=True)
    elapsed_time = time.time() - start_time
    solution_len = 'No Solution'
    if result:
        solution_len = result.path_cost
    else:
        print(f'None returned from A* {heuristic} search. problem not solvable')

    return [elapsed_time, solution_len, removedNodes]


def solve_puzzle(puzzle_name, puzzle_list, heuristic_list):
    wb = create_excel('as1_'+puzzle_name+'.xlsx')

    for h in heuristic_list:
        ws = create_sheet(wb, h)
        write_headers(ws, ['Problem', 'Initial_state', 'Run Time (s)', 'Solution Length', 'Nodes Removed'])
        for x in range(len(puzzle_list)):
            if puzzle_name == '8Puzzle':
                display_8puzzle(puzzle_list[x].initial)
            elif puzzle_name == 'duckPuzzle':
                display_duckpuzzle(puzzle_list[x].initial)

            elapsed_time, path_cost, removedNodes=astar_puzzle_solver(puzzle_list[x], h)
            data = [x+1, puzzle_list[x].initial, elapsed_time, path_cost, removedNodes]
            write_data(ws, data)
            
            print(f'elapsed time (in seconds): {elapsed_time}s')
            print(f'solution_length: {path_cost}')
            print(f'removedNodes: {removedNodes}')

    close_excel(wb)


# ----------------------------------------------------------
# ----------MAIN------------------------------------------------
# ----------------------------------------------------------
# ----------------------------------------------------------


def main():
    # eight_Puzzles = []
    # duck_puzzles = []

    # number_of_puzzles = 10

    # for x in range(number_of_puzzles):
    #     eight_Puzzles.append(make_rand_8puzzle(1))
    #     duck_puzzles.append(make_random_duckPuzzle(1))

    
    puzzles = ['8Puzzle', 'duckPuzzle']
    heuristic = [ 'tile', 'manhattan', 'max' ]


    # create 1 duck puzzle and 1 8 puzzle to solve
    duck_puzzles = [make_random_duckPuzzle()]
    eight_Puzzles = [make_rand_8puzzle()]


    # puzzle = make_rand_8puzzle()
    # duck_puzzles = [puzzle]
    # eight_Puzzles = [puzzle]

    solve_puzzle(puzzles[0], eight_Puzzles, heuristic)
    solve_puzzle(puzzles[1], duck_puzzles, heuristic)


if __name__ == "__main__":
    main()









