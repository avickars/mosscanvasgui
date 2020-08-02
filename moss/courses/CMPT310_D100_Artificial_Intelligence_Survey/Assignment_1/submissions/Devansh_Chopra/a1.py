import random
from search import *
import time

# Name: Devansh Chopra
# Student #: 301-275-491

# ------------------------------ Question 1 Implementation ------------------------------

# Returns a new instance of an EightPuzzle problem with a random initial state that is solvable 
def make_rand_8puzzle():
    test1 = EightPuzzle(Problem)
    k = False
    while(k != True):
        random_tuple = tuple(random.sample(range(9), 9))
        k = test1.check_solvability(random_tuple)
    display(random_tuple)
    return EightPuzzle(random_tuple, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)) 

# Takes an 8-puzzle state as input and prints a neat and readble representation of it
def display(state):
    count = 0
    for i, item in enumerate(state, start = 1):
        if (item == 0):
            item = '*'
        print(item, end=" ")
        if not i % 3:
            print()

# ------------------------------ Question 2 Implementation ------------------------------

# A* search using the Manhattan Distance Heuristic
def Eight_manhattan(node):
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

# A* search calculating the max of the misplaced tile heuristic and the Manhattan distance heuristic
def Eight_max_of_both(node):
    temporary = EightPuzzle(node.state)
    return max(Eight_manhattan(node), newH(node))

# New Default heuristic function for the misplaced tile which doesnt include zero 
def newH(node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g and s!=0 and g!=0 for (s, g) in zip(node.state, (1, 2, 3, 4, 5, 6, 7, 8, 0)))

# 10 random 8-puzzle instances solved using 3 algorithms and returned time, length of the solution and number of nodes removed
def compare_algorithms():
    print('  ')
    print('----------------------------- Eight Puzzle Data -----------------------------')
    for i in range(1,11):
        print('  ')
        print("------------ Trial Number ", i, ' ------------')
        print('  ')
        New_EightPuzzle = make_rand_8puzzle()

        print('  ')
        print('--- Misplaced tile heuristic ---')
        print('  ')
        
        start1 = time.time()
        result_astar_search, pop = astar_search(New_EightPuzzle, newH)
        total_time1 = time.time() - start1
        print(f'Total running time of trial {i} in seconds is: {total_time1}')
        print(f'The length of the solution of trial {i} is: {len(result_astar_search.solution())}')
        print(f'The total number of nodes removed from the frontier in trial {i} is: ', pop)

        print('  ')
        print('--- Manhattan Distance heuristic ---')
        print('  ')

        start2 = time.time()
        result_manhattan, total_pop2 = astar_search(New_EightPuzzle, Eight_manhattan)
        total_time2 = time.time() - start2
        print(f'Total running time of trial {i} in seconds is: {total_time2}')
        print(f'The length of the solution of trial {i} is: {len(result_manhattan.solution())}')
        print(f'The total number of nodes removed from the frontier in trial {i} is: ', total_pop2)

        print('  ')
        print('--- Max of the misplaced tile heuristic and Manhattan Distance heuristic ---')
        print('  ')

        start3 = time.time()
        result_max, total_pop3 = astar_search(New_EightPuzzle, Eight_max_of_both)
        total_time3 = time.time() - start3
        print(f'Total running time of trial {i} in seconds is: {total_time3}')
        print(f'The length of the solution of trial {i} is: {len(result_max.solution())}')
        print(f'The total number of nodes removed from the frontier in trial {i} is: ', total_pop3)

# ------------------------------ Question 3 Implementation ------------------------------

# DuckPuzzle class that is the same as the 8-puzzle, except the board has a duck looking shape
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
            possible_actions.remove('UP')
            possible_actions.remove('LEFT');
        if index_blank_square == 1:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
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

        if blank == 0:
            all_moves = {'RIGHT': 1, 'DOWN': 2}
            neighbor = blank + all_moves[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank] 
        if blank == 1:
            all_moves = {'LEFT': -1, 'DOWN': 2}
            neighbor = blank + all_moves[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank] 
        if blank == 2:
            all_moves = {'UP': -2, 'RIGHT': 1}
            neighbor = blank + all_moves[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank] 
        if blank == 3:
            all_moves = {'UP': -2, 'RIGHT': 1, 'LEFT': -1, 'DOWN': 3}
            neighbor = blank + all_moves[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank] 
        if blank == 4:
            all_moves = {'RIGHT': 1, 'LEFT': -1, 'DOWN': 3}
            neighbor = blank + all_moves[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank] 
        if blank == 5:
            all_moves = {'LEFT': -1, 'DOWN': 3}
            neighbor = blank + all_moves[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank] 
        if blank == 6:
            all_moves = {'UP': -3, 'RIGHT': 1}
            neighbor = blank + all_moves[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank] 
        if blank == 7:
            all_moves = {'UP': -3, 'RIGHT': 1, 'LEFT': -1}
            neighbor = blank + all_moves[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank] 
        if blank == 8:
            all_moves = {'UP': -3, 'LEFT': -1}
            neighbor = blank + all_moves[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank] 

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state, Puzzle):
        """ Checks if the given state is solvable """

        for i in range(0,100):
            all_actions = Puzzle.actions(state)
            length = len(all_actions)
            index = random.randint(1,length)
            result_state = Puzzle.result(state, all_actions[index-1])
            state = result_state

        return state, True


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

