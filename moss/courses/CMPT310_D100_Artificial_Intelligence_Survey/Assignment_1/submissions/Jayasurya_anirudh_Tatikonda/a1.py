# a1.py
import random
import time
from search import *

def make_rand_8puzzle():
    randomPuzzle = (random.randint(1,8),)
    #print(randomPuzzle)
    while len(randomPuzzle) < 8:
        var = random.randint(1,8)
        #print(var)
        if var in randomPuzzle :
            continue
        else :
            randomPuzzle = randomPuzzle + (var,)
    
    x = random.randint(0,8)
    randomPuzzle = randomPuzzle[ : (x) ] + (0,) + randomPuzzle[x:]
    eight = EightPuzzle(randomPuzzle)
    if eight.check_solvability(eight.initial):
        return eight
    else:
       return make_rand_8puzzle()


def display(state):
    counter = 0
    for i in state:
        if i == 0:
            print ('*' + ' ', end = '')
            counter += 1
        else:
            print(str(i) + ' ', end = '')
            counter += 1
        if counter == 3:
            print('\n')
            counter = 0
    print('\n')
        
eight = make_rand_8puzzle()
# print(eight.initial)
# eight.initial = (1,2,3,4,5,6,7,0,8)   
display(eight.initial)
start_time = time.time()
print(astar_search(eight).state)
elapsed_time = time.time() - start_time
print(f'elapsed time (in seconds): {elapsed_time}s')

# print(eight.check_solvability(eight.initial))

