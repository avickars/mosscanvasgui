#a1.py

import statistics
import random
import time
from search_a1 import *

""" ======================================== Q1 ======================================= """
""" Q1 - Part 1 """
""" 
Return an instance of an EightPuzzle problem
    a- random initial state
    b- solvable
"""
def make_rand_8puzzle():

    lock = True
    
    while lock:
        values = generateGameState()
        epInst = EightPuzzle(values)
        if epInst.check_solvability(values):
            lock = False

    return epInst


def generateGameState():
    """ Initial Values Array (for random tuple)"""
    values = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    """ Generate random tuple (of 1 to 8) for initial state """
    random.shuffle(values)
    return tuple(values)


""" Q1 - Part 2 """
"""
Take an EightPuzzle state as input and print a neat and readable representation
    a- 0 is the blank and should be represented as '*'
"""
def display(state):
    for i in range(len(state)):
        print(state[i], end = ' ')
        if i > 0 and (i+1) % 3 == 0:
            print('\n')
    print('\n')



""" ======================================== Q2 ======================================= """

""" Search using Manhattan Distance heuristic """
def astar_search_manhattandist(problem, manDist=None, display=False):
    """ Q2 Modification (1) """
    start_time = time.time()

    """ A* search using manhattan distance instead of misplaced tile """
    manDist = memoize(manDist or problem.manDist, 'manDist')
    returnNode = best_first_graph_search_tracking(problem, lambda n: n.path_cost + manDist(n), display)

    """ Q2 Modification (1) -Taken from Assignment 1 Documentation"""
    elapsed_time = time.time() - start_time
    print(f'Elapsed time for manhattan distance search (in seconds): {elapsed_time}s')
    return returnNode

""" Search using the MAX of Misplaced Tile heurisitic and Manhattan Distance heuristic """
def astar_search_max_hybrid(problem, hFactor=None, display=False):
    """ Q2 Modification (1) """
    start_time = time.time()

    """ A* search using max between manhattan distance and misplaced tile """
    manDist = memoize(hFactor or problem.manDist, 'manDist')
    h = memoize(hFactor or problem.h, 'h')
    returnNode = best_first_graph_search_tracking(problem, lambda n: n.path_cost + max(h(n), manDist(n)), display)

    """ Q2 Modification (1) -Taken from Assignment 1 Documentation"""
    elapsed_time = time.time() - start_time
    print(f'Elapsed time for hybrid search (in seconds): {elapsed_time}s')
    return returnNode


""" ======================================== Q3 ======================================= """



""" DuckPuzzle Class """ 
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
        ibs = index_blank_square

        if ibs == 0 or ibs == 2 or ibs == 6:
            possible_actions.remove('LEFT')
        if ibs == 1 or ibs == 5 or ibs == 8:
            possible_actions.remove('RIGHT')
        if ibs == 0 or ibs == 1 or ibs == 4 or ibs == 5:
            possible_actions.remove('UP')
        if ibs == 2 or ibs == 6 or ibs == 7 or ibs == 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': 0, 'DOWN': 1, 'LEFT': 2, 'RIGHT': 3}

        """ Switch Case: for each index, provides index change values for up, down, left, right """
        switch = {
            0: (0, 2, 0, 1),
            1: (0, 2, -1, 1),
            2: (-2, 0, 0, 1),
            3: (-2, 3, -1, 1),
            4: (0, 3, -1, 1),
            5: (0, 3, -1, 0),
            6: (-3, 0, 0, 1),
            7: (-3, 0, -1, 1),
            8: (-3, 0, -1, 0)
        }

        neighbor = blank + switch.get(blank)[delta[action]]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        return sum(s != g for (s, g) in zip(node.state, self.goal))

    """ Q2 - A) Manhattan distance heuristic """
    def manDist(self, node):
        sumDist = 0        
        initialState = node.state
        goalState = self.goal

        for i in range(len(initialState)):
            """ Find index of node value in goal state """
            indexGoal = int(goalState.index(initialState[i]))
            indexInitial = int(i)

            """ Sum of horizontal and vertical distance """
            manDistNode = abs((indexInitial//3)-(indexGoal//3)) + abs((indexInitial%3)-(indexGoal%3))
            
            """ Add to sum of distances """
            sumDist += manDistNode

        return sumDist

    

""" Duck Puzzle Functions """
def display_duck(state):
    print(state[0], end = ' ')
    print(state[1])
    print(state[2], end = ' ')
    print(state[3], end = ' ')
    print(state[4], end = ' ')
    print(state[5])
    print(' ', end = ' ')
    print(state[6], end = ' ')
    print(state[7], end = ' ')
    print(state[8])
    print('\n')


def make_rand_duckPuzzle():
    initalValues = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    state = initalValues       
    dpStart = DuckPuzzle(initalValues)

    """ Make 100-200 random moves from goal state to reach a valid starting state """
    for i in range(random.randint(100,200)):
        #pick random action from possible actions
        actionList = dpStart.actions(state)
        randomAction = random.choice(actionList)
        state = dpStart.result(state, randomAction)

    dpInst = DuckPuzzle(state)
    return dpInst

def main():
    """ Q2 - Make 10 random EightPuzzle states """
    print("EightPuzzle : Creating and Solving 10 random puzzles")
    EightPuzzleArray = [0] * 10
    for i in EightPuzzleArray:
        EightPuzzleArray[i] = make_rand_8puzzle()

        """ Default A* search """
        astar_search(EightPuzzleArray[i])
            
        """ Manhattan Distance A* search """
        astar_search_manhattandist(EightPuzzleArray[i])

        """ Hybrid A* search """
        astar_search_max_hybrid(EightPuzzleArray[i])

        """ For ease of reading """    
        print("\n")
    
    
    """ Q3 - Make random DuckPuzzle states """
    print("DuckPuzzle : Creating and Solving 10 random puzzles")
    DuckPuzzleArray = [0] * 10
    for i in DuckPuzzleArray:
        DuckPuzzleArray[i] = make_rand_duckPuzzle()

        """ Default A* search """
        astar_search(DuckPuzzleArray[i])

        """ Manhattan Distance A* search """
        astar_search_manhattandist(DuckPuzzleArray[i])

        """ Hybrid A* search """
        astar_search_max_hybrid(DuckPuzzleArray[i])

        """ For ease of reading """    
        print("\n")

if __name__ == "__main__":
    main()