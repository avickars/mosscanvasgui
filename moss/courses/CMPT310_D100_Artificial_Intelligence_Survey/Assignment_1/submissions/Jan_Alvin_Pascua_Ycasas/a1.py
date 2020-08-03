from search import *
import random
import time

# START QUESTION 1

def make_rand_8puzzle():
  while True: 
    puzzle_numbers = tuple(list(range(9)))
    # puzzle = EightPuzzle(tuple(random.sample(puzzle_numbers, k = len(puzzle_numbers))))
    puzzle = EightPuzzle((1, 2, 3, 4, 5, 7, 8, 6, 0))
    
    if(puzzle.check_solvability(puzzle.goal)):
      return puzzle

def display(puzzle_numbers):
  result = ""
  
  for var in puzzle_numbers:
    index = puzzle_numbers.index(var)
    
    if(index != 0 and index % 3 == 0):
      result += "\n"
    
    if(var == 0):
      result += "* "
    else:
      result += str(var) + " "
      
  print(result)
  
# puzzle = make_rand_8puzzle()
# display(puzzle.initial)

# END OF QUESTION 1


# START OF QUESTION 2

# Eight Puzzle
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

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        state = node.state
        
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        current_state = {}
        
        # place the values in the states
        for value in range(len(state)):
            current_state[state[value]] = index[value]
            
        # calculate distance
        distance = 0
        for value in range(0, 9):
            current_state_position = current_state[value]
            index_goal_position = index_goal[value]
            
            distance += abs(current_state_position[0] - index_goal_position[0])
            distance += abs(current_state_position[1] - index_goal_position[1])

        return distance
    
    def max_distance(self, node): 
        misplacedH = self.h(node)
        manhattanH = self.manhattan(node)
        return max(misplacedH, manhattanH)

# Helper Functions
def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    counter = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        counter += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, counter
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, counter

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def astar_search_default(puzzle_numbers):
    puzzle = EightPuzzle(puzzle_numbers)
    
    startTime = time.time()
    node, removed_nodes_counter = astar_search(puzzle)
    endTime = time.time()
    
    print("--- EXECUTION TIME (astar_search_default): " + str((endTime - startTime)))
    print("--- LENGTH (astar_search_default): " + str(len(node.solution())))
    print("--- TOTAL NUMBER OF REMOVED NODES (astar_search_default): " + str(removed_nodes_counter))

def astar_search_manhattan(puzzle_numbers):
    puzzle = EightPuzzle(puzzle_numbers)
    
    startTime = time.time()
    node, removed_nodes_counter = astar_search(puzzle, h=puzzle.manhattan)
    endTime = time.time()
    
    print("--- EXECUTION TIME (astar_search_manhattan): " + str((endTime - startTime)))
    print("--- LENGTH (astar_search_manhattan): " + str(len(node.solution())))
    print("--- TOTAL NUMBER OF REMOVED NODES (astar_search_manhattan): " + str(removed_nodes_counter))
    
def astar_search_max(puzzle_numbers):
    puzzle = EightPuzzle(puzzle_numbers)
    
    startTime = time.time()
    node, removed_nodes_counter = astar_search(puzzle, h=puzzle.max_distance)
    endTime = time.time()
    
    print("--- EXECUTION TIME (astar_search_max): " + str((endTime - startTime)))
    print("--- LENGTH (astar_search_max): " + str(len(node.solution())))
    print("--- TOTAL NUMBER OF REMOVED NODES (astar_search_max): " + str(removed_nodes_counter))
    
# NUMBER_OF_TIMES = 10

# for x in range(NUMBER_OF_TIMES):
#     # make the random puzzle
#     puzzle = make_rand_8puzzle()
#     puzzle_numbers = puzzle.initial
    
#     # display the current state
#     display(puzzle_numbers)
    
#     # do the algorithms
#     astar_search_default(puzzle_numbers)
#     print("\n")
#     astar_search_manhattan(puzzle_numbers)
#     print("\n")
#     astar_search_max(puzzle_numbers)
#     print("\n")

# END OF QUESTION 2

class DuckPuzzle(Problem):
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

        if(index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5):
            possible_actions.remove('UP')
        
        if(index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6):
            possible_actions.remove('LEFT')
        
        if(index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8):
            possible_actions.remove('RIGHT')
        
        if(index_blank_square > 5 or index_blank_square == 2):
            possible_actions.remove('DOWN')

        return possible_actions

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal
    
    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'LEFT': -1, 'RIGHT': 1}
        
        if(blank == 0 or blank == 1):
            delta['UP'] = 0
            delta['DOWN'] = 2
        elif(blank >= 2 and blank <= 5):
            delta['UP'] = -2
            delta['DOWN'] = 3
        elif(blank >= 6 and blank <= 8):
            delta['UP'] = -3
            delta['DOWN'] = 0
            
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)
    
    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        # TODO: GOTTA IMPLEMENT
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
        state = node.state
        
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        current_state = {}
        
        # place the values in the states
        for value in range(len(state)):
            current_state[state[value]] = index[value]
            
        # calculate distance
        distance = 0
        for value in range(0, 9):
            current_state_position = current_state[value]
            index_goal_position = index_goal[value]
            
            distance += abs(current_state_position[0] - index_goal_position[0])
            distance += abs(current_state_position[1] - index_goal_position[1])

        return distance
    
    def max_distance(self, node): 
        misplacedH = self.h(node)
        manhattanH = self.manhattan(node)
        return max(misplacedH, manhattanH)
    
def make_rand_8puzzle_duckpuzzle():
  while True: 
    puzzle_numbers = tuple(list(range(9)))
    puzzle = DuckPuzzle(tuple(random.sample(puzzle_numbers, k = len(puzzle_numbers))))
    
    if(puzzle.check_solvability(puzzle.goal)):
      return puzzle
  
def display_duckpuzzle(puzzle_numbers):
  result = ""
  
  for var in puzzle_numbers:
    index = puzzle_numbers.index(var)
    
    if(index == 6):
        result += "  "
        
    if(var == 0):
      result += "* "
    else:
      result += str(var) + " "
    
    if(index == 1 or index == 5 or index == 8):
      result += "\n"
      
  print(result)
  
# NUMBER_OF_TIMES = 10

# for x in range(NUMBER_OF_TIMES):
#     # make the puzzle
#     puzzle = make_rand_8puzzle_duckpuzzle()
#     puzzle_numbers = puzzle.initial
    
#     # display the current state
#     display_duckpuzzle(puzzle_numbers)
    
#     # do the algorithms
#     astar_search_default(puzzle_numbers)
#     print("\n")
#     astar_search_manhattan(puzzle_numbers)
#     print("\n")
#     astar_search_max(puzzle_numbers)
#     print("\n")
    
# END OF QUESTION 3