from search import *
from random import seed
from random import shuffle
from datetime import datetime
import math
import time

pop_counter = 0

def make_rand_8puzzels():
	
	seed(datetime.now())
	sequence = [i for i in range (9)]
	shuffle(sequence)
	a = EightPuzzle(tuple(sequence))
	r = a.check_solvability(a.initial)
	if r:
		return a
	else:
		del a
		a = make_rand_8puzzels()
		return a
		
def display(state):
	temp = list(state)
	i = temp.index(0)
	temp[i]= "*"
	print(temp[0],temp[1],temp[2])
	print(temp[3],temp[4],temp[5])
	print(temp[6],temp[7],temp[8])
	del temp
	
def misplaced(node):
	goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]
	tuple(goal)
	return sum(s != g for (s, g) in zip(node.state, goal))

def manhatten_distance(node):
	state = list(node.state)
	total_for_all = 0
	for i in range(8):
		j = (i+8)%9
		goal_x = j%3
		goal_y = math.floor(j/3)
		temp = state.index(i)
		current_x = temp%3
		current_y = math.floor(temp/3)
		
		total_for_all += abs(goal_x - current_x) + abs(goal_y - current_y) 
		
	#print(total_for_all)
	return total_for_all
               
def max_man(node):
	x = manhatten_distance(node)
	y = misplaced(node)
	return max(x,y)
	
def custom_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return custom_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def custom_best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    global pop_counter
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        pop_counter += 1
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

def main_program():

	global pop_counter
	eight_puzzels = []
	
	for i in range(10):
		eight_puzzels.append(make_rand_8puzzels())
		display(eight_puzzels[i].initial)
		print("")
	
	list_times_misplaced = []
	list_paths_misplaced = []
	list_pops_misplaced = []	
	
	print("Misplaced Tile Heuristic")
	pop_counter = 0
	for i in range(10):
		temp = eight_puzzels[i]
		start = time.time()
		path = custom_astar_search(temp, temp.h)
		endtime = time.time() - start
		list_times_misplaced.append(endtime)
		print("Trail #", i+1)
		print("Time for trail: ",round(list_times_misplaced[i],3))
		list_paths_misplaced.append(len(path.solution()))
		print("Number of moves: ",list_paths_misplaced[i])
		list_pops_misplaced.append(pop_counter)
		print("Number of pops: ",list_pops_misplaced[i])
		pop_counter = 0
		print("")
		del temp
	
	print("Averge time = ", round(sum(list_times_misplaced)/len(list_times_misplaced), 3)," Seconds")
	print("Averge number of moves = ", sum(list_paths_misplaced)/len(list_paths_misplaced))
	print("Averge number of pops = ", sum(list_pops_misplaced)/len(list_pops_misplaced))
	print("")
	list_times_misplaced.clear()
	list_paths_misplaced.clear()
	list_pops_misplaced.clear()
	
	print("Manhatten Distance Heuristic")
	pop_counter = 0
	for i in range(10):
		temp = eight_puzzels[i]
		start = time.time()
		path = custom_astar_search(temp, manhatten_distance)
		endtime = time.time() - start
		list_times_misplaced.append(endtime)
		print("Trail #", i+1)
		print("Time for trail: ",round(list_times_misplaced[i],3))
		list_paths_misplaced.append(len(path.solution()))
		print("Number of moves: ",list_paths_misplaced[i])
		list_pops_misplaced.append(pop_counter)
		print("Number of pops: ",list_pops_misplaced[i])
		pop_counter = 0
		print("")
		del temp
	
	print("Averge time = ", round(sum(list_times_misplaced)/len(list_times_misplaced), 3)," Seconds")
	print("Averge number of moves = ", sum(list_paths_misplaced)/len(list_paths_misplaced))
	print("Averge number of pops = ", sum(list_pops_misplaced)/len(list_pops_misplaced))
	print("")
	list_times_misplaced.clear()
	list_paths_misplaced.clear()
	list_pops_misplaced.clear()
	
	print("Max Heuristic")
	pop_counter = 0
	for i in range(10):
		temp = eight_puzzels[i]
		start = time.time()
		path = custom_astar_search(temp, max_man)
		endtime = time.time() - start
		list_times_misplaced.append(endtime)
		print("Trail #", i+1)
		print("Time for trail: ",round(list_times_misplaced[i],3))
		list_paths_misplaced.append(len(path.solution()))
		print("Number of moves: ",list_paths_misplaced[i])
		list_pops_misplaced.append(pop_counter)
		print("Number of pops: ",list_pops_misplaced[i])
		pop_counter = 0
		print("")
		del temp
	
	print("Averge time = ", round(sum(list_times_misplaced)/len(list_times_misplaced), 3)," Seconds")
	print("Averge number of moves = ", sum(list_paths_misplaced)/len(list_paths_misplaced))
	print("Averge number of pops = ", sum(list_pops_misplaced)/len(list_pops_misplaced))
	print("")
	list_times_misplaced.clear()
	list_paths_misplaced.clear()
	list_pops_misplaced.clear()
	
		
