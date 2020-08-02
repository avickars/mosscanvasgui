# a1.py
import time
from search import *


# ================================================
# Extended classes

class EightPuzzleEx(EightPuzzle):

    def display(self, state):
        for i in range(9):
            if i == 2 or i == 5 or i == 8:
                if state[i] == 0:
                    print('* ')
                else:
                    print(str(state[i]) + ' ')
            else:
                if state[i] == 0:
                    print('* ', end='')
                else:
                    print(str(state[i]) + ' ', end='')

    def manH(self, node):
        ret = 0

        for tile in range(1, 9):
            s = node.state.index(tile)
            g = self.goal.index(tile)
            x_dist = abs(g % 3 - s % 3)
            y_dist = abs(int(g / 3) - int(s / 3))
            ret += x_dist + y_dist

        return ret


class DuckPuzzle(EightPuzzle):

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        blank = self.find_blank_square(state)

        if blank == 0 or blank == 2 or blank == 6:
            possible_actions.remove('LEFT')
        if blank < 2 or blank == 4 or blank == 5:
            possible_actions.remove('UP')
        if blank == 1 or blank == 5 or blank == 8:
            possible_actions.remove('RIGHT')
        if blank > 5 or blank == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank > 3:
            up = -3
        else:
            up = -2

        if blank < 3:
            down = 2
        else:
            down = 3

        delta = {'UP': up, 'DOWN': down, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def display(self, state):
        for i in range(9):
            if i == 1 or i == 5 or i == 8:
                if state[i] == 0:
                    print('*')
                else:
                    print(str(state[i]))
            elif i == 6:
                if state[i] == 0:
                    print('  * ', end='')
                else:
                    print('  ' + str(state[i]) + ' ', end='')
            else:
                if state[i] == 0:
                    print('* ', end='')
                else:
                    print(str(state[i]) + ' ', end='')

    def manH(self, node):
        ret = 0

        for tile in range(1, 9):
            s = node.state.index(tile)
            g = self.goal.index(tile)

            # s coordinates
            if s in [0, 1]:
                s_row = 0
            elif s in [2, 3, 4, 5]:
                s_row = 1
            else:
                s_row = 2

            if s in [0, 2]:
                s_col = 0
            elif s in [1, 3, 6]:
                s_col = 1
            elif s in [4, 7]:
                s_col = 2
            else:
                s_col = 3

            # g coordinates
            if g in [0, 1]:
                g_row = 0
            elif g in [2, 3, 4, 5]:
                g_row = 1
            else:
                g_row = 2

            if g in [0, 2]:
                g_col = 0
            elif s in [1, 3, 6]:
                g_col = 1
            elif s in [4, 7]:
                g_col = 2
            else:
                g_col = 3

            x_dist = abs(g_col - s_col)
            y_dist = abs(g_row - s_row)
            ret += x_dist + y_dist

        return ret


# ================================================
def make_rand_8puzzle():
    # generate random initial list
    init = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    random.shuffle(init)
    ret = EightPuzzleEx(initial=tuple(init))

    # keep generating random tuple until solvable
    while not ret.check_solvability(tuple(init)):
        random.shuffle(init)
        ret = EightPuzzleEx(initial=tuple(init))

    return ret


def make_rand_duckpuzzle():
    # start with goal state
    init = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    ret = DuckPuzzle(initial=tuple(init))

    # do 50 random moves
    for i in range(50):
        move = random.choice(ret.actions(ret.initial))
        state = ret.result(ret.initial, move)
        ret = DuckPuzzle(initial=state)

    return ret


# modified A* search for max of misplaced tile and Manhattan
def astar_search_mod(problem, h1, h2, display=False):
    return best_first_graph_search(problem, lambda n: n.path_cost + max(h1(n), h2(n)), display)


# ================================================
def solvePuzzle(puzzle):
    puzzle.display(puzzle.initial)

    print("============ Misplaced Tile Heuristic ============")
    start = time.time()
    node = astar_search(puzzle, h=puzzle.h, display=True)
    print("Elapsed time (in seconds): ", time.time() - start)
    print("Number of tiles moved: ", len(node.path()) - 1)

    print("============ Manhattan Distance Heuristic ============")
    start = time.time()
    node = astar_search(puzzle, h=puzzle.manH, display=True)
    print("Elapsed time (in seconds): ", time.time() - start)
    print("Number of tiles moved: ", len(node.path()) - 1)

    print("============ Max heuristic ============")
    start = time.time()
    node = astar_search_mod(puzzle, h1=puzzle.h, h2=puzzle.manH, display=True)
    end = time.time()
    print("Elapsed time (in seconds): ", end - start)
    print("Number of tiles moved: ", len(node.path()) - 1)


# ================================================
p0 = make_rand_8puzzle()
p1 = make_rand_8puzzle()
p2 = make_rand_8puzzle()
p3 = make_rand_8puzzle()
p4 = make_rand_8puzzle()
p5 = make_rand_8puzzle()
p6 = make_rand_8puzzle()
p7 = make_rand_8puzzle()
p8 = make_rand_8puzzle()
p9 = make_rand_8puzzle()

solvePuzzle(p0)
solvePuzzle(p1)
solvePuzzle(p2)
solvePuzzle(p3)
solvePuzzle(p4)
solvePuzzle(p5)
solvePuzzle(p6)
solvePuzzle(p7)
solvePuzzle(p8)
solvePuzzle(p9)


# ================================================
d0 = make_rand_duckpuzzle()
d1 = make_rand_duckpuzzle()
d2 = make_rand_duckpuzzle()
d3 = make_rand_duckpuzzle()
d4 = make_rand_duckpuzzle()
d5 = make_rand_duckpuzzle()
d6 = make_rand_duckpuzzle()
d7 = make_rand_duckpuzzle()
d8 = make_rand_duckpuzzle()
d9 = make_rand_duckpuzzle()

solvePuzzle(d0)
solvePuzzle(d1)
solvePuzzle(d2)
solvePuzzle(d3)
solvePuzzle(d4)
solvePuzzle(d5)
solvePuzzle(d6)
solvePuzzle(d7)
solvePuzzle(d8)
solvePuzzle(d9)