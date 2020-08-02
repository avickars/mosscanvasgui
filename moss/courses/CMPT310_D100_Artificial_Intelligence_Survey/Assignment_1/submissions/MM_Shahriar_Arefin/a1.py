# a1.py - Shahriar Arefin

from search import *
import random
import time

#----------------------------------------------------------------------
#QUESTION 3: Duck Puzzle Class
class DuckPuzzle(Problem):
    """ The problem of Duck Puzzle, where one of the
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
        ##
        ####
         ###

        not_UP = (0,1,4,5) #squares that can't move up
        not_DOWN = (2, 6, 7, 8) #squares that can't move down
        not_LEFT = (0, 2, 6) #tuple that contains squares that can't move left
        not_RIGHT = (1, 5, 8) #tuples that contains squares that can't move right 

          
        if index_blank_square in not_UP:
            possible_actions.remove('UP')
        if index_blank_square in not_DOWN:
            possible_actions.remove('DOWN')
        if index_blank_square in not_LEFT:
            possible_actions.remove('LEFT')
        if index_blank_square in not_RIGHT:
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # Seeing the duck shape we can see at tiles 0,1,2 Up results in -2 and down move results
        # in +2. However, right and left movement results in same +1 and -1.
        # We als osee only for tile 3 UP results in +2 and down results in -3

        #Exception 1 for tile 3
        delta_exception_one = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        tile_three=(3, 3, 3)

        #Exception 2 for tile 0,1,2
        delta_exception_two = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        alternative_tiles = (0, 1, 2)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank in alternative_tiles:
            neighbor = blank + delta_exception_two[action]
        elif blank in tile_three:
            neighbor = blank + delta_exception_one[action]
        else:
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


#----------------------------------------------------------------------
#QUESTION 3: HELPER FUNCTIONS 
def display_duck_puzzle(state):

    state=list(state)
    for i in range (0,9):
        if state[i]==0:
            state[i]="*"
    empty_space=' '
    
    print(state[0], state[1])
    print(state[2],state[3], state[4], state[5])
    print(empty_space, state[6], state[7], state[8])

def make_rand_duck_puzzle():

    #Any solvable state can be reached from the goal state by some sequence of legal moves.
    goal_state=(1, 2, 3, 4, 5, 6, 7 ,8, 0)
    DuckPuzzle_=DuckPuzzle(initial=goal_state)

    random_state = list(goal_state)
    
    
    #num of tiles moved = path cost, take from 8puzzle.
    num_of_tiles_moved = random.randint(1,100000)

    for x in range(num_of_tiles_moved):
        possible_moves = DuckPuzzle_.actions(random_state)
        move = random.choice(possible_moves)
        # print('possible moves = ', possible_moves)
        # print('move = ', move , '\n')
        random_state = DuckPuzzle_.result(random_state, move)

    return random_state

#----------------------------------------------------------------------
#QUESTION 3: Manhattan-distance_heuristic for duck puzzle
def Duckpuzzle_manhattan_distance_heuristic(node):
    state = node.state
    goal_state=[1, 2, 3, 4 ,5, 6, 7, 8, 0]
    coordinate=((0,0), (1,0), (0,1), (1,1), (2,1), (3,1), (1,2), (2,2), (3,2))


    dx=0
    dy=0
    _sum=0
    x = 0
    y = 1
    for i in range(len(state)):
        if state[i] == 0:
            continue

        state_value = state[i]

        state_x = coordinate[i][x]
        goal_x = coordinate[goal_state.index(state_value)][x]

        state_y = coordinate[i][y]
        goal_y = coordinate[goal_state.index(state_value)][y]

        dx = abs(state_x-goal_x)
        dy = abs(state_y-goal_y)

        _sum = _sum + dx + dy

    return(_sum)
#------------------------------------------------------------------------

#----------------------------------------------------------------------
#QUESTION 2.2: Manhattan-distance_heuristic 

def EightPuzzle_manhattan_distance_heuristic(node):
    state = node.state
    goal_state=[1, 2, 3, 4 ,5, 6, 7, 8, 0]
    
    dx=0
    dy=0
    _sum=0
    for i in range(len(state)):
        if state[i] == 0:
            continue

        state_x = i%3
        goal_x = (goal_state.index(state[i]))%3
        state_y = i//3
        goal_y = (goal_state.index(state[i]))//3

        dx = abs(state_x-goal_x)
        dy = abs(state_y-goal_y)

        _sum = _sum + dx + dy


    
    return(_sum)

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#QUESTION 2.3: Max_heuristic 
def MaxHeuristic(node, DuckPuzzle_= False):

    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    Misplaced_tiles_Heuristic = sum(s != g for (s, g) in zip(node.state, goal))
    if DuckPuzzle_ == True:
        Manhattan_distance_heuristic = Duckpuzzle_manhattan_distance_heuristic(node)
    else:
        Manhattan_distance_heuristic = EightPuzzle_manhattan_distance_heuristic(node)

    return max(Misplaced_tiles_Heuristic, Manhattan_distance_heuristic)


#----------------------------------------------------------------------

def a1_best_first_graph_search(problem, f, display=False):
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
    pop_count = 0
    while frontier:
        node = frontier.pop()
        pop_count = pop_count + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return (node, pop_count)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def a1_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return a1_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


#------------------------------------------------------------------------
#QUESTION 1: HELPER FUNCTIONS 
def display_eight_puzzle(state):

    state=list(state)
    for i in range (0,9):
        if state[i]==0:
            state[i]="*"
    
    print(state[0], state[1], state[2])
    print(state[3], state[4], state[5])
    print(state[6], state[7], state[8])

def make_rand_8puzzle():
    
    initial_state = []
    random_state = []
    available_nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    while len(available_nums) != 0:
        num = random.choice(available_nums)
        random_state.append(num)
        available_nums.remove(num)


    solvability = False
    random_state = tuple(random_state)
    EightPuzzle_object = EightPuzzle(initial=random_state)

    while solvability == False:       

        if EightPuzzle_object.check_solvability(random_state):
            solvability = True
            initial_state = random_state
            break
        # print("solvability = ",  solvability)
        random_state = []
        available_nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        
        while len(available_nums) != 0:
            num = random.choice(available_nums)
            random_state.append(num)
            available_nums.remove(num)

        random_state = tuple(random_state)
        EightPuzzle_object = EightPuzzle(initial=random_state)

    return initial_state

#------------------------------------------------------------------------

def Puzzle_Analysis(DuckPuzzle_= False):
    ten_random_puzzle = []
    Time =[]
    Path_cost = []
    Pop_count = []

    for x in range(10):
        
        print("-----", x+1, "----------")
        print("Random Solvable instance:")
        if DuckPuzzle_== True:
            ten_random_puzzle.append(make_rand_duck_puzzle())
            display_duck_puzzle(ten_random_puzzle[x])
            Puzzle_instance = DuckPuzzle(initial=ten_random_puzzle[x])
        else:
            ten_random_puzzle.append(make_rand_8puzzle())
            display_eight_puzzle(ten_random_puzzle[x])
            Puzzle_instance = EightPuzzle(initial=ten_random_puzzle[x])

        #Search Algorithm Using Misplaced Tiles Heuristic
        print("Search Algorithm Using Misplaced Tiles Heuristic:")
        if DuckPuzzle_== True:
            start=time.time()
            solved_state = a1_astar_search(Puzzle_instance)
            total_time=time.time() - start

        else:
            start=time.time()
            solved_state = a1_astar_search(Puzzle_instance)
            total_time=time.time() - start

        total_time = round(total_time, 5)
        pop_count = solved_state[1]
        solved_state = solved_state[0]


        print("Number of tiles moved = ", solved_state.path_cost)
        print("Time Taken to solve= ", total_time, " seconds")
        print("Pop_count =  ", pop_count)


        #Search Algorithm using Manhattan Distance Heuristic
        Node_object = Node(ten_random_puzzle[x])
        print("\nSearch Algorithm Using Manhattan Distance Heuristic:")
        if DuckPuzzle_== True:
            start=time.time()
            solved_state = a1_astar_search(Puzzle_instance, h=Duckpuzzle_manhattan_distance_heuristic)
            total_time=time.time() - start

        else:
            start=time.time()
            solved_state = a1_astar_search(Puzzle_instance, h=EightPuzzle_manhattan_distance_heuristic)
            total_time=time.time() - start

        total_time = round(total_time, 5)
        pop_count = solved_state[1]
        solved_state = solved_state[0]

        print("Number of tiles moved = ", solved_state.path_cost)
        print("Time Taken to solve= ", total_time, " seconds")
        print("Pop_count =  ", pop_count)


        #Search Algorithm using MaxHeuristic
        print("\nSearch Algorithm using MaxHeuristic:")
        if DuckPuzzle_== True:
            start=time.time()
            solved_state = a1_astar_search(Puzzle_instance, h=MaxHeuristic)
            total_time=time.time() - start

        else:
            start=time.time()
            solved_state = a1_astar_search(Puzzle_instance, h=MaxHeuristic)
            total_time=time.time() - start

        total_time = round(total_time, 5)
        pop_count = solved_state[1]
        solved_state = solved_state[0]


        print("Number of tiles moved = ", solved_state.path_cost)
        print("Time Taken to solve= ", total_time, " seconds")
        print("Pop_count =  ", pop_count)
        print("Solved state:")
        if DuckPuzzle_== True:
            display_duck_puzzle(solved_state.state)
        else:
            display_eight_puzzle(solved_state.state)
        print('\n')    


    
if __name__ == "__main__":

    Searching_Algorithm_Heuristic = ('Misplaced_Tiles', 'Manhattan_distance', 'MaxHeuristic')
    print("##########################")
    print("##                      ##")
    print("##     EightPuzzle      ##")
    print("##                      ##")
    print("##########################")

    Puzzle_Analysis(DuckPuzzle_ = False)

    print("##########################")
    print("##                      ##")
    print("##     DuckPuzzle       ##")
    print("##                      ##")
    print("##########################")

    Puzzle_Analysis(DuckPuzzle_ = True)




