###                                                                          ###
###          ██████ ███    ███ ██████  ████████ ██████   ██  ██████          ###
###         ██      ████  ████ ██   ██    ██         ██ ███ ██  ████         ###
###         ██      ██ ████ ██ ██████     ██     █████   ██ ██ ██ ██         ###
###         ██      ██  ██  ██ ██         ██         ██  ██ ████  ██         ###
###          ██████ ██      ██ ██         ██    ██████   ██  ██████          ###
###                                                                          ###

### ###         Artificial Intelligence Survey :: Homework 01            ### ###
###                                                                          ###
###                                                                          ###
###        Team Member[s]:     Ian Carlsen                                   ###
###        Student Number[s]:  3012-74353                                    ###
###        Student Email[s]:   ian_carlsen [at] sfu [dot] ca                 ###
###                                                                          ###
###        submission[s]   [x] a1.py                                         ###
###                        [ ] a1.xlsx                                       ###
###                                                                          ###
### ######################################################################## ###


from search import EightPuzzle, Problem, astar_search

import random
import time
import csv

#
#
#
### ___________________________________________________________________________
def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""

    #create varialbe to count the number of Nodes removed
    nodes_removed = 0

    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        nodes_removed = nodes_removed + 1

        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            
            return node, node.path_cost, nodes_removed
            #return node

        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
        nodes_removed = nodes_removed + len(node.expand(problem)) - 1
    return None

