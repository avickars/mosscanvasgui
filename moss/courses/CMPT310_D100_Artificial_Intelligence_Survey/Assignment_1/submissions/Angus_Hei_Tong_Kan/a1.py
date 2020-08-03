# a1.py
# By Angus Kan 

from search import *
import numpy as np
import time 


#Function for making the puzzles
def make_rand_8puzzle():
    state = tuple(np.random.permutation(9))
    puzzle = EightPuzzle(initial = state)
    while not puzzle.check_solvability(state):
        state = tuple(np.random.permutation(9))
        puzzle = EightPuzzle(initial = state)
    return state

def generate_duck_puzzle():
    new_state = tuple(np.array([1,2,3,4,5,6,7,8,0]))
    New_puzzle = DuckPuzzle(initial = new_state)
    number_of_moves = np.random.randint(150,600)
    for _ in range(0, number_of_moves):
        actions = New_puzzle.actions(new_state)
        range_of_moves = len(actions)
        random_move = np.random.choice(range_of_moves)
        new_state = New_puzzle.result(new_state, actions[random_move])
    return new_state

#display functions
def display(state): 
    l = list(state)
    puzzle = EightPuzzle(initial = state)
    blank = puzzle.find_blank_square(state)
    l[blank] = "*"
    state = tuple(l)
    print(state[0], state[1], state[2])
    print(state[3], state[4], state[5])
    print(state[6], state[7], state[8])

def displayDuck(state):
    l = list(state)
    puzzle = DuckPuzzle(initial = state)
    blank = puzzle.find_blank_square(state)
    l[blank] = "*"
    state = tuple(l)
    print(state[0], state[1])
    print(state[2], state[3], state[4], state[5])
    print(' ',state[6], state[7] ,state[8])


#time
def f(problem, h):
    start_time = time.time()
    astar_search(problem, h)
    elapsed_time = time.time() - start_time
    return elapsed_time


#Heuristics
def manhattan(node):
    current_state = node.state
    #puzzle = EightPuzzle(node.state)
    index_goal = {0: [2,2], 1: [0,0], 2: [0,1], 3: [0,2], 4: [1,0], 5: [1,1], 6: [1,2], 7: [2,0], 8: [2,1]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    for i in range(9):
        index_state[current_state[i]] = index[i]
    distance = 0
    
    for i in range(9):
        x1 = index_state[i][0]
        x2 = index_goal[i][0]
        y1 = index_state[i][1]
        y2 = index_goal[i][1]
        distance += abs(x1-x2) + abs(y1-y2)
    
    return distance

def manhattanDuck(node):
    current_state = node.state
    #puzzle = EightPuzzle(node.state)
    index_goal = {0: [2,3], 1: [0,0], 2: [0,1], 3: [1,0], 4: [1,1], 5: [1,2], 6: [1,3], 7: [2,1], 8: [2,2]}
    index_state = {}
    index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
    for i in range(9):
        index_state[current_state[i]] = index[i]
    distance = 0
    
    for i in range(9):
        x1 = index_state[i][0]
        x2 = index_goal[i][0]
        y1 = index_state[i][1]
        y2 = index_goal[i][1]
        distance += abs(x1-x2) + abs(y1-y2)
    
    return distance

def misplaced(node):
   goal_state = (1,2,3,4,5,6,7,8,0)
   return sum(s != g for (s, g) in zip(node.state, goal_state))

def max_h_duck(node):
    return max(manhattanDuck(node), misplaced(node))

def max_h(node):
    return max(manhattan(node), misplaced(node))


# Modified Best first graph search to return number of nodes removed
def nodes_removed_from_frontier(problem, f, display=False):
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
    number_of_nodes = 0
    while frontier:
        node = frontier.pop()
        number_of_nodes = 1 + number_of_nodes
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            solved = node.state
            return number_of_nodes, node.state
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
                    
    return None

#function to solve the DuckPuzzle
def solved_duck(problem, initialstate,  h):
    #Uses function for calculating time
    time_to_solve = f(problem, h)

    #Uses function for calculating length of solution
    puzzle_node = astar_search(problem, h)
    solved = Node
    solved_path = solved.path(puzzle_node)
    length = len(solved_path)

    #Uses function for calculating number of nodes removed from frontier
    nodes_removed = nodes_removed_from_frontier(problem, h)

    if problem.goal_test(nodes_removed[1]):
        print('Problem solved')
        print('Time needed to complete is: {}' .format(time_to_solve))
        print('Length of the solution is: {}' .format(length))
        print('Nodes removed from frontier is: {}' .format(nodes_removed[0]))
        displayDuck(nodes_removed[1])
    else: 
        print("not solved")


#function to solve the EightPuzzle
def solved(problem, initialstate,  h):
    if problem.check_solvability(initialstate):
        #Uses function for calculating time
        time_to_solve = f(problem, h)

        #Uses function for calculating length of solution
        puzzle_node = astar_search(problem, h)
        solved = Node
        solved_path = solved.path(puzzle_node)
        length = len(solved_path)

        #Uses function for calculating number of nodes removed from frontier
        nodes_removed = nodes_removed_from_frontier(problem, h)
        if problem.goal_test(nodes_removed[1]):
            print('Problem solved')
            print('Time needed to complete is: {}' .format(time_to_solve))
            print('Length of the solution is: {}' .format(length))
            print('Nodes removed from frontier is: {}' .format(nodes_removed[0]))
            display(nodes_removed[1])
        else: 
            print("not solved")
    else:
        print("Not solvable")

#Created new class for DuckPuzzle
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
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        if blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank > 3:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
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

#Generates and solves a EightPuzzle 
#Prints the three values needed
def do_EightPuzzle():
    print("EightPuzzle")
    state = make_rand_8puzzle()
    display(state)
    puzzle = EightPuzzle(initial = state)
    print("Using Manhattan heuristics")
    solved(puzzle, state, manhattan)
    print("Using misplaced tiles heuristics")
    solved(puzzle, state, misplaced)
    print("Using max of the misplaced tile heuristic and the Manhattan distance heuristic")
    solved(puzzle, state, max_h)

#Generates and solves a DuckPuzzle 
#Prints the three values needed
def do_DuckPuzzle():
    print("DuckPuzzle")
    state = generate_duck_puzzle()
    displayDuck(state)
    puzzle = DuckPuzzle(initial = state)
    print("Using Manhattan heuristics")
    solved_duck(puzzle, state, manhattanDuck)
    print("Using misplaced tiles heuristics")
    solved_duck(puzzle, state, misplaced)
    print("Using max of the misplaced tile heuristic and the Manhattan distance heuristic")
    solved_duck(puzzle, state, max_h_duck)

#question 1
state = make_rand_8puzzle()
display(state)

do_DuckPuzzle()

do_EightPuzzle()