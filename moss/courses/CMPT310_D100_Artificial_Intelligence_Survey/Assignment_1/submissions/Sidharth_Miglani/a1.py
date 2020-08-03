from search import *
import random
import time

#--------------Global variables---------------- 

# goal stste for 8-puzzle
goal_state = (1,2,3,4,5,6,7,8,0)

# total nodes removed from frontier
total_nodes_removed = 0

# list to store time for A* search - misplaced tiles
time_q1 = []
time_q1_hp =[]

# list to store time for A* search - Manhattan
time_q2 = []
time_q2_hp = []

# list to store time for A* search - Max of Manhattan && Misplaced
time_q3 = []
time_q3_hp = []



# Question 1: Helper Functions-----------------------------------------------

# ceates a random solvable puzzle
def make_rand_8puzzle():

    solvability = False
    while solvability == False:
        goal = list(goal_state)

        random.shuffle(goal)

        goal = tuple(goal)

        random_puzzle = EightPuzzle(goal)
        solvability = random_puzzle.check_solvability(goal)
    return random_puzzle

# prints a 3x3 puzzle
def display(state):
    for i in range(len(state)):
        if state[i] == 0:
            print("*", end=" "),
        else:
            print(state[i], end=" ")
        if i % 3 == 2:
            print()

# Question 2: Compare Algorithms----------------------------------------------

# "all_puzzles" contains 10 random puzzles for testing
all_puzzles = []
for i in range (0,10):
    all_puzzles.append(make_rand_8puzzle())

# default misplaced tiles heuristic from search.py
def misplaced_tiles(node):
    return sum(s != g for (s, g) in zip(node.state, goal_state))

