#a1.py
from search import *
import random as ran
import time 


# Question 1 ------- 
def display(state):
  state_l = list(state)
  counter  = 0
  for i in range(9):
    counter += 1
    if(state_l[i] == 0):
      state_l[i] = "*"
    print(str(state_l[i]), end = ' ')
    if((counter == 3) or (counter == 6) or (counter == 9)):
      print("")

      

def make_rand_8puzzle():
  goal = [1,2,3,4,5,6,7,8,0]

  #Start with an intial state that's already solved 

  initial = [1,2,3,4,5,6,7,8,0]

  temp_puz = EightPuzzle(initial)

  #make 70 random moves 
  for i in range(70):

    leg_actions = temp_puz.actions(initial)

    blank_index = temp_puz.find_blank_square(initial)

    track1 = len(leg_actions)

    ran_num = ran.randrange(0,track1,1)


    if(leg_actions[ran_num] == 'UP'):
      num1 = initial[blank_index - 3]
      initial[blank_index] = num1
      initial[blank_index -3] = 0

    if(leg_actions[ran_num] == 'DOWN'):
      num2 = initial[blank_index + 3]
      initial[blank_index] = num2
      initial[blank_index + 3] = 0

    if(leg_actions[ran_num] == 'LEFT'):
      num3 = initial[blank_index - 1]
      initial[blank_index] = num3
      initial[blank_index -1] = 0
    

    if(leg_actions[ran_num] == 'RIGHT'):
      num4 = initial[blank_index + 1]
      initial[blank_index] = num4
      initial[blank_index +1] = 0

      
  tup_initial = tuple(initial)

  ran_puzz = EightPuzzle(tup_initial)

  return ran_puzz

# ----------------------------------


# Question 2 ---------------------------

#Importing best graph search to reflect changes in search.py

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    count = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        count += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print("The cost of the solution is:", len(node.solution()))
            print("Nodes removed from frontier: ", count)
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


# Bringing in astar for continuity ---

def astar_search(problem, h=None, display=False):
  """A* search is best-first graph search with f(n) = g(n)+h(n).
  You need to specify the h function when you call astar_search, or
  else in your Problem subclass."""
  h = memoize(h or problem.h, 'h')
  return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# Defining the Manhattan Heuristic for Eight Puzzle 
def Manhattan_ei(node):
  state = node.state
  # dy, dx 

  # Making a dictionary using: #https://www.programiz.com/python-programming/dictionary 
  #https://stackoverflow.#com/questions/30280856/populating-a-dictionary-using-for-loops-python
  #https://stackoverflow.com/questions/18449360/access-item-in-a-list-of-lists
  # as reference
  
  # the dictonary relates each location to a set of x and y values
  # goal_dist = {0:[0,0], 1:[2,2], 2:[1,2], 3:[0,2], 4:[2,1], 5:[1,1], 6:[0,1], 7:[2,0], 8:[1,0]}

  #goal = (1,2,3,4,5,6,7,8,0)
  state_dist = {}

  index_dist = [[2,2], [1,2], [0,2], [2,1], [1,1], [0,1], [2,0], [1,0], [0,0]]

  for i in range(len(state)):
    state_dist[state[i]] = index_dist[i]

  # Lists to be used in the for loop 
  # excluding 0 as that shouldn't be included 
  ylist_1 = [1,2,3]
  ylist_2 = [4,5,6]
  ylist_3 = [7,8]

  xlist_1 = [3,6]
  xlist_2 = [1,4,7]
  xlist_3 = [2,5,8]


  dis_x = 0
  dis_y = 0

  # For Debugging purposes
  # print(state_dist[4][1])
  # print("")

 # iterate through the puzzle to calculate the absolute y distances

  for j in range(9):
    if(j in ylist_1):
      dis_y += abs(2 - state_dist[j][1])

    if(j in ylist_2):
      dis_y += abs(1 - state_dist[j][1])


    if(j in ylist_3):
      dis_y += abs(0 - state_dist[j][1])

 # iterate through the puzzle to calculate the absolute x distances
  for k in range(9):
    if(k in xlist_1):
      dis_x += abs(0 - state_dist[k][0])

    if(k in xlist_2):
      dis_x += abs(2 - state_dist[k][0])

    if(k in xlist_3):
      dis_x += abs(1 - state_dist[k][0])

  return dis_x + dis_y 


