# a1.py
    
from search import *
    
# ...
import sys, math
import random
import time
from itertools import permutations



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

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        if index_blank_square == 1:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 2:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square == 5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
        if index_blank_square == 8:    
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')
        
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank==0:
            delta['DOWN']=2
        if blank==1:
            delta['DOWN']=2
        if blank==2:
            delta['UP']=-2
        if blank==3:
            delta['UP']=-2    
            delta['DOWN']=3
        if blank==4:
            delta['DOWN']=3
        if blank==5:
            delta['DOWN']=3
        if blank==6:
            delta['UP']=-3
        if blank==7:
            delta['UP']=-3
        if blank==8:
            delta['UP']=-3
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


def my_best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    counter_popped=0
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        counter_popped+=1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            node.counter_popped=counter_popped
            return node
        
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None
def my_astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return my_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def make_rand_8puzzle():
    """returns a new instance of an EightPuzzle problem
    with a random initial state that is solvable"""
    perm = tuple(permutations([0, 1, 2, 3, 4, 5, 6, 7, 8]))
    state=random.choice(perm)
    x=(EightPuzzle(initial = state))
    y= x.check_solvability(state)
    if (y==True):
        # display(state)
        return state
    else:
        return (make_rand_8puzzle())
    
def make_rand_duckPuzzle():
    """returns a new instance of a Duck Puzzle problem
    with a random initial state that is solvable"""
    final=(1,2,3,4,5,6,7,8,0)
    goal=list(final)
    puzzle=DuckPuzzle(final)
    tile_moves=random.randint(1,1000)
    for x in range(tile_moves):
        action_possible=puzzle.actions(goal)
        move=random.choice(action_possible)
        goal=puzzle.result(goal, move)
    # displayDuck(goal)
    return goal
    

    
def displayDuck(state):
    """takes a Duck puzzle state as input and prints a representation of it"""
    state=list(state)
    for i in range(0,9):
        if (state[i]==0):
            state[i]="*"
   
    print(state[0],state[1],end="\n")
    print(state[2],state[3],state[4],state[5],end="\n")
    print(" ",state[6],state[7],state[8])

        
        
   
def display(state):
    """takes a Eight puzzle state as input and prints a representation of it"""
    for i in range(0,9):
          if(i%3==0):
              print("")

          if(state[i]!=0):
              print(state[i],end=" ")
   
          else:
              print("*",end=" ")


def EightPuzzle_manhattan_distance(node):
    """takes a Eight Puzzle node as input and gives manhattan distance"""
    current = node.state
    distance = 0
    hori = 0
    vert = 0
    goal=(1,2,3,4,5,6,7,8,0)
    for i in current:
        position_difference = abs(goal.index(i)-current.index(i))
        if i!=0:
            hori= position_difference % 3
            vert= position_difference / 3
            distance += hori + int(vert)
            if abs(goal.index(i)%3 - current.index(i)%3)==2 and position_difference%3==1:
                distance+=2         
    
    return distance
def manhattanDuck_distance(node):
    """takes a Duck Puzzle node as input and gives the manhattan distance of it"""
    state=node.state
    goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)
    coordinates={0:(0,0), 1:(1,0), 2:(2,0),3:(0,1), 4:(1,1), 5:(2,1),6:(0,2), 7:(1,2), 8:(2,2)}
    sum=0
    for i in state:        
        if i!=0:
            temp=goal.index(i)
            initial=state.index(i)
            x1,y1=coordinates[temp]
            x2,y2=coordinates[initial]
            sum+=(abs(x1-x2) + abs(y1-y2))
        else:
            sum+=0

    return sum  
           
def Max_heuristic_eightPuzle(node):
    """takes a Eight Puzzle node as input and gives max heuristic """
    objectEight=EightPuzzle(initial=node.state)
    distance=EightPuzzle_manhattan_distance(node)
    x=objectEight.h(node)
    return max(distance,x)

