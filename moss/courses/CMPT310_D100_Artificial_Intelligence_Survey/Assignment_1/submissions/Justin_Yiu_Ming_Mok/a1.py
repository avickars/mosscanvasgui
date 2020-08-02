# a1.py

import random
import time
from itertools import permutations

#returns a new instance of an EightPuzzle problem with a random initial state that is solvable
def make_rand_8puzzle():
    
    #create a permutation list
    perm = list(permutations([0, 1, 2, 3, 4, 5, 6, 7, 8]))
    #state is the variable to collect the randomized values of the permutation
    state = random.choice(perm)
    return state

def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    """ Define goal state and initialize a problem """
    super().__init__(initial, goal)

def find_blank_square(state):
    """Return the index of the blank square in a given state"""

    return state.index(0)

def actions(state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

#derived from https://www.geeksforgeeks.org/sum-manhattan-distances-pairs-points/
def manhattan(x,y,n):
    sum = 0
    for i in range (n):
        for j in range (i+1,n):
            #equation for manhattan distance
            sum += (abs(x[i] - x[j]) + abs(y[i]-y[j]))
    return sum 



    
#takes an 8-puzzle state as input and prints a neat and readable representaito of it
def display(state):
  
    #for each value in state: 0,1,2,3,4,5,6,7,8,9
    for i in range(0,9):
        #if each row has 3 numbers then create a new row
        if(i%3 == 0):
            print("")
          
        #if the value is not 0 then print the value
        
        if(state[i] != 0):
            print(state[i]," ",end = "")

        #0 is the blank and should be printed as a* character
        else:
            print("* ",end = "")


#main method
if __name__=="__main__":

    print("Misplaced Tile Heuristic Search")
    print("")
    start_time = time.time()
    state = make_rand_8puzzle()
    display(state)
    final_time = time.time() - start_time
    print (f'Time (in seconds): {final_time}s')
    print (f'Moves: {actions(state)}')
    print("")
    
    print("Manhattan distance heuristic")
    print("")
    start_time1 = time.time()
    state = make_rand_8puzzle()
    display(state)
    final_time1 = time.time() - start_time1
    x = state
    y = [0,1,2,3,4,5,6,7,8]
    n = len(x)
    print (f'Time (in seconds): {final_time1}s')
    print (f'Moves: {actions(state)}')
    print (f'Manhattan:{manhattan(x,y,n)}')
    print("")
# ...