# a1.py

from search import *
import time

# ...
# Sources:
# Bounced ideas off my brother Kris
# 
# Best-first graph search and A* search modified from textbook code
# 
# DuckPuzzle was written using EightPuzzle as a model
# 
# Manhattan lookup table inspired by chp 3 notes:
# https://www2.cs.sfu.ca/CourseCentral/310/tjd/chp3_search.html
# 
# Used this to generate random duck puzzle by shuffling goal state:
# https://stackoverflow.com/questions/4859292/how-to-get-a-random-value-from-dictionary-in-python
# 
# Helped with understanding solvability of EightPuzzle:
# https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
# 
# ...

# beginning of modifications to search.py
def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    
    # add global counter to keep track of nodes removed
    nodes_removed = 0

    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        nodes_removed += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                print(nodes_removed, "nodes have been removed from frontier")
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
                    nodes_removed += 1
    return None
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    start_time = time.time()
    solution = best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
    elapsed_time = time.time() - start_time
    print(elapsed_time, "seconds to find solution")
    # number of moves = length of solution path - 1 (root node doesn't account for a move)
    print(len(solution.path())-1, "moves to solution")
    return solution
# end of modifications to search.py

class DuckPuzzle(Problem):
  """ The problem of sliding tiles numbered from 1 to 8 on a duck-shaped board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square)
    Board looks like this:
    1 2 - -
    3 4 5 6
    - 7 8 * """
  def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    """ Define goal state and initialize a problem """
    self.initial = initial
    self.goal = goal

  def find_blank_square(self, state):
    """Return the index of the blank square in a given state"""

    return state.index(0)

  def actions(self, state):
    """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    index_blank_square = self.find_blank_square(state)

    if index_blank_square in (0,2,6):
        possible_actions.remove('LEFT')
    if index_blank_square in (0,1,4,5):
        possible_actions.remove('UP')
    if index_blank_square in (1,5,8):
        possible_actions.remove('RIGHT')
    if index_blank_square in (2,6,7,8):
        possible_actions.remove('DOWN')

    return possible_actions

  def result(self, state, action):
    """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

    # blank is the index of the blank square
    blank = self.find_blank_square(state)
    new_state = list(state)
    # three possibilites for deltas based on blank index
    if blank < 3:
      delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
    elif blank == 3:
      delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
    else:
      delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
    neighbor = blank + delta[action]
    new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

    return tuple(new_state)

  def goal_test(self, state):
    """ Given a state, return True if state is a goal state or False, otherwise """

    return state == self.goal

  def check_solvability(self, state):
    """ Solvability check from EightPuzzle doesn't work here """
    return None

  def h(self, node):
    """ Return the heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles """

    return sum(s != g for (s, g) in zip(node.state, self.goal))



# lookup table for Manhattan heuristic for EightPuzzle
# nine/zero tile listed first for easy indexing
manhattan = ((4, 3, 2, 3, 2, 1, 2, 1, 0), \
             (0, 1, 2, 1, 2, 3, 2, 3, 4), \
             (1, 0, 1, 2, 1, 2, 3, 2, 3), \
             (2, 1, 0, 3, 2, 1, 4, 3, 2), \
             (1, 2, 3, 0, 1, 2, 1, 2, 3), \
             (2, 1, 2, 1, 0, 1, 2, 1, 2), \
             (3, 2, 1, 2, 1, 0, 3, 2, 1), \
             (2, 3, 4, 1, 2, 3, 0, 1, 2), \
             (3, 2, 3, 2, 1, 2, 1, 0, 1))
# lookup table for Manhattan heuristic for DuckPuzzle
duckhattan = ((5, 4, 4, 3, 2, 1, 2, 1, 0), \
              (0, 1, 1, 2, 3, 4, 3, 4, 5), \
              (1, 0, 2, 1, 2, 3, 2, 3, 4), \
              (1, 2, 0, 1, 2, 3, 2, 3, 4), \
              (2, 1, 1, 0, 1, 2, 1, 2, 3), \
              (3, 2, 2, 1, 0, 1, 2, 1, 2), \
              (4, 3, 3, 2, 1, 0, 3, 2, 1), \
              (3, 2, 2, 1, 2, 3, 0, 1, 2), \
              (4, 3, 3, 2, 1, 2, 1, 0, 1))

def make_rand_8puzzle(t):
  temp = [1, 2, 3, 4, 5, 6, 7, 8, 0]
  
  for i in range(9):
    r_index = random.randint(0,8)
    temp[i], temp[r_index] = temp[r_index], temp[i]
  random_state = tuple(temp)

  puzzle = t(random_state)
  if puzzle.check_solvability(random_state):
    # print("solvable puzzle generated")
    return puzzle
  else:
    # print("puzzle not solvable, re-generating...")
    return make_rand_8puzzle(t)

def make_rand_duckpuzzle():
  # start off with solved state
  temp = DuckPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0))
  current_state = temp.initial
  # shuffle the board by doing random legal moves 100000 times
  for i in range(100000):
    possible_actions = temp.actions(current_state)
    current_state = temp.result(current_state, random.choice(possible_actions))
  temp.check_solvability(current_state)
  return DuckPuzzle(current_state)

def display(state):
  for i in range(9):
    if state[i] == 0:
      print("*", end=" ")
    else:
      print(state[i], end=" ")

    if i % 3 == 2:
      print(" ")

def display_duck(state):
  for i in range(9):
    if i == 6:
      print(" ", end=" ")
    if state[i] == 0:
      print("*", end=" ")
    else:
      print(state[i], end=" ")

    if i in (1,5,8):
      print(" ")

def h_manhattan(node):
  sum = 0
  # for each position in the current state, look at the tile and then get its distance from home
  for i in range(9):
    sum += manhattan[node.state[i]][i]
  return sum

def h_duckhattan(node):
  sum = 0
  for i in range(9):
    sum += duckhattan[node.state[i]][i]
  return sum

# puzzle = make_rand_8puzzle()
# display(puzzle.initial)
# display(astar_search(puzzle, display=True).state)

# ...
print("Generating 10 EightPuzzles")
puzzles = []
for i in range(10):
  puzzles.append(make_rand_8puzzle(EightPuzzle))
  print("Puzzle", i+1)
  display(puzzles[i].initial)

# ...
print("Testing misplaced tiles heuristic")
for i in range(10):
  print("Searching puzzle", i+1)
  astar_search(puzzles[i], display=True)

# ...
print("Testing Manhattan heuristic")
for i in range(10):
  print("Searching puzzle", i+1)
  astar_search(puzzles[i], h=h_manhattan, display=True)

# ...
print("Testing max of either heuristic")
for i in range(10):
  print("Searching puzzle", i+1)
  astar_search(puzzles[i], h=lambda n: max(puzzles[i].h(n),h_manhattan(n)), display=True)


#...
print(" ")
print("Generating 10 DuckPuzzles")
puzzles = []
for i in range(10):
  puzzles.append(make_rand_duckpuzzle())
  print("Puzzle", i+1)
  display_duck(puzzles[i].initial)

# ...
print("Testing misplaced tiles heuristic")
for i in range(10):
  print("Searching puzzle", i+1)
  astar_search(puzzles[i], display=True)

# ...
print("Testing Manhattan heuristic")
for i in range(10):
  print("Searching puzzle", i+1)
  astar_search(puzzles[i], h=h_duckhattan, display=True)

# ...
print("Testing max of either heuristic")
for i in range(10):
  print("Searching puzzle", i+1)
  astar_search(puzzles[i], h=lambda n: max(puzzles[i].h(n),h_duckhattan(n)), display=True)