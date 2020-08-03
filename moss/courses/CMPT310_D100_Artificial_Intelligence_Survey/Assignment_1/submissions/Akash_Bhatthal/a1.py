#!/usr/bin/env python3

"""a1.py: CMPT 310 Assignment 1"""

# Author:       Akash Bhatthal
__author__   = "Akash Bhatthal"

# Sources:
#   Headers
#     https://stackoverflow.com/questions/1523427/what-is-the-common-header-format-of-python-files
#     https://developer.lsst.io/python/numpydoc.html#py-docstring-basics
#   Main Function
#     https://stackoverflow.com/questions/419163/what-does-if-name-main-do
#   Python Documentation
#     https://docs.python.org/3/library/random.html
#     https://docs.python.org/3/library/time.html
#     https://docs.python.org/3/library/csv.html
#   A* Algorithm Research
#     https://youtu.be/GazC3A4OQTE
#     https://youtu.be/ySN5Wnu88nE
#     https://blog.goodaudience.com/solving-8-puzzle-using-a-algorithm-7b509c331288
#   Manhattan Heuristic
#     https://xlinux.nist.gov/dads/HTML/manhattanDistance.html
#     https://cse.iitk.ac.in/users/cs365/2009/ppt/13jan_Aman.pdf
#   Other
#     https://www.geeksforgeeks.org/ternary-operator-in-python
#     https://www.w3schools.com/python/ref_keyword_assert.asp
#     https://www.python-course.eu/python3_decorators.php
#     https://www.python-course.eu/python3_memoization.php
#     https://www.w3schools.com/python/ref_func_zip.asp
#     https://www.programiz.com/python-programming/methods/list/index
#     https://realpython.com/python-csv/

#--------------------------------#

from search import *                        # aima-python
from random import sample, choice           # used to generate random puzzle states
from time import time                       # used to determine algorithm runtime
import csv                                  # used to record data

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
QUESTION_THREE = True   # If True, generates a DuckPuzzle instead of an EightPuzzle

def main():
  """ Main Procedure """

  numOfPuzzles = 10
  with open("assign1.csv", mode='w') as dataFile:
    writer = csv.writer(dataFile, delimiter=',', quotechar='"')
    writer.writerow(["Test", "Puzzle", "Heuristic", "Elapsed Time", "Length", "Popped"])

    for i in range(numOfPuzzles):
      print("Test", i + 1)

      if QUESTION_THREE:
        print("Generating a random duck-puzzle...")
        randPuzzle = make_rand_duck_puzzle()
      else:
        print("Generating a random 8-puzzle...")
        randPuzzle = make_rand_8puzzle()

      manhattan = randPuzzle.manhattan
      maximum = randPuzzle.maximum
      initialState = randPuzzle.initial
      randPuzzle.display(initialState)
      print()
      # print(manhattan(Node(initialState)))

      print("A*-search using the misplaced tile heuristic...")
      elapsedTime, length, popped = astar_search(randPuzzle)
      writer.writerow([i + 1, initialState, 'Misplaced', elapsedTime, length, popped])
      print()

      print("A*-search using the Manhattan distance heuristic...")
      elapsedTime, length, popped = astar_search(randPuzzle, h=manhattan)
      writer.writerow([i + 1, initialState, 'Manhattan', elapsedTime, length, popped])
      print()

      print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic...")
      elapsedTime, length, popped = astar_search(randPuzzle, h=maximum)
      writer.writerow([i + 1, initialState, 'Maximum', elapsedTime, length, popped])
      print()

#--------------------------------#

def make_rand_8puzzle():
  """ Returns a new instance of an EightPuzzle problem with a random initial state that is solvable. """

  isSolvable = False
  while (not isSolvable):
    randomPuzzle = EightPuzzle(tuple(random.sample(range(9), 9)))
    isSolvable = randomPuzzle.check_solvability(randomPuzzle.initial)
  return randomPuzzle


