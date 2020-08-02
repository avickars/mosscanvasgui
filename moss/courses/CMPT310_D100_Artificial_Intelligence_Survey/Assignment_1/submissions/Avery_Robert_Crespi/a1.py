# =============================================================================
# a1.py
# =============================================================================

from search import memoize, Node, Problem, PriorityQueue

from collections import namedtuple  # For Solution type.
import csv  # For saving results.
import random  # For randomizing state.
import time  # For timing code.
from typing import Callable, Tuple, List  # For type annotations.

SEED = 0xACE
NUM_PUZZLES = 10
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
Solution = namedtuple("Solution", ("tiles_moved", "nodes_removed", "time"))
State = Tuple[int, ...]

# =============================================================================
# Copied from search.py and modified
# =============================================================================


def best_first_graph_search(problem: Problem, f: Callable) -> Solution:
    """Copied from search.py and modified."""
    f = memoize(f, "f")
    start_time = time.time()  # Start the timer.
    node = Node(problem.initial)
    node.tiles_moved = 0  # Store the number of tiles moved in the node.
    frontier = PriorityQueue("min", f)
    frontier.append(node)
    nodes_removed = 0  # Track the number of nodes removed from the frontier.
    explored = set()
    while frontier:
        node = frontier.pop()
        nodes_removed += 1  # Increment nodes removed.
        if problem.goal_test(node.state):
            end_time = time.time()  # End the timer.
            return Solution(
                tiles_moved=node.tiles_moved,
                nodes_removed=nodes_removed,
                time=round(end_time - start_time, 5),
            )
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                child.tiles_moved = node.tiles_moved + 1  # Increment tiles moved.
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    child.tiles_moved = node.tiles_moved + 1  # Increment tiles moved.
                    frontier.append(child)
    assert False, "No solution found!"


def astar_search(problem: Problem, h: Callable) -> Solution:
    """Copied from search.py and modified."""
    h = memoize(h, "h")
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


