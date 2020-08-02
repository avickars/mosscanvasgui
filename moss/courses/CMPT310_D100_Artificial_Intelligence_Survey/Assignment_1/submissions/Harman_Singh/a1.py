from search import *
import random
import time
import operator


######################### From Search.py ##########################################################

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
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return (node, len(explored), len(explored) - len(frontier)) # Modified Return statement
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    NAME = 'EightPuzzle'

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

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))
    
    def manhattanDistance(self, node):
        """This method computes manhattan distance for two grids
        :param node:
        :return manhattan distance:
        """
        return sum(
          abs((val-1)%3 - i%3) + abs((val-1)//3 - i//3) for i, val in enumerate(node.state)
        )
    
    def hybridHeuristic(self, node):
        """This method get best result from manahattan distance and misplace title
        heuristics
        :param node:
        :return max of manhattan and misplaces title heuristics
        """
        return max(self.h(node), self.manhattanDistance(node))


# Helper function for shuffling states
def shufflePuzzle(puzzle):
  state = puzzle.goal
  for _ in range(100):
      action = random.choice(puzzle.actions(state))
      state = puzzle.result(state, action)
  puzzle.initial = state


################################# Question 1 ######################################################

def make_rand_8puzzle():
  """This method initializes random state for EightPuzzle class
  which is solvable
  :return Instance of EightPuzzle Class:
  """
  eightPuzzle = EightPuzzle()
  shufflePuzzle(eightPuzzle)
  return eightPuzzle

  # Another Method
  """
  initial = [x for x in range(9)]
  random.shuffle(initial)

  eightPuzzle = EightPuzzle(initial)

  while not eightPuzzle.check_solvability(eightPuzzle.initial):
    random.shuffle(eightPuzzle.initial)
  
  eightPuzzle.initial = tuple(eightPuzzle.initial)
  
  assert eightPuzzle.check_solvability(eightPuzzle.initial)
  return eightPuzzle
  """

def display(state):
  """This functions prints formated state
  :param state:
  """
  for i in range(0, len(state), 3):
    for j in range(i, i+3):
      print(state[j] if state[j] else '*', end=" ")
    print()

##################################### Question 3 #######################################################
class DuckPuzzle(Problem):
    GOAL_STATE = (1, 2, -1, -1, 3, 4, 5, 6, -1, 7, 8, 0)
    NAME = 'DuckPuzzle'
    
    def __init__(self, initial, goal=(1, 2, -1, -1, 3, 4, 5, 6, -1, 7, 8, 0)):
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

        # No Up - > 0, 1, 2, 6, 7
        # No Left -> 0, 4, 9
        # No right -> 1, 7, 11
        # No down -> 4, 9, 10, 11
        if index_blank_square in {0, 4, 9}:
            possible_actions.remove('LEFT')
        if index_blank_square in {0, 1, 2, 6, 7}:
            possible_actions.remove('UP')
        if index_blank_square in {1, 7, 11}:
            possible_actions.remove('RIGHT')
        if index_blank_square in {4, 9, 10, 11}:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
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
    
    def manhattanDistance(self, node):
        """This method computes manhattan distance for two grids
        :param node:
        :return manhattan distance:
        """
        excluded = {-1, 0}
        goalIndex = {value: (idx//4, idx%4) for idx, value in enumerate(self.goal) if value not in excluded}
        return sum((
            abs(idx//4 - goalIndex[v][0]) +
            abs(idx%4 - goalIndex[v][1])
          ) for idx, v in enumerate(node.state) if v not in excluded
        )
    
    def hybridHeuristic(self, node):
        """This method get best result from manahattan distance and misplace title
        heuristics
        :param node:
        :return max of manhattan and misplaces title heuristics
        """
        return max(self.h(node), self.manhattanDistance(node))

def runPuzzle(puzzle, heuristic):
  startTime = time.time()
  shufflePuzzle(puzzle)
  _, length, removed = astar_search(
    problem=puzzle,
    h={
      'manhattan': puzzle.manhattanDistance,
      'hybrid': puzzle.hybridHeuristic,
      'default': puzzle.h
    }[heuristic],
    display=False
  )
  print(f'-> Length: {length}, Removed: {removed}')
  return time.time() - startTime

def benchMark(puzzle):
  print(f'----------> Benchmarking {puzzle.NAME} <----------------')
  totalTimeByHeuristic = {}
  for test in range(10):
    print(f'\U0001f449 Running Iteration {test+1}...')
    for heuristic in ['manhattan', 'hybrid', 'default']:
      totalTimeByHeuristic[heuristic] = totalTimeByHeuristic.get(heuristic, [])
      totalTimeByHeuristic[heuristic].append(runPuzzle(puzzle, heuristic))
      print(f'\u2714\uFE0F Finished Running Heuristic-{heuristic.capitalize()} in {totalTimeByHeuristic[heuristic][-1]}')
    print()

  print('All Iteration Completed Successully \U0001f525')
  print()
  
  
  print('################# STATS #################')
  for heuristic in ['default', 'manhattan', 'hybrid']:
    # print(f'Total Time Taken by {heuristic} -> {totalTimeByHeuristic[heuristic]}')
    print(f'Average Time Taken by {heuristic} -> {sum(totalTimeByHeuristic[heuristic])/10}')
  print()

  print('################# Best Heuristic #################')
  print(f'--> {min(totalTimeByHeuristic.items(), key=operator.itemgetter(1))[0]}')
  print()
  print('################# Worst Heuristic #################')
  print(f'--> {max(totalTimeByHeuristic.items(), key=operator.itemgetter(1))[0]}')
  print()


def main():
  print('################# Starting Up #################')
  print()
  benchMark(DuckPuzzle(DuckPuzzle.GOAL_STATE))
  benchMark(EightPuzzle(EightPuzzle.GOAL_STATE))

if __name__ == "__main__":
  main()