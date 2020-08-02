# a1.py
# Written by Marco Liang
# May 20, 2020

from search import *
from random import shuffle
import time

#helper functions
def make_rand_8puzzle():
    initial = [i for i in range(9)]
    while True:
        shuffle(initial) #shuffle the initial array
        puzzle = EightPuzzle(initial) #construct the puzzle
        if(puzzle.check_solvability(puzzle.initial)): #check for solvability, if solvable, loop ends
            puzzle.initial = tuple(initial)
            puzzle.state = puzzle.initial
            break
    return puzzle

#displays 8 puzzle, takes in state array
def display(state):
    for i in range(len(state)):
        if(state[i]==0):
            print('*', end=' ')
        else:
            print(state[i], end=' ')
        if((i+1)%3==0):
            print('\n', end='')

def make_rand_duck():
    puzzle = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0)) # create duck puzzle as goal state
    iterations = random.randrange(100,500) #iterations to run for
    puzzle.state = puzzle.initial
    for _ in range(0, iterations):
        act = random.choice(puzzle.actions(puzzle.state)) #choose random action from available ones
        puzzle.state = puzzle.result(puzzle.state, act) #uses result to generate the next state
    puzzle.initial = puzzle.state
    return puzzle

def display_duck(state):
    for i in range(len(state)):
        if(i==6): #there's a gap before index 6 tile
            print('  ', end='')
        if(state[i]==0):
            print('*', end=' ')
        else:
            print(state[i], end=' ')
        if(i==1 or i==5 or i==8):
            print('\n', end='')

#these two helper functions are used for getting the row and col of duck puzzle pieces
def get_row(index):
    if index in [0,1]:
        return 0
    if index in [2,3,4,5]:
        return 1
    if index in [6,7,8]:
        return 2

def get_col(index):
    if index in [0,2]:
        return 0
    if index in [1,3,6]:
        return 1
    if index in [4,7]:
        return 2
    if index in [5,8]:
        return 3

#referencing code from search.py of aima-python code base
#A* search algorithm
def astar_search_modified(problem, h=None):
    start_time = time.time()
    h = memoize(h or problem.h, 'h')
    result = best_first_graph_search_modified(problem, lambda n: n.path_cost + h(n))
    elapsed_time = time.time() - start_time
    print("elapsed time: {}s".format(elapsed_time))
    return result

#mostly same as search.py, but prints node_popped counter and solution length
def best_first_graph_search_modified(problem, f):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    nodes_popped = 0
    while frontier:
        node = frontier.pop()
        nodes_popped = nodes_popped + 1
        if problem.goal_test(node.state):
            print("nodes popped: {}".format(nodes_popped))
            print("length of solution: {}".format(len(node.solution())))
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

#heuristics
def misplaced_tile(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return sum(s != g for (s, g) in zip(node.state, goal))

def manhattan(node):
    goalRow = (2,0,0,0,1,1,1,2,2)
    goalCol = (2,0,1,2,0,1,2,0,1)
    return sum(abs(i/3 - goalRow[s]) + abs(i%3 - goalCol[s]) for i,s in enumerate(node.state))

def max_of_both(node):
    return max(misplaced_tile(node), manhattan(node))

def manhattan_duck(node):
    goalRow = (2,0,0,1,1,1,1,2,2)
    goalCol = (3,0,1,0,1,2,3,1,2)
    return sum(abs(get_row(i) - goalRow[s]) + abs(get_col(i)- goalCol[s]) for i,s in enumerate(node.state))

def max_of_both_duck(node):
    return max(misplaced_tile(node), manhattan_duck(node))

#based on EightPuzzle class of search.py of aima-python code base
class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
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

    def result(self, state, action): #generates the next state based on action
        blank = self.find_blank_square(state)  #blank is the index of the blank square
        new_state = list(state)

        if(blank > 1 and blank < 4):
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state): #returns true if state == goal
        return state == self.goal

def Question2(iterations):
    print("The 8 Puzzle")
    for i in range(1,iterations+1):    
        print("Run {}".format(i))
        s = make_rand_8puzzle()
        display(s.state)
        print("Using misplaced tile heuristic")
        astar_search_modified(s, misplaced_tile)
        print("Using Manhattan distance heuristic")
        astar_search_modified(s, manhattan)
        print("Using max of misplaced tile and Manhattan distance heuristics")
        astar_search_modified(s, max_of_both)

def Question3(iterations):
    print("The Duck Puzzle")
    for i in range(1,iterations+1):    
        print("Run {}".format(i))
        s = make_rand_duck()
        display_duck(s.state)
        print("Using misplaced tile heuristic")
        astar_search_modified(s, misplaced_tile)
        print("Using Manhattan distance heuristic")
        astar_search_modified(s, manhattan_duck)
        print("Using max of misplaced tile and Manhattan distance heuristics")
        astar_search_modified(s, max_of_both_duck)

Question2(10) #run for 10 iterations
Question3(10)