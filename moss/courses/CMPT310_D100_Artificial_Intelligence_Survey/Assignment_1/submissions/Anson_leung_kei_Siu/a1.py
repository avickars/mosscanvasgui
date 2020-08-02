from search import *
import random
import time

"""Make random 8x8 puzzle that is solvable"""
def make_rand_8puzzle():
    """create a tuple of random permutation of 0-8 and check its solvability"""
    t=tuple(range(9))
    t_rand=tuple(random.sample(t,len(t)))
    ep=EightPuzzle(t_rand)
    while (ep.check_solvability(t_rand)==False):
        t_rand=tuple(random.sample(t,len(t)))
    
    return t_rand

"""Display a puzzle state in 3x3 board"""
def display(state):
    L=list(state)
    for x in range(9):
        if L[x]==0:
            L[x]='*'
            break
    print(L[0],L[1],L[2])
    print(L[3],L[4],L[5])
    print(L[6],L[7],L[8])


"""Modify from best_first_graph_search in search.py that also return
total number of moves and number of nodes removed from frontier"""
def best_first_graph_search_details(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    counter=0
    explored = set()
    while frontier:
        node = frontier.pop()
        counter=counter+1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node.path_cost,counter
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

"""Modify from astar_search from search.py"""
def astar_search_details(problem, h=None, display=False):
    
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_details(problem, lambda n: n.path_cost + h(n), display)

"""Modify h from search.py since we do not count 0"""
def mod_h(node):
    h=0
    for i in range(9):
        if node.state[i]==0:
            pass
        else:
            if node.state[i]!=i+1:
                h=h+1
    return h


"""Print out all records on a given EightPuzzle state using default 
heuristic method"""
def default_heuristic(state):
    ep=EightPuzzle(state)
    start_time = time.time()
    astar_search(ep,h=mod_h)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    record=astar_search_details(ep,h=mod_h)
    print('total number of moves = ',record[0])
    print('number of nodes removed from frontier = ',record[1])

"""function of calculating Manhattan distance of a given state"""
def Manhattan_h(node):
    man_dist=0
    for i in range(9):
        if node.state[i]==0:
            pass
        else:    
            if node.state[i]>=1 and node.state[i]<=3:
                goal_row=0
            elif node.state[i]>=4 and node.state[i]<=6:
                goal_row=1
            else:
                goal_row=2
                
            goal_col=(node.state[i]-1)%3
            if i>=0 and i<=2:
                state_row=0
            elif i>=3 and i<=5:
                state_row=1
            else:
                state_row=2
            state_col=i%3
            man_dist=man_dist+abs(state_row-goal_row)+abs(state_col-goal_col)
    return man_dist

"""Print out all records on a given EightPuzzle state using Manhattan distance 
heuristic method"""
def Manhattan_distance_heuristic(state):
    ep=EightPuzzle(state)
    start_time = time.time()
    astar_search(ep,h=Manhattan_h)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    record=astar_search_details(ep,h=Manhattan_h)
    print('total number of moves = ',record[0])
    print('number of nodes removed from frontier = ',record[1])

""" Finding max value between default h value and manhattan distance on a given EightPuzzle state"""  
def max_value(node):
    return max(Manhattan_h(node),mod_h(node))

"""Print out all records on a given EightPuzzle state using max 
heuristic method"""
def max_heuristic(state):
    ep=EightPuzzle(state)
    start_time = time.time()
    astar_search(ep,h=max_value)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    record=astar_search_details(ep,h=max_value)
    print('total number of moves = ',record[0])
    print('number of nodes removed from frontier = ',record[1])

"""Create a DuckPuzzle class problem"""
class DuckPuzzle(Problem):
    """Constructor with initial state input"""
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)
    
    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)
    
    def actions(self, state):
        """ Return the actions that can be executed in the given state."""

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions.remove('UP')
            possible_actions.remove('LEFT')
        if index_blank_square ==1 or index_blank_square==5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square ==2 or index_blank_square==6:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
        if index_blank_square == 4:
            possible_actions.remove('UP')
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

        if blank==0:
            if action=='RIGHT':
                neighbor=blank+1
            elif action=='DOWN':
                neighbor=blank+2
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        elif blank==1:
            if action=='LEFT':
                neighbor=blank-1
            elif action=='DOWN':
                neighbor=blank+2
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        elif blank==2:
            if action=='UP':
                neighbor=blank-2
            elif action=='RIGHT':
                neighbor=blank+1
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        elif blank==3:
            if action=='UP':
                neighbor=blank-2
            elif action=='DOWN':
                neighbor=blank+3
            elif action=='LEFT':
                neighbor=blank-1
            elif action=='RIGHT':
                neighbor=blank+1
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        elif blank==4:
            if action=='DOWN':
                neighbor=blank+3
            elif action=='LEFT':
                neighbor=blank-1
            elif action=='RIGHT':
                neighbor=blank+1
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        elif blank==5:
            if action=='DOWN':
                neighbor=blank+3
            elif action=='LEFT':
                neighbor=blank-1
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        elif blank==6:
            if action=='UP':
                neighbor=blank-3
            elif action=='RIGHT':
                neighbor=blank+1
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        elif blank==7:
            if action=='UP':
                neighbor=blank-3
            elif action=='LEFT':
                neighbor=blank-1
            elif action=='RIGHT':
                neighbor=blank+1
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        elif blank==8:
            if action=='UP':
                neighbor=blank-3
            elif action=='LEFT':
                neighbor=blank-1
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal
    
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

