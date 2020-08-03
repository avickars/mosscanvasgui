# a1.py

from search import *
import random
import time
from itertools import permutations


class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)):
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
        if (index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6):
            possible_actions.remove('LEFT')
        if (index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5):
            possible_actions.remove('UP')
        if (index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8):
            possible_actions.remove('RIGHT')
        if (index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8):
            possible_actions.remove('DOWN')
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if (blank == 0 or blank == 1):
            delta['DOWN'] = 2
        if (blank == 3 or blank == 4 or blank == 5):
            delta['DOWN'] = 3
        if (blank == 2 or blank == 3):
            delta['UP'] = -2
        if (blank == 6 or blank == 7 or blank == 8):
            delta['UP'] = -3
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        return sum(s != g for (s, g) in zip(node.state, self.goal))

def make_rand_8puzzle():
    check = False
    while check != True:
        generate_puzzle = tuple(random.sample(range(0, 9), 9))
        rand = EightPuzzle(initial=generate_puzzle)
        check = rand.check_solvability(state=generate_puzzle)
        if check:
            display (generate_puzzle)
        else:
            print ("")
    return rand

def display(state):
    for i in range(0, 9):
        if (i % 3 == 0):
            print("")
        #Print * instead of 0
        if (state[i] == 0):
            print("*", end = " ")  
        elif (state[i] != 0):
            print(state[i], end = " ")

def make_rand_duckpuzzle():
    z = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    rand = list(z)
    puzzle_generate = DuckPuzzle(z)
    span = random.randint(1, 1000)
    for x in range(span):
        possibilities = puzzle_generate.actions(rand)
        move_tile = random.choice(possibilities)
        rand = puzzle_generate.result(rand, move_tile)
    return rand
    
def displayDuckPuzzle(state):
    state = list(state)
    for i in range(0, 9):
        if (state[i] == 0):
            state[i] = "*"
    print(state[0], state[1])
    print(state[2], state[3], state[4], state[5])
    print(" ", state[6], state[7], state[8])
            
def new_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return new_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def new_best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    count = 0
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        count += 1
        if problem.goal_test(node.state): 
            # node.count=count
            return node,count
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def EightPuzzle_manhattan(node):
    state=node.state
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    sum = 0
    coordinates = {0:(0,0), 1:(1,0), 2:(2,0), 3:(0,1), 4:(1,1), 5:(2,1), 6:(0,2), 7:(1,2), 8:(2,2)}
    for i in state:
        if i == 0:
            sum += 0
        else:
            temp_index = goal.index(i)
            initial_index = state.index(i)
            x1, y1 = coordinates[temp_index]
            x2, y2 = coordinates[initial_index]
            sum += (abs(x1 - x2) + abs(y1 - y2))
    return sum  

def DuckPuzzle_manhattan(node):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    sum = 0
    coordinates = {0:(0,0), 1:(1,0), 2:(2,0), 3:(0,1), 4:(1,1), 5:(2,1), 6:(0,2), 7:(1,2), 8:(2,2)}
    for i in node.state:
        if i == 0:
            sum += 0
        else:
            temp_index = goal.index(i)
            initial_index = node.state.index(i)
            x1, y1 = coordinates[temp_index]
            x2, y2 = coordinates[initial_index]
            sum += (abs(x1 - x2) + abs(y1 - y2))
    return sum  

    #For the Maximum of the misplaced tile heuristic and the Manhattan distance heuristic
def max_eight_puzzle(node):
    temp1obj = EightPuzzle(initial=node.state)
    length1 = EightPuzzle_manhattan(node)
    new1 = temp1obj.h(node)
    return max(length1, new1)

    #For the Maximum of the misplaced tile duck-puzzle and the Manhattan distance duck-puzzle
def max_duck_puzzle(node):
    temp2obj = DuckPuzzle(initial=node.state)
    length2 = DuckPuzzle_manhattan(node)
    new2 = temp2obj.h(node)
    return max(length2, new2)

def EightPuzzle_heuristics():
    temp = make_rand_8puzzle()
    new_node = Node(temp.initial)
    object_=EightPuzzle(temp)
    print("")
    print("")
    #For the Misplaced Tile Heuristic 
    print("MISPLACED TILE HEURISTIC")
    start = time.time()
    solution_path, node_removed = new_astar_search(temp, temp.h)
    print("The total running time in seconds:", time.time()-start)
    print("The length of the solution: ", len(solution_path.solution()))
    print("The total number of nodes removed from frontier: ", node_removed)
    print("-------------------------------------------------------")
    print("\n")
    #For the Manhattan Distance Heuristic 
    print("MANHATTAN DISTANCE HEURISTIC")
    start = time.time()
    solution_path, node_removed = new_astar_search(temp, EightPuzzle_manhattan)
    print("The total running time in seconds: ", time.time()-start)
    print("The length of the solution: ", len(solution_path.solution()))
    print("The total number of nodes removed from frontier: ", node_removed)
    print("-------------------------------------------------------")
    print("\n")
    #For the Max of Misplaced and Manhattan Distance Heuristic
    print("MAX OF MISPLACED AND MANHATTAN DISTANCE HEURISTIC")
    start = time.time()
    solution_path, node_removed = new_astar_search(temp, max_eight_puzzle)
    print("The total running time in seconds: ", time.time()-start)
    print("The length of the solution: ", len(solution_path.solution()))
    print("The total number of nodes removed from frontier: ", node_removed)
    print("-------------------------------------------------------")
    print("\n")
    
def DuckPuzzle_heuristics():
    temp1 = make_rand_duckpuzzle()
    temp = DuckPuzzle(initial=temp1)
    new_node = Node(temp.initial)
    print(displayDuckPuzzle(state=temp1))
    print("")
    print("")
    #For the Misplaced Tile Duck-Puzzle
    print("MISPLACED TILE DUCK-PUZZLE")
    start = time.time()
    solution_path, node_removed = new_astar_search(temp, temp.h)
    print("The total running time in seconds: ", time.time()-start)
    print("The length of the solution: ", len(solution_path.solution()))
    print("The total number of nodes removed from frontier: ", node_removed)
    print("-------------------------------------------------------")
    print("\n")
    #For the Manhattan Distance Duck-Puzzle
    print("MANHATTAN DUCK-PUZZLE")
    start = time.time()
    solution_path,node_removed = new_astar_search(temp, DuckPuzzle_manhattan)
    print("The total running time in seconds: ", time.time()-start)
    print("The length of the solution: ", len(solution_path.solution()))
    print("The total number of nodes removed from frontier: ", node_removed)
    print("-------------------------------------------------------")
    print("\n")
    #For the Max of Misplaced and Manhattan Distance
    print("MAX OF MISPLACED AND MANHATTAN DUCK-PUZZLE")
    start = time.time()
    solution_path,node_removed = new_astar_search(temp, max_duck_puzzle)
    print("The total running time in seconds: ", time.time()-start)
    print("The length of the solution: ", len(solution_path.solution()))
    print("The total number of nodes removed from frontier: ", node_removed)
    print("-------------------------------------------------------")
    print("\n")
   



if __name__ == '__main__':
    
    print ("Random solvable puzzle generated:")
    
    print("-------EIGHT PUZZLE------")

    for i in range(1, 11):
        print("---------", i ,"------------")
        EightPuzzle_heuristics()
    
    print("-------DUCK PUZZLE------")

    for i in range(1, 11):
        print("---------", i ,"------------")
        DuckPuzzle_heuristics()
        
        


