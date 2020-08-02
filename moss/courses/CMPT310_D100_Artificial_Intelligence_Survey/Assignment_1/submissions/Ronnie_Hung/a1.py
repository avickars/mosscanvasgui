from search import *
import random
import time
import numpy as np
import pandas as pd

tests = []

#----------- Question 1: Helper Functions ----------- 
def make_rand_8puzzle():
    #https://note.nkmk.me/en/python-random-shuffle/
    init_num = [i for i in range(9)]
    rand_init = tuple(random.sample(init_num, len(init_num)))
    # print(rand_init)

    eightpuzzle_obj = EightPuzzle(rand_init)
    
    while eightpuzzle_obj.check_solvability(rand_init) == False:
        # print('The given state is not solvable!')
        init_num = [i for i in range(9)]
        rand_init = tuple(random.sample(init_num, len(init_num)))
        # print(rand_init)

    return EightPuzzle(rand_init)

def display(state):
    for i in range(9):
        elem = state[i]
        if elem == 0:
            elem = '*'
        if (i+1) % 3 != 0:
            print(elem, end=' ')
        else:
            print(elem)

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
        #not including 0
        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

#----------- Question 2: Comparing Algorithms ----------- 
    def manhattan_h(self, node):
        """ Return the heuristic value for a given state. 
        h(n) = sum of the distances of the tiles from their goal positions """
        # https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game
        sum = 0
        for i in range(9):
            n = node.state[i]
            # print('\nstate: ', n)
            # print('goal: ', self.goal.index(n))
            # print('goal: ', g)
            dist = (abs(int(i/3) - int(self.goal.index(n)/3)) + abs((i%3) - self.goal.index(n)%3))
            # print('distance: ', dist)

            sum += dist
        return sum

    def max_h(self, node):
        return max(self.h(node), self.manhattan_h(node))

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
    nodesRemoved = 0
    while frontier:
        node = frontier.pop()
        nodesRemoved += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, nodesRemoved
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, nodesRemoved

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

#----------- Question 3 -----------
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

        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank == 0 or blank == 1:
            delta = {'UP':-2, 'DOWN':2, 'LEFT':-1, 'RIGHT':1}
           
        elif blank == 2 or blank == 3 or blank == 4 or blank == 5:
            delta = {'UP':-2, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
            
        elif blank == 6 or blank == 7 or blank == 8:
            delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    #Since the given duck puzzle in make_rand_duckpuzzle will always be solvable (because it's made by doing only valid moves), this function will always return True
    def check_solvability(self, state):
        return True

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        #not including 0
        return sum(s != g  and s != 0 for (s, g) in zip(node.state, self.goal))

    def manhattan_h(self, node):
        """ Return the heuristic value for a given state. 
        h(n) = sum of the distances of the tiles from their goal positions """
        # got some help from other students to get the distance in the duck puzzle
        state = node.state
        goal_index = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]} 
        current_index = {}
        index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
 
        sum = 0

        for i in range(len(state)):
            current_index[state[i]] = index[i]

        for i in range(9):
            n = node.state[i]
            # print('\nstate: ', n)
            # print('current index: ', current_index[n])
            # print('goal index: ', goal_index[n])
            dist = abs(current_index[n][0] - goal_index[n][0]) + abs(current_index[n][1] - goal_index[n][1]
            )
            # print('distance: ', dist)
            sum += dist

        return sum

    def max_h(self, node):
        return max(self.h(node), self.manhattan_h(node))

def make_rand_duckpuzzle():
    p = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))
    state = p.initial
    # display_duck(state)
    rand_num_action = random.randint(1, 100)
    # print('\n# of random actions: ', rand_num_action)

    for i in range(rand_num_action):
        # print('\nstep ', i+1)
        actions = p.actions(state)
        # print(actions)
        rand_action = random.randint(0, len(actions)-1)
        # print('Random action (index): ', rand_action)
        state = p.result(state, actions[rand_action])
        # display_duck(state)
    return DuckPuzzle(state)

def display_duck(state):
    for i in range(9):
        elem = state[i]
        if elem == 0:
            elem = '*'
        if i == 1:
            print(elem, '\n', end='' )
        elif i == 5:
            print(elem, '\n ', end=' ')
        else:
            print(elem, end=' ')
    print('\n')


