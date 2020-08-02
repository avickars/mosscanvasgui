# a1.py
# Gerardo Gandeaga
# 301387300

import time
from search import *

random.seed(time.time)

goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# generated from the duck tests generator below
duck_tests = (
    (2, 3, 1, 4, 0, 8, 7, 6, 5),
    (1, 2, 0, 3, 5, 6, 8, 4, 7),
    (2, 3, 1, 7, 6, 8, 5, 4, 0),
    (3, 1, 2, 5, 7, 8, 6, 0, 4),
    (1, 2, 3, 8, 4, 5, 6, 7, 0),
    (3, 0, 2, 1, 5, 8, 6, 7, 4),
    (3, 1, 2, 4, 6, 5, 0, 8, 7),
    (3, 1, 2, 7, 8, 0, 6, 4, 5),
    (0, 1, 3, 2, 6, 7, 4, 5, 8),
    (2, 0, 1, 3, 7, 6, 4, 8, 5),
    (3, 1, 2, 7, 6, 0, 5, 4, 8),
    (3, 0, 2, 1, 5, 8, 4, 6, 7),
    (2, 3, 0, 1, 4, 8, 5, 7, 6),
    (1, 2, 3, 4, 0, 6, 8, 7, 5),
    (3, 1, 0, 2, 7, 5, 8, 4, 6)
)

# create a random 8 puzzle
def make_rand_8puzzle():
    # create a list of 9 elements of values 0, 1...8 in random order
    state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # shuffle the list
    random.shuffle(state)

    # create puzzle using the list we shuffled converted to a tuple
    state = tuple(state)
    eight_puzzle = EightPuzzle(state)

    # check if the puzzle is solvable, if not then make a recursive call to generate a new random puzzle
    if (eight_puzzle.check_solvability(state) == False):
        eight_puzzle = make_rand_8puzzle()
    else:
        display(state)

    # return a solvable list
    return eight_puzzle

# display state tuple
def display(state):
    state_str = ""

    i = 1
    for n in state:
        # add star or number to string
        if (n == 0):
            state_str += " " + '*'
        else:
            state_str += " " + str(n)

        # add a new line for every 3 numbers
        if (i % 3 == 0):
            state_str += "\n"

        i += 1
    
    # print out the state string
    print(state_str)

# display state tuple
def display_duck(state):
    state_str = ""

    for n in state[0:2]:
        state_str += " " + str(n)
    
    state_str += "\n"

    for n in state[2:6]:
        state_str += " " + str(n)

    state_str += "\n  "

    for n in state[6:10]:
        state_str += " " + str(n)
    
    # print out the state string
    print(state_str.replace('0', '*'))

# resources used to learn the concept:
# https://en.wikipedia.org/wiki/Manhattan_distance
# https://computervision.fandom.com/wiki/Manhattan_distance
def manhattan(node):
    state = node.state # current state of the puzzle 
    goal_indexes = { # the goal state with there "physical" locations (dictionary idea was given in tests/test_search.py)
        1: [0, 0], 2: [0, 1], 3: [0, 2], 
        4: [1, 0], 5: [1, 1], 6: [1, 2], 
        7: [2, 0], 8: [2, 1], 0: [2, 2]
    }

    """ get manhatten distances from the out of place numbers.
    our definition of a manhattan distance will be the length of the vertical and horizontal components of the euclidean distance in cells
    from the starting point to the goal point. """
    mhtn_dist = 0
    wrong_place_str = "["

    # find the out of place numbers
    for i in range(len(state)):
        num = state[i]
        
        # we do not need 0 for the manhattan distance
        if num == 0: 
            continue
        
        index = [int(i / 3), int(i % 3)] # get 2d undex from tuple positon

        # check if the number is not in the right place
        if (index != goal_indexes[num]):
            # calculate distance for the incorrectly positioned numbers
            # verical value
            vert = abs(index[0] - (goal_indexes[num])[0])
            # horizontal value
            hor = abs(index[1] - (goal_indexes[num])[1])
            mhtn_dist += hor + vert
            wrong_place_str += " " + str(num)   

    wrong_place_str += " ]"
    # print("numbers in the wrong place " + wrong_place_str + " distance = " + str(mhtn_dist));
    # display(state)

    return mhtn_dist

def tiles_and_manhattan_max(node):
    # calculate manhattan
    mhtn_dist = manhattan(node)
    # calculate tiles misplaced
    tiles_mplaced = 0
    for i in range(len(node.state)):
        if (node.state[i] != 0 and node.state[i] != goal[i]): 
            tiles_mplaced += 1

    # display the max
    return max(mhtn_dist, tiles_mplaced)

