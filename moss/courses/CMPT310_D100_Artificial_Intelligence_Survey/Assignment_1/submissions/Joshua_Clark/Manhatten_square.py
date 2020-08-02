import random
import time
def actions(state,index):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['RIGHT', 'DOWN', 'UP', 'LEFT']

        if index % 3 == 0:
            possible_actions.remove('LEFT')
        if index < 3:
            possible_actions.remove('UP')
        if index % 3 == 2:
            possible_actions.remove('RIGHT')
        if index > 5:
            possible_actions.remove('DOWN')

        return possible_actions

def result(state, action, value, index):


    new_state = list(state)

    delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
    new = index + delta[action]
    new_state[new] = value


    return tuple(new_state)
def display(state):
        temp = list(state)
        index = temp.index(0)
        temp[index] = '*'
        matrix = [temp[i:i+3] for i in range(0,len(temp),3)]
        for l in matrix:
                print (l)
def make_rand_8puzzle(current):
        current = random.sample(range(9),9)
        return current
        
x0 = (0,1,2,1,2,3,2,3,4)
x1 = (1,0,1,2,1,2,3,2,3)
x2 = (2,1,0,3,2,1,4,3,2)
x3 = (1,2,3,0,1,2,1,2,3)
x4 = (2,1,2,1,0,1,2,1,2)
x5 = (3,2,1,2,1,0,3,2,1)
x6 = (2,3,4,1,2,3,0,1,2)
x7 = (3,2,3,2,1,2,1,0,1)
x8 = (4,3,2,3,2,1,2,1,0)

diff = (x0,x1,x2,x3,x4,x5,x6,x7,x8)

moves = [[1],[2],[3],[4],[5],[6],[7],[8]]

delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
goal = (1,2,3,4,5,6,7,8,0)

init = current =(1,2,3,4,5,6,7,8,0)

init = current = make_rand_8puzzle(current)
display(current)
start_time = time.time()
accum = 0
for x in range(len(init)):
    current = init
    prev = diff[current[x]-1][x]
    new = x
    value = current[x]
    while((diff[value-1][new] > 0) and init[x] != 0):
        action = actions(current,new)
        for thing in action:
            value = current[new]
            results = result(current,thing,value,new)
            temp = new + delta[thing]
            if(diff[value-1][temp] < prev):
                    new = temp
                    current = results
                    prev = diff[value-1][temp]
                    accum += 1
                    moves[value-1].append(thing)
                    break
        
print("accum is ",accum)
for x in range (len(moves)):
        print(moves[x])
elapsed_time = time.time() - start_time
print(elapsed_time)