# Function rewritten to ignore 0 tile
def h(node):
  """ Return the heuristic value for a given state. Default heuristic function used is 
  h(n) = number of misplaced tiles """

  state = node.state
  state_le = len(state)
  goal = (1,2,3,4,5,6,7,8,9,0)
  count = 0

  for j in range(state_le):
    if(state[j] == 0):
      continue   
    if(state[j] != goal[j]):
      count += 1

  return count


# Max Heuritic for Eight Puzzle 

def max_heur(node):
  de_heur = h(node)
  man_heur = Manhattan_ei(node)
  return (max(de_heur, man_heur))

#count made to keep track of iteration 
count_1 = 0
x = 10
print("Testing ",x," puzzles")
print("")
for i in range(x):
  test_2 = make_rand_8puzzle()
  count_1 += 1

  #Testing the Eight Puzzle 
  print("")
  print("Statistics for the Eight puzzle")
  print("Stats for puzzle: ", count_1)
  print("")
  print("-----------------------------------------------------------------")

  print("Solving using the default heuristic: ")
  print("")

  de_start = time.time()
  result = astar_search(test_2, h)
  de_end = time.time() 
  print("The time it took for default was: ", de_end - de_start)

  print("")




  print("Solving using the Manhattan heuristic: ")

  print("")

  man_start = time.time()
  result_2 = astar_search(test_2,Manhattan_ei)
  man_end = time.time()
  print("The time it took for Manhattan was: ", man_end - man_start)

  print("")

  print("Solving using the Max heuristic: ")

  print("")

  max_start = time.time()
  result_3 = astar_search(test_2, max_heur)
  max_end = time.time()
  print("The time it took for Max Heuristic was: ", max_end - max_start)
  print("")


# ----------------------------------------------


# Question 3 ----------------------------------

class DuckPuzzle(Problem):

  def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    """ Define goal state and initialize a problem """
    super().__init__(initial, goal)

  def find_blank_square(self, state):
    """Return the index of the blank square in a given state"""

    return state.index(0)

# The major difference between Duck Puzzle and Eight Puzzle
# is how the actions are computed 

  def actions(self, state):
    """ Return the actions that can be executed in the given state.
    The result would be a list, since there are only four possible actions
    in any given state of the environment """

    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    index_blank_square = self.find_blank_square(state)

    #left - exception 
    l_excep = [0, 2, 6]

    #up - exception 
    u_excep = [0, 1, 4, 5]

    #right - exception 
    r_excep = [1, 5, 8]

    #down - exception 

    d_excep = [2, 6, 7, 8]

    if index_blank_square in l_excep:
      possible_actions.remove('LEFT')
    if index_blank_square in u_excep:
      possible_actions.remove('UP')
    if index_blank_square in r_excep:
      possible_actions.remove('RIGHT')
    if index_blank_square in d_excep:
      possible_actions.remove('DOWN')

    return possible_actions


  def result(self, state, action):
    """ Given state and action, return a new state that is the result of the action.
    Action is assumed to be a valid action in the state """

    up = 0
    down = 0

    # blank is the index of the blank square
    blank = self.find_blank_square(state)
    new_state = list(state)

    if(blank < 3):
      up = -2
      down = 2
    elif(blank == 3):
      up = -2
      down = 3
    else:
      up = -3
      down = 3


    delta = {'UP': up, 'DOWN': down, 'LEFT': -1, 'RIGHT': 1}
    neighbor = blank + delta[action]
    new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

    return tuple(new_state)

  def goal_test(self, state):
    """ Given a state, return True if state is a goal state or False, otherwise """

    return state == self.goal

