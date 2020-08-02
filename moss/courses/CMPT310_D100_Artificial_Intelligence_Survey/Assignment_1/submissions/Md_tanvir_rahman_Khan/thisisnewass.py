import random
from search import *
import time

class EightPuzzle(Problem):

    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """
 
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)
    
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

        delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
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
            for j in range(i+1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j]!= 0:
                    inversion += 1
        
        return inversion % 2 == 0
    
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        # Don't include zero. The heuristic function never ever overestimate the true cost
        # but the default one does

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

####Question: 1####
def make_rand_8puzzle():
    state = [0,1,2,3,4,5,6,7,8]
    random.shuffle(state)                           # random shuffle the states

    Eight_Puzzle = EightPuzzle(tuple(state))        
    while(Eight_Puzzle.check_solvability(state) == False):      # check solvability 
     random.shuffle(state)                   
     Eight_Puzzle = EightPuzzle(tuple(state))            # Eight_Puzzle is actually a object 

    
    return Eight_Puzzle                     

    
# default states
    

def display(state):
 i=0;
 for i in range(0,9,3):
  if (state[i]==0):
   print('*',state[i+1],state[i+2])
  elif(state[i+1]==0):
   print(state[i],'*',state[i+2])
  elif(state[i+2]==0):
   print(state[i],state[i+1],'*')
  else:
   print(state[i],state[i+1],state[i+2])








######Question 2###########

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
    numberofpops=0;
    while frontier:
        node = frontier.pop()
        numberofpops=numberofpops+1;
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node,numberofpops
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None,numberofpops

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display) 

def maxofbothheuristic(node):
    newpuzzle=EightPuzzle(node.state);
    return(max(Amanhattanheuristic(node),newpuzzle.h(node)));



def Amisplacedheuristic():
    aaa=make_rand_8puzzle();
    display(aaa.initial);
    starttime=time.time();
    r,total=astar_search(aaa);
    print("This is solution ", r.solution());

    print("Length is =", len(r.solution()));
    endtime=time.time();
    
    elapsedtime=endtime-starttime;
    print("Elapsed time", elapsedtime);
    print("Total number of pops",total);

    print("Manhattan on the run");
    manhattanstate=aaa;
    display(aaa.initial)
    manhattanstarttime=time.time();
    resultmanhattan,totalmanhattan=astar_search(manhattanstate,h=Amanhattanheuristic);
    endtimemanhattan=time.time();
    elapsedtimemanhattan=endtimemanhattan-manhattanstarttime;
    print("This solution is", resultmanhattan.solution());
    print("Length of the solution is", len(resultmanhattan.solution()));
    print(f"Elapsed time is = ",elapsedtimemanhattan);
    print("Total number of pops",totalmanhattan);

    print("Maxofboth heuristic on the run")
    maxofboth=aaa;
    display(maxofboth.initial);
    maxofbothstarttime=time.time();
    resultmaxofboth,totalpopsmaxofboth=astar_search(maxofboth,h=maxofbothheuristic);
    maxofbothendtime=time.time();
    maxofbothelapsedtime=maxofbothendtime-maxofbothstarttime;
    print("The solution is", resultmaxofboth.solution());
    print("Length of the solution is=",len(resultmaxofboth.solution()));
    print(f"Elapsed time",maxofbothelapsedtime);
    print("Total number of pops",totalpopsmaxofboth);




def Amanhattanheuristic(node):
    totaldistance=0;
    cstate=node.state;
    xdistance=0;
    ydistance=0;
    lengthofstate=len(cstate);
    goalindex={0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]};
    index=[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]];
    currentindex={};
    for i in range(lengthofstate):
        currentindex[cstate[i]]=index[i];

    for j in range(1,9):
        xdistance +=abs(goalindex[j][0]-currentindex[j][0]);
        ydistance +=abs(goalindex[j][1]-currentindex[j][1]);
    totaldistance=xdistance+ydistance;
    return totaldistance;



    


    






def display10times():
    for i in range(10):
     print("This is the ", i, "time, another", 10-1-i, "times to go");
     Amisplacedheuristic();

display10times();



########Question 3##############################################################################################

class DuckPuzzle(Problem):

    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """
 
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)
    
    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)
    
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """
        
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']       
        index_blank_square = self.find_blank_square(state)
        '''if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')'''

      
        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        if index_blank_square ==1:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square == 2:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
        if index_blank_square==3:
            return possible_actions
        if index_blank_square == 4:
            possible_actions.remove('UP')
        if index_blank_square ==5:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        if index_blank_square ==6:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square ==7:
            possible_actions.remove('DOWN')
        if index_blank_square ==8:
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
          delta={'DOWN':2,'RIGHT':1}
        if blank==1:
          delta={'DOWN':2,'LEFT':-1}
        if blank==2:
          delta={'UP':-2,'RIGHT':1}
        if blank==3:
          delta={'RIGHT':1,'LEFT':-1,'UP':-2,'DOWN':3}
        else:
          delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}


        
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
            for j in range(i+1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j]!= 0:
                    inversion += 1
        
        return inversion % 2 == 0
    
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        # Don't include zero. The heuristic function never ever overestimate the true cost
        # but the default one does

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))





def displayDuckPuzzle(state):
    indexofduckdisplay=0;
    for indexofduckdisplay in range(0,2,2):
        if state[0]==0:
         print('*',state[1]);
        elif state[1]==0:
         print(state[0],'*');
        else:
         print(state[0],state[1]);

    for indexofduckdisplay in range (2,6,4):
        if state[indexofduckdisplay]==0:
            print('*',state[indexofduckdisplay+1],state[indexofduckdisplay+2],state[indexofduckdisplay+3]);
        elif state[indexofduckdisplay+1]==0:
            print(state[indexofduckdisplay],'*',state[indexofduckdisplay+2],state[indexofduckdisplay+3]);
        elif state[indexofduckdisplay+2]==0:
            print(state[indexofduckdisplay],state[indexofduckdisplay+1],'*',state[indexofduckdisplay+3]);
        elif state[indexofduckdisplay+3]==0 :
            print(state[indexofduckdisplay],state[indexofduckdisplay+1],state[indexofduckdisplay+2],'*');
        else :
            print(state[indexofduckdisplay],state[indexofduckdisplay+1],state[indexofduckdisplay+2],state[indexofduckdisplay+3]);

    for indexofduckdisplay in range (6,9,3):
        if state[indexofduckdisplay]==0:
            print('','*',state[indexofduckdisplay+1],state[indexofduckdisplay+2]);
        elif state[indexofduckdisplay+1]==0:
            print('',state[indexofduckdisplay],'*',state[indexofduckdisplay+2]);
        elif state[indexofduckdisplay+2]==0:
            print('',state[indexofduckdisplay],state[indexofduckdisplay+1],'*');
        else :
            print('',state[indexofduckdisplay],state[indexofduckdisplay+1],state[indexofduckdisplay+2])




def make_random_DuckPuzzle():
    duckstate=[1,2,3,4,5,6,7,8,0];
    duck_puzzle=DuckPuzzle(duckstate)
    unsolvedstate=duckstate
    for i in range(random.randint(1,100)):
        posaction=duck_puzzle.actions(unsolvedstate);
        randlegalactions=random.choice(posaction);
        unsolvedstate=duck_puzzle.result(unsolvedstate,randlegalactions);
    #displayDuckPuzzle(unsolvedstate);

    return DuckPuzzle(unsolvedstate);





def manhattanDuckpuzzle(node):
    duckmanhattandistance=0;
    duckgoalindex={1:[0,0],2:[0,1],3:[1,0],4:[1,1],5:[1,2],6:[1,3],7:[2,1],8:[2,2],0:[2,3]};
    duckcurrent={};
    duckindex=[[0,0],[0,1],[1,0],[1,1],[1,2],[1,3],[2,1],[2,2],[2,3]];
    currentstate=node.state;
    x, y = 0, 0
    
    for i in range(len(currentstate)):
        duckcurrent[currentstate[i]] = duckindex[i]
    
    duckmanhattandistance = 0

    # Don't include zero. The heuristic function never ever overestimate the true cost
    # but the default one does
    for i in range(1,9):
        for j in range(2):
            duckmanhattandistance = abs(duckgoalindex[i][j] - duckcurrent[i][j]) + duckmanhattandistance
    
    return duckmanhattandistance


def AmisplacedheuristicDuckPuzzle():
    bbb=make_random_DuckPuzzle();
    displayDuckPuzzle(bbb.initial);
    starttime1=time.time();
    r1,total1=astar_search(bbb);
    

    print("This is solution ", r1.solution());

    print("Length is =", len(r1.solution()));
    endtime1=time.time();
    
    elapsedtime1=endtime1-starttime1;
    print("Elapsed time", elapsedtime1);
    print("Total number of pops",total1);

    print("Manhattan DuckPuzzle on the run");
    manhattanstate1=bbb;
    displayDuckPuzzle(bbb.initial)
    manhattanstarttime1=time.time();
    resultmanhattan1,totalmanhattan1=astar_search(manhattanstate1,h=manhattanDuckpuzzle);
    endtimemanhattan1=time.time();
    elapsedtimemanhattan1=endtimemanhattan1-manhattanstarttime1;
    print("This solution is", resultmanhattan1.solution());
    print("Length of the solution is", len(resultmanhattan1.solution()));
    print(f"Elapsed time is = ",elapsedtimemanhattan1);
    print("Total number of pops",totalmanhattan1);

    print("Maxofboth DuckPuzzle heuristic on the run")
    maxofboth1=bbb;
    displayDuckPuzzle(maxofboth1.initial);
    maxofbothstarttime1=time.time();
    resultmaxofboth1,totalpopsmaxofboth1=astar_search(maxofboth1,h=maxofbothheuristicDuck);
    maxofbothendtime1=time.time();
    maxofbothelapsedtime1=maxofbothendtime1-maxofbothstarttime1;
    print("The solution is", resultmaxofboth1.solution());
    print("Length of the solution is=",len(resultmaxofboth1.solution()));
    print(f"Elapsed time",maxofbothelapsedtime1);
    print("Total number of pops",totalpopsmaxofboth1);

def maxofbothheuristicDuck(node):
    newpuzzle1=DuckPuzzle(node.state);
    return(max(manhattanDuckpuzzle(node),newpuzzle1.h(node)));

#AmisplacedheuristicDuckPuzzle()
def runningDuckPuzzle10times():
    for i in range (0,10):
        print("Running",i,"another", 9-i,"Times")
        AmisplacedheuristicDuckPuzzle();

runningDuckPuzzle10times();


    






















