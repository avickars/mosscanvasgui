"""
Assignment 1 file for running 8-Puzzle, Duck Puzzle and finding the A* algortihym optimality

"""

# Imports required for this file to run. 
import random
import time
import csv
from utils import memoize, PriorityQueue
from search import EightPuzzle, Node, Problem


class EightPuzzleGame(EightPuzzle):
    '''
    EightPuzzleGame class derived from EightPuzzle.
    -> calculateMissplacedTiles() - for calculating the missplaced tiles heurstic ( parent class uses 0 as tiles so need overwrite)
    -> calculateManhattenDist()   - for calculating the manhatten distance
    -> maxH()                     - for max of both heurstic
    Have not counted 0 as the tiles in this assignment and has followed the textbook. '''

    def __init__(self, initial):
        super().__init__(initial)

    def calculateMissplacedTiles(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal) if s != 0)

    def calculateManhattenDist(self,node):
        h_value = 0
        for i, number in enumerate(node.state):
            if number:
                # This formula is derived from patern finding. Modulo oprartor gives x val and floor devision gives y val
                #   so manhatten distance = abs(x-x1) + abs(y-y1)
                #   this is more neat approch than the hardcorded value approch. 
            
                h_value += abs((number-1)%3 - i%3) + abs((number-1)//3 - i//3)
        return h_value

    def maxH(self, node):
        return max(self.calculateManhattenDist(node), self.calculateMissplacedTiles(node))


class DuckPuzzle(Problem):
    '''
    DuckPuzzle class derived from Problem.
    -> calculateMissplacedTiles() - for calculating the missplaced tiles heurstic ( parent class uses 0 as tiles so need overwrite)
    -> calculateManhattenDist()   - for calculating the manhatten distance
    -> maxH()                     - for max of both heurstic
    -> actions(), check_solvability(), results() have been changed to fulfill the requirments. 
    Have not counted 0 as the tiles in this assignment and has followed the textbook. '''

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
        leftMoveAllowed =  (1,5,8,3,4,7)
        rightMoveAllowed = (0,2,6,3,4,7)
        downMoveAllowed =  (0,1,3,4,5)
        upMoveAllowed =    (2,3,6,7,8)
        if index_blank_square not in leftMoveAllowed:
            possible_actions.remove('LEFT')
        if index_blank_square not in rightMoveAllowed:
            possible_actions.remove('RIGHT')
        if index_blank_square not in upMoveAllowed:
            possible_actions.remove('UP')
        if index_blank_square not in downMoveAllowed:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if (blank in (0,1)): delta['DOWN'] = 2
        if (blank in (2,3)): delta['UP'] = -2

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        # for it to be solvable first 3 index should have 1,2,3 only 
        # Reason is because 1,2,3 can not be moved to the second block which is show below. 
        #  |1|2|            First Block:  |1|2|     Second Block:  
        #  |3|0|4|5|                      |2|0|                    |0|4|5|
        #    |6|7|8|                                               |6|7|8|         
        # Zero is empty space and it is not possible to move 1,2,3 to the 2nd and 3rd row(second block.)
        # Given the width of the first block to be 2. It would be only solvable if the inversion is odd if zero is in first row. 
        # For second block, it would be solvable if inversions are even. Credits given to below source. 
        # https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html

        validSet = (1,2,3)
        if (state[0] not in validSet or state[1] not in validSet or state[2] not in validSet):
            return None

        # find inversion for the first for indexes 
        inversionFirst = 0
        for i in range(0,3):
            for j in range(i+1, 4):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversionFirst += 1
        # find the inversion for the second block and must be even in order to be solvble
        inversionSecond = 0
        for i in range(3, len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversionSecond += 1   
        
        # # blank is the index of the blank square
        blank = self.find_blank_square(state)

        # solvable if only zero is on the first row and it has to be odd inversion for the frist block. 
        if ( blank < 2 and inversionFirst % 2 != 0):
            return inversionSecond % 2 == 0
        else:
            return (inversionFirst % 2 == 0 and inversionSecond % 2 == 0)

    def calculateMissplacedTiles(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal) if s != 0)

    def calculateManhattenDist(self,node):
        dictIndexCord     = { 0: (1,1), 1: (1,2), 2: (2,1), 3: (2,2) , 4: (2,3), 5: (2,4) , 6: (3,2), 7: (3,3), 8: (3,4)  }
        dictGoalCord = { 1: (1,1), 2: (1,2), 3: (2,1), 4: (2,2) , 5: (2,3), 6: (2,4) , 7: (3,2), 8: (3,3) }

        h_value = 0
        for i, num in enumerate(node.state):
            if (num == 0): continue
            h_value += abs( dictIndexCord[i][0] - dictGoalCord[num][0]) + abs( dictIndexCord[i][1] - dictGoalCord[num][1])
        
        return h_value

    def maxH(self, node):
        return max(self.calculateManhattenDist(node), self.calculateMissplacedTiles(node))

    def display(self, state):
        print (state[0], state[1])
        print (state[2], state[3],state[4], state[5])
        print (" ", state[6], state[7], state[8])


## below function code is from the search.py with some modification.
def astar_search(problem, h, display, row):
    """ Modifications are made for counting the poped nodes from frontier and for statstics generation. """

    h = memoize(h or problem.h, 'h')
    f = memoize(lambda n: n.path_cost + h(n), 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    frontierPopCount = 0
    start_time = time.time()
    while frontier:
        node = frontier.pop()
        frontierPopCount += 1
        if problem.goal_test(node.state):
            if display:
                print("Solution:", node.depth, "Nodes poped from fontier:", frontierPopCount)
            elapsed_time = time.time() - start_time
            row.extend([elapsed_time, node.depth, frontierPopCount])
            return node, row
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def display(state):
    #clousure function
    def printer(str):
        print (str, end ='')

    for index, number in enumerate(state):
        printer(number) if (number != 0 ) else printer("*")
        printer("\n") if ( (index + 1) % 3 == 0 and index != 0 ) else printer(" ")
    
    # I have assumed that at the end there is carrige return based on the look given on the assignment page. 


def make_rand_8puzzle():
    while True:
        initialPuzzel = tuple(random.sample( range(0,9), 9))
        puzzel = EightPuzzleGame(initialPuzzel)
        if (puzzel.check_solvability(puzzel.initial)):
            return puzzel


def make_rand_duckpuzzle():
    while True:
        initialPuzzel = tuple(random.sample( range(0,9), 9))
        puzzel = DuckPuzzle(initialPuzzel)
        if (puzzel.check_solvability(puzzel.initial)):
            return puzzel


def paly_the_game(gameName, samples):
    '''
    This is function to run all the samples to solve puzzle using the A* search with different heurstics. 
    '''
    for i in range(0, samples):
        tempPuzzel = gameName()
        print ("Sample #:",tempPuzzel.initial)
        row = [ i+1 ,tempPuzzel.initial]
        node, row = astar_search(tempPuzzel, tempPuzzel.calculateManhattenDist, False, row)
        node, row = astar_search(tempPuzzel, tempPuzzel.calculateMissplacedTiles, False, row)
        node, row = astar_search(tempPuzzel, tempPuzzel.maxH, False, row)

        with open('a1.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)


"""
To generate the statistics for the algorithm performance. Uncomment the bellow function. 
It will create file called a1.csv where you would able to see the data.
Also make sure for 8puzzle it takes time to run so limit your sample number. 
"""
# paly_the_game(make_rand_duckpuzzle, 1)
