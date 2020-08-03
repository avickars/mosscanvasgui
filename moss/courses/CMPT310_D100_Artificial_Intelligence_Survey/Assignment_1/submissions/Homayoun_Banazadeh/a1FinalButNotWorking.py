from search import *
import time
import numpy as np

#Note:this was my final code but it was not working. So I have submited this and the other one that is working 
#which was not my final code. I tried implementing a counter in best_first_graph_search after every pop to count 
#for each time we pop the frontier. To do that, I had to change the astar_search function to return that sum everytime.
#However, it was not working for some reason. 
#Also, I tried counting how many moves there are to complete a puzzle by using 
#something like this: LengthForMisplayed[i] = len(astar_search(instance, h=linear_distance).solution()) but I doubt
#it was working correctly because it always gave the same number for default heuristic and manhattan. Other than that 
#everything should work about fine. Pkease take a time to go over my final code because I spend a lot of
#time on it and it is important for me to understand what I did wrong. Most importantly, I could not 
#understand the relationship between the class Node and best_first_graph_search and aster_search. Therefore,
#it was really hard to understand the big picture of how everything is working. Please help me understand this. Thanks.

 
def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    sum = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        sum = sum + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return (node,sum)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None



def CHANGED_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)



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
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

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



def make_rand_8puzzle():
    my_check_state = False
    while my_check_state == False:
        state = tuple(np.random.permutation(9))
        my_initial_puzzle = EightPuzzle(initial=state)
        my_check_state = my_initial_puzzle.check_solvability(state)
    return my_initial_puzzle


def display(state):
    state2 = list(state)
    for i, item in enumerate(state2):
        if item == 0:
            state2[i] = '*'
    print(state2[0],state2[1],state2[2],'\n')
    print(state2[3],state2[4],state2[5],'\n')
    print(state2[6],state2[7],state2[8],'\n')
    
    
    
def linear_distance(node):
    state=node.state
    sum=0
    for i in range(9):
        if state[i] != 0:
            if state[i] != i+1:
                sum+=1
    return sum

def aStar_misplayed_tile(instance):
    start_time = time.time()
    node, sum = CHANGED_astar_search(instance)
    elapsed_time = time.time() - start_time
    return elapsed_time,sum


def manhattan_distance(node):
    state=node.state
    arr = [[state[0],state[1],state[2]],
           [state[3],state[4],state[5]],
           [state[6],state[7],state[8]]]
    sum = 0
    for i in range(3):
        for j in range(3):
            if arr[i][j] != 0:
                if arr[i][j] == 1:
                    sum += abs(i-0) + abs(j-0)
                if arr[i][j] == 2:
                    sum += abs(i-0) + abs(j-1)
                if arr[i][j] == 3:
                    sum += abs(i-0) + abs(j-2)
                if arr[i][j] == 4:
                    sum += abs(i-1) + abs(j-0)
                if arr[i][j] == 5:
                    sum += abs(i-1) + abs(j-1)
                if arr[i][j] == 6:
                    sum += abs(i-1) + abs(j-2)
                if arr[i][j] == 7:
                    sum += abs(i-2) + abs(j-0)
                if arr[i][j] == 8:
                    sum += abs(i-2) + abs(j-1)
    return sum
def aStar_manhattan_tile(instance):
    start_time = time.time()
    node , sum = CHANGED_astar_search(instance,h=manhattan_distance)
    elapsed_time = time.time() - start_time
    return elapsed_time,sum



def max_manhattan_versus_misplayed_distance(node):
    score1 = manhattan_distance(node)
    score2 = linear_distance(node)
    return max(score1, score2)
def aStar_manhattan_versus_misplayed_tile(instance):
    start_time = time.time()
    node , sum = CHANGED_astar_search(instance,h=max_manhattan_versus_misplayed_distance)
    elapsed_time = time.time() - start_time
    return elapsed_time,sum


