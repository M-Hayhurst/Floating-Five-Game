'''The AI routine for five in a row. This function will take a board object as argument and return a coordinate, denoting the computers move'''
import numpy as np
from random import choice as RandomChoice

AIversion = '3'

def RowToThreat(row,char):
	'''takes a list or chars. Returns a list with elements (A,i) where A is the streak size obtained by inserting char at index i
	I'm pretty sure it works... '''
	results=[]
	for i in range(len(row)):	#loop through each element
		if row[i] != ' ':	#we are only interrested in open elements
			pass
		else:
			leftChars=0		#number of uninterrupted chars to the left
			leftSpaces=0	#elements to the left of the chars which aren't the opponent and can thus potentially contribute to a steak
			n=i
			while n>0:
				n-=1 	#move one element to the left
				if row[n]==char and leftSpaces == 0:	#if the element is a char, and no spaces have yet been encountered
					leftChars+=1
				elif row[n] in {' ',char}:	#if element is a space, or a space has earlier been encountered
					leftSpaces+=1
				else:	#element must be opponent character
					break

			rightChars = 0	#do the same, moving to the right
			rightSpaces = 0
			n=i
			while n<len(row)-1:
				n+=1
				if row[n]==char and rightSpaces == 0:
					rightChars+=1
				elif row[n] in {' ',char}:
					rightSpaces+=1
				else:
					break

			if rightSpaces and leftSpaces:
				modifier = 0.2	#add 0.2 to the score if two way expansion is possible
			else:
				modifier = 0
			if char == 'o':
				modifier += 0.1 #make if preferable to inprove the computers stance

			if rightChars+leftChars>0 and rightChars+rightSpaces+leftChars+leftSpaces>=4:	#first condition ensures char in the middle of nowhere dont get counted. Second condition ensures only pential 5-streak get counted 
				results.append([leftChars+rightChars+1+modifier,i])

	return results

def MakeThreatList(board,l,h):
	result = []
	for char in {'x','o'}:
		# Do rows
		for n in range(h):
			rowRes = RowToThreat(board[n,:],char)
			for x in rowRes:
				result.append([x[0], (n,x[1]) ])	#append threatlevel, row num, coloum num
	
		# Do coloums
		for n in range(h):
			rowRes = RowToThreat(board[:,n],char)
			for x in rowRes:
				result.append([x[0], (x[1],n) ])	#append threatlevel, row num, coloum num
	
		#do the top left diagonals
		for s in range(-h+1,l):	#s is the diagonal number
			rowRes = RowToThreat(board.diagonal(s),char)
			for x in rowRes:
				if s<0:
					result.append([x[0], (-s+x[1],x[1]) ])
				else:
					result.append([x[0], (x[1],s+x[1]) ])
	
		#do the top left diagonals
		for s in range(-h+1,l):	#s is the diagonal number
			rowRes = RowToThreat(np.fliplr(board).diagonal(s),char)
			for x in rowRes:
				if s<0:
					result.append([x[0], (-s+x[1], abs(x[1] - (l-1))) ])	#just as before, except we mirror the coloums number around the center
				else:
					result.append([x[0], (x[1], abs(s+x[1] - (l-1))) ])

	#result = list(set(result))	#remove double ocurrences in an easy but ineffecient way
	#result.sort(reverse=True)	#sort after threat, with the highest threat in the top of the list
	return result

def AIGetMove(board, verbose=False):
	'''compile list of possible coordinates and threat levels'''
	threatList = MakeThreatList(board.b,board.l,board.h)
	lCords = [] # a list of coordinates returned by MakeThreatList
	lThreat = []

	for (threat,cord) in threatList:
		if cord not in lCords:
			lCords.append(cord)
			lThreat.append([threat])
		else:
			lThreat[lCords.index(cord)].append(threat)

	#sort the threat lists and fill with zeros so all have length 8
	for theat in lThreat:
		theat.sort(reverse=True)
		theat.extend([0]*(8-len(theat)))

	if verbose:
		print('\n'*5)
		for line in zip(lCords,lThreat):
			print(line)

	for i in range(8):	# as each theatlist can only have 8 elements, 4 for each player
		maxThreat = max([x[i] for x in lThreat] )

		# remove cords if corrosponding theats if they are less than the maximum
		lCords = [lCords[n] for n in range(len(lCords)) if lThreat[n][i] >= maxThreat]
		lThreat = [lThreat[n] for n in range(len(lThreat)) if lThreat[n][i] >= maxThreat]
		
		if verbose:
			print('Sorting after i=',i,':')
			print(list(zip(lCords,lThreat))) 

		if len(lCords) == 1:
			return lCords[0]

	# if all remaining options are equally good, choose one at random
	return RandomChoice(lCords)



if __name__ == '__main__':
	import fiveRow2
	#testBoard = np.array([[' ','x','x','o'],['o',' ',' ','x'],[' ',' ','o','x'],[' ',' ','o',' ']])
	#print testBoard
	#xList = MakeThreatList(testBoard,4,4,'x')
	#print 'xList:',xList
	#oList = MakeThreatList(testBoard,4,4,'o')
	#print 'oList:',oList

	testRows = []

	testBoard = fiveRow2.Board(8,8)
	testBoard.AddChar('x',(3,3))
	testBoard.AddChar('x',(4,4))
	testBoard.AddChar('x',(5,5))
	#testBoard.AddChar('o',(5,6))
	testBoard.printBoard()

	y = AIGetMove(testBoard,verbose=True)
	print(y)




##fill up the test board with human moves
#testBoard.b = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
#
#testBoard.printBoard()
#
#
## generate the 4 versions of the testboard
#norm = testBoard.b
#
#diag = [norm.diagonal(i) for i in range(-testBoard.h+1,testBoard.l)]
#revDiag = [np.fliplr(norm).diagonal(i) for i in range(-testBoard.l+1,testBoard.h)]

