#name = bob (jia bao) lu
#student number = 301260391



import random
import time
from search import *

# Q1
def make_rand_8puzzle():
    puzzle = EightPuzzle(Problem)
    # state = list(np.arange(9))
    # np.random.shuffle(state)

    state = []
    for i in range(9):
        state.append(i)

    random.shuffle(state)

    while puzzle.check_solvability(tuple(state)) != 1:
        # np.random.shuffle(state)
        random.shuffle(state)
        # print(state)

    puzzle.__init__(tuple(state))
    # puzzle.__init__(tuple(list(state)))
    return puzzle

#not yet done display in shapes of ex.
#1,2,3
#4,5,6
#7,8,0
def display(state):
    state = tuple(state)
    stateMap = ['*','1','2','3','4','5','6','7','8']
    print(stateMap[state[0]]+stateMap[state[1]]+stateMap[state[2]])
    print(stateMap[state[3]]+stateMap[state[4]]+stateMap[state[5]])
    print(stateMap[state[6]]+stateMap[state[7]]+stateMap[state[8]])

#   for i in range(len(state)):
#       if state[i] == 0:
#           state[i] = '*'
#       else:
#           state[i] == str(state[i])

#   print(np.reshape(np.array(state), (3, 3)))

#   return mat

# Q2
# A* search and breadth first search are borrowed from 'search.py' functions in the textbook code 
def astar_search(problem, h=None):
  h = memoize(h or problem.h, 'h')
  return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

def best_first_graph_search(problem, f):
  f = memoize(f, 'f')
  node = Node(problem.initial)
  frontier = PriorityQueue('min', f)
  frontier.append(node)
  explored = set()
  count = 0
  while frontier:
      node = frontier.pop()
      count = count + 1
      if problem.goal_test(node.state):
          print("the length of the solution: ", node.path_cost)
          print("the total number of nodes that were removed from frontier: ", count)
          return node
      explored.add(node.state)
      for child in node.expand(problem):
          if child.state not in explored and child not in frontier:
              frontier.append(child)
          elif child in frontier:
              if f(child) < frontier[child]:
                  del frontier[child]
                  frontier.append(child)
  return print("the length of the solution: ", node.path_cost,"\n","the total number of nodes that were removed from frontier: ", count)

# define Manhattan heuristic for 8-puzzle
def manhattan_h(node):
    state = tuple(node.state)
    r_goal=[2,0,0,0,1,1,1,2,2]
    c_goal=[2,0,1,2,0,1,2,0,1]
    r_index=[]
    c_index=[]

    for i in range(9):
        index = state.index(i)
        r_index.append(int(index/3))
        c_index.append(index%3)

    manhattan_dist = 0
    for i in range(9):
        manhattan_dist = manhattan_dist+abs(r_index[i]-r_goal[i])+abs(c_index[i]-c_goal[i])

    # state = np.reshape(list(node.state), (3,3))
    # goal = [[2,2], [0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1]]
    # coordinates=[]
    # for i in range(9):
    #   coordinates.append([np.where(state == i)[0][0], np.where(state == i)[1][0]])
    # manhattan_dist = np.sum(np.absolute(np.subtract(np.array(coordinates), np.array(goal))))

    # print(manhattan_dist)
    return manhattan_dist

# define Max heuristic for 8-puzzle
def max_h(node):
    manhattan_dist = manhattan_h(node)
    misplaced_tiles = 0
    state = tuple(node.state)
    
    if state[-1] != 0:
        misplaced_tiles = misplaced_tiles + 1
    for i in range(8):
        if state[i] != i+1:
            misplaced_tiles = misplaced_tiles + 1

    max_value = max(manhattan_dist, misplaced_tiles)
    return max_value

def solving_8puzzle():
    eight_puzzle = make_rand_8puzzle()
    display(eight_puzzle.initial)
    
    # A*-search using the misplaced tile heuristic
    print("Solving 8-puzzle using the misplaced tile heuristic:")
    start_time = time.time()
    astar_search(eight_puzzle, eight_puzzle.h)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print()

    # A*-search using the Manhattan distance heuristic
    print("Solving 8-puzzle using the Manhattan distance heuristic:")
    start_time = time.time()
    astar_search(eight_puzzle, manhattan_h)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print()

    # A*-search using the Max heuristic
    print("Solving 8-puzzle using the max heuristic:")
    start_time = time.time()
    astar_search(eight_puzzle, max_h)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print()