def make_rand_DuckPuzzle():
    state = tuple(np.random.permutation(9))
    my_initial_puzzle = DuckPuzzle(initial=state)
    return my_initial_puzzle


timeForMisplayed = [0,0,0,0,0,0,0,0,0,0]
timeForManhattan = [0,0,0,0,0,0,0,0,0,0]
timeForMaxBoth = [0,0,0,0,0,0,0,0,0,0]
LengthForMisplayed = [0,0,0,0,0,0,0,0,0,0]
LengthForManhattan = [0,0,0,0,0,0,0,0,0,0]
LengthForMaxBoth = [0,0,0,0,0,0,0,0,0,0]
frontierForMisplayed = [0,0,0,0,0,0,0,0,0,0]
frontierForManhattan = [0,0,0,0,0,0,0,0,0,0]
frontierForMaxBoth = [0,0,0,0,0,0,0,0,0,0]

Duck_timeForMisplayed = [0,0,0,0,0,0,0,0,0,0]
Duck_timeForManhattan = [0,0,0,0,0,0,0,0,0,0]
Duck_timeForMaxBoth = [0,0,0,0,0,0,0,0,0,0]
Duck_LengthForMisplayed = [0,0,0,0,0,0,0,0,0,0]
Duck_LengthForManhattan = [0,0,0,0,0,0,0,0,0,0]
Duck_LengthForMaxBoth = [0,0,0,0,0,0,0,0,0,0]
Duck_frontierForMisplayed = [0,0,0,0,0,0,0,0,0,0]
Duck_frontierForManhattan = [0,0,0,0,0,0,0,0,0,0]
Duck_frontierForMaxBoth = [0,0,0,0,0,0,0,0,0,0]

for i in range(3):
    instance = make_rand_8puzzle()
    timeForMisplayed[i],frontierForMisplayed[i] = aStar_misplayed_tile(instance)
    timeForManhattan[i],frontierForManhattan[i] = aStar_manhattan_tile(instance)
    timeForMaxBoth[i],frontierForMaxBoth[i] = aStar_manhattan_versus_misplayed_tile(instance)
    LengthForMisplayed[i] = len(astar_search(instance, h=linear_distance).solution())
    LengthForManhattan[i] = len(astar_search(instance, h=manhattan_distance).solution())
    LengthForMaxBoth[i] = len(astar_search(instance, h=max_manhattan_versus_misplayed_distance).solution())
    instance2 = make_rand_DuckPuzzle()
    Duck_timeForMisplayed[i],Duck_frontierForMisplayed[i] = aStar_misplayed_tile(instance2)
    Duck_timeForManhattan[i],Duck_frontierForManhattan[i] = aStar_manhattan_tile(instance2)
    Duck_timeForMaxBoth[i],Duck_frontierForMaxBoth[i] = aStar_manhattan_versus_misplayed_tile(instance2)
    Duck_LengthForMisplayed[i] = len(astar_search(instance2, h=linear_distance).solution())
    Duck_LengthForManhattan[i] = len(astar_search(instance2, h=manhattan_distance).solution())
    Duck_LengthForMaxBoth[i] = len(astar_search(instance2, h=max_manhattan_versus_misplayed_distance).solution())
    

print(timeForMisplayed)
print(frontierForMisplayed)
print(timeForManhattan)
print(frontierForManhattan)
print(timeForMaxBoth)
print(frontierForMaxBoth)
print(LengthForMisplayed)
print(LengthForManhattan)
print(LengthForMaxBoth)
print(Duck_timeForMisplayed)
print(Duck_frontierForMisplayed)
print(Duck_timeForManhattan)
print(Duck_frontierForManhattan)
print(Duck_timeForMaxBoth)
print(Duck_frontierForMaxBoth)
print(Duck_LengthForMisplayed)
print(Duck_LengthForManhattan)
print(Duck_LengthForMaxBoth)
