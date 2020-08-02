import random
def actions(state,index):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['RIGHT', 'DOWN', 'UP', 'LEFT']
        #index_blank_square = state.index(value)

        if index < 2 or index == 4 or index == 5:
            possible_actions.remove('UP')
        if index > 5 or index == 2:
            possible_actions.remove('DOWN')
        if index % 4 == 1 or index == 8:
            possible_actions.remove('RIGHT')
        if index % 4 == 2 or index == 0:
            possible_actions.remove('LEFT')

        return possible_actions

def result(state, action, value, index, delta):

    new_state = list(state)


    new = index + delta[action]

    new_state[new] = value

    return tuple(new_state)

def fun_delta(delta,index):
        if index == 0:
                delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif index == 1:
                delta = {'UP': -3, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif index == 2:
                delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        elif index == 3:
                delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
                delta = delta
        return delta
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

x0 = (0,1,1,2,3,4,3,4,5)
x1 = (1,0,2,1,2,3,2,3,4)
x2 = (1,2,0,1,2,3,2,3,4)
x3 = (2,1,1,0,1,2,1,2,3)
x4 = (3,2,2,1,0,1,2,1,2)
x5 = (4,3,3,2,1,0,3,2,1)
x6 = (3,2,2,1,2,3,0,1,2)
x7 = (4,3,3,2,1,2,1,0,1)
x8 = (5,4,4,3,2,1,2,1,0)

diff = (x0,x1,x2,x3,x4,x5,x6,x7,x8)

moves = [[1],[2],[3],[4],[5],[6],[7],[8]]

delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
goal = (1,4,3,2,5,6,7,8,0)
current = (1,2,3,4,5,6,7,8,0)

init = current = make_rand_8puzzle(current)
display(current)
accum = 0
print(init)
for x in range(len(init)):
    current = init
    prev = diff[current[x]-1][x]
    new = x
    value = current[x]
    while((diff[value-1][new] > 0) and init[x] != 0):
        this_delta = fun_delta(delta,new)
        action = actions(current,new)
        for thing in action:
            value = current[new]
            results = result(current,thing,value,new,this_delta)
            temp = new + this_delta[thing]
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