# Q3
# the duck puzzle class
class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        self.goal = goal
        Problem.__init__(self, initial, goal)
    
    def find_blank_square(self, state):
        return state.index(0)
    
    def actions(self, state):
        # possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'UP^', 'DOWN^']
        final_possible_actions = []       
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            final_possible_actions = ['RIGHT', 'DOWN^']
        if index_blank_square == 1:
            final_possible_actions = ['LEFT', 'DOWN^']
        if index_blank_square == 2:
            final_possible_actions = ['UP^', 'RIGHT']
        if index_blank_square == 3:
            final_possible_actions = ['LEFT', 'RIGHT', 'DOWN', 'UP^']
        if index_blank_square == 4:
            final_possible_actions = ['LEFT', 'RIGHT', 'DOWN']
        if index_blank_square == 5:
            final_possible_actions = ['LEFT', 'DOWN']
        if index_blank_square == 6:
            final_possible_actions = ['UP', 'RIGHT']
        if index_blank_square == 7:
            final_possible_actions = ['UP','LEFT','RIGHT']
        if index_blank_square == 8:        
            final_possible_actions = ['LEFT', 'UP']

        return final_possible_actions

    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1, 'UP^':-2, 'DOWN^':2}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)
    
    def goal_test(self, state):
        return state == self.goal
    

        #not yet solvability for duck puzzle
        #note: make ordered list and action random time to make solvable puzzle

    def check_solvability(self, state):
        puzzle = DuckPuzzle(Problem)
        x = 50 # random.randint(1, 10)
        # i=0
        state = tuple(state)
        for i in range(x):
            ac = puzzle.actions(state)
            y = random.randint(0, len(ac) - 1)
            act = ac[y]
            new_state = puzzle.result(state, act)
            state = new_state
        return state
    
    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

def make_rand_duckPuzzle():
    puzzle = DuckPuzzle(Problem)
    state = (1,2,3,4,5,6,7,8,0)
    state = puzzle.check_solvability(state)
    puzzle.__init__(tuple(state))
    return puzzle
        
    
def display_duck(state):
    state = tuple(state)
    stateMap = ['*','1','2','3','4','5','6','7','8']
    print(stateMap[state[0]]+stateMap[state[1]]+' '+' ')
    print(stateMap[state[2]]+stateMap[state[3]]+stateMap[state[4]]+stateMap[state[5]])
    print(' '+stateMap[state[6]]+stateMap[state[7]]+stateMap[state[8]])

# define Manhattan heuristic for duck-puzzle
def manhattan_h_duck(node):
    state = tuple(node.state)
    r_goal=[2,0,0,1,1,1,1,2,2]
    c_goal=[3,0,1,0,1,2,3,1,2]
    r_index=[]
    c_index=[]
    for i in range(9):
        index = state.index(i)
        if index < 2:
            r_index.append(0)
            c_index.append(index)
        elif index < 6:
            r_index.append(1)
            c_index.append(index-2)
        else:
            r_index.append(2)
            c_index.append(index-5)     
    # print(r_index)
    # print(c_index)
    manhattan_dist = 0
    for i in range(9):
        manhattan_dist = manhattan_dist+abs(r_index[i]-r_goal[i])+abs(c_index[i]-c_goal[i])
    return manhattan_dist

# define Max heuristic for duck-puzzle
def max_h_duck(node):
    manhattan_dist = manhattan_h_duck(node)
    misplaced_tiles = 0
    state = tuple(node.state)

    if state[-1] != 0:
        misplaced_tiles = misplaced_tiles + 1
    for i in range(8):
        if state[i] != i+1:
            misplaced_tiles = misplaced_tiles + 1

    max_value = max(manhattan_dist, misplaced_tiles)
    return max_value

def solving_duckPuzzle():
    # duck = DuckPuzzle(Problem)
    duck_puzzle = make_rand_duckPuzzle()
    display_duck(duck_puzzle.initial)

    # A*-search using the misplaced tile heuristic
    print("Solving duck-puzzle using the misplaced tile heuristic:")
    start_time = time.time()
    astar_search(duck_puzzle, duck_puzzle.h)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print()

    # A*-search using the Manhattan distance heuristic
    print("Solving duck-puzzle using the Manhattan distance heuristic:")
    start_time = time.time()
    astar_search(duck_puzzle, manhattan_h_duck)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print()

    # A*-search using the Max heuristic
    print("Solving duck-puzzle using the max heuristic:")
    start_time = time.time()
    astar_search(duck_puzzle, max_h_duck)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print()

def main():
    #for i in range(9):
        solving_8puzzle()
        solving_duckPuzzle()

if __name__== "__main__":
    main()

