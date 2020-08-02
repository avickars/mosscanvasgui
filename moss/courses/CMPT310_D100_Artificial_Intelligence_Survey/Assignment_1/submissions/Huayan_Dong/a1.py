#a1.py

from search import *
import time

# ...

#-----------------------------------------------------------------------

# best_first_graph_search() in search.py is modified for Question 2 & 3
# replace the best_first_graph_search() in search.py with the following implementation
# and remove the implementation in this file before running this .py file

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
            return node, len(explored) # Modified to return the number of nodes removed from frontier for Question 2 & 3
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

# class EightPuzzle(Problem) in search.py is modified for Question 2
# replace the definition in search.py with the following definition
# and remove the definition in this file before running this .py file
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

    def h(self, node): #modified to exclude tile blank
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles. (Tile Blank is not included to be admissible) """

        return sum((s != g and s != 0) for (s, g) in zip(node.state, self.goal))


#---------------------------------------------------------------------

init_state = ()

# Question 1: Helper Functions
""" 
Write a function called make_rand_8puzzle() that returns a new instance of an EightPuzzle problem with a random initial state that is solvable. Note that EightPuzzle has a method called check_solvability that you should use to help ensure your initial state is solvable.
"""

def make_rand_8puzzle():
        init = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        while True:
              random.shuffle(init)
              newPuzzle = EightPuzzle(tuple(init))
              solvable = newPuzzle.check_solvability(init)
              if solvable:
                   global init_state
                   init_state = tuple(init)
                   break
              else:
                   del newPuzzle
        return newPuzzle

"""
Write a function called display(state) that takes an 8-puzzle state (i.e. a tuple that is a permutation of (0, 1, 2, ..., 8)) as input and prints a neat and readable representation of it. 0 is the blank, and should be printed as a * character.

For example, if state is (0, 3, 2, 1, 8, 7, 4, 6, 5) , then display(state) should print:
* 3 2
1 8 7
4 6 5
"""
def display(state):
        s = ""
        for num in state:
            if num == 0:
               s = s + "* "
            else:
               s = s + str(num) + " "

            if state.index(num) % 3 == 2:
               print (s)
               s = ""
        print("")
        return

#-----------------------------------------------------------------------
# Question 2: Comparing Algorithms
"""
Create 10 (more would be better!) random 8-puzzle instances (using your code from above), and solve each of them using the algorithms below. Each algorithm should be run on the exact same set of problems to make the comparison fair.

For each solved problem, record:
	the total running time in seconds
	the length (i.e. number of tiles moved) of the solution
	that total number of nodes that were removed from frontier
You will probably need to make some modifications to the A* code to get all this data.

The algorithms you should test are:
	A*-search using the misplaced tile heuristic (this is the default heuristic in the EightPuzzle class)
	A*-search using the Manhattan distance heuristic. Please implement your own (correctly working!) version of the Manhattan heuristic.
		Be careful: there is an incorrect Manhattan distance function in tests/test_search.py. So don’t use that!
	A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic
Summarize all your data in a single table in a spreadsheet as described below.

Based on your data, which algorithm is the best? Explain how you came to your conclusion.

"""

def manhattan(node):
        goal = (1,2,3,4,5,6,7,8,0)
        goal_index = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
        res = 0
        for i in range (3):
            for j in range (3):
                num = node.state[i*3+j]
                if num != 0:
                   goal_location = goal_index[goal.index(num)]
                   res = res + abs(goal_location[0]-i) + abs(goal_location[1]-j)
        return res

def maxh(node):
        goal = (1,2,3,4,5,6,7,8,0)
        h1 = sum(s != g for (s, g) in zip(node.state, goal))
        h2 = manhattan(node)
        return max(h1,h2)

def eight(): # using hints in Assignment 1 for timing
        """Generate a random eight-puzzle, and solve the same puzzle using A* search using 3 different heuristics"""
        puzzle = make_rand_8puzzle()
        #init_state = (0,3,7,1,5,6,2,8,4)
        #puzzle = EightPuzzle(init_state)
        print(init_state)

        #algorithm 1
        start_time = time.time()
        sol, pop = astar_search(puzzle,None,False)
        elapsed_time = time.time() - start_time
        print("Algorithm 1")
        print(f'Total running time (in seconds): {elapsed_time}s') 
        print("Length of the solution: ", sol.depth)
        print("Number of nodes removed from frontier: ", pop)
        del puzzle
        
        #algorithm 2
        puzzle = EightPuzzle(init_state)
        start_time = time.time()
        sol, pop = astar_search(puzzle,h=manhattan,display=False)
        elapsed_time = time.time() - start_time
        print("Algorithm 2")
        print(f'Total running time (in seconds): {elapsed_time}s') 
        print("Length of the solution: ", sol.depth)
        print("Number of nodes removed from frontier: ", pop)
        del puzzle

        #algorithm 3
        puzzle = EightPuzzle(init_state)
        start_time = time.time()
        sol, pop = astar_search(puzzle,h=maxh,display=False)
        elapsed_time = time.time() - start_time
        print("Algorithm 3")
        print(f'Total running time (in seconds): {elapsed_time}s') 
        print("Length of the solution: ", sol.depth)
        print("Number of nodes removed from frontier: ", pop)
        del puzzle
        
        return

#-----------------------------------------------------------------------

# Question 3: The House-Puzzle
"""
(Duck-puzzle) Implement a new Problem class called DuckPuzzle that is the same as the 8-puzzle, except the board has this shape (that looks a bit like a duck facing to the left):

