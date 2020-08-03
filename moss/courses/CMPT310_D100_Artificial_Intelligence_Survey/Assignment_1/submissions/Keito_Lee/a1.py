# a1.py

from search import *
import random
import time


#function copied from search.py and added a cout_pop variable for counting the number of frontier.pop() calls
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
    count_pop = 0
    while frontier:
        node = frontier.pop()
        count_pop = count_pop + 1
        if problem.goal_test(node.state):
            if display:
                # print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                print("Nodes removed from frontier: ", count_pop)
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



#class copied over from search.py
#mahattan and max_hue methods were added for assignment
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

    #although this implementation of the missing tile heuristic includes counts for the 0 tile,
    #I am leaving it here and using the it as given by the textbook since my TA stated to
    #use the given implementation
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        state = node.state
        pos = { 1: [0,0], 2: [1,0], 3: [2,0], 4: [0,1], 5: [1,1], 6: [2,1], 7: [0,2], 8: [1,2], 9: [2,2] }
        count = 0

        for i in pos:
            curr_coord = pos.get(i)
            curr_tup_val = state[i-1]

            if curr_tup_val == 0:
                goal_coord = pos.get(9)
            else:
                goal_coord = pos.get(state[i-1])
            if state[i-1] != 0:
                count = count + ( abs(goal_coord[0] - curr_coord[0]) + abs(goal_coord[1] - curr_coord[1]) )

        return count

    def max_hue(self, node):
        man = self.manhattan(node)
        default = self.h(node)
        return max(man, default)



#class adapted from Eightpuzzle class in search.py altered for DuckPuzzle implementation
#mahattan and max_hue added by me 
class DuckPuzzle(Problem):
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

        # changed conditions for allowable actions to fit that of the duck puzzle
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # since the shape of the duck puzzle changes the position of the indexes relative to eachother,
        # I put a different set of actions for the smaller square in the top left and the larger square
        # in the bottom right. I put a specific set of instructions for just index 3 since it is part of
        # both squares giving it properties of both depending on going UP on DOWN.
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

    #removed check_solvability from the 8-puzzle class since it is not usable for the duck puzzle

    #although this implementation of the missing tile heuristic includes counts for the 0 tile,
    #I am leaving it here and using the it as given by the textbook since my TA stated to
    #use the given implementation
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    #same logic as the eight puzzle but changed the coordinates
    def manhattan(self, node):
        state = node.state
        pos = { 1: [0,0], 2: [1,0], 3: [0,1], 4: [1,1], 5: [2,1], 6: [3,1], 7: [1,2], 8: [2,2], 9: [3,2] }
        count = 0

        for i in pos:
            curr_coord = pos.get(i)
            curr_tup_val = state[i-1]

            if curr_tup_val == 0:
                goal_coord = pos.get(9)
            else:
                goal_coord = pos.get(state[i-1])
            if state[i-1] != 0:
                count = count + ( abs(goal_coord[0] - curr_coord[0]) + abs(goal_coord[1] - curr_coord[1]) )

        return count

    def max_hue(self, node):
        man = self.manhattan(node)
        default = self.h(node)

        return max(man, default)



#print each value of tuple at each index. After every third index start on a newline
def display(state):
    for i in range(len(state)):
        if ( (i == 2) or (i == 5) or (i == 8) ):
            if ( state[i] == 0 ):
                print("*", " ")
            else:
                print(state[i], " ")
        else:
            if ( state[i] == 0 ):
                print("*", " ", end = '')
            else:
                print(state[i], " ", end = '')

                

#using python random shuffle function to shuffle list with 9 elements 0 to 9. Then use check_solvability to see if random 
#list turned into tuple is solvable and if so, return a new instance of eight puzzle with that tuple
def make_rand_8puzzle():
    newlist = [0,1,2,3,4,5,6,7,8]
    res = False
    while res != True:
        random.shuffle(newlist)
        newtup = tuple(newlist)
        puzz = EightPuzzle(newtup)
        res = puzz.check_solvability(newtup) 
    display(newtup)
    return puzz



