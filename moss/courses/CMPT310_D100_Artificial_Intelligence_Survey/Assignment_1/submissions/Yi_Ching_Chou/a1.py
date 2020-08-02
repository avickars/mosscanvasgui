# a1.py
# Yi Ching Chou (David)
# 301148967
# ycchou@sfu.ca

from search import *
import time, math, random

def main():
    # Compare algorithms for EightPuzzle
    compare_algorithms_on_eight_puzzle()
    # Compare algorithms for DuckPuzzle
    compare_algorithms_on_duck_puzzle()

# ______________________________________________________________________________
# Question 1

def make_rand_8puzzle():
    """
    Return a random EightPuzzle problem.
    Keep shuffling the EightPuzzle state until it is solvable.
    """
    state = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    ep = EightPuzzle(state)

    # Convert state to list to shuffle
    state_list = list(state)
    isSolvable = False
    while not isSolvable:
        random.shuffle(state_list)
        isSolvable = ep.check_solvability(state_list)

    return EightPuzzle(tuple(state_list))

def display(state):
    """Display the state of EightPuzzle in a nice format."""
    end = "\n"
    for i in range(len(state)):
        # insert new line when it is at position 2, 5, and 8
        if i % 3 == 2:
            end = "\n"
        else:
            end = " "
        print(state[i] if state[i] != 0 else "*", end=end)
# ______________________________________________________________________________

# ______________________________________________________________________________
# Question 2

def compare_algorithms_on_eight_puzzle():
    """Compare algorithms on EightPuzzle"""
    # Try increasing sample size to do better benchmarking
    num_samples = 10
    eight_puzzle_problem_list = get_8puzzle_problems(num_samples)

    # Convert EightPuzzle instances to EnhancedEightPuzzle instance so that it will have
    # - A correct misplaced heuristic to exclude the blank tile
    # - A Manhattan heuristic
    # - A max heuristic
    enhanced_8puzzle_list = []
    for eight_puzzle in eight_puzzle_problem_list:
        enhanced_8puzzle = convert_8puzzle_to_enhanced_version(eight_puzzle)
        enhanced_8puzzle_list.append(enhanced_8puzzle)

    print("-------------start of misplaced heuristic-------------")
    print("Sample size: ", num_samples)
    start_time = time.time()
    astar_misplaced_heuristic(enhanced_8puzzle_list)
    time_taken = time.time() - start_time
    print("-------------end of misplaced heuristic-------------")

    print("-------------start of Manhattan heuristic-------------")
    print("Sample size: ", num_samples)
    start_time = time.time()
    astar_manhattan_heuristic(enhanced_8puzzle_list)
    time_taken = time.time() - start_time
    print("-------------end of Manhattan heuristic-------------")

    print("-------------start of choosing max heuristics-------------")
    print("Sample size: ", num_samples)
    start_time = time.time()
    astar_max_manhattan_misplaced(enhanced_8puzzle_list)
    time_taken = time.time() - start_time
    print("-------------end of choosing max heuristics-------------")

def get_8puzzle_problems(size = 10):
    """Get a list of EightPuzzle problems"""
    problem_list = []
    # Create EightPuzzle problem instances
    for i in range(size):
        problem_list.append(make_rand_8puzzle())

    return problem_list

def convert_8puzzle_to_enhanced_version(eight_puzzle):
    """
    Convert EightPuzzle to EnhancedEightPuzzle, so that each instances
    have manhattan heuristics and max heuristics. Also, we want to
    fix the default misplaced heuristic not to include the blank tile.
    """
    return EnhancedEightPuzzle(eight_puzzle.initial, eight_puzzle.goal)

def astar_misplaced_heuristic(problem_list):
    """Use A* search with misplaced heuristic to run a list of EightPuzzle problems"""
    for i in range(len(problem_list)):
        problem = problem_list[i]
        display(problem.initial)
        start_time = time.time()
        goal_node = astar_search(problem, problem.h ,True)
        time_taken = time.time() - start_time
        print_result(time_taken, len(goal_node.solution()))

def astar_manhattan_heuristic(problem_list):
    """Use A* search with Manhattan heuristic to run a list of EightPuzzle problems"""
    for i in range(len(problem_list)):
        problem = problem_list[i]
        display(problem.initial)
        start_time = time.time()
        goal_node = astar_search(problem, problem.manhattan_heuristic, True)
        time_taken = time.time() - start_time
        print_result(time_taken, len(goal_node.solution()))

def astar_max_manhattan_misplaced(problem_list):
    """Use A* search with max value heuristic to run a list of EightPuzzle problems"""
    for i in range(len(problem_list)):
        problem = problem_list[i]
        display(problem.initial)
        start_time = time.time()
        goal_node = astar_search(problem, problem.max_manhattan_misplaced, True)
        time_taken = time.time() - start_time
        print_result(time_taken, len(goal_node.solution()))

