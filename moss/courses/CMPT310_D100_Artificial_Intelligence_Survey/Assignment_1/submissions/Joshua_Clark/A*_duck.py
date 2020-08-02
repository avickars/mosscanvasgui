import sys

import random

import bisect

from collections import deque

import time

# Python program for implementation of Quicksort Sort 

# This function takes last element as pivot, places 
# the pivot element at its correct position in sorted 
# array, and places all smaller (smaller than pivot) 
# to left of pivot and all greater elements to right 
# of pivot 
def partition(arr,low,high): 
	i = ( low-1 )		 # index of smaller element 
	pivot = arr[high]	 # pivot 

	for j in range(low , high): 

		# If current element is smaller than or 
		# equal to pivot 
		if arr[j].f_val <= pivot.f_val: 
		
			# increment index of smaller element 
			i = i+1
			arr[i],arr[j] = arr[j],arr[i] 

	arr[i+1],arr[high] = arr[high],arr[i+1] 
	return ( i+1 ) 

# The main function that implements QuickSort 
# arr[] --> Array to be sorted, 
# low --> Starting index, 
# high --> Ending index 

# Function to do Quick sort 
def quickSort(arr,low,high): 
	if low < high: 

		# pi is partitioning index, arr[p] is now 
		# at right place 
		pi = partition(arr,low,high) 

		# Separately sort elements before 
		# partition and after partition 
		quickSort(arr, low, pi-1) 
		quickSort(arr, pi+1, high) 


def selection_sort(nums):
    # This value of i corresponds to how many values were sorted
    for i in range(len(nums)):
        # We assume that the first item of the unsorted segment is the smallest
        lowest_value_index = i
        # This loop iterates over the unsorted items
        for j in range(i + 1, len(nums)):
            if nums[j].f_val < nums[lowest_value_index].f_val:
                lowest_value_index = j
        # Swap values of the lowest unsorted element with the first unsorted
        # element
        nums[i], nums[lowest_value_index] = nums[lowest_value_index], nums[i]
class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)


        

class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal = (1,2,3,4,5,6,7,8,0)):
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
        index= self.find_blank_square(state)

        if index < 2 or index == 4 or index == 5:
            possible_actions.remove('UP')
        if index > 5 or index == 2:
            possible_actions.remove('DOWN')
        if index % 4 == 1 or index == 8:
            possible_actions.remove('RIGHT')
        if index % 4 == 2 or index == 0:
            possible_actions.remove('LEFT')
        return possible_actions

        return possible_actions

    def result(self, state, action,delta):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        #delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)
    def init_print(self):
        print(self.initial)
        
        #print(np.matrix(self.initial))

    def current_print(self,state):
        print(state)
    def goal_print(self):

        print(self.goal)

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
    def zip(self,state):
        accum = 0
        for (s,g) in zip(state,self.goal):
            if (s != g):
                accum = accum + 1
        return accum

        #return (node.state)
        
    def h(self, node):

        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        print(node.state)
        #return sum(s != g for (s, g) in zip(node.state, self.goal))

    def difference(self,state):
        """Here check goal[i] with state[i], if different, accum"""
        accum = 0
        for x in range(9):
            if self.goal[x] != state[x]:
                accum += 1
        return accum

    def fun_delta(self,delta,index):
                if index == 0:
                        delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
                elif index == 1:
                        delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
                elif index == 2:
                        delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
                elif index == 3:
                        delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
                else:
                        delta = delta
                return delta

class State_Stats(EightPuzzle):


    def __init__(self,state,g_val):
        self.state = state
        self.next = None
        #Link prev states g val to current states g val
        self.g_val = g_val
        self.h_val = 0
        self.f_val = 0
        
        self.prev = None
def make_rand_8puzzle(current):
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        for x in range(1000):
                prev = current
                delta = solver.fun_delta(delta,current.index(0))
                actions = solver.actions(current)
                rand = random.randint(0,len(actions)-1)
                current = solver.result(prev,actions[rand],delta)
        return current
def display(state):
    temp = list(state)
    index = temp.index(0)
    temp[index] = '*'
    matrix = [temp[i:i+3] for i in range(0,len(temp),3)]
    #tuple(matrix)
    for l in matrix:
          print (l)
        
init = current = (1,2,3,4,5,6,7,8,0)


solver = EightPuzzle(init)


queue = []

delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}


init = current = make_rand_8puzzle(current)

start_time = time.time()
solver = EightPuzzle(init)

State = State_Stats(current,0)
actions = solver.actions(current)


queue.append(State)
error = False
delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
prevState = State_Stats(current,0)
accum = 0
memo = []
memo.append(solver.initial)
if(1<0):
    print("Not possible")
    error = True
    exit
else:

    while (not(solver.goal_test(current))):
        temp = []
        memo_iter = 0
        accum += 1
        this_delta = solver.fun_delta(delta,queue[0].state.index(0))
        actions = solver.actions(queue[0].state)
        prev = current = queue[0].state
        prevState = State_Stats(prev,queue[0].g_val)
        length = len(actions)
        for x in range(length):
            test = solver.result(prev,actions[x],this_delta)
            State = State_Stats(test,prevState.g_val)
            State.g_val = prevState.g_val + 1
            State.h_val = solver.difference(test)
            State.f_val = State.h_val + State.g_val
            State.prev = prevState
            temp.append(State)
        queue[0].f_val = 99999
        quickSort(temp,0,length-1)
        queue[0].f_val = 99999
        r = 1

        for y in temp:
            if (y.state not in memo):
                memo.append(y.state)
            else:
                continue
            length1 = len(queue)
            if (length1 == 1):
                queue.append(y)
                continue    
            while (queue[r].f_val < y.f_val):
                r += 1
                if (r == length1):
                     queue.append(y)
                     break
            temp2 = queue[r]
            queue.append(queue[0])
            for p in range(r,length1):
                 temp1 = temp2
                 temp2 = queue[p+1]
                 queue[p+1] = temp1
            queue[r] = y


        del (queue[0])

        current = queue[0].state

if not(error):
        display(current)
        print(queue[0].g_val)
        elapsed_time = time.time() - start_time
        print(elapsed_time)
        print(accum)