# Duck Puzzle
class DuckPuzzle(EightPuzzle):

    def actions(self, state):
        """ This function overrides the parent EightPuzzle class to chnage the tile movement rules 
        to fit the duck puzzle """
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT' ]
        blank_index = self.find_blank_square(state)

        """
        index structure: this structure ensures that our mahattan heuristic implementation will work with the duck puzzle and eight puzzle
        [0,0][0,1]           <- 2 items
        [1,0][1,1][1,2][1,3] <- 4 items
             [2,1][2,2][2,3] <- 3 items """
        index = self.blank_2d_index(blank_index)
        y = index[0]
        x = index[1]

        # remove impossible actions
        # vertical actions
        if (y == 0 or (y == 1 and x > 1)):
            possible_actions.remove('UP')
        if (y == 2 or (y == 1 and x == 0)): 
            possible_actions.remove('DOWN')
        # horizontal actions
        if (x == 0 or (y == 2 and x == 1)): 
            possible_actions.remove('LEFT')
        if (x == 3 or (y == 0 and x == 1)):
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        blank_index = self.find_blank_square(state)
        y = self.blank_2d_index(blank_index)[0]
        delta = 0
        new_state = list(state)

        # calculate move distance
        if (action == 'UP'):
            # row 2
            if (y == 1): 
                delta = -2
            # row 3 
            else: 
                delta = -3
        elif (action == 'DOWN'):
            # row 1
            if (y == 0): 
                delta = 2
            # row 2 
            else: 
                delta = 3
        elif (action == 'LEFT'):
            delta = -1
        elif (action == 'RIGHT'):
            delta = 1

        # swap blank and number
        num_index = blank_index + delta
        new_state[blank_index], new_state[num_index] = new_state[num_index], new_state[blank_index]

        return tuple(new_state) 
        
    # convert a list index to a point (y, x)
    def blank_2d_index(self, blank):
        # evaluate (x, y) indexes from linear list index
        y = 0
        x = 0

        # first row 
        if (blank < 2): 
            x = blank
        # third row
        elif (blank > 5):
            y = 2
            x = blank - 5
        # second row
        else:
            y = 1
            x = blank - 2

        return (y, x)

# this function was used to generate duck puzzle tests for analyzing the 
def generate_solvable_duck_tests():
    i = 0
    success = 10
    duck_tests = ()
    while i < success:
        # create a list of 9 elements of values 0, 1...8 in random order
        state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        # shuffle the list
        random.shuffle(state)

        # create puzzle using the list we shuffled converted to a tuple
        state = tuple(state)
        duck_puzzle = DuckPuzzle(state)
        res = astar_search(duck_puzzle, h=manhattan)

        if res != None and res not in duck_tests:
            i += 1
            print(state)

    return duck_tests


# test scripts ---------------------------------------

def run_duck_puzzle_test_trials():
    # duck tests
    i = 1
    for x in duck_tests:

        print("Trial", i, "\n")

        display_duck(x)

        duck_puzzle = DuckPuzzle(x)
        print("\nManhattan ------------------------------------------------------")

        start = time.time()
        astar_search(duck_puzzle, h=manhattan, display=True)
        end = time.time() - start

        print("time:", end)

        print("Misplaced Tiles ------------------------------------------------")

        start = time.time()
        astar_search(duck_puzzle, h=None, display=True)
        end = time.time() - start

        print("time:", end)

        print("Max of Manhattan and Misplaced Tiles ---------------------------")

        start = time.time()
        astar_search(duck_puzzle, h=tiles_and_manhattan_max, display=True)
        end = time.time() - start

        print("time:", end, "\n")

        i += 1

def run_eight_puzzle_test_trials():
    for x in range(15):
        print("Trial", (x + 1), "\n")
        eight_puzzle = make_rand_8puzzle()
        print("Manhattan ------------------------------------------------------")

        start = time.time()
        astar_search(eight_puzzle, h=manhattan, display=True)
        end = time.time() - start

        print("time:", end)

        print("Misplaced Tiles ------------------------------------------------")

        start = time.time()
        astar_search(eight_puzzle, h=None, display=True)
        end = time.time() - start

        print("time:", end)

        print("Max of Manhattan and Misplaced Tiles ---------------------------")

        start = time.time()
        astar_search(eight_puzzle, h=tiles_and_manhattan_max, display=True)
        end = time.time() - start

        print("time:", end, "\n")

# run_duck_puzzle_test_trials()
# run_eight_puzzle_test_trials()
# generate_solvable_duck_tests()

# -----------------------------------------------------
