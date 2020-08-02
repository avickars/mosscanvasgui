import random
import sys
import time
sys.path.insert(0, 'C:\\Users\\minh2\\aima-python')
from search import *

temp = EightPuzzle((1,2,3,4,5,6,7,8,0))
duckPuzzle = DuckPuzzle((1,2,3,4,5,6,7,8,0))

#Question 1
def make_rand_8puzzle():
    string = [0,1,2,3,4,5,6,7,8]
    solvable = bool(0) 
    while solvable == bool(0):
        random.shuffle(string)
        solvable = temp.check_solvability(string)
            
    return EightPuzzle(tuple(string))

def display(state):
    string = list(state)
    obj = EightPuzzle(string)
    blank_index = obj.find_blank_square(string)
    string[blank_index]='*'
    

    print (str(string[0])+" " + str(string[1]) +" " + str(string[2]) + "\n" 
          + str(string[3])+" " + str(string[4]) +" " + str(string[5])+ "\n" 
          + str(string[6])+" " + str(string[7]) +" " + str(string[8]))
    
    
#Question 2
def manhattanDistanceEightPuzzle(node):
		matrix = convertToMatrix(node.state)
		mhd = 0
		for i in range(3):
			for j in range(3):
				if matrix[i][j] != 0:
					x, y = divmod(matrix[i][j]-1, 3)
					mhd += abs(x - i) + abs(y - j)
		return mhd

def maxHeuristicEightPuzzle(node):
	x = manhattanDistanceEightPuzzle(node)
	y = temp.h(node)
	return max(x,y)

#Helper functions
def convertToMatrix(state):
    x=[]
    y=[]

    for i,item in enumerate(state):
        x.append(item)
        if (i+1)%3 == 0:

            y.append(x)
            x =[]
    return y

#Question 3
class DuckPuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        self.goal = goal
        Problem.__init__(self, initial, goal)
    
    def find_blank_square(self, state):
        return state.index(0)
    
    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']       
        index_blank_square = self.find_blank_square(state)
        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        if index_blank_square == 1:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        if index_blank_square == 2:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        if index_blank_square == 6:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')
        return possible_actions

    def result(self, state, action):
        index_blank_square = self.find_blank_square(state)
        new_state = list(state)
        if index_blank_square == 0:
            delta = {'DOWN':2, 'RIGHT':1}
        if index_blank_square == 1:
            delta = {'DOWN':2, 'LEFT':-1}
        if index_blank_square == 2 :
        	delta = {'UP':-2, 'RIGHT':1}
        if index_blank_square == 3:
            delta = {'DOWN':3, 'LEFT':-1, 'RIGHT':1, 'UP':-2}
        if index_blank_square == 4:
            delta = {'DOWN':3, 'LEFT':-1, 'RIGHT':1}
        if index_blank_square == 5:
            delta = {'DOWN':3, 'LEFT':-1}
        if index_blank_square == 6:
            delta = {'UP':-3, 'RIGHT':1}
        if index_blank_square == 7:
            delta = {'UP':-3, 'LEFT':-1, 'RIGHT':1}
        if index_blank_square == 8:
            delta = {'UP':-3, 'LEFT':-1}
      
        neighbor = index_blank_square + delta[action]
        new_state[index_blank_square], new_state[neighbor] = new_state[neighbor], new_state[index_blank_square]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal
    
    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))
    


def manhattanDistanceDuckPuzzle(node):
        state = node.state
        mhd = 0
        index_goal = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]}
        index = {0:[0,0], 1:[0,1], 2:[1,0], 3:[1,1], 4:[1,2], 5:[1,3], 6:[2,1], 7:[2,2], 8:[2,3]}
        
        for i in range(len(state)):
            row, col = index[i]
            goalRow, goalCol = index_goal[state[i]]
            mhd += abs(row - goalRow) + abs(col - goalCol) 
        
        return mhd


def maxHeuristicDuckPuzzle(node):
	x = manhattanDistanceDuckPuzzle(node)
	y = duckPuzzle.h(node)
	return max(x, y)
    

#Helper functions taken from search.py with some modification
def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    count_pop = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        count_pop = count_pop + 1
        if problem.goal_test(node.state):
            print("Length of the solution = "+ str(len(node.path())))
            print("Number of nodes that were removed from frontier = "+ str(count_pop))
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    print("NOT SOLVABLE")
    return None


def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def main():
    #question 1
    print("QUESTION 1:\n")
    state = make_rand_8puzzle()
    print("Initial Puzzle = " + str(state.initial)+ "\n")
    display(state.initial)
    print("------------------------------------")
    print()
    
    #question 2
    print("QUESTION 2:\n")
    for i in range(1):
        print("PUZZLE " + str(i+1) + ":")
        state = make_rand_8puzzle()
        print("Initial Puzzle = " + str(state.initial)+ "\n")

        print("EIGHT PUZZLE - MISPLACED TILE HEURISTIC")
        start = time.time()
        astar_search(state, state.h)
        finish = time.time() 
        print("Total run time: " + str(finish - start) + "s")
        print("------------------------------------")
        print()

        print("EIGHT PUZZLE - MANHATTAN DISTANCE")
        start = time.time()
        astar_search(state, manhattanDistanceEightPuzzle)
        finish = time.time() 
        print("Total run time: " + str(finish - start) + "s")
        print("------------------------------------")
        print()

        print("EIGHT PUZZLE - MAXIUM HEURISTIC")
        start = time.time()
        astar_search(state, maxHeuristicEightPuzzle)
        finish = time.time() 
        print("Total run time: " + str(finish - start) + "s")
        print("------------------------------------")
        print()
    
    #question 3
    print("QUESTION 3:\n")
    duckPuzzleArr = [
    list((1,2,3,0,8,5,4,7,6)),
    list((3,1,2,7,4,6,0,5,8)),
    list((0,1,3,2,7,4,5,8,6)), 
    list((3,1,2,8,4,6,0,7,5)),
    list((1,0,3,2,4,6,8,7,5)),
    list((0,1,3,2,4,6,8,7,5)),
    list((2,0,1,3,8,5,4,7,6)),
    list((1,2,3,8,6,5,7,4,0)),
    list((1,2,3,7,8,6,0,4,5)),
    list((0,1,3,2,8,6,7,4,5))]

    for i in range(10):
        print("PUZZLE " + str(i+1) + ":")
        duckPuzzTuple = tuple(duckPuzzleArr[i])
        duckPuzzle = DuckPuzzle(duckPuzzTuple)

        print("Initial Puzzle = " + str(duckPuzzle.initial)+ "\n")
        print("DuckPuzzle - MISPLACED TILE HEURISTIC")
        start = time.time()
        astar_search(duckPuzzle, duckPuzzle.h)
        finish = time.time() 
        print("Total run time: " + str(finish - start) + "s")
        print("------------------------------------")
        print()

        print("DuckPuzzle - MANHATTAN DISTANCE")
        start = time.time()
        astar_search(duckPuzzle, manhattanDistanceDuckPuzzle)
        finish = time.time() 
        print("Total run time: " + str(finish - start) + "s")
        print("------------------------------------")
        print()

        print("DuckPuzzle - MAXIUM HEURISTIC")
        start = time.time()
        astar_search(duckPuzzle, maxHeuristicDuckPuzzle)
        finish = time.time() 
        print("Total run time: " + str(finish - start) + "s")
        print("------------------------------------")
        print()

    
    
    
main()
    