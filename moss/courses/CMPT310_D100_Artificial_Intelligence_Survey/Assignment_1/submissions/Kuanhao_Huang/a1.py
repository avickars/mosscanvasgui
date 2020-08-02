import sys
from search import*
import random
import time


def best_first_graph_search(problem, f, display=False):
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
    remove = 0
    while frontier:
        node = frontier.pop()
        remove +=1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print("total number of nodes that were removed from frontier", remove)
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


class EightPuzzle(Problem):
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

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
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

    def manhattan(self, node):
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
    def max_h(self,state):
        return max(self.h(state), self.manhattan(state))

#Q1
def display(state):
    new_state=""
    for i in state:
        if i == 0:
            new_state+='*'
        else:
            new_state+=str(i)
    print(new_state[0:3])
    print(new_state[3:6])
    print(new_state[6:9])
    return
#The puzzle is genertated by initial with valid random moves, so it must be solvable
def make_rand_8puzzle():
    initial =(1,2,3,4,5,6,7,8,0)
    state = tuple(initial)
    rand_val = random.randint(10,1000)
    puzzle = EightPuzzle(state)
    for i in range(rand_val):
        possible_actions = puzzle.actions(state)
        state = puzzle.result(state,random.choice(possible_actions))
    print('initial state')
    display(state)
    return EightPuzzle(state)


#Q3
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
        if index_blank_square ==  1 or index_blank_square == 5 or index_blank_square == 8:
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

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        delta2 = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        delta3 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank < 3:
           neighbor = blank + delta2[action] 
        elif blank > 4:
            neighbor = blank + delta[action]
        else:
            neighbor = blank + delta3[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
    
        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        state_1 =(0,1,1,2,3,4,3,4,5)
        state_2 =(1,0,1,1,2,3,2,3,4)
        state_3 =(1,2,0,1,2,3,2,3,4)
        state_4 =(2,1,1,0,1,2,1,2,3)
        state_5 =(3,2,2,1,0,1,2,1,2)
        state_6 =(4,3,3,2,1,0,3,2,1)
        state_7 =(3,2,2,1,2,3,0,1,2)
        state_8 =(4,3,3,2,1,2,1,0,1)
        state = node.state
        mhd = 0

        n = state.index(1)
        mhd += state_1[n]
        n = state.index(2)
        mhd += state_2[n]
        n = state.index(3)
        mhd += state_3[n]
        n = state.index(4)
        mhd += state_4[n]
        n = state.index(5)
        mhd += state_5[n]
        n = state.index(6)
        mhd += state_6[n]
        n = state.index(7)
        mhd += state_7[n]
        n = state.index(8)
        mhd += state_8[n]

        return mhd
    def max_h(self,state):
        return max(self.h(state), self.manhattan(state))



#Q1
puzzle = make_rand_8puzzle()
print("________________\n")

print("Using misplaced heuristic")

start_time = time.time()
node = astar_search(puzzle,h=puzzle.h)
elapsed_time = time.time() - start_time
elapsed_time ="{:.10f}".format(elapsed_time)
print(f'elapsed_time (in seconds): {elapsed_time}s')
print("solution length:", node.path_cost)

print("____________________________________________________________________\n")

print("Using Manhattan heuristic")

start_time = time.time()
node1 = astar_search(puzzle,h=puzzle.manhattan)
elapsed_time = time.time() - start_time
elapsed_time ="{:.10f}".format(elapsed_time)
print(f'elapsed_time (in seconds): {elapsed_time}s')
print("solution length:", node1.path_cost)

print("____________________________________________________________________\n")

print("Using max of misplaced heuristic and Manhattan heuristic")

start_time = time.time()
node2 = astar_search(puzzle,h=puzzle.max_h)
elapsed_time = time.time() - start_time
elapsed_time ="{:.10f}".format(elapsed_time)
print(f'elapsed_time (in seconds): {elapsed_time}s')
print("solution length:", node2.path_cost) 


#Q3   
def display_duckpuzzle(state):
    count = 0
    new_state=""
    for i in state:
        if count ==6:
            new_state+=' '
        if i == 0:
            new_state+='*'
        else:
            new_state+=str(i)
        count+=1
    print(new_state[0:2])
    print(new_state[2:6])
    print(new_state[6:10])
    return

#The puzzle is genertated by initial with valid random moves, so it must be solvable
def make_rand_duckpuzzle():
    initial =(1,2,3,4,5,6,7,8,0)
    state = tuple(initial)
    rand_val = random.randint(10,1000)
    puzzle = DuckPuzzle(state)
    for i in range(rand_val):
        possible_actions = puzzle.actions(state)
        state = puzzle.result(state,random.choice(possible_actions))
    print('initial state')
    display_duckpuzzle(state)
    return DuckPuzzle(state)
#Q3
puzzle_duck = make_rand_duckpuzzle()
print("________________\n")

print("Using misplaced heuristic")

start_time = time.time()
node = astar_search(puzzle_duck,h=puzzle_duck.h)
elapsed_time = time.time() - start_time
elapsed_time ="{:.10f}".format(elapsed_time)
print(f'elapsed_time (in seconds): {elapsed_time}s')
print("solution length:", node.path_cost)

print("____________________________________________________________________\n")

print("Using Manhattan heuristic")

start_time = time.time()
node1 = astar_search(puzzle_duck,h=puzzle_duck.manhattan)
elapsed_time = time.time() - start_time
elapsed_time ="{:.10f}".format(elapsed_time)
print(f'elapsed_time (in seconds): {elapsed_time}s')
print("solution length:", node1.path_cost)

print("____________________________________________________________________\n")

print("Using max of misplaced heuristic and Manhattan heuristic")

start_time = time.time()
node2 = astar_search(puzzle_duck,h=puzzle_duck.max_h)
elapsed_time = time.time() - start_time
elapsed_time ="{:.10f}".format(elapsed_time)
print(f'elapsed_time (in seconds): {elapsed_time}s')
print("solution length:", node2.path_cost)

