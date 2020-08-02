# a1.py

# Assignment 1
# Langjia Wu 301387029

# some reference:

# wiki for Manhattan distance: https://zh.wikipedia.org/wiki/%E6%9B%BC%E5%93%88%E9%A0%93%E8%B7%9D%E9%9B%A2
# python documentation on 3.8.3:  https://docs.python.org/3/
# udemy python course: https://www.udemy.com/course/complete-python-bootcamp/learn
# Tutorial code from Mahmoud TA group: tutorial1.py and tutorial2.py

'''
Contents

Imports

best_first_graph_search_new -->> for giving back a frontier removal node count
astar_search_new -->> matching the best_first search
EightPuzzle_New -->> for changing the h() ignore 0 tiles

Q1
make_rand_8puzzle -->> for Eight Puzzle, generating a random state and also check_solvability
display -->> for Eight Puzzle displaying

Q2
manhattan_h -->> normal manhattan method for Eight Puzzle
manhattan_max_h -->> Max() method for Eight Puzzle

Q3
DuckPuzzle -->> Base on Eight Puzzle, changed implementation on actions() result() and h()
make_rand_duckpuzzle -->> unlike Eight Puzzle, since we could not prove if it is solvable by random generate, I use goal state the random move tile to create puzzle
duke_display -->> displaying Duck Puzzle

manhattan_h_duck -->> Manhattan Method for duck puzzle
manhattan_max_h_duck -->> Max method for duck puzzle


test code to generata data -->> creating for loops for both Eight and Duck puzzle, give back each puzzle image, frontier node removal, time, cost and print a short summary in the
    end, more information check a1.xlsx
'''


# This import is from tutorial 1, to locate my aima-python on windows
import sys
sys.path.insert(0, 'E:\\CMPT310\\aima-python')
from search import *

# some library I needed for time tracking and creating random puzzle state
import time
import random
from random import randint

# the following are copy code from search.py, but have renamed and some more edition
# In order to keep track on frontier removal
# both will be rename as: *****_new()
# In this assignment all the A* calling will be using these methods locally

# In this case since requirement said "node removed from frontier", I would consider
# the deletion and append is just putting a node to the back of frontier, but not "removed"
# The EightPuzzle_New is exact same as the original one , only change is made on h()
# added the case that ignore the 0 tile


# only changed to give back a node removal counter
def best_first_graph_search_new(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    # this is the addition count for frontier
    frontier_removal_count = 0

    while frontier:
        node = frontier.pop()

        #counter need to plus 1
        frontier_removal_count += 1

        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")

            #give back the counter
            print('the current method is having node removed as counted {} times'.format(frontier_removal_count))

            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    #give back the counter for data collection
    print('the current method is having node removed as counted {} times'.format(frontier_removal_count))
    return None

# only renaming for matching the best_first_graph_search_new
def astar_search_new(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_new(problem, lambda n: n.path_cost + h(n), display)


class EightPuzzle_New(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
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
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def check_solvability(self, state):
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1
        return inversion % 2 == 0

    def h(self, node):
        # ignore 0 tile
        return sum(s != 0 and s != g for (s, g) in zip(node.state, self.goal))

# Question 1

# this method will generate a puzzle and make sure it is solvable
def make_rand_8puzzle() -> EightPuzzle_New:
    # newstate=(1, 2, 3, 4, 5, 6, 8, 7, 0)  # this is insolvable  7 and 8 swapped
    newstate=(1, 2, 3, 4, 5, 6, 7, 8, 0)  # this is same as goal
    goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    newPuzzle = EightPuzzle_New(newstate, goal)

    # make sure the list is shuffled(randomly generated)
    mylist = list(newPuzzle.initial)
    random.shuffle(mylist)
    newPuzzle.initial = tuple(mylist)

    # check for solvability, if not solvable, re-shuffle until solvable
    while not newPuzzle.check_solvability(newPuzzle.initial):
        mylist = list(newPuzzle.initial)
        random.shuffle(mylist)
        newPuzzle.initial = tuple(mylist)
    return newPuzzle

# this method will show the state in 8 puzzle way
def display(state):
    # print in 2D
    for x in range(3):
        for y in range(3):
            if(state[3 * x + y] == 0):
                print('*', end = ' ')
            else:
                print(state[3 * x + y], end = ' ')
        print() # line change
    print()


# Question 2

# this is the manhattan method for 8 puzzle
def manhattan_h(Problem, node):
    """ This is the Manhattan distance heuristic method, using |xi-xj| + |yi-yj|
    using 1 2 3 for cols and rows calculation

    using number on calculation as index + 1:
    1 2 3
    4 5 6
    7 8 9
    Note: we need to ignore 0 tile since it is empty.
    """
    # getting all position's manhattan
    sum = 0
    count = 0 # count is acting as index of state
    for s in node.state:
        if s == 0: # skip 0 tile
            count += 1
            continue
        # evaluate the current slot x and y
        current_position = count + 1  # using number from 1 - 9
        # for x
        if current_position % 3 == 0: # for all 3 tiles on right -> 3 6 9
            current_x = 3
        else:
            current_x = current_position % 3
        # for y
        if current_position < 4:
            current_y = 1
        elif current_position > 6:
            current_y = 3
        else:
            current_y = 2
        count += 1

        # evaluate the tile original position x and y
        # for y
        if s < 4:
            y1 = 1
        elif s > 6:
            y1 = 3
        else:
            y1 = 2
        # for x
        if s % 3 == 0:
            x1 = 3
        else:
            x1 = s % 3
        # manhattan calculation
        sum += abs(current_x - x1) + abs(current_y - y1)
    return sum

def manhattan_max_h(Problem, node):
    """ This is returning the max of the Manhattan distance heuristic and the misplace method
    """
    sum = 0
    count = 0 # count is acting as index of state
    for s in node.state:
        if s == 0: # skip 0 tile
            count += 1
            continue
        # evaluate the current slot x and y
        current_position = count + 1  # using number from 1 - 9
        # for x
        if current_position % 3 == 0: # for all 3 tiles on right -> 3 6 9
            current_x = 3
        else:
            current_x = current_position % 3
        # for y
        if current_position < 4:
            current_y = 1
        elif current_position > 6:
            current_y = 3
        else:
            current_y = 2
        count += 1

        # evaluate the tile original position x and y
        # for y
        if s < 4:
            y1 = 1
        elif s > 6:
            y1 = 3
        else:
            y1 = 2
        # for x
        if s % 3 == 0:
            x1 = 3
        else:
            x1 = s % 3
        # manhattan calculation
        sum += abs(current_x - x1) + abs(current_y - y1)

    # in here use max to compare manhattan and displace
    return max(sum, Problem.h(node) )

# Question 3

# this is the duck puzzle class used for testing, actions and result has been rewrite
class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    # changed, since action should be different
    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        # hard coded since the shape is different
        if index_blank_square in [0, 2, 6]:
            possible_actions.remove('LEFT')
        if index_blank_square in [0, 1, 4, 5]:
            possible_actions.remove('UP')
        if index_blank_square in[1, 5, 8]:
            possible_actions.remove('RIGHT')
        if index_blank_square in [2, 6, 7, 8]:
            possible_actions.remove('DOWN')
        return possible_actions


    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)
        #delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        # hard coded, some impossible move has been set to 999
        if blank == 0:
            delta = {'UP': 999, 'DOWN': 2, 'LEFT': 999, 'RIGHT': 1}
        elif blank == 1:
            delta = {'UP': 999, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 999}
        elif blank == 2:
            delta = {'UP': -2, 'DOWN': 999, 'LEFT': 999, 'RIGHT': 1}
        elif blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 4:
            delta = {'UP': 999, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 5:
            delta = {'UP': 999, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 999}
        elif blank == 6:
            delta = {'UP': -3, 'DOWN': 999, 'LEFT': 999, 'RIGHT': 1}
        elif blank == 7:
            delta = {'UP': -3, 'DOWN': 999, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 999, 'LEFT': -1, 'RIGHT': 999}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def check_solvability(self, state):
        # no need to care this since the duck is generate as random move from goal state
        return True

    def h(self, node):
        #return sum(s != g for (s, g) in zip(node.state, self.goal))
        return sum(s != 0 and s != g for (s, g) in zip(node.state, self.goal))

# this is the method for random moving from a goal state
def make_rand_duckpuzzle() -> DuckPuzzle :
    Maxmove = 999999
    newstate=(1, 2, 3, 4, 5, 6, 7, 8, 0)  # this is same as goal
    goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    myDuckPuzzle = DuckPuzzle(newstate, goal)
    for i in range(Maxmove):
        # take all possible choice, then use % to select one
        possible_action = myDuckPuzzle.actions(myDuckPuzzle.initial)
        move_choice = randint(0,99) % len(possible_action)
        myDuckPuzzle.initial = myDuckPuzzle.result(myDuckPuzzle.initial, possible_action[move_choice])
    return myDuckPuzzle

# this is a hard coded for duck puzzle display
def duke_display(state):
    # print as duck
    mylist = list(state)
    for i in mylist:
        if i == 0:
            mylist[i] = '*'
    print(mylist[0], end=' ')
    print(mylist[1], end='\n')
    print(mylist[2], end=' ')
    print(mylist[3], end=' ')
    print(mylist[4], end=' ')
    print(mylist[5], end='\n  ')
    print(mylist[6], end=' ')
    print(mylist[7], end=' ')
    print(mylist[8], end='\n')

# note: for duck puzzle we should handle some different manhattan method since the shape is changed
def manhattan_h_duck(Problem, node):
    """ This is the Manhattan distance heuristic method, using |xi-xj| + |yi-yj|
    in this case, still using count as our index handler
    """
    # getting all position's manhattan
    sum = 0
    count = 0 # count is acting as index of state
    for s in node.state:
        if s == 0: # skip 0 tile
            count += 1
            continue
        # evaluate the current slot x and y
        current_position = count + 1  # using number from 1 - 9,
        #this should be same as s value if  tile is located correctly

        if s == current_position: # skip those correct tiles
            count += 1
            continue
        # for x
        if current_position in [1, 3]:
            current_x = 1
        elif current_position in [2, 4, 7]:
            current_x = 2
        elif current_position in [5, 8]:
            current_x = 3
        else:    # 6
            current_x = 4

        # for y
        if current_position in [1, 2]:
            current_y = 1
        elif current_position in [3, 4, 5, 6]:
            current_y = 2
        else: # 7 or 8
            current_y = 3
        count += 1

        # evaluate the tile original position x and y
        # for x
        if s in [1, 3]:
            x1 = 1
        elif s in [2, 4, 7]:
            x1 = 2
        elif s in [5, 8]:
            x1 = 3
        else:    # 6
            x1 = 4

        # for y
        if s in [1, 2]:
            y1 = 1
        elif s in [3, 4, 5, 6]:
            y1 = 2
        else: # 7 or 8
            y1 = 3
        # manhattan calculation
        sum += abs(current_x - x1) + abs(current_y - y1)
    #print('the current duck sum is {}'.format(sum))
    return sum

def manhattan_max_h_duck(Problem, node):
    """ This is returning the max of the Manhattan distance heuristic and the misplace method
    """
    # getting all position's manhattan
    sum = 0
    count = 0 # count is acting as index of state
    for s in node.state:
        if s == 0: # skip 0 tile
            count += 1
            continue
        # evaluate the current slot x and y
        current_position = count + 1  # using number from 1 - 9,
        #this should be same as s value if  tile is located correctly

        if s == current_position: # skip those correct tiles
            count += 1
            continue
        # for x
        if current_position in [1, 3]:
            current_x = 1
        elif current_position in [2, 4, 7]:
            current_x = 2
        elif current_position in [5, 8]:
            current_x = 3
        else:    # 6
            current_x = 4

        # for y
        if current_position in [1, 2]:
            current_y = 1
        elif current_position in [3, 4, 5, 6]:
            current_y = 2
        else: # 7 or 8
            current_y = 3
        count += 1

        # evaluate the tile original position x and y
        # for x
        if s in [1, 3]:
            x1 = 1
        elif s in [2, 4, 7]:
            x1 = 2
        elif s in [5, 8]:
            x1 = 3
        else:    # 6
            x1 = 4

        # for y
        if s in [1, 2]:
            y1 = 1
        elif s in [3, 4, 5, 6]:
            y1 = 2
        else: # 7 or 8
            y1 = 3
        # manhattan calculation
        sum += abs(current_x - x1) + abs(current_y - y1)
    # in here use max to compare manhattan and displace
    return max(sum, Problem.h(node) )




########    test code to generata data    ########

############# Q1 Q2 test
# there are time and cost array
puzzle_time1 = []
puzzle_time2 = []
puzzle_time3 = []
puzzle_cost1 = []
puzzle_cost2 = []
puzzle_cost3 = []

test_num = 20

for i in range(test_num): # test_num
    print('This is solving the {} puzzle '.format(i + 1) )
    current_puzzle = make_rand_8puzzle()
    display(current_puzzle.initial)

    # misplace heuristic
    print('Misplace heuristic')
    start_time = time.time()
    node1 = astar_search_new(current_puzzle, h=current_puzzle.h)
    end_time = time.time()
    puzzle_time1.append(end_time - start_time)
    puzzle_cost1.append(node1.path_cost)
    print(node1.path_cost)
    print('Time is {}'.format(end_time - start_time))

    # Manhattan
    print('Manhattan')
    start_time = time.time()
    node2 = astar_search_new(current_puzzle, h = lambda n : manhattan_h(current_puzzle, n) )
    end_time = time.time()
    puzzle_time2.append(end_time - start_time)
    puzzle_cost2.append(node2.path_cost)
    print(node2.path_cost)
    print('Time is {}'.format(end_time - start_time))

    # Max of manhattan and misplaced
    print('Max of manhattan and misplaced')
    start_time = time.time()
    node3 = astar_search_new(current_puzzle, h = lambda n : manhattan_max_h(current_puzzle, n) )
    end_time = time.time()
    puzzle_time3.append(end_time - start_time)
    puzzle_cost3.append(node3.path_cost)
    print(node3.path_cost)
    print('Time is {}'.format(end_time - start_time))

    print()

print('Misplace', end = '\n')
print(puzzle_cost1)
print(puzzle_time1)
print('The average cost is {}'.format(sum(puzzle_cost1)/test_num ))
print('The average time is {}'.format(sum(puzzle_time1)/test_num ))
print('Manhattan', end = '\n')
print(puzzle_cost2)
print(puzzle_time2)
print('The average cost is {}'.format(sum(puzzle_cost2)/test_num ))
print('The average time is {}'.format(sum(puzzle_time2)/test_num ))
print('Max of Manhattan and Misplace', end = '\n')
print(puzzle_cost3)
print(puzzle_time3)
print('The average cost is {}'.format(sum(puzzle_cost3)/test_num ))
print('The average time is {}'.format(sum(puzzle_time3)/test_num ))


print("\n\n\n\n")

############ Question 3
print("this is for DDDDDUUUUUCCCCKKKK NOW")
#print('test start here')
'''
puzzle_time1 = []
puzzle_time2 = []
puzzle_time3 = []
puzzle_cost1 = []
puzzle_cost2 = []
puzzle_cost3 = []

test_num = 10
'''
for i in range(test_num):
    print('This is the {} duke puzzle '.format(i + 1) )
    current_puzzle_duck = make_rand_duckpuzzle()
    duke_display(current_puzzle_duck.initial)

    # misplace heuristic
    print('Misplace heuristic')
    start_time = time.time()
    node1 = astar_search_new(current_puzzle_duck, h=current_puzzle_duck.h)
    end_time = time.time()
    puzzle_time1.append(end_time - start_time)
    puzzle_cost1.append(node1.path_cost)
    print('the path cost is {}'. format(node1.path_cost))
    print('Time is {}'.format(end_time - start_time))

    # manhattan
    print('Manhattan method')
    start_time = time.time()
    node2 = astar_search_new(current_puzzle_duck, h = lambda n : manhattan_h_duck(current_puzzle_duck, n) )
    end_time = time.time()
    puzzle_time2.append(end_time - start_time)
    puzzle_cost2.append(node2.path_cost)
    print('the path cost is {}'. format(node2.path_cost))
    print('Time is {}'.format(end_time - start_time))

    # Max of manhattan and misplaced
    print('Max of manhattan and misplaced')
    start_time = time.time()
    node3 = astar_search_new(current_puzzle_duck, h = lambda n : manhattan_max_h_duck(current_puzzle_duck, n) )
    end_time = time.time()
    puzzle_time3.append(end_time - start_time)
    puzzle_cost3.append(node3.path_cost)
    print('the path cost is {}'. format(node3.path_cost))
    print('Time is {}'.format(end_time - start_time))

print('Misplace', end = '\n')
print(puzzle_cost1)
print(puzzle_time1)
print('The average cost on duck is {}'.format(sum(puzzle_cost1)/test_num ))
print('The average time on duck is {}'.format(sum(puzzle_time1)/test_num ))
print('Manhattan', end = '\n')
print(puzzle_cost2)
print(puzzle_time2)
print('The average cost on duck is {}'.format(sum(puzzle_cost2)/test_num ))
print('The average time on duck is {}'.format(sum(puzzle_time2)/test_num ))
print('Max of Manhattan and Misplace', end = '\n')
print(puzzle_cost3)
print(puzzle_time3)
print('The average cost on duck is {}'.format(sum(puzzle_cost3)/test_num ))
print('The average time on duck is {}'.format(sum(puzzle_time3)/test_num ))
