import numpy as np
from search import *
import time
#**********************
#Q1
#**********************
def make_rand_8puzzle():
    while True: 
        random_state = tuple(np.random.permutation(9))
        puzzle = EightPuzzle(initial=random_state)
        if puzzle.check_solvability(random_state):
            return random_state


state = tuple(np.random.permutation(9))
dummy_puzzle = EightPuzzle(initial=state)

def display(state):
    for index in range(9):
        temp = state[index]
        if(temp == 0):
            temp = "*"
        if (index + 1) % 3 == 0:
            print(temp, " ")
        else:
            print(temp, " ", end ='')
    
    print(" ")

#**********************
#Q2
#**********************

def my_best_first_graph_search(problem, f, display=False):
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
    total_cost = 0
    while frontier:
        node = frontier.pop()
        total_cost += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, total_cost
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, total_cost

def my_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return my_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def manhattan_h(node):
    goal_state = {1:[0,0],2:[1,0],3:[2,0],4:[0,1],5:[1,1],6:[2,1],7:[0,2],8:[1,2],0:[2,2]}
    current_state = {node.state[0]:[0,0],node.state[1]:[1,0],node.state[2]:[2,0],node.state[3]:[0,1],node.state[4]:[1,1],node.state[5]:[2,1],node.state[6]:[0,2],node.state[7]:[1,2],node.state[8]:[2,2]}
    total = 0
    for index in range(0,9):
        x_dif = abs(current_state[index][0] - goal_state[index][0])
        y_dif = abs(current_state[index][1] - goal_state[index][1])
        #print(index,": ",x_dif+y_dif)
        total += (x_dif+y_dif)
    return total

def max_h(node):
    puzzle = EightPuzzle(node.state)
    return max(manhattan_h(node), puzzle.h(node))


for x in range (10):
    #creating puzzle
    initial_state = make_rand_8puzzle()
    puzzle = EightPuzzle(initial_state)
    print("Puzzle #",x,": Puzzle to solve.")
    display(initial_state)
    
    #solving puzzle with misplaced tile heuristic
    print("Puzzle #",x,": misplaced tile heuristic.")
    start_time = time.time()
    result, removed = my_astar_search(puzzle)
    finish_time = time.time()
    moves = result.solution()
    
    print("Time: ",finish_time-start_time)
    print("Tile Moves: ", len(moves))
    print("Nodes Removed: ",removed,"\n")

    #solving puzzle with tile manhattan distance heuristic
    print("Puzzle #",x,": manhantan distance heuristic.")
    start_time = time.time()
    result, removed = my_astar_search(puzzle,h=manhattan_h)
    finish_time = time.time()
    moves = result.solution()

    print("Time: ",finish_time-start_time)
    print("Tile Moves: ", len(moves))
    print("Nodes Removed: ",removed,"\n")

    print("Puzzle #",x,": max of manhantan distance heuristic and tile misplacement heuristic.")
    start_time = time.time()
    result, removed = my_astar_search(puzzle,h=max_h)
    finish_time = time.time()
    moves = result.solution()
    print("Time: ",finish_time-start_time)
    print("Tile Moves: ", len(moves))
    print("Nodes Removed: ",removed,"\n")


#**********************
#Q3
#**********************

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

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square >= 6:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        else:
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


#Manhattan heuristic function for duck puzzle
def duck_manhattan_h(node):
    goal_state = {1:[0,0],2:[1,0],3:[0,1],4:[1,1],5:[2,1],6:[3,1],7:[1,2],8:[2,2],0:[3,2]}
    current_state = {node.state[0]:[0,0],node.state[1]:[1,0],node.state[2]:[0,1],node.state[3]:[1,1],node.state[4]:[2,1],node.state[5]:[3,1],node.state[6]:[1,2],node.state[7]:[2,2],node.state[8]:[3,2]}
    total = 0
    for index in range(0,9):
        x_dif = abs(current_state[index][0] - goal_state[index][0])
        y_dif = abs(current_state[index][1] - goal_state[index][1])
        #print(index,": ",x_dif+y_dif)
        total += (x_dif+y_dif)
    return total

def duck_max_h(node):
    puzzle = DuckPuzzle(node.state)
    return max(duck_manhattan_h(node), puzzle.h(node))


def display_duckpuzzle(state):
    print(state[0]," ",state[1])
    print(state[2]," ",state[3]," ",state[4]," ",state[5]," ")
    print("   ",state[6]," ",state[7]," ",state[8]," ")

def make_rand_duckpuzzle():
    #Set initial state as goal state
    current_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = DuckPuzzle(initial = current_state)
    #Randomly shuffle the puzzle to get a random solvable state
    for x in range(0,5000): 
        possible_actions = puzzle.actions(current_state)
        current_state = puzzle.result(action=random.choice(possible_actions),state=current_state)
    return current_state

for x in range (10):
    #creating puzzle
    initial_state = make_rand_duckpuzzle()
    puzzle = DuckPuzzle(initial_state)
    print("Puzzle #",x,": Puzzle to solve.")
    display_duckpuzzle(initial_state)
    

    #solving puzzle with tile misplacement heuristic
    print("Puzzle #",x,": tile heuristic.")
    start_time = time.time()
    result, removed = my_astar_search(puzzle)
    finish_time = time.time()
    moves = result.solution()
    print(finish_time-start_time,",",len(moves),",",removed, end=',')
    print("Time: ",finish_time-start_time)
    print("Tile Moves: ", len(moves))
    print("Nodes Removed: ",removed,"\n")

    #solving puzzle with tile manhattan distance heuristic
    print("Puzzle #",x,": manhantan distance heuristic.")
    start_time = time.time()
    result, removed = my_astar_search(puzzle,h=duck_manhattan_h)
    finish_time = time.time()
    moves = result.solution()
    print(finish_time-start_time,",",len(moves),",",removed, end=',')
    print("Time: ",finish_time-start_time)
    print("Tile Moves: ", len(moves))
    print("Nodes Removed: ",removed,"\n")

    print("Puzzle #",x,": max of manhantan distance heuristic and tile misplacement heuristic.")
    start_time = time.time()
    result, removed = my_astar_search(puzzle,h=duck_max_h)
    finish_time = time.time()
    moves = result.solution()
    print(finish_time-start_time,",",len(moves),",",removed)

