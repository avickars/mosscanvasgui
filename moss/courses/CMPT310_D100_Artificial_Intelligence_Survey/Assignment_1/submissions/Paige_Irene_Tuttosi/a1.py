# a1.py

from search import *
import random
import copy
import pprint
import csv
import time

textfile = open("a1.csv", "w+")
headers = ["puzzle", "search", "timing", "length", "remove\n"]
textfile.write(",".join(headers))

pp = pprint.PrettyPrinter(width=500, compact=True)

# For all questions
for_csv = []
runs = 38

#Question1

def make_rand_8puzzle():
  solvable = False
  puzzle = [1,2,3,4,5,6,7,8,0]
  while not solvable:
    random.shuffle(puzzle)
    new_puzzle = EightPuzzle(tuple(puzzle))
    solvable = new_puzzle.check_solvability(new_puzzle.initial)

  return new_puzzle

def display(state):
  puzzle = list(state)
  new_puzzle = copy.deepcopy(puzzle)
  i = new_puzzle.index(0)
  new_puzzle[i] = '*'
  print(*new_puzzle[0:3], sep=' ')
  print(*new_puzzle[3:6], sep=' ')
  print(*new_puzzle[6:9], sep=' ')

#Question2

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
    removed = 0
    while frontier:
        node = frontier.pop()
        removed += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, removed, len(explored)]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return [None, removed, len(explored)]

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    # you need to tell A* which heruistic to usd, no h does default misplaces
    if h == "manhattan":
        h = memoize(problem.manhattan, 'manhattan')
    elif h == "max":
        h = memoize(problem.max_h, 'max_h')
    else:
      h = memoize(problem.h, 'h')

    start_time = time.time()
    solution, removed, length = best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
    elapsed_time = time.time() - start_time

    return [solution, elapsed_time, length, removed]

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

    #fixed to not count 0
    def h(self, node):
      """ Return the heuristic value for a given state. Default heuristic function used is h(n) = number of misplaced tiles """
      misplaced = 0
      for (s, g) in zip(node.state, self.goal):
        if s != g and s != 0:
          misplaced += 1
      return misplaced

    def manhattan(self, node):
        """ Return the manhattan heuristic value for a given state. """
        
        # change goal and curent state to a list
        current = list(node.state)
        goal = list(self.goal)
        h = 0

        # iterate over the current state
        for i, tile in enumerate(current):
            # since we are in a 3x3 table we can use this to find the location
            if tile != 0:
              current_row, current_col = int(i/3), i%3
              # we find the index of the current number in the goal
              # use the use the 3x3 property on that index to get location
              goal_row, goal_col = int(goal.index(tile)/3), goal.index(tile)%3
              # sum the differences in location
              h += (abs(current_row - goal_row) + abs(current_col - goal_col))

        return h

    def max_h(self, node):
        """ Return the maximum heuristic value for a given state betweent the
            misplaced and manhattan heuristics. """

        return max(EightPuzzle.h(self,node), EightPuzzle.manhattan(self,node))

