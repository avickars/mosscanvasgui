from search import *
import math
import time
import random

#This is the code Directly Copied from search.py
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

#This code is also directly copied from search.py but I added a variable to count
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
    #this number_pop is used to count how many times the frontier pop the node
    number_pop = 0
    while frontier:

        node = frontier.pop()
        number_pop += 1
        #When ever frontier calls pop, number increment by 1
        if problem.goal_test(node.state):
            if display:
                print("There are :", number_pop,  "nodes there were removed from frontier" )
                #print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
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


#Question 1: Helper Functions

def make_rand_8puzzle():
    initial = [1,2,3,4,5,6,7,8,0]
    #many thanks to my friend John since he told me there is a shuffle function
    #shuffle randomly change the order of the puzzle
    random.shuffle(initial)
    new_puzzle = EightPuzzle(tuple(initial))
    #While the puzzle is not sovable
    while not new_puzzle.check_solvability(initial):
        #shuffle the puzzle again until it is sovable
        random.shuffle(initial)
    #create the object and return it
    new_puzzle = EightPuzzle(tuple(initial))
    return new_puzzle

#This display function is for the EightPuzzle but not for the HousePuzzle
def display(state):
    first_row =[]
    second_row=[]
    third_row=[]
    blank_position = state.index(0)
    for itr in range (0,3):
        if (itr != blank_position):
            first_row.append(state[itr])
        else:
            first_row.append("*")
    for itr in range (3,6):
        if (itr != blank_position):
            second_row.append(state[itr])
        else:
            second_row.append("*")
    for itr in range (6,9):
        if (itr != blank_position):
            third_row.append(state[itr])
        else:
            third_row.append("*")

    print(first_row[0],first_row[1],first_row[2])
    print(second_row[0],second_row[1],second_row[2])
    print(third_row[0],third_row[1],third_row[2])

#Qustion 2: Comparing Algorithms
#This misplaced tile function is for both EightPuzzle and HousePuzzle since their goal is exactly the same
def misplaced_tile_heuristic (node):
    #Let the variable puzzle to be the current state of the node
    puzzle=node.state
    #initialize the h_value we need
    h_value = 0
    #Since 0 is at the last space of the tuple(list), we first need to check if 1 is at the position 0 and so on
    for x in range (1, 9):
        if (puzzle[x-1] != x):
            h_value += 1
    # 0 is not checked in the for loop, so if 0 is not at the last position, increase the h_value by 1
    if (puzzle[8] != 0):
        h_value += 1
    return h_value

