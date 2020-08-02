from search import *
import array as arr 
import time
import random 


def make_rand_8puzzle():    
	newpuzzle = EightPuzzle(())
	possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

	iterations = random.randint(1,100)


	goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)
	solvability = False;
	while solvability == False:
		for i in range(iterations):
			# randomaction = random.randint(0,3)
			newactions = newpuzzle.actions(goal);
			theaction = random.choice(newactions)
			goal = newpuzzle.result(goal,theaction);
		if newpuzzle.check_solvability(goal):
			break; 
	return goal ;


def display(state):
	a = state; 
	for i in range(0,len(state)):
		if(a[i] == 0):
			print("*",end = " ")
		else:
			print(a[i],end = " ")
		if (i+1) % 3 == 0:
			print("\n");
	
	return 

def new_best_first_graph_search(problem, f, display=False):
	"""Search the nodes with the lowest f scores first.
	You specify the function f(node) that you want to minimize; for example,
	if f is a heuristic estimate to the goal, then we have greedy best
	first search; if f is node.depth then we have breadth-first search.
	There is a subtlety: the line "f = memoize(f, 'f')" means that the f
	values will be cached on the nodes as they are computed. So after doing
	a best first search you can examine the f values of the path returned."""
	popcnt = 0 ;
	f = memoize(f, 'f')
	node = Node(problem.initial)
	frontier = PriorityQueue('min', f)
	frontier.append(node)
	explored = set()
	while frontier:
		node = frontier.pop()
		popcnt+=1;
		if problem.goal_test(node.state):
			if display:
				print(len(explored), " paths have been expanded and", len(frontier), "paths remain in the frontier")
			return (len(node.path())-1,popcnt)
		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				frontier.append(child)
			elif child in frontier:
				if f(child) < frontier[child]:
					del frontier[child]
					frontier.append(child)
	return None


def astar_search(problem, h=None, display=False):
	"""A* search is best-first graph search with f(n) = g(n)+h(n).
	You need to specify the h function when you call astar_search, or
	else in your Problem subclass."""
	h = memoize(h or problem.h, 'h')
	return new_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


class solveEightPuzzle(Problem):
	
	def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
		""" Define goal state and initialize a problem """
		super().__init__(initial, goal)
		self.initial = initial

		
	def actions(self,state):
		puzzle = EightPuzzle(())
		ans = puzzle.actions(state)
		return ans

	def result(self,state,action):
		ret = ()
		puzzle = EightPuzzle(());
		ans = puzzle.result(state,action)
		return ans;



	def manhattandist(self,node):
		tiles = {};
		tiles[1] = (0,0);
		tiles[2] = (0,1);
		tiles[3] = (0,2);
		tiles[4]  = (1,0);
		tiles[5] = (1,1);
		tiles[6] = (1,2);
		tiles[7] = (2,0);
		tiles[8] = (2,1);

		tups = node.state;
		sum = 0 ;
		for nums in range(0,len(tups)):
			if tups[nums] == 0 :
				continue;
			x = nums/3;
			y = nums%3;

			coordinate = tiles[tups[nums]];
			sum+=(abs(coordinate[0] - x) + abs(coordinate[1] - y));
		return sum ;

	def maxoftwoh(self,node):
		puzzle = EightPuzzle(())
		num1 = puzzle.h(node);
		num2 = self.manhattandist(node);
		return max(num1,num2);


	def solvebyh(self,state):
		theproblem = Problem(state,self.goal)
		theproblem.actions = self.actions
		theproblem.result = self.result
		puzzle = EightPuzzle(())
		
		package = astar_search(theproblem,puzzle.h);
	  
	   
		return package

	def solvebyMan(self,state):
		theproblem = Problem(state,self.goal)
		theproblem.actions = self.actions
		theproblem.result = self.result
		package = astar_search(theproblem,self.manhattandist)
	  
		
		return package

	def solvebymaxof2(self,state):
		theproblem = Problem(state,self.goal)
		theproblem.actions = self.actions
		theproblem.result = self.result
		package = astar_search(theproblem,self.maxoftwoh)
	 
		
		return package

def make_rand_DuckPuzzle():
	possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

	iterations = random.randint(1,1000)

	delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}

	puzzle = DuckPuzzle(());
	goal=(1, 2, 100, 100, 3, 4, 5, 6, 100, 7, 8, 0)
	for i in range(iterations):
		# randomaction = random.randint(0,3)
		newactions = puzzle.actions(goal);
		theaction = random.choice(newactions)
		goal = puzzle.result(goal,theaction);
	return goal ;


