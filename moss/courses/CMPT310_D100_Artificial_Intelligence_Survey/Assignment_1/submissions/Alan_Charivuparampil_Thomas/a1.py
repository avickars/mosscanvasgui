# a1.py
# Alan Thomas
# 301363048

# Got support from peer conversations on Discord group CMPT 310 chats
# Took idea for Manhattan Distance Heuristic from tests/test_search.py

from search import *
import time

# ...
goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)



# ______________________________________________________________________________
# Duck Class

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

    def actions(self, state):   # actions() changed to suit DuckPuzzle
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 and index_blank_square > 3 and index_blank_square < 6:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):     # result() changed to suit DuckPuzzle
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if(blank >= 0 and blank <= 2):
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif(blank >= 4 and blank <= 8):
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif(blank == 3):
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


# ______________________________________________________________________________



#---HELPER FUNCTION for EightPuzzle---
def make_rand_8puzzle():    # Creates a random Eight Puzzle that is solvable
    puzzle = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    solvable = False
    while(solvable == False):
        random.shuffle(puzzle)
        puzzleGen = EightPuzzle(puzzle)
        solvable = puzzleGen.check_solvability(puzzle)
    solvable_puzzle = tuple(puzzle)
    return solvable_puzzle

def display_EightPuzzle(state):     # Displays the Eight Puzzle
    for i in range(9):
        if state[i]==0:
            print('*', end=' ')
        else:
            print(state[i], end=' ')
        if (i+1)%3==0:
            print('')


#---HELPER FUNCTION for DuckPuzzle---
def display_DuckPuzzle(state):      # Displays the Duck Puzzle
    for i in range(9):
        if state[i]==0:
            print('*', end=' ')
        else:
            print(state[i], end=' ')
        if (i+1)==2 or (i+1)==9:
            print('')
        if (i+1)==6:
            print('')
            print('  ', end='')



def best_first_graph_search_mod(problem, f, display=False):     # bfs function that returns node and frontiers removed
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
    total_nodes_removed = 0
    while frontier:
        node = frontier.pop()
        total_nodes_removed = total_nodes_removed + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, total_nodes_removed]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None



def astar_search_function(problem, h=None, display=False):      # A* Search function
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_mod(problem, lambda n: n.path_cost + h(n), display)



def misplaced_tile(node):   # Misplaced Tile Heuristics for both 8Puzzle and DuckPuzzle
    """ Return the heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles """

    return sum(s != 0 and s != g for (s, g) in zip(node.state, goal))


def manhattan_EightPuzzle(node):       # Manhattan Distance Heuristics for 8Puzzle
    state = node.state
    index_goal = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1], 0: [2, 2]}
    test = [[state[0], state[1], state[2]], [state[3], state[4], state[5]], [state[6], state[7], state[8]]]
    
    xposition = 0
    yposition = 0

    for i in range(3):
        for j in range(3):
            position = index_goal[test[i][j]]
            xposition = xposition + abs(position[0]-i)
            yposition = yposition + abs(position[1]-j)
    return xposition + yposition


def manhattan_DuckPuzzle(node):     # Manhattan Distance Heuristics for DuckPuzzle
    state = node.state
    index_goal = {1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2], 0: [2, 3]}
    test = [[state[0], state[1], 9, 9], [state[2], state[3], state[4], state[5]], [9, state[6], state[7], state[8]]]
    
    xposition = 0
    yposition = 0

    for i in range(3):
        for j in range(4):
            if test[i][j] != 9:
                position = index_goal[test[i][j]]
                xposition = xposition + abs(position[0]-i)
                yposition = yposition + abs(position[1]-j)
    return xposition + yposition


def maxOfMisplaced_and_Manhattan_Eight(node):       # Max of Misplaced Tile and Manhattan Distance Heuristics for 8Puzzle
    value_of_misplaced = misplaced_tile(node)
    # print(value_of_misplaced)
    value_of_manhattan = manhattan_EightPuzzle(node)
    # print(value_of_manhattan)
    return max(value_of_misplaced, value_of_manhattan)