main_program()

'''class Duck_EightPuzzle(Problem):
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
	
	switch (index_blank_square)
	case 0: possible_actions.remove('UP')
		possible_actions.remove('LEFT')
		break;
	case 1: possible_actions.remove('UP')
		possible_actions.remove('RIGHT')
		break;
	case 2: possible_actions.remove('DOWN')
		possible_actions.remove('LEFT')
		break;
	case 3: break;
	case 4: possible_actions.remove('UP')
		break;
	case 5: possible_actions.remove('UP')
		possible_actions.remove('RIGHT')
		break;
	case 6: possible_actions.remove('DOWN')
		possible_actions.remove('LEFT')
		break;
	case 7: possible_actions.remove('DOWN')
		break;
	case 8: possible_actions.remove('DOWN')
		possible_actions.remove('RIGHT')
		break;

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """
	blank = self.find_blank_square(state)
	new_state = list(state)
	
	switch (blank)	{
	case 0: if action == 'DOWN'
			temp = new_state[2]
			new_state[2] = new_state[0]
			new_state[0] = temp
		else
			temp = new_state[1]
			new_state[1] = new_state[0]
			new_state[0] = temp
			
		break;
	case 1: if action == 'LEFT'
			temp = new_state[0]
			new_state[0] = new_state[1]
			new_state[1] = temp
		else
			temp = new_state[3]
			new_state[3] = new_state[1]
			new_state[1] = temp
		break;
	case 2: if action == 'UP'
			temp = new_state[0]
			new_state[0] = new_state[2]
			new_state[2] = temp
		else
			temp = new_state[3]
			new_state[3] = new_state[2]
			new_state[2] = temp
		break;
	case 3: if action == 'UP'
			temp = new_state[1]
			new_state[1] = new_state[3]
			new_state[3] = temp
		else if action == 'LEFT'
			temp = new_state[2]
			new_state[2] = new_state[3]
			new_state[3] = temp
		else if action == 'RIGHT'
			temp = new_state[4]
			new_state[4] = new_state[3]
			new_state[3] = temp
		else
			temp = new_state[6]
			new_state[6] = new_state[3]
			new_state[3] = temp
		break;
	case 4: if action == 'LEFT'
			temp = new_state[3]
			new_state[3] = new_state[4]
			new_state[4] = temp
		else if action == 'RIGHT'
			temp = new_state[5]
			new_state[5] = new_state[4]
			new_state[4] = temp
		else
			temp = new_state[7]
			new_state[7] = new_state[4]
			new_state[4] = temp
		break;
	case 5: if action == 'LEFT'
			temp = new_state[4]
			new_state[4] = new_state[5]
			new_state[5] = temp
		else 
			temp = new_state[8]
			new_state[8] = new_state[5]
			new_state[5] = temp
		break;
	case 6: if action == 'UP'
			temp = new_state[3]
			new_state[3] = new_state[6]
			new_state[6] = temp
		else
			temp = new_state[7]
			new_state[7] = new_state[6]
			new_state[6] = temp
		break;
	case 7: if action == 'UP'
			temp = new_state[4]
			new_state[4] = new_state[7]
			new_state[7] = temp
		else if action == 'RIGHT'
			temp = new_state[8]
			new_state[8] = new_state[7]
			new_state[7] = temp
		else
			temp = new_state[6]
			new_state[6] = new_state[7]
			new_state[7] = temp
		break;
	case 8: if action == 'UP'
			temp = new_state[5]
			new_state[5] = new_state[8]
			new_state[8] = temp
		else
			temp = new_state[7]
			new_state[7] = new_state[8]
			new_state[8] = temp
		break
	}
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal


    def h(self, node):
       return sum(s != g for (s, g) in zip(node.state, self.goal))
       
'''


