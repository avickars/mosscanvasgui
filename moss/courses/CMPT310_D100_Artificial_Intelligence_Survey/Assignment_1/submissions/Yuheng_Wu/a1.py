from search import *
import threading
import time
import datetime
import random


# Re-implementation of the EightPuzzle in Search.py to add the additional h-values
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

    def h_man(self, node):
        def distance(position):
            return (int(position / 3), position % 3)

        # Manhattan Heuristic Function

        totalManhattenDistance = 0;

        for x in node.state:
            currentIndex = node.state.index(x)
            currentDistance = distance(currentIndex)

            requiredIndex = self.goal.index(x)
            requriedDistance = distance(requiredIndex)

            singleManhattenDistance = abs(currentDistance[0] - requriedDistance[0]) + abs(
                currentDistance[1] - requriedDistance[1])
            totalManhattenDistance = totalManhattenDistance + singleManhattenDistance

        return totalManhattenDistance

    def h_max(self, node):
        return max(self.h(node), self.h_man(node))


# Copied implementation of the EightPuzzle in Search.py to change the shape of the puzzle and add the additional h-values
class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index(0)

    def actions(self, state):

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': (0, 0, -2, -2, 0, 0, -3, -3, -3), 'DOWN': (2, 2, 0, 3, 3, 3, 0, 0, 0),
                 'LEFT': (0, -1, 0, -1, -1, -1, 0, -1, -1), 'RIGHT': (1, 0, 1, 1, 1, 0, 1, 1, 0)}

        neighbor = blank + delta[action][blank]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def h_man(self, node):
        # Manhattan Heuristic Function

        totalManhattenDistance = 0;

        gridLocation = [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)]

        for x in node.state:
            currentIndex = node.state.index(x)
            currentLocation = gridLocation[currentIndex]

            requiredIndex = self.goal.index(x)
            requiredLocation = gridLocation[requiredIndex]

            singleManhattenDistance = abs(currentLocation[0] - requiredLocation[0]) + abs(
                currentLocation[1] - requiredLocation[1])
            totalManhattenDistance = totalManhattenDistance + singleManhattenDistance

        return totalManhattenDistance

    def h_max(self, node):
        return max(self.h(node), self.h_man(node))


#########################################
# Question 1
def display(state):
    index = 0;
    result = ""
    for value in state:
        if value == 0:
            result = result + "*"
        else:
            result = result + str(value)

        index = index + 1

        if index % 3 == 0 and index != 0:
            result = result + "\n"

    return result


#########################################

#########################################
# Questions 2 and 3

# Creates a Random EightPuzzle by randomising the problem and checking if it is solvable
def make_rand_8puzzle():
    solution = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    problem = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    random.shuffle(problem)

    puzzle = EightPuzzle(tuple(problem), solution)

    while not puzzle.check_solvability(problem):
        random.shuffle(problem)
        puzzle = EightPuzzle(tuple(problem), solution)

    return puzzle


# Creates a Random DuckPuzzel by doing 1000 random legal moves
def make_rand_duck_puzzle():
    solution = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    problem = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    puzzle = DuckPuzzle(problem, solution)

    for x in range(1000):
        possibleActions = puzzle.actions(problem)
        randomAction = random.choice(possibleActions)
        problem = puzzle.result(problem, randomAction)
        puzzle = DuckPuzzle(problem, solution)

    return puzzle


def general_thread_function(id):
    output = ""

    # change this to EightPuzzle or DuckPuzzle for questions 2 or 3
    puzzle = make_rand_8puzzle()
    output += "Thread #" + str(id) + "\n" + str(puzzle.initial) + '\n'

    timer1 = time.time()
    result1 = "Max" + '\n'
    searchResult1 = astar_search(puzzle, puzzle.h_max, True)
    result1 += "Popped: " + str(searchResult1[1]) + '\n'
    result1 += "Time Elapsed: " + str(datetime.timedelta(seconds=time.time() - timer1)) + '\n'
    result1 += "Length: " + str(searchResult1[0].depth) + '\n'

    output += result1 + '\n'

    timer2 = time.time()
    result2 = "Manhattan" + '\n'
    searchResult2 = astar_search(puzzle, puzzle.h_man, True)
    result2 += "Popped: " + str(searchResult2[1]) + '\n'
    result2 += "Time Elapsed: " + str(datetime.timedelta(seconds=time.time() - timer2)) + '\n'
    result2 += "Length: " + str(searchResult2[0].depth) + '\n'
    output += result2 + '\n'

    timer3 = time.time()
    result3 = "Misplaced" + '\n'
    searchResult3 = astar_search(puzzle, puzzle.h, True)
    result3 += "Popped: " + str(searchResult3[1]) + '\n'
    result3 += "Time Elapsed: " + str(datetime.timedelta(seconds=time.time() - timer3)) + '\n'
    result3 += "Length: " + str(searchResult3[0].depth) + '\n'
    output += result3 + '\n'

    output += "-------------------------------"

    print(output)


#########################################


# main function
for x in range(10):
    x = threading.Thread(target=general_thread_function, args=(x,))
    x.start()
    time.sleep(1)