def print_result(time, len_solution):
    """Print out the length of solution and time taken for the problem"""
    print("The length of the solution: ", len_solution)
    print("Time taken for this problem: ", time, "s")
    print("")

class EnhancedEightPuzzle(EightPuzzle):
    """
    EnhancedEightPuzzle implements
    - A correct misplaced heuristic to exclude the blank tile
    - A Manhattan heuristic
    - A max heuristic
    """
    def h(self, node):
        """This misplaced heuristic is fixed to exclude the blank tile"""
        num_misplaced = 0
        for i in range(len(node.state)):
            # Skip blank tile
            if node.state[i] == 0:
                continue
            if node.state[i] != self.goal[i]:
                num_misplaced = num_misplaced + 1
        return num_misplaced

    def manhattan_heuristic(self, node):
        """Return the Mahattan distance for a given node"""
        len_row = 3;
        manhattan_distance = 0
        for i in range(len(node.state)):
            # Skip blank tile
            if node.state[i] == 0:
                continue
            goal_position = self.goal.index(node.state[i])
            goal_row = math.floor(goal_position / len_row)
            goal_col = goal_position % len_row

            # i represents the current position
            current_row = math.floor(i / len_row)
            current_col = i % len_row

            row_distance = abs(goal_row - current_row)
            col_distance = abs(goal_col - current_col)

            manhattan_distance = manhattan_distance + row_distance + col_distance

        return manhattan_distance

    def max_manhattan_misplaced(self, node):
        """Return the max of Manhattan distance and misplaced tiles"""
        return max(self.manhattan_heuristic(node), self.h(node))
# ______________________________________________________________________________

# ______________________________________________________________________________
# Question 3

def compare_algorithms_on_duck_puzzle():
    """Compare algorithms on DuckPuzzle"""
    print("---------DuckPuzzle Compare---------")
    num_samples = 10
    problem_list = get_duck_puzzle_problems(num_samples)

    print("-------------start of DuckPuzzle misplaced heuristic-------------")
    print("Sample size: ", num_samples)
    start_time = time.time()
    astar_duck_puzzle_misplaced(problem_list)
    time_taken = time.time() - start_time
    print("-------------end of DuckPuzzle misplaced heuristic-------------")

    print("-------------start of DuckPuzzle manhattan heuristic-------------")
    print("Sample size: ", num_samples)
    start_time = time.time()
    astar_duck_puzzle_manhattan(problem_list)
    time_taken = time.time() - start_time
    print("-------------end of DuckPuzzle misplaced heuristic-------------")

    print("-------------start of DuckPuzzle max heuristic-------------")
    print("Sample size: ", num_samples)
    start_time = time.time()
    astar_duck_puzzle_max_heuristic(problem_list)
    time_taken = time.time() - start_time
    print("-------------end of DuckPuzzle max heuristic-------------")

def make_rand_duck_puzzle():
    """Make random DuckPuzzle by applying random legal moves"""
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    dp = DuckPuzzle(state)
    # Make random moves to create a random DuckPuzzle
    num_moves = random.randint(1000, 9999)
    for i in range(num_moves):
        available_actions = dp.actions(dp.initial)
        random_move = available_actions[random.randint(0, len(available_actions) - 1)]
        dp.initial = dp.result(dp.initial, random_move)
    return dp

def display_duck_puzzle(state):
    """Display the state of DuckPuzzle in a nice format"""
    end_of_row_positions = (1, 5, 8)
    empty_after_position = 5
    
    for i in range(len(state)):
        if i in end_of_row_positions:
            print(state[i] if state[i] != 0 else "*", end = "\n")
        else:
            print(state[i] if state[i] != 0 else "*", end = " ")
        if i == empty_after_position:
            print(" ", end = " ")

def get_duck_puzzle_problems(size = 10):
    """Get a list of DuckPuzzle problems"""
    problem_list = []
    for i in range(size):
        problem_list.append(make_rand_duck_puzzle())
    return problem_list

def astar_duck_puzzle_misplaced(problem_list):
    """Use A* search with misplaced heuristic to run a list of DuckPuzzle problems"""
    for i in range(len(problem_list)):
        problem = problem_list[i]
        display_duck_puzzle(problem.initial)
        start_time = time.time()
        goal_node = astar_search(problem, problem.misplaced_heuristic, True)
        time_taken = time.time() - start_time
        print_result(time_taken, len(goal_node.solution()))
 
