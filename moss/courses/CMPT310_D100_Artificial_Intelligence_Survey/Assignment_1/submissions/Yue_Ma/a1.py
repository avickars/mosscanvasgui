# #   a1.py
import time
import numpy as np
from search import *

# #   Question 1
#   Write a function called make_rand_8puzzle() 
#   that returns a new instance of an EightPuzzle 
#   problem with a random initial state that is solvable.
def make_rand_8puzzle() :
    state = (0,1,2,3,4,5,6,8,7)
    new_puzzle = EightPuzzle(initial = state)
    while new_puzzle.check_solvability(state) == False :
        state = tuple(np.random.permutation(9))
        new_puzzle = EightPuzzle(initial = state)
    return new_puzzle

# x = make_rand_8puzzle()
# print(x.initial)

# Write a function called display(state) that takes 
# an 8-puzzle state (i.e. a tuple that is a permutation 
# of (0, 1, 2, …, 8)) as input and prints a neat and 
# readable representation of it. 0 is the blank, and 
# should be printed as a * character.
def display(state):
    temp = list(state)
    temp[state.index(0)] = '*'
    for x in range(len(temp)):
        if x % 3 == 2:
            print(temp[x], end='\n')
        else:
            print(temp[x], end=' ')
    

# state = (0,3,2,1,8,7,4,6,5)
# display(state)

# #   Question 2
# #------Exchange the Given code in Search.py------------
# # Helper function for A*-search using the misplaced tile 
# # heuristic (this is the default heuristic in the EightPuzzle class)
# # A* search Algorithm is a best first search algorithm
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
    removed = 0                 # initial total number of nodes that were removed from frontier
    while frontier:
        node = frontier.pop()
        removed += 1            # count the total # of nodes that were removed from frontier
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, removed
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, removed

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# Helper function for A*-search using the Manhattan distance 
# heuristic Please implement your own (correctly working!) 
# version of the Manhattan heuristic.
# Helper function
# Find the number of rows and columns of the specified number 
# in the original 8 puzzle
def find_xy(node, goal_num):
    for x in range(3):
        for y in range(3):
            if node[x][y] == goal_num :
                return x, y

# Main Function to calculate the distance of Manhatton
# The main idea is from:
# https://www.andrew.cmu.edu/course/15-121/labs/HW-7%20Slide%20Puzzle/lab.html
def Manhattan_dis(node):
    goal = [ [1,2,3], [4,5,6],[7,8,0] ]
    state = [ [0,0,0],[0,0,0],[0,0,0] ]
    index = 0
    for x in range(3):
        for y in range(3):
            state[x][y] = node.state[index]
            index += 1
    
    manhattan_distance = 0
    for row_g in range(3):
        for column_g in range(3):
            if goal[row_g][column_g] == 0:
                break

            row_s,column_s = find_xy(state, goal[row_g][column_g])
            each_entry_distance = abs(row_s - row_g) + abs(column_s - column_g) # Manhattan way 
            manhattan_distance += each_entry_distance

    return manhattan_distance

# A*-search using the max of the misplaced 
# tile heuristic and the Manhattan distance heuristic
def max_dis(node):
    eight_puzzle = EightPuzzle(node.state)
    man = Manhattan_dis(node)
    mis = eight_puzzle.h(node)
    return max(man,mis)

# Create 10 (more would be better!) random 8-puzzle instances 
# (using your code from above), and solve each of them using 
# the algorithms below.

