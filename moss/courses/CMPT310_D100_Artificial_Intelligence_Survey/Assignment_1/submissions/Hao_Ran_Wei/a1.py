import numpy as np
from search import *
import time

class DuckPuzzle (Problem):
    def __init__(self, initial, goal=(1,2,10,10,3,4, 5, 6,10,7, 8, 0)):
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

        if index_blank_square % 4 == 0 or index_blank_square == 9:
            possible_actions.remove('LEFT')
        if index_blank_square < 4 or index_blank_square == 6 or index_blank_square == 7:
            possible_actions.remove('UP')
        if index_blank_square % 4 == 3 or index_blank_square == 1:
            possible_actions.remove('RIGHT')
        if index_blank_square > 7 or index_blank_square == 4:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """
        #default h from eight puzzle.
        return sum(s != g for (s, g) in zip(node.state, self.goal))
    def mh (self,node):
        #edited the function manhattan in tests/test_search.py to work, does not include 0 in it's calculations
        #Manhattan distance heuristic function
        state = node.state

        index_goal = {0: [2,3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [0,3],[1, 0],[1, 1],[1, 2],[1,3],[2, 0], [2, 1], [2, 2], [2,3]]
        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhd = 0
        for i in range(8):
            #loop rolling for optimization
            x = i + 1
            mhd = abs(index_goal[x][0] - index_state[x][0]) + mhd
            mhd = abs(index_goal[x][1] - index_state[x][1]) + mhd
        return mhd

    def Maxh (self,node):
        #returns the max of the two functions
        #Max heuristic function
        return max (self.h(node),self.mh(node))
class Eight(EightPuzzle):

    def mh (self,node):
        #edited the function manhattan in tests/test_search.py to work, does not include 0 in it's calculations
        #Manhattan distance heuristic function
        state = node.state

        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        for i in range(len(state)):
            index_state[state[i]] = index[i]


        mhd = 0
        for i in range(8):
            #loop rolling for optimization
            x = i + 1
            mhd = abs(index_goal[x][0] - index_state[x][0]) + mhd
            mhd = abs(index_goal[x][1] - index_state[x][1]) + mhd
        return mhd

    def Maxh (self,node):
        #returns the max of the two functions
        #Max heuristic function
        return max (self.h(node),self.mh(node))



def best_first_graph_search2(problem, f, display=False):

    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    count = 0
    while frontier:
        node = frontier.pop()
        count = count + 1
        if problem.goal_test(node.state):
            if display:
                #depth is the number of moves made to for the solution
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print("length (i.e. number of tiles moved) of the solution: ", node.depth)
            print("total number of nodes that were removed from frontier: ", count)
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
def astar_search2(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search2(problem, lambda n: n.path_cost + h(n), display)

def make_rand_8puzzle():
    """ generates a random solvable puzzle for EightPuzzle"""
    state = tuple(np.random.permutation(9))
    dummy_puzzle = EightPuzzle (initial=state)
    while dummy_puzzle.check_solvability(state) == False:
        state = tuple(np.random.permutation(9))
        dummy_puzzle = EightPuzzle (initial=state)
    return state
def make_rand_Duck():
    """generates a random solvable puzzle for DuckPuzzle"""
    state = (1,2,10,10,3,4, 5, 6,10,7, 8, 0)
    moves = np.random.randint(low = 10, high = 1000, size = 1)[0]
    puzzle = DuckPuzzle (initial=state)
    for i in range(moves):

        action = np.random.choice(puzzle.actions(state = state))

        state = puzzle.result(state = state, action = action)
    return state

def display(state):
    """ Display the state in the correct format"""
    for x in range(3):
        if state [x] != 0:
            print(state [x], end =" ")
        else:
            print ("*", end =" ")
    print()
    for x in range(3,6):
        if state [x] != 0:
            print(state [x], end =" ")
        else:
            print ("*", end =" ")
    print()
    for x in range(6,9):
        if state [x] != 0:
            print(state [x], end =" ")
        else:
            print ("*", end =" ")
    return

def display_duck(state):
    """ Display the state in the correct format"""
    num = len(state)

    for x in range(num):
        if state [x] == 10 and x % (int (num**(1/3) + 2)) != int(num**(1/3) + 1):
            print(" ", end =" ")
        elif state [x] == 10 and x % (int (num**(1/3) + 2)) == int(num**(1/3) + 1):
            print(" ")
        elif state [x] != 0 and x % (int (num**(1/3) + 2)) != int(num**(1/3) + 1):
            print(state [x], end =" ")
        elif state [x] != 0 and x % (int (num**(1/3) + 2)) == int(num**(1/3) +1):
            print(state [x])
        elif state [x] == 0 and x % (int (num**(1/3) + 2)) == int(num**(1/3) +1):
            print("*")
        else:
            print ("*", end =" ")
    return

def run_puzzle_eight (dummy_puzzle):
    #example of dummy_puzzle = (3, 7, 1, 4, 6, 0, 8, 2, 5)
    display(dummy_puzzle)
    print()
    puzzle = Eight (initial=dummy_puzzle)
    print()
    print()
    print("########   A*-search using the misplaced tile heuristic   ########")
    print()
    start_time = time.time()
    astar_search2(puzzle,puzzle.h,False)
    elapsed_time = time.time() - start_time
    print("elapsed time (in seconds):", end =" ")
    print(elapsed_time)
    print()
    print()
    print("########   A*-search using the Manhattan distance heuristic   ########")
    print()
    start_time = time.time()
    astar_search2(puzzle,puzzle.mh,False)
    elapsed_time = time.time() - start_time
    print("elapsed time (in seconds):", end =" ")
    print(elapsed_time)
    print()
    print()
    print("########   A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic   ########")
    print()
    start_time = time.time()
    astar_search2(puzzle,puzzle.Maxh,False)
    elapsed_time = time.time() - start_time
    print("elapsed time (in seconds):", end =" ")
    print(elapsed_time)
    print()
    print()
    return

def run_puzzle_duck (dummy_puzzle):
    #example of dummy_puzzle = (3, 1, 10, 10, 2, 7, 4, 5, 10, 8, 0, 6)
    display_duck(dummy_puzzle)
    print()
    puzzle = DuckPuzzle (initial=dummy_puzzle)
    print()
    print()
    print("########   A*-search using the misplaced tile heuristic   ########")
    print()
    start_time = time.time()
    astar_search2(puzzle,puzzle.h,False)
    elapsed_time = time.time() - start_time
    print("elapsed time (in seconds):", end =" ")
    print(elapsed_time)
    print()
    print()
    print("########   A*-search using the Manhattan distance heuristic   ########")
    print()
    start_time = time.time()
    astar_search2(puzzle,puzzle.mh,False)
    elapsed_time = time.time() - start_time
    print("elapsed time (in seconds):", end =" ")
    print(elapsed_time)
    print()
    print()
    print("########   A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic   ########")
    print()
    start_time = time.time()
    astar_search2(puzzle,puzzle.Maxh,False)
    elapsed_time = time.time() - start_time
    print("elapsed time (in seconds):", end =" ")
    print(elapsed_time)
    print()
    print()
    return
def test_all():
    #runs all the the random puzzles
    #eightpuzzles
    puzzle = (6,3,7,8,2,1,4,0,5)
    run_puzzle_eight (puzzle)
    puzzle = (4,7,0,5,8,3,1,6,2)
    run_puzzle_eight (puzzle)
    puzzle = (3,7,1,4,6,0,8,2,5)
    run_puzzle_eight (puzzle)
    puzzle = (6,3,1,0,7,5,2,4,8)
    run_puzzle_eight (puzzle)
    puzzle = (5,3,2,1,8,0,7,4,6)
    run_puzzle_eight (puzzle)
    puzzle = (5,1,2,0,8,7,4,3,6)
    run_puzzle_eight (puzzle)
    puzzle = (5,0,1,4,2,6,7,3,8)
    run_puzzle_eight (puzzle)
    puzzle = (1,4,6,2,3,5,0,8,7)
    run_puzzle_eight (puzzle)
    puzzle = (2,1,8,5,7,0,6,4,3)
    run_puzzle_eight (puzzle)
    puzzle = (3,6,0,7,1,8,5,4,2)
    run_puzzle_eight (puzzle)

    #duckpuzzles
    puzzle = (3, 1, 10, 10, 2, 7, 0, 4, 10, 6, 5, 8)
    run_puzzle_duck (puzzle)
    puzzle = (2, 3, 10, 10, 1, 7, 0, 6, 10, 8, 5, 4)
    run_puzzle_duck (puzzle)
    puzzle = (1, 2, 10, 10, 3, 0, 8, 4, 10, 5, 6, 7)
    run_puzzle_duck (puzzle)
    puzzle = (0, 1, 10, 10, 3, 2, 6, 7, 10, 4, 5, 8)
    run_puzzle_duck (puzzle)
    puzzle = (2, 3, 10, 10, 0, 1, 4, 6, 10, 8, 7, 5)
    run_puzzle_duck (puzzle)
    puzzle = (1, 2, 10, 10, 3, 4, 0, 7, 10, 8, 5, 6)
    run_puzzle_duck (puzzle)
    puzzle = (3, 1, 10, 10, 0, 2, 8, 6, 10, 5, 7, 4)
    run_puzzle_duck (puzzle)
    puzzle = (3, 1, 10, 10, 2, 0, 8, 7, 10, 6, 5, 4)
    run_puzzle_duck (puzzle)
    puzzle = (2, 3, 10, 10, 0, 1, 8, 5, 10, 7, 6, 4)
    run_puzzle_duck (puzzle)
    puzzle = (0, 1, 10, 10, 3, 2, 6, 4, 10, 7, 8, 5)
    run_puzzle_duck (puzzle)
    return

#to run all puzzles in the tables
#test_all()