# a1.py

from search import *

# Question 1: Helper Functions

print ("Question 1: Helper Functions")
print()

import random

import time

def make_rand_8puzzle():
    #The main idea: Firstly, generated a sequential tuple with length 9 and randomly change the order among these numbers
    
    puzzle_sequential=tuple(range(9))
    
    state=tuple(random.sample(puzzle_sequential,len(puzzle_sequential)))

    return state


def display(state):
    #The main idea: Setting up "position" to flag the position of these numbers from 1-9, if the number located at position 3, 6 and 9 indicates
    # the new line begins, so I use position %3 to find 3, 6 and 9. In the process of printing, change the occurance of 0 to * and the rest of
    #numbers keep same.
    
    position=0
    
    for x in tuple(range(9)):
        
        position=position+1
        
        if state[x] == 0:
            print("*"+ " ",end='')
            
        else:
            print (str(state[x])+" ",end='')
            
        if (position%3==0): # use position %3 to find 3, 6 and 9
            print()    
        
state=make_rand_8puzzle() # randomly generate the 1st puzzle

puzzle_class= EightPuzzle(Problem) 

solvability= puzzle_class.check_solvability(state) #Check solvability for the 1st puzzle



i=0 #while loop condition variable

while i<10: #This while loop condition just simply makes sure the program can be enter into the while loop because i is always 0, less than 10
    
    if solvability == False: #if the puzzle cannot be solved
        
        #Then regenerate new puzzle and check its solvability again
        
        state=make_rand_8puzzle()
        
        solvability= puzzle_class.check_solvability(state)
        
        print("This puzzle cannot be solved. Redo")
        
        i=0 #This line make sure the while loop is still valid in order to check whether solvability is false or not 
        
    else:# Solvability is True so break this while loop (i.e it's unnecessary to regenerate new puzzle)
        
        print("This puzzle can be solved")
        
        break
   
print("state is "+ str(state))

display(state)# print out this state in 3*3 format
print()


print()
print("------------------------------------------")
print()


# Question 2: Comparing Algorithms

print("Question 2: Comparing Algorithms")
print()


#----Modidfication Part----

'''Modify the A* code''' # I added a manhattan_distance (state) function and max_misplaced_mht function to get new heuristic value 

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

    def h(self, node): # original h value (i.e. the number of misplaced tiles)
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        misplaced=sum(s != g for (s, g) in zip(node.state, self.goal))
        for (a,b) in zip(node.state, self.goal):  # exclude the 0 tile 
            if a==0:
                misplaced=misplaced-1
        return misplaced


    def manhattan_distance (self,node):# my version of manhanttan distance function (h value) [get some hints from def manhattan(node) in test_search.py]
         d_x=0

         d_y=0
    
         initial_state = node.state # the puzzle waits to be solved
    
         goal_state = (1,2,3,4,5,6,7,8,0)
    
         mh_distance=0
    
         for a in initial_state:#try to find the index difference (examine whether each tile is in the correct position) between each tile in initial and goal state
             misplaced = abs (initial_state.index(a)-goal_state.index(a))
        
             if a !=0: # 0 tile is not make sense in calculating Manhanttan distance since it is empty
                 
                 d_x=misplaced%3 #since this is a 3*3 puzzle
            
                 d_y=misplaced//3

                 mh_distance+=d_x+d_y # ordinary case: distance incrementing in x and y directions
        
             #when the tile is located at the last position in a row and correct position is on the first position of next row 
                 if abs(goal_state.index(a)%3-initial_state.index(a)%3)==2 and misplaced %3 ==1:
                      mh_distance+=2 # Although the index difference is only 1, we need extra two steps in x direction
                
         return mh_distance
        

    def max_misplaced_mht(self,node):  #heuristic value= max number between misplaced tiles and manhattan distance
        
        misplaced_h=self.h(node)  #simply call the previous functions
        
        manhattan_h=self.manhattan_distance(node) #simply call the previous functions
        
        max_h=max (misplaced_h,manhattan_h) #return max value between misplaced tiles and manhattan distance as new heuristic value

        return max_h