def algorithm_test_8puzzle():
    # make random instance of 8 puzzle
    eight_puzzle = make_rand_8puzzle()
    
    # first algotithm - the misplaced tile heuristic
    display(eight_puzzle.initial)
    
    start_time = time.time()
    len_of_solution, num_of_removed = astar_search(eight_puzzle)
    elapsed_time = time.time() - start_time
    
    print("\nA*-search using the misplaced tile heuristic: ")
    print(f'\telapsed time (in seconds): {elapsed_time}s')
    print("\tlength of solution: ", len(len_of_solution.solution()))
    print("\ttotal number of nodes: ", num_of_removed)

    # second algotithm - A*-search using the Manhattan distance heuristic

    start_time = time.time()
    len_of_solution_man, num_of_removed_man = astar_search(eight_puzzle, h=Manhattan_dis)
    elapsed_time = time.time() - start_time

    print("A*-search using the Manhattan distance heuristic: ")
    print(f'\telapsed time (in seconds): {elapsed_time}s')
    print("\tlength of solution: ", len(len_of_solution_man.solution()))
    print("\ttotal number of nodes: ", num_of_removed_man)

    # third algorithm - A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic

    start_time = time.time()
    len_of_solution_max, num_of_removed_max =  astar_search(eight_puzzle, h=max_dis)
    elapsed_time = time.time() - start_time

    print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic: ")
    print(f'\telapsed time (in seconds): {elapsed_time}s')
    print("\tlength of solution: ", len(len_of_solution_max.solution()))
    print("\ttotal number of nodes: ", num_of_removed_max)

def running_10_times():
    for i in range(10):
        print("\nThe ", i+1, "times")
        algorithm_test_8puzzle()

# print('\n')
# running_10_times()

#   Question 3: The House-Puzzle
# (Duck-puzzle) Implement a new Problem class called DuckPuzzle 
# that is the same as the 8-puzzle, except the board has this shape 
# (that looks a bit like a duck facing to the left):

