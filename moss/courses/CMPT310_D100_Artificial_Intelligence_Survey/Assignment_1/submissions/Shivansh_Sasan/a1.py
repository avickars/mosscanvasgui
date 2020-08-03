#Shivansh Sasan
#301329132

# a1.py

#from search import *
from utils import *
import random
import time

global remFront

# Question 1
#=====================================================================================

class Problem:

    def __init__(self, initial, goal=None):

        self.initial = initial
        self.goal = goal

    def actions(self, state):

        raise NotImplementedError

    def result(self, state, action):

        raise NotImplementedError

    def goal_test(self, state):

        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):

        return c + 1

    def value(self, state):

        raise NotImplementedError

# ______________________________________________________________________________


class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):

        return hash(self.state)

def best_first_graph_search(problem, f, display=False):

    f = memoize(f, 'f')
    node = Node(problem.initial)
    remFront = 0
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        remFront += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print('Removed nodes from frontier: ',remFront)
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    print('Removed nodes from frontier: ',remFront)
    return None

# A* with misplaced tiles
def astar_search(problem, h=None, display=False):

    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# A* with manhattan distance heuristic
def astar_search_man(problem, h=None, display=False):

    h = memoize(h or problem.manH, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

# A* with maximum of the two heuristic
def astar_search_max(problem, h=None, display=False):

    h = memoize(h or problem.maxH, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

class EightPuzzle(Problem):

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

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    #implemet the manhattan distance heuristic
    def manH(self, node):
        man = [
        [4,3,2,3,2,1,2,1,0], #0
        [0,1,2,1,2,3,2,3,4],
        [1,0,1,2,1,2,3,2,3],
        [2,1,0,3,2,1,4,3,2],
        [1,2,3,0,1,2,1,2,3],
        [2,1,2,1,0,1,2,1,2],
        [3,2,1,2,1,0,3,2,1],
        [2,3,4,1,2,3,0,1,2],
        [3,2,3,2,1,2,1,0,1], #8
        ]

        state = node.state
        i = 0
        maa = 0
        for i in range(1,9):
            maa += man[i][state.index(i)]
        return maa

    #implemet the maximum heuristic
    def maxH (self,node):
        return max(self.h(node), self.manH(node))

class DuckPuzzle(Problem):
    # Duck puzzle

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_duck_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_duck_actions.remove('UP')
            possible_duck_actions.remove('LEFT')
        if index_blank_square == 1:
            possible_duck_actions.remove('UP')
            possible_duck_actions.remove('RIGHT')
        if index_blank_square == 2:
            possible_duck_actions.remove('DOWN')
            possible_duck_actions.remove('LEFT')
        if index_blank_square == 3:
            return possible_duck_actions
        if index_blank_square == 4:
            possible_duck_actions.remove('UP')
        if index_blank_square == 5:
            possible_duck_actions.remove('UP')
            possible_duck_actions.remove('RIGHT')
        if index_blank_square == 6:
            possible_duck_actions.remove('DOWN')
            possible_duck_actions.remove('LEFT')
        if index_blank_square == 7:
            possible_duck_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_duck_actions.remove('DOWN')
            possible_duck_actions.remove('RIGHT')
        return tuple(possible_duck_actions)

    def result(self, state, action):
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        if blank > 3:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

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
        #number of misplaced tiles
        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manH(self, node):
        man = [
        [5,4,4,3,2,1,2,1,0], #0
        [0,1,1,2,3,4,3,4,5],
        [1,0,2,1,2,3,2,3,4],
        [1,2,0,1,2,3,2,3,4],
        [2,1,1,0,1,2,1,2,3],
        [3,2,2,1,0,1,2,1,2],
        [4,3,3,2,1,0,3,2,1],
        [3,2,2,1,2,3,0,1,2],
        [4,3,3,2,1,2,1,0,1], #8
        ]

        state = node.state
        i = 0
        maa = 0
        for i in range(1,9):
            maa += man[i][state.index(i)]
        return maa

    def maxH (self,node):
        return max(self.h(node), self.manH(node))

#=====================================================================================

def make_rand_8puzzle():
    lst = random.sample(range(0,9),9)
    tup = tuple(lst)
    thePuzzle = EightPuzzle(tup)

    while(not thePuzzle.check_solvability(thePuzzle.initial)):
        tup = random.sample(range(0,9),9)
        tup = tuple(tup)

        thePuzzle = EightPuzzle(tup)
    
    return thePuzzle

#duck puzzle randomly generated through random actions on the goal state
def make_rand_duck_puzzle():
    dPuz = DuckPuzzle((1,2,3,4,5,6,7,8,0))

    randMoves = random.randint(10,250)

    randomiser = 0
    while randomiser < randMoves:
        act = dPuz.actions(dPuz.initial)
        dPuz.initial = dPuz.result(dPuz.initial, random.choice((act)))
        randomiser += 1
    
    return dPuz

def display(state):
    i = 0
    while i < 9:
        tempState = (state[i], state[i+1], state[i+2])

        if 0 in tempState:
            tempStateList = list(tempState)
            tempStateList[tempStateList.index(0)] = '*'
            tempState = tuple(tempStateList)
        #print(tempState[0]," ",tempState[1]," ", tempState[2])
        print(tempState[0],tempState[1], tempState[2])
        i += 3

def displayDuck(state):

    zeroIndex = state.index(0)

    if zeroIndex <=1:
        if zeroIndex == 0:
            print('*',state[1])
        else:
            print(state[0],'*')
        
        print(state[2],state[3],state[4],state[5])
        print(' ',state[6],state[7],state[8])
        return

    if zeroIndex <= 5 and zeroIndex > 1:
        print(state[0],state[1])
        if zeroIndex == 2:
            print('*',state[3],state[4],state[5])
        if zeroIndex == 3:
            print(state[2],'*',state[4],state[5])
        if zeroIndex == 4:
            print(state[2],state[3],'*',state[5])
        if zeroIndex == 5:
            print(state[2],state[3],state[4],'*')
        print(' ',state[6],state[7],state[8])
        return

    if zeroIndex <= 8 and zeroIndex > 5:
        print(state[0],state[1])
        print(state[2],state[3],state[4],state[5])
        if zeroIndex == 6:
            print(' ','*',state[7],state[8])
        if zeroIndex == 7:
            print(' ',state[6],'*',state[8])
        if zeroIndex == 8:
            print(' ',state[6],state[7],'*')
        return

def main():

    """
    Function Names:

    make_rand_8puzzle()
    display(tuple)

    make_rand_duck_puzzle() #duck puzzle randomly generated through random actions on the goal state
    displayDuck(tuple)      #use this fucntion to display duck puzzle

    astar_search()          #default A*
    astar_search_man()      # A* with manhattan
    astar_search_max()      # A* with maximum heuristic

    """

    print('===========  8 puzzles  ===========')
    totalMisplacedTime_8 = 0
    totalManhattanTime_8 = 0
    totalMaxTime_8 = 0

    misplacedTimes_8 = []
    manhattanTimes_8 = []
    maxTimes_8 = []

    cases = 0

    while cases < 10:
        print('====== Random Case #', cases+1,' ======')

        randPuz = make_rand_8puzzle()
        display(randPuz.initial)

        print("====  MISPLACED TILE HEURISTIC ====")
        misTime1 = time.time()
        randPuzSol_mis = astar_search(randPuz).solution()
        misTime2 = time.time() - misTime1
        print('Time Elapsed with misplaced tile: ', misTime2)
        misplacedTimes_8.append(misTime2)
        totalMisplacedTime_8 += misTime2
        print('The length of the solution: ', len(randPuzSol_mis))

        print("\n==== MANHATTAN HEURISTIC ====")
        manTime1 = time.time()
        randPuzSol_man = astar_search_man(randPuz).solution()
        manTime2 = time.time() - manTime1
        print('Time Elapsed with MANHATTAN heuristic: ', manTime2)
        manhattanTimes_8.append(manTime2)
        totalManhattanTime_8 += manTime2
        print('The length of the solution: ', len(randPuzSol_man))

        print("\n=====  MAX OF THE HEURISTICS =====")
        maxTime1 = time.time()
        randPuzSol_max = astar_search_max(randPuz).solution()
        maxTime2 = time.time() - maxTime1
        print('Time Elapsed with MANHATTAN heuristic: ', maxTime2)
        totalMaxTime_8 += maxTime2
        maxTimes_8.append(maxTime2)
        print('The length of the solution: ', len(randPuzSol_max))

        print('\n')

        cases += 1

    print('===========  DUCK puzzles  ===========')

    totalMisplacedTime_duck = 0
    totalManhattanTime_duck = 0
    totalMaxTime_duck = 0

    misplacedTimes_duck = []
    manhattanTimes_duck = []
    maxTimes_duck = []

    cases = 0

    while cases < 10:
        print('====== Random Case #', cases+1,' ======')

        randPuz = make_rand_duck_puzzle()
        displayDuck(randPuz.initial)

        print("====  MISPLACED TILE HEURISTIC ====")
        misTime1 = time.time()
        randPuzSol_mis = astar_search(randPuz).solution()
        misTime2 = time.time() - misTime1
        print('Time Elapsed with misplaced tile: ', misTime2)
        misplacedTimes_duck.append(misTime2)
        totalMisplacedTime_duck += misTime2
        print('The length of the solution: ', len(randPuzSol_mis))

        print("\n==== MANHATTAN HEURISTIC ====")
        manTime1 = time.time()
        randPuzSol_man = astar_search_man(randPuz).solution()
        manTime2 = time.time() - manTime1
        print('Time Elapsed with MANHATTAN heuristic: ', manTime2)
        manhattanTimes_duck.append(manTime2)
        totalManhattanTime_duck += manTime2
        print('The length of the solution: ', len(randPuzSol_man))

        print("\n=====  MAX OF THE HEURISTICS =====")
        maxTime1 = time.time()
        randPuzSol_max = astar_search_max(randPuz).solution()
        maxTime2 = time.time() - maxTime1
        print('Time Elapsed with MANHATTAN heuristic: ', maxTime2)
        totalMaxTime_duck += maxTime2
        maxTimes_duck.append(maxTime2)
        print('The length of the solution: ', len(randPuzSol_max))

        print('\n')

        cases += 1

    print('=====   RESULTS   ======\n')
    
    print(' ====  8 puzzle  ====')
    print('Total time over 10 puzzles by MISPLACED Tiles: ', totalMisplacedTime_8)
    print('Total time over 10 puzzles by MANHATTAN Tiles: ', totalManhattanTime_8)
    print('Total time over 10 puzzles by MAX heuristic: ', totalMaxTime_8)

    print('\n ====All values====')
    print('All manhattan times: ', manhattanTimes_8)
    print('All misplaced tiles times: ', misplacedTimes_8)
    print('All MAX times: ', maxTimes_8)


    print('DUCK puzzle: ')
    print('Total time over 10 puzzles by MISPLACED Tiles: ', totalMisplacedTime_duck)
    print('Total time over 10 puzzles by MANHATTAN Tiles: ', totalManhattanTime_duck)
    print('Total time over 10 puzzles by MAX heuristic: ', totalMaxTime_duck)

    print('\n ====All values====')
    print('All misplaced tiles times: ', misplacedTimes_duck)
    print('All manhattan times: ', manhattanTimes_duck)
    print('All MAX times: ', maxTimes_duck)


if __name__ == "__main__":
    main()