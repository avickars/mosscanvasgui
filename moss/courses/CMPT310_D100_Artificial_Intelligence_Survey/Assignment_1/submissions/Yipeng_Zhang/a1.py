from search import *
import random
import time

def make_rand_8puzzle():
    list = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    while 1:
        randomList = random.sample(list, 9)
        randomTuple = tuple(randomList)
        if (randomTuple[0] == 0 or randomTuple[2] == 0 or randomTuple[6] == 0 or randomTuple[8] == 0):
            myPuzzle = EightPuzzle(initial=randomTuple, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))
            if (myPuzzle.check_solvability(state=myPuzzle.initial)):
                break

    return myPuzzle

def make_rand_Duckpuzzle():
    list = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    Tuple = tuple(list)
    myPuzzle = DuckPuzzle(Tuple, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))
    steps = random.randint(20000, 25000)
    while steps != 0:
        action = random.sample(myPuzzle.actions(state=myPuzzle.initial), 1)
        action = action[0]
        myPuzzle.initial = myPuzzle.result(state=myPuzzle.initial, action=action)
        steps = steps - 1

    return myPuzzle

def displayEightPuzzle(state):
    print(state[0], state[1], state[2])
    print(state[3], state[4], state[5])
    print(state[6], state[7], state[8])

def displayDuckPuzzle(state):
    print(state[0], state[1])
    print(state[2], state[3], state[4], state[5])
    print(" ", state[6], state[7], state[8])

def myEightPuzzleFunction(node):
    distance = 0
    for index, item in enumerate(node.state):
        prev_row, prev_col = int(index / 3), index % 3
        if(item == 0):
            goal_row, goal_col = 2, 2
        elif(int(item / 4) == 0):
            goal_row, goal_col = 0, item % 4 - 1
        elif(int(item / 7) == 0):
            goal_row, goal_col = 1, item % 7 - 4
        else:
            goal_row, goal_col = 2, item % 10 - 7
        distance += abs(prev_row - goal_row) + abs(prev_col - goal_col)
    return distance