class DuckPuzzle(Problem):
    
    def __init__(self, initial, goal=(1,2,3,4,5,6,7,8,0)):
        """Define goal state and initialize a problem"""
        super().__init__(initial, goal)
        
    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index(0)
    
    def actions(self, state):
        """Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment"""
        possible_action = ['UP', 'DOWN','LEFT','RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square < 2 or (index_blank_square > 3 and index_blank_square < 6):
            possible_action.remove('UP')
        if index_blank_square == 2 or index_blank_square > 5 :
            possible_action.remove('DOWN')
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_action.remove('LEFT')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_action.remove('RIGHT')
        
        return possible_action
    
    def result(self, state, action) :
        """Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state"""

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank < 3:
            delta = {'UP':-2, 'DOWN':2, 'LEFT':-1, 'RIGHT':1}
        elif blank == 3:
            delta = {'UP':-2, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
        else:
            delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
        
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)
    
    def goal_test(self, state):
        """Given a state, return True if state is a goal state or False, otherwise"""

        return state == self.goal
    
    def check_solvability(self, state):
        """Checks if the given state is solvable"""
        # top 2x2 box
        check2x2 = [0,1,2,3]
        index_of_1 = state.index(1)
        index_of_2 = state.index(2)
        index_of_3 = state.index(3)

        if index_of_1 < 4 and index_of_2 < 4 and index_of_3 < 4 :
            check2x2.remove(index_of_1)
            check2x2.remove(index_of_2)
            check2x2.remove(index_of_3)

            # if the remaining value is not blank, False
            if state[check2x2[0]] != 0 :
                return False
            
            # if 1 is in index 0, but 2 is not in index 1
            if index_of_1 == 0 and index_of_2 != 1 :
                return False
            elif index_of_1 == 1 and index_of_2 != 3: # if 1 is in index 1, but 2 is not in index 3
                return False
            elif index_of_1 == 3 and index_of_2 != 2: # if 1 is in index 3, but 2 is not in index 2
                return False
            elif index_of_1 == 2 and index_of_2 != 0: # if 1 is in index 2, but 2 is not in index 0
                    return False
            
            inversion = 0
            for i in range(3, len(state)):
                for j in range( i+1, len(state)):
                    if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                        inversion += 1
            return inversion % 2 == 0
        else:
            return False

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

# end of DuckPuzzle class
# Question 3 part 1
# make random Duck Puzzle

def make_rand_DuckPuzzle():
    state = (0,1,2,3,4,5,6,8,7)
    new_puzzle = DuckPuzzle(initial = state)
    while new_puzzle.check_solvability(state) == False :
        state = tuple(np.random.permutation(9))
        new_puzzle = DuckPuzzle(initial = state)
    return new_puzzle

# x = make_rand_DuckPuzzle()
# print(x.initial)

# do display
def display_DuckPuzzle(state):
    temp_state = list(state)
    temp_state[state.index(0)] = '*'
    for i in range(9):
        if i == 1 or i == 5 or i == 8:
            print(temp_state[i], end='\n')
        elif i == 6:
            print(' ', temp_state[i], end=' ')
        else:
            print(temp_state[i], end=' ')

# state = (1,2,3,4,5,6,7,8,0)
# display_DuckPuzzle(state)

# Question 3 part 2 

def find_duck_xy(node, goal_num):
    for x in range(3):
        for y in range(len(node[x])):
            if node[x][y] == goal_num :
                return x, y

def Manhattan_dis_duck(node):
    goal = [ [1,2], [3,4,5,6],[7,8,0] ]
    state = [ [0,0],[0,0,0,0],[0,0,0] ]
    temp = list(node.state)
    state[0] = temp[0:2]
    state[1] = temp[2:6]
    state[2] = temp[6:9]
    
    manhattan_distance = 0
    for row_g in range(3):
        for column_g in range(len(goal[row_g])):
            if goal[row_g][column_g] == 0:
                break

            row_s,column_s = find_duck_xy(state, goal[row_g][column_g])
            each_entry_distance = abs(row_s - row_g) + abs(column_s - column_g) # Manhattan way 
            manhattan_distance += each_entry_distance

    return manhattan_distance

def max_dis_duck(node):
    eight_puzzle = DuckPuzzle(node.state)
    man = Manhattan_dis_duck(node)
    mis = eight_puzzle.h(node)
    return max(man,mis)
# Create 10 (more would be better!) random 8-puzzle instances 
# (using your code from above), and solve each of them using 
# the algorithms below.
def algorithm_test_duckpuzzle():
    # make random instance of 8 puzzle
    duck_puzzle = make_rand_DuckPuzzle()
    
    # first algotithm - the misplaced tile heuristic
    display_DuckPuzzle(duck_puzzle.initial)
    
    start_time = time.time()
    len_of_solution, num_of_removed = astar_search(duck_puzzle)
    elapsed_time = time.time() - start_time
    
    print("\nA*-search using the misplaced tile heuristic: ")
    print(f'\telapsed time (in seconds): {elapsed_time}s')
    print("\tlength of solution: ", len(len_of_solution.solution()))
    print("\ttotal number of nodes: ", num_of_removed)

    # second algotithm - A*-search using the Manhattan distance heuristic

    start_time = time.time()
    len_of_solution_man, num_of_removed_man = astar_search(duck_puzzle, h=Manhattan_dis_duck)
    elapsed_time = time.time() - start_time

    print("A*-search using the Manhattan distance heuristic: ")
    print(f'\telapsed time (in seconds): {elapsed_time}s')
    print("\tlength of solution: ", len(len_of_solution_man.solution()))
    print("\ttotal number of nodes: ", num_of_removed_man)

    # third algorithm - A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic

    start_time = time.time()
    len_of_solution_max, num_of_removed_max =  astar_search(duck_puzzle, h=max_dis_duck)
    elapsed_time = time.time() - start_time

    print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic:")
    print(f'\telapsed time (in seconds): {elapsed_time}s')
    print("\tlength of solution: ", len(len_of_solution_max.solution()))
    print("\ttotal number of nodes: ", num_of_removed_max)

def running_10_times_duck():
    for i in range(10):
        print("The ", i+1, "times")
        algorithm_test_duckpuzzle()

running_10_times_duck()