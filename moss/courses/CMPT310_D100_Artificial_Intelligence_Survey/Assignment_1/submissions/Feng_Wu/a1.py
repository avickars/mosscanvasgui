import numpy as np
import time
import random
from search import *


class EightPuzzle(Problem):
    """Modified Eight Puzzle class with new heuristics functions"""

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
        h(n) = number of misplaced tiles, not including empty space in our calculation """
        non_zero_node_state = list(node.state)
        non_zero_node_state.remove(0)
        non_zero_node_state = tuple(non_zero_node_state)
        non_zero_goal = list(self.goal)
        non_zero_goal.remove(0)
        non_zero_goal = tuple(non_zero_goal)
        return sum(s != g for (s, g) in zip(non_zero_node_state, non_zero_goal))

    def manhattan(self, node):
        """Modified heuristics function: Manhattan distance"""
        """
        Referred to the link below for information on how to calculate Manhattan distance
        https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
        """
        total_length = 0
        for i in range(1,9):
            state_index = node.state.index(i)
            goal_index = self.goal.index(i)
            length = abs(state_index%3 - goal_index%3) + abs(state_index//3 - goal_index//3)
            total_length = total_length + length
        return total_length

    def max_tile_manhattan(self, node):
        """Modified heuristics function: Max tile heuristic and Manhattan distance"""
        manhattan_total_length = 0
        for i in range(1,9):
            state_index = node.state.index(i)
            goal_index = self.goal.index(i)
            length = abs(state_index%3 - goal_index%3) + abs(state_index//3 - goal_index//3)
            manhattan_total_length = manhattan_total_length + length
        non_zero_node_state = list(node.state)
        non_zero_node_state.remove(0)
        non_zero_node_state = tuple(non_zero_node_state)
        non_zero_goal = list(self.goal)
        non_zero_goal.remove(0)
        non_zero_goal = tuple(non_zero_goal)
        misplaced_tiles = sum(s != g for (s, g) in zip(non_zero_node_state, non_zero_goal))
        return max(misplaced_tiles, manhattan_total_length)

class DuckPuzzle(Problem):
    """Duck puzzle class with new heuristics functions"""

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

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        elif index_blank_square == 1:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        elif index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif index_blank_square == 4:
            possible_actions.remove('UP')
        elif index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        elif index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif index_blank_square == 7:
            possible_actions.remove('DOWN')
        elif index_blank_square == 8:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')
        
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        # modification so satisfy duck puzzle delta
        if blank >= 0 and blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif blank > 3:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles, not including empty space in our calculation """
        non_zero_node_state = list(node.state)
        non_zero_node_state.remove(0)
        non_zero_node_state = tuple(non_zero_node_state)
        non_zero_goal = list(self.goal)
        non_zero_goal.remove(0)
        non_zero_goal = tuple(non_zero_goal)
        return sum(s != g for (s, g) in zip(non_zero_node_state, non_zero_goal))

    def manhattan(self, node):
        """Modified heuristics function: Manhattan distance"""
        """
        Referred to the link below for information on how to calculate Manhattan distance
        https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
        """
        total_length = 0
        for i in range(1,9):
            state_index = node.state.index(i)
            goal_index = self.goal.index(i)
            length = abs(state_index%3 - goal_index%3) + abs(state_index//3 - goal_index//3)
            total_length = total_length + length
        return total_length

    def max_tile_manhattan(self, node):
        """Modified heuristics function: Max tile heuristic and Manhattan distance"""
        manhattan_total_length = 0
        for i in range(1,9):
            state_index = node.state.index(i)
            goal_index = self.goal.index(i)
            length = abs(state_index%3 - goal_index%3) + abs(state_index//3 - goal_index//3)
            manhattan_total_length = manhattan_total_length + length
        non_zero_node_state = list(node.state)
        non_zero_node_state.remove(0)
        non_zero_node_state = tuple(non_zero_node_state)
        non_zero_goal = list(self.goal)
        non_zero_goal.remove(0)
        non_zero_goal = tuple(non_zero_goal)
        misplaced_tiles = sum(s != g for (s, g) in zip(non_zero_node_state, non_zero_goal))
        return max(misplaced_tiles, manhattan_total_length)
    
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    start_time = time.time()
    h = memoize(h or problem.h, 'h')
    node, nodes_removed, length = best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
    elapsed_time = time.time() - start_time
    print(f'Total elapsed time (in seconds): {elapsed_time}s')
    print('The total number of nodes that were removed from frontier:', nodes_removed)
    print('The length of the solution:', length )
    return node

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
    nodes_removed = 0
    while frontier:
        node = frontier.pop()
        nodes_removed += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, nodes_removed, len(node.solution())
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, nodes_removed, None

def make_rand_duck_puzzle():
    initial = (1,2,3,4,5,6,7,8,0)
    test_puzzle = DuckPuzzle(initial)
    for index in range(0,1000):
        possible_actions = test_puzzle.actions(test_puzzle.initial)
        random_action = possible_actions[random.randint(0,len(possible_actions)-1)]
        result = test_puzzle.result(test_puzzle.initial, random_action)
        test_puzzle.initial = result
    final_randomized_puzzle = DuckPuzzle(test_puzzle.initial)
    return final_randomized_puzzle


def make_rand_8puzzle():
    """Makes a random 3x3 puzzle"""
    flag = False
    while flag == False:
        random_generated = tuple(np.random.permutation(9))
        test_puzzle = EightPuzzle(initial = random_generated)
        result = test_puzzle.check_solvability(random_generated)
        if result == True:
            return test_puzzle


def display(state):
    """displays the puzzle state in 3x3 format"""
    state_list = list(state)
    for index, value in enumerate(state):
        if value == 0:
            state_list[index] = '*'
    print(state_list[0], state_list[1], state_list[2])
    print(state_list[3], state_list[4], state_list[5])
    print(state_list[6], state_list[7], state_list[8],'\n')

def display_duck(state):
    """displays the duck puzzle state """
    state_list = list(state)
    for index, value in enumerate(state):
        if value == 0:
            state_list[index] = '*'
    print(state_list[0], state_list[1])
    print(state_list[2], state_list[3], state_list[4], state_list[5])
    print(' ',state_list[6], state_list[7], state_list[8], '\n')


if __name__ == "__main__":
    #Actual program
    number_of_test = 10
    for i in range(0,number_of_test):
        print('3x3 puzzle',i+1, '\n' )
        random_puzzle = make_rand_8puzzle()
        display(random_puzzle.initial)
        print('Misplaced tile heuristic:')
        astar_search(random_puzzle)
        print('Manhattan heuristic:')
        astar_search(random_puzzle, h=random_puzzle.manhattan)
        print('Max heuristic:')
        astar_search(random_puzzle, h=random_puzzle.max_tile_manhattan)
        print('\n')

    for j in range(0,number_of_test):
        print('duck puzzle',j+1, '\n' )
        random_puzzle = make_rand_duck_puzzle()
        display_duck(random_puzzle.initial)
        print('Misplaced tile heuristic:')
        astar_search(random_puzzle)
        print('Manhattan heuristic:')
        astar_search(random_puzzle, h=random_puzzle.manhattan)
        print('Max heuristic:')
        astar_search(random_puzzle, h=random_puzzle.max_tile_manhattan)
        print('\n')

