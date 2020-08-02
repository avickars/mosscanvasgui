# a1.py
from search import *
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
    start_time = time.time()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            elapsed_time = time.time()-start_time
            if display:
                print("solution length: ",node.depth)
                print('elapsed time (in seconds): ',elapsed_time)
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node,elapsed_time,len(explored)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None
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
        score = 0
        rows = [2,0,0,0,1,1,1,2,2,2]
        columns = [2,0,1,2,0,1,2,0,1,2]
        for i in range(1,len(node.state)+1):
            score += abs(rows[node.state[i-1]] - rows[i]) + abs(columns[node.state[i-1]] - columns[i])
            
        return score
    def max_h(self, node):
        return max(self.h(node),self.manhattan(node))


# ______________________________________________________________________________
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

        if index_blank_square in [0,2,6]:
            possible_actions.remove('LEFT')
        if index_blank_square in [0,1,4,5]:
            possible_actions.remove('UP')
        if index_blank_square in [1,5,8]:
            possible_actions.remove('RIGHT')
        if index_blank_square in [2,6,7,8]:
            possible_actions.remove('DOWN')

        return possible_actions
    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if(blank < 4):
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        return True
    
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))
    def manhattan(self, node):
        score = 0
        rows = [2,0,0,1,1,1,1,2,2,2]
        columns = [3,0,1,0,1,2,3,1,2,3]
        for i in range(1,len(node.state)+1):
            score += abs(rows[node.state[i-1]] - rows[i]) + abs(columns[node.state[i-1]] - columns[i])
        return score
    def max_h(self, node):
        return max(self.h(node),self.manhattan(node))
def make_rand_8puzzle():
    numList = [1,2,3,4,5,6,7,8,0]
    solvable = False
    while(solvable == False):
        random.shuffle(numList)
        numTuple = tuple(numList)
        eightPuzzle = EightPuzzle(numTuple)    
        if(eightPuzzle.check_solvability(numTuple)):
            solvable = True
    display(numTuple)
    return eightPuzzle
def display(state):
    for x in range(9):
        if(x%3==0):
            print()
        if(state[x] == 0):
            print("*", end=" ");
        else:
            print(state[x], end=" ");
    print()
def test_duck_puzzle():
    numList = [1,2,3,4,5,6,7,8,0]
    solvable = False
    while(solvable == False):
        data = []
        random.shuffle(numList)
        numTuple = tuple(numList)
        puzzle = DuckPuzzle(numTuple)
        data.append(astar_search(puzzle,h=puzzle.h,display=False))
        data.append(astar_search(puzzle,h=puzzle.manhattan,display=False))
        data.append(astar_search(puzzle,h=puzzle.max_h,display=False))
        if(data[0] != None):
            solvable = True
            print(numTuple[0],numTuple[1])
            print(numTuple[2],numTuple[3],numTuple[4],numTuple[5])
            print(numTuple[6],numTuple[7],numTuple[8])
    return data

puzzles = []
misplaced_data = []
manhattan_data = []
max_data = []

for i in range(20):
    puzzle = make_rand_8puzzle()
    puzzles.append(puzzle)
    misplaced_data.append(astar_search(puzzle,h=puzzle.h,display=True))
    manhattan_data.append(astar_search(puzzle,h=puzzle.manhattan,display=True))
    max_data.append(astar_search(puzzle,h=puzzle.max_h,display=True))
for i in range(20):
    display(puzzles[i].initial)
    print("misplaced heuristic: ",misplaced_data[i][0].depth," ",misplaced_data[i][1]," ",misplaced_data[i][2])
    print("manhattan heuristic: ",manhattan_data[i][0].depth," ",manhattan_data[i][1]," ",manhattan_data[i][2])
    print("max heuristic: ",max_data[i][0].depth," ",max_data[i][1]," ",max_data[i][2])

for i in range(20):
    data = test_duck_puzzle()
    print("misplaced heuristic: ",data[0][0].depth," ",data[0][1]," ",data[0][2])
    print("manhattan heuristic: ",data[1][0].depth," ",data[1][1]," ",data[1][2])
    print("max heuristic: ",data[2][0].depth," ",data[2][1]," ",data[2][2])
    