''' Make best_first_graph_search function can diplay some needed messages'''

def best_first_graph_search(problem, f, display=True):  # here I change display equal to True to display the printing message in this function
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
    nodes_removed=0 # here I added a new counter variable to save the number of nodes removed from the frontier
    while frontier:
        node = frontier.pop()
        nodes_removed=nodes_removed+1 # The previous line pop a node from frontier so after poping, I incremented the counter variable
        if problem.goal_test(node.state):
            if display:
                #print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                print("There are in total "+ str(nodes_removed)+" nodes have been removed from frontier.") # The new printing message
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

''' The modification for astar search is : Make astar_search can print the message (from best_first_graph_serach function)'''
''' There are three versions of astar_search(...) functions, each for one algorithm (one of ways to calculate heuristic value)'''

# version #1: heuristic value= number of misplaced tiles
def astar_search(problem, h=None, display=True): # Here I also change the display equal to True in order to display message
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    
    # here I add a value "True" to display the message from best_first_graph_serach function
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display=True)

# version #2: heuristic value=Manhattan Distance
def astar_search_manhanttan (problem, h=None, display=True):
    h=problem.manhattan_distance
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display=True) # now new f=g+h= path cost + manhattan distance

# version #3: heuristic value=Max values between previous two numbers
def astar_search_max_heuristic (problem, h=None, display=True):
    h=problem.max_misplaced_mht
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display=True) # now new f=g+h= path cost + max value



#----Test Part----

''' Create 10 random 8-puzzle instances and solve each of them via three different algorithms'''

j=0 # variable for while loop's condition
number_puzzles=1 #variable that use to count the number of puzzles

print("The ten puzzles are: ")
print()

while j<10: #since j=0 forever, this while loop will be valid permanently but may breaked out due to its if statement
    
    if solvability ==False: #if this puzzle unsolvable,then does not contribute to number_puzzle but regenerate a new puzzle until it is solvable
        
        state=make_rand_8puzzle()
        
        solvability= puzzle_class.check_solvability(state)

        
    else: #if the puzzle is solvable, then display it and count one for it.
        
        print(str(number_puzzles)+" puzzle")
        display (state)
        print()

        eight_puzzle=EightPuzzle(state) 
        
        start_time=time.time() #here start recording the time

        #----Misplaced tile heuristic----
        
        print("This solvable puzzle is solved by (Misplaced tile heuristic): ")
        print()
        
        ''' Begin solving the puzzle '''

        puzzle_solution= astar_search(eight_puzzle).solution() # I saved puzzle solution to a new list called puzzle_solution 
        
        time_usage=time.time()-start_time #here finish recording the time

        print(puzzle_solution)
        
        print("This solvable puzzle takes: "+ str(time_usage)+" seconds to complete!")
        print()

        print ("The length of the solution is " + str(len(puzzle_solution))) # get the length of the puzzle_solution list --> the length of solution
        print()

        #----Manhanttan distance heuristic----

        print("This solvable puzzle is solved by (Manhanttan distance heuristic): ")
        print()
        
        ''' Begin solving the puzzle '''

        start_time_mht=time.time() #here start recording the time

        puzzle_solution_mht=astar_search_manhanttan(eight_puzzle).solution()
        
        time_usage_mht=time.time()-start_time_mht #here finish recording the time
        print(puzzle_solution_mht)
        
        print("This solvable puzzle takes: "+ str(time_usage_mht)+" seconds to complete!")
        print()

        print ("The length of the solution is " + str(len(puzzle_solution_mht))) # get the length of the puzzle_solution list --> the length of solution
        print()

        #----Max heuristic value----

        print("This solvable puzzle is solved by (Max heuristic value): ")
        print()
        
        ''' Begin solving the puzzle '''

        start_time_max=time.time() #here start recording the time

        puzzle_solution_max=astar_search_max_heuristic(eight_puzzle).solution()
        
        time_usage_max=time.time()-start_time_max #here finish recording the time
        print(puzzle_solution_max)
        
        print("This solvable puzzle takes: "+ str(time_usage_max)+" seconds to complete!")
        print()

        print ("The length of the solution is " + str(len(puzzle_solution_max))) # get the length of the puzzle_solution list --> the length of solution
        print()

        
        number_puzzles=number_puzzles+1 #count the number of puzzles
     
        state=make_rand_8puzzle() #After the previous puzzle is solvable, it's time for the rest of new puzzle, continue generating puzzles here
        
        solvability= puzzle_class.check_solvability(state) #check its solvability
        
        if number_puzzles==11: # when the total number of puzzles are 10 (since I start counting from 1, so here is 11), break this while loop
            
            break