#This Manhattan distance function is only for EightPuzzle
def Manhattan_distance_heuristic(node):
    #since we are not allowed to use the function that is provided, I used a really stupid to figure out the Manhattan Distance
    #I did all the math job on the paper and simply those if statements can figure out the h_value
    puzzle = node.state
    h_value = 0
    position_0 = puzzle.index(0)
    position_1 = puzzle.index(1)
    position_2 = puzzle.index(2)
    position_3 = puzzle.index(3)
    position_4 = puzzle.index(4)
    position_5 = puzzle.index(5)
    position_6 = puzzle.index(6)
    position_7 = puzzle.index(7)
    position_8 = puzzle.index(8)

    if (position_1 == 0):
        h_value += 0
    if (position_1 == 1 or position_1 == 3):
        h_value += 1
    if (position_1 == 2 or position_1 == 4 or position_1 == 6):
        h_value += 2
    if (position_1 == 5 or position_1 == 7):
        h_value += 3
    if (position_1 == 8):
        h_value += 4

    if (position_2 == 1):
        h_value += 0
    if (position_2 == 0 or position_2 == 2 or position_2 == 4):
        h_value += 1
    if (position_2 == 3 or position_2 == 5 or position_2 == 7):
        h_value += 2
    if (position_2 == 6 or position_2 == 8):
        h_value += 3

    if (position_3 == 2):
        h_value += 0
    if (position_3 == 1 or position_3 == 5):
        h_value += 1
    if (position_3 == 0 or position_3 == 4 or position_3 == 8):
        h_value += 2
    if (position_3 == 3 or position_3 == 7):
        h_value += 3
    if (position_3 == 6):
        h_value += 4

    if (position_4 == 3):
        h_value += 0
    if (position_4 == 0 or position_4 == 4 or position_4 == 6):
        h_value += 1
    if (position_4 == 1 or position_4 == 5 or position_4 == 7):
        h_value += 2
    if (position_4 == 2 or position_4 == 8):
        h_value += 3

    if (position_5 == 4):
        h_value += 0
    if (position_5 == 1 or position_5 == 3 or position_5 == 5 or position_5 == 7):
        h_value += 1
    if (position_5 == 0 or position_5 == 2 or position_5 == 6 or position_5 == 8):
        h_value += 2

    if (position_6 == 5):
        h_value += 0
    if (position_6 == 2 or position_6 == 4 or position_6 == 8):
        h_value += 1
    if (position_6 == 1 or position_6 == 3 or position_6 == 7):
        h_value += 2
    if (position_6 == 0 or position_6 == 6):
        h_value += 3

    if (position_7 == 6):
        h_value += 0
    if (position_7 == 3 or position_7 == 7):
        h_value += 1
    if (position_7 == 0 or position_7 == 4 or position_7 == 8):
        h_value += 2
    if (position_7 == 1 or position_7 == 5):
        h_value += 3
    if (position_7 == 2):
        h_value += 4

    if (position_8 == 7):
        h_value += 0
    if (position_8 == 4 or position_8 == 6 or position_8 == 8):
        h_value += 1
    if (position_8 == 1 or position_8 == 3 or position_8 == 5):
        h_value += 2
    if (position_8 == 0 or position_8 == 2):
        h_value += 3

    if (position_0 == 8):
        h_value += 0
    if (position_0 == 5 or position_0 == 7):
        h_value += 1
    if (position_0 == 2 or position_0 == 4 or position_0 == 6):
        h_value += 2
    if (position_0 == 1 or position_0 == 3):
        h_value += 3
    if (position_0 == 0):
        h_value += 4

    return h_value

#This function is simple since it just call the two functions that is written and replace the bigger value of those two
def Max_of_Manhattan_and_Misplaced_tile (node):
    h_mis = misplaced_tile_heuristic(node)
    h_man = Manhattan_distance_heuristic(node)
    return max(h_mis,h_man)


#Question 3 The House-Puzzle