def astar_duck_puzzle_manhattan(problem_list):
    """Use A* search with Manhattan heuristic to run a list of DuckPuzzle problems"""
    for i in range(len(problem_list)):
        problem = problem_list[i]
        display_duck_puzzle(problem.initial)
        start_time = time.time()
        goal_node = astar_search(problem, problem.manhattan_heuristic ,True)
        time_taken = time.time() - start_time
        print_result(time_taken, len(goal_node.solution()))

def astar_duck_puzzle_max_heuristic(problem_list):
    """Use A* search with max value heuristic to run a list of DuckPuzzle problems"""
    for i in range(len(problem_list)):
        problem = problem_list[i]
        display_duck_puzzle(problem.initial)
        start_time = time.time()
        goal_node = astar_search(problem, problem.max_misplaced_manhattan_heuristic ,True)
        time_taken = time.time() - start_time
        print_result(time_taken, len(goal_node.solution()))

class DuckPuzzle(Problem):
    """
    The implementation of DuckPuzzle problem.
    """
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)
    
    def find_blank_square(self, state):
        return state.index(0)
    
    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        # Predefined non-available actions for each positions
        positions_no_left_actions = (0, 2, 6)
        positions_no_right_actions = (1, 5, 8)
        positions_no_up_actions = (0, 1, 4, 5)
        positions_no_down_actions = (2, 6, 7 ,8)

        # Check and remove non-available actions
        if index_blank_square in positions_no_left_actions:
            possible_actions.remove('LEFT')
        if index_blank_square in positions_no_right_actions:
            possible_actions.remove('RIGHT')
        if index_blank_square in positions_no_up_actions:
            possible_actions.remove('UP')
        if index_blank_square in positions_no_down_actions:
            possible_actions.remove('DOWN')
        return possible_actions

    def swap_tiles(self, state_list, source, target):
        temp = state_list[source]
        state_list[source] = state_list[target]
        state_list[target] = temp
    
    def result(self, state, action):
        # The last position of each rows
        end_of_first_row = 1
        end_of_second_row = 5
        
        # Convert tuple to list so that we can swap tiles
        state_list = list(state)
        index_blank_square = self.find_blank_square(state_list)
        
        if action == 'UP':
            # If the blank is in the second row
            if index_blank_square > end_of_first_row and index_blank_square <= end_of_second_row:
                neighbor_offset = -2
            # If the blank is in the third row
            elif index_blank_square > end_of_second_row:
                neighbor_offset = -3

        elif action == 'DOWN':
            # If the blank is in the first row
            if index_blank_square <= end_of_first_row:
                neighbor_offset = 2
            # If the blank is in the second row
            elif index_blank_square > end_of_first_row and index_blank_square <= end_of_second_row:
                neighbor_offset = 3
            
        elif action == 'LEFT':
            neighbor_offset = -1

        elif action == 'RIGHT':
            neighbor_offset = 1

        index_neighbor = index_blank_square + neighbor_offset
        self.swap_tiles(state_list, index_blank_square, index_neighbor)
            
        return tuple(state_list)

    def goal_test(self, state):
        return state == self.goal

    def misplaced_heuristic(self, node):
        num_misplaced = 0
        for i in range(len(node.state)):
            # Skip blank tile
            if node.state[i] == 0:
                continue
            if node.state[i] != self.goal[i]:
                num_misplaced = num_misplaced + 1
        return num_misplaced

    def manhattan_heuristic(self, node):
        # We can treat this shape as a 4x3 matrix, while some tiles are non-movable
        # In this way, it is easier to calculate their vertical and horizontal distances
        len_row = 4
        
        # Map each position to the positions of 4x3 matrix
        # Original position : new 4x3 position
        position_map = {
            0: 0,
            1: 1,
            2: 4,
            3: 5,
            4: 6,
            5: 7,
            6: 9,
            7: 10,
            8: 11
        }
        
        state = node.state
        manhattan_distance = 0
        for i in range(len(state)):
            # Skip blank tile
            if state[i] == 0:
                continue
            # Map position to 4x3 matrix position
            current_position = position_map[i]
            goal_position = position_map[self.goal.index(state[i])]

            current_row = math.floor(current_position / len_row)
            current_col = current_position % len_row

            goal_row = math.floor(goal_position / len_row)
            goal_col = goal_position % len_row

            row_distance = abs(goal_row - current_row)
            col_distance = abs(goal_col - current_col)

            manhattan_distance = manhattan_distance + row_distance + col_distance

        return manhattan_distance

    def max_misplaced_manhattan_heuristic(self, node):
        return max(self.misplaced_heuristic(node), self.manhattan_heuristic(node))

# ______________________________________________________________________________

if __name__ == '__main__':
    main()