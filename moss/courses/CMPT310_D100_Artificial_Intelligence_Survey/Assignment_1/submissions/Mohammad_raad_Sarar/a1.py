# a1.py

from search import *
import random
import time




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

        rem_left = [0,2,6]
        rem_up = [0,1,4,5]
        rem_right = [1,5,8]
        rem_down = [2,6,7,8]

        if index_blank_square in rem_left:
            possible_actions.remove('LEFT')
        if index_blank_square in rem_up:
            possible_actions.remove('UP')
        if index_blank_square in rem_right:
            possible_actions.remove('RIGHT')
        if index_blank_square in rem_down:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        new_state = list(state)
        blank = self.find_blank_square(state)
        destination = 0
        if action == "UP":
            if blank in [2,3]:
                destination = blank-2
            if blank in [6,7,8]:
                destination = blank-3

        if action == "DOWN":
            if blank in [0,1]:
                destination = blank+2
            if blank in [3,4,5]:
                destination = blank+3

        if action == "RIGHT":
                destination = blank+1
        if action == "LEFT":
                destination = blank-1

        new_state[blank], new_state[destination] = new_state[destination], new_state[blank]
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))





def astar_search_overload(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_overload(problem, lambda n: n.path_cost + h(n), display)

def best_first_graph_search_overload(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned.
    Modified to also return popcount as a part of node"""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    popcount = 0
    while frontier:
        node = frontier.pop()
        popcount = popcount + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            node.popcount = popcount
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

def make_rand_8Puzzle ():
    """ Returns a 8-puzzle object with random initial State that is solvable """
    solvable = False

    while solvable != True:
        x = tuple(random.sample (range (9), 9))
        # x = (1,2,3,4,5,0,7,8,6) # 1 move away
        # x = (1,2,3,4,0,5,7,8,6) # 2 move away
        print ("X = " , x)
        EP_temp = EightPuzzle(initial = x)
        solvable = EP_temp.check_solvability(state = x)
        if solvable:
            display(x)
        else:
            print ("Not Solvable. \nTrying Again")
    return EP_temp

def make_rand_DuckPuzzle ():
    """ Returns a 8-puzzle object with random initial State that is solvable by shuffling from goal state.
    Any state reached by legal moves from goal is solvable"""
    state = (1,2,3,4,5,6,7,8,0)
    DP_temp = DuckPuzzle(initial = state)
    moves = random.randint(1000, 50000)
    for x in range (0, moves):
        actions = DP_temp.actions(state)
        select_action = actions [random.randint(0, len(actions)-1)]
        result = DP_temp.result(state, select_action)
        state = result
    display_DuckPuzzle(state)
    DP_temp = DuckPuzzle(initial = state)
    return DP_temp

def display (state):
    """ Displays an 8-puzzle with correct orientation on the console"""
    print ("\n")
    counter = 1
    for x in state:

        if x == 0:
            print("*", end = " ")
        else:
            print (x, end = " ")

        if counter%3 == 0:
            print ("\n")
        counter = counter + 1

def display_DuckPuzzle(state):
    """ Displays a Duck-puzzle with correct orientation on the console"""
    print ("\n")
    counter = 1
    state_list = list(state)
    for x in range (0,9):
        if state_list[x] == 0:
            state_list[x] = "*"

    for x in state_list:
        if counter ==2 or counter ==6 :
            print (x)
        else:
            if counter ==7:
                print (" ", end = " ")
            print (x, end = " ")
        counter = counter + 1

    print ("\n")

def manhattan_eight_puzzle (node):
    """ Implementation of heuristic function h(n) = manhattan distance for 8-puzzle"""
    all_moves = 0
    goal_state = [1,2,3,4,5,6,7,8,0]
    for x in range (0,9):

        if node.state[x] != 0:
            #get the height of each element in state and find what height they should be
            current_height = int(x/3)
            goal_height = int((goal_state.index(node.state[x])) /3)
            #get the vertical difference
            vertical_moves = abs (goal_height-current_height)
            #get the width of each element in state and find what width they should be
            current_width = int(x%3)
            goal_width = int((goal_state.index(node.state[x]) %3))
            #get the horizontal difference
            horizontal_moves = abs (current_width-goal_width)
            total_moves = vertical_moves + horizontal_moves
            all_moves = all_moves + total_moves
    return all_moves

def manhattan_Duck_puzzle(node):
    """ Implementation of heuristic function h(n) = manhattan distance for Duck-puzzle"""
    goal_state = [1,2,3,4,5,6,7,8,0]
    matrix = [[0,0],[0,1],[1,0],[1,1],[1,2],[1,3],[2,1],[2,2],[2,3]]
    # matrix looks like this:
    # 00 01
    # 10 11 12 13
    #    21 22 23
    #each elelment yx is the vertical position followed by the horizontal
    all_moves = 0
    for x in range (0,9):
        if node.state[x] != 0:
            #get the height and width of each element in state using the matrix
            current = matrix[x]
            current_height = current[0]
            current_width = current[1]
            #get the height and width of the goal of each element using the matrix
            goal= None
            goal = matrix[(goal_state.index(node.state[x]))]
            goal_height = goal[0]
            goal_width = goal[1]
            #calculate vertical and horizontal moves
            vertical_moves = abs (current_height-goal_height)
            horizontal_moves = abs (current_width - goal_width)
            total_moves = vertical_moves + horizontal_moves
            all_moves = all_moves + total_moves
    return all_moves

def max_misplaced_tile_manhattan_eight_puzzle (node):
    """ Implementation of heuristic function h(n) =max of manhattan distance
    and number of misplaced tiles for 8-puzzle"""
    goal_state = [1,2,3,4,5,6,7,8,0]
    return max(sum(s != g for (s, g) in zip(node.state, goal_state)) , manhattan_eight_puzzle(node))

def max_misplaced_tile_manhattan_Duck_puzzle(node):
    """ Implementation of heuristic function h(n) =max of manhattan distance
    and number of misplaced tiles for Duck-puzzle"""
    goal_state = [1,2,3,4,5,6,7,8,0]
    return max(sum(s != g for (s, g) in zip(node.state, goal_state)) , manhattan_Duck_puzzle(node))




# MAIN
number_of_iterations = 10
metadata = {}

print("\n\n============")
print("EIGHT PUZZLE")
print("============\n\n")

EP_initial = {}
for x in range (0,number_of_iterations):

    puzzle = make_rand_8Puzzle()
    key = str(puzzle.initial).strip(")()")
    method = {
    }

    # A* search using misplaced tiles
    print("\n-------------------------------")
    print("A* search using misplaced tiles")
    print("-------------------------------\n")
    start = time.time()
    node = astar_search_overload(puzzle)
    end = time.time()
    time_t = end-start
    print ("time_taken: " ,time_t)
    print ("popcouuntt: " ,node.popcount)
    print ("path cost: " ,node.path_cost)
    metrics ={
        "time_taken" : time_t,
        "length":node.path_cost,
        "popcount" :node.popcount,
    }
    method ["Astar_misp"] = metrics

    # A* search using Manhattan
    print("\n---------------------------")
    print("#A* search using Manhattan")
    print("---------------------------\n")
    start = time.time()
    node = astar_search_overload(puzzle, h = manhattan_eight_puzzle )
    end = time.time()
    time_t = end-start
    print ("time_taken: " ,time_t)
    print ("popcouuntt: " ,node.popcount)
    print ("path cost: " ,node.path_cost)
    metrics ={
        "time_taken" : time_t,
        "length":node.path_cost,
        "popcount" :node.popcount,
    }
    method ["Astar_manh"] = metrics

    # A* search using Max of Manhattan and misplaced tiles
    print("\n----------------------------------------------------")
    print("A* search using Max of Manhattan and misplaced tiles")
    print("----------------------------------------------------\n")
    start = time.time()
    node = astar_search_overload(puzzle, h = max_misplaced_tile_manhattan_eight_puzzle)
    end = time.time()
    time_t = end-start
    print ("time_taken: " ,time_t)
    print ("popcouuntt: " ,node.popcount)
    print ("path cost: " ,node.path_cost)
    metrics ={
        "time_taken" : time_t,
        "length":node.path_cost,
        "popcount" :node.popcount,
    }
    method ["max_Astar_misp_and_Astar_manh"] = metrics

    EP_initial [key] = method
metadata["EightPuzzle"] = EP_initial




print("\n\n============")
print("DUCK PUZZLE")
print("============\n\n")

DP_initial = {}
for x in range (0,number_of_iterations):
    puzzle = make_rand_DuckPuzzle()
    key = str(puzzle.initial).strip(")()")

    # A* search using misplaced tiles
    print("\n-------------------------------")
    print("A* search using misplaced tiles")
    print("-------------------------------\n")
    start = time.time()
    node = astar_search_overload(puzzle)
    end = time.time()
    time_t = end-start
    method = {
    }
    print ("time_taken: " ,time_t)
    print ("popcouuntt: " ,node.popcount)
    print ("path cost: ", node.path_cost,)
    metrics ={
        "time_taken" : time_t,
        "length":node.path_cost,
        "popcount" :node.popcount,
    }
    method ["Astar_misp"] = metrics

    #A* search using Manhattan
    print("\n---------------------------")
    print("#A* search using Manhattan")
    print("---------------------------\n")
    start = time.time()
    node = astar_search_overload(puzzle, h = manhattan_Duck_puzzle)
    end = time.time()
    time_t = end-start
    print ("time_taken: " ,time_t)
    print ("popcouuntt: " ,node.popcount)
    print ("path cost: ", node.path_cost,)
    metrics ={
        "time_taken" : time_t,
        "length":node.path_cost,
        "popcount" :node.popcount,
    }
    method ["Astar_manh"] = metrics

    # A* search using Max of Manhattan and misplaced tiles
    print("\n----------------------------------------------------")
    print("A* search using Max of Manhattan and misplaced tiles")
    print("----------------------------------------------------\n")
    start = time.time()
    node = astar_search_overload(puzzle, h = max_misplaced_tile_manhattan_Duck_puzzle)
    end = time.time()
    time_t = end-start
    print ("time_taken: " ,time_t)
    print ("popcouuntt: " ,node.popcount)
    print ("path cost: " ,node.path_cost)
    metrics ={
        "time_taken" : time_t,
        "length":node.path_cost,
        "popcount" :node.popcount,
    }
    method ["max_Astar_misp_and_Astar_manh"] = metrics

    DP_initial [key] = method
metadata["DuckPuzzle"] = DP_initial

print ("\n\n++++++++++++++++++++++++++++++++++++++++++++++++")
print ("ALL YOUR TEST DATA ARRANGED IN DICTIONARY BELOW:")
print ("You can put this in https://codebeautify.org/python-formatter-beautifier for a more human-readable-format")
print ("++++++++++++++++++++++++++++++++++++++++++++++++\n")
print (metadata)
print ("\n++++++++++++++++++++++++++++++++++++++++++++++++\n")
