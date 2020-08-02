import numpy as np
from search import *
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

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan_distance(self, node):
        state = node.state
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index_state = {}
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        x, y = 0, 0
        
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        
        manh_dist = 0
        manh_x = 0
        manh_y = 0
        
        for i in range(9):
           x = abs(index_goal[i][0] - index_state[i][0]) 
           manh_x = x + manh_x
           y = abs(index_goal[i][1] - index_state[i][1])
           manh_y = y + manh_y

        manh_dist = manh_x + manh_y

        return manh_dist

    def max_distance(self, node):
    	return (max(self.h(node), self.manhattan_distance(node)))

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n),display)



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
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, len(explored)]
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
	state = tuple(np.random.permutation(9))
	puzzle = EightPuzzle(initial=state)

	while puzzle.check_solvability(state) == False:
		state = tuple(np.random.permutation(9))
		puzzle = EightPuzzle(initial=state)

	return puzzle


def display(state):
	for i in range(0,9):
		if (i%3==0 and i!=0):
			print("")

		if(state[i]!=0):
			print(state[i], "",end="")
		else:
			print("*","",end="")

	print("")


for i in range(10):

	puzzle = make_rand_8puzzle()

	display(puzzle.initial)

	print("A*-search using the misplaced tile heuristic ")

	start = time.time()
	output = astar_search(puzzle)
	end = time.time()

	print ("The total running time in seconds: ",end-start)
	print("The length (i.e. number of tiles moved) of the solution: ",output[0].path_cost)
	print ("Total number of nodes that were removed from frontier: ",output[1], "\n")


	print("A*-search using the Manhattan distance heuristic ")

	start = time.time()
	output_mht = astar_search(puzzle, h=puzzle.manhattan_distance)
	end = time.time()

	print ("The total running time in seconds: ",end-start)
	print("The length (i.e. number of tiles moved) of the solution: ",output_mht[0].path_cost)
	print ("Total number of nodes that were removed from frontier: ",output_mht[1], "\n")


	print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic ")

	start = time.time()
	output_max = astar_search(puzzle, h=puzzle.max_distance)
	end = time.time()

	print ("The total running time in seconds: ",end-start)
	print("The length (i.e. number of tiles moved) of the solution: ",output_max[0].path_cost)
	print ("Total number of nodes that were removed from frontier: ",output_max[1], "\n")


class DuckPuzzle(Problem):
    """ 
    +--+--+
    |  |  |
    +--+--+--+--+
    |  |  |  |  |
    +--+--+--+--+
       |  |  |  |
       +--+--+--+
    
     1 2
     3 4 5 6   goal state
       7 8 *
    """

    def __init__(self, initial, goal=(1,2,3,4,5,6,7,8,0)):
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

        no_move_up = (0,1,4,5)
        no_move_down = (2,6,7,8)
        no_move_left = (0,2)
        no_move_right = (5,8)

        if index_blank_square in no_move_left:
            possible_actions.remove('LEFT')
        if index_blank_square in no_move_up:
            possible_actions.remove('UP')
        if index_blank_square in no_move_right:
            possible_actions.remove('RIGHT')
        if index_blank_square in no_move_down:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta_1 = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        group_1 = {1,3,6}
        delta_2 = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        if blank in group_1:
            neighbor = blank + delta_1[action]
        else:
            neighbor = blank + delta_2[action]

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


    def manhattan_distance(self, node):
        state = node.state
        #index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index_goal = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}

        index_state = {}
        #index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]

        x, y = 0, 0
        
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        
        manh_dist = 0
        manh_x = 0
        manh_y = 0
        
        for i in range(9):
           x = abs(index_goal[i][0] - index_state[i][0]) 
           manh_x = x + manh_x
           y = abs(index_goal[i][1] - index_state[i][1])
           manh_y = y + manh_y

        manh_dist = manh_x + manh_y

        return manh_dist

    def max_distance(self, node):
        return (max(self.h(node), self.manhattan_distance(node)))


def make_rand_duck_puzzle():
    state = tuple(np.random.permutation(9))
    puzzle = DuckPuzzle(initial=state)

    while puzzle.check_solvability(state) == False:
        state = tuple(np.random.permutation(9))
        puzzle = DuckPuzzle(initial=state)

    return puzzle


def display_duck_puzzle(state):
    state_display = []

    for i in range(0,9):
        state_display.append(state[i])
        if state_display[i] == 0:
            state_display[i] = "*"

    print(state_display[0],state_display[1]," ")
    print(state_display[2],state_display[3],state_display[4],state_display[5])
    print(" ", state_display[6],state_display[7],state_display[8])



for i in range(10):

    duck_puzzle = make_rand_duck_puzzle()

    display_duck_puzzle(duck_puzzle.initial)

    print("A*-search using the misplaced tile heuristic ")

    start = time.time()
    output = astar_search(duck_puzzle)
    end = time.time()

    print ("The total running time in seconds: ",end-start)
    print("The length (i.e. number of tiles moved) of the solution: ",output[0].path_cost)
    print ("Total number of nodes that were removed from frontier: ",output[1], "\n")


    print("A*-search using the Manhattan distance heuristic ")

    start = time.time()
    output_duck_mht = astar_search(duck_puzzle, h=duck_puzzle.manhattan_distance)
    end = time.time()

    print ("The total running time in seconds: ",end-start)
    print("The length (i.e. number of tiles moved) of the solution: ",output_duck_mht[0].path_cost)
    print ("Total number of nodes that were removed from frontier: ",output_duck_mht[1], "\n")


    print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic ")

    start = time.time()
    output_duck_max = astar_search(duck_puzzle, h=duck_puzzle.max_distance)
    end = time.time()

    print ("The total running time in seconds: ",end-start)
    print("The length (i.e. number of tiles moved) of the solution: ",output_duck_max[0].path_cost)
    print ("Total number of nodes that were removed from frontier: ",output_duck_max[1], "\n")






