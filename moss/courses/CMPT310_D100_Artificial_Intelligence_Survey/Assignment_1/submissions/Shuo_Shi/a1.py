import random

from search import EightPuzzle, astar_search, Problem


def make_rand_8puzzle():

    while True:
        state = [i for i in range(9)]
        for i in range(10):
            i, j = random.randint(0, 8), random.randint(0, 8)       # switch two tiles
            state[i], state[j] = state[j], state[i]
        puzzle = EightPuzzle(tuple(state))
        if puzzle.check_solvability(tuple(state)):      # if the puzzle is solvable, return the puzzle
            return puzzle


def display(state):
    l = list([str(x) for x in state])   # # display the puzzle row by row
    l[l.index("0")] = "*"
    print(" ".join(l[:3]))
    print(" ".join(l[3:6]))
    print(" ".join(l[6:]), end=None)


def display_duck(puzzle):
    l = list([str(x) for x in puzzle.initial])      # display the puzzle row by row
    l[l.index("0")] = "*"
    print(l[0]+" "+l[1])
    print(" ".join([l[2], l[3], l[4], l[5]]))
    print("  "+" ".join(l[6:]))


def make_rand_duckpuzzle():
    l = [i for i in range(1, 9)]
    l.append(0)
    puzzle = DuckPuzzle(tuple(l))
    state = puzzle.initial

    for i in range(200):
        actions = puzzle.actions(state)
        state = puzzle.result(state, random.choice(actions))        # do a moving randomly

    return DuckPuzzle(state)


class DuckPuzzle(Problem):
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

        if index_blank_square == 0:     # for every position, the possible action list is different
            return ['RIGHT', 'DOWN']
        elif index_blank_square == 1:
            return ['LEFT', 'DOWN']
        elif index_blank_square == 2:
            return ['RIGHT', 'UP']
        elif index_blank_square == 3:
            return possible_actions
        elif index_blank_square == 4:
            possible_actions.remove('UP')
            return possible_actions
        elif index_blank_square == 5:
            return ['LEFT', 'DOWN']
        elif index_blank_square == 6:
            return ['UP', 'RIGHT']
        elif index_blank_square == 7:
            possible_actions.remove('DOWN')
            return possible_actions
        elif index_blank_square == 8:
            return ['UP', 'LEFT']

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        x, y = self.convert(blank)
        if action == 'UP':
            x -= 1
        elif action == 'DOWN':
            x += 1
        elif action == 'LEFT':
            y -= 1
        elif action == 'RIGHT':
            y += 1

        d = {self.convert(i): i for i in range(9)}

        neighbor = d[(x, y)]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def h1(self, node):
        total = 0
        for i in range(9):
            p = node.state.index(i)
            x, y = self.convert(p)      # convert to position
            x1, y1 = self.convert((i-1) % 9)
            total += abs(x - x1) + abs(y - y1)  # calculate the manhattan distance
        return total

    def convert(self, p):       # convert sequence to grid coordinate
        if p <= 1:
            return 0, p
        elif 1 < p <= 5:
            return 1, p-2
        else:
            return 2, p-5

    def h2(self, node):
        return max([self.h(node), self.h1(node)])   # max of mismatch and manhattan distance


if __name__ == '__main__':

    for i in range(10):
        puzzle = make_rand_8puzzle()        # generate a 8 puzzle problem
        display(puzzle.initial)

        # puzzle = make_rand_duckpuzzle()       #  generate a duck puzzle problem
        # display_duck(puzzle)

        print(puzzle.initial)

        x1 = astar_search(puzzle, puzzle.h)     # search using mismatch

        x2 = astar_search(puzzle, puzzle.h1)    # search using manhattan distance

        x3 = astar_search(puzzle, puzzle.h2)    # search using max of mismatch and manhattan distance

        print(x1[0])
        print(x2[0])
        print(x3[0])

        print(x1[2])
        print(x2[2])
        print(x3[2])

        print(x1[1])
        print(x2[1])
        print(x3[1])



