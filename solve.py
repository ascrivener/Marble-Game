from copy import deepcopy


state_dict = {}

class State:
	def __init__(self, board, numPieces):
		self.board = board
		self.numPieces = numPieces

	def hasWon(self):
		return self.numPieces == 1

	def __str__(self):
		return ('\n'.join([' '.join([str(x) for x in row]) for row in self.board])) + '\n'

	def getChildren(self):
		dirs = [[-1,0],[0,-1],[1,0],[0,1]]
		children = []
		for i in range(7):
			for j in range(7):
				if self.board[i][j] == '-':
					for dir in dirs:
						i_1 = i+2*dir[0]
						j_1 = j+2*dir[1]
						i_2 = i+dir[0]
						j_2 = j+dir[1]
						if inRange(i_1,j_1) and self.board[i_1][j_1] == 'X' and self.board[i_2][j_2] == 'X':
							newState = State(deepcopy(self.board),deepcopy(self.numPieces))
							newState.board[i][j] = 'X'
							newState.board[i_1][j_1] = '-'
							newState.board[i_2][j_2] = '-'
							newState.numPieces-=1
							# print str(newState)
							children.append(newState)

		return children

	def heuristic(self):
		s = 0
		for i in range(7):
			for j in range(7):
				if self.board[i][j] == 'X':
					s += (i-3)**2 + (j-3)**2

		return s

	def __eq__(self,other):
		if not isinstance(other,State):
			return False

		test = True
		for i in range(7):
			if test == False:
				break
			for j in range(7):
				if self.board[i][j] != other.board[i][j]:
					test = False
					break

		return test

	def __hash__(self):
		return hash(frozenset([frozenset(row) for row in self.board]))




def inRange(i,j):
	return 0 <= i and i < 7 and 0 <= j and j < 7

def search(state):
	print str(state)
	print len(state_dict)
	if state in state_dict:
		# print str(state)
		return state_dict[state]
	elif (state.hasWon()):
		print str(state)
		state_dict[state] = 1
		return 1
	else:
		pathToWin = False
		l = sorted(state.getChildren(),key=lambda state : state.heuristic())
		for i in range(2):
			if (len(l) > i and search(l[i]) == 1):
				pathToWin = True
				break
		if pathToWin:
			state_dict[state] = 1
			return 1
		else:
			state_dict[state] = -1
			return -1

if __name__ == '__main__':
	# print hash(frozenset([frozenset([1])]))

	init = [[0]*7 for x in range(7)]
	for i in range(7):
		for j in range(7):
			if (2 <= i and i <= 4) or (2 <= j and j <= 4):
				init[i][j] = 'X'
				if i == 3 and j == 3:
					init[i][j] = '-'


	curState = State(init,32)
	search(curState)