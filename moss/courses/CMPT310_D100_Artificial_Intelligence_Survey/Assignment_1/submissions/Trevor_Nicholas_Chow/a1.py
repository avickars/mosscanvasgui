# a1.py
from search import *
import random
import time
#Changed this function in searh.py to print the nodes_removed to the screen
#There are no other changes made to search.py
def best_first_graph_search(problem, f, display=False):
        nodes_removed = 0
        f = memoize(f, 'f')
        node = Node(problem.initial)
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        explored = set()
        while frontier:
            node = frontier.pop()
            nodes_removed = nodes_removed + 1
            if problem.goal_test(node.state):
                if display:
                    print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                    print("Number of noded removed from frontier: ", nodes_removed)
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

#Didnt change this function, but need it to call modified best_first_graph_search
def astar_search(problem, h=None, display=False):
        """A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass."""
        h = memoize(h or problem.h, 'h')
        return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

#Similar to EightPuzzle class
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

        #possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions = ['DOWN', 'RIGHT']
        elif index_blank_square == 1:
            possible_actions = ['DOWN', 'LEFT']
        elif index_blank_square == 2 or index_blank_square == 6:
            possible_actions = ['UP', 'RIGHT']
        elif index_blank_square == 3:
            possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        elif index_blank_square == 4:
            possible_actions = ['DOWN', 'LEFT', 'RIGHT']
        elif index_blank_square == 5:
            possible_actions = ['DOWN', 'LEFT']
        elif index_blank_square == 7:
            possible_actions = ['UP', 'LEFT', 'RIGHT']
        elif index_blank_square == 8:
            possible_actions = ['UP','LEFT']

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        if blank == 3 or blank == 2:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 0 or blank == 1:
            delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
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
# ______________________________________________________________________________

#creates a randum DuckPuzzle by doing actions from the goal state
def make_rand_duckpuzzle():
        temp_arr = Duck.goal
        cycles = random.randint(0, 1000);
        for i in range(cycles):
            possible_actions = Duck.actions(temp_arr)
            temp = len(possible_actions) - 1
            choice = random.randint(-1, temp)
            temp_arr = Duck.result(temp_arr,possible_actions[choice])
        return temp_arr

#Displays the state in DuckPuzzle format
def display2(state):
        count = 0
        for i in range(9):
            count = count + 1
            if count == 7:
                print(" ", end =" ")
            if state[i] == 0:
                print("*", end =" ")
            else:
                print(state[i], end =" ")
            if count == 2:
                print("")
            if count == 6:
                print("")
        print("")

#Manhattan distance calculation for DuckPuzzle
def Manhattan2(node):
        distance = 0
        for i in Duck.goal:
                x2,y2 = Map(i)
                c = node.state.index(i)
                #bypass 0 tile
                if c == 0:
                    continue
                elif c == 8:
                    x1,y1 = Map(0)
                else:
                    x1,y1 = Map(c+1)
                distance = distance + abs(x2 - x1) + abs(y2 - y1)
        return distance

#Assign x and y value depending on the where the value is in the state
def Map2(value):
        if value == 0:
            return (3,2)
        if value == 1:
            return (0,0)
        if value == 2:
            return (1,0)
        if value == 3:
            return (0,1)
        if value == 4:
            return (1,1)
        if value == 5:
            return (2,1)
        if value == 6:
            return (3,1)
        if value == 7:
            return (1,2)
        if value == 8:
            return (2,2)

#Compares Manhattan and Misplaced and takes the max value
def Max_Manhattan_Mispplace2(node):
        h1 = Duck.h(node)
        h2 = Manhattan2(node)
        if h1 > h2:
            return h1
        else:
            return h2

#Creates a random EightPuzzle by doing actions from the goal state
def make_rand_8puzzle():
        temp_arr = EP.goal
        cycles = random.randint(0, 1000);
        for i in range(cycles):
            possible_actions = EP.actions(temp_arr)
            temp = len(possible_actions) - 1
            choice = random.randint(-1, temp)
            temp_arr = EP.result(temp_arr, possible_actions[choice])
        return temp_arr

