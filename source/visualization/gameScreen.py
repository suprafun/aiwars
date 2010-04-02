import os
from core.point import *
from tilemap import *
from spriteCollection import *
from levelProcessor import *


class GameScreen:
	def __init__(self, game, imageCache, screenDimension):
		self.game = game
		self.imageCache = imageCache
		self.screenDimension = screenDimension
		
		self.cameraMouseOffset = Point(0, 0)
		self.rightMouseButtonDown = False
		
		self.drawGrid = True
		
		self.camera = Point(0, 0)
		
		# Level visualization
		self.baseTilemap = Tilemap()
		self.gridTilemap = Tilemap()
		self.spriteCollection = SpriteCollection()
	#
	
	def onKeyDown(self, key):
		if key == ord('g'):
			self.drawGrid = not self.drawGrid
	#
	
	def onKeyUp(self, key):
		pass
	#
	
	def onMouseDown(self, button, position):
		if button == 3: # Right mouse button, TODO: Look for pygame constants for this?
			self.cameraMouseOffset.x = self.camera.x - position[0]
			self.cameraMouseOffset.y = self.camera.y - position[1]
			self.rightMouseButtonDown = True
	#
	
	def onMouseUp(self, button, position):
		if button == 3:
			self.rightMouseButtonDown = False
	#
	
	def onMouseMove(self, position):
		if self.rightMouseButtonDown:
			self.camera.x = position[0] + self.cameraMouseOffset.x
			self.camera.y = position[1] + self.cameraMouseOffset.y
			
			self.clampCameraToLevel()
	#
	
	def update(self):
		pass
	#
	
	def draw(self, screen):
		self.baseTilemap.draw(screen, self.camera)
		self.spriteCollection.draw(screen, self.camera)
		
		if self.drawGrid:
			self.gridTilemap.draw(screen, self.camera)
	#
	
	
	def clampCameraToLevel(self):
		margin = 5
		
		levelWidth = self.baseTilemap.width() * self.baseTilemap.getTileSize().x + margin
		levelHeight = self.baseTilemap.height() * self.baseTilemap.getTileSize().y + margin
		
		if levelWidth <= self.screenDimension[0]:
			self.camera.x = (self.screenDimension[0] - levelWidth) / 2
		else:
			self.camera.x = min(margin, max(self.screenDimension[0] - levelWidth, self.camera.x))
		
		if levelHeight <= self.screenDimension[1]:
			self.camera.y = (self.screenDimension[1] - levelHeight) / 2
		else:
			self.camera.y = min(margin, max(self.screenDimension[1] - levelHeight, self.camera.y))
	#
	
	def updateLevel(self):
		self.baseTilemap = Tilemap()
		self.gridTilemap = Tilemap()
		self.spriteCollection = SpriteCollection()
		
		createTilemapFromLevel(self.baseTilemap, \
		                       '../textures/terrain/tiles', \
		                       self.spriteCollection, \
		                       '../textures/terrain/sprites', \
		                       Point(32, 32), \
		                       self.imageCache, \
		                       self.game.level, \
		                       self.game.gameDatabase)
		
		self.gridTilemap.addImage(self.imageCache.getImage('../textures/terrain/grid_lines.png'))
		self.gridTilemap.setSize(Point(self.game.level.width(), self.game.level.height()), 0)
		
		self.clampCameraToLevel()
	#
#