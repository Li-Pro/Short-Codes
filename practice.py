import tkinter as tk

class Game:
	class Player:
		def __init__(self, game):
			self.posX = game.WIDTH/2
			self.posY = game.HEIGHT/2
			
			self.theGame = game
		
		def initDraw(self):
			canvas = self.theGame.canvas
			posX, posY = self.posX, self.posY
			self.playerId = canvas.create_rectangle(posX-5, posY-5, posX+5, posY+5, fill='#ffd900')
		
		def move(self, vx=0, vy=0):
			canvas = self.theGame.canvas
			canvas.move(self.playerId, vx, vy)
	
	WIDTH, HEIGHT = 800, 600
	def __init__(self, root):
		self.root = root
		
		canvas = tk.Canvas(root, width=Game.WIDTH, height=Game.HEIGHT, background='#000000')
		self.canvas = canvas
		self.player = Game.Player(self)
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
		
		self.player.move(vx, vy)
		
		self.root.after(20, self.onUpdate)
	
	def addObj(self):
		return
	
	def render():
		return

def main():
	root = tk.Tk()
	root.title(__file__)
	
	game = Game(root)
	root.mainloop()

if __name__ == "__main__":
	main()