from search import *


#Reference:
#EightPuzzle class and best_first_graph_search function are from the aima-python search.py
#the idea for how to calculate manhattan distance is from https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
import random

import time
random.seed(0)



def make_rand_8puzzle():
    init = list(range(9))
    random.shuffle(init)
    init_state = EightPuzzle(tuple(init))
    while not init_state.check_solvability(init):
        init = list(range(9))
        random.shuffle(init)
        init_state = EightPuzzle(tuple(init))

    return init_state


def make_rand_duck_puzzle():
    duck_puzzle = DuckPuzzle(num_steps_to_inital=random.randint(100, 200))
    return duck_puzzle

def display(state):
	for i, each in enumerate(state.initial):
		if i%3 == 0 and i != 0:
			print()
		if each == 0:
			each = "*"
		print(str(each)+" ", end="")
	print()

def displayDuck(state):
    for each in state.initial[:2]:
        if each == 0:
            each = "*"
        print(str(each)+" ", end="")
    print()
    for each in state.initial[2:6]:
        if each == 0:
            each = "*"
        print(str(each)+" ", end="")    
    print()
    print("  ", end="")
    for each in state.initial[6:]:
        if each == 0:
            each = "*"
        print(str(each)+" ", end="")


def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    frontier_removed = 0
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
            return node, frontier_removed, len(explored)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier_removed += 1
                    frontier.append(child)
    return None 
	
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

    #original h
    # def h(self, node):
    #     """ Return the heuristic value for a given state. Default heuristic function used is 
    #     h(n) = number of misplaced tiles """

    #     return sum(s != g for (s, g) in zip(node.state, self.goal))
    
    #algo2
    # def h(self, node):
    #     dist = 0
    #     for i, num in enumerate(node.state):
    #         if num:
    #             tmp = abs((num-1)%3 - i%3) + abs((num-1)//3 - i//3)
    #             dist += tmp
    #     return dist


    # algo3
    def h(self, node):
        dist = 0
        for i, num in enumerate(node.state):
            if num:
                tmp = abs((num-1)%3 - i%3) + abs((num-1)//3 - i//3)
                dist += tmp
        mis_place = sum(s != g for (s, g) in zip(node.state, self.goal))
        return max(dist, mis_place)		




class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial=None, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0), num_steps_to_inital = 25):
        """ Define goal state and initialize a problem """
        initial = goal
        for _ in range(num_steps_to_inital):
            possible_actions = self.actions(initial)
            initial = self.result(initial, random.choice(possible_actions))
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):

        index_blank_square = self.find_blank_square(state)

        if index_blank_square  == 0:
            return ['RIGHT', 'DOWN']
        if index_blank_square == 1:
            return ['LEFT','DOWN']
        if index_blank_square  == 2:
            return ['UP', 'RIGHT']
        if index_blank_square == 3:
            return ['UP','DOWN','LEFT','RIGHT']
        if index_blank_square  == 4:
            return ['RIGHT', 'DOWN','LEFT']
        if index_blank_square == 5:
            return ['LEFT','DOWN']
        if index_blank_square == 6:
            return ['UP','RIGHT']
        if index_blank_square == 7:
            return ['LEFT','UP','RIGHT']
        if index_blank_square == 8:
            return ['LEFT','UP']

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        neighbors = {
        	0: {'RIGHT': 1, 'DOWN':2},
        	1: {'LEFT': 0, 'DOWN':3},
        	2: {'UP': 0, 'RIGHT':3},
        	3: {'UP': 1, 'DOWN':6, 'RIGHT':4,"LEFT":2},
        	4: {'RIGHT': 5, 'DOWN': 7, 'LEFT': 3},
        	5: {'LEFT': 4, 'DOWN': 8},
        	6: {'UP': 3, 'RIGHT': 7},
        	7: {'LEFT': 6, 'RIGHT': 8, 'UP': 4},
        	8: {'LEFT': 7, 'UP': 5},
        }
        neighbor = neighbors[blank][action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    #original h
    # def h(self, node):
    #     """ Return the heuristic value for a given state. Default heuristic function used is 
    #     h(n) = number of misplaced tiles """

    #     return sum(s != g for (s, g) in zip(node.state, self.goal))
    
    #algo2
    # def h(self, node):
    #     dist = 0
    #     for i, num in enumerate(node.state):
    #         if num:
    #             tmp = abs((num-1)%3 - i%3) + abs((num-1)//3 - i//3)
    #             dist += tmp
    #     return dist


    # algo3
    def h(self, node):
        dist = 0
        for i, num in enumerate(node.state):
            if num:
                tmp = abs((num-1)%3 - i%3) + abs((num-1)//3 - i//3)
                dist += tmp
        mis_place = sum(s != g for (s, g) in zip(node.state, self.goal))
        return max(dist, mis_place)



for rep in range(10):
	random.seed(rep)
	print("**** Experiment "+str(rep)+"****")

	state = make_rand_8puzzle()
	# state = make_rand_duck_puzzle()
	display(state)
	# displayDuck(state)

	start_time = time.time()
	# run algo1
	node, frontier_removed, num_act = astar_search(state)
	end_time = time.time()
	print(f"time consumed: ", end_time - start_time)
	print(f"frontier removed: {frontier_removed}")
	print(f"length of the solutin: {num_act}")

print()
print("***************Experiment for DuckPuzzle**********************")
print()


for rep in range(10):
	random.seed(rep)
	print("**** Experiment "+str(rep)+"****")

	state = make_rand_duck_puzzle()
	displayDuck(state)

	start_time = time.time()
	# run algo1
	node, frontier_removed, num_act = astar_search(state)
	end_time = time.time()
	print(f"time consumed: ", end_time - start_time)
	print(f"frontier removed: {frontier_removed}")
	print(f"length of the solutin: {num_act}")