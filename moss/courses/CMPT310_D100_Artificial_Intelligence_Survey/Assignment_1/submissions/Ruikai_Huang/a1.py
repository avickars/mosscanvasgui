# a1.py

from search import *
import random
import itertools
import math
import time

def fix_puzzle(state):
    if state[0]==0:
        state[1],state[2]=state[2],state[1]
    elif state[1]==0:
        state[0],state[2]=state[2],state[0]
    else:
        state[0],state[1]=state[1],state[0]
            

def make_rand_8puzzle():
    state=list(range(9))
    random.shuffle(state)
    state0=state.copy()
    if not EightPuzzle.check_solvability(None,state):
        fix_puzzle(state)
    # assert(EightPuzzle.check_solvability(None,state)),print("state:",state0)
    return EightPuzzle(tuple(state))

def display(state):
    for i in range(len(state)):
        print(state[i] if state[i] else '*',end='\n' if i%3==2 else ' ')

# adapted from aima-python
def my_best_first_graph_search(problem,f,display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    # removed=0
    while frontier:
        # assert(removed==len(explored))
        node = frontier.pop()
        # removed+=1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node,len(explored),len(frontier)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None,len(explored),len(frontier)

# adapted from aima-python
def my_astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return my_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def h_manhantan(node):
    tbl=[
        [
            0,0,0,
            0,0,0,
            0,0,0,
        ],
        [
            0,1,2,
            1,2,3,
            2,3,4,
        ],
        [
            1,0,1,
            2,1,2,
            3,2,3,
        ],
        [
            2,1,0,
            3,2,1,
            4,3,2,
        ],
        [
            1,2,3,
            0,1,2,
            1,2,3,
        ],
        [
            2,1,2,
            1,0,1,
            2,1,2,
        ],
        [
            3,2,1,
            2,1,0,
            3,2,1,
        ],
        [
            2,3,4,
            1,2,3,
            0,1,2,
        ],
        [
            3,2,3,
            2,1,2,
            1,0,1,
        ],
    ]

    return sum(tbl[tile][pos] for pos,tile in enumerate(node.state))

def test_my_puzzles(show=False):
    puzs=[
        (2, 3, 8, 7, 4, 5, 0, 6, 1),
        (3, 5, 6, 2, 0, 4, 1, 7, 8),
        (7, 2, 4, 0, 5, 8, 6, 1, 3),
        (3, 2, 1, 5, 7, 6, 0, 8, 4),
        (7, 5, 1, 3, 8, 4, 0, 6, 2),
        (6, 1, 8, 5, 3, 4, 7, 0, 2),
        (1, 2, 8, 0, 7, 3, 6, 5, 4),
        (3, 0, 5, 7, 8, 4, 2, 1, 6),
        (4, 3, 0, 2, 6, 1, 5, 7, 8),
        (4, 0, 5, 6, 2, 3, 7, 1, 8),
        ]
    data=[[],[],[]]
    for puz in puzs:
        prob=EightPuzzle(puz)

        h_misplace=lambda n: sum(s!=0 and s != g for (s, g) in zip(n.state, prob.goal))
        h_max=lambda n: max(h_manhantan(n),h_misplace(n))

        heurs=[h_misplace,h_manhantan,h_max]

        if show:
            display(puz)
        for i in range(3):
            t0=time.time()
            node,num_expl,num_frt=my_astar_search(prob,h=heurs[i],display=show)
            t1=time.time()
            data[i].append([t1-t0,node.path_cost,num_expl])

    return data

class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)
    
    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square==0 or index_blank_square==2 or index_blank_square==6:
            possible_actions.remove('LEFT')
        if index_blank_square<2 or index_blank_square==4 or index_blank_square==5:
            possible_actions.remove('UP')
        if index_blank_square==1 or index_blank_square==5 or index_blank_square==8:
            possible_actions.remove('RIGHT')
        if index_blank_square==2 or index_blank_square>=6:
            possible_actions.remove('DOWN')
        
        return possible_actions
    
    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'LEFT': -1, 'RIGHT': 1}

        if blank<2:
            delta['DOWN']=2
        elif blank<6:
            delta['UP']=-2
            delta['DOWN']=3
        else:
            delta['UP']=-3
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal
    
    def h(self, node):
        return sum(s != g and s!=0 for (s, g) in zip(node.state, self.goal))
    
    def display(self,state):
        for i in range(2):
            print(state[i] if state[i] else '*',end=' ')
        print()

        for i in range(2,6):
            print(state[i] if state[i] else '*',end=' ')
        print()

        print('  ',end='')
        for i in range(6,9):
            print(state[i] if state[i] else '*',end=' ')
        print()

