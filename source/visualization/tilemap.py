from core.point import *


class Tilemap:
	def __init__(self):
		self.position = Point(0, 0)
		self.tileSize = Point(32, 32)
		
		self.images = []
		self.tiles = []
		
		self.visible = True
	#
	
	def getTile(self, position):
		return self.tiles[position.y][position.x]
	#
	
	def setTile(self, position, index):
		self.tiles[position.y][position.x] = index
	#
	
	def addImage(self, image):
		self.images.append(image)
		return len(self.images) - 1
	#
	
	def setTileSize(self, tileSize):
		self.tileSize = tileSize
	#
	
	def getTileSize(self):
		return self.tileSize
	#
	
	def setSize(self, size, fillIndex = -1):
		while self.height() < size.y:
			self.tiles.append([])
		while self.height() > size.y:
			self.tiles.pop()
		
		for row in self.tiles:
			while len(row) < size.x:
				row.append(fillIndex)
			while len(row) > size.x:
				row.pop()
	#
	
	def width(self):
		if self.height() == 0:
			return 0
		else:
			return len(self.tiles[0])
	#
	
	def height(self):
		return len(self.tiles)
	#
	
	def draw(self, screen, offset):
		if not self.visible:
			return
		
		drawPos = self.position + offset
		for y in xrange(self.height()):
			for x in xrange(self.width()):
				if self.tiles[y][x] != -1:
					screen.blit(self.images[self.tiles[y][x]], (drawPos.x + x * self.tileSize.x, drawPos.y + y * self.tileSize.y))
	#
#