#same logic as eight puzzle but altered for duck puzzle
def display_duck_puzzle(state):
    for i in range(len(state)):
        if ( (i == 1) or (i == 5) or (i == 8) ):
            if ( state[i] == 0 ):
                print("*", " ")
            else:
                print(state[i], " ")
        elif (i == 6):
            if ( state[i] == 0 ):
                print("  ", "*", " ", end = '')
            else:
                print("  ", state[i], " ", end = '') 
        else:
            if ( state[i] == 0 ):
                print("*", " ", end = '')
            else:
                print(state[i], " ", end = '')    



#makes an instance of duck puzzle with a random starting state by starting at goal state and doing legal moves
def make_rand_duckpuzzle():

    #initialize instance of Duck Puzzle with goal state as the initial state
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzz = DuckPuzzle(state)
    last_move = None

    #make a random number of moves between 10 and 150
    for i in range(random.randint(10, 150)):
        pos_actions = puzz.actions(state)
        check = 0

        #loops until a move that is legal and not the opposite as the move made previously is found
        #if previous move is left then moving right will put in back in original position so eliminate right as option
        while check == 0:
            index = random.randint(0, len(pos_actions)-1)
            if last_move == None:
                check = 1
            elif last_move == 'UP':
                if pos_actions[index] != 'DOWN':
                    check = 1
            elif last_move == 'DOWN':
                if pos_actions[index] != 'UP':
                    check = 1
            elif last_move == 'LEFT':
                if pos_actions[index] != 'RIGHT':
                    check = 1
            elif last_move == 'RIGHT':
                if pos_actions[index] != 'LEFT':
                    check = 1

        #use result method to move tile according to move chosen and update last_move
        new_state = puzz.result(state, pos_actions[index])
        state = new_state
        last_move = pos_actions[index]

    #display final state and update puzz with new state    
    display_duck_puzzle(state)
    puzz = DuckPuzzle(state)

    return puzz



print("Eight Puzzle Results:")

for i in range(10):

    print("Eight Puzzle #", i+1)
    print(" ")
    eightpuzzle = make_rand_8puzzle()
    print(" ")

    print("Missing Tile")

    start_time1 = time.time()

    sol1 = astar_search(eightpuzzle, display=True)

    elapsed_time1 = time.time() - start_time1

    print(f'Total elapsed time (in seconds): {elapsed_time1}s')
    print("Number of tiles moved: ", len(sol1.path()) - 1)
    print(" ")


    print("Manhattan")

    start_time2 = time.time()

    sol2 = astar_search(eightpuzzle, eightpuzzle.manhattan, display=True)

    elapsed_time2 = time.time() - start_time2

    print(f'Total elapsed time (in seconds): {elapsed_time2}s')
    print("Number of tiles moved: ", len(sol2.path()) - 1)
    print(" ")


    print("Maximum")

    start_time3 = time.time()

    sol3 = astar_search(eightpuzzle, eightpuzzle.max_hue, display=True)

    elapsed_time3 = time.time() - start_time3

    print(f'Total elapsed time (in seconds): {elapsed_time3}s')
    print("Number of tiles moved: ", len(sol3.path()) - 1)
    print(" ")

# #______________________________________________________________________________________

print("\n")

print("Duck Puzzle Results:")

for i in range(10):    

    print("Duck Puzzle #", i+1)
    print(" ")
    duckpuzzle = make_rand_duckpuzzle()
    print(" ")

    print("Missing Tile")

    start_time1 = time.time()

    sol1 = astar_search(duckpuzzle, display=True)

    elapsed_time1 = time.time() - start_time1

    print(f'Total elapsed time (in seconds): {elapsed_time1}s')
    print("Number of tiles moved: ", len(sol1.path()) - 1)
    print(" ")


    print("Manhattan")

    start_time2 = time.time()

    sol2 = astar_search(duckpuzzle, duckpuzzle.manhattan, display=True)

    elapsed_time2 = time.time() - start_time2

    print(f'Total elapsed time (in seconds): {elapsed_time2}s')
    print("Number of tiles moved: ", len(sol2.path()) - 1)
    print(" ")


    print("Maximum")

    start_time3 = time.time()

    sol3 = astar_search(duckpuzzle, duckpuzzle.max_hue, display=True)

    elapsed_time3 = time.time() - start_time3

    print(f'Total elapsed time (in seconds): {elapsed_time3}s')
    print("Number of tiles moved: ", len(sol3.path()) - 1)
    print(" ")