class DuckPuzzle(Problem):
	def __init__(self, initial, goal=(1, 2, 100, 100, 3, 4, 5, 6, 100, 7, 8, 0)):
		""" Define goal state and initialize a problem """
		super().__init__(initial, goal)

	def find_blank_square(self, state):
		"""Return the index of the blank square in a given state"""

		return state.index(0)

	def actions(self,state):
		possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
		index_blank_square = self.find_blank_square(state)



		if index_blank_square ==1  or index_blank_square == 7 or index_blank_square ==11:
			possible_actions.remove('RIGHT')
		if index_blank_square == 4 or index_blank_square == 9 or index_blank_square == 10 or index_blank_square == 11:
			possible_actions.remove('DOWN')
		if index_blank_square == 0 or index_blank_square == 4 or index_blank_square ==9:
			possible_actions.remove('LEFT')
		if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 6 or index_blank_square ==7:
			possible_actions.remove('UP')

		return possible_actions


	def goal_test(self,state):
		return state == self.goal

	def result(self,state,action):

		blank = self.find_blank_square(state)
		new_state = list(state)

		delta = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}

		neighbor = blank + delta[action]

		new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank];


		return tuple(new_state)



	def h(self,node):
		goalsize = len(self.goal)
		diff = 0 ;
		thestate = node.state;
		for i in range(0,goalsize):

			if self.goal[i] != thestate[i]:
				diff+=1;
		return diff
		
	def manhattandist(self,node):
		goalsize = len(self.goal)
		thestate = node.state;
		tiles = {}
		for i in range(0,goalsize):
			if self.goal[i] == -1 or self.goal[i] == 0 :
				continue;
			tiles[self.goal[i]] = (i/4,i%4)

		total = 0 ;

		for i in range(0,goalsize):
			if thestate[i] == -1 or thestate[i] == 0:
				continue;

			if thestate[i] != self.goal[i]:
				x = i/4;
				y = i%4;
				thenum = tiles[thestate[i]]

				total += (abs(x-thenum[0])  + abs(y-thenum[1]) );

		return total; 

	def maxoftwoh(self,node):
		num1 = self.h(node);
		num2 = self.manhattandist(node);
		return max(num1,num2);

	def solvebyh(self,state):
		theproblem = Problem(state,self.goal)
		theproblem.actions = self.actions
		theproblem.result = self.result
		package = astar_search(theproblem,self.h);
		return package

	def solvebyMan(self,state):
		theproblem = Problem(state,self.goal)
		theproblem.actions = self.actions
		theproblem.result = self.result
		package = astar_search(theproblem,self.manhattandist)
		return package

	def solvebymaxof2(self,state):
		theproblem = Problem(state,self.goal)
		theproblem.actions = self.actions
		theproblem.result = self.result
		package = astar_search(theproblem,self.maxoftwoh)
		return package
		
		
	def display(self,state):
		a = state;
		for i in range(0,len(a)):
			if(a[i] == 0):
				print("*",end= " ")
			elif a[i] != 100:
				print(a[i],end = " ")
			else:
				print("-",end = " ")
			if (i+1)%4 == 0 :
				print("\n");
	
		return 
   
# ___________________________________


def eightpuzzle():
	temp = EightPuzzle(())
	for i in range(10) :
		puzzle = solveEightPuzzle(())
		tups = make_rand_8puzzle()
		display(tups)
		

	
		print("solvebyh")
		print("--------------")

		start_time = time.time();
		package = puzzle.solvebyh(tups)
		elapsed_time = time.time() - start_time
		print("it took ",elapsed_time," second");
		print("node path => ",package[0])
		print("nodes removed => " , package[1])
		print("\n");
		
		print("solvebyMan")
		print("--------------")

		start_time = time.time()
		package = puzzle.solvebyMan(tups)
		elapsed_time = time.time()-start_time
		print("it took ",elapsed_time," second");
		print("node path => ",package[0])
		print("nodes removed => " , package[1])
		print("\n");
		
		print("solvebymaxof2")
		print("--------------")

		start_time = time.time()
		package = puzzle.solvebymaxof2(tups)
		elapsed_time = time.time()-start_time
		print("it took ",elapsed_time," second");
		print("node path => ",package[0])
		print("nodes removed => " , package[1])

def duckpuzzle():
	for i in range(10):
		puzzle = DuckPuzzle(())
		tups = make_rand_DuckPuzzle()
		puzzle.display(tups)


		print("\n");
		print("--------------")
		print("solvebyh")
		print("--------------")

		start_time = time.time();
		package = puzzle.solvebyh(tups)
		elapsed_time = time.time() - start_time
		print("it took ",elapsed_time," second");
		print("node path => ",package[0])
		print("nodes removed => " , package[1])
		
		print("\n");
		print("--------------")
		print("solvebyMan")
		print("--------------")

		start_time = time.time()
		package = puzzle.solvebyMan(tups)
		elapsed_time = time.time()-start_time
		print("it took ",elapsed_time," second");
		print("node path => ",package[0])
		print("nodes removed => " , package[1])
		print("\n");
		print("--------------")
		print("solvebymaxof2")
		print("--------------")

		start_time = time.time()
		package = puzzle.solvebymaxof2(tups)
		elapsed_time = time.time()-start_time
		print("it took ",elapsed_time," second");
		print("node path => ",package[0])
		print("nodes removed => " , package[1])


# to run eightpuzzle

eightpuzzle()

# to run duckpuzzle
duckpuzzle()
