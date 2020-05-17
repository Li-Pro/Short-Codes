import tkinter as tk
import math
import time

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
		
		self.objId = canvas.create_line(posX, posY, posX+self.vX, posY+self.vY, fill='#b7ff30')
		# self.fx3 = canvas.create_oval(posX-15, posY-15, posX+15, posY+15, fill='#050505', outline='')
		# # canvas.scale(self.fx3, posX, posY, self.vX+1, self.vY+1)
		# self.fx2 = canvas.create_oval(posX-12, posY-12, posX+12, posY+12, fill='#080808', outline='')
		# self.fx1 = canvas.create_oval(posX- 9, posY- 9, posX+ 9, posY+ 9, fill='#111111', outline='')
	
	def update(self):
		game = self.theGame
		if not game.isValidPos(self.posX, self.posY):
			game.removeObj(self)
			return
		
		canvas = self.theGame.canvas
		self.posX += self.vX
		self.posY += self.vY
		
		canvas.move(self.objId, self.vX, self.vY)
		# print('# Updating')

#--------------------------------------------------------------------


class Game:
	WIDTH, HEIGHT = 800, 600
	def __init__(self, root):
		self.root = root
		
		canvas = tk.Canvas(root, width=Game.WIDTH, height=Game.HEIGHT, background='#000000')
		self.canvas = canvas
		self.player = Player(self)
		self.objects = []
		
		self.initDraw()
		self.initControl()
		self.root.after(20, self.onUpdate)
	
	def initDraw(self):
		self.canvas.pack()
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
		return (posX >= 0 and posX < self.WIDTH) and (posY >= 0 and posY < self.HEIGHT)
	
	def onExit(self, event):
		self.root.destroy()
	
	def render():
		return

def main():
	root = tk.Tk()
	root.title(__file__)
	
	game = Game(root)
	root.mainloop()

if __name__ == "__main__":
	main()