# manhattan distance heuristic
# motivation from aima-python/tests/test_search.py 
def manhattan_distance(node):
        state = node.state
        # indeces arrangement on goal sate 
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        # indeces arrangement on the given state
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        mhd = 0
        # iterating 1 to 8, ignoring 0 (since it is a empty space)
        for i in range(1,9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        return mhd

# max of (manhattan_distance , misplaced_tiles)
def max_manhattan_misplaced(node):
    if(manhattan_distance(node) >= misplaced_tiles(node)):
        return manhattan_distance(node)
    else:
        return misplaced_tiles(node)

# slightly modifies A* search from search.py to retrieve total nodes removed from frontier
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# slightly modifies this function from search.py to know total nodes removed from frontier 
def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""

    global total_nodes_removed 
    total_nodes_removed = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        total_nodes_removed+=1
        if problem.goal_test(node.state):
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
    return None


print("\n    A* Search - Misplaced Tile Heuristic    \n")
for i in range (0,10):
    start = time.time()
    solution = astar_search(all_puzzles[i], h = misplaced_tiles).solution()
    end = time.time()
    time_q1.append(end-start)
    print("\nTotal Time           : ", time_q1[i])
    print("Length of solution   : ",len(solution))
    print("Total Nodes Removed  : ", total_nodes_removed)

print("\n    A* Search - Manhattan distance heuristic    \n")
for i in range (0,10):
    start = time.time()
    solution = astar_search(all_puzzles[i], h = manhattan_distance).solution()
    end = time.time()
    time_q2.append(end-start)
    print("\nTotal Time           : ", time_q2[i])
    print("Length of solution   : ",len(solution))
    print("Total Nodes Removed  : ", total_nodes_removed)

print("\n    A* Search - MAX of (Manhattan distance and Misplaced tiles)    \n")
for i in range (0,10):
    start = time.time()
    solution = astar_search(all_puzzles[i], h = max_manhattan_misplaced).solution()
    end = time.time()
    time_q3.append(end-start)
    print("\nTotal Time           : ", time_q3[i])
    print("Length of solution   : ",len(solution))
    print("Total Nodes Removed  : ", total_nodes_removed)



# Question 3: House/ Duck Puzzle--------------------------------------------------------------------

class HousePuzzle(Problem):

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

        if index_blank_square  == 1:
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

        # delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        # modified delta values according to House Puzzle format
        if blank == 0:
            delta = {'DOWN': 2, 'RIGHT': 1}
        if blank == 1:
            delta = {'DOWN': 2, 'LEFT': -1}
        if blank == 2:
            delta = {'UP': -2, 'RIGHT': 1}
        if blank == 3:
            delta = {'UP': -2, 'LEFT': -1, 'RIGHT': 1, 'DOWN': 3}
        if blank == 4:
            delta = {'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank == 5:
            delta = {'DOWN': 3, 'LEFT': -1}
        if blank == 6:
            delta = {'RIGHT': 1, 'UP': -3}
        if blank == 7:
            delta = {'RIGHT': 1, 'UP': -3, 'LEFT': -1}
        if blank == 8:
            delta = {'UP': -3, 'LEFT': -1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

# random.randint(a, b)
# Return a random integer N such that a <= N <= b.

def manhattan_distance(node):
        state = node.state
        # indeces arrangement on goal sate 
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        # indeces arrangement on the given state
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        mhd = 0
        # iterating 1 to 8, ignoring 0 (since it is a empty space)
        for i in range(1,9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        return mhd

def make_rand_housePuzzle():
    # instance of house puzzle in goal state - so we know its solvable
    completed_puzzle = HousePuzzle(goal_state)
    #initial node to perform random actions on the node state
    node = Node(completed_puzzle.initial)
    # loop of 1000 to randomize the actions
    for i in range (100):
        for j in range(10):
            actions = completed_puzzle.actions(node.state)
            # print(actions)
            random_move  = random.randint(0,len(actions)-1)
            # print(node.state,"     ",actions,"     ",random_move)
            node.state = completed_puzzle.result(node.state, actions[random_move])
    return (HousePuzzle(node.state))

# create 10 random house puzzles
all_Housepuzzles = []
for i in range (0,10):
    all_Housepuzzles.append(make_rand_housePuzzle())

print("\n")

#  print house puzzles state
for i in range (0,10):
    print(all_Housepuzzles[i].initial)

# manhattan distance modified for duck puzzle
def manhattan_distance_duck(node):
        state = node.state
        # indeces arrangement on goal sate 
        index_goal = {0: [2, 2], 8: [2, 1], 7: [2, 0], 6: [1, 3], 5: [1, 2], 4: [1, 1], 3: [1, 0], 2: [0, 1], 1: [0, 0]}
        index_state = {}
        index = [[0, 0], [0, 1], [1,0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2]]
        # indeces arrangement on the given state
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        mhd = 0
        # iterating 1 to 8, ignoring 0 (since it is a empty space)
        for i in range(1,9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
        return mhd

def max_manhattan_misplaced_duck(node):
    return max(misplaced_tiles(node), manhattan_distance_duck(node))


print("\n               Duck Puzzle \n")
print("\n   A* Search - Misplaced Tile Heuristic    \n")
for i in range (0,10):
    start = time.time()
    solution = astar_search(all_Housepuzzles[i], h = misplaced_tiles).solution()
    end = time.time()
    time_q1_hp.append(end-start)
    print("\nTotal Time           : ", time_q1_hp[i])
    print("Length of solution   : ",len(solution))
    print("Total Nodes Removed  : ", total_nodes_removed)
    
#     print("time: ",time_q1[i])

    
print("\n   A* Search - Manhattan Distance Heuristic    \n")
for i in range (0,10):
    start = time.time()
    solution = astar_search(all_Housepuzzles[i], h = manhattan_distance_duck).solution()
    end = time.time()
    time_q2_hp.append(end-start)
    print("\nTotal Time           : ", time_q2_hp[i])
    print("Length of solution   : ",len(solution))
    print("Total Nodes Removed  : ", total_nodes_removed)
    # arr_print_nodes_q2.append(total_nodes_removed)
# for i in range (0,10):
#     print("manhattan nodes removed: ",arr_print_nodes_q2[i])
# for i in range (0,10):    
#     print("time: ",time_q2[i])


print("\n    A* Search - MAX of (Manhattan distance and Misplaced tiles)    \n")
for i in range (0,10):
    start = time.time()
    solution = astar_search(all_Housepuzzles[i], h = max_manhattan_misplaced_duck).solution()
    end = time.time()
    time_q3_hp.append(end-start)
    print("\nTotal Time           : ", time_q3_hp[i])
    print("Length of solution   : ",len(solution))
    print("Total Nodes Removed  : ", total_nodes_removed)
    # arr_print_nodes_q3.append(total_nodes_removed)
    
# for i in range (0,10):
#     print("max of manhattan and misplaced tiles nodes removed: ",arr_print_nodes_q3[i])
# for i in range (0,10):
#     print("time: ",time_q3[i])