#This DuckPuzzle class basically inherit from EightPuzzle, I basically modified the functions in the EightPuzzle
class DuckPuzzle (EightPuzzle):
    #Since the shape of the puzzle is defferent, the actions that apply to the puzzle is changed as well
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """
        #I did all the math job on my paper, so basically it will still work as in the EightPuzzle
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        if index_blank_square == 1:
            possible_actions.remove('UP')
            possible_actions.remove("RIGHT")
        if index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 6:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')

        return possible_actions

    #I modified the function so this result function works for the House Puzzle
    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)
        if (blank == 0):
            if (action == 'RIGHT'):
                new_state[0], new_state[1] = new_state[1], new_state[0]
            if (action == 'DOWN'):
                new_state[0], new_state[2] = new_state[2], new_state[0]
        if (blank == 1):
            if (action == 'LEFT'):
                new_state[1], new_state[0] = new_state[0], new_state[1]
            if (action == 'DOWN'):
                new_state[1], new_state[3] = new_state[3], new_state[1]
        if (blank == 2):
            if (action == 'UP'):
                new_state[2], new_state[0] = new_state[0], new_state[2]
            if (action == 'RIGHT'):
                new_state[2], new_state[3] = new_state[3], new_state[2]
        if (blank == 3):
            if (action == 'UP'):
                new_state[3], new_state[1] = new_state[1], new_state[3]
            if (action == 'DOWN'):
                new_state[3], new_state[6] = new_state[6], new_state[3]
            if (action == 'LEFT'):
                new_state[3], new_state[2] = new_state[2], new_state[3]
            if (action == 'RIGHT'):
                new_state[3], new_state[4] = new_state[4], new_state[3]
        if (blank == 4):
            if (action == 'DOWN'):
                new_state[4], new_state[7] = new_state[7], new_state[4]
            if (action == 'LEFT'):
                new_state[4], new_state[3] = new_state[3], new_state[4]
            if (action == 'RIGHT'):
                new_state[4], new_state[5] = new_state[5], new_state[4]
        if (blank == 5):
            if (action == 'DOWN'):
                new_state[5], new_state[8] = new_state[8], new_state[5]
            if (action == 'LEFT'):
                new_state[5], new_state[4] = new_state[4], new_state[5]
        if (blank == 6):
            if (action == 'UP'):
                new_state[6], new_state[3] = new_state[3], new_state[6]
            if (action == 'RIGHT'):
                new_state[6], new_state[7] = new_state[7], new_state[6]
        if (blank == 7):
            if (action == 'UP'):
                new_state[7], new_state[4] = new_state[4], new_state[7]
            if (action == 'LEFT'):
                new_state[7], new_state[6] = new_state[6], new_state[7]
            if (action == 'RIGHT'):
                new_state[7], new_state[8] = new_state[8], new_state[7]
        if (blank == 8):
            if (action == 'UP'):
                new_state[8], new_state[5] = new_state[5], new_state[8]
            if (action == 'LEFT'):
                new_state[8], new_state[7] = new_state[7], new_state[8]

        return tuple(new_state)

#The Manhattan distance for the House Puzzle is different from the EightPuzzle
#I modified the fucntion, again I did all the math on the paper.
def Manhattan_distance_heuristic_Duck(node):
    puzzle = node.state
    h_value = 0
    position_0 = puzzle.index(0)
    position_1 = puzzle.index(1)
    position_2 = puzzle.index(2)
    position_3 = puzzle.index(3)
    position_4 = puzzle.index(4)
    position_5 = puzzle.index(5)
    position_6 = puzzle.index(6)
    position_7 = puzzle.index(7)
    position_8 = puzzle.index(8)

    if (position_1 == 0):
        h_value += 0
    if (position_1 == 1 or position_1 == 2):
        h_value += 1
    if (position_1 == 3):
        h_value += 2
    if (position_1 == 4 or position_1 == 6):
        h_value += 3
    if (position_1 == 5 or position_1 == 7):
        h_value += 4
    if (position_1 == 8):
        h_value += 5

    if (position_2 == 1):
        h_value += 0
    if (position_2 == 0 or position_2 == 3):
        h_value += 1
    if (position_2 == 2 or position_2 == 4 or position_2 == 6):
        h_value += 2
    if (position_2 == 5 or position_2 == 7):
        h_value += 3
    if (position_2 == 8):
        h_value += 4

    if (position_3 == 2):
        h_value += 0
    if (position_3 == 0 or position_3 == 3):
        h_value += 1
    if (position_3 == 1 or position_3 == 4 or position_3 == 6):
        h_value += 2
    if (position_3 == 5 or position_3 == 7):
        h_value += 3
    if (position_3 == 8):
        h_value += 4

    if (position_4 == 3):
        h_value += 0
    if (position_4 == 1 or position_4 ==2 or position_4 == 4 or position_4 == 6):
        h_value += 1
    if (position_4 == 0 or position_4 == 5 or position_4 == 7):
        h_value += 2
    if (position_4 == 8):
        h_value += 3

    if (position_5 == 4):
        h_value += 0
    if (position_5 == 3 or position_5 == 5 or position_5 == 7):
        h_value += 1
    if (position_5 == 1 or position_5 == 2 or position_5 == 6 or position_5 == 8):
        h_value += 2
    if (position_5 == 0):
        h_value += 3

    if (position_6 == 5):
        h_value += 0
    if (position_6 == 4 or position_6 == 8):
        h_value += 1
    if (position_6 == 3 or position_6 == 7):
        h_value += 2
    if (position_6 == 1 or position_6 == 2 or position_6 == 6):
        h_value += 3
    if (position_6 == 0):
        h_value += 4

    if (position_7 == 6):
        h_value += 0
    if (position_7 == 3 or position_7 == 7):
        h_value += 1
    if (position_7 == 1 or position_7 == 2 or position_7 == 4 or position_7 == 8):
        h_value += 2
    if (position_7 == 0 or position_7 == 5):
        h_value += 3

    if (position_8 == 7):
        h_value += 0
    if (position_8 == 4 or position_8 == 6 or position_8 == 8):
        h_value += 1
    if (position_8 == 3 or position_8 == 5):
        h_value += 2
    if (position_8 == 1 or position_8 == 2):
        h_value += 3
    if (position_8 == 0):
        h_value += 4

    if (position_0 == 8):
        h_value += 0
    if (position_0 == 5 or position_0 == 7):
        h_value += 1
    if (position_0 == 4 or position_0 == 6):
        h_value += 2
    if (position_0 == 3):
        h_value += 3
    if (position_0 == 1 or position_0 == 2):
        h_value += 4
    if (position_0 == 0):
        h_value += 5
    return h_value

#This max function is basically the same as before, it is just that the Manhattan distances needs to call the right one to calculate
def Max_of_Manhattan_and_Misplaced_tile_Duck (node):
    h_mis = misplaced_tile_heuristic(node)
    h_man = Manhattan_distance_heuristic_Duck(node)
    return max(h_mis,h_man)

#The display function is also modified for the House Puzzle
def display_Duck(state):
    first_row =[]
    second_row=[]
    third_row=[]
    third_row.append(' ')
    blank_position = state.index(0)
    for itr in range (0,2):
        if (itr != blank_position):
            first_row.append(state[itr])
        else:
            first_row.append("*")
    for itr in range (2,6):
        if (itr != blank_position):
            second_row.append(state[itr])
        else:
            second_row.append("*")
    for itr in range (6,9):
        if (itr != blank_position):
            third_row.append(state[itr])
        else:
            third_row.append("*")

    print(first_row[0],first_row[1])
    print(second_row[0],second_row[1],second_row[2],second_row[3])
    print(third_row[0],third_row[1],third_row[2],third_row[3])

#This function will generate a sovable duck puzzle to run
#This check_sovability function is contained in this generate function
def make_rand_Duck_puzzle():
    initial = [1,2,3,4,5,6,7,8,0]
    new_puzzle = DuckPuzzle(tuple(initial))
    for i in range (random.randint(1000,2000)):
        possible_actions = new_puzzle.actions(initial)
        x = random.randint(0, len(possible_actions)-1)
        initial = new_puzzle.result(initial, possible_actions[x])
    Duck = DuckPuzzle(tuple(initial))

    return Duck


#This is calling functions Question 2
print("Start showing Question 2!")
print(" ")
for x in range(10):
    print("This is the loop #",x+1,".")
    puzzle = make_rand_8puzzle()
    display(puzzle.initial)

    print("Using Misplaced Tile Heuristic")
    start_time = time.time()
    result = astar_search(puzzle, h=misplaced_tile_heuristic, display=True).solution()
    elapsed_time = time.time() - start_time
    print("The length of the path is :" ,len(result), " steps")
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("\n")

    print("Using Manhattan Distance Heuristic")
    start_time = time.time()
    result = astar_search(puzzle, h=Manhattan_distance_heuristic, display=True).solution()
    elapsed_time = time.time() - start_time
    print("The length of the path is :" ,len(result), " steps")
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("\n")

    print("Using Max of Misplaced Tile and Manhattan Distance")
    start_time = time.time()
    result = astar_search(puzzle, h=Max_of_Manhattan_and_Misplaced_tile, display=True).solution()
    elapsed_time = time.time() - start_time
    print("The length of the path is :" ,len(result), " steps")
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("\n")
    print("############################################")

#This is calling functions Question 3
#Start showing Question 3
print("Start showing Question 3!")
print(" ")
for x in range (10):
    print("This is the loop #", x+1)
    puzzle = make_rand_Duck_puzzle()
    display_Duck(puzzle.initial)
 
    print("Using Misplaced Tile Heuristic")
    start_time = time.time()
    result = astar_search(puzzle, h=misplaced_tile_heuristic, display=True).solution()
    elapsed_time = time.time() - start_time
    print("The length of the path is :" ,len(result), " steps")
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("\n")

    print("Using Manhattan Distance Heuristic")
    start_time = time.time()
    result = astar_search(puzzle, h=Manhattan_distance_heuristic_Duck, display=True).solution()
    elapsed_time = time.time() - start_time
    print("The length of the path is :" ,len(result), " steps")
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("\n")

    print("Using Max of Misplaced Tile and Manhattan Distance")
    start_time = time.time()
    result = astar_search(puzzle, h=Max_of_Manhattan_and_Misplaced_tile_Duck, display=True).solution()
    elapsed_time = time.time() - start_time
    print("The length of the path is :" ,len(result), " steps")
    print(f'elapsed time (in seconds): {elapsed_time}s')
    print("\n")
    print("############################################")