#
#
#
### ___________________________________________________________________________
class EightPuzzle_hwk01(EightPuzzle):

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))
    
    def manhattan_heuristic(self, node):
        """ Return the Manhattan Heuristic value for a given state. """

        board  = node.state
        goal   = self.goal
        result = 0

        for i in range(0, 9):
            if board[i] != 0:
                b      = board.index(i)
                g      = goal.index(i)
                result = result + (abs(b % 3 - g % 3) + abs(b // 3 - g // 3))

        return result

    def maximum(self,node):
        """ Return the maximum h(n) value between the default Replaced Tile Heuristic, 
        and the Manhattan Heuristic."""

        h1 = self.h(node)
        h2 = self.manhattan_heuristic(node)

        if h1 > h2:
            return h1

        else:
            return h2

        

#
#
#
### ___________________________________________________________________________
class DuckPuzzle_hwk01(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)
        # Indecies      Goal
        # ┌─┬─┐         ┌─┬─┐
        # │0│1│         │1│2│
        # ├─┼─┼─┬─┐     ├─┼─┼─┬─┐
        # │2│3│4│5│     │3│4│5│6│
        # └─┼─┼─┼─┤     └─┼─┼─┼─┤
        #   │6│7│8│       │7│8│█│
        #   └─┴─┴─┘       └─┴─┴─┘

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
        
        impossible_action_up    = [0,1,4,5]
        impossible_action_left  = [0,2,6]
        impossible_action_right = [1,5,8]
        impossible_action_down  = [2,6,7,8]

        # ┌─┬─┐
        # │█│█│
        # ├─┼─┼─┬─┐
        # │ │ │█│█│
        # └─┼─┼─┼─┤
        #   │ │ │ │
        #   └─┴─┴─┘
        if impossible_action_up.count(index_blank_square) > 0:
            possible_actions.remove('UP')

        # ┌─┬─┐
        # │█│ │
        # ├─┼─┼─┬─┐
        # │█│ │ │ │
        # └─┼─┼─┼─┤
        #   │█│ │ │
        #   └─┴─┴─┘
        if impossible_action_left.count(index_blank_square) > 0:
            possible_actions.remove('LEFT')

        # ┌─┬─┐
        # │ │█│
        # ├─┼─┼─┬─┐
        # │ │ │ │█│
        # └─┼─┼─┼─┤
        #   │ │ │█│
        #   └─┴─┴─┘
        if impossible_action_right.count(index_blank_square) > 0:
            possible_actions.remove('RIGHT')

        # ┌─┬─┐
        # │ │ │
        # ├─┼─┼─┬─┐
        # │█│ │ │ │
        # └─┼─┼─┼─┤
        #   │█│█│█│
        #   └─┴─┴─┘
        if impossible_action_down.count(index_blank_square) > 0:
            possible_actions.remove('DOWN')

        return possible_actions


    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta = {
            
            
        # ┌──┬──┐
        # │  │  │
        # ├──┼──┼──┬──┐
        # │−2│−2│−2│−2│
        # └──┼──┼──┼──┤
        #    │−3│−3│−3│
        #    └──┴──┴──┘
        'UP':     (-3 if blank >= 6 else -2), 

        # ┌──┬──┐
        # │ 2│ 2│
        # ├──┼──┼──┬──┐
        # │  │ 3│ 3│ 3│
        # └──┼──┼──┼──┤
        #    │  │  │  │  
        #    └──┴──┴──┘
        'DOWN':   ( 3 if blank >= 3 else  2),

        # ┌──┬──┐
        # │  │−1│
        # ├──┼──┼──┬──┐
        # │  │−1│−1│−1│
        # └──┼──┼──┼──┤
        #    │  │−1│−1│
        #    └──┴──┴──┘ 
        'LEFT':    -1, 

        # ┌──┬──┐
        # │ 1│  │
        # ├──┼──┼──┬──┐
        # │ 1│ 1│ 1│  │
        # └──┼──┼──┼──┤
        #    │ 1│ 1│  │
        #    └──┴──┴──┘ 
        'RIGHT':    1}

        
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
    
    def manhattan_heuristic(self, node):
        """ Return the Manhattan Heuristic value for a given state. """

        board  = node.state
        goal   = self.goal
        result = 0

        for i in range(0, 9):
            if board[i] != 0:
                b      = board.index(i)
                g      = goal.index(i)
                result = result + (abs(b % 3 - g % 3) + abs(b // 3 - g // 3))

        return result

    def maximum(self,node):
        """ Return the maximum h(n) value between the default Replaced Tile Heuristic, 
        and the Manhattan Heuristic."""

        h1 = self.h(node)
        h2 = self.manhattan_heuristic(node)

        if h1 > h2:
            return h1

        else:
            return h2

#
#
#
### ___________________________________________________________________________
def make_rand_8puzzle(goal):

    l_finished_board = list(goal)

    while True:
        # uses the random.shuffle() function to randomize the goal state, then
        # use check_solvability() to continue
        random.shuffle(l_finished_board)

        l_new_board = l_finished_board
        state      = tuple(l_new_board)
        puzzle     = EightPuzzle_hwk01(state)
        IsSolvable = puzzle.check_solvability(state)

        if IsSolvable:
            display(state)
                # display new board configuration
            break

    return puzzle 


#
#
#
### ___________________________________________________________________________
def make_rand_duck_puzzle(goal):
    """Return a random initial state that is solvable"""

    duck_puzzle = DuckPuzzle_hwk01(goal)
    for i in range(1000):
        # Compelte 1000 random moves starting with the goal state 
        # to 'effectively' randomize the board.
        # Since check_solvability() is not available, 
        # by acting on a complete board randomly with only valid moves, 
        # we can ensure thats the resule will be solvable.

        random_action   = duck_puzzle.actions(goal)
        i_action        = random.randint(0,len(random_action)-1)
        randomAction    = random_action[i_action]
        new_duck_puzzle = duck_puzzle.result(goal,randomAction)

    duck_puzzle.initial = new_duck_puzzle
    duck_puzzle.state   = new_duck_puzzle
    duck_puzzle.goal    = goal
    
    duck_display(new_duck_puzzle)
        # display new board configuration

    return duck_puzzle

#
#
#
### ___________________________________________________________________________
def display(state):
    """
    display(state) will print a graphical representation of the current EightPuzzle board configuration
    
    ex. 
    
    1 2 3
    4 5 6
    7 8 0
    """
    i = state.index(0)
    l_new_board = list(state)
    l_new_board[i] = "*"
    state = tuple(l_new_board)

    print(state[0] , " " , state[1] , " " , state[2] )
    print(state[3] , " " , state[4] , " " , state[5] )
    print(state[6] , " " , state[7] , " " , state[8], '\n' )

#
#
#
# _____________________________________________________________________________
def duck_display(state):
    """
    duck_display(state) will print a graphical representation of the current DuckPuzzle board configuration
    
    ex. 
    
    1 2 
    3 4 5 6
      7 8 0
    """
    i = state.index(0)
    l_new_board = list(state)
    l_new_board[i] = "*"
    state = tuple(l_new_board)

    print( state[0], " "     , state[1] )
    print( state[2], " "     , state[3], " "     , state[4], " "     , state[5])
    print( " "     , " "     , state[6], " "     , state[7], " "     , state[8], '\n' )


#
#
#
### ___________________________________________________________________________
PRINT_ALL = 0
    # PRINT_ALL: variable to control console printing
    
goal = ( 1, 2, 3, 4, 5, 6, 7, 8, 0 )
    # goal: The configuration of board tiles that indicates a 'complete' game.

NUM_BOARDS = 1
    # NUM_BOARDS: the number of  independantly randomized board configurations to run for each puzzle type.

with open('eight_results.csv', mode='w',newline='')as outfile:
    results_writer = csv.writer(outfile)
    results_writer.writerow(['Board #', 'Algorithm #', 'Trial #', 'Duration [s]', 'Nodes Removed', 'Nodes Removed (length)'])
    # will open and overwrite a file called 'eight_results.csv', and load column names.
    # 'eight_results.csv' will be used to store data to compare the durations of each algorithm and board configuration.
    
with open('duck_results.csv', mode='w',newline='')as outfile:
    results_writer = csv.writer(outfile)
    results_writer.writerow(['Board #', 'Algorithm #', 'Trial #', 'Duration [s]', 'Nodes Removed', 'Nodes Removed (length)'])
    # will open and overwrite a file called 'duck_results.csv', and load column names.
    # 'duck_results.csv' will be used to store data to compare the durations of each algorithm and board configuration.

with open('eight_boards.csv', mode='w',newline='')as boards_outfile:
    boards_writer = csv.writer(boards_outfile)
    boards_writer.writerow(['Board #', 'Initial State'])
    # will open and overwrite a file called 'eight_boards.csv', and load column names.
    # 'eight_boards.csv' will store the board configurations relating to the BoardId foreign key.
   
with open('duck_boards.csv', mode='w',newline='')as boards_outfile:
    boards_writer = csv.writer(boards_outfile)
    boards_writer.writerow(['Board #', 'Initial State'])
    # will open and overwrite a file called 'eight_results.csv', and load column names.
    # 'duck_boards.csv' will store the board configurations relating to the BoardId foreign key.
#
#
#                           
#  _. _ |_ |_   _    _ _ | _ 
# (-|(_)| )|___|_)|_|/_/_|(- 
#    _/        |             
### ___________________________________________________________________________
for i in range(1, NUM_BOARDS+1,1):

    


    eight_puzzle = make_rand_8puzzle(goal)


    with open('eight_boards.csv', mode='a',newline='')as eightpuzzle_boards_outfile:
        eightpuzzle_boards_writer = csv.writer(eightpuzzle_boards_outfile)
        eightpuzzle_boards_writer.writerow([i, eight_puzzle.initial])

    problem_title    = "A*-Search"
    #print(problem_title)

    trials = 1

    for k in range(1,trials+1,1):

        #
        #
        #
        # p02.1
        problem_subtitle = "Manhattan Distance Heuristic"
        print("|-- ", problem_subtitle)

 
        time_start      = time.time()
        eight_solution = astar_search(eight_puzzle, eight_puzzle.manhattan_heuristic)
        time_duration   = time.time() - time_start

        print("|   |-- the total running time: ", '%.2f'%time_duration, "s.")
        print("|   |-- the length (i.e. number of tiles moved): ",            eight_solution[1])
        print("|   |-- that total number of nodes removed (from frontier): ", eight_solution[2])
        print("|   ")
 
        j = 1
        with open('eight_results.csv', mode='a',newline='') as results_outfile:
            results_writer = csv.writer(results_outfile)
            results_writer.writerow([i, j, k, time_duration, eight_solution[1], eight_solution[2]])
        #print( i, ", ", j, ", ", k)

        #
        #
        #
        # p02.2
        problem_subtitle = "Misplaced Tile Heuristic"
        print("|-- ", problem_subtitle)

        time_start      = time.time()
        eight_solution = astar_search(eight_puzzle)
        time_duration   = time.time() - time_start

        print("|   |-- the total running time: ", '%.2f'%time_duration, "s.")
        print("|   |-- the length (i.e. number of tiles moved): ",            eight_solution[1])
        print("|   |-- that total number of nodes removed (from frontier): ", eight_solution[2])
        print("|   ")

        j = 2
        with open('eight_results.csv', mode='a',newline='') as results_outfile:
            results_writer = csv.writer(results_outfile)
            results_writer.writerow([i, j, k, time_duration, eight_solution[1], eight_solution[2]])
        #print( i, ", ", j, ", ", k)

        #
        #
        #
        # p02.3
        problem_subtitle = "Max of Misplaced Tile and Manhattan Distance Heuristics"
        print("|-- ", problem_subtitle)


        time_start      = time.time()
        eight_solution = astar_search(eight_puzzle, eight_puzzle.maximum)
        time_duration   = time.time() - time_start

        print("|   |-- the total running time: ", '%.2f'%time_duration, "s.")
        print("|   |-- the length (i.e. number of tiles moved): ",            eight_solution[1])
        print("|   |-- that total number of nodes removed (from frontier): ", eight_solution[2],"\n\n")

        j = 3
        with open('eight_results.csv', mode='a',newline='') as results_outfile:
            results_writer = csv.writer(results_outfile)
            results_writer.writerow([i, j, k, time_duration, eight_solution[1], eight_solution[2]])
            #print( i, ", ", j, ", ", k)
            # ...     

#
#
# 
#                           
#  _|    _|    _    _ _ | _ 
# (_||_|(_|(__|_)|_|/_/_|(- 
#             |             
### ___________________________________________________________________________
for i in range(1, NUM_BOARDS+1,1):

    duck_puzzle = make_rand_duck_puzzle(goal)


    with open('duck_boards.csv', mode='a',newline='')as duckpuzzle_boards_outfile:
        duckpuzzle_boards_writer = csv.writer(duckpuzzle_boards_outfile)
        duckpuzzle_boards_writer.writerow([i, duck_puzzle.initial])

    problem_title    = "A*-Search"
    #print(problem_title)

    trials = 1

    for k in range(1,trials+1,1):

        #
        #
        #
        # p02.1
        problem_subtitle = "Manhattan Distance Heuristic"
        print("|-- ", problem_subtitle)

 
        time_start      = time.time()
        duck_solution = astar_search(duck_puzzle, duck_puzzle.manhattan_heuristic)
        time_duration   = time.time() - time_start

        print("|   |-- the total running time: ", '%.2f'%time_duration, "s.")
        print("|   |-- the length (i.e. number of tiles moved): ",            duck_solution[1])
        print("|   |-- that total number of nodes removed (from frontier): ", duck_solution[2])
        print("|   ")
 
        j = 1
        with open('duck_results.csv', mode='a',newline='') as results_outfile:
            results_writer = csv.writer(results_outfile)
            results_writer.writerow([i, j, k, time_duration, duck_solution[1], duck_solution[2]])
        #print( i, ", ", j, ", ", k)

        #
        #
        #
        # p02.2
        problem_subtitle = "Misplaced Tile Heuristic"
        print("|-- ", problem_subtitle)

        time_start      = time.time()
        duck_solution = astar_search(duck_puzzle)
        time_duration   = time.time() - time_start

        print("|   |-- the total running time: ", '%.2f'%time_duration, "s.")
        print("|   |-- the length (i.e. number of tiles moved): ",            duck_solution[1])
        print("|   |-- that total number of nodes removed (from frontier): ", duck_solution[2])
        print("|   ")

        j = 2
        with open('duck_results.csv', mode='a',newline='') as results_outfile:
            results_writer = csv.writer(results_outfile)
            results_writer.writerow([i, j, k, time_duration, duck_solution[1], duck_solution[2]])
        #print( i, ", ", j, ", ", k)

        #
        #
        #
        # p02.3
        problem_subtitle = "Max of Misplaced Tile and Manhattan Distance Heuristics"
        print("|-- ", problem_subtitle)


        time_start      = time.time()
        duck_solution = astar_search(duck_puzzle, duck_puzzle.maximum)
        time_duration   = time.time() - time_start

        print("|   |-- the total running time: ", '%.2f'%time_duration, "s.")
        print("|   |-- the length (i.e. number of tiles moved): ",            duck_solution[1])
        print("|   |-- that total number of nodes removed (from frontier): ", duck_solution[2],"\n\n")

        j = 3
        with open('duck_results.csv', mode='a',newline='') as results_outfile:
            results_writer = csv.writer(results_outfile)
            results_writer.writerow([i, j, k, time_duration, duck_solution[1], duck_solution[2]])
        #print( i, ", ", j, ", ", k)
        # ...     
