# a1.py

from search import *

# ...

#Robert Zhou
#CMPT 310
#GO TO MAIN FUNCTION TO CHANGE BETWEEN PUZZLES AND HEURISTICS

from search import EightPuzzle
import random
from queue import PriorityQueue
import sys
import time
import secrets

class DuckPuzzle(Problem): #class template/layout for DuckPuzzle taken from the original EightPuzzle class

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        blank = self.find_blank_square(state)

        if(blank == 0 or blank == 2 or blank == 6):
            possible_actions.remove('LEFT')
        if(blank == 0 or blank == 1 or blank == 4 or blank == 5):
            possible_actions.remove('UP')
        if(blank == 1 or blank == 5 or blank == 8):
            possible_actions.remove('RIGHT')
        if(blank == 2 or blank == 6 or blank == 7 or blank == 8):
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        up = 0
        down = 0
        if(blank == 2 or blank == 3):
            up = -2
        elif(blank == 6 or blank == 7 or blank == 8):
            up = -3
        if(blank == 0 or blank == 1):
            down = 2
        elif(blank == 3 or blank == 4 or blank == 5):
            down = 3
        delta = {'UP': up, 'DOWN': down, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))


def make_rand_8puzzle():

    if(type == "duck"): #for duckpuzzle, specify type variable as "duck"
        initial = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        puzzle = DuckPuzzle(tuple(initial))
        puzzle.state = tuple(initial)
        for x in range(random.randint(75,475)):
        #using random shuffling on the goal state (between 75-475 times, random choice each time)
            cc = puzzle.actions(puzzle.state)
            dc = secrets.choice(cc)
            puzzle.state = puzzle.result(puzzle.state, dc)
        return puzzle
        
    #otherwise, normal eightpuzzle
    initial = [6, 7, 1, 8, 3, 2, 4, 0, 5]
    puzzle = EightPuzzle(tuple(initial))
    """
    puzzle.state = tuple(initial)
    for x in range(random.randint(50,300)):
        cc = puzzle.actions(puzzle.state)
        dc = secrets.choice(cc)
        puzzle.state = puzzle.result(puzzle.state, dc)
    #this is the randomly moving tiles method. I decided to use check_solvability instead for eightPuzzle
    #but this method is still used in duckPuzzle
    #also, it can't be used with the current 'initial' because that layout is unsolvable
    """
    solvable = 0
    while solvable == 0:
        random.shuffle(initial)
        if puzzle.check_solvability(initial) == True: #using check_solvability function from the included search.py
            solvable = 1
    puzzle.state = tuple(initial)
    return puzzle

def display(state):

    if(type == "duck"): #for duckpuzzle, specify type variable as "duck"
        state = list(state)
        displayer = ''.join(str(i) for i in state)
        displayer = displayer.replace("0", "*")
        print(displayer[0] + ' ' + displayer[1] + '\n' + displayer[2] + ' ' + displayer[3] + ' ' + displayer[4] + ' ' + displayer[5] + '\n  ' + displayer[6] + ' ' + displayer[7] + ' ' + displayer [8] + '\n')
        return
        
    #otherwise, normal eightpuzzle
    state = list(state)
    displayer = ''.join(str(i) for i in state)
    displayer = displayer.replace("0", "*")
    print(displayer[0] + ' ' + displayer[1] + ' ' + displayer[2] + '\n' + displayer[3] + ' ' + displayer[4] + ' ' + displayer[5] + '\n' + displayer[6] + ' ' + displayer[7] + ' ' + displayer[8] + '\n')