+--+--+
|  |  |
+--+--+--+--+
|  |  |  |  |
+--+--+--+--+
   |  |  |  |
   +--+--+--+

 1 2
 3 4 5 6   goal state
   7 8 *

Tiles slide into the blank (the *) as in the regular 8-puzzle, but now the board has a different shape which changes the possible moves.

As in the previous question, test this problem using the same approach, and the same algorithms, as in the previous problem.

Be careful generating random instances: the check_solvability function from the EightPuzzle probably doesn’t work with this board!

Based on your results, how does the Duck-puzzle compare to the 8-puzzle: is it easier, harder, or about the same difficulty?

"""
def manhattanDuck(node):
        """ Tile Blank is not included to make Manhattan heuristic admissible """
        goal = (1,2,-1,-1,3,4,5,6,-1,7,8,0)
        goal_index = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)]
        res = 0
        stat = list(node.state)
        stat.insert(2,-1)
        stat.insert(3,-2)
        stat.insert(8,-3)
        for i in range (3):
            for j in range (4):
                num = stat[i*4+j]
                if num > 0:
                   goal_location = goal_index[goal.index(num)]
                   res = res + abs(goal_location[0]-i) + abs(goal_location[1]-j)
        return res

def maxhDuck(node):
        goal = (1,2,3,4,5,6,7,8,0)
        h1 = sum(s != g for (s, g) in zip(node.state, goal))
        h2 = manhattanDuck(node)
        return max(h1,h2)

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

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        elif index_blank_square % 4 == 1:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        elif index_blank_square % 4 == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif index_blank_square == 4:
            possible_actions.remove('UP')
        elif index_blank_square == 7:
            possible_actions.remove('DOWN')
        elif index_blank_square == 8:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        new_state = list(state)
        new_state.insert(2,-1)
        new_state.insert(3,-2)
        new_state.insert(8,-3)
        blank = self.find_blank_square(new_state)
        delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        new_state.remove(-1)
        new_state.remove(-2)
        new_state.remove(-3)
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable. (This function is copied over from class EightPuzzle and is not used) """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles. (Tile Blank is not included to be admissible) """

        return sum((s != g and s != 0) for (s, g) in zip(node.state, self.goal))


def make_rand_Duckpuzzle():
        """ Perform 200 to 300 random valid actions to the goal state to generate a "random" Duck puzzle"""
        init = (1,2,3,4,5,6,7,8,0)
        newPuzzle = DuckPuzzle(init)
        numAction = random.randint(200, 300)
        for i in range(numAction):
            actionslist = newPuzzle.actions(init)
            act = random.choice(actionslist)
            init = newPuzzle.result(init,act)
        del newPuzzle
        global init_state
        init_state = init
        return DuckPuzzle(init)

def displayDuck(state):
        l = list(state)
        l.insert(2,-1)
        l.insert(3,-2)
        l.insert(8,-3)
        s = ""
        for num in l:
            if num == 0:
               s = s + "* "
            elif num < 0:
               s = s + "  "
            else:
               s = s + str(num) + " "

            if l.index(num) % 4 == 3:
               print (s)
               s = ""
        print("")
        return

def duck(): # using hints in Assignment 1 for timing
        """Generate a random Duck puzzle, and solve the same puzzle using A* search using 3 different heuristics"""
        puzzle = make_rand_Duckpuzzle()
        #init_state = (1,0,3,2,5,6,4,7,8)
        #puzzle = DuckPuzzle(init_state)
        print(init_state)

        #algorithm 1
        start_time = time.time()
        sol, pop = astar_search(puzzle,None,False)
        elapsed_time = time.time() - start_time
        print("Algorithm 1")
        print(f'Total running time (in seconds): {elapsed_time}s') 
        print("Length of the solution: ", sol.depth)
        print("Number of nodes removed from frontier: ", pop)
        del puzzle

        #algorithm 2
        puzzle = DuckPuzzle(init_state)
        start_time = time.time()
        sol, pop = astar_search(puzzle,h=manhattanDuck,display=False)
        elapsed_time = time.time() - start_time
        print("Algorithm 2")
        print(f'Total running time (in seconds): {elapsed_time}s') 
        print("Length of the solution: ", sol.depth)
        print("Number of nodes removed from frontier: ", pop)
        del puzzle

        #algorithm 3
        puzzle = DuckPuzzle(init_state)
        start_time = time.time()
        sol, pop = astar_search(puzzle,h=maxhDuck,display=False)
        elapsed_time = time.time() - start_time
        print("Algorithm 3")
        print(f'Total running time (in seconds): {elapsed_time}s') 
        print("Length of the solution: ", sol.depth)
        print("Number of nodes removed from frontier: ", pop)
        del puzzle

        return
      
##############################################################################################
print("Eight Puzzle")
for i in range (10):
    print("Puzzle ", i)
    eight()
    print("")

print("Duck Puzzle")
for i in range (10):
    print("Puzzle ", i)
    duck()
    print("")

