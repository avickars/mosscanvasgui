from search import *
import random
import time

def make_rand_8puzzle():
    input = [1,2,3,4,5,6,7,8,0]
    while (True):
        random.shuffle(input)
        puzz = EightPuzzle(input)
        if(puzz.check_solvability(input)):
            puzz.initial = tuple(puzz.initial)
            break
    return puzz

def display(state):
    new_state = list(state).copy()
    output = ''
    dictionary = {0: '*', 1: '1', 2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8'}
    for i in range(len(new_state)):
        output += dictionary[new_state[i]]
        if(i % 3 == 2 and i != len(new_state)):
            output += '\n'
        else:
            output += ' '
    print(output)
    

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    # copied from the textbook code so that it can be modified
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print('path length', len(node.path())-1)
                print(len(explored)+1, "nodes removed from the frontier")
            path_len = len(node.path())-1
            nodes_removed = len(explored)+1
            return path_len, nodes_removed
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None 

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    # unchanged from textbook
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def manhattan(node):
    state = list(node.state)
    dist = 0
    for i in range(9):
        # the value that is currently stored in the index
        val = state[i]     
        if val == 0:
            continue
        # where the value should be located
        x1 = (val-1)%3
        y1 = (val-1)//3
        # where it is currently located
        x2 = i%3
        y2 = i//3
        # manhattan distance per piece of the puzzle
        dist += abs(x1-x2) + abs(y1-y2)
    return dist


class DuckPuzzle(EightPuzzle):
    
    def __init__(self, initial, goal=(1,2,None,None,3,4,5,6,None,7,8,0)):
        # use None to represent the spaces that are not possible moves in a 3x4 board
        super().__init__(initial, goal)
        
    def actions(self, state):
        # have to change this to take the new 4x4 board and None squares into account
        
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
        lst = list(state)

        if index_blank_square % 4 == 0 or lst[index_blank_square-1] == None:
            possible_actions.remove('LEFT')
        if index_blank_square < 4 or lst[index_blank_square-4] == None:
            possible_actions.remove('UP')
        if index_blank_square % 4 == 3 or lst[index_blank_square+1] == None:
            possible_actions.remove('RIGHT')
        if index_blank_square > 7 or lst[index_blank_square+4] == None:
            possible_actions.remove('DOWN')

        return possible_actions
    
    def result(self, state, action):
        # changed the values of up and down for the new 3x4 board
        
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)
    
    def check_solvability(self, state):
        # won't work with the new arangement of the puzzle, raise an exception if its used
        raise Exception('Don\'t use this')
    
# ______________________________________________________ end of DuckPuzzle

def dispDuck(state):
    new_state = list(state).copy()
    output = ''
    dictionary = {0: '*', None : ' ', 1: '1', 2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8'}
    for i in range(len(new_state)):
        output += dictionary[new_state[i]]
        if(i % 4 == 3 and i != len(new_state)):
            output += '\n'
        else:
            output += ' '
    print(output)
    
def make_rand_dpuzzle():
    """ Since all of the moves on the puzzle board are reversible,
        I chose to start with a completed board and then permutate
        it by choosing possible moves at random"""
    
    # start off with a completed puzzle
    puzz = DuckPuzzle((1,2,None,None,3,4,5,6,None,7,8,0))
    state = puzz.initial
    # keep track of the most recent move so we don't reverse our moves
    last_move = None
    # my way of making sure that our new move doesn't reverse our previous move
    dictionary = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1, None: 0}
    # make 100 random moves 
    for _ in range(100):
        # retrieve a list of possible actions from our current state
        actions = puzz.actions(state)
        # loop while our selected action doesn't undo the previous one
        while True:
            # select a random action from our list
            index = random.randrange(len(actions))
            if(dictionary[last_move] + dictionary[actions[index]] != 0):
                break
        # update our last move to the one we are about to make
        last_move = actions[index]
        # make the move
        state = puzz.result(state, actions[index])
    # set the new initial state to the one we just created
    puzz.initial = state
    return puzz

    
def duck_manhattan(node):
    state = list(node.state)
    dist = 0
    # dictionary for where the values should be 
    homes = {1:(0,0),2:(1,0),3:(0,1),4:(1,1),5:(2,1),6:(3,1),7:(1,2),8:(2,2)}
    for i in range(12):
        # the value that is currently stored in the index
        val = state[i]     
        # skip the empty squares
        if val == None or val == 0:
            continue
        x1 = i % 4
        y1 = i // 4
        x2, y2 = homes[val]
        dist += abs(x1-x2) + abs(y1-y2)
    return dist


# ____________________________________________________________



eight_puzzles = []
duck_puzzles = []
for i in range(10):
    eight_puzzles.append(make_rand_8puzzle())
    duck_puzzles.append(make_rand_dpuzzle())
eight_lens_missing = []
eight_rem_missing = []
eight_times_missing = []
duck_lens_missing = []
duck_rem_missing = []
duck_times_missing = []
eight_lens_manhattan = []
eight_rem_manhattan = []
eight_times_manhattan = []
duck_lens_manhattan = []
duck_rem_manhattan = []
duck_times_manhattan = []
for puzz in eight_puzzles:
    start = time.time()
    length, rem = astar_search(problem=puzz,h=puzz.h, display=False)
    end = time.time()
    eight_lens_missing.append(length)
    eight_rem_missing.append(rem)
    eight_times_missing.append((end-start)*1000)            # time in ms
    start = time.time()
    length, rem = astar_search(problem=puzz,h=manhattan, display=False)
    end = time.time()
    eight_lens_manhattan.append(length)
    eight_rem_manhattan.append(rem)
    eight_times_manhattan.append((end-start)*1000) 
for puzz in duck_puzzles:
    start = time.time()
    length, rem = astar_search(problem=puzz,h=puzz.h, display=False)
    end = time.time()
    duck_lens_missing.append(length)
    duck_rem_missing.append(rem)
    duck_times_missing.append((end-start)*1000)            # time in ms
    start = time.time()
    length, rem = astar_search(problem=puzz,h=duck_manhattan, display=False)
    end = time.time()
    duck_lens_manhattan.append(length)
    duck_rem_manhattan.append(rem)
    duck_times_manhattan.append((end-start)*1000) 
print('Eight puzzle, missing tile:')
for i in range(10):
    print(eight_times_missing[i],'ms,',eight_lens_missing[i],'path length,',eight_rem_missing[i],'nodes removed from frontier')
print('Eight puzzle, manhattan:')
for i in range(10):
    print(eight_times_manhattan[i],'ms,',eight_lens_manhattan[i],'path length,',eight_rem_manhattan[i],'nodes removed from frontier')
print('Duck puzzle, missing tile:')
for i in range(10):
    print(duck_times_missing[i],'ms,',duck_lens_missing[i],'path length,',duck_rem_missing[i],'nodes removed from frontier')
print('Duck puzzle, manhattan:')
for i in range(10):
    print(duck_times_manhattan[i],'ms,',duck_lens_manhattan[i],'path length,',duck_rem_manhattan[i],'nodes removed from frontier')