#a1.py
#CMPT310 - Assignment 1
#Author: ChinHo Wan
#Student no.: 301308171

"""Read https://www.d.umn.edu/~jrichar4/8puz.html for general ideas"""
"""Read https://www2.cs.sfu.ca/CourseCentral/310/tjd/a1.html for requirements"""
"""Read https://www2.cs.sfu.ca/CourseCentral/310/tjd/chp3_search.html for solving problem by searching"""
"""Read Textbook - Artificial Intelligence A Modern Approach Third Edition (Stuart J. Russell and Peter Norvig) chapter 3 for solving problem by searching"""
"""Watched lecture recordings for tree search ideas"""
"""Got some help during office hour from TA (Vincent Haung)"""

from search import *
import random
import numpy 
import time

"""=== Q1 functions ==="""
def rand_init_state():
    """This function will generate and return a solvable 8-puzzle using check_solvability from search.py """
    goal_state = (1,2,3,4,5,6,7,8,0)
    while True:
        init_state = tuple(numpy.random.permutation(goal_state))
        state = EightPuzzle(init_state)
        if (state.check_solvability(init_state) == True):
            return  init_state

def display(state):
    """This function will replace 0 as * from the tuple and display as the shape of 8-puzzle"""
    temp = list(state)
    for i in range(len(temp)):
        if temp[i] == 0: temp[i] = '*'
    print(temp[0], temp[1], temp[2])
    print(temp[3], temp[4], temp[5])
    print(temp[6], temp[7], temp[8])
    print()

"""=== Q2 functions ==="""
def h_m(node):
    """Modified: This function will not count the 0 as misplaced tile"""
    """ Return the heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles """
    goal_state = (1,2,3,4,5,6,7,8,0)
    counter = 0
    for i in range(9):
        if (node.state[i] != 0):
            if (goal_state[i] != node.state[i]):
                counter = counter + 1

    return counter

def find_location(loc):
    """Helper function for cal_man_distance"""
    temp_x = int(loc / 3)
    temp_y = loc % 3
    return temp_x, temp_y

def cal_man_distance(node):
    """This function will calculate the Manhattan distance"""
    # Manhattan Heuristic Function
    total = 0
    goal_state = (1,2,3,4,5,6,7,8,0)
    for i in range(9):
        temp_x1 = 0 
        temp_y1 = 0 
        temp_x2 = 0 
        temp_y2 = 0 
        """Finding the location of data in goal state"""
        data = goal_state[i]
        #if (data != 0):
        temp_x2, temp_y2 = find_location(i)
        """Finding the location of each data in current state"""
        for k in range (9):
            if (node.state[k] == data):
                temp_x1, temp_y1 = find_location(k)
        
        total = total + abs(temp_x2 - temp_x1) + abs(temp_y2 - temp_y1)
    return total 

def max_func(node):
    """This will function will find the max of the Default heuristic 
    and the Manhattan distance heuristic"""
    #puzzle = EightPuzzle(node.state)
    #return max(cal_man_distance(node),puzzle.h(node))
    return max(cal_man_distance(node),h_m(node))
    
def astar_search_m(problem, h=None, display=False):
    """ Modified astar_search function from search.py. 
    Purpose: Able to call the modified best_first_graph_search function)
    Modification: astar_search -> astar_search_m; best_first_graph_search -> best_first_graph_search_m"""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_m(problem, lambda n: n.path_cost + h(n), display)

def best_first_graph_search_m(problem, f, display=False):
    """ Modified best_first_graph_search function from search.py
    Modification: Called path_cost() and returns as length of the solution; 
    Added and returns as node_counter to track the number of nodes removed""" 
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    node_counter = 0
    while frontier:
        node = frontier.pop()
        node_counter += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, node.path_cost, node_counter
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def default_method(state):
    """This function will use Default heuristic method to solve the puzzle 
    and print out the required informations"""
    start_time = time.time()
    puzzle = EightPuzzle(state)
    info = astar_search_m(puzzle, h= h_m, display= False)
    running_time = time.time() - start_time
    print("Default heuristic: ")
    print("Total running time(sec): ", running_time)
    print("The length of the solution: ", info[1])
    print("Total number of nodes that were removed from frontier: ", info[2])
    print()

def Manhattan_method(state):
    """This function will use Manhattan distance heuristic method to solve the puzzle
    and print out the required informations"""
    start_time = time.time()
    puzzle = EightPuzzle(state)
    info = astar_search_m(puzzle, h= cal_man_distance, display= False)
    running_time = time.time() - start_time
    print("Manhattan distance heuristic: ")
    print("Total running time(sec): ", running_time)
    print("The length of the solution: ", info[1])
    print("Total number of nodes that were removed from frontier: ", info[2])
    print()