def manhattan(puzzle, state):

    if(type == "duck"): #for duckpuzzle, specify type variable as "duck"
        """
        coordinates = {0:(0,0), 1:(1,0), 2:(0,1),
                       3:(1,1), 4:(2,1), 5:(3,1),
                       6:(1,2), 7:(2,2), 8:(3,2)}
        """
        coordinates = {0:(0,0), 1:(1,0), 2:(2,0),
                       3:(0,1), 4:(1,1), 5:(2,1),
                       6:(0,2), 7:(1,2), 8:(2,2)}
        h = 0
        for i in state:
            x1, y1 = coordinates[state[i]]
            x2, y2 = coordinates[puzzle.goal[i]]
            h = h + abs(x1-x2) + abs(y1-y2)
        return h
    #manhattan distance method for duckpuzzle adapted 
    #from https://www.csee.umbc.edu/courses/671/fall09/code/python/p8.py
    #found via https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game

    #otherwise, normal eightpuzzle
    return sum(abs(x%3 - y%3) + abs(x//3 - y//3) for x, y in ((state.index(i), puzzle.goal.index(i)) for i in range(1, 9)))
    #manhattan distance method adapted from stackexchange
    #https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
    
def misplaced(puzzle, state): 
    #the same default heuristic from search.py
    #but modified to take the 'state' instead of the entire puzzle to get puzzle.state
    #so it can be used without having to create new puzzle classes everytime
    return sum(s != g for (s, g) in zip(state, puzzle.goal))
    """
    count = 0
    for i in state:
        if(state[i] != puzzle.goal[i] and state[i] != 0):
            count = count+1
    return count
    """
    
def a_star(puzzle, heuristic):
    frontier = PriorityQueue()
    initial = puzzle.state
    if(heuristic == "misplaced"):
        frontier.put((misplaced(puzzle, initial), initial))
    elif(heuristic == "manhattan"):
        frontier.put((manhattan(puzzle, initial), initial))
    elif(heuristic == "max"):
        maxHeuristic = max((misplaced(puzzle, initial)), (manhattan(puzzle, initial)))
        frontier.put((maxHeuristic, initial))
    else:
        sys.exit("Please give the program a heuristic of 'misplaced', 'manhattan', or 'max' and try again.")
    visited = []
    actions = {}
    cost = {}
    depth = {}
    actions[initial] = list()
    cost[initial] = 0
    depth[initial] = 0
    while(frontier.empty() == False):
        current = frontier.get()
        visited.append(current[1])
        if(current[1] == puzzle.goal):
            display(current[1])
            return (actions[current[1]], len(visited), len(actions[current[1]]))
        nextActions = puzzle.actions(current[1])
        f = current[0]
        for next in nextActions:
            state = puzzle.result(current[1], next)
            depth[state] = depth[current[1]]+1
            if state not in visited:
                if(heuristic == "misplaced"):
                    cost[state] = depth[state] + misplaced(puzzle, state)
                    actions[state] = list(actions[current[1]]) + list(next[0])
                    frontier.put((cost[state], state))
                    display(state)
                elif(heuristic == "manhattan"):
                    cost[state] = depth[state] + manhattan(puzzle, state)
                    actions[state] = list(actions[current[1]]) + list(next[0])
                    frontier.put((cost[state], state))
                    display(state)
                elif(heuristic == "max"):
                    cost[state] = depth[state] + max((misplaced(puzzle, state)), (manhattan(puzzle, state)))
                    actions[state] = list(actions[current[1]]) + list(next[0])
                    frontier.put((cost[state], state))
                    display(state)
    sys.exit("The given puzzle is unsolvable.")

#main
type = "eight" #choose "eight" puzzle or "duck" puzzle
heuristic = "manhattan" #choose "misplaced" tile heuristic or "manhattan" distance heuristic or "max" of the two heuristic

#NOTE: when calculating for heuristics, I read that we were supposed to not include the tile with 0
#but I had already run all my tests (11 *3 *2 of them) with 0 included and I didn't want to redo them
#and later I heard that you said in tutorial it was okay if we included it, so I hope that's okay.
#ex. I still have the excluding-0 version of misplaced tile heuristic commented out

puzzle = make_rand_8puzzle()
initial = puzzle.state
display(initial)


t = time.time()
(actions, expanded, moves) = a_star(puzzle, heuristic)
timing = time.time() - t

print("Original puzzle was: ")
display(initial)
print("Expanded a total of", expanded, "nodes using", heuristic, "heuristic.")
print("Solution was found in", timing, "seconds, with a total of", moves, "moves.")
print(actions)
