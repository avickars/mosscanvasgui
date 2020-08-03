from search import *
import random
import time
import secrets

class new_EightPuzzle(Problem):
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
        return sum(s != g  and s != 0 for (s, g) in zip(node.state, self.goal))



    """ idea of definition of Manhattan distance from the textbook，code implementation changed based on the test_search.py"""
    def mht(self, node):
        state = node.state
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        index_state = {}
        mht_move = 0
        for i in range(len(state)):
            index_state[state[i]] = index[i]

        for i in range(1,9):
            for j in range(2):
                mht_move = abs(index_state[i][j] - index_goal[i][j]) + mht_move
        return mht_move


    def max(self, node):
        return max(self.h(node), self.mht(node))
        

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
        if index_blank_square < 4:
            if index_blank_square == 0:
                possible_actions = ['RIGHT','DOWNTWO']
            elif index_blank_square == 1:
                possible_actions = ['LEFT','DOWNTWO']
            elif index_blank_square == 2:
                possible_actions = ['UPTWO','RIGHT']
            else:
                possible_actions[0] = 'UPTWO'
        elif index_blank_square == 4:
            possible_actions.remove('UP')
        elif index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        elif index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif index_blank_square == 7:
            possible_actions.remove('DOWN')
        elif index_blank_square == 8:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')       

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1, 'UPTWO':-2, 'DOWNTWO':2}
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

        return sum(s != g  and s != 0 for (s, g) in zip(node.state, self.goal))

    """ idea of definition of Manhattan distance from the textbook，code implementation changed based on the test_search.py"""
    def mht(self, node):
        state = node.state
        index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
        index_state = {}
        index = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        mht_move = 0
        for i in range(1,9):
            for j in range(2):
                mht_move = abs(index_goal[i][j] - index_state[i][j]) + mht_move
        return mht_move


    def max(self, node):
        return max(self.h(node), self.mht(node))

# ___________________________________

def new_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return new_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def new_best_first_graph_search(problem, f, display=False):
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
    removed_frontier = 0
    while frontier:
        node = frontier.pop()
        removed_frontier += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, removed_frontier
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def make_rand_8puzzle():
    while True:
        puz = random.sample(range(0, 9), 9)
        puz = tuple(puz)
        puz2 = new_EightPuzzle(puz)
        if(puz2.check_solvability(puz2.initial)):
            return puz2

def display(puz):
    blank = puz.find_blank_square(puz.initial)
    new_state = list(puz.initial)
    new_state[blank]='*'
    state = tuple(new_state)
    for x in range(0,3):
        print(state[x],end='')
    print('\n',end='')
    for x in range(3,6):
        print(state[x],end='')
    print('\n',end='')
    for x in range(6,9):
        print(state[x],end='')
    print('\n',end='')


    """ 8 puzzle measurement """
for i in range(0,10):
    puz = make_rand_8puzzle()
    display(puz)

    start_time_heu = time.time()
    algorithm_heu = new_astar_search(puz, puz.h)
    elapsed_time_heu = time.time() - start_time_heu
    length_heu = algorithm_heu[0].path_cost
    removed_node_heu = algorithm_heu[1]
    print(f'running time for heu src:{elapsed_time_heu}s')
    print(f'length for heu src: {length_heu}')
    print(f'# of nodes removed: {removed_node_heu}')

    start_time_mht = time.time()
    algorithm_mht = new_astar_search(puz, puz.mht)
    elapsed_time_mht = time.time() - start_time_mht
    length_mht = algorithm_mht[0].path_cost
    removed_node_mht = algorithm_mht[1]
    print(f'running time for Manhattan heu:{elapsed_time_mht}s')
    print(f'length for Manhattan heu: {length_mht}')
    print(f'# of nodes removed: {removed_node_mht}')

    start_time_max = time.time()
    algorithm_max = new_astar_search(puz, puz.max)
    elapsed_time_max = time.time() - start_time_max
    length_max = algorithm_max[0].path_cost
    removed_node_max = algorithm_max[1]
    print(f'running time for the max of two:{elapsed_time_max}s')
    print(f'length for max of two: {length_max}')
    print(f'# of nodes removed: {removed_node_max}')



    """RANDOM puzzle for duck puzzle"""
def Duck_make_rand_8puzzle():
    puz = [1,2,3,4,5,6,7,8,0]
    temp = DuckPuzzle(puz)
    for i in range(1000):
        moves = temp.actions(temp.initial)
        rdm = secrets.choice(moves) 
        temp.initial = temp.result(temp.initial,rdm)
    return temp


    """ measurement for duck puzzle """
for i in range(0,10):
    puz = Duck_make_rand_8puzzle()
    dsiplay(puz)
    start_time_heu = time.time()
    algorithm_heu = new_astar_search(puz, puz.h)
    elapsed_time_heu = time.time() - start_time_heu
    length_heu = algorithm_heu[0].path_cost
    removed_node_heu = algorithm_heu[1]
    print(f'DUCK: running time for heu src:{elapsed_time_heu}s')
    print(f'DUCK:length for heu src: {length_heu}')
    print(f'DUCK:# of nodes removed: {removed_node_heu}')

    start_time_mht = time.time()
    algorithm_mht = new_astar_search(puz, puz.mht)
    elapsed_time_mht = time.time() - start_time_mht
    length_mht = algorithm_mht[0].path_cost
    removed_node_mht = algorithm_mht[1]
    print(f'DUCK:running time for Manhattan heu:{elapsed_time_mht}s')
    print(f'DUCK:length for Manhattan heu: {length_mht}')
    print(f'DUCK:# of nodes removed: {removed_node_mht}')

    start_time_max = time.time()
    algorithm_max = new_astar_search(puz, puz.max)
    elapsed_time_max = time.time() - start_time_max
    length_max = algorithm_max[0].path_cost
    removed_node_max = algorithm_max[1]
    print(f'DUCK:running time for the max of two:{elapsed_time_max}s')
    print(f'DUCK:length for max of two: {length_max}')
    print(f'DUCK:# of nodes removed: {removed_node_max}')
