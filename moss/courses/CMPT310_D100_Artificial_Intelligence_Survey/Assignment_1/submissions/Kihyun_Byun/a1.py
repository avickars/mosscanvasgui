# a1.py

from search import *
import random
import time

# Author:Keenan Byun
# Date: May 25 2020
# CMPT310



#------------------------COPIED FROM search.py FOR MODIFY PURPOSE---------------------------

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
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print("total number of nodes that were removed from frontier:",len(explored))
                print("the length of the solution:",node.depth)
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

def astar_search(problem, h, display=True):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

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
        result=sum(s != g for (s, g) in zip(node.state, self.goal))
        if(node.state[8]==0):
            return result
        else:
            return result-1
        
    def m(self, node):
        """Return the heuristic value for a given state. h(n) = Manhattan distance """
        result=0
        for i in range (len(node.state)):
            if(node.state[i]!=0):
                x1=i%3
                y1=int(i/3)
                x2=(node.state[i]-1)%3
                y2=int((node.state[i]-1)/3)
                result+=abs(x1-x2)+abs(y1-y2)
        return result

class EightPuzzleT(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a duck puzzle board, where one of the
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
            possible_actions.remove('LEFT')
        elif index_blank_square == 1 or index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        elif index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif index_blank_square == 4:
            possible_actions.remove('UP')
        elif index_blank_square == 7:
            possible_actions.remove('DOWN')
        elif index_blank_square == 8:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')
            

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        if(blank<3):
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if(blank>3):
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if(blank==3):
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        result=sum(s != g for (s, g) in zip(node.state, self.goal))
        if(node.state[8]==0):
            return result
        else:
            return result-1
        
    def m(self, node):
        """Return the heuristic value for a given state. h(n) = Manhattan distance """
        result=0
        for i in range (len(node.state)):
            if(node.state[i]!=0):
                x1=i%3
                y1=int(i/3)
                x2=(node.state[i]-1)%3
                y2=int((node.state[i]-1)/3)
                result+=abs(x1-x2)+abs(y1-y2)
        return result

# ____________________________END__________________________________________________
def ff(problem):
    """time measure function for a function"""
    A=Node(a.initial)
    
    print("-----------------misplaced tile heuristic--------------------------------------")
    start_time = time.time()
    astar_search(problem,problem.h)
    """misplaced tile heuristic"""
    elapsed_time = time.time() - start_time
    print("elapsed time (in seconds):",elapsed_time)
    print("misplaced tile heuristic value: ", a.h(A), end='\n')
    
    print("-----------------manhattan heuristic-------------------------------------------")
    start_time = time.time()
    astar_search(problem,problem.m)
    """manhattan heuristic"""
    elapsed_time = time.time() - start_time
    print("elapsed time (in seconds):",elapsed_time)
    print("manhattan heuristic value: ", a.m(A), end='\n')
    

    print("-----------------max of misplaced tile heuristic and manhattan heuristic-------")
    if(a.h(A)>a.m(A)):
        start_time = time.time()
        astar_search(problem,problem.h)
        elapsed_time = time.time() - start_time
        print("elapsed time (in seconds):",elapsed_time)
    else:
        start_time = time.time()
        astar_search(problem,problem.m)
        elapsed_time = time.time() - start_time
        print("elapsed time (in seconds):",elapsed_time)
    """max of misplaced tile heuristic and manhattan heuristic"""
    print('\n')
    return None

def make_rand_8puzzle():
    """returns a instance of EightPuzzle class with randomly initialized state."""
    swit=0
    while(swit==0):
        rand_initial=[0,1,2,3,4,5,6,7,8]
        random.shuffle(rand_initial)
        rand_initial=tuple(rand_initial)
        puzzle8=EightPuzzle(rand_initial)
        if(puzzle8.check_solvability(puzzle8.initial)==True):
            swit=1 
    return puzzle8

def display(state):
    """display a given state to 3x3 puzzle form. 0 is supposed to be printed as blank('*')"""
    for i in range(len(state)):
        if (state[i]==0):
            print('*', end=' ')
        else:
            print(state[i], end=' ')
        if(i==2 or i==5 or i==8):
            print('\n', end='')

def make_rand_8puzzleT():
    """returns a instance of EightPuzzleT class with randomly initialized state."""
    initial=(1,2,3,4,5,6,7,8,0)
    puzzleT=EightPuzzleT(initial)
    state=initial
    for i in range(1000):
        act=random.choice(puzzleT.actions(state))
        state=puzzleT.result(state,act)
    puzzleT.initial=state
    return puzzleT

def displayT(state):
    """display a given state to duck puzzle form. 0 is supposed to be printed as blank('*')"""
    for i in range(len(state)):
        if (i!=6):
            if (state[i]!=0):
                print(state[i], end=' ')
            else:
                print('*', end=' ')
        else:
            if (state[i]!=0):
                print(' ', state[i], end=' ')
            else:
                print('  *', end=' ')
        if(i==1 or i==5 or i==8):
            print('\n', end='')

            

for i in range(10):
    a=make_rand_8puzzleT()
    displayT(a.initial)
    ff(a)

for i in range(10):
    b=make_rand_8puzzle()
    display(b.initial)
    ff(b)