class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a duck shaped board, where one of the
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

        # looking at the puzzle shape, remove illegal moves
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # 0,1
        delta1 = {'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        # 2,3
        delta2 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        # 4,5
        delta3 = {'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        # 6,7,8
        delta4 = {'UP' : -3, 'LEFT': -1, 'RIGHT': 1}

        if blank == 0 or blank == 1:
          neighbor = blank + delta1[action]
          new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        elif blank == 2 or blank == 3:
          neighbor = blank + delta2[action]
          new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        elif blank == 4 or blank == 5:
          neighbor = blank + delta3[action]
          new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        else:
          neighbor = blank + delta4[action]
          new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    # fixed to not count 0
    def h(self, node):
      """ Return the heuristic value for a given state. Default heuristic function used is h(n) = number of misplaced tiles """
      misplaced = 0
      for (s, g) in zip(node.state, self.goal):
        if s != g and s != 0:
          misplaced += 1
      return misplaced

    def manhattan(self, node):
        """ Return the manhattan heuristic value for a given state. """
        
        # change goal and curent state to a list
        current = list(node.state)
        goal = list(self.goal)
        h = 0
        current.insert(2, None)
        current.insert(3, None)
        current.insert(8, None)
        goal.insert(2, None)
        goal.insert(3, None)
        goal.insert(8, None)

        # iterate over the current state
        for i, tile in enumerate(current):
            if tile != None and tile != 0:
              # since we are in a 3x3 table we can use this to find the location
              current_row, current_col = int(i/4), i%4
              # we find the index of the current number in the goal
              # use the use the 3x3 property on that index to get location
              goal_row, goal_col = int(goal.index(tile)/4), goal.index(tile)%4
              # sum the differences in location
              h += (abs(current_row - goal_row) + abs(current_col - goal_col))

        return h

    def max_h(self, node):
      """ Return the maximum heuristic value for a given state betweent the
      misplaced and manhattan heuristics. """

      return max(EightPuzzle.h(self,node), EightPuzzle.manhattan(self,node))


results1 = []
initial1 = []

for i in range(0,runs):
  #create the random solvable puzzle
  puzzle = make_rand_8puzzle()
  #run each type of search
  h_solution = astar_search(puzzle)
  manhattan_solution = astar_search(puzzle, "manhattan")
  max_solution = astar_search(puzzle, "max")
  # store for easy diaplay
  results1.append({
    "h": {
      "node": h_solution[0].state,
      "timing": h_solution[1],
      "length": h_solution[2],
      "removed": h_solution[3]
    },
    "manhattan": {
        "node": manhattan_solution[0].state,
        "timing": manhattan_solution[1],
        "length": manhattan_solution[2],
        "removed": manhattan_solution[3]
    },
    "max": {
        "node": max_solution[0].state,
        "timing": max_solution[1],
        "length": max_solution[2],
        "removed": max_solution[3]
    },
  })

  initial1.append(puzzle.initial)

  for_csv.append(["eight", "misplaced", str(h_solution[1]), str(h_solution[2]), str(h_solution[3])])
  for_csv.append(["eight", "manhattan", str(manhattan_solution[1]), str(manhattan_solution[2]), str(manhattan_solution[3])])
  for_csv.append(["eight", "max", str(max_solution[1]), str(max_solution[2]), str(max_solution[3])])

# display results
for i in range(0,runs):
  intro = "Run number " + str(i+1)
  print(intro)
  print("\nInitial puzzle:")
  display(initial1[i])
  print("\nSolution Misplaced:")
  display(results1[i]['h']['node'])
  pp.pprint(results1[i]['h'])
  print("\nSolution Manhattan")
  display(results1[i]['manhattan']['node'])
  pp.pprint(results1[i]['manhattan'])
  print("\nSolution Max")
  display(results1[i]['max']['node'])
  pp.pprint(results1[i]['max'])
  print("\n\n")

#Question3

def displayDuck(state):
  puzzle = list(state)
  new_puzzle = copy.deepcopy(puzzle)
  i = new_puzzle.index(0)
  new_puzzle[i] = '*'
  print(*new_puzzle[0:2], sep=' ')
  print(*new_puzzle[2:6], sep=' ')
  print(end = '  ')
  print(*new_puzzle[6:9], sep=' ')

# create random duck puzzle

def make_duck_puzzle():
  # start at solved
  puzzle = [1,2,3,4,5,6,7,8,0]
  # create instance
  new_puzzle = DuckPuzzle(tuple(puzzle))
  # move 1 tile 100 times
  for i in range(0,1000):
    # get the possible actions for current state
    possible_actions = new_puzzle.actions(new_puzzle.initial)
    # randomly choose one of these
    action = random.choice(possible_actions)
    new_puzzle.initial = new_puzzle.result(new_puzzle.initial, action)

  return new_puzzle

results2 = []
initial2 = []

for i in range(0,runs):
  #create the random solvable puzzle
  puzzle = make_duck_puzzle()
  #run each type of search
  h_solution = astar_search(puzzle)
  manhattan_solution = astar_search(puzzle, "manhattan")
  max_solution = astar_search(puzzle, "max")
  # store for easy diaplay
  results2.append({
    "h": {
      "node": h_solution[0].state,
      "timing": h_solution[1],
      "length": h_solution[2],
      "removed": h_solution[3]
    },
    "manhattan": {
        "node": manhattan_solution[0].state,
        "timing": manhattan_solution[1],
        "length": manhattan_solution[2],
        "removed": manhattan_solution[3]
    },
    "max": {
        "node": max_solution[0].state,
        "timing": max_solution[1],
        "length": max_solution[2],
        "removed": max_solution[3]
    },
  })

  initial2.append(puzzle.initial)

  for_csv.append(["duck", "misplaced", str(h_solution[1]), str(h_solution[2]), str(h_solution[3])])
  for_csv.append(["duck", "manhattan", str(manhattan_solution[1]), str(manhattan_solution[2]), str(manhattan_solution[3])])
  for_csv.append(["duck", "max", str(max_solution[1]), str(max_solution[2]), str(max_solution[3])])

# display results
for i in range(0,runs):
  intro = "Run number " + str(i+1)
  print(intro)
  print("\nInitial puzzle:")
  displayDuck(initial2[i])
  print("\nSolution Misplaced:")
  displayDuck(results2[i]['h']['node'])
  pp.pprint(results2[i]['h'])
  print("\nSolution Manhattan")
  displayDuck(results2[i]['manhattan']['node'])
  pp.pprint(results2[i]['manhattan'])
  print("\nSolution Max")
  displayDuck(results2[i]['max']['node'])
  pp.pprint(results2[i]['max'])
  print("\n\n")

for row in for_csv:
  textfile.write(",".join(row) + "\n")

textfile.close()