print()
print("-------------------------------------------------------------------------------------------------------")
print()

# Question 3: The House-Puzzle

print("Question 3: The House-Puzzle")

''' Below is the new DuckPuzzle class '''
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

    def actions(self, state):  # Modifications
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
        ''' I list up all possible actions for each possible blank index '''
        if index_blank_square==0: #for example, when blank space is at position 0, then this blank space cannot move up and left
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
            
        if index_blank_square==1: #when blank space is at position 1, then this blank space cannot move up and move right
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
            
        if index_blank_square==2: 
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
            
        if index_blank_square==4:
            possible_actions.remove('UP')
            
        if index_blank_square==5:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')

        if index_blank_square==6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')

        if index_blank_square==7:
            possible_actions.remove('DOWN')

        if index_blank_square==8:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):   # Modifications
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        ''' I list up three possible cases for position of blank spaces '''
        if blank<3: #for example, if blank=2, then it is able to move up to position 0 by 'UP':-2 (2-2=0 so that's why there is '-2')
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1} 
        '''Below follows same reasons'''   
        if blank==3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """
        ''' Main idea: Convert the duck puzzle into two parts, one is 2*2 and the other one is 2*3. The 2*2 matrix must have 1,2,3 consecutively,
        otherwise, this puzzle is unsolvable. I need an equation P=inversion+the sum of the index of row and column where blank space located. Since
        the goal state has P=5, so the initial state must also have P-value an odd number to make this puzzle solvable. '''
            
        two_two_matrix=[]
        two_three_matrix=[]
        two_two_matrix_three=[]
        two_two_goal=[1,2,3,4]
        two_three_goal=[4,5,6,7,8,0]

        for x in range(4): #Create a 2*2 maxtrix which contains first four numbers in state
            two_two_matrix.append(state[x])
            
        for y in range (3,9):#Create a 2*3 maxtrix which contains from 4th number to 8th number in state
            two_three_matrix.append(state[y])

        for z in range (3):
            two_two_matrix_three.append(state[z]) #Create a list of number which contain first three numbers
        
        ''' 2*2 Matrix inversions '''
        two_two_inversion=0
        for m in range(len(two_two_matrix)):
            for n in range(m+1,len(two_two_matrix)):
                if (two_two_matrix[m]>two_two_matrix[n])and two_two_matrix[m] != 0 and two_two_matrix[n] != 0:
                    two_two_inversion+=1
                    
        ''' 2*3 Matrix inversions '''            
        two_three_inversion=0
        for p in range(len(two_three_matrix)):
            for q in range(p+1,len(two_three_matrix)):
                if (two_three_matrix[p]>two_three_matrix[q])and two_three_matrix[p] != 0 and two_three_matrix[q] != 0:
                    two_three_inversion+=1
                    

        index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}
        index_state= {}
        index=[[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]

        for a in range(len(state)):#save the unsolved puzzle into index_state corresponds to their positions
            index_state[state[a]] = index[a]

        row_col_sum_goal=index_goal[0][0]+index_goal[0][1] #P-value of goal state, this must be an odd number (2+3=5)
            
        # We focus on 2*2 matrix
        if two_two_matrix[0]==1 and two_two_matrix[1]==2 and two_two_matrix[2]==3: # the first three numbers must be 1,2,3 consecutively
            if 0 in two_two_matrix:  #if the blank space is in 2*2 matrix
                row_col_sum_two_two=2 #index_state[0][0]+index_state[0][1] (bottom right is the only place to put 0 and the index is [1,1])
                solvability_two_two=row_col_sum_two_two + two_two_inversion #calculate the P-value for this 2*2 matrix
                if solvability_two_two %2 != 0: #this 2*2 puzzle is solvable
                    #now I need to make sure whether the 2*3 puzzle is solvable or not
                    row_col_sum_two_three= 2 # Set up this fake blank at top left corner 
                    solvability_two_three= row_col_sum_two_three + two_three_inversion # calculate the P-value for this 2*3 matrix
                    if solvability_two_three %2 != 0: # this 2*3 puzzle is also solvable
                        return True # the whole puzzle is solvable since two separate part are all solvable
                    else:
                        return False # Because 2*3 puzzle is unsolvable, so the whole puzzle cannot be solved
                else:
                    return False # if 2*2 puzzle is unsolvable, there is no need to check 2*3, the whole puzzle is unsolvable
            else: #if 0 is not in 2*2 matrix
                if two_two_matrix_three[0]==1 and two_two_matrix_three[1]==2 and two_two_matrix_three[2]==3: #the first three numbers must be 1,2,3 consecutively
                    row_col_sum_two_two=2 #Set up this fake blank at bottom right corner
                    solvability_two_two=row_col_sum_two_two + two_two_inversion #calculate the P-value for this 2*2 matrix
                    if solvability_two_two %2 != 0: # this 2*2 puzzle is solvable
                      #now I need to make sure whether the 2*3 puzzle is solvable or not
                        row_col_sum_two_three=index_state[0][0]+index_state[0][1] #Add up the sum of row and colunm where blank space located
                        solvability_two_three= row_col_sum_two_three + two_three_inversion #calculate the P-value for this 2*3 matrix
                        if solvability_two_three %2 != 0: # this 2*3 puzzle is solvable
                            return True # if both 2*2 and 2*3 are solvable, the whole puzzle is solvable
                        else:
                            return False # if 2*3 puzzle is unsolvable, the whole puzzle is unsolvable
                else:
                    return False # if 2*2 puzzle is unsolvable, there is no need to check solvability for 2*3 puzzle
        else:
            return False # if 2*2 puzzle do not contain 1,2,3, there is unnecessary to proceed the middle part
                            
        


    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


    def manhattan_distance (self,node):# my version of manhanttan distance function (h value) [get some hints from def manhattan(node) in test_search.py]
    
         state = node.state # the puzzle waits to be solved
    
         index_goal = {0: [2, 3], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3], 7: [2, 1], 8: [2, 2]}

         index_state= {}

         index=[[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3]]
    
         mhd=0

         for i in range(len(state)): #save the unsolved puzzle into index_state
            index_state[state[i]] = index[i]
                  
         for i in range(1,9): #because 0 should not be included in calculation of Manhattan Distance so the range is from 1 to 8
             for j in range(2):
                 mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

         return mhd
    

    def max_misplaced_mht(self,node):  #heuristic value= max number between misplaced tiles and manhattan distance
        
        misplaced_h=self.h(node)  #simply call the previous functions
        
        manhattan_h=self.manhattan_distance(node) #simply call the previous functions
        
        max_h=max (misplaced_h,manhattan_h) #return max value between misplaced tiles and manhattan distance as new heuristic value

        return max_h
    
''' Class declarition ends here'''



def display_duck(state): #display the state in duck format
    #The strategy is similar to ordinary 8-puzzle but we need to pay extra attention to position 1 and 5.
    position_duck=-1
    
    for y in tuple(range(9)):
        
        position_duck=position_duck+1
        
        if state[y] == 0: #Change the occurance of 0 to *
            print("*"+ " ",end='')
            
        else: # printing out the rest of numbers
            print (str(state[y])+" ",end='')
            
        if position_duck==1 or position_duck==5: # we need to add a new line after position 1 and 5
            print()
            
            if position_duck==5: #The number at position 6 has to be two spaces away from the beginning of the row
                print("  ",end= '')
                
    
duck_state=make_rand_8puzzle() # randomly generate a permutation

duckpuzzle_class= DuckPuzzle(Problem) 

duck_solvability= duckpuzzle_class.check_solvability(duck_state) #Check solvability for the 1st puzzle


m=0 #while loop condition variable

while m<10: #This while loop condition just simply makes sure the program can be enter into the while loop because i is always 0, less than 10
    
    if duck_solvability == False: #if the puzzle cannot be solved
        
        #Then regenerate new puzzle and check its solvability again
        
        duck_state=make_rand_8puzzle()
        
        duck_solvability= duckpuzzle_class.check_solvability(duck_state)
        
        #print("This puzzle cannot be solved. Redo")
        
        i=0 #This line make sure the while loop is still valid in order to check whether solvability is false or not 
        
    else:# Solvability is True so break this while loop (i.e it's unnecessary to regenerate new puzzle)
        
        print("This puzzle can be solved")
        
        break
   
print("state is "+ str(duck_state))

display_duck(duck_state)# print out this state in duck format
print()

j=0 # variable for while loop's condition
number_puzzles=1 #variable that use to count the number of puzzles

print("The ten puzzles are: ")
print()

while j<10: #since j=0 forever, this while loop will be valid permanently but may breaked out due to its if statement
    
    if duck_solvability ==False: #if this puzzle unsolvable,then does not contribute to number_puzzle but regenerate a new puzzle until it is solvable
        
        duck_state=make_rand_8puzzle()
        
        duck_solvability= duckpuzzle_class.check_solvability(duck_state)

        
    else: #if the puzzle is solvable, then display it and count one for it.
        
        print(str(number_puzzles)+" puzzle")
        display_duck (duck_state)
        print()

        duck_puzzle=DuckPuzzle(duck_state) 
        
        start_time=time.time() #here start recording the time

        #----Misplaced tile heuristic----
        
        print("This solvable puzzle is solved by (Misplaced tile heuristic): ")
        print()
        
        ''' Begin solving the puzzle '''

        puzzle_solution= astar_search(duck_puzzle).solution() # I saved puzzle solution to a new list called puzzle_solution 
        
        time_usage=time.time()-start_time #here finish recording the time

        print(puzzle_solution)
        
        print("This solvable puzzle takes: "+ str(time_usage)+" seconds to complete!")
        print()

        print ("The length of the solution is " + str(len(puzzle_solution))) # get the length of the puzzle_solution list --> the length of solution
        print()

        #----Manhanttan distance heuristic----

        print("This solvable puzzle is solved by (Manhanttan distance heuristic): ")
        print()
        
        ''' Begin solving the puzzle '''

        start_time_mht=time.time() #here start recording the time

        puzzle_solution_mht=astar_search_manhanttan(duck_puzzle).solution()
        
        time_usage_mht=time.time()-start_time_mht #here finish recording the time
        print(puzzle_solution_mht)
        
        print("This solvable puzzle takes: "+ str(time_usage_mht)+" seconds to complete!")
        print()

        print ("The length of the solution is " + str(len(puzzle_solution_mht))) # get the length of the puzzle_solution list --> the length of solution
        print()

        #----Max heuristic value----

        print("This solvable puzzle is solved by (Max heuristic value): ")
        print()
        
        ''' Begin solving the puzzle '''

        start_time_max=time.time() #here start recording the time

        puzzle_solution_max=astar_search_max_heuristic(duck_puzzle).solution()
        
        time_usage_max=time.time()-start_time_max #here finish recording the time
        print(puzzle_solution_max)
        
        print("This solvable puzzle takes: "+ str(time_usage_max)+" seconds to complete!")
        print()

        print ("The length of the solution is " + str(len(puzzle_solution_max))) # get the length of the puzzle_solution list --> the length of solution
        print()

        
        number_puzzles=number_puzzles+1 #count the number of puzzles
     
        duck_state=make_rand_8puzzle() #After the previous puzzle is solvable, it's time for the rest of new puzzle, continue generating puzzles here
        
        duck_solvability= duckpuzzle_class.check_solvability(duck_state) #check its solvability
        
        if number_puzzles==11: # when the total number of puzzles are 10 (since I start counting from 1, so here is 11), break this while loop
            
            break

print()



    
    