def Max_heuristic_duckPuzle(node):
    """takes a Duck Puzzle node as input and gives max heuristic """
    objectDuck=DuckPuzzle(initial=node.state)
    distance=manhattanDuck_distance(node)
    x=objectDuck.h(node)
    return max(distance,x)
    
def EightPuzzleTotalHeuristic(): 
    """Gives the entire analysis of eight puzzle"""
    b= make_rand_8puzzle()
    eightpuzzleobject=EightPuzzle(initial=b)
    print("<==Initial State",display(b))
    print("-Aster Search using misplaced tile-")
    print("\n")
    object1=Node(b)
    t_0=time.time()
    aster_1=my_astar_search(eightpuzzleobject)
    t_1=time.time()
    print("Time Taken: ",t_1-t_0)
    print("\n")
    print("Tiles Moved: ",aster_1.path_cost)
    print("\n")
    print("Popped Nodes: ",aster_1.counter_popped)
    print("<==Final State",display(aster_1.state))
    
    print("-Aster Search using Manhattan distance-")
    t_2=time.time()
    aster_2=my_astar_search(eightpuzzleobject,h=EightPuzzle_manhattan_distance)
    t_3=time.time()
    print("Time Taken: ",t_3-t_2)
    print("\n")
    print("Tiles Moved: ",aster_2.path_cost)
    print("\n")
    print("Popped Nodes: ",aster_2.counter_popped)
    print("<==Final State",display(aster_2.state))
    
    print("-Aster Search using max of the misplaced tile-")
    t_4=time.time()
    aster_3=my_astar_search(eightpuzzleobject,h=Max_heuristic_eightPuzle)
    t_5=time.time()
    print("Time Taken: ",t_5-t_4)
    print("\n")
    print("Tiles Moved: ",aster_3.path_cost)
    print("\n")
    print("Popped Nodes: ",aster_3.counter_popped)
    print("<==Final State",display(aster_3.state))
 
def DuckPuzzleTotalHeuristic():
    """Gives the entire analysis of duck puzzle"""
    b= make_rand_duckPuzzle()
    duckpuzzleobject= DuckPuzzle(initial=b)
    print("^Initial State",displayDuck(b))
    print("-Aster Search using misplaced tile-")
   
    object1=Node(b)
    t_0=time.time()
    aster_1=my_astar_search(duckpuzzleobject)
    t_1=time.time()
    print("Time Taken: ",t_1-t_0)
    print("\n")
    print("Tiles Moved: ",aster_1.path_cost)
    print("\n")
    print("Popped Nodes: ",aster_1.counter_popped)
    print("^Final State",displayDuck(aster_1.state))
    
    print("-Aster Search using Manhattan distance-")
    t_2=time.time()
    aster_2=my_astar_search(duckpuzzleobject,h=manhattanDuck_distance)
    t_3=time.time()
    print("Time Taken: ",t_3-t_2)
    print("\n")
    print("Tiles Moved: ",aster_2.path_cost)
    print("\n")
    print("Popped Nodes: ",aster_2.counter_popped)
    print("^Final State",displayDuck(aster_2.state))
    
    print("-Aster Search using max of the Misplaced tile and Manhattan-")
    t_4=time.time()
    aster_3=my_astar_search(duckpuzzleobject,h=Max_heuristic_duckPuzle)
    t_5=time.time()
    print("Time Taken: ",t_5-t_4)
    print("\n")
    print("Tiles Moved: ",aster_3.path_cost)
    print("\n")
    print("Popped Nodes: ",aster_3.counter_popped)
    print("^Final State",displayDuck(aster_3.state))
    
if __name__ == '__main__':
    print("EIGHT PUZZLE ANALYSIS: ")
    for i in range(1,11):
        print("Number ",i," Analysis")
        EightPuzzleTotalHeuristic()
        
    print("DUCK PUZZLE ANALYSIS: ")
    for i in range(1,11):
        print("Number ",i," Analysis")
        DuckPuzzleTotalHeuristic()
    
    
    
   
    
    
    

    
    

    
    

    

  
    


        