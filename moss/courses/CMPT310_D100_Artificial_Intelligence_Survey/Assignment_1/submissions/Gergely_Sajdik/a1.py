# a1.py Gergely Sajdik 301142046


from search import *
import time


#-------------------------------------------------------------------------------------------------------------


#QUESTION 1:


#-------------------------------------------------------------------------------------------------------------

def make_rand_8puzzle():
	initialOrder = random.sample(range(9), 9)
	initialOrder = tuple(initialOrder)
	#initialOrder = (4,0,6,5,8,1,2,3,7)
	#initialOrder = (0,8,1,3,4,6,2,7,5)
	#initialOrder = (1,2,3,4,5,6,7,8,0)
	#initialOrder = (1,2,3,4,5,6,0,7,8)
	objName = EightPuzzle(initialOrder)
	while EightPuzzle.check_solvability(objName, objName.initial) == False:
	    initialOrder = random.sample(range(9), 9)
	    initialOrder = tuple(initialOrder)
	    objName = EightPuzzle(initialOrder)
	return objName

def display(state):
        counter = 0
        for i in range(len(state)):
            if counter == 3 or counter == 6:
                print("")
            if state[i] == 0:
                print("*", end = " ")
            else:
                print(state[i], end = " ")
            counter+=1
        print("\n")


"""Testing and example for Question 1"""
#thePuzzle = make_rand_8puzzle()
#display(thePuzzle.initial)
#print('The blank square is located at position ' + str(EightPuzzle.find_blank_square(thePuzzle,thePuzzle.initial)))
#print('The puzzle has been solved: ' + str(EightPuzzle.goal_test(thePuzzle, thePuzzle.initial)))
#print("\n")


#-------------------------------------------------------------------------------------------------------------


# QUESTION 2


#-------------------------------------------------------------------------------------------------------------

#Refactored code into one section for Question 2 to avoid code duplication
def runPuzzle(i, manhattan, findMax):

    thePuzzle = make_rand_8puzzle()
    thePuzzle.manhattanH = manhattan
    thePuzzle.findMaxH = findMax
    #startingNode = Node(thePuzzle.initial)
    #display(thePuzzle.initial)

    start_time = time.time()
    finalNode = astar_search(thePuzzle, display = True)
    elapsed_time = time.time() - start_time
    #display(finalNode.state)
    print("The elapsed time (in seconds) for Puzzle #" + str(i+1) + " is " + str(elapsed_time))
    print("The amount of moves required to solve the puzzle was " + str(finalNode.path_cost) + "\n")



#Remove the two # to run commented heuristic and from ln 92 (question2_8puzzle)
def question2_8puzzle():

    """Runs using default misplaced tile heuristic"""
    #for i in range(25):
        #runPuzzle(i, False, False)

    """Runs using manhattan heuristic"""
    #for i in range(25):
        #runPuzzle(i, True, False)

    """Runs using the max value of default and manhattan (compares them)"""
    #for i in range(25):
        #runPuzzle(i, False, True) 

#question2_8puzzle()


#-------------------------------------------------------------------------------------------------------------


# QUESTION 3


#-------------------------------------------------------------------------------------------------------------
def make_rand_Duckpuzzle():
	initialOrder = random.sample(range(9), 9)
	initialOrder = tuple(initialOrder)
	#initialOrder = (1,2,3,4,5,6,0,7,8)
	objName = DuckPuzzle(initialOrder)
	while DuckPuzzle.check_solvability(objName, objName.initial) == False:
	    initialOrder = random.sample(range(9), 9)
	    initialOrder = tuple(initialOrder)
	    objName = DuckPuzzle(initialOrder)
	return objName

def runDuckPuzzle(i, manhattan, findMax):

    thePuzzle = make_rand_Duckpuzzle()
    thePuzzle.manhattanH = manhattan
    thePuzzle.findMaxH = findMax
    #startingNode = Node(thePuzzle.initial)
    #display(thePuzzle.initial)

    start_time = time.time()
    finalNode = astar_search(thePuzzle, display = True)
    elapsed_time = time.time() - start_time
    #display(finalNode.state)
    if finalNode != None:
        print("The elapsed time (in seconds) for Puzzle #" + str(i+1) + " is " + str(elapsed_time))
        print("The amount of moves required to solve the puzzle was " + str(finalNode.path_cost) + "\n")


#Remove the two # to run commented heuristic and from ln 145 (question3_DuckPuzzle)
def question3_DuckPuzzle():

    """Runs using default misplaced tile heuristic"""
    #for i in range(5000):
        #runDuckPuzzle(i, False, False)

    """Runs using manhattan heuristic"""
    #for i in range(5000):
        #runDuckPuzzle(i, True, False)

    """Runs using the max value of default and manhattan (compares them)"""
    #for i in range(5000):
        #runDuckPuzzle(i, False, True) 

#question3_DuckPuzzle()





