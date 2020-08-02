# a1.py

from search import *
import time
# ...


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
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            num_explored = len(explored)
            return node, num_explored, node.depth  #num_explored holds all nodes removed from frontire and depth is
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

    def manhattan_distance(self, node):
        """My implementation"""
        goalCR = {}
        for i in range(0,9):    #create a dictionary of coordinates where the tile should be
            if(self.goal[i]==0):
                continue       #skip the blank square to make admissable

            col = i%3
            row = int(i/3)
            goalCR[self.goal[i]] = (col,row)
        sum =0
        for i in range(0,9):    #manhattan distance can be calculated by difference of X and Y coordinates
            if(node.state[i]==0):
                continue       #skip the blank square to make admissable

            col = i%3
            row = int(i/3)
            sum += abs(col-goalCR[node.state[i]][0]) + abs(row-goalCR[node.state[i]][1])
        return sum

    def max_heuristic(self, node):
        """My implementation"""
        return max(self.h(node),self.manhattan_distance(node))

class HousePuzzle(Problem):
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
        """ MODIFIED: Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """
        top_indices = (0,1,4,5)
        bottom_indices = (2,6,7,8)
        left_indices = (0,2,6)
        right_indices = (1,5,8)
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square in left_indices:
            possible_actions.remove('LEFT')
        if index_blank_square in top_indices:
            possible_actions.remove('UP')
        if index_blank_square in right_indices:
            possible_actions.remove('RIGHT')
        if index_blank_square in bottom_indices:
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


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan_distance(self, node):
        """My implementation"""
        goalCR = {}
        for i in range(0,9):
            if(self.goal[i]==0):
                continue       #skip the blank square to make admissable

            col = i%3
            row = int(i/3)
            goalCR[self.goal[i]] = (col,row)
        sum =0
        for i in range(0,9):
            if(node.state[i]==0):
                continue       #skip the blank square to make admissable
            col = i%3
            row = int(i/3)
            sum += abs(col-goalCR[node.state[i]][0]) + abs(row-goalCR[node.state[i]][1])
        return sum

    def max_heuristic(self, node):
        """My implementation"""
        return max(self.h(node),self.manhattan_distance(node))



def make_rand_8puzzle():
    state = (1,2,3,4,5,6,7,8,0)
    goal = (1,2,3,4,5,6,7,8,0)
    randomPuzzle = EightPuzzle(state,goal)
    for i in range(0,100):
        actions = randomPuzzle.actions(state)
        index = int(random.random()*len(actions))
        state = randomPuzzle.result(state,actions[index])
    if(randomPuzzle.check_solvability(state)):
        return EightPuzzle(state,goal)
    else:
        print("unsolvable\n")

def make_rand_housepuzzle():
    state = (1,2,3,4,5,6,7,8,0)
    goal = (1,2,3,4,5,6,7,8,0)
    randomPuzzle = HousePuzzle(state,goal)
    for i in range(0,100):
        actions = randomPuzzle.actions(state)
        index = int(random.random()*len(actions))
        state = randomPuzzle.result(state,actions[index])
    return HousePuzzle(state,goal)

def display(state):
    printStr = ""
    for i in range(0,9):
        if(i%3==0):
            printStr = printStr+"\n"
        if(state[i]==0):
            printStr = printStr+"*"+" "
        else:
            printStr = printStr+str(state[i])+" "
    print(printStr)

'''def manhattan_distance(node):
    "version that doesn't take into account the goal, real version is in search.py"
    ones_mask = (0, 1, 2, 1,  2,  3, 2,  3,  4)
    twos_mask = (1, 0, 1, 2,  1,  2, 3,  2,  3)
    threes_mask = (2,  1,  0,  3,  2,  1,  4,  3,  2)
    fours_mask =(1,  2,  3,  0,  1,  2,  1,  2,  3)
    fives_mask =(2,  1,  2,  1,  0,  1,  2,  1,  2)
    sixs_mask =(3,  2,  1,  2,  1,  0,  3,  2,  1)
    sevens_mask =(2,  3,  4,  1,  2,  3,  0,  1,  2)
    eights_mask =(3,  2,  3,  2,  1,  2,  1,  0,  1)
    nines_mask =(4,  3,  2,  3,  2,  1,  2,  1,  0)

    mask_list = (ones_mask, twos_mask, threes_mask, fours_mask, fives_mask, sixs_mask, sevens_mask, eights_mask, nines_mask)
    sum = 0
    for i in range(0,9):
        if(node.state[i]==0):
            sum+= mask_list[8][i]
        else:
            sum += mask_list[node.state[i]-1][i]
    return sum'''



def main():
    list_of_puzzles = []
    for i in range(0,100):
        puzzle = make_rand_8puzzle()
        list_of_puzzles.append(puzzle)


    num_moves_list = []
    num_nodes_list = []

    start_time = time.time()        #max heuristic
    for i in range(0,10):
        solution, num_nodes, num_moves = astar_search(list_of_puzzles[i], h =list_of_puzzles[i].max_heuristic )
        print(solution)
        num_moves_list.append(num_moves)
        num_nodes_list.append(num_nodes)
    elapsed_time = time.time() - start_time
    print(f'Max of Manhattan and Misplaced tile heuristic, elapsed time (in seconds): {elapsed_time}s')
    print(num_moves_list)
    print(sum(num_moves_list) / len(num_moves_list) )
    print(min(num_moves_list))
    print(max(num_moves_list))
    print(num_nodes_list)
    print(sum(num_nodes_list) / len(num_nodes_list) )
    print(min(num_nodes_list))
    print(max(num_nodes_list))
    num_moves_list.clear()
    num_nodes_list.clear()

    start_time = time.time()        #manhattan heuristic
    for i in range(0,10):
        solution, num_nodes, num_moves = astar_search(list_of_puzzles[i], h =list_of_puzzles[i].manhattan_distance )
        print(solution)
        num_moves_list.append(num_moves)
        num_nodes_list.append(num_nodes)
    elapsed_time = time.time() - start_time
    print(f'Manhattan heuristic, elapsed time (in seconds): {elapsed_time}s')
    print(num_moves_list)
    print(sum(num_moves_list) / len(num_moves_list) )
    print(min(num_moves_list))
    print(max(num_moves_list))
    print(num_nodes_list)
    print(sum(num_nodes_list) / len(num_nodes_list) )
    print(min(num_nodes_list))
    print(max(num_nodes_list))
    num_moves_list.clear()
    num_nodes_list.clear()

    start_time = time.time()        #default heuristic
    for i in range(0,10):
        solution, num_nodes, num_moves = astar_search(list_of_puzzles[i])
        print(solution)
        num_moves_list.append(num_moves)
        num_nodes_list.append(num_nodes)
    elapsed_time = time.time() - start_time
    print(f'Misplaced tile heuristic, elapsed time (in seconds): {elapsed_time}s')
    print(num_moves_list)
    print(sum(num_moves_list) / len(num_moves_list) )
    print(min(num_moves_list))
    print(max(num_moves_list))
    print(num_nodes_list)
    print(sum(num_nodes_list) / len(num_nodes_list) )
    print(min(num_nodes_list))
    print(max(num_nodes_list))
    num_moves_list.clear()
    num_nodes_list.clear()


if __name__ == "__main__":
    main()
