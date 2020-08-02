# a1.py
# Name: Kay Arellano
# ID (Student #): karellan (301316684)

from search import *

import random
import time

duck_orientation = [[0,1,1,2,3,4,3,4,5],
                    [1,0,2,1,2,3,2,3,4],
                    [1,2,0,1,2,3,2,3,4],
                    [2,1,1,0,1,2,1,2,3],
                    [3,2,2,1,0,1,2,1,2],
                    [4,3,3,2,1,0,3,2,1],
                    [3,2,2,1,2,3,0,1,2],
                    [4,3,3,2,1,2,1,0,1]]

''' QUESTION 1 '''
def make_rand_8puzzle():
    tmp = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while 1:
        # generate a random list
        random.shuffle(tmp)

        # check if puzzle is solvable
        gen_puzzle = EightPuzzle(tuple(tmp))
        if gen_puzzle.check_solvability(tuple(tmp)):
            return gen_puzzle

def display(state):
    # replace 0 to '*'
    new_state = list(state)
    new_state[state.index(0)] = '*'

    # print puzzle
    i = 0
    while i < 9:
        print(str(new_state[i]) + ' ' + str(new_state[i+1]) + ' ' + str(new_state[i+2]))
        i += 3

''' QUESTION 2 '''
# (0,0) | (1,0) | (2,0)
# (0,1) | (1,1) | (2,1)
# (0,2) | (1,2) | (2,2)

# modified default heuristic function from EightPuzzle class
def mt_heuristic(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return sum((s != g) and (s != 0) for (s, g) in zip(node.state, goal))

def md_heuristic(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    cur = node.state
    md_sum = 0

    # find x and y positions
    for (i, j) in zip(cur, goal):
        if i != j and i != 0:
            row = abs(int(goal.index(i)%3) - int(cur.index(i)%3))
            col = abs(int(goal.index(i)/3) - int(cur.index(i)/3))
            md_sum += (row + col) 
 
    return md_sum

def max_h(node):
    puzzle = EightPuzzle(node)
    return max(md_heuristic(node), puzzle.h(node))

def q2_results():
    print("\nUsing Eight Puzzle Board:")

    cur_puzzle = make_rand_8puzzle()
    display(cur_puzzle.initial)

    ''' A*-search algorithm w/ misplaced tile heuristic
        --> misplaced tile heuristic: # of tiles not in goal state'''
    print("A*-search using Misplaced Tile Heuristic:")
    mt_start = time.time()
    astar_search_2(cur_puzzle, mt_heuristic, False)
    mt_end = (time.time() - mt_start)
    print("Total running time (seconds): " + str(mt_end) + "\n")

    ''' A*-search algorithm w/ Manhattan heuristic
        --> Manhattan heuristic: sum of distances b/w 
            current tile position and goal position'''
    print("A*-search using Manhattan Distance Heuristic:")
    md_start = time.time()
    astar_search_2(cur_puzzle, md_heuristic, False)
    md_end = (time.time() - md_start)
    print("Total running time (seconds): " + str(md_end) + "\n")

    ''' A*-search algorithm w/ max of Manhattan heuristic
        and misplaced tile heuristic'''
    print("A*-search using Maximum Heuristic:")
    max_start = time.time()
    astar_search_2(cur_puzzle, max_h, False)
    max_end = (time.time() - max_start)
    print("Total running time (seconds): " + str(max_end) + " \n")

''' QUESTION 3 '''
def make_rand_DuckPuzzle():
    duck = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))
    length = random.choice(range(15,100))
    cur = duck.initial
    chosen_act = 'init'

    i = 0
    while i <= length:
        # fetch possible actions and choose random action
        acts = duck.actions(cur)
        if cur != duck.initial:
            if chosen_act == 'UP':  opp = 'DOWN'
            elif chosen_act == 'DOWN':  opp = 'UP'
            elif chosen_act == 'LEFT':  opp = 'RIGHT'
            else: opp = "LEFT" 
            acts.remove(opp)    # remove the action going to its previous state
        chosen_act = random.choice(acts)

        # go to next state following random action
        cur = duck.result(cur, chosen_act)
        i += 1
    
    return DuckPuzzle(cur)

def md_heuristic_2(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    cur = node.state
    md_sum = 0

    for (i, j) in zip(cur, goal):
        if i != 0 and i != 0:
            md_sum += duck_orientation[i-1][cur.index(i)]
 
    return md_sum

def max_h_2(node):
    puzzle = DuckPuzzle(node)
    x, y = md_heuristic_2(node), puzzle.h(node)
    return max(md_heuristic_2(node), puzzle.h(node))

def display_DuckPuzzle(state):
    # replace 0 to '*'
    new_state = list(state)
    new_state[state.index(0)] = '*'

    # print puzzle
    i = 0
    while i < 9:
        if i == 6:   print(' ', end = ' ')
        print(str(new_state[i]) + ' ', end = '')
        if i == 1 or i == 5 or i == 8:    print('\n', end = '')
        i += 1

# taken from search.py
def best_first_graph_search_2(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            print("Number of tiles moved for solution: " + str(len(node.solution())))
            print("Number of tiles removed from frontier: " + str(len(explored)))
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    print(len(explored))
    return None

# taken from search.py
def astar_search_2(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_2(problem, lambda n: n.path_cost + h(n), display)

# taken from search.py
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

        if index_blank_square in [0, 2, 6]:
            possible_actions.remove('LEFT')
        if index_blank_square in [0, 1, 4, 5]:
            possible_actions.remove('UP')
        if index_blank_square in [1, 5, 8]:
            possible_actions.remove('RIGHT')
        if index_blank_square in [2, 6, 7, 8]:
            possible_actions.remove("DOWN")

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank < 2:
            delta['DOWN'] = 2
        if blank > 1 and blank < 4:
            delta['UP'] = -2

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum((s != g) and (s != 0) for (s, g) in zip(node.state, self.goal))

def q3_results():
    print("\nUsing Duck Puzzle board:")

    cur_puzzle = make_rand_DuckPuzzle()
    display_DuckPuzzle(cur_puzzle.initial)

    ''' A*-search algorithm w/ misplaced tile heuristic
        --> misplaced tile heuristic: # of tiles not in goal state'''
    print("A*-search using Misplaced Tile Heuristic:")
    mt_start = time.time()
    astar_search_2(cur_puzzle, cur_puzzle.h, False)
    mt_end = (time.time() - mt_start)
    print("Total running time (seconds): " + str(mt_end) + "\n")

    ''' A*-search algorithm w/ Manhattan heuristic
        --> Manhattan heuristic: sum of distances b/w 
            current tile position and goal position'''
    print("A*-search using Manhattan Distance Heuristic:")
    md_start = time.time()
    astar_search_2(cur_puzzle, md_heuristic_2, False)
    md_end = (time.time() - md_start)
    print("Total running time (seconds): " + str(md_end) + "\n")

    ''' A*-search algorithm w/ max of Manhattan heuristic
        and misplaced tile heuristic'''
    print("A*-search using Maximum Heuristic:")
    max_start = time.time()
    astar_search_2(cur_puzzle, max_h_2, False)
    max_end = (time.time() - max_start)
    print("Total running time (seconds): " + str(max_end) + " \n")

q2_results() 
q3_results()
#