"""
A Simple Minesweeper
Beat this game: make your self the top 0.0%
"""

import argparse
import random
import tkinter as tk
import tkinter.font as tkfont

_gameStarted = False
_gameScores = 0

def adjacent(i, j, N, M, diag=False):
	def valid(i, j):
		return (0 <= i < N) and (0<= j < M)
	
	for vx in range(-1, 2):
		for vy in range(-1, 2):
			vvalid = ((vx!=0) or (vy!=0)) if diag else ((vx!=0) != (vy!=0))
			if vvalid:
				nx, ny = i+vx, j+vy
				if valid(nx, ny):
					yield (nx, ny)

def sumAround(i, j, N, M, data):
	return sum(data[x][y]==1 for x, y in adjacent(i, j, N, M, diag=True))

def startGame(dats, i, j):
	global _gameStarted
	
	_gameStarted = True
	N, M, BCNT, buttons, data = dats
	
	bombs = set(random.sample(range(0, N*M), BCNT))
	while (i*M + j) in bombs:
		bombs = set(random.sample(range(0, N*M), BCNT))
	
	for i in range(N):
		for j in range(M):
			data[i][j] = int((i*M + j) in bombs)
	
	return

def dfs(i, j, N, M, data, connects):
	data[i][j] = -1
	connects.append((i, j))
	
	if sumAround(i, j, N, M, data) == 0:
		for x, y in adjacent(i, j, N, M, diag=True):
			if data[x][y] == 0:
				dfs(x, y, N, M, data, connects)

def updateGrid(dats, i, j):
	N, M, BCNT, buttons, data = dats
	if data[i][j] == 1:
		for i in range(N):
			for j in range(M):
				if data[i][j] == 1:
					buttons[i][j].configure(background='#ff0000', text=' ')
				
				buttons[i][j].configure(state='disabled')
		
		return False
	
	else:
		blockConnect = []
		dfs(i, j, N, M, data, blockConnect)
		for x, y in blockConnect:
			btn = buttons[x][y]
			
			sumadj = sumAround(x, y, N, M, data)
			sumtxt = str(sumadj) if sumadj else ' '
			
			btn.configure(background='#ffffff', text=sumtxt)
			btn.configure(state='disabled')
		
		if all(all(data[i][j] != 0 for j in range(M)) for i in range(N)):
			for i in range(N):
				for j in range(M):
					if data[i][j] == 1:
						buttons[i][j].configure(background='#00ff00', text=' ')
					
					buttons[i][j].configure(state='disabled')
		
		return True

def onBtnPressed(event, i, j, dats):
	global _gameStarted, _gameScores
	
	N, M, BCNT, buttons, data = dats
	
	if not _gameStarted:
		startGame(dats, i, j)
	
	btn = buttons[i][j]
	if btn['state'] == 'disabled':
		return
	
	if updateGrid(dats, i, j):
		_gameScores += N*M

def parseArgs():
	parser = argparse.ArgumentParser(description='A minesweeper game.')
	parser.add_argument('-s', '--size', type=int, nargs=2, default=(10, 20),
						metavar=('N', 'M'), help='Set the area size.')
	
	parser.add_argument('-c', '--count', type=int, default=30,
						help='Set the number of mines.')
	
	args = parser.parse_args()
	N, M, BCNT = (*args.size, args.count)
	N = max(1, N)
	M = max(1, M)
	BCNT = max(0, min(BCNT, N*M-1))
	
	return (N, M, BCNT)

def printScoring():
	global _gameScores
	
	_logbase = 1.101382
	print('You scored: ', _gameScores)
	print('Only {}% can do this.'.format(100 // math.log(_gameScores, _logbase)))
	
	return

def main():
	N, M, BCNT = parseArgs()
	
	root = tk.Tk()
	root.wm_attributes('-fullscreen', 'true')
	
	for i in range(N):
		root.grid_rowconfigure(i, weight=1)
	
	for j in range(M):
		root.grid_columnconfigure(j, weight=1)
	
	btnFont = tkfont.Font(family='Consolas', size=32)
	buttons = [[] for i in range(N)]
	data = [[-1]*M for i in range(N)]
	dats = (N, M, BCNT, buttons, data)
	
	for i in range(N):
		for j in range(M):
			btn = tk.Button(root)
			buttons[i].append(btn)
			
			btn.grid(row=i, column=j, sticky='nsew')
			btn.configure(font=btnFont, text=' ', background='#e8ed87')
			
			mkPress = lambda i, j, dats: (lambda event: onBtnPressed(event, i, j, dats))
			btn.bind('<Button-1>', mkPress(i, j, dats))
	
	root.bind('<Escape>', lambda event: root.destroy())
	root.mainloop()
	
	printScoring()

main()
