# a1.py

from search import *

# This file contains code answers to CMPT 310 Assignment 1

# NOTE: this code assumes all 8-Puzzle Goal states are (1,2,3,4,5,6,7,8,0),
#   otherwise, EightPuzzle.check_solvability() may not work

import random
from datetime import datetime
import math
import time

PUZZLE_TYPE = 8 # assumes only NxN-1 types
MIN_ITERATION = 10
MAX_ITERATION = 15
NODES_REMOVED = 0
random.seed(datetime.now())



## QUESTION 1 ## -------------------------------------------

# returns opposite Puzzle action
# assumes action parameter is part of the known Actions
def opposite_action(action):
  actionArr = [['UP', 'DOWN'], ['LEFT', 'RIGHT']]
  for pair in actionArr:
    if action in pair:
      pair.remove(action)
      return pair[0]

# create solved instance
def generate_goal_state(size):
  puzzle8 = []
  for i in range(1,size+1):
    puzzle8.append(i)
  puzzle8.append(0)
  return tuple(puzzle8)

# returns new goal instance of an EightPuzzle or DuckPuzzle problem
# assume all new states must be different from goal state
# takes as parameter type_of_puzzle, which can be 'duck' or 'puzzle8'
# This algorithm guarantees to create solvable puzzles, assuming
# all functions were implemented correctly in the Puzzle class, because
# this function simply starts from a solved state, makes legal moves,
# then stops. Because of this, we can solve the puzzle by simply undoing all
# the moves this function performed, and we would the goal state
def make_rand_puzzle(type_of_puzzle):
  puzzle = []
  puzzle = generate_goal_state(PUZZLE_TYPE)
  puzzle_goal = puzzle
  if type_of_puzzle == "puzzle8":
    puzzle_helper = EightPuzzle_mod(puzzle, puzzle_goal)
  elif type_of_puzzle == "duck":
    puzzle_helper = DuckPuzzle(puzzle, puzzle_goal)
  else:
    print("ERROR")
  nIter = random.randint(MIN_ITERATION, MAX_ITERATION)

  n = 0
  previous_action = []
  while n < nIter:
    possible_actions = puzzle_helper.actions(puzzle)
    if previous_action != []:
      # not allowing actions to be undone increases randomness
      possible_actions.remove(opposite_action(previous_action))
    chosen_action = random.choice(possible_actions)
    puzzle = puzzle_helper.result(puzzle, chosen_action)
    previous_action = chosen_action
    n = n + 1
  
  # in case of randomness failure (which is unlikely), guarantee a non-goal solution
  if puzzle == puzzle_goal:
    if len(puzzle_goal) >= 2:
      temp = puzzle[len(puzzle)-2]
      puzzle[len(puzzle)-2] = puzzle[len(puzzle)-1]
      puzzle[len(puzzle)-1] = temp

  if type_of_puzzle == "puzzle8":
    return EightPuzzle_mod(puzzle, puzzle_goal)
  elif type_of_puzzle == "duck":
    return DuckPuzzle(puzzle, puzzle_goal)


# neatly print n-puzzle
# assumes all puzzle types are NxN
def display(state):
  puzzle_size = PUZZLE_TYPE+1
  side_len = int(math.sqrt(puzzle_size))
  for i in range(0, puzzle_size):
    char = state[i]
    if char == 0:
      print('*', end='')
    else:
      print(char, end='')
    if i % side_len == side_len-1:
      print("")
    else:
      print(" ", end='')





## QUESTION 2 ## -------------------------------------------

# The EightPuzzle class was modified due to a limitation:
# Limitation: heuristic functions here all assume the Goal state is (1,2,3,4,5,6,7,8,0)
#   because it only takes a Node as input, and cannot know the Goal inside EightPuzzle.
#   To assume other Goal state, the function needs to be placed inside the EightPuzzle,
#   but that may cause issues where two classes are defined with the same name,
#   so the class will be renamed to a modified version
class EightPuzzle_mod(Problem):
  """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
  squares is a blank. A state is represented as a tuple of length 9, where  element at
  index i represents the tile number  at index i (0 if it's an empty square) """

  def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    """ Define goal state and initialize a problem """
    super().__init__(initial, goal)    
    self.squareSideLen = 3
    # this matrix will treat Goal tile value as an index, and store the index
    # of the tile as the value
    # Example: in (1,4,6,2,3,4,7,8,0), we have tile Value 4 at Index 1,
    #   so self.matrix will store at index 4, value 1
    self.matrix = [] 
    self.generate_manhattan_matrix()

  # Generates a pre computed Matrix like array for the Goal state
  # this is used to speed up calculations, by storing index of Goal value
  def generate_manhattan_matrix(self):
    k = 0
    for i in range(0, len(self.goal)):
      self.matrix.append(-1) #dummy array of same size as Goal
    while k < len(self.matrix):
      goalValue = self.goal[k]
      self.matrix[goalValue] = k
      k = k + 1

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

  # Heuristic function that returns total number of misplaced tiles
  # Note: this Heuristic function is modified from the original EightPuzzle,
  #   because the original Heuristic considered tile '0', and counted it
  #   as a mispalced tile. Doing this, in example (1,2,3,4,5,6,7,0,8)
  #   we have a misplaced count of 1 tile (tile '8') and it takes 1 move
  #   to complete the puzzle. But, using the default Misplaced heuristic
  #   function EightPuzzle.h(Node), we get a misplaced count of 2, instead of 1.
  #   To fix this, we disregard comparisons with tile '0' for current state only,
  #   but we do not disregard the tile '0' in the Goal state, because it is a valid
  #   position, which the current state must match
  #   (This error was pointed out by a TA during the lecture)
  def h(self, node):
    return sum(s != g and (s != 0) for (s, g) in zip(node.state, self.goal))

  # Assumes it is a NxN 8-puzzle
  # Proof that x2-x1 and y2-y1 result in manhattan distance between tiles A and B, for DuckPuzzle:
  # We can only travel horizontally and vertically, and not diagonally.
  # Because of this, the shortest path between tiles A and B will be a set S
  # of Horizontal and Vertical movements. In any case, we will have to move some h Horizontal tiles
  # and some v Vertical tiles. The question is, now that we have a non NxN square puzzle with
  # missing pieces, can we reach node A to B in the DuckPuzzle, by only Horizontal and Vertical moves
  # without going a longer path due to missing tiles?
  # Well, we can see that on any row and on any column, all the tiles in that row or column
  # are not divided by any missing tiles. For example, there is no case where we start on a row (or column),
  # continue on that row, then hit a tile that does not exist, but the row continues after the missing tile, and we need to navigate around the missing tile (for example, we can see the DuckPuzzle has 2 missing tiles in
  # its top-right and one in the bottom-left corner, but notice that there are no non-existing tiles dividing some row or column, and we can navigate the whole row or column from start to end, without hitting a missing tile)
  # becasue of this, the logic stands as follows:
  # We start at some node A, then to get closer to B, we move either Horizotal or
  # Vertical (whichever is valid). Because there are no missing tiles within a row or column, we are able
  # to make a valid move without being blocked, because there are no missing tiles. (We basically can navigate the same row from start to end, without having to switch rows to avoid a missing tile, so essentially there is no missing tile that we would have to walk around in our the shortest path).
  # Doing that, we have decreased the number of movements we had in S, and are now closer to the node B.
  # So, as there are no missing tiles dividing a row, we essentially have all tiles we need to go from A to B,
  # on a shortest path. (The logic is similar for EightPuzzle)
  #
  # Another way of arguing that the missing tiles in the corners of the DuckPuzzle is to notice that
  # no matter which tile A and B we choose, we can always form a rectagle where A and B are the corners, and
  # notice that this rectangle will have its corners connected, without some path being
  # restricted to go backwards (ie on each move within the Rectangle, were getting closed to the other corner)
  def heuristic_manhattan_distance(self, node):
    manhattan_sum = 0
    index = 0
    for i in node.state:
      if i == 0: # including 0 causes heuristic to be not admissible
        index = index + 1
        continue
      indexModX = index % self.squareSideLen
      indexGoalModX = self.matrix[i] % self.squareSideLen
      x = abs(indexModX-indexGoalModX)
      indexModY = index // self.squareSideLen # row
      indexGoalModY = self.matrix[i] // self.squareSideLen
      y = abs(indexModY-indexGoalModY)
      manhattan_sum = manhattan_sum + (x+y)
      index = index + 1
    return manhattan_sum
  
  # For question 2, returns MAX of the two heuristics
  def max_misplaced_manhattan(self, node):
    return max(self.heuristic_manhattan_distance(node), self.h(node))

def increment_nodes_removed():
  global NODES_REMOVED
  NODES_REMOVED = NODES_REMOVED + 1
  return

# the following code was not modified from original
# (it was simply added to overwrite the functions used in search.py,
#    so that functions for Question 2 can be used using "from a1 import *")
def astar_search_mod(problem, h=None, display=False):
  """A* search is best-first graph search with f(n) = g(n)+h(n).
  You need to specify the h function when you call astar_search, or
  else in your Problem subclass."""
  h = memoize(h or problem.h, 'h')
  return best_first_graph_search_mod(problem, lambda n: n.path_cost + h(n), display)

# the following function has been modified from the original aima-python code
# to display the number of Nodes removed from Frontier
def best_first_graph_search_mod(problem, f, display=False):
  """Search the nodes with the lowest f scores first.
  You specify the function f(node) that you want to minimize; for example,
  if f is a heuristic estimate to the goal, then we have greedy best
  first search; if f is node.depth then we have breadth-first search.
  There is a subtlety: the line "f = memoize(f, 'f')" means that the f
  values will be cached on the nodes as they are computed. So after doing
  a best first search you can examine the f values of the path returned."""
  global NODES_REMOVED
  NODES_REMOVED = 0
  f = memoize(f, 'f')
  node = Node(problem.initial)
  frontier = PriorityQueue('min', f)
  frontier.append(node)
  explored = set()
  while frontier:
    node = frontier.pop()
    increment_nodes_removed()
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
          increment_nodes_removed()
          frontier.append(child)
  return None
  

# runs the A* Search algorithm and prints the necessary data
# for Quetion 2 in the assignment, for a given puzzle,
# and prints the total run time, length of solution, and nodes removed from frontier,
# based on each of the 3 heuristic functions in Question 2
def print_question_2_3_data(print_type):
  # Heuristic based on number of misplaced tiles
  for i in range(0, 10):
    puzzle8 = make_rand_puzzle(print_type)
    print("\n*** Solving puzzle: ", puzzle8.initial)
    for j in range(0, 1): #better to average, use higher number
      print("\nPuzzle", i, "Attempt", j)
      start_time = time.time()
      astar_search_mod(puzzle8, puzzle8.h)
      elapsed_time = time.time() - start_time
      print("Elapsed_time time: ", elapsed_time)
      print("Nodes removed from 'Misplaced Tile Heuristic' frontier: {}".format(NODES_REMOVED))
      
      start_time = time.time()
      astar_search_mod(puzzle8, puzzle8.heuristic_manhattan_distance)
      elapsed_time = time.time() - start_time
      print("Elapsed_time time: ", elapsed_time)
      print("Nodes removed from 'Manhattan' frontier: {}".format(NODES_REMOVED))
      
      start_time = time.time()
      astar_search_mod(puzzle8, puzzle8.max_misplaced_manhattan)
      elapsed_time = time.time() - start_time
      print("Elapsed_time time: ", elapsed_time)
      print("Nodes removed from 'Max' frontier: {}".format(NODES_REMOVED))



## QUESTION 3 ## ----------------------------------------------------------------

# This class is based on Problem, but has a lot of functions from EightPuzzle_mod,
# so it made sense to multilevel inherit EightPuzzle_mod, to reduce code duplication
class DuckPuzzle(EightPuzzle_mod):
  def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    super().__init__(initial, goal)    
    self.squareSideLen = 4
    
  # Accounts for Square State having -1, and adapts the index by translating it
  def translate_to_duck_index(self, indexOrig):
    indexSquare = indexOrig
    if indexOrig > 1:
      indexSquare = indexSquare + 2
    if indexOrig > 5:
      indexSquare = indexSquare + 1
    return indexSquare
  
  # reverse of translate_to_duck_index()
  def translate_from_duck_index(self, indexSquare):
    indexOrig = indexSquare
    if indexSquare > 1:
      indexOrig = indexOrig - 2
    if indexOrig > 5:
      indexOrig = indexOrig - 1
    return indexOrig

  
  def find_blank_square(self, state):
    """Return the index of the blank square in a given state"""
    return state.index(0)

  def actions(self, state):
    """ Return the actions that can be executed in the given state.
    The result would be a list, since there are only four possible actions
    in any given state of the environment """

    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    index_blank_square = self.find_blank_square(state)
    index_duck = self.translate_to_duck_index(index_blank_square)
    
    # remove all moves that cannot be completed
    if index_duck % self.squareSideLen == 0 or index_duck == 9:
      possible_actions.remove('LEFT')
    if index_duck <= 1 or index_duck == 6 or index_duck == 7:
      possible_actions.remove('UP')
    if index_duck % self.squareSideLen == 3 or index_duck == 1:
      possible_actions.remove('RIGHT')
    if index_duck >= 9 or index_duck == 4:
      possible_actions.remove('DOWN')
      
    return possible_actions

  def result(self, state, action):
    """ Given state and action, return a new state that is the result of the action.
    Action is assumed to be a valid action in the state """

    # blank is the index of the blank square
    blank = self.translate_to_duck_index(self.find_blank_square(state))
    new_state = list(state)

    delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
    neighbor = blank + delta[action]
    
    new_state[self.translate_from_duck_index(blank)], new_state[self.translate_from_duck_index(neighbor)] = new_state[self.translate_from_duck_index(neighbor)], new_state[self.translate_from_duck_index(blank)]

    return tuple(new_state)

  def goal_test(self, state):
    """ Given a state, return True if state is a goal state or False, otherwise """

    return state == self.goal

  def h(self, node):
    return sum(s != g and (s != 0) for (s, g) in zip(node.state, self.goal))

  # For explanation, see EightPuzzle_mod (or README.txt ?)
  def heuristic_manhattan_distance_duck(self, node):
    manhattan_sum = 0
    index = 0
    for i in node.state:
      if i == 0: # including 0 causes heuristic to be not admissible
        index = index + 1
        continue
      index = self.translate_to_duck_index(index)
      matrixIndexValue = self.translate_to_duck_index(self.matrix[i])
      indexModX = index % self.squareSideLen
      indexGoalModX = matrixIndexValue % self.squareSideLen
      x = abs(indexModX-indexGoalModX)
      indexModY = index // self.squareSideLen # row
      indexGoalModY = matrixIndexValue // self.squareSideLen
      y = abs(indexModY-indexGoalModY)
      manhattan_sum = manhattan_sum + (x+y)
      index = self.translate_from_duck_index(index)
      index = index + 1
    return manhattan_sum
  
  # For question 2, returns MAX of the two heuristics
  def max_misplaced_manhattan_duck(self, node):
    return max(self.heuristic_manhattan_distance_duck(node), self.h(node))