def maxOfMisplaced_and_Manhattan_Duck(node):        # Max of Misplaced Tile and Manhattan Distance Heuristics for DuckPuzzle
    value_of_misplaced = misplaced_tile(node)
    # print(value_of_misplaced)
    value_of_manhattan = manhattan_DuckPuzzle(node)
    # print(value_of_manhattan)
    return max(value_of_misplaced, value_of_manhattan)


# For loop to create statistics for 13 8Puzzles
for x in range(13):
    randomPuzzle = make_rand_8puzzle()
    ObjectPuzzle = EightPuzzle(randomPuzzle)

    display_EightPuzzle(randomPuzzle)
    print('')

    # Misplaced Tile Heuristics
    print("Misplaced Tile Heuristics")
    start_time = time.time()
    node1 = astar_search_function(ObjectPuzzle, h=misplaced_tile)
    elapsed_time = time.time() - start_time
    print('elapsed time (in seconds): ' + str(elapsed_time) + 's')
    print('Length of solution: ' + str(node1[0].path_cost))
    print('Total nodes removed: ' + str(node1[1]))
    print('')

    # Manhattan Distance Heuristics
    print("Manhattan Distance Heuristics")
    start_time = time.time()
    node2 = astar_search_function(ObjectPuzzle, h=manhattan_EightPuzzle)
    elapsed_time = time.time() - start_time
    print('elapsed time (in seconds): ' + str(elapsed_time) + 's')
    print('Length of solution: ' + str(node2[0].path_cost))
    print('Total nodes removed: ' + str(node2[1]))
    print('')

    # Max of Misplaced Tile and Manhattan Distance Heuristics
    print("Max of Misplaced Tile and Manhattan Distance Heuristics")
    start_time = time.time()
    node3 = astar_search_function(ObjectPuzzle, h=maxOfMisplaced_and_Manhattan_Eight)
    elapsed_time = time.time() - start_time
    print('elapsed time (in seconds): ' + str(elapsed_time) + 's')
    print('Length of solution: ' + str(node3[0].path_cost))
    print('Total nodes removed: ' + str(node3[1]))
    print('')
    print('')
    print('')


# For loop to create statistics for 13 DuckPuzzles
for y in range(10):
    randomPuzzle = make_rand_8puzzle()
    ObjectPuzzle = DuckPuzzle(randomPuzzle)

    display_DuckPuzzle(randomPuzzle)
    print('')

    # Misplaced Tile Heuristics
    print("Misplaced Tile Heuristics")
    start_time = time.time()
    node1 = astar_search_function(ObjectPuzzle, h=misplaced_tile)
    elapsed_time = time.time() - start_time
    print('elapsed time (in seconds): ' + str(elapsed_time) + 's')
    print('Length of solution: ' + str(node1[0].path_cost))
    print('Total nodes removed: ' + str(node1[1]))
    print('')

    # Manhattan Distance Heuristics
    print("Manhattan Distance Heuristics")
    start_time = time.time()
    node2 = astar_search_function(ObjectPuzzle, h=manhattan_DuckPuzzle)
    elapsed_time = time.time() - start_time
    print('elapsed time (in seconds): ' + str(elapsed_time) + 's')
    print('Length of solution: ' + str(node2[0].path_cost))
    print('Total nodes removed: ' + str(node2[1]))
    print('')

    # Max of Misplaced Tile and Manhattan Distance Heuristics
    print("Max of Misplaced Tile and Manhattan Distance Heuristics")
    start_time = time.time()
    node3 = astar_search_function(ObjectPuzzle, h=maxOfMisplaced_and_Manhattan_Duck)
    elapsed_time = time.time() - start_time
    print('elapsed time (in seconds): ' + str(elapsed_time) + 's')
    print('Length of solution: ' + str(node3[0].path_cost))
    print('Total nodes removed: ' + str(node3[1]))
    print('')
    print('')
    print('')