## Done with the class Declaration --------------




# Making a random instance of Duck Puzzle for testing purposes


def make_rand_duckpuzzle():

  #Start with an intial state that's already solved 

  initial = (1,2,3,4,5,6,7,8,0)

  temp_puz = DuckPuzzle(initial)

  #make 70 random moves 
  for i in range(70):

    leg_actions = temp_puz.actions(initial)


    track1 = len(leg_actions)

    ran_num = ran.randint(0,(track1-1))


    if(leg_actions[ran_num] == 'UP'):
      initial = temp_puz.result(initial, 'UP')

    if(leg_actions[ran_num] == 'DOWN'):
      initial = temp_puz.result(initial, 'DOWN')

    if(leg_actions[ran_num] == 'LEFT'):
      initial = temp_puz.result(initial, 'LEFT')
    

    if(leg_actions[ran_num] == 'RIGHT'):
      initial = temp_puz.result(initial, 'RIGHT')

      
  tup_initial = tuple(initial)

  ran_puzz = EightPuzzle(tup_initial)

  return ran_puzz



## Making Manhattan for Duck Puzzle -------

def Manhattan_duck(node):
  state = node.state 
  state_dist = {}

  index_dist = [[3,2], [2,2], [3,1], [2,1], [1,1], [0,1], [2,0], [1,0], [0,0]]

  for i in range(len(state)):
    state_dist[state[i]] = index_dist[i]

  ylist_1 = [1, 2]
  ylist_2 = [3, 4, 5, 6]
  ylist_3 = [7, 8]

  xlist_1 = [1, 3]
  xlist_2 = [2, 4, 7]
  xlist_3 = [5,8]
  xlist_4 = [6]


  dis_x = 0
  dis_y = 0

  for j in range(9):
    if(j in ylist_1):
      dis_y += abs(2 - state_dist[j][1])

    if(j in ylist_2):
      dis_y += abs(1 - state_dist[j][1])

    if(j in ylist_3):
      dis_y += abs(0 - state_dist[j][1])

  for k in range(9):
    if(k in xlist_1):
      dis_x += abs(3 - state_dist[k][0])

    if(k in xlist_2):
      dis_x += abs(2 - state_dist[k][0])

    if(k in xlist_3):
      dis_x += abs(1 - state_dist[k][0])

    if(k in xlist_4):
      dis_x += abs(0 - state_dist[k][0])

  return dis_x + dis_y 

def max_heur_d(node):
  de_heur = h(node)
  man_heur = Manhattan_duck(node)
  return (max(de_heur, man_heur))


# count made to keep track of iteration 
count_2 = 0
y = 10
print("Testing ",y, " puzzles")
print("")
for j in range(y):

  duck = make_rand_duckpuzzle()

  count_2 += 1
  print("")
  print("")
  print("-----------------------------------------------------------------")
  print("")
  print("Statistics for the Duck Puzzle")
  print("Stats for puzzle: ", count_2)
  print("")
  print("")




  print("Solving using the Default heuristic: ")
  print("")

  de_start = time.time()
  result = astar_search(duck, h)
  de_end = time.time() 
  print("The time it took for default was: ", de_end - de_start)

  print("")
  print("Solving using the Manhattan heuristic: ")
  print("")

  man_start = time.time()
  result_2 = astar_search(duck,Manhattan_duck)
  man_end = time.time()
  print("The time it took for Manhattan was: ", man_end - man_start)


  print("")
  print("Solving using the Max heuristic: ")
  print("")

  max_start = time.time()
  result_4 = astar_search(duck, max_heur_d)
  max_end = time.time() 
  print("The time it took for default was: ", max_end - max_start)
  print("-----------------------------------------------------------------")


