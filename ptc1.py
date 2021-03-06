"""
A Simple Game.
Control: <Space> + WASD
Beat this game: make your self the top 0.0%
"""

## TODO: 
## 1. replace move() into coords()
## 2. features: level / better collision check

# Tkinter + Canvas practice

import math
import random
import tkinter as tk
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
			game.addObj(ChasingRect(game, self))
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
		
		posX, posY = self.posX, self.posY
		canvas.coords(self.objId, posX, posY, posX+self.vX, posY+self.vY)

class ChasingRect(GameObject):
	def __init__(self, game, player):
		self.thePlayer = player
		self.theGame = game
		
		radius = 300
		deg = random.uniform(0, 2*math.pi)
		relatX = radius * math.cos(deg)
		relatY = radius * math.sin(deg)
		
		self.posX = player.posX + relatX
		self.posY = player.posY + relatY
		
		self.speed = 7
	
	def initDraw(self):
		canvas = self.theGame.canvas
		posX, posY = self.posX, self.posY
		self.objId = canvas.create_rectangle(posX-8, posY-8, posX+8, posY+8, fill='#0026ff')
	
	def update(self):
		game = self.theGame
		canvas = game.canvas
		for obj in game.objects:
			if isinstance(obj, Bullet):
				vX = obj.posX - self.posX
				vY = obj.posY - self.posY
				dist = math.sqrt(vX*vX + vY*vY)
				
				if dist < 30:
					game.addScore(50)
					game.removeObj(self)
					canvas.delete(self.objId)
					return
		
		player = self.thePlayer
		
		vX = player.posX - self.posX
		vY = player.posY - self.posY
		unitSpeed = math.sqrt(vX*vX + vY*vY)
		
		if unitSpeed < 12:
			self.theGame.onChased()
			return
		
		modUnit = self.speed / unitSpeed
		vX *= modUnit
		vY *= modUnit
		
		self.posX += vX
		self.posY += vY
		canvas.move(self.objId, vX, vY)
		
		return True

#--------------------------------------------------------------------


class Game:
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
		
		self.score = 0
	
	def initDraw(self):
		self.canvas.grid(sticky='NSEW')
		self.player.initDraw()
	
	def initControl(self):
		self.keyTyped = set()
		self.root.bind('<KeyPress>', self.onKeyPressed)
		self.root.bind('<KeyRelease>', self.onKeyReleased)
		self.root.bind('<Escape>', self.onEscape)
	
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
	
	def onEscape(self, event):
		self.onExit()
	
	def onChased(self):
		print('Ooooooh')
		self.onExit()
	
	def onExit(self):
		self.root.destroy()
		score = self.score
		if self.score:
			lgscore = math.ceil(math.log2(self.score / 50))
			pcnt = (10/9) * (10**(-lgscore))
		else:
			pcnt = 100.0
		print('Your score: ', self.score)
		print('Only {:.12f}% can do this.'.format(pcnt))
		exit()
	
	def addScore(self, score):
		self.score += score
	
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