# Returns a new instance of the DuckPuzzle problem with a random initial state that is solvable 
def make_rand_DuckPuzzle():
    NewPuzzle = DuckPuzzle(Problem)
    starting_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    new_State, checker = NewPuzzle.check_solvability(starting_state, NewPuzzle)
    display_Duck(new_State)
    print("PUZZLE IS: ", new_State)
    return DuckPuzzle(new_State, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)) 

# Takes a DuckPuzzle state as input and prints a neat and readble representation of it
def display_Duck(state):
    temp = list(state)
    for i in range(9):
        if temp[i] == 0:
            temp[i] = '*'
    state = tuple(temp)        
    print(state[0], end=" ")
    print(state[1])
    print(state[2], end=" ")
    print(state[3], end=" ")
    print(state[4], end=" ")
    print(state[5])
    print(" ", state[6], end=" ")
    print(state[7], end=" ")
    print(state[8])

# A* search using the Manhattan Distance Heuristic for DuckPuzzle
def manhattan_Duck(node):
    state = node.state
    index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
    index_state = {}
    index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]
    for i in range(len(state)):
        index_state[state[i]] = index[i]
    mhd = 0
    for i in range(1,9):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
    return mhd

# A* search calculating the max of the misplaced tile heuristic and the Manhattan distance heuristic for the DuckPuzzle
def max_of_both_Duck(node):
    temporary = DuckPuzzle(node.state)
    return max(manhattan_Duck(node), newH(node))

# 10 random DuckPuzzle instances solved using 3 algorithms and returned time, length of the solution and number of nodes removed
def compare_algorithms_Duck():
    print('  ')
    print('----------------------------- Duck Puzzle Data -----------------------------')
    for i in range(1,11):
        print('  ')
        print("------------ Trial Number for Duck ", i, ' ------------')
        print('  ')
        Duck = make_rand_DuckPuzzle()

        print('  ')
        print('--- Misplaced tile heuristic ---')
        print('  ')

        start1 = time.time()
        result_Duck, pop1 = astar_search(Duck, newH)
        total_time1 = time.time() - start1
        print(f'Total running time of trial {i} in seconds is: {total_time1}')
        print(f'The length of the solution of trial {i} is: {len(result_Duck.solution())}')
        print(f'The total number of nodes removed from the frontier in trial {i} is: ', pop1)

        print('  ')
        print('--- Manhattan Distance heuristic ---')
        print('  ')

        start2 = time.time()
        Duck_result_manhattan, total_pop2 = astar_search(Duck, manhattan_Duck)
        total_time2 = time.time() - start2
        print(f'Total running time of trial {i} in seconds is: {total_time2}')
        print(f'The length of the solution of trial {i} is: {len(Duck_result_manhattan.solution())}')
        print(f'The total number of nodes removed from the frontier in trial {i} is: ', total_pop2)

        print('  ')
        print('--- Max of the misplaced tile heuristic and Manhattan Distance heuristic ---')
        print('  ')

        start3 = time.time()
        Duck_result_max, total_pop3 = astar_search(Duck, max_of_both_Duck)
        total_time3 = time.time() - start3
        print(f'Total running time of trial {i} in seconds is: {total_time3}')
        print(f'The length of the solution of trial {i} is: {len(Duck_result_max.solution())}')
        print(f'The total number of nodes removed from the frontier in trial {i} is: ', total_pop3)

# ------------------------------ Helper Functions ------------------------------

# Copied from search.py and edited as needed
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
    pops = 0
    while frontier:
        node = frontier.pop()
        pops += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, pops
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, pops

# Copied from search.py
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# Function for getting all the data 
if __name__ == "__main__":
    # Getting Data for 8-puzzle
    compare_algorithms()

    # Getting Data for DuckPuzzle
    compare_algorithms_Duck()

