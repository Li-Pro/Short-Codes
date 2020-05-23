import random
import tkinter as tk
import tkinter.font as tkfont

_gameStarted = False

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
	N, M, buttons, data = dats
	
	bombs = set(random.sample(range(0, N*M), (N*M) // 5))
	while (i*M + j) in bombs:
		bombs = set(random.sample(range(0, N*M), (N*M) // 5))
	
	for i in range(N):
		for j in range(M):
			data[i][j] = int((i*M + j) in bombs)
	
	return

def dfs(i, j, N, M, data, connects):
	data[i][j] = -1
	connects.append((i, j))
	
	if sumAround(i, j, N, M, data) == 0:
		for x, y in adjacent(i, j, N, M, diag=True):
			# print('##', x, y)
			if data[x][y] == 0:
				dfs(x, y, N, M, data, connects)

def updateGrid(dats, i, j):
	N, M, buttons, data = dats
	print(data[i][j])
	if data[i][j] == 1:
		for i in range(N):
			for j in range(M):
				if data[i][j] == 1:
					buttons[i][j].configure(background='#ff0000', text='*')
					buttons[i][j].configure(state='disabled')
	else:
		blockConnect = []
		dfs(i, j, N, M, data, blockConnect)
		print('#', blockConnect)
		for x, y in blockConnect:
			btn = buttons[x][y]
			# print(btn.keys())
			# print(btn['font'])
			
			sumadj = sumAround(x, y, N, M, data)
			sumtxt = str(sumadj) if sumadj else ''
			
			btn.configure(background='#ffffff', text=sumtxt)
			btn.configure(state='disabled')
	
	return

def onBtnPressed(event, i, j, dats):
	global _gameStarted
	
	N, M, buttons, data = dats
	
	if not _gameStarted:
		startGame(dats, i, j)
	
	# print('#', buttons)
	btn = buttons[i][j]
	if btn['state'] == 'disabled':
		return
	
	print('Pressed: ', i, j)
	# help(btn.getvar)
	# print(btn['state'])
	# print(*(x for x in dir(btn) if 'config' in x))
	
	updateGrid(dats, i, j)

def main():
	root = tk.Tk()
	root.wm_attributes('-fullscreen', 'true')
	
	N, M = 10, 20
	
	for i in range(N):
		root.grid_rowconfigure(i, weight=1)
	
	for j in range(M):
		root.grid_columnconfigure(j, weight=1)
	
	btnFont = tkfont.Font(family='Consolas', size=36)
	buttons = [[] for i in range(N)]
	data = [[-1]*M for i in range(N)]
	dats = (N, M, buttons, data)
	
	for i in range(N):
		for j in range(M):
			btn = tk.Button(root)
			buttons[i].append(btn)
			
			btn.grid(row=i, column=j, sticky='nsew')
			btn.configure(font=btnFont, text=' ')
			
			mkPress = lambda i, j, dats: (lambda event: onBtnPressed(event, i, j, dats))
			btn.bind('<Button-1>', mkPress(i, j, dats))
	
	root.bind('<Escape>', lambda event: root.destroy())
	root.mainloop()

main()