def gen_duck():
    s0=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    p0=DuckPuzzle(initial=(1, 2, 3, 4, 5, 6, 7, 8, 0))

    for _ in range(100000):
        acts=p0.actions(s0)
        a=random.choice(acts)
        s0=p0.result(s0,a)

    return DuckPuzzle(s0)

def duck_manhattan(node):
    tbl=[
        [
            0,0,0,
            0,0,0,
            0,0,0,
        ],
        [
            0,1,
            1,2,3,4,
              3,4,5,
        ],
        [
            1,0,
            2,1,2,3,
              2,3,4,
        ],
        [
            1,2,
            0,1,2,3,
              2,3,4,
        ],
        [
            2,1,
            1,0,1,2,
              1,2,3,
        ],
        [
            3,2,
            2,1,0,1,
              2,1,2,
        ],
        [
            4,3,
            3,2,1,0,
              3,2,1,
        ],
        [
            3,2,
            2,1,2,3,
              0,1,2,
        ],
        [
            4,3,
            3,2,1,2,
              1,0,1,
        ],
        [
            5,4,
            4,3,2,1,
              2,1,0,
        ],
    ]

    return sum(tbl[tile][pos] for pos,tile in enumerate(node.state))

def test_duck_puzzles(show=False):
    puzs=[
        (2, 3, 1, 5, 0, 6, 8, 4, 7),
        (3, 1, 0, 2, 6, 7, 8, 4, 5),
        (2, 0, 1, 3, 4, 6, 5, 8, 7),
        (1, 2, 0, 3, 7, 5, 6, 8, 4),
        (1, 2, 3, 5, 8, 4, 6, 7, 0),
        (2, 3, 1, 5, 0, 4, 8, 7, 6),
        (2, 3, 1, 4, 6, 8, 0, 7, 5),
        (2, 3, 1, 8, 0, 4, 5, 6, 7),
        (3, 1, 2, 8, 0, 5, 7, 6, 4),
        (2, 3, 0, 1, 8, 4, 5, 6, 7),
    ]

    data=[[],[],[]]
    for puz in puzs:
        prob=DuckPuzzle(puz)

        duck_max=lambda n: max(duck_manhattan(n),prob.h(n))

        heurs=[prob.h,duck_manhattan,duck_max]

        if show:
            prob.display(puz)
        for i in range(3):
            t0=time.time()
            node,num_expl,num_frt=my_astar_search(prob,h=heurs[i],display=show)
            t1=time.time()
            data[i].append([t1-t0,node.path_cost,num_expl])

    return data

if __name__=='__main__':
    
    print('=====================================')
    print('8 puzzles:')
    res=test_my_puzzles(True)

    print('time:')
    for j in range(10):
        for k in range(3):
            print("%.6f"%(res[k][j][0]),end='\t')
        print()

    print('length:')
    for j in range(10):
        for k in range(3):
            print("%d"%(res[k][j][1]),end='\t')
        print()
    
    print('removed:')
    for j in range(10):
        for k in range(3):
            print("%d"%(res[k][j][2]),end='\t')
        print()

    print('=====================================')
    print('duck puzzle:')
    res=test_duck_puzzles(True)

    print('time:')
    for j in range(10):
        for k in range(3):
            print("%.6f"%(res[k][j][0]),end='\t')
        print()

    print('length:')
    for j in range(10):
        for k in range(3):
            print("%d"%(res[k][j][1]),end='\t')
        print()
    
    print('removed:')
    for j in range(10):
        for k in range(3):
            print("%d"%(res[k][j][2]),end='\t')
        print()
        