def myDuckPuzzleFunction(node):
    distance = 0
    for index, item in enumerate(node.state):
        if index == 0:
            temp = {0: 5, 1: 0, 2: 1, 3: 1, 4: 2, 5: 3, 6: 4, 7: 3, 8: 4}
            distance += temp[item]
        elif index == 1:
            temp = {0: 4, 1: 1, 2: 0, 3: 2, 4: 1, 5: 2, 6: 3, 7: 2, 8: 3}
            distance += temp[item]
        elif index == 2:
            temp = {0: 4, 1: 1, 2: 2, 3: 0, 4: 1, 5: 2, 6: 3, 7: 2, 8: 3}
            distance += temp[item]
        elif index == 3:
            temp = {0: 3, 1: 2, 2: 1, 3: 1, 4: 0, 5: 1, 6: 2, 7: 1, 8: 2}
            distance += temp[item]
        elif index == 4:
            temp = {0: 2, 1: 3, 2: 2, 3: 2, 4: 1, 5: 0, 6: 1, 7: 2, 8: 1}
            distance += temp[item]
        elif index == 5:
            temp = {0: 1, 1: 4, 2: 3, 3: 3, 4: 2, 5: 1, 6: 0, 7: 3, 8: 2}
            distance += temp[item]
        elif index == 6:
            temp = {0: 2, 1: 3, 2: 2, 3: 2, 4: 1, 5: 2, 6: 3, 7: 0, 8: 1}
            distance += temp[item]
        elif index == 7:
            temp = {0: 1, 1: 4, 2: 3, 3: 3, 4: 2, 5: 1, 6: 2, 7: 1, 8: 0}
            distance += temp[item]
        elif index == 8:
            temp = {0: 0, 1: 5, 2: 4, 3: 4, 4: 3, 5: 2, 6: 1, 7: 2, 8: 1}
            distance += temp[item]
    return distance


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

        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions = ['DOWN', 'RIGHT']
        elif index_blank_square == 1 or index_blank_square == 5:
            possible_actions = ['DOWN', 'LEFT']
        elif index_blank_square == 2 or index_blank_square == 6:
            possible_actions = ['UP', 'RIGHT']
        elif index_blank_square == 3:
            possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        elif index_blank_square == 4:
            possible_actions = ['DOWN', 'LEFT', 'RIGHT']
        elif index_blank_square == 7:
            possible_actions = ['UP', 'LEFT', 'RIGHT']
        else:
            possible_actions = ['UP', 'LEFT']

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank == 0 or blank == 1:
            delta = {'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 2 or blank == 3 or blank == 4 or blank == 5:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'LEFT': -1, 'RIGHT': 1}
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


if __name__ == "__main__":

    #Eight Puzzle Question

    EightPuzzleList = []
    for i in range(0, 10):
        EightPuzzleList.append(make_rand_8puzzle())

    for i in range(0, 10):

        print("\n")
        print("The", i + 1, "Puzzle")
        print("\n")

        # Manhattan distance heuristic
        print("Manhattan distance heuristic")
        start = time.time()
        a = astar_search(EightPuzzleList[i], h=myEightPuzzleFunction, display=True)
        end = time.time()
        print(f'elapsed time (in seconds): {end - start}s')
        print("The total path cost is", a.path_cost)

        print("-----------------------------------------------------------")

        # misplaced tile heuristic
        print("misplaced tile heuristic")
        start = time.time()
        a = astar_search(EightPuzzleList[i], display=True)
        end = time.time()
        print(f'elapsed time (in seconds): {end - start}s')
        print("The total path cost is", a.path_cost)

        print("-----------------------------------------------------------")

        # max of the misplaced tile heuristic and the Manhattan distance heuristic
        print("max of the misplaced tile heuristic and the Manhattan distance heuristic")
        node = Node(state=EightPuzzleList[i].initial)
        h1 = EightPuzzleList[i].h(node)
        h2 = myEightPuzzleFunction(node)
        if (h1 > h2):
            h = EightPuzzleList[i].h
        else:
            h = myEightPuzzleFunction
        start = time.time()
        a = astar_search(EightPuzzleList[i], h, display=True)
        end = time.time()
        print(f'elapsed time (in seconds): {end - start}s')
        print("The total path cost is", a.path_cost)

        print("-----------------------------------------------------------")


    # Duck Puzzle Question
    DuckPuzzleList = []
    for i in range(0, 10):
        DuckPuzzleList.append(make_rand_Duckpuzzle())

    for i in range(0, 10):

        print("\n")
        print("The", i + 1, "Puzzle")
        print("\n")

        # Manhattan distance heuristic
        print("Manhattan distance heuristic")
        start = time.time()
        a = astar_search(DuckPuzzleList[i], h=myDuckPuzzleFunction, display=True)
        end = time.time()
        print(f'elapsed time (in seconds): {end - start}s')
        print("The total path cost is", a.path_cost)

        print("-----------------------------------------------------------")

        # misplaced tile heuristic
        print("misplaced tile heuristic")
        start = time.time()
        a = astar_search(DuckPuzzleList[i], display=True)
        end = time.time()
        print(f'elapsed time (in seconds): {end - start}s')
        print("The total path cost is", a.path_cost)

        print("-----------------------------------------------------------")

        # max of the misplaced tile heuristic and the Manhattan distance heuristic
        print("max of the misplaced tile heuristic and the Manhattan distance heuristic")
        node = Node(state=DuckPuzzleList[i].initial)
        h1 = DuckPuzzleList[i].h(node)
        h2 = myDuckPuzzleFunction(node)
        if (h1 > h2):
            h = DuckPuzzleList[i].h
        else:
            h = myDuckPuzzleFunction
        start = time.time()
        a = astar_search(DuckPuzzleList[i], h, display=True)
        end = time.time()
        print(f'elapsed time (in seconds): {end - start}s')
        print("The total path cost is", a.path_cost)

        print("-----------------------------------------------------------")


   