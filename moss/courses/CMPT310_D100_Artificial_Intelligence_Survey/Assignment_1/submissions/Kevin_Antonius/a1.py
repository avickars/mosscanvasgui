from search import *
import numpy as np
import time

#Notes, I was mistakenly working with Jupyter-notebook instead of python file. 
#Tried to converted it to a1.py. might have some dependencies issues. 

#Write a function called make_rand_8puzzle() that returns a new instance of an EightPuzzle problem with 
#a random initial state that is solvable. Note that EightPuzzle has a method called check_solvability 
#that you should use to help ensure your initial state is solvable.
def make_rand_8puzzle():
    #refer to TA Tutorial
    solveable = False
    while(not solveable):
        state = tuple(np.random.permutation(9))
        board = EightPuzzle(initial=state)
        solveable = board.check_solvability(state)
    return board 

def display(state):
    for i in range(0,9,1):
        if(state[i] == 0):
            #refer to :https://careerkarma.com/blog/python-print-without-new-line/
            print("* ", end='')
        else:
            print(state[i], "", end='')
        if((i+1)%3 == 0):
            print()

def manhattanHeuristic(node):
    inputState = node.state
    goalState = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    currentState = {}
    indices = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    for i in range(len(inputState)):
        currentState[inputState[i]] = indices[i]
    mDistance = 0
    for i in range(1, 9):
        for j in range(2):
            mDistance = abs(goalState[i][j] - currentState[i][j]) + mDistance
    return mDistance

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search1(problem, lambda n: n.path_cost + h(n), display)

def best_first_graph_search1(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    global nodeRemoved
    nodeRemoved = 0
    while frontier:
        node = frontier.pop()
        # calculating the total number of nodes that were removed from frontier
        nodeRemoved = nodeRemoved + 1
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

for test in range(10):
    # variable for point # 3
    global nodeRemoved
    print("This is result number: ", test)
    #Creating Differnt State each iteration
    state = tuple(np.random.permutation(9))
    puzzle = EightPuzzle(initial=state)
    
    #Crated Same puzzle for testing
    display(puzzle.initial)
    
    
    #Misplaced tile heuristic
    misplace_start_time = time.time()
    solution = astar_search(example, example.h).solution()
    misplace_time_taken = time.time() - misplace_start_time 
    print("Misplace tile Result:")
    print("Time Taken: ",misplace_time_taken)
    print("Lengh of Solution :", len(solution))
    print("Total number of nodes removed ", nodeRemoved)
    
    #----------- Manhattan Heuristic
    manhattan_start_time = time.time()
    solution = astar_search(example, manhattanHeuristic).solution()
    manhattan_time_taken = time.time() - misplace_start_time 
    print("Misplace tile Result:")
    print("Time Taken: ",manhattan_time_taken)
    print("Lengh of Solution :", len(solution))
    print("Total number of nodes removed ", nodeRemoved)
    
    