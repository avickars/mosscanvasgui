# a1.py
from search import *
from notebook import psource, heatmap, gaussian_kernel, show_map, final_path_colors, display_visual, plot_NQueens

# Needed to hide warnings in the matplotlib sections
import warnings
warnings.filterwarnings("ignore")
import time

arr=[0, 1, 2, 3, 4, 5, 6, 7, 8]
def make_rand_8puzzle():
    random.shuffle(arr)
    while True:
        retPz = EightPuzzle((arr[2], arr[4], arr[3], arr[1], arr[5], arr[6], arr[7], arr[8], arr[0])) 
        if retPz.check_solvability((arr[2], arr[4], arr[3], arr[1], arr[5], arr[6], arr[7], arr[8], arr[0])):
            display(arr)
            return retPz
        else:
            random.shuffle(arr)

def display(state):
    for i in range(9):
        if state[i] == 0:
            print("*", end = ' ')
        else:
            print(state[i], end = ' ')
        if (i+1) % 3 == 0:
            print("")

print("---Part 2 Starts---")
print("---pz1---")
pz1 = make_rand_8puzzle()
print("---pz2---")
pz2 = make_rand_8puzzle()
print("---pz3---")
pz3 = make_rand_8puzzle()
print("---pz4---")
pz4 = make_rand_8puzzle()
print("---pz5---")
pz5 = make_rand_8puzzle()
print("---pz6---")
pz6 = make_rand_8puzzle()
print("---pz7---")
pz7 = make_rand_8puzzle()
print("---pz8---")
pz8 = make_rand_8puzzle()
print("---pz9---")
pz9 = make_rand_8puzzle()
print("---pz10---")
pz10 = make_rand_8puzzle()
print("")

#misplaced title heuristic
print("---misplaced Tiles Heristice---")
start_time_initial = time.time()
start_time = start_time_initial
print("---pz1---")
print(astar_search(pz1).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz2---")
print(astar_search(pz2).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = start_time_initial
print("---pz3---")
print(astar_search(pz3).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz4---")
print(astar_search(pz4).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = start_time_initial
print("---pz5---")
print(astar_search(pz5).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz6---")
print(astar_search(pz6).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = start_time_initial
print("---pz7---")
print(astar_search(pz7).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz8---")
print(astar_search(pz8).solution())
print("local elapsed time: ", time.time() - start_time)
print("---pz9---")
print(astar_search(pz9).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz10---")
print(astar_search(pz10).solution())
print("local elapsed time: ", time.time() - start_time)
print("global elapsed time: ", time.time() - start_time_initial)
print("")

#Manhattan
print("---Manhattan distance Heristice---")
start_time_initial = time.time()
start_time = start_time_initial
print("---pz1---")
print(astar_search(pz1, manhattan).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz2---")
print(astar_search(pz2, manhattan).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = start_time_initial
print("---pz3---")
print(astar_search(pz3, manhattan).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz4---")
print(astar_search(pz4, manhattan).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = start_time_initial
print("---pz5---")
print(astar_search(pz5, manhattan).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz6---")
print(astar_search(pz6, manhattan).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = start_time_initial
print("---pz7---")
print(astar_search(pz7, manhattan).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz8---")
print(astar_search(pz8, manhattan).solution())
print("local elapsed time: ", time.time() - start_time)
print("---pz9---")
print(astar_search(pz9, manhattan).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz10---")
print(astar_search(pz10, manhattan).solution())
print("local elapsed time: ", time.time() - start_time)
print("global elapsed time: ", time.time() - start_time_initial)
print("")

#Max
print("---Max of two---")
start_time_initial = time.time()
start_time = start_time_initial
print("---pz1---")
print(astar_search(pz1, max_heuristic).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz2---")
print(astar_search(pz2, max_heuristic).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = start_time_initial
print("---pz3---")
print(astar_search(pz3, max_heuristic).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz4---")
print(astar_search(pz4, max_heuristic).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = start_time_initial
print("---pz5---")
print(astar_search(pz5, max_heuristic).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz6---")
print(astar_search(pz6, max_heuristic).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = start_time_initial
print("---pz7---")
print(astar_search(pz7, max_heuristic).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz8---")
print(astar_search(pz8, max_heuristic).solution())
print("local elapsed time: ", time.time() - start_time)
print("---pz9---")
print(astar_search(pz9, max_heuristic).solution())
print("local elapsed time: ", time.time() - start_time)
start_time = time.time()
print("---pz10---")
print(astar_search(pz10, max_heuristic).solution())
print("local elapsed time: ", time.time() - start_time)
print("global elapsed time: ", time.time() - start_time_initial)
print("")

# test puzzles
# puzzle_1 = EightPuzzle((2, 4, 3, 1, 5, 6, 7, 8, 0))
# puzzle_2 = EightPuzzle((1, 2, 3, 4, 5, 6, 0, 7, 8))
# puzzle_3 = EightPuzzle((1, 2, 3, 4, 5, 7, 8, 6, 0))
print("Done!!")