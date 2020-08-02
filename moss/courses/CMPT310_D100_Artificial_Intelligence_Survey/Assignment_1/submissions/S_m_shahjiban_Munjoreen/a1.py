# a1.py
# by: S M Shahjiban Munjoreen
#     smunjore@sfu.ca
#     301323565

from search import *
import random
from heapq import heappush, heappop
import time

# code that i changed/ added

def manhattan8(node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        

        return sum(abs((val-1)%3 - i%3) + abs((val-1)//3 - i//3) for i, val in enumerate(node.state) if val)

def maximummm(node):
    a = sum(s != g for (s, g) in zip(node.state, [1,2,3,4,5,6,7,8,0]))
    b = sum(abs((val-1)%3 - i%3) + abs((val-1)//3 - i//3) for i, val in enumerate(node.state) if val)

    return max(a, b)

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    count = 0
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        count +=1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print("Nodes removed:\t" , count)
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

# question 1: Helper functions

def make_rand_8puzzle():
    """ This function returns a new instance of an EightPuzzle
    problem with a random initial state that is solvable """

    while(True):
        new_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        random.shuffle(new_state)
        new_state = tuple(new_state)
        new_puzzle = EightPuzzle(Problem(new_state))
        new_puzzle.initial = new_state

        if new_puzzle.check_solvability(new_puzzle.initial) == True:
            return new_puzzle


def display(state):
    """ This function takes an 8-puzzle state as input and
    prints a neat and readable representation of it """

    state_ = list(state)
    zero_index = state_.index(0)
    state_[zero_index] = "*"
    print(state_[0], state_[1], state_[2])
    print(state_[3], state_[4], state_[5])
    print(state_[6], state_[7], state_[8])

# question 2: Comparing algorithms========================================

print("====================_____8 PUZZLE_____====================\n")

for i in range(0,1):
    puz = make_rand_8puzzle()
    print("[", i + 1, "] starting puzzle:\n")
    display(puz.initial)
    
    print("")

    print("MISPLACED TILES AS HEURISTIC\n")
    start_time = time.time()
    x = best_first_graph_search(puz, puz.h)
    elapsed_time = time.time() - start_time
    print("Time taken:\t", elapsed_time, " seconds")
    steps = 0
    for i in x.path():
        steps += 1
    print("Steps:\t\t", steps)

    print("")
    
    print("MANHATTAN DISTANCE AS HEURISTIC\n")
    start_time = time.time()
    x = best_first_graph_search(puz, manhattan8)
    elapsed_time = time.time() - start_time
    print("Time taken:\t", elapsed_time, " seconds")
    steps = 0
    for i in x.path():
        steps += 1
    print("Steps:\t\t", steps)

    print("")

    print("MAX OF THE TWO AS HEURISTIC\n")
    start_time = time.time()
    x = best_first_graph_search(puz, maximummm)
    elapsed_time = time.time() - start_time
    print("Time taken:\t", elapsed_time, " seconds")
    steps = 0
    for i in x.path():
        steps += 1
    print("Steps:\t\t", steps)
    print("")

# question 3: The House Puzzle================================================

class HousePuzzle(Problem):
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

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        elif index_blank_square == 1:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        elif index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif index_blank_square == 2:
            return possible_actions
        elif index_blank_square == 4:
            possible_actions.remove('UP')
        elif index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        elif index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif index_blank_square == 7:
            possible_actions.remove('DOWN')
        elif index_blank_square == 8:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if(blank == 0):
            delta = {'DOWN': 2, 'RIGHT': 1}
        elif (blank == 1):
            delta = {'LEFT': -1, 'DOWN': 2}
        elif (blank == 2):
            delta = {'RIGHT': 1, 'UP': -2}
        elif (blank == 3):
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif (blank == 4):
            delta = {'LEFT': -1, 'DOWN': 3, 'RIGHT': 1}
        elif (blank == 5):
            delta = {'LEFT': -1, 'DOWN': 3}
        elif (blank == 6):
            delta = {'UP': -3, 'RIGHT': 1}
        elif (blank == 7):
            delta = {'LEFT': -1, 'UP': -3, 'RIGHT': 1}
        elif (blank == 8):
            delta = {'UP': -3, 'LEFT': -1}
       
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)


    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):   
        """ Checks if the given state is solvable """

        """proof: starting from index 3 to 8, the house puzzle mimics the 8 puzzle. therefore,
        the solvability is checked the same way

        index 0 to 3 is what i would like to prove. 0 to 3 is only 4 tiles, it is seperated
        from the rest of the puzzle by index 4. due to this, tile 1,2,3 will always remain in
        0, 1, 2 or 3. tiles 5 or above will never reach position 0, 1, 2

        given position 3 can hold any tile, we can replace it with * eventually through some
        moves. as for tile 1,2, and 3 there is only a small number of ways they can be arranged
        legally. i checked all of those requirements below

        e.g. if index 0 is * and index 1 is 1, index 2 must be 3 and never 2. if it is 2, the puzzle
        is not solvable. i exhausted all such cases to come up with function, thank  you"""

        for i in range(0,3):
            if state[i] != 0 and state[i] != 1 and state[i] != 2 and state[i] != 3:
                return False
            
        for i in range(1,4):
            if state[0] != i and state[1] != i and state[2] != i and state[3] != i:
                return False
                
        if (state[0] == 0):
            if (state[1] == 1):
                if (state[2] == 2) or (state[3] == 3):
                    return False
            if (state[1] == 2):
                if (state[2] == 3) or (state[3] == 1):
                    return False
            if (state[1] == 3):
                if (state[2] == 1) or (state[3] == 2):
                    return False

        elif (state[1] == 0):
            if (state[0] == 1):
                if (state[2] == 2) or (state[3] == 3):
                    return False
            if (state[0] == 2):
                if (state[2] == 3) or (state[3] == 1):
                    return False
            if (state[0] == 3):
                if (state[2] == 1) or (state[3] == 2):
                    return False

        elif (state[2] == 0):
            if (state[0] == 1):
                if (state[1] == 3) or (state[3] == 2):
                    return False
            if (state[0] == 2):
                if (state[1] == 1) or (state[3] == 3):
                    return False
            if (state[0] == 3):
                if (state[1] == 2) or (state[3] == 1):
                    return False

        else:
            if (state[0] == 1):
                if (state[1] == 3) or (state[2] == 2):
                    return False
            if (state[0] == 2):
                if (state[1] == 1) or (state[2] == 3):
                    return False
            if (state[0] == 3):
                if (state[1] == 2) or (state[2] == 1):
                    return False
        
        inversion = 0
        for i in range(3, 8):
            for j in range(i + 1, 9):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1
        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):  # changed this
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        state = node.state
        goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
        index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]
        x = 0
        y = 0
        state_index = {}

        for i in range(len(state)):
            state_index[state[i]] = index[i]

        distance = 0

        for i in range(0, 9):
            for j in range(2):
                distance += abs(goal[i][j] - state_index[i][j])

        return distance

    def maximum(self, node): # not done
        a = self.h(node)
        b = self.manhattan(node)

        return max(a, b)

def make_rand_house_puzzle():
    """ This function returns a new instance of an EightPuzzle
    problem with a random initial state that is solvable """

    while(True):
        new_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        random.shuffle(new_state)
        new_state = tuple(new_state)
        new_puzzle = HousePuzzle(Problem(new_state))
        new_puzzle.initial = new_state

        if new_puzzle.check_solvability(new_puzzle.initial) == True:
            return new_puzzle


def house_display(state):
    """ This function takes an 8-puzzle state as input and
    prints a neat and readable representation of it """

    state_ = list(state)
    zero_index = state_.index(0)
    state_[zero_index] = "*"
    print(state_[0], state_[1])
    print(state_[2], state_[3], state_[4], state_[5])
    print(" ", state_[6], state_[7], state_[8])

# time to compare==============================================

print("====================_____HOUSE PUZZLE_____====================\n")

for i in range(0,1):
    puz = make_rand_house_puzzle()
    print("[", i + 1, "] starting puzzle:\n")
    house_display(puz.initial)
    
    print("")

    print("MISPLACED TILES AS HEURISTIC\n")
    start_time = time.time()
    x = best_first_graph_search(puz, puz.h)
    elapsed_time = time.time() - start_time
    print("Time taken:\t", elapsed_time, " seconds")
    steps = 0
    for i in x.path():
        steps += 1
    print("Steps:\t\t", steps)

    print("")
    
    print("MANHATTAN DISTANCE AS HEURISTIC\n")
    start_time = time.time()
    x = best_first_graph_search(puz, puz.manhattan)
    elapsed_time = time.time() - start_time
    print("Time taken:\t", elapsed_time, " seconds")
    steps = 0
    for i in x.path():
        steps += 1
    print("Steps:\t\t", steps)

    print("")

    print("MAX OF THE TWO AS HEURISTIC\n")
    start_time = time.time()
    x = best_first_graph_search(puz, puz.maximum)
    elapsed_time = time.time() - start_time
    print("Time taken:\t", elapsed_time, " seconds")
    steps = 0
    for i in x.path():
        steps += 1
    print("Steps:\t\t", steps)
    print("")


