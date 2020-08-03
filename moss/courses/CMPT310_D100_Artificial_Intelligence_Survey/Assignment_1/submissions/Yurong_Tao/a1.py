from search import *
import numpy as np
import time

#Q1
def make_rand_8puzzle():
    state = tuple(np.random.permutation(9))
    dummy_puzzle = EightPuzzle(initial=state)
    solve = dummy_puzzle.check_solvability(state)
    if solve == True:
        return state
    else:
        return make_rand_8puzzle()

def display(state):
    #astate = np.array(state).reshape(3,3)
    for i in range(9):
        if state[i] != 0:
            if i%3 != 2:
                print(state[i], end=" ")
            else:
                print(state[i], end="\n")
        else:
            if i%3 != 2:
                print("*", end=" ")
            else:
                print("*", end="\n")

'''state = make_rand_8puzzle()
print("random 8-puzzle state is:", state)
display(state)'''

#Q2

def make_rand_8puzzle_ten():
    for i in range(10):
        state = tuple(np.random.permutation(9))
        dummy_puzzle = EightPuzzle(initial=state)
        solve = dummy_puzzle.check_solvability(state)
        if solve == True:
            return state
        else:
            return make_rand_8puzzle_ten()

def best_first_graph_search(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    removed_num = 0
    while frontier:
        node = frontier.pop()
        removed_num += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node,removed_num
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None,removed_num

def astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def hman(node):
    dis_sum = 0   
    for i, item in enumerate(node.state):
        state_row,state_col = int(i/3),int(i%3)
        if item == 0:
            goal_row = 2
            goal_col = 2
        else:
            goal_row,goal_col = int((item-1)/3),(item-1)%3
        dis_sum += abs(state_row-goal_row) + abs(state_col-goal_col)
        
    return dis_sum

def hmax(node):
    initm_puzzle = EightPuzzle(initial=node.state)
    initm_node = Node(state = node.state)
    misH = initm_puzzle.h(initm_node)
    mantH = hman(node)
    if misH > mantH:
        return misH
    else:
        return mantH

def misH(state):
    init_puzzle = EightPuzzle(initial=state)
    init_node = Node(state = state)
    hmis = init_puzzle.h(init_node)
    start_time = time.time()
    length,num_removed = astar_search(init_puzzle, h=init_puzzle.h)
    complete_time = time.time()
    running_time = complete_time - start_time
    print("misplaced: ")
    print("the total running time in seconds: ", running_time)
    print("length: ", length.path_cost)
    print("num_removed: ", num_removed)

def manH(state):
    init_puzzle = EightPuzzle(initial=state)
    start_time = time.time()
    length,num_removed = astar_search(init_puzzle, h=hman)
    complete_time = time.time()
    running_time = complete_time - start_time
    print("manhattan: ")
    print("the total running time in seconds: ", running_time)
    print("length: ", length.path_cost)
    print("num_removed: ", num_removed)

def maxH(state):
    init_puzzle = EightPuzzle(initial=state)
    start_time = time.time()
    length,num_removed = astar_search(init_puzzle, h=hmax)
    complete_time = time.time()
    running_time = complete_time - start_time
    print("max heuristic: ")
    print("the total running time in seconds: ", running_time)
    print("length: ", length.path_cost)
    print("num_removed: ", num_removed)

'''for i in range(10):
    state = make_rand_8puzzle_ten()
    print("random 8-puzzle state is:", state)
    misH(state)
    manH(state)
    maxH(state)'''

#Q3
class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square in [0, 2, 6]:
            possible_actions.remove('LEFT')
        if index_blank_square in [0, 1, 4, 5]:
            possible_actions.remove('UP')
        if index_blank_square in [1, 5, 8]:
            possible_actions.remove('RIGHT')
        if index_blank_square in [2, 6, 7, 8]:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank in [0, 1]:
            delta = {'DOWN': 2}
        if blank in [2, 3]:
            delta = {'UP': -2}
        
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def check_solvability(self, state):
        for i in [0, 1, 2, 3]:
            if state[i] not in [1, 2, 3, 4]:
                return False
            
        for i in [4, 5, 6, 7, 8]:
            if state[i] not in [0, 5, 6, 7, 8]:
                return False
        
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

def make_rand_duck_puzzle():
    state = tuple(np.random.permutation(9))
    dummy_puzzle = DuckPuzzle(initial=state)
    solve = dummy_puzzle.check_solvability(state)
    if solve == True:
        return state
    else:
        return make_rand_duck_puzzle()

for i in range(10):
    state = make_rand_duck_puzzle()
    print("random duck-puzzle state is:", state)
    misH(state)
    manH(state)
    maxH(state)