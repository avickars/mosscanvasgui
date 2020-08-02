# a1.py
import time
# my code will not run without search.py
from search import *
from itertools import permutations


class SubClass(EightPuzzle):
    # If i set goal to none, it will inherit from the parent,if not
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))
        self.goal = goal  # I dont have to set goal but i can if i want because of this line

    def display(self, state):
        length = len(state)
        for x in range(length):
            if x % 3 == 0 and x != 0:  # set to the new line
                print()
            if (state[x] == 0):
                # add end= " " to print on the same line until the first if statement is met
                print("*", end=" ")
            else:
                print(state[x], end=" ")
        print()

        # this is a helper function for me to go back to the previous state
    def reverseAction(self, actionName):
        if actionName == "UP":
            return "DOWN"
        if actionName == "DOWN":
            return "UP"
        if actionName == "LEFT":
            return "RIGHT"
        if actionName == "RIGHT":
            return "LEFT"

    def make_rand_8puzzle(self):
        # my first method only gets 87 possible random states using simple brute force search 2 times
        answerList = []
        actionList = []
        futureList = []
        finalList = []
        # i will move from the goal to get all the answers and append them to the list

        # since the goal itself is also solvable, I push it to the answerList too and start from it
        nextState = self.goal  # get the goal value from the parent
        answerList.append(nextState)
        actionList = EightPuzzle.actions(self, nextState)  # get the current available actions

        exit = False
        count = 0
        while (exit == False or len(answerList) == 1):
            actionList = EightPuzzle.actions(self, nextState)
            lengthOfAction = len(actionList)
            if lengthOfAction == 2:
                actionName = actionList[0]
                nextState = EightPuzzle.result(self, nextState, actionName)
                if (nextState not in answerList):
                    answerList.append(nextState)
                    count += 1
                    # print("21")
                    # experiment
                    nextState = EightPuzzle.result(
                        self, nextState, self.reverseAction(actionName))
                    actionName = actionList[1]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    if ((nextState not in futureList) and (nextState not in answerList)):
                        futureList.append(nextState)
                    nextState = EightPuzzle.result(
                        self, nextState, self.reverseAction(actionName))
                    actionName = actionList[0]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    # experiment
                else:
                    nextState = EightPuzzle.result(
                        self, nextState, self.reverseAction(actionName))
                    actionName = actionList[1]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    if (nextState not in answerList):
                        answerList.append(nextState)
                        count += 1
                        # print("22")
                    else:
                        exit = True
            elif lengthOfAction == 3:
                actionName = actionList[0]
                nextState = EightPuzzle.result(self, nextState, actionName)
                if (nextState not in answerList):
                    answerList.append(nextState)
                    count += 1
                    # print("31")
                    # experiment
                    nextState = EightPuzzle.result(
                        self, nextState, self.reverseAction(actionName))
                    actionName = actionList[1]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    if ((nextState not in futureList) and (nextState not in answerList)):
                        futureList.append(nextState)
                    nextState = EightPuzzle.result(
                        self, nextState, self.reverseAction(actionName))
                    actionName = actionList[2]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    if ((nextState not in futureList) and (nextState not in answerList)):
                        futureList.append(nextState)
                    nextState = EightPuzzle.result(
                        self, nextState, self.reverseAction(actionName))
                    actionName = actionList[0]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    # experiment
                else:
                    nextState = EightPuzzle.result(
                        self, nextState, self.reverseAction(actionName))
                    actionName = actionList[1]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    if (nextState not in answerList):
                        answerList.append(nextState)
                        count += 1
                        # print("32")
                    else:
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[2]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        if (nextState not in answerList):
                            answerList.append(nextState)
                            count += 1
                            # print("33")
                        else:
                            exit = True

            else:
                actionName = actionList[0]
                nextState = EightPuzzle.result(self, nextState, actionName)
                if (nextState not in answerList):
                    answerList.append(nextState)
                    count += 1
                    # print("41")
                    # experiment
                    nextState = EightPuzzle.result(
                        self, nextState, self.reverseAction(actionName))
                    actionName = actionList[1]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    if ((nextState not in futureList) and (nextState not in answerList)):
                        futureList.append(nextState)
                    nextState = EightPuzzle.result(
                        self, nextState, self.reverseAction(actionName))
                    actionName = actionList[2]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    if ((nextState not in futureList) and (nextState not in answerList)):
                        futureList.append(nextState)
                    nextState = EightPuzzle.result(
                        self, nextState, self.reverseAction(actionName))
                    actionName = actionList[3]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    if ((nextState not in futureList) and (nextState not in answerList)):
                        futureList.append(nextState)
                    nextState = EightPuzzle.result(
                        self, nextState, self.reverseAction(actionName))
                    actionName = actionList[0]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    # experiment
                else:
                    nextState = EightPuzzle.result(
                        self, nextState, self.reverseAction(actionName))
                    actionName = actionList[1]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    if (nextState not in answerList):
                        answerList.append(nextState)
                        count += 1
                        # print("42")
                    else:
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[2]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        if (nextState not in answerList):
                            answerList.append(nextState)
                            count += 1
                            # print("43")
                        else:
                            nextState = EightPuzzle.result(
                                self, nextState, self.reverseAction(actionName))
                            actionName = actionList[3]
                            nextState = EightPuzzle.result(self, nextState, actionName)
                            if (nextState not in answerList):
                                answerList.append(nextState)
                                count += 1
                                # print("44")
                            else:
                                exit = True

        exit = False
        lengthOfFuture = len(futureList)

        for i in range(lengthOfFuture):
            nextState = futureList[i]  # get the goal value from the parent
            if nextState in answerList:
                # print("been here a a")
                continue
            answerList.append(nextState)
            # get the current available actions
            actionList = EightPuzzle.actions(self, nextState)
            while (exit == False or len(answerList) == 1):
                actionList = EightPuzzle.actions(self, nextState)
                lengthOfAction = len(actionList)
                if lengthOfAction == 2:
                    actionName = actionList[0]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    if (nextState not in answerList):
                        answerList.append(nextState)
                        count += 1
                        # print("21")
                        # experiment
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[1]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        if ((nextState not in futureList) and (nextState not in answerList)):
                            futureList.append(nextState)
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[0]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        # experiment
                    else:
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[1]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        if (nextState not in answerList):
                            answerList.append(nextState)
                            count += 1
                            # print("22")
                        else:
                            exit = True
                elif lengthOfAction == 3:
                    actionName = actionList[0]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    if (nextState not in answerList):
                        answerList.append(nextState)
                        count += 1
                        # print("31")
                        # experiment
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[1]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        if ((nextState not in futureList) and (nextState not in answerList)):
                            futureList.append(nextState)
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[2]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        if ((nextState not in futureList) and (nextState not in answerList)):
                            futureList.append(nextState)
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[0]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        # experiment
                    else:
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[1]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        if (nextState not in answerList):
                            answerList.append(nextState)
                            count += 1
                            # print("32")
                        else:
                            nextState = EightPuzzle.result(
                                self, nextState, self.reverseAction(actionName))
                            actionName = actionList[2]
                            nextState = EightPuzzle.result(self, nextState, actionName)
                            if (nextState not in answerList):
                                answerList.append(nextState)
                                count += 1
                                # print("33")
                            else:
                                exit = True

                else:
                    actionName = actionList[0]
                    nextState = EightPuzzle.result(self, nextState, actionName)
                    if (nextState not in answerList):
                        answerList.append(nextState)
                        count += 1
                        # print("41")
                        # experiment
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[1]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        if ((nextState not in futureList) and (nextState not in answerList)):
                            futureList.append(nextState)
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[2]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        if ((nextState not in futureList) and (nextState not in answerList)):
                            futureList.append(nextState)
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[3]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        if ((nextState not in futureList) and (nextState not in answerList)):
                            futureList.append(nextState)
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[0]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        # experiment
                    else:
                        nextState = EightPuzzle.result(
                            self, nextState, self.reverseAction(actionName))
                        actionName = actionList[1]
                        nextState = EightPuzzle.result(self, nextState, actionName)
                        if (nextState not in answerList):
                            answerList.append(nextState)
                            count += 1
                            # print("42")
                        else:
                            nextState = EightPuzzle.result(
                                self, nextState, self.reverseAction(actionName))
                            actionName = actionList[2]
                            nextState = EightPuzzle.result(self, nextState, actionName)
                            if (nextState not in answerList):
                                answerList.append(nextState)
                                count += 1
                                # print("43")
                            else:
                                nextState = EightPuzzle.result(
                                    self, nextState, self.reverseAction(actionName))
                                actionName = actionList[3]
                                nextState = EightPuzzle.result(self, nextState, actionName)
                                if (nextState not in answerList):
                                    answerList.append(nextState)
                                    count += 1
                                    # print("44")
                                else:
                                    exit = True

        for i in answerList:
            if i not in finalList:
                finalList.append(i)
        for j in futureList:
            if j not in finalList:
                finalList.append(j)

        lengthOfAnswer = len(finalList)

        randomPick = random.randint(1, lengthOfAnswer-1)
        return finalList[randomPick]

    def make_rand_8puzzle_method2(self):
        # this is my second way of doing it, using the checker function as a helper function. This method will get all the
        # solvable outcomes out of 362880 which is 181440
        perm = permutations((1, 2, 3, 4, 5, 6, 7, 8, 0))
        answerList = []
        count = 0
        for i in perm:
            isSolvable = EightPuzzle.check_solvability(self, i)
            if isSolvable:
                # count += 1
                answerList.append(i)
        lengthOfAnswer = len(answerList)
        randomPick = random.randint(0, lengthOfAnswer-1)
        # print(count)
        return answerList[randomPick]

    def get_ten_rand_puzzles(self):
        # this method returns a list of 10 random puzzles using make_rand_8puzzle method
        answerList = []

        while len(answerList) < 10:
            puzzle = self.make_rand_8puzzle()
            if puzzle not in answerList:
                answerList.append(puzzle)

        return answerList

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1
        return inversion % 2 == 0

        # borrow from search.py and added self param
    def best_first_graph_search(self, problem, f, display=False):
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
        # to get the number of nodes being deleted from the frontier
        deleteCount = 0
        ##
        explored = set()
        while frontier:

            node = frontier.pop()
            ##
            deleteCount += 1
            ##
            if problem.goal_test(node.state):

                if display:
                    print(len(explored), "paths have been expanded and",
                          len(frontier), "paths remain in the frontier")

                return node, deleteCount
            explored.add(node.state)

            for child in node.expand(problem):
                if child.state not in explored and child not in frontier:
                    frontier.append(child)
                elif child in frontier:
                    if f(child) < frontier[child]:
                        del frontier[child]
                        frontier.append(child)
        return None

    def astar_search(self, problem, h=None, display=False):
        # borrow from search.py and added self param
        """A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass."""

        h = memoize(h or problem.h, 'h')  # calling the h function

        return self.best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
        # my understanding n  here is a node, h takes a node as a param

    def astar_search_max_between(self, problem, h=None, display=False):
        h = memoize(h or problem.h, 'h')  # calling the h function

        # before passing in the lambda, i check if h(n) > manhattan(n), and pass in the bigger one however, manhattan distance is always bigger
        return self.best_first_graph_search(problem, lambda n: n.path_cost + (h(n) if h(n) > self.manhattan(n) else self.manhattan(n)), display)

    def solve_in_misplaced_tile(self, puzzleList):
        # this function takes in a puzzle list that has 10 puzzles using the misplaced tile heuristic
        print("Using misplaced heuristic:")
        for i in range(len(puzzleList)):
            puzzle = puzzleList[i]
            problem = EightPuzzle(puzzle)

            start_time = time.time()  # get the running time of astar_search
            # using the default heuristic function
            returnTuple = self.astar_search(problem, self.h)
            elapsed_time = time.time() - start_time

            elapsed_time = '%.6f' % (elapsed_time)

            print("It takes " + str(elapsed_time) + "sec to solve puzzle " + str(i+1) + " and " +
                  str(returnTuple[1]) + " nodes removed from the frontier and moved " + str(returnTuple[1]-1) + " tile(s)")

    def solve_in_manhattan(self, puzzleList):
        # this function takes in a puzzle list that has 10 puzzles using the manhattan heuristic
        print("Using manhattan distance heuristic:")
        for i in range(len(puzzleList)):
            puzzle = puzzleList[i]
            problem = EightPuzzle(puzzle)

            start_time = time.time()  # get the running time of astar_search
            # using the default heuristic function
            returnTuple = self.astar_search(problem, self.manhattan)
            elapsed_time = time.time() - start_time

            elapsed_time = '%.6f' % (elapsed_time)

            print("It takes " + str(elapsed_time) + "sec to solve puzzle " + str(i+1) + " and " +
                  str(returnTuple[1]) + " nodes removed from the frontier and moved " + str(returnTuple[1]-1) + " tile(s)")

    def solve_in_max_between_misplaced_and_mahattan(self, puzzleList):
        # this function takes in a puzzle list that has 10 puzzles using the manhattan heuristic
        print("Using max between misplaced and manhattan distance heuristic:")
        for i in range(len(puzzleList)):
            puzzle = puzzleList[i]
            problem = EightPuzzle(puzzle)

            start_time = time.time()  # get the running time of astar_search
            # using the default heuristic function
            returnTuple = self.astar_search_max_between(problem)
            elapsed_time = time.time() - start_time

            elapsed_time = '%.6f' % (elapsed_time)

            print("It takes " + str(elapsed_time) + "sec to solve puzzle " + str(i+1) + " and " +
                  str(returnTuple[1]) + " nodes removed from the frontier and moved " + str(returnTuple[1]-1) + " tile(s)")

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        goalState = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        indexGoal = {0: [2, -2], 1: [0, 0], 2: [1, 0], 3: [2, 0],
                     4: [0, -1], 5: [1, -1], 6: [2, -1], 7: [0, -2], 8: [1, -2]}

        initialState = node.state
        # initialize an empty dictionary to hold and x and y index or each number , using top left corner as (0,0) and move from it
        indexInitial = {0: [0, 0], 1: [0, 0], 2: [0, 0], 3: [0, 0],
                        4: [0, 0], 5: [0, 0], 6: [0, 0], 7: [0, 0], 8: [0, 0]}

        # according to the node.state we get from the node, arrange the dictionary
        for i in range(len(initialState)):
            if i == 0:
                indexInitial[initialState[i]] = [0, 0]
            if i == 1:
                indexInitial[initialState[i]] = [1, 0]
            if i == 2:
                indexInitial[initialState[i]] = [2, 0]
            if i == 3:
                indexInitial[initialState[i]] = [0, -1]
            if i == 4:
                indexInitial[initialState[i]] = [1, -1]
            if i == 5:
                indexInitial[initialState[i]] = [2, -1]
            if i == 6:
                indexInitial[initialState[i]] = [0, -2]
            if i == 7:
                indexInitial[initialState[i]] = [1, -2]
            if i == 8:
                indexInitial[initialState[i]] = [2, -2]

        # calculate the total distance by comparing each number's distance with the goal number's distance and sum them up
        totalDistance = 0
        for i in range(len(initialState)):
            totalDistance += abs(indexInitial.get(i)[0]-indexGoal.get(i)[0]) + \
                abs(indexInitial.get(i)[1] - indexGoal.get(i)[1])

        return totalDistance


