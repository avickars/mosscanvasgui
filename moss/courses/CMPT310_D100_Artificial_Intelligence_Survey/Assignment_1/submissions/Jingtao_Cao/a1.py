# a1.py
import time
from search import *
#q1
def newastar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return newbest_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
def newbest_first_graph_search(problem, f, display=False):
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
    removed_nodes = 0
    while frontier:
        node = frontier.pop()
        removed_nodes += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node,removed_nodes
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)

    return None
class newEightPuzzle(Problem):
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

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

    def man(self,node):
        state = node.state
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        state_index = {} 
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
 
        for i in range(len(state)):
            state_index[state[i]] = index[i]
        mhd = 0

        for i in range(1,9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - state_index[i][j]) + mhd

        return mhd

    def max_of_two(self,node):
        mis = sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))
        state = node.state
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        state_index = {} 
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
 
        for i in range(len(state)):
            state_index[state[i]] = index[i]
        man = 0
        for i in range(1,9):
            for j in range(2):
                man = abs(index_goal[i][j] - state_index[i][j]) + man

        return max(man,mis)
def make_rand_8puzzle():
    random_list = [1,2,3,4,5,6,7,8,0]
    while True:
        random.shuffle(random_list)
        random_list = tuple(random_list)
        neweightPuzzle = newEightPuzzle(random_list)
        if(neweightPuzzle.check_solvability(random_list)):
            break
        random_list = list(random_list)
    return neweightPuzzle
def display(state):
    j = 1
    for i in state:
        if(j%3 == 0):
            print(str(i) if i != 0 else '*')
        else:
             print(str(i)+' ' if i != 0 else '* ',end="")
        j+=1
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
            possible_actions = ['RIGHT','DOWN2']
        if index_blank_square == 1:
            possible_actions = ['LEFT','DOWN2']
        if index_blank_square == 2:
            possible_actions = ['UP2','RIGHT']
        if index_blank_square == 3:
            possible_actions = ['UP2','RIGHT','LEFT','DOWN']
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions = ['LEFT','DOWN']
        if index_blank_square == 6:
            possible_actions = ['UP','RIGHT']
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_actions = ['LEFT','UP']

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1, "UP2": -2, "DOWN2":2}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

    def man(self,node):
        state = node.state
        index_goal = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
        state_index = {} 
        index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
        
        for i in range(len(state)):
            state_index[state[i]] = index[i]
        mhd = 0
        for i in range(1,9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - state_index[i][j]) + mhd

        return mhd
    def max_of_two(self,node):
        mis = sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))
        state = node.state
        index_goal = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
        state_index = {} 
        index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
        
        for i in range(len(state)):
            state_index[state[i]] = index[i]
        man = 0
        for i in range(1,9):
            for j in range(2):
                man = abs(index_goal[i][j] - state_index[i][j]) + man
                
        return max(man,mis)
        
def make_rand_duckpuzzle():
    random_list = [2,3,1,4,5,6,7,8,0]
    duckPuzzle = DuckPuzzle(random_list)
    for i in range(1000):
        action = random.choice(duckPuzzle.actions(duckPuzzle.initial))
        duckPuzzle.initial = duckPuzzle.result(duckPuzzle.initial, action)
    return duckPuzzle

for i in range(10):
    instance = make_rand_8puzzle()
    start_time = time.time()
    finish=newastar_search(instance,instance.h)
    print("MIS trial {i}\n time: {time} nodes removed: {removed_nodes}  length: {length}".format(i=i+1,time=(time.time() - start_time),
    removed_nodes=finish[1],length=finish[0].path_cost))
    start_time = time.time()
    finish=newastar_search(instance,instance.man)
    print("MAN trial {i}\n time: {time} nodes removed: {removed_nodes}  length: {length}".format(i=i+1,time=(time.time() - start_time),
    removed_nodes=finish[1],length=finish[0].path_cost))
    start_time = time.time()
    finish=newastar_search(instance,instance.max_of_two)
    print("MAX trial {i}\n time: {time} nodes removed: {removed_nodes}  length: {length}".format(i=i+1,time=(time.time() - start_time),
    removed_nodes=finish[1],length=finish[0].path_cost))
print()
print()    
for i in range(10):
    instance = make_rand_duckpuzzle()
    start_time = time.time()
    finish=newastar_search(instance,instance.h)
    print("MIS trial {i}\n time: {time} nodes removed: {removed_nodes}  length: {length}".format(i=i+1,time=(time.time() - start_time),
    removed_nodes=finish[1],length=finish[0].path_cost))
    start_time = time.time()
    finish=newastar_search(instance,instance.man)
    print("MAN trial {i}\n time: {time} nodes removed: {removed_nodes}  length: {length}".format(i=i+1,time=(time.time() - start_time),
    removed_nodes=finish[1],length=finish[0].path_cost))
    start_time = time.time()
    finish=newastar_search(instance,instance.max_of_two)
    print("MAX trial {i}\n time: {time} nodes removed: {removed_nodes}  length: {length}".format(i=i+1,time=(time.time() - start_time),
    removed_nodes=finish[1],length=finish[0].path_cost))
       




