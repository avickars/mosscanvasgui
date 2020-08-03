# a1.py
#standard libraries
import time
from random import randint

from search import Problem
from search import Node
from search import astar_search
from search import memoize
from search import best_first_graph_search

class EightPuzzle_a1(Problem):
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

        return sum(s != g for (s, g) in zip(node.state, self.goal))
    
    def h_manhat(self, node):
        """ Return the manhattan distance heuristic value for a given state"""
        state = node.state
        position_actual = {}
        position_values = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        position_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        
        for x in range(9):
            position_actual[state[x]] = position_values[x]
        
        manhat_y = 0
        manhat_x = 0
        
        for x in range(1,9):
           manhat_x = abs(position_goal[x][0] - position_actual[x][0]) + manhat_x
           manhat_y = abs(position_goal[x][1] - position_actual[x][1]) + manhat_y
        return (manhat_y + manhat_x)

    def h_max(self, node):
        misplace_value = self.h(node)
        manhat_value = self.h_manhat(node)
        return (max(misplace_value, manhat_value))


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
        #0 or 2 or 6 doesnt work
        index_cant_left = (0,2,6)
        index_cant_up = (0,1,4,5)
        index_cant_right = (1,5,8)
        index_cant_down = (2,6,7,8)

        if index_blank_square in index_cant_left:
            possible_actions.remove('LEFT')
        if index_blank_square in index_cant_up:
            possible_actions.remove('UP')
        if index_blank_square in index_cant_right:
            possible_actions.remove('RIGHT')
        if index_blank_square in index_cant_down:
            possible_actions.remove('DOWN')
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        #______________________________________________
        """needs refactoring"""
        # blank is the index of the blank square
        blank = self.find_blank_square(state)

        new_state = list(state)

        if blank <= 2:
            delta = {'UP': -2, 'DOWN': +2, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))
    
    def h_manhat(self, node):
        """ Return the manhattan distance heuristic value for a given state"""
        state = node.state
        position_actual = {}
        position_values = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
        position_goal = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
        
        for x in range(9):
            position_actual[state[x]] = position_values[x]
        
        manhat_x = 0
        manhat_y = 0
        
        for x in range(9):
           manhat_x = abs(position_goal[x][0] - position_actual[x][0]) + manhat_x
           manhat_y = abs(position_goal[x][1] - position_actual[x][1]) + manhat_y
        
        return (manhat_x + manhat_y)

    def h_max(self, node):
        misplace_value = self.h(node)
        manhat_value = self.h_manhat(node)
        return (max(misplace_value, manhat_value))

#manhattan search function

def astar_search_manhat(problem, h=None, display = True):
    """astar search with manhattan block calculation"""
    h = memoize(h or problem.h_manhat, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost +h(n), display)

#search fucntion that uses the max of manhattan and heuristic misplaced as the h value
def astar_search_max(problem, h=None, display = True):
    """astar search with max of manhattan and heuristic"""
    h = memoize(h or problem.h_max, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost +h(n), display)

#function to generate random eight puzzle
def make_rand_8puzzle():
    puzzle_list= [1,2,3,4,5,6,7,8,0]
    for x in range(9):
        randindex = (randint(0,8))
        temp = puzzle_list[x]
        puzzle_list[x] = puzzle_list[randindex]
        puzzle_list[randindex] = temp
    if EightPuzzle_a1.check_solvability(EightPuzzle_a1, puzzle_list):
        #print("Solvable puzzle generated.")
        return EightPuzzle_a1(tuple(puzzle_list))
    else:
        #print("Unsolvable puzzle. Regenerating.")
        return make_rand_8puzzle()


#funtion to generate random duck puzzle

def make_rand_duckpuzzle():
    puzzle_list = [1,2,3,4,5,6,7,8,0]
    puzzle = DuckPuzzle(puzzle_list)
    node_duck_inital = Node(puzzle.initial)
    node_duck_two = node_duck_inital
    for x in range(1000):
        node_choices = node_duck_two.expand(puzzle)
        int_choice = randint(0,len(node_duck_two.expand(puzzle))-1)
        node_duck_two = node_choices[int_choice]
    return DuckPuzzle(node_duck_two.state)

#function to display eight puzzle

def display_eightpuzzle(state):
    for x in range(9):
        if state[x] != 0:
            print(state[x], end = " ")
        else:
            print("*", end = " ")
        if x == 2 or x == 5 or x == 8:
            print(" ")

#function to display duck puzzle

def display_duckpuzzle(state):
    for x in range(9):
        if state[x] != 0:
            print(state[x], end = " ")
        else:
            print("*", end = " ")
        
        if x == 1 or x == 5 or x == 8:
            print(" ")
        if x == 5:
            print("  ", end ="")    



#testing functions

print("==========Eight Puzzle===========")
for x in range(1,11):

    #test= (0,1,3,4,2,6,7,5,8)
    #test=(0,2,1,8,7,4,6,5,3)
    #test_puzzle = EightPuzzle_a1(test)

    test_puzzle = make_rand_8puzzle()
    #display_eightpuzzle(test_puzzle.initial)

    print("heuristic")
    start = time.perf_counter()
    puzzle_solved = astar_search(test_puzzle)
    print(puzzle_solved.path_cost)
    stop = time.perf_counter()
    print(stop-start)
    
    print("manhattan")
    start = time.perf_counter()
    puzzle_solved_manhat = astar_search_manhat(test_puzzle)
    print(puzzle_solved_manhat.path_cost)
    stop = time.perf_counter()
    print(stop-start)

    print("max")
    start = time.perf_counter()
    puzzle_solved_max = astar_search_max(test_puzzle)
    print(puzzle_solved_max.path_cost)
    stop = time.perf_counter()
    print(stop-start)


print("===========Duck Puzzle============")

for x in range(1,11):
    duck_test = make_rand_duckpuzzle()
    #display_duckpuzzle(duck_test.initial)

    print("heuristic")
    start = time.perf_counter()
    duck_test_solved_h = astar_search(duck_test)
    print(duck_test_solved_h.path_cost)
    stop = time.perf_counter()
    print(stop-start)

    print("manhattan")
    start = time.perf_counter()
    duck_test_solved_man = astar_search_manhat(duck_test)
    print(duck_test_solved_man.path_cost)
    stop = time.perf_counter()
    print(stop-start)

    print("max")
    start = time.perf_counter()
    duck_test_solved_max = astar_search_max(duck_test)
    print(duck_test_solved_max.path_cost)
    stop = time.perf_counter()
    print(stop-start)