def main():
 #----------- Question 2: Comparing Algorithms ----------- 
    #--------- 8PUZZLE --------------
    print('------ 8-PUZZLE -----')
    puzzles = []
    for i in range(10):
        puzzles.append(make_rand_8puzzle())

    i = 1
    for p in puzzles:
        print('\npuzzle ', i)
        display(p.initial)

        print('\n---h(n) = number of misplaced tiles---')
        st = time.time()
        result, nodesRemoved = astar_search(p, h=p.h)
        et = time.time() - st
        sol = result.solution()
        print('Elapased time in seconds: ', et)
        print('Length of solution: ', len(sol))
        print('Number of nodes removed: ', nodesRemoved)

        print('\n---h(n) = Manhattan distance ---')
        st = time.time()
        result, man_nodesRemoved = astar_search(p, h=p.manhattan_h)
        man_et = time.time() - st
        man_sol = result.solution()
        print('Elapased time in seconds: ', man_et)
        print('Length of solution: ', len(man_sol))
        print('Number of nodes removed: ', man_nodesRemoved)

        print('\n---h(n) = max of of the misplaced tile heuristic and the Manhattan distance heuristic---')
        st = time.time()
        result, max_nodesRemoved = astar_search(p, h=p.max_h)
        max_et = time.time() - st
        max_sol = result.solution()
        print('Elapased time in seconds: ', max_et)
        print('Length of solution: ', len(max_sol))
        print('Number of nodes removed: ', max_nodesRemoved)

        tests.append([et, len(sol), nodesRemoved, man_et, len(man_sol), man_nodesRemoved, max_et, len(max_sol), max_nodesRemoved])

        i += 1
    
    df = pd.DataFrame(tests, columns=['orig h - time', 'orig h - length', 'orig h - # nodes removed', 'manhattan dist h - time', 'manhattan dist h - length', 'manhattan dist h - # nodes removed', 'max h - time', 'max h - length', 'max h - # nodes removed'])

    #uncomment below to get exported csv file
    df.to_csv('a1_q2.csv', index=False)
    # """

#--------- Question 3: DUCK PUZZLE --------------
    print('------ DUCK PUZZLE -----')
    puzzles = []
    for i in range(10):
        puzzles.append(make_rand_duckpuzzle())

    i = 1
    for p in puzzles:
        print('\npuzzle ', i)
        display_duck(p.initial)

        print('---h(n) = number of misplaced tiles---')
        st = time.time()
        result, nodesRemoved = astar_search(p, h=p.h)
        # print(result.nodesRemoved)
        et = time.time() - st
        sol = result.solution()
        print('Elapased time in seconds: ', et)
        print('Length of solution: ', len(sol))
        print('Number of nodes removed: ', nodesRemoved)

        print('\n---h(n) = Manhattan distance ---')
        st = time.time()
        result, man_nodesRemoved = astar_search(p, h=p.manhattan_h)
        man_et = time.time() - st
        man_sol = result.solution()
        print('Elapased time in seconds: ', man_et)
        print('Length of solution: ', len(man_sol))
        print('Number of nodes removed: ', man_nodesRemoved)

        print('\n---h(n) = max of of the misplaced tile heuristic and the Manhattan distance heuristic---')
        st = time.time()
        result, max_nodesRemoved = astar_search(p, h=p.max_h)
        max_et = time.time() - st
        max_sol = result.solution()
        print('Elapased time in seconds: ', max_et)
        print('Length of solution: ', len(max_sol))
        print('Number of nodes removed: ', max_nodesRemoved)
        # print(man_sol)

        tests.append([et, len(sol), nodesRemoved, man_et, len(man_sol), man_nodesRemoved, max_et, len(max_sol), max_nodesRemoved])

        i += 1
    
    df = pd.DataFrame(tests, columns=['orig h - time', 'orig h - length', 'orig h - # nodes removed', 'manhattan dist h - time', 'manhattan dist h - length', 'manhattan dist h - # nodes removed', 'max h - time', 'max h - length', 'max h - # nodes removed'])
    # """

    #uncomment below to get exported csv file
    df.to_csv('a1_q3.csv', index=False)

if __name__ == '__main__':
    main()
    