import tkinter as tk
import math
import time

def _hexRGB(r, g, b):
	return '{:02x}{:02x}{:02x}'.format(r, g, b)

def _fRGB(r, g, b):
	return '#' + _hexRGB(r, g, b)

#------------------------ Game Objects ------------------------------

class GameObject:
	def __init__(self, game):
		self.theGame = game
	
	def initDraw(self):
		return
	
	def update(self):
		return

class Player(GameObject):
	speed = 10
	def __init__(self, game):
		super().__init__(game)
		
		self.posX = game.WIDTH/2
		self.posY = game.HEIGHT/2
		
		self.lastVX = self.speed
		self.lastVY = 0
		
		self.lastShootTime = time.time()
	
	def initDraw(self):
		canvas = self.theGame.canvas
		posX, posY = self.posX, self.posY
		self.playerId = canvas.create_rectangle(posX-8, posY-8, posX+8, posY+8, fill='#ffd900')
	
	def move(self, vx=0, vy=0):
		if (not vx) and (not vy):
			return
		
		unitLen = math.sqrt(vx*vx + vy*vy)
		modUnit = self.speed / unitLen
		
		vx *= modUnit
		vy *= modUnit
		
		newPosX, newPosY = self.posX + vx, self.posY + vy
		if not self.theGame.isValidPos(newPosX, newPosY):
			return
		
		self.lastVX = vx
		self.lastVY = vy
		
		self.posX = newPosX
		self.posY = newPosY
		
		canvas = self.theGame.canvas
		canvas.move(self.playerId, vx, vy)
	
	def shoot(self, now):
		if now - self.lastShootTime >= 0.1:
			game = self.theGame
			game.addObj(Bullet(game, self))
			game.addObj(ShootFX(game, self))
			
			self.lastShootTime = now

class Bullet(GameObject):
	speed = 50
	def __init__(self, game, player):
		super().__init__(game)
		
		self.posX = player.posX
		self.posY = player.posY
		
		vX = player.lastVX
		vY = player.lastVY
		
		unitSpeed = math.sqrt(vX*vX + vY*vY)
		modUnit = self.speed / unitSpeed
		self.vX = vX * modUnit
		self.vY = vY * modUnit
	
	def initDraw(self):
		canvas = self.theGame.canvas
		posX, posY = self.posX, self.posY
		
		self.objId = canvas.create_line(posX, posY, posX+self.vX, posY+self.vY, fill='#b7ff30', width=8.0)
	
	def update(self):
		game = self.theGame
		if not game.isValidPos(self.posX, self.posY):
			game.removeObj(self)
			game.canvas.delete(self.objId)
			return
		
		canvas = self.theGame.canvas
		self.posX += self.vX
		self.posY += self.vY
		
		canvas.move(self.objId, self.vX, self.vY)

class ShootFX(GameObject):
	def __init__(self, game, player):
		super().__init__(game)
		
		self.posX = player.posX
		self.posY = player.posY
		
		self.CD = 1
	
	def initDraw(self):
		canvas = self.theGame.canvas
		posX, posY = self.posX, self.posY
		
		self.objIds = []
		for sz in range(20, 1110, 45):
			st, ed = 68, 0
			at = 45 - (1110-sz)//45
			now = int(st + (ed-st) * (at/45))
			# print('#', st, ed, at, now, _fRGB(now, now, now))
			
			nobj = canvas.create_oval(posX-sz, posY-sz, posX+sz, posY+sz, fill=_fRGB(now, now, now), outline='')
			canvas.tag_lower(nobj)
			self.objIds.append(nobj)
	
	def update(self):
		if not self.CD:
			self.theGame.removeObj(self)
			for Id in self.objIds:
				self.theGame.canvas.delete(Id)
		else:
			self.CD -= 1

#--------------------------------------------------------------------


class Game:
	# WIDTH, HEIGHT = 800, 600
	def __init__(self, root):
		root.grid_rowconfigure(0, weight=1)
		root.grid_columnconfigure(0, weight=1)
		self.root = root
		
		self.WIDTH, self.HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
		
		canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, background='#000000')
		self.canvas = canvas
		self.player = Player(self)
		self.objects = []
		
		self.initDraw()
		self.initControl()
		self.root.after(20, self.onUpdate)
	
	def initDraw(self):
		# self.canvas.pack()
		self.canvas.grid(sticky='NSEW')
		self.player.initDraw()
	
	def initControl(self):
		self.keyTyped = set()
		self.root.bind('<KeyPress>', self.onKeyPressed)
		self.root.bind('<KeyRelease>', self.onKeyReleased)
		self.root.bind('<Escape>', self.onExit)
	
	def onKeyPressed(self, event):
		key = event.char.lower()
		self.keyTyped.add(key)
		
	def onKeyReleased(self, event):
		key = event.char.lower()
		self.keyTyped.discard(key)
	
	def onUpdate(self):
		# objects update
		for obj in self.objects:
			obj.update()
		
		# player move
		player = self.player
		now = time.time()
		
		vx, vy = 0, 0
		for key in self.keyTyped:
			if key == 'w':
				vy -= 5
			elif key == 's':
				vy += 5
			
			if key == 'a':
				vx -= 5
			elif key == 'd':
				vx += 5
			
			if key == ' ':
				player.shoot(now)
		
		player.move(vx, vy)
		self.canvas.tag_raise(player.playerId)
		
		self.root.after(20, self.onUpdate)
	
	def addObj(self, obj):
		self.objects.append(obj)
		obj.initDraw()
	
	def removeObj(self, obj):
		self.objects.remove(obj)
	
	def isValidPos(self, posX, posY):
		return (posX >= 5 and posX < self.WIDTH-5) and (posY >= 5 and posY < self.HEIGHT-5)
	
	def onExit(self, event):
		self.root.destroy()
	
	def render():
		return

def main():
	root = tk.Tk()
	root.title(__file__)
	root.state('zoomed')
	
	game = Game(root)
	root.mainloop()

if __name__ == "__main__":
	main()