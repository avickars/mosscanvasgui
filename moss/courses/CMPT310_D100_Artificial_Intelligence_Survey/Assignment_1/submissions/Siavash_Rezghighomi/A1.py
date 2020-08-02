# a1.py
from search import *
from utils import *
import random
import time
import numpy as np

### Question 1
def make_rand_8puzzle():
    initialState = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(initialState)
    rand_puzzle = EightPuzzle(tuple(initialState), (1,2,3,4,5,6,7,8,0))
    tempTuple = tuple(initialState)
    while rand_puzzle.check_solvability(tempTuple) != 1:
        random.shuffle(initialState)
        rand_puzzle = EightPuzzle(tuple(initialState), (1,2,3,4,5,6,7,8,0))
        tempTuple = tuple(initialState) 
    return rand_puzzle

def display(state):
    for i in range(0,9):
        if (i % 3 == 0):
            print("")
        if (state[i] != 0):
            print(state[i], " ", end = "")
        else:
            print("* ", "", end = "")
    print()



### Question 2
### Part1: A*Search - Misplaced tile heuristic
def heuristicValue(node):
    """ Return the heuristic value for a given state. Default heuristic function used is
    h(n) = number of misplaced tiles """
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
    return sum(s != g for (s, g) in zip(node.state, goal))

### Part2: A*Search - Manhattan heuristic
def manhattanDistance(node):
        state = node.state
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhd = 0

        for i in range(1,9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

        return mhd   

def astar_manhattanSearch(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

### Part3: A*Search - Max heuristic
def maxHeuristicValue(node):
        misplaced = heuristicValue(node)
        manhattan = manhattanDistance(node)
        return (max(misplaced, manhattan))

def astar_maxHeuristicSearch(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)



### Question3
class DuckPuzzle(Problem):
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
        if index_blank_square == 1:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        if index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 6:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        if blank == 0:
            delta = {'UP': 0, 'DOWN': 2, 'LEFT': 0, 'RIGHT': 1}
        if blank == 1:
            delta = {'UP': 0, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 0}
        if blank == 2:
            delta = {'UP': -2, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}
        if blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank == 4:
            delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank == 5:
            delta = {'UP': 0, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 0}
        if blank == 6:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 1}
        if blank == 7:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
        if blank == 8:
            delta = {'UP': -3, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 0}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

def make_rand_DuckPuzzle(DuckPuzzle):
    initialState = DuckPuzzle.initial
    for i in range (1,50):
        temp_action = DuckPuzzle.actions(initialState)
        temp_puzzle = random.choice(temp_action)
        initialState = DuckPuzzle.result(initialState, temp_puzzle)
    DuckPuzzle.initial = initialState
    return DuckPuzzle


def main():
    print("Beginning of the main function: ")

### Question 1
if __name__ == "__main__":
    main()
    testPuzzle = make_rand_8puzzle()
    tempState = (0, 3, 2, 1, 8, 7, 4, 6, 5)
    display(tempState)
    display(testPuzzle.initial)
    print("") 
    print("End of question 1") 
    print("") 



### Question 2
## Part1: A*Search - Misplaced tile heuristic
print("Question2 - Part1: Misplaced tile heuristic")
for i in range (1,16):
    print(i)
    tempPuzzle = make_rand_8puzzle()
    start = time.time()
    tempNode = astar_search(tempPuzzle, h=heuristicValue)
    end = time.time() - start
    print("Total running time in seconds:", end)
    print("Nodes removed from frontier:", tempNode[1])
    print("Path cost is:", len(tempNode[0].path())) 
    print("") 
    
### Part2: A*Search - Manhattan heuristic
print("Question2 - Part2: Manhattan Search")
for i in range(1,16):
    print(i)
    tempPuzzle = make_rand_8puzzle()
    start = time.time()
    tempNode = astar_manhattanSearch(tempPuzzle, h=manhattanDistance)
    end = time.time() - start
    print("Total running time in seconds:", end)
    print("Nodes removed from frontier:", tempNode[1])
    print("Path cost is:", len(tempNode[0].path())) 
    print("") 

### Part3: A*Search - Max heuristic
for i in range(1,16):
    print("Question2 - Part3: Max Heuristic Search")
    print(i)
    tempPuzzle = make_rand_8puzzle()
    start = time.time()
    tempNode = astar_maxHeuristicSearch(tempPuzzle, h=maxHeuristicValue)
    end = time.time() - start
    print("Total running time in seconds:", end)
    print("Nodes removed from frontier:", tempNode[1])
    print("Path cost is:", len(tempNode[0].path())) 
    print("") 
print("End of question 2") 
print("") 



### Question 3
### Part1: A*Search - Misplaced tile heuristic
print("Question3 - Part1: Misplaced tile heuristic")
for i in range (1,16):
    print(i)
    abc = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))
    tempPuzzle = make_rand_DuckPuzzle(abc)
    start = time.time()
    temp1, temp2 = astar_search(tempPuzzle, h=heuristicValue)
    end = time.time() - start
    print("Total running time in seconds:", end)
    print("Nodes removed from frontier:", temp2)
    print("Path cost is:", len(temp1.solution()))
    print("") 

### Part2: A*Search - Manhattan heuristic
print("Question3 - Part2: Manhattan Search")
for i in range(1,16):
    print(i)
    abc = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))
    tempPuzzle = make_rand_DuckPuzzle(abc)
    start = time.time()
    temp1, temp2 = astar_manhattanSearch(tempPuzzle, h=manhattanDistance)
    end = time.time() - start
    print("Total running time in seconds:", end)
    print("Nodes removed from frontier:", temp2)
    print("Path cost is:", len(temp1.solution()))
    print("") 

### Part3: A*Search - Max heuristic
print("Question3 - Part3: Max Heuristic Search")
for i in range(1,16):
    print(i)
    abc = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))
    tempPuzzle = make_rand_DuckPuzzle(abc)
    start = time.time()
    temp1, temp2 = astar_maxHeuristicSearch(tempPuzzle, h=maxHeuristicValue)
    end = time.time() - start
    print("Total running time in seconds:", end)
    print("Nodes removed from frontier:", temp2)
    print("Path cost is:", len(temp1.solution()))
    print("") 
print("End of question 3") 