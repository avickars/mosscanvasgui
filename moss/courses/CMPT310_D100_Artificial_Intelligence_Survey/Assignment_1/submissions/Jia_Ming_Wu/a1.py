from search import *
import random
import time

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
        #not to include 0
        return sum(s != g and s!= 0 for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        """manhattan heuristic"""
        state = node.state
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index_state = {} 
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
 
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        mhd = 0
        
        for i in range(1,9):
            
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

        
        return mhd

    def maxh(self, node):
        """Max of two heuristic, h or manhattan"""
        h_heuristic = self.h(node)
        manhattan_heuristic = self.manhattan(node)
        if h_heuristic > manhattan_heuristic:
            return h_heuristic
        else:
            return manhattan_heuristic

       
def check_solvability(state):
        """ Checks if the given state is solvable """
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1
        return inversion % 2 == 0

def make_rand_8puzzle() :
        """return a puzzle problem with a random initial state that is solvable"""

        temp_puzzle=random.sample(range(9), 9);
        while check_solvability(temp_puzzle)!=True:
            temp_puzzle=random.sample(range(9), 9);
        else:
            temp_puzzle=tuple(temp_puzzle);
            puzzle = EightPuzzle(temp_puzzle);
        return puzzle;

def make_rand_duckpuzzle() :
        """return a puzzle problem with a random initial state that is solvable"""
        temp_puzzle=random.sample(range(9), 9);
        temp_puzzle=tuple(temp_puzzle);
        puzzle = duckPuzzle(temp_puzzle);
        while astar_search(puzzle) is None:
            temp_puzzle=random.sample(range(9), 9);
            temp_puzzle=tuple(temp_puzzle);
            puzzle = duckPuzzle(temp_puzzle);
        else:
            return puzzle

def display(state):

    temp_state = [];
    for x in range(9):
        if (state[x] == 0):
            temp_state.append("*");
        else:
            temp_state.append(state[x]);

 
    print(temp_state[0],temp_state[1],temp_state[2])
    print(temp_state[3],temp_state[4],temp_state[5])
    print(temp_state[6],temp_state[7],temp_state[8])

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""

    #used to count node pop
    count=0;
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        #record count of node pop
        count+=1;
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            #return node and count together
            return [node,count]
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

    #added manhattan and maxh solution
    h = memoize(h or problem.h or problem.manhattan or problem.maxh, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

class duckPuzzle(Problem):
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

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # movement for 0 1 2
        delta_lessthanthree = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}

        # movement for 3
        delta_three = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        # movement for 4 5 6 7 8
        delta_overthree = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}


        #sum up the action
        if blank == 3:
           neighbor = blank + delta_three[action]
        elif blank in (0,1,2):
           neighbor = blank + delta_lessthanthree[action]
        else:
            neighbor = blank + delta_overthree[action]


        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0
        

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        #not to include 0
        return sum(s != g and s!=0 for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        """Manhattan heuristic"""
        state = node.state
        index_goal = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
        index_state = {} 
        index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
        

        for i in range(len(state)):
            index_state[state[i]] = index[i]
       
        mhd = 0

        for i in range(1,9):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
            

        return mhd


    def maxh(self, node):
        """Max of two heuristic, h or manhattan"""
        h_heuristic = self.h(node)
        manhattan_heuristic = self.manhattan(node)
        if h_heuristic > manhattan_heuristic:
            return h_heuristic
        else:
            return manhattan_heuristic

def display_duckpuzzle(state):

    temp_state = [];
    for x in range(9):
        if (state[x] == 0):
            temp_state.append("*");
        else:
            temp_state.append(state[x]);

 
    print(temp_state[0],temp_state[1])
    print(temp_state[2],temp_state[3],temp_state[4],temp_state[5])
    print(" ",temp_state[6],temp_state[7],temp_state[8])




##------Main for normal puzzle
def eightpuzzle_main():
    print("------Eight Puzzle Solve------")
    for i in range(1,11):
        print("puzzle: ", i)
        puzzle=make_rand_8puzzle()
        display(puzzle.initial)
        print("Misplaced tile heuristic")
        start_time = time.time()
        output = astar_search(puzzle,puzzle.h,True)
        elapsed_time = time.time()
        print ("Time Spent: ",elapsed_time-start_time)
        print("Path cost: ",output[0].path_cost)
        print("Node pop: ",output[1])

        print("Manhattan heuristic")
        start_time = time.time()
        output = astar_search(puzzle,puzzle.manhattan,True)
        elapsed_time = time.time()
        print ("Time Spent: ",elapsed_time-start_time)
        print("Path cost: ",output[0].path_cost)
        print("Node pop: ",output[1])

        print("Max of two heuristic")
        start_time = time.time()
        output = astar_search(puzzle,puzzle.maxh,True)
        elapsed_time = time.time()
        print ("Time Spent: ",elapsed_time-start_time)
        print("Path cost: ",output[0].path_cost)
        print("Node pop: ",output[1])

#------Main for duck puzzle
def duckpuzzle_main():
    print("------Duck Puzzle Solve-------")
    for i in range(1,11):
        print("puzzle: ", i)
        puzzle=make_rand_duckpuzzle();
        display_duckpuzzle(puzzle.initial);

        print("Misplaced tile heuristic")
        start_time = time.time()
        output = astar_search(puzzle,puzzle.h,True)
        elapsed_time = time.time()
        print ("Time Spent: ",elapsed_time-start_time)
        print("Path cost: ",output[0].path_cost)
        print("Node pop: ",output[1])

        print("Manhattan heuristic")
        start_time = time.time()
        output = astar_search(puzzle,puzzle.manhattan,True)
        elapsed_time = time.time()
        print ("Time Spent: ",elapsed_time-start_time)
        print("Path cost: ",output[0].path_cost)
        print("Node pop: ",output[1])

        print("Max of two heuristic")
        start_time = time.time()
        output = astar_search(puzzle,puzzle.maxh,True)
        elapsed_time = time.time()
        print ("Time Spent: ",elapsed_time-start_time)
        print("Path cost: ",output[0].path_cost)
        print("Node pop: ",output[1])




### function to test eight puzzle
eightpuzzle_main()

### function to test duck puzzle
duckpuzzle_main()