class EightPuzzle(Problem):
    """Copied from search.py and modified."""

    def __init__(self, initial: State, goal: State = GOAL_STATE):
        super().__init__(initial, goal)

    def find_blank_square(self, state: State) -> int:
        """Find the index of the blank square."""
        return state.index(0)

    def actions(self, state: State) -> List[str]:
        """Return the list of possible actions."""
        possible_actions = ["UP", "DOWN", "LEFT", "RIGHT"]
        blank = self.find_blank_square(state)
        if blank % 3 == 0:
            possible_actions.remove("LEFT")
        if blank < 3:
            possible_actions.remove("UP")
        if blank % 3 == 2:
            possible_actions.remove("RIGHT")
        if blank > 5:
            possible_actions.remove("DOWN")
        return possible_actions

    def result(self, state: State, action: str) -> State:
        """Apply an action to a state."""
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta = {"UP": -3, "DOWN": 3, "LEFT": -1, "RIGHT": 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        return tuple(new_state)

    def goal_test(self, state: State) -> bool:
        """Test if the goal has been reached."""
        return state == self.goal

    def check_solvability(self, state: State) -> bool:
        """Check if the puzzle is solvable."""
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1
        return inversion % 2 == 0

    def misplaced_tiles(self, node: Node) -> int:
        """Compute the misplaced tiles heuristic."""
        # Don't count the blank tile.
        return sum(s != g for (s, g) in zip(node.state, self.goal) if s != 0)

    def manhattan_distance(self, node: Node) -> int:
        """Compute the Manhattan distance heuristic."""
        dist = 0
        # Don't count the blank tile.
        for n in range(1, 9):
            goalIndex = self.goal.index(n)
            goalRow, goalCol = goalIndex // 3, goalIndex % 3
            stateIndex = node.state.index(n)
            stateRow, stateCol = stateIndex // 3, stateIndex % 3
            dist += abs(goalRow - stateRow) + abs(goalCol - stateCol)
        return dist


# =============================================================================
# Question 1: Helper Functions
# =============================================================================


def make_rand_8puzzle() -> EightPuzzle:
    """Return a random instance of an EightPuzzle that is solvable."""
    puzzle = EightPuzzle(list(range(9)))
    # Repeatedly shuffle the initial state until it becomes solveable.
    # On average, 2 shuffles will be required because 50% of states are solveable.
    random.shuffle(puzzle.initial)
    while not puzzle.check_solvability(puzzle.initial):
        random.shuffle(puzzle.initial)
    puzzle.initial = tuple(puzzle.initial)
    return puzzle


def display(state: State):
    """Print a neat representation of an EightPuzzle state."""
    # Convert digits to strings, with special case for 0.
    pretty = [str(n) if n != 0 else "*" for n in state]
    print(" ".join(pretty[0:3]))
    print(" ".join(pretty[3:6]))
    print(" ".join(pretty[6:9]))


# =============================================================================
# Question 2: Comparing Algorithms
# =============================================================================


if __name__ == "__main__":
    random.seed(SEED)  # Seed the RNG to make sure that the puzzles don't change.
    rows = []
    for i in range(NUM_PUZZLES):
        print("Solving eight puzzle {} of {} ...".format(i + 1, NUM_PUZZLES))
        p = make_rand_8puzzle()
        misplaced = astar_search(p, h=p.misplaced_tiles)
        manhattan = astar_search(p, h=p.manhattan_distance)
        combined = astar_search(
            p, h=lambda n: max(p.misplaced_tiles(n), p.manhattan_distance(n)),
        )
        rows.append(
            (" ".join(str(n) for n in p.initial), *misplaced, *manhattan, *combined)
        )
    print("Writing eight puzzle solutions to file ...")
    with open("a1_eight_puzzle.csv", mode="w") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

# =============================================================================
# Question 3: Duck Puzzle
# =============================================================================


class DuckPuzzle(Problem):
    """Implements a new Problem class called DuckPuzzle.

     1 2
     3 4 5 6   goal state
       7 8 *
    """

    def __init__(self, initial: State, goal: State = GOAL_STATE):
        super().__init__(initial, goal)

    def randomize(self, moves: int = 100):
        """Randomize the initial state by applying random actions."""
        for i in range(moves):
            possible_actions = self.actions(self.initial)
            action = random.choice(possible_actions)
            self.initial = self.result(self.initial, action)

    def find_blank_square(self, state: State) -> int:
        """Find the index of the blank square."""
        return state.index(0)

    def actions(self, state: State) -> List[str]:
        """Return the list of possible actions."""
        blank = self.find_blank_square(state)
        possible_actions = []
        # Increment the index to match the goal state.
        if blank + 1 not in (1, 2, 5, 6):
            possible_actions.append("UP")
        if blank + 1 not in (1, 3, 7):
            possible_actions.append("LEFT")
        if blank + 1 not in (3, 7, 8, 9):
            possible_actions.append("DOWN")
        if blank + 1 not in (2, 6, 9):
            possible_actions.append("RIGHT")
        return possible_actions

    def result(self, state: State, action: str) -> State:
        """Apply an action to a state."""
        blank = self.find_blank_square(state)
        new_state = list(state)
        # The top row has different vertical deltas.
        # Increment the index to match the goal state.
        delta = {
            "UP": -2 if blank + 1 in (1, 2) else -3,
            "DOWN": 2 if blank + 1 in (1, 2) else 3,
            "LEFT": -1,
            "RIGHT": 1,
        }
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        return tuple(new_state)

    def goal_test(self, state: State) -> bool:
        """Test if the goal has been reached."""
        return state == self.goal

    def misplaced_tiles(self, node: Node) -> int:
        """Compute the misplaced tile heuristic."""
        # Don't count the blank tile.
        return sum(s != g for (s, g) in zip(node.state, self.goal) if s != 0)

    def manhattan_distance(self, node: Node) -> int:
        """Compute the Manhattan distance heuristic."""
        dist = 0
        # Hard-code the row and column of each index.
        indexToRow = [0, 0, 1, 1, 1, 1, 2, 2, 2]
        indexToCol = [0, 1, 0, 1, 2, 3, 0, 1, 2]
        # Don't count the blank tile.
        for n in range(1, 9):
            stateIndex = node.state.index(n)
            goalIndex = self.goal.index(n)
            dist += abs(indexToRow[stateIndex] - indexToRow[goalIndex])
            dist += abs(indexToCol[stateIndex] - indexToCol[goalIndex])
        return dist


if __name__ == "__main__":
    random.seed(SEED)  # Seed the RNG to make sure that the puzzles don't change.
    rows = []
    for i in range(NUM_PUZZLES):
        print("Solving duck puzzle {} of {} ...".format(i + 1, NUM_PUZZLES))
        dp = DuckPuzzle(GOAL_STATE)
        dp.randomize(moves=100)
        misplaced = astar_search(dp, h=dp.misplaced_tiles)
        manhattan = astar_search(dp, h=dp.manhattan_distance)
        combined = astar_search(
            dp, lambda n: max(dp.misplaced_tiles(n), dp.manhattan_distance(n))
        )
        rows.append(
            (" ".join(str(n) for n in dp.initial), *misplaced, *manhattan, *combined)
        )
    print("Writing duck puzzle solutions to file ...")
    with open("a1_duck_puzzle.csv", mode="w") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