"""Print out all records on a given DuckPuzzle state using default 
heuristic method"""
def default_heuristic_duck(state):
    dp=DuckPuzzle(state)
    start_time = time.time()
    astar_search(dp,h=mod_h)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    record=astar_search_details(dp,h=mod_h)
    print('total number of moves = ',record[0])
    print('number of nodes removed from frontier = ',record[1])

"""Finding Manhattan distance of a given state on DuckPuzzle problem"""
def Manhattan_h_duck(node):
    man_dist=0
    for i in range(9):
        if node.state[i]==0:
            pass
        else:
            """finding the row position of goal state"""
            if node.state[i]>=1 and node.state[i]<=2:
                goal_row=0
            elif node.state[i]>=3 and node.state[i]<=6:
                goal_row=1
            else:
                goal_row=2
            """finding the column position of goal state"""
            if node.state[i]==1 or node.state[i]==3:
                goal_col=0   
            elif node.state[i]==2 or node.state[i]==4 or node.state[i]==7:
                goal_col=1
            elif node.state[i]==5 or node.state[i]==8:
                goal_col=2
            else:
                goal_col=3
            """finding the row position of input state"""
            if i>=0 and i<=1:
                state_row=0
            elif i>=2 and i<=5:
                state_row=1
            else:
                state_row=2
            """finding the column position of input state"""
            if i==0 or i==2:
                state_col=0
            elif i==3 or i==3 or i==6:
                state_col=1
            elif i==4 or i==7:
                state_col=2
            else:
                state_col=3
            man_dist=man_dist+abs(state_row-goal_row)+abs(state_col-goal_col)
    return man_dist

"""Print out all records on a given DuckPuzzle state using Manhattan distance 
heuristic method"""
def Manhattan_distance_heuristic_duck(state):
    dp=DuckPuzzle(state)
    start_time = time.time()
    astar_search(dp,h=Manhattan_h_duck)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    record=astar_search_details(dp,h=Manhattan_h_duck) 
    print('total number of moves = ',record[0])
    print('number of nodes removed from frontier = ',record[1])

""" Finding max value between default h value and manhattan distance on a given DuckPuzzle state"""  
def max_value_duck(node):
    return max(Manhattan_h_duck(node),mod_h(node))

"""Print out all records on a given DuckPuzzle state using max 
heuristic method"""
def max_heuristic_duck(state):
    dp=DuckPuzzle(state)
    start_time = time.time()
    astar_search(dp,h=max_value_duck)
    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
    record=astar_search_details(dp,h=max_value_duck)
    print('total number of moves = ',record[0])
    print('number of nodes removed from frontier = ',record[1])

"""Generating a solvable DuckPuzzle initial state"""
def generate_solvable_duckpuzzle():
        """start with goal state and randomly move 5000 steps"""
        current_state=(1,2,3,4,5,6,7,8,0)
        dp=DuckPuzzle(current_state)
        for i in range(5000):
            current_state=dp.result(current_state,random.choice(dp.actions(current_state)))
        
        return current_state

"""Main function"""
def main():
    
    """Test for 10 random EightPuzzle"""
    for i in range(10):
        eight_puzzle=make_rand_8puzzle()
        print('Default heuristic record %i (EightPuzzle):'% (i+1))
        default_heuristic(eight_puzzle)
        print('Manhattan distance heuristic record %i (EightPuzzle):'% (i+1))
        Manhattan_distance_heuristic(eight_puzzle)
        print('Max distance heuristic record %i (EightPuzzle):'% (i+1))
        max_heuristic(eight_puzzle)
        print('\n')
    """Test for 10 random DuckPuzzle"""
    for i in range(10):
        duck_puzzle=generate_solvable_duckpuzzle()
        
        print('Default heuristic record %i (DuckPuzzle):'% (i+1))
        default_heuristic_duck(duck_puzzle)
        print('Manhattan distance heuristic record %i (DuckPuzzle):'% (i+1))
        Manhattan_distance_heuristic_duck(duck_puzzle)
        print('Max distance heuristic record %i (DuckPuzzle):'% (i+1))
        max_heuristic_duck(duck_puzzle)
        print('\n')
    

if __name__ == "__main__":
    main()

    
        