def max_defNman(state):
    """This function will use default heuristic or Manhattan distance heuristic method (Based on the MAX) 
    to solve the puzzle and print out the required informations"""
    start_time = time.time()
    puzzle = EightPuzzle(state)
    info = astar_search_m(puzzle, h= max_func, display= False)
    running_time = time.time() - start_time
    print("The max of the Default heuristic and the Manhattan distance heuristic: ")
    print("Total running time(sec): ", running_time)
    print("The length of the solution: ", info[1])
    print("Total number of nodes that were removed from frontier: ", info[2])
    print()


"""=== Q3 functions ==="""
"""need implement"""
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on Duck-Puzzle, where one of the
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

        if (index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6):
            possible_actions.remove('LEFT')
        if (index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5):
            possible_actions.remove('UP')
        if (index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8):
            possible_actions.remove('RIGHT')
        if (index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8):
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        #delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        #neighbor = blank + delta[action]
        #new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        neighbor = 0
        if (blank == 0):
            if (action == 'DOWN'):
                neighbor = 2
            elif (action == 'RIGHT'):
                neighbor = 1
        elif (blank == 1):
            if (action == 'DOWN'):
                neighbor = 3
            elif (action == 'RIGHT'):
                neighbor = 0
        elif (blank == 2):
            if (action == 'UP'):
                neighbor = 0
            elif (action == 'RIGHT'):
                neighbor = 3
        elif (blank == 3):
            if (action == 'LEFT'):
                neighbor = 2
            elif (action == 'UP'):
                neighbor = 1
            elif (action == 'RIGHT'):
                neighbor = 4
            elif (action == 'DOWN'):
                neighbor = 6
        elif (blank == 4):
            if (action == 'LEFT'):
                neighbor = 3
            elif (action == 'RIGHT'):
                neighbor = 5  
            elif (action == 'DOWN'):
                neighbor = 7 
        elif (blank == 5):
            if (action == 'LEFT'):
                neighbor = 4
            elif (action == 'DOWN'):
                neighbor = 8  
        elif (blank == 6):
            if (action == 'UP'):
                neighbor = 3
            elif (action == 'RIGHT'):
                neighbor = 7
        elif (blank == 7):
            if (action == 'LEFT'):
                neighbor = 6
            elif (action == 'UP'):
                neighbor = 4
            elif (action == 'RIGHT'):
                neighbor = 8
        elif (blank == 8):
            if (action == 'LEFT'):
                neighbor = 7
            elif (action == 'UP'):
                neighbor = 5

        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        return sum(s != g for (s, g) in zip(node.state, self.goal))


def rand_init_state_duck():
    """This function will generate and return a solvable Duck-puzzle by using 
    random moves method from goal state"""
    goal_state = (1,2,3,4,5,6,7,8,0)
    init_state = goal_state

    move = 1000
    while (move > 0):
        temp = DuckPuzzle(init_state)
        possible_actions = temp.actions(init_state)
        actions_temp = random.choice(possible_actions)
        init_state = temp.result(init_state,actions_temp)
        move = move - 1
    return init_state

def display_duck(state):
    """This function will replace  0 as * from the tuple and display as the shape of Duck-puzzle"""
    temp = list(state)
    for i in range(len(temp)):
        if temp[i] == 0: temp[i] = '*'
    print(temp[0], temp[1], " ", " ")
    print(temp[2], temp[3], temp[4], temp[5])
    print(" ", temp[6], temp[7], temp[8])
    print()

def find_location_duck(loc):
    """Helper function for cal_man_distance (For Duck-Puzzle)"""
    """calculates row"""
    temp_x = 0
    temp_y = 0
    if(loc == 0 or loc == 1):
        temp_x = 0
    elif (loc == 2 or loc == 3 or loc == 4 or loc == 5):
        temp_x = 1
    elif (loc == 6 or loc == 7 or loc == 8):
        temp_x = 2
    """calculates column"""
    if(loc == 0 or loc == 2):
        temp_y = 0
    elif (loc == 1 or loc == 3 or loc == 6):
        temp_y = 1
    elif (loc == 4 or loc == 7):
        temp_y = 2
    elif (loc == 5 or loc == 8):
        temp_y = 3

    return temp_x, temp_y

"""need implement"""
def cal_man_distance_duck(node):
    """This function will calculate the Manhattan distance (For Duck-Puzzle)"""
    # Manhattan Heuristic Function
    total = 0
    goal_state = (1,2,3,4,5,6,7,8,0)
    for i in range(9):
        temp_x1 = 0 
        temp_y1 = 0 
        temp_x2 = 0 
        temp_y2 = 0 
        """Finding the location of data in goal state"""
        data = goal_state[i]
        #if (data != 0):
        temp_x2, temp_y2 = find_location_duck(i)
        """Finding the location of each data in current state"""
        for k in range (9):
            if (node.state[k] == data):
                temp_x1, temp_y1 = find_location_duck(k)
        
        total = total + abs(temp_x2 - temp_x1) + abs(temp_y2 - temp_y1)
    return total 

def max_func_duck(node):
    """This will function will find the max of the Default heuristic 
    and the Manhattan distance heuristic (For Duck-Puzzle)"""
    #puzzle = DuckPuzzle(node.state)
    #return max(cal_man_distance(node),puzzle.h(node))
    return max(cal_man_distance_duck(node),h_m(node))

def default_method_duck(state):
    """This function will use Default heuristic method to solve the puzzle 
    and print out the required informations (For Duck-Puzzle)"""
    start_time = time.time()
    puzzle = DuckPuzzle(state)
    info = astar_search_m(puzzle, h= h_m, display= False)
    running_time = time.time() - start_time
    print("Default heuristic: ")
    print("Total running time(sec): ", running_time)
    print("The length of the solution:", info[1])
    print("Total number of nodes that were removed from frontier:", info[2])
    print()

def Manhattan_method_duck(state):
    """This function will use Manhattan distance heuristic method to solve the puzzle
    and print out the required informations (For Duck-Puzzle)"""
    start_time = time.time()
    puzzle = DuckPuzzle(state)
    info = astar_search_m(puzzle, h= cal_man_distance_duck, display= False)
    running_time = time.time() - start_time
    print("Manhattan distance heuristic: ")
    print("Total running time(sec): ", running_time)
    print("The length of the solution: ", info[1])
    print("Total number of nodes that were removed from frontier: ", info[2])
    print()

def max_defNman_duck(state):
    """This function will use default heuristic or Manhattan distance heuristic method (Based on the MAX) 
    to solve the puzzle and print out the required informations (For Duck-Puzzle)"""
    start_time = time.time()
    puzzle = DuckPuzzle(state)
    info = astar_search_m(puzzle, h= max_func_duck, display= False)
    running_time = time.time() - start_time
    print("The max of the Default heuristic and the Manhattan distance heuristic: ")
    print("Total running time(sec): ", running_time)
    print("The length of the solution: ", info[1])
    print("Total number of nodes that were removed from frontier: ", info[2])
    print()

"""=== Main function for testing ==="""
def main():
    """Test for Q1"""
    """Generates and displays a random solvable inital state"""
    init_state = rand_init_state()
    print("===Test Started===")
    print("---Q1 Testing---")
    print(init_state)
    display(init_state)
    print("---Q1 Ended---\n")
   
    """Test for Q2"""
    """Generates and displays 10 different random solvable inital states"""
    print("---Test for Q2 (8-puzzle)---")
    test_size = 10
    puzzle_list = list()
    for i in range(test_size):
        init_state_temp = rand_init_state()
        puzzle_list.append(init_state_temp)
    
    """Solves each 8-puzzle from the list with different methods"""
    for i in range(test_size):
        print("8-Puzzle ", i+1, ": ") 
        display( puzzle_list[i])
        default_method(puzzle_list[i])
        Manhattan_method(puzzle_list[i])
        max_defNman(puzzle_list[i])
    print("---Q2 Ended---\n")

    """Test for Q3"""
    """Generates and displays 10 different random solvable inital states (duck puzzle)"""
    print("---Test for Q3 (Duck-puzzle)---")
    test_size_duck = 10
    puzzle_list_duck = list()
    for i in range(test_size_duck):
        init_state_duck = rand_init_state_duck()
        puzzle_list_duck.append(init_state_duck)

    """Solves each duck puzzle from the list with different methods"""
    for i in range(test_size_duck):
        print("Duck-puzzle ", i+1, ": ") 
        display_duck(puzzle_list_duck[i])
        default_method_duck(puzzle_list_duck[i]) 
        Manhattan_method_duck(puzzle_list_duck[i])
        max_defNman_duck(puzzle_list_duck[i])

    print("---Q3 Ended---")
    print("===Test Ended===\n")

if __name__ == "__main__":
    main()
