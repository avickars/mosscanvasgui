# a1.py
#The code from the aima python repository did not run on my computer.
#I consistently got messaged that modules were not being found despite
#my installing them. For this reason I was not able to run any of the algorithms
#but still coded as much as I could. 



from search import *
import random
import time 

#


#function that returns a random configuration of the
#eight-puzzle, provided the arragement of tiles is
#solvable. 
def make_rand_8puzzle():

    
    state_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    #list of all possible elements of a state
    
    while True:
    
        random_state_list = random.sample(state_numbers, 8)
        random_state_tuple = tuple(random_state_list)

        puzzle  = EightPuzzle(initial = random_state_tuple) 
    
        if puzzle.check_solvability(random_state_tuple) == True:
            return puzzle
    #a list is created that is a random permutation of (0,..,8),
    #and converted to a tuple. This tuple is then passed to a new
    #instance of an eight-puzzle. The state is checked for
    #solvability, and the loop iterates until a solvable state
    #is generated. 
def display(state):
    for i in range(3):
        if state[i] == 0:
            print('*')
        else:
            print(state[i])
            
    print('\n')
    
    for i in range(3):
        if state[i+3] == 0:
            print('*')
        else:
            print(state[i+3])
            
    print('\n')

    for i in range(3):
        if state[i+6] == 0:
            print('*')
        else:
            print(state[i+6])
    #simple function to print the configuration of an eight-puzzle.
    #the empty space is represented by the '*' character.



    
    


def Manhattan_h(state):
    initial = state
    manDist = 0
    for i, item in range(0,9):
                 prev_row, prev_col = int(i/3), i % 3
                 goal_row, goal_col = int(item/3), item % 3
                 manDist += abs(prev_row-goal_row) + abs(prev_col - goal_col)
    return manDist
#help for writing Manhattan distance function from:
#https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game

def heuristic_max(manhattan, h):
    return max(manhattan, h)


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

        if index_blank_square == 0 or 2 or 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or 1 or 4 or 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or 5 or 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or 6 or 7 or 8
            possible_actions.remove('DOWN')

        return possible_actions
        #the irregular shape of the puzzle warrants very specific conditions for which
        #certain actions can be taken.
                             

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': 0, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
        if blank in range(6,9):
                 delta['UP'] = -3
        if blank in range(2,4):
                 delta['UP'] = -2
        if blank in range(0,2):
                 delta['DOWN'] = 2
        if blank in range(3,6):
                 delta['DOWN'] = 3
        #there is no fixed pattern for which an empty space is permitted to perform
        #an action, so specific conditions must be defined due to the irregularity of the
        #puzzle
        
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


def make_rand_duckPuzzle():

    
    duck_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    #list of all possible elements of a state
    
    while True:
    
        random_state_list = random.sample(duck_numbers, 8)
        random_state_tuple = tuple(random_state_list)

        puzzle  = DuckPuzzle(initial = random_state_tuple) 
    
        if puzzle.check_solvability(random_state_tuple) == True:
            return puzzle

puzzle_1 = make_rand_8puzzle()
puzzle_2 = make_rand_8puzzle()
puzzle_3 = make_rand_8puzzle()
puzzle_4 = make_rand_8puzzle()
puzzle_5 = make_rand_8puzzle()
puzzle_6 = make_rand_8puzzle()
puzzle_7 = make_rand_8puzzle()
puzzle_8 = make_rand_8puzzle()
puzzle_9 = make_rand_8puzzle()
puzzle_10 = make_rand_8puzzle()
#generate 10 8 puzzles
D_puzzle_1 = make_rand_duckPuzzle()
D_puzzle_2 = make_rand_duckPuzzle()
D_puzzle_3 = make_rand_duckPuzzle()
D_puzzle_4 = make_rand_duckPuzzle()
D_puzzle_5 = make_rand_duckPuzzle()
D_puzzle_6 = make_rand_duckPuzzle()
D_puzzle_7 = make_rand_duckPuzzle()
D_puzzle_8 = make_rand_duckPuzzle()
D_puzzle_9 = make_rand_duckPuzzle()
D_puzzle_10 = make_rand_duckPuzzle()
#generate 10 duck puzzles


        
    

    
