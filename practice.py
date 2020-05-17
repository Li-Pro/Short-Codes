import tkinter as tk
import math

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
		
		self.lastVX = vx
		self.lastVY = vy
		
		self.posX += vx
		self.posY += vy
		
		canvas = self.theGame.canvas
		canvas.move(self.playerId, vx, vy)

class Bullet(GameObject):
	speedMod = 5
	def __init__(self, game, player):
		super().__init__(game)
		
		self.posX = player.posX
		self.posY = player.posY
		
		self.vX = player.lastVX * self.speedMod
		self.vY = player.lastVY * self.speedMod
	
	def initDraw(self):
		canvas = self.theGame.canvas
		posX, posY = self.posX, self.posY
		vX, vY = self.vX, self.vY
		
		boundV = (vX/5, vY/5)
		boundPV = (-boundV[1]/3, boundV[0]/3)
		
		bound1 = (posX - boundPV[0]/2, posY - boundPV[1]/2)
		bound2 = (posX + boundV[0] + boundPV[0]/2, posY + boundV[1] + boundPV[1]/2)
		
		self.objId = canvas.create_oval(bound1[0], bound1[1], bound2[0], bound2[1], fill='#b7ff30')
	
	def update(self):
		canvas = self.theGame.canvas
		canvas.move(self.objId, self.vX, self.vY)

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
	
	def onKeyPressed(self, event):
		# print('#', dir(event), ord(event.char))
		key = event.char.lower()
		self.keyTyped.add(key)
		
	def onKeyReleased(self, event):
		key = event.char.lower()
		self.keyTyped.discard(key)
	
	def onUpdate(self):
		# player move
		player = self.player
		
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
				self.addObj(Bullet(self, player))
		
		self.player.move(vx, vy)
		
		# objects update
		for obj in self.objects:
			obj.update()
		
		self.root.after(20, self.onUpdate)
	
	def addObj(self, obj):
		self.objects.append(obj)
		obj.initDraw()
	
	def render():
		return

def main():
	root = tk.Tk()
	root.title(__file__)
	
	game = Game(root)
	root.mainloop()

if __name__ == "__main__":
	main()