#Displays the state in EightPuzzle format
def display(state):
        count = 0
        for i in range(9):
            count = count + 1
            #https://www.stechies.com/python-print-without-newline/
            #Resource for printing multiple charcters on the same line
            if state[i] == 0:
                print("*", end =" ")
            else:
                print(state[i], end =" ")
            if count % 3 == 0:
                print("")

#Calculates the Manhattan distance for EightPuzzle state
def Manhattan(node):
        distance = 0
        for i in EP.goal:
                x2,y2 = Map(i)
                c = node.state.index(i)
                #bypass 0 tile
                if c == 0:
                    continue
                elif c == 8:
                    x1,y1 = Map(0)
                else:
                    x1,y1 = Map(c+1)
                distance = distance + abs(x2 - x1) + abs(y2 - y1)
        return distance

#Assign x and y value depending on the where the value is in the state for EightPuzzle
def Map(value):
        if value == 0:
            return (2,2)
        if value == 1:
            return (0,0)
        if value == 2:
            return (1,0)
        if value == 3:
            return (2,0)
        if value == 4:
            return (0,1)
        if value == 5:
            return (1,1)
        if value == 6:
            return (2,1)
        if value == 7:
            return (0,2)
        if value == 8:
            return (1,2)

#Compares Manhattan and Misplaced and takes the max value
def Max_Manhattan_Misplace(node):
        h1 = EP.h(node)
        h2 = Manhattan(node)
        if h1 > h2:
            return h1
        else:
            return h2

#Main
for i in range(10):
    print("**********************")
    print("EightPuzzle Test #", i+1)
    print("**********************")
    EP = EightPuzzle(0)
    EP.initial = tuple(make_rand_8puzzle())
    display(EP.initial)

    #Misplaced for EightPuzzle
    start_time = time.time()
    a = astar_search(EP, EP.h, True)
    elapsed_time = time.time() - start_time
    print("The EightPuzzle(Misplaced) completed in seconds is :", elapsed_time)
    print("Number of tiles moved/path_cost: ", a.path_cost)
    print("--------------------")


    #Manhattan for EightPuzzle
    start_time = time.time()
    a = astar_search(EP, Manhattan, True)
    elapsed_time = time.time() - start_time
    print("The EightPuzzle(Manhattan) completed in seconds is :", elapsed_time)
    print("Number of tiles moved/path_cost: ", a.path_cost)
    print("--------------------")

    #Max for EightPuzzle
    start_time = time.time()
    a = astar_search(EP, Max_Manhattan_Misplace, True)
    elapsed_time = time.time() - start_time
    print("The EightPuzzle(Max) completed in seconds is :", elapsed_time)
    print("Number of tiles moved/path_cost: ", a.path_cost)
    print("--------------------")

    print("**********************")
    print("DuckPuzzle Test #", i+1)
    print("**********************")
    Duck = DuckPuzzle(0)
    Duck.initial = tuple(make_rand_duckpuzzle())
    display2(Duck.initial)

    #Misplaced for DuckPuzzle
    start_time = time.time()
    a = astar_search(Duck, Duck.h, True)
    elapsed_time = time.time() - start_time
    print("The DuckPuzzle(Misplaced) completed in seconds is :", elapsed_time)
    print("Number of tiles moved/path_cost: ", a.path_cost)
    print("--------------------")

    #Manhattan for DuckPuzzle
    start_time = time.time()
    a = astar_search(Duck, Manhattan2, True)
    elapsed_time = time.time() - start_time
    print("The DuckPuzzle(Manhattan) completed in seconds is :", elapsed_time)
    print("Number of tiles moved/path_cost: ", a.path_cost)
    print("--------------------")

    #Max for DuckPuzzle
    start_time = time.time()
    a = astar_search(Duck, Max_Manhattan_Mispplace2, True)
    elapsed_time = time.time() - start_time
    print("The DuckPuzzle(Max) completed in seconds is :", elapsed_time)
    print("Number of tiles moved/path_cost: ", a.path_cost)
    print("--------------------")

print("DONE")
# ...