class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0))
        self.goal = goal

    def display(self, state):
        legthOfNumber = len(str(state[0]))
        for i in range(len(state)):
            if i == 2:
                print()
            if i == 6:
                print(" ")
                print(" ", end=" ")
            if (state[i] == 0):
                print("*", end=" ")
            else:
                print(state[i], end=" ")
        print()

        # borrow from the 8 puzzle class
    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

        # borrow this from the puzzle class with modification to suit my need
    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        x = 0
        y = 0
        if blank == 0 or blank == 1:
            y = 2
        if blank == 2 or blank == 3 or blank == 4 or blank == 5:
            y = 3  # even tho setting y= -2 will make 3,4,5 go out of bounds, they will not have this action in the action list
            x = -2
        if blank == 6 or blank == 7 or blank == 8:
            x = -3
            # no need to set y value since it does not need to go down

        delta = {'UP': x, 'DOWN': y, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

        # borrow this from the puzzle class no modification
    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def best_first_graph_search(self, problem, f, display=False):
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
        # added delete count
        deleteCount = 0
        ##
        explored = set()
        while frontier:

            node = frontier.pop()
            ##
            deleteCount += 1
            ##
            if problem.goal_test(node.state):
                if display:
                    print(len(explored), "paths have been expanded and",
                          len(frontier), "paths remain in the frontier")
                return node, deleteCount
            explored.add(node.state)

            for child in node.expand(problem):
                if child.state not in explored and child not in frontier:
                    frontier.append(child)
                elif child in frontier:
                    if f(child) < frontier[child]:
                        del frontier[child]
                        frontier.append(child)
        return None

    def astar_search(self, problem, h=None, display=False):
        # borrow from search.py and added self param
        """A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass."""

        h = memoize(h or problem.h, 'h')  # calling the h function
        return self.best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

    def astar_search_max_between(self, problem, h=None, display=False):

        h = memoize(h or problem.h, 'h')  # calling the h function
        # before passing in the lambda, i check if h(n) > manhattan(n), and pass in the bigger one, however I realize manhattan distance is always bigger
        return self.best_first_graph_search(problem, lambda n: n.path_cost + (h(n) if h(n) > self.manhattan1(n) else self.manhattan1(n)), display)

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def actions(self, state):
        # borrow from the 8puzzle class with modification to suit the need to duckpuzzle
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 2 or index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')
        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')

        return possible_actions

    def reverseAction(self, actionName):
        # this is a helper function for generating puzzles
        if actionName == "UP":
            return "DOWN"
        if actionName == "DOWN":
            return "UP"
        if actionName == "LEFT":
            return "RIGHT"
        if actionName == "RIGHT":
            return "LEFT"

    def make_rand_duck_puzzle(self):
        answerList = []
        actionList = []
        futureList = []
        finalList = []
        # i will move from the goal to get all the answers and append them to the list

        # since the goal itself is also solvable, I push it to the answerList too and start from it
        nextState = self.goal  # get the goal value from the parent
        answerList.append(nextState)
        actionList = EightPuzzle.actions(self, nextState)  # get the current available actions

        exit = False
        count = 0
        while (exit == False or len(answerList) == 1):
            actionList = self.actions(nextState)
            lengthOfAction = len(actionList)
            if lengthOfAction == 2:
                actionName = actionList[0]
                nextState = self.result(nextState, actionName)
                if (nextState not in answerList):
                    answerList.append(nextState)
                    count += 1
                    nextState = self.result(
                        nextState, self.reverseAction(actionName))
                    actionName = actionList[1]
                    nextState = self.result(nextState, actionName)
                    if ((nextState not in futureList) and (nextState not in answerList)):
                        futureList.append(nextState)
                    nextState = self.result(
                        nextState, self.reverseAction(actionName))
                    actionName = actionList[0]
                    nextState = self.result(nextState, actionName)
                else:
                    nextState = self.result(
                        nextState, self.reverseAction(actionName))
                    actionName = actionList[1]
                    nextState = self.result(nextState, actionName)
                    if (nextState not in answerList):
                        answerList.append(nextState)
                        count += 1
                    else:
                        exit = True
            elif lengthOfAction == 3:
                actionName = actionList[0]
                nextState = self.result(nextState, actionName)
                if (nextState not in answerList):
                    answerList.append(nextState)
                    count += 1
                    nextState = self.result(
                        nextState, self.reverseAction(actionName))
                    actionName = actionList[1]
                    nextState = self.result(nextState, actionName)
                    if ((nextState not in futureList) and (nextState not in answerList)):
                        futureList.append(nextState)
                    nextState = self.result(
                        nextState, self.reverseAction(actionName))
                    actionName = actionList[2]
                    nextState = self.result(nextState, actionName)
                    if ((nextState not in futureList) and (nextState not in answerList)):
                        futureList.append(nextState)
                    nextState = self.result(
                        nextState, self.reverseAction(actionName))
                    actionName = actionList[0]
                    nextState = self.result(nextState, actionName)
                else:
                    nextState = self.result(
                        nextState, self.reverseAction(actionName))
                    actionName = actionList[1]
                    nextState = self.result(nextState, actionName)
                    if (nextState not in answerList):
                        answerList.append(nextState)
                        count += 1
                    else:
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[2]
                        nextState = self.result(nextState, actionName)
                        if (nextState not in answerList):
                            answerList.append(nextState)
                            count += 1
                        else:
                            exit = True

            else:
                actionName = actionList[0]
                nextState = self.result(nextState, actionName)
                if (nextState not in answerList):
                    answerList.append(nextState)
                    count += 1
                    nextState = self.result(
                        nextState, self.reverseAction(actionName))
                    actionName = actionList[1]
                    nextState = self.result(nextState, actionName)
                    if ((nextState not in futureList) and (nextState not in answerList)):
                        futureList.append(nextState)
                    nextState = self.result(
                        nextState, self.reverseAction(actionName))
                    actionName = actionList[2]
                    nextState = self.result(nextState, actionName)
                    if ((nextState not in futureList) and (nextState not in answerList)):
                        futureList.append(nextState)
                    nextState = self.result(
                        nextState, self.reverseAction(actionName))
                    actionName = actionList[3]
                    nextState = self.result(nextState, actionName)
                    if ((nextState not in futureList) and (nextState not in answerList)):
                        futureList.append(nextState)
                    nextState = self.result(
                        nextState, self.reverseAction(actionName))
                    actionName = actionList[0]
                    nextState = self.result(nextState, actionName)
                else:
                    nextState = self.result(
                        nextState, self.reverseAction(actionName))
                    actionName = actionList[1]
                    nextState = self.result(nextState, actionName)
                    if (nextState not in answerList):
                        answerList.append(nextState)
                        count += 1
                    else:
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[2]
                        nextState = self.result(nextState, actionName)
                        if (nextState not in answerList):
                            answerList.append(nextState)
                            count += 1
                        else:
                            nextState = self.result(
                                nextState, self.reverseAction(actionName))
                            actionName = actionList[3]
                            nextState = self.result(nextState, actionName)
                            if (nextState not in answerList):
                                answerList.append(nextState)
                                count += 1
                            else:
                                exit = True

        exit = False
        lengthOfFuture = len(futureList)

        for i in range(lengthOfFuture):
            nextState = futureList[i]  # get the goal value from the parent
            if nextState in answerList:
                continue
            answerList.append(nextState)
            # get the current available actions
            actionList = EightPuzzle.actions(self, nextState)
            while (exit == False or len(answerList) == 1):
                actionList = self.actions(nextState)
                lengthOfAction = len(actionList)
                if lengthOfAction == 2:
                    actionName = actionList[0]
                    nextState = self.result(nextState, actionName)
                    if (nextState not in answerList):
                        answerList.append(nextState)
                        count += 1
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[1]
                        nextState = self.result(nextState, actionName)
                        if ((nextState not in futureList) and (nextState not in answerList)):
                            futureList.append(nextState)
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[0]
                        nextState = self.result(nextState, actionName)
                    else:
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[1]
                        nextState = self.result(nextState, actionName)
                        if (nextState not in answerList):
                            answerList.append(nextState)
                            count += 1
                        else:
                            exit = True
                elif lengthOfAction == 3:
                    actionName = actionList[0]
                    nextState = self.result(nextState, actionName)
                    if (nextState not in answerList):
                        answerList.append(nextState)
                        count += 1
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[1]
                        nextState = self.result(nextState, actionName)
                        if ((nextState not in futureList) and (nextState not in answerList)):
                            futureList.append(nextState)
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[2]
                        nextState = self.result(nextState, actionName)
                        if ((nextState not in futureList) and (nextState not in answerList)):
                            futureList.append(nextState)
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[0]
                        nextState = self.result(nextState, actionName)
                    else:
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[1]
                        nextState = self.result(nextState, actionName)
                        if (nextState not in answerList):
                            answerList.append(nextState)
                            count += 1
                        else:
                            nextState = self.result(
                                nextState, self.reverseAction(actionName))
                            actionName = actionList[2]
                            nextState = self.result(nextState, actionName)
                            if (nextState not in answerList):
                                answerList.append(nextState)
                                count += 1
                            else:
                                exit = True

                else:
                    actionName = actionList[0]
                    nextState = self.result(nextState, actionName)
                    if (nextState not in answerList):
                        answerList.append(nextState)
                        count += 1
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[1]
                        nextState = self.result(nextState, actionName)
                        if ((nextState not in futureList) and (nextState not in answerList)):
                            futureList.append(nextState)
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[2]
                        nextState = self.result(nextState, actionName)
                        if ((nextState not in futureList) and (nextState not in answerList)):
                            futureList.append(nextState)
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[3]
                        nextState = self.result(nextState, actionName)
                        if ((nextState not in futureList) and (nextState not in answerList)):
                            futureList.append(nextState)
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[0]
                        nextState = self.result(nextState, actionName)
                    else:
                        nextState = self.result(
                            nextState, self.reverseAction(actionName))
                        actionName = actionList[1]
                        nextState = self.result(nextState, actionName)
                        if (nextState not in answerList):
                            answerList.append(nextState)
                            count += 1
                        else:
                            nextState = self.result(
                                nextState, self.reverseAction(actionName))
                            actionName = actionList[2]
                            nextState = self.result(nextState, actionName)
                            if (nextState not in answerList):
                                answerList.append(nextState)
                                count += 1
                            else:
                                nextState = self.result(
                                    nextState, self.reverseAction(actionName))
                                actionName = actionList[3]
                                nextState = self.result(nextState, actionName)
                                if (nextState not in answerList):
                                    answerList.append(nextState)
                                    count += 1
                                else:
                                    exit = True

        for i in answerList:
            if i not in finalList:
                finalList.append(i)
        for j in futureList:
            if j not in finalList:
                finalList.append(j)

        lengthOfAnswer = len(finalList)

        randomPick = random.randint(1, lengthOfAnswer-1)
        return finalList[randomPick]

    def get_ten_rand_puzzles(self):
        # this method returns a list of 10 random puzzles using make_rand_8puzzle method
        answerList = []

        while len(answerList) < 10:
            puzzle = self.make_rand_duck_puzzle()
            if puzzle not in answerList:
                answerList.append(puzzle)

        return answerList

    def solve_in_misplaced_tile(self, puzzleList):
        # this function takes in a puzzle list that has 10 puzzles using the misplaced tile heuristic
        print("Using misplaced heuristic:")

        for i in range(len(puzzleList)):
            puzzle = puzzleList[i]
            problem = DuckPuzzle(puzzle)
            start_time = time.time()  # get the running time of astar_search
            # using the default heuristic function
            returnTuple = self.astar_search(problem, self.h)
            elapsed_time = time.time() - start_time
            elapsed_time = '%.6f' % (elapsed_time)
            print("It takes " + str(elapsed_time) + "sec to solve puzzle " + str(i+1) + " and " +
                  str(returnTuple[1]) + " nodes removed from the frontier and moved " + str(returnTuple[1]-1) + " tile(s)")

    def solve_in_manhattan(self, puzzleList):
        # this function takes in a puzzle list that has 10 puzzles using the manhattan heuristic
        print("Using manhattan distance heuristic:")
        for i in range(len(puzzleList)):
            puzzle = puzzleList[i]
            problem = DuckPuzzle(puzzle)

            start_time = time.time()  # get the running time of astar_search
            # using the default heuristic function
            returnTuple = self.astar_search(problem, self.manhattan1)
            elapsed_time = time.time() - start_time

            elapsed_time = '%.6f' % (elapsed_time)

            print("It takes " + str(elapsed_time) + "sec to solve puzzle " + str(i+1) + " and " +
                  str(returnTuple[1]) + " nodes removed from the frontier and moved " + str(returnTuple[1]-1) + " tile(s)")

    def solve_in_max_between_misplaced_and_mahattan(self, puzzleList):
        # this function takes in a puzzle list that has 10 puzzles using the manhattan heuristic
        print("Using max between misplaced and manhattan distance heuristic:")
        for i in range(len(puzzleList)):
            puzzle = puzzleList[i]
            problem = DuckPuzzle(puzzle)

            start_time = time.time()  # get the running time of astar_search
            # using the default heuristic function
            returnTuple = self.astar_search_max_between(problem)
            elapsed_time = time.time() - start_time

            elapsed_time = '%.6f' % (elapsed_time)

            print("It takes " + str(elapsed_time) + "sec to solve puzzle " + str(i+1) + " and " +
                  str(returnTuple[1]) + " nodes removed from the frontier and moved " + str(returnTuple[1]-1) + " tile(s)")

    def manhattan1(self, node):
        # in manhattan distance, my coordinate system becomes:
        # (0,0),(1,0),(-1,0),(1,-1),(2,-1).... in order to fit with the shape of duck puzzle
        goalState = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        indexGoal = {0: [3, -2], 1: [0, 0], 2: [1, 0], 3: [0, -1],
                     4: [1, -1], 5: [2, -1], 6: [3, -1], 7: [1, -2], 8: [2, -2]}

        initialState = node.state
        # initialize an empty dictionary to hold and x and y index or each number , using top left corner as (0,0) and move from it
        indexInitial = {0: [0, 0], 1: [0, 0], 2: [0, 0], 3: [0, 0],
                        4: [0, 0], 5: [0, 0], 6: [0, 0], 7: [0, 0], 8: [0, 0]}

        # according to the node.state we get from the node, arrange the dictionary
        for i in range(len(initialState)):
            if i == 0:
                indexInitial[initialState[i]] = [0, 0]
            if i == 1:
                indexInitial[initialState[i]] = [1, 0]
            if i == 2:
                indexInitial[initialState[i]] = [0, -1]
            if i == 3:
                indexInitial[initialState[i]] = [1, -1]
            if i == 4:
                indexInitial[initialState[i]] = [2, -1]
            if i == 5:
                indexInitial[initialState[i]] = [3, -1]
            if i == 6:
                indexInitial[initialState[i]] = [1, -2]
            if i == 7:
                indexInitial[initialState[i]] = [2, -2]
            if i == 8:
                indexInitial[initialState[i]] = [3, -2]

        # calculate the total distance by comparing each number's distance with the goal number's distance and sum them up
        totalDistance = 0
        for i in range(len(initialState)):
            totalDistance += abs(indexInitial.get(i)[0]-indexGoal.get(i)[0]) + \
                abs(indexInitial.get(i)[1] - indexGoal.get(i)[1])

        return totalDistance


def main():
    initial = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    problem1 = SubClass(initial)
    problem2 = DuckPuzzle(initial)

    # these two functions will produce 10 puzzles each and pass them to the puzzle list
    puzzleList1 = problem1.get_ten_rand_puzzles()
    puzzleList2 = problem2.get_ten_rand_puzzles()
    # these functions will solve these 10 puzzles and record the time, #nodes being removed from the frontier and length of the solution
    print("''''''''''''''''''''''Solving the following 10 Eight-Puzzles'''''''''''''''''''''''''''''")
    for i in range(len(puzzleList1)):
        problem1.display(puzzleList1[i])
        print()
    problem1.solve_in_misplaced_tile(puzzleList1)
    problem1.solve_in_manhattan(puzzleList1)
    problem1.solve_in_max_between_misplaced_and_mahattan(puzzleList1)

    print("''''''''''''''''''''''Solving the following 10 Duck-Puzzles'''''''''''''''''''''''''''''")
    for i in range(len(puzzleList2)):
        problem2.display(puzzleList2[i])
        print()

    problem2.solve_in_misplaced_tile(puzzleList2)
    problem2.solve_in_manhattan(puzzleList2)
    problem2.solve_in_max_between_misplaced_and_mahattan(puzzleList2)


main()