def make_rand_duck_puzzle(moves=1000):
  """ Returns a new instance of a DuckPuzzle problem with a random initial state that is solvable. """

  currState = GOAL
  currPuzzle = DuckPuzzle(currState)
  for i in range(moves):
    action = choice(currPuzzle.actions(currState))
    currState = currPuzzle.result(currState, action)
  return DuckPuzzle(currState)


# Adapted from search.py
def best_first_graph_search(problem, f, display=False):
  """ Search the nodes with the lowest f scores first.
  You specify the function f(node) that you want to minimize; for example,
  if f is a heuristic estimate to the goal, then we have greedy best
  first search; if f is node.depth then we have breadth-first search.
  There is a subtlety: the line "f = memoize(f, 'f')" means that the f
  values will be cached on the nodes as they are computed. So after doing
  a best first search you can examine the f values of the path returned. """

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
          return (node, len(explored) + 1)
      explored.add(node.state)
      for child in node.expand(problem):
          if child.state not in explored and child not in frontier:
              frontier.append(child)
          elif child in frontier:
              if f(child) < frontier[child]:
                  del frontier[child]
                  frontier.append(child)
  return (None, len(explored))


# Adapted from search.py
def astar_search(problem, h=None, display=False):
  """ A* search is best-first graph search with f(n) = g(n)+h(n).
  You need to specify the h function when you call astar_search, or
  else in your Problem subclass. """

  assert type(problem) in (DuckPuzzle, EightPuzzle)

  startTime = time()
  h = memoize(h or problem.h, 'h')
  node, popped = best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
  elapsedTime = time() - startTime

  length = node.path_cost
  assert popped > 0
  assert length >= 0

  print(f'elapsed time (in seconds): {elapsedTime}s')
  print(f'length of the solution: {length} tile{"s" if length != 1 else ""} moved')
  print(f'total number of nodes removed from frontier: {popped}')
  return (elapsedTime, length, popped)

#--------------------------------#

# Adapted from EightPuzzle in search.py
class EightPuzzle(Problem):
  """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
  squares is a blank. A state is represented as a tuple of length 9, where  element at
  index i represents the tile number  at index i (0 if it's an empty square) """

  def __init__(self, initial, goal=GOAL):
    """ Define goal state and initialize a problem """

    super().__init__(initial, goal)

  def display(self, state):
    """ Takes an 8-puzzle state as input and prints a neat and readable representation of it. """

    assert type(state) == tuple
    assert len(state) == 9
    for i in range(9):
      if i % 3 == 0 and i != 0:
        print()
      print('*' if state[i] == 0 else state[i], end=' ')
    print()

  def find_blank_square(self, state):
      """ Return the index of the blank square in a given state """

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

  def manhattan(self, node):
    """ Manhattan Distance Heuristic. The distance between two points measured along axes at right angles. """

    goal = self.goal
    state = node.state
    def coor(i):
      return (i // 3, i % 3)
    def uncoor(arr):
      return arr[0] * 3 + arr[1]
    posDiffs = [(coor(state.index(i)), coor(goal.index(i))) for i in state]
    distSum = 0
    for posDiff in posDiffs:
      if state[uncoor(posDiff[0])]:
        distSum += sum(abs(g - s) for (s, g) in zip(posDiff[0], posDiff[1]))
    return distSum

  def maximum(self, node):
    """ A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic """

    return max(self.manhattan(node), self.h(node))

#--------------------------------#

# Adapted from EightPuzzle in search.py
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a duck-shaped board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where an element at
    index i represents the tile number at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=GOAL):
      """ Define goal state and initialize a problem """

      super().__init__(initial, goal)

    def display(self, state):
      """ Takes a duck-puzzle state as input and prints a neat and readable representation of it. """

      assert type(state) == tuple
      assert len(state) == 9

      def printTiles(i, j):
        tiles = ""
        for i in range(i-1, j):
          tiles += ('*' if state[i] == 0 else str(state[i])) + ' '
        print(tiles)

      printTiles(1, 2)
      printTiles(3, 6)
      print("  ", end='')
      printTiles(7, 9)
      
    def find_blank_square(self, state):
      """ Return the index of the blank square in a given state """
      return state.index(0)

    def actions(self, state):
      """ Return the actions that can be executed in the given state.
      The result would be a list, since there are only four possible actions
      in any given state of the environment """

      possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
      index_blank_square = self.find_blank_square(state)
      if index_blank_square in (0, 2, 6):
        possible_actions.remove('LEFT')
      if index_blank_square in (0, 1, 4, 5):
        possible_actions.remove('UP')
      if index_blank_square in (1, 5, 8):
        possible_actions.remove('RIGHT')
      if index_blank_square in (2, 6, 7, 8):
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

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
      """ Manhattan Distance Heuristic. The shortest traversable distance between two points. """

      goal = self.goal
      state = node.state
      distSum = 0

      invalidGoal = Exception("DuckPuzzle.manhattan.getDist: Invalid goal index")
      invalidState = Exception("DuckPuzzle.manhattan.getDist: Invalid state index")

      def getDist(s, g):
        if s == 0:
          if g == 0:
            return 0
          elif g in (1, 2):
            return 1
          elif g == 3:
            return 2
          elif g in (4, 6):
            return 3
          elif g in (5, 7):
            return 4
          elif g == 8:
            return 5
          else:
            raise invalidGoal
        elif s == 1:
          if g == 1:
            return 0
          elif g in (0, 3):
            return 1
          elif g in (2, 4, 6):
            return 2
          elif g in (5, 7):
            return 3
          elif g == 8:
            return 4
          else:
            raise invalidGoal
        elif s == 2:
          if g == 2:
            return 0
          elif g in (0, 3):
            return 1
          elif g in (1, 4, 6):
            return 2
          elif g in (5, 7):
            return 3
          elif g == 8:
            return 4
          else:
            raise invalidGoal
        elif s == 3:
          if g == 3:
            return 0
          elif g in (1, 2, 4, 6):
            return 1
          elif g in (0, 5, 7):
            return 2
          elif g == 8:
            return 3
          else:
            raise invalidGoal
        elif s == 4:
          if g == 4:
            return 0
          elif g in (3, 5, 7):
            return 1
          elif g in (1, 2, 6, 8):
            return 2
          elif g == 0:
            return 3
          else:
            raise invalidGoal
        elif s == 5:
          if g == 5:
            return 0
          elif g in (4, 8):
            return 1
          elif g in (3, 7):
            return 2
          elif g in (1, 2, 6):
            return 3
          elif g == 0:
            return 4
          else:
            raise invalidGoal
        elif s == 6:
          if g == 6:
            return 0
          elif g in (3, 7):
            return 1
          elif g in (1, 2, 4, 8):
            return 2
          elif g in (0, 5):
            return 3
          else:
            raise invalidGoal
        elif s == 7:
          if g == 7:
            return 0
          elif g in (4, 6, 8):
            return 1
          elif g in (3, 5):
            return 2
          elif g in (1, 2):
            return 3
          elif g == 0:
            return 4
          else:
            raise invalidGoal
        elif s == 8:
          if g == 8:
            return 0
          elif g in (5, 7):
            return 1
          elif g in (4, 6):
            return 2
          elif g == 3:
            return 3
          elif g in (1, 2):
            return 4
          elif g == 0:
            return 5
          else:
            raise invalidGoal
        else:
          raise invalidState
        
      for tile in state:
        stateIndex = state.index(tile)
        goalIndex = goal.index(tile)
        distSum += getDist(stateIndex, goalIndex)
      return distSum

    def maximum(self, node):
      """ A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic """

      return max(self.manhattan(node), self.h(node))


if __name__ == "__main__":
  main()