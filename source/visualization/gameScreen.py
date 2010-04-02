import os
import pygame
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
		self.cameraDragging = False
		self.arrowKeyState = {pygame.constants.K_UP: False, \
		                      pygame.constants.K_DOWN: False, \
		                      pygame.constants.K_LEFT: False, \
		                      pygame.constants.K_RIGHT: False}
		self.arrowKeyMovement = {pygame.constants.K_UP: Point(0, 1), \
		                        pygame.constants.K_DOWN: Point(0, -1), \
		                        pygame.constants.K_LEFT: Point(1, 0), \
		                        pygame.constants.K_RIGHT: Point(-1, 0)}
		self.arrowKeyMovementSpeed = 32
		
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
		elif self.arrowKeyState.has_key(key):
			self.arrowKeyState[key] = True
	#
	
	def onKeyUp(self, key):
		if self.arrowKeyState.has_key(key):
			self.arrowKeyState[key] = False
	#
	
	def onMouseDown(self, button, position):
		if button == 3: # Right mouse button, TODO: Look for pygame constants for this?
			self.cameraMouseOffset.x = self.camera.x - position[0]
			self.cameraMouseOffset.y = self.camera.y - position[1]
			self.cameraDragging = True
	#
	
	def onMouseUp(self, button, position):
		if button == 3:
			self.cameraDragging = False
	#
	
	def onMouseMove(self, position):
		if self.cameraDragging:
			self.camera.x = position[0] + self.cameraMouseOffset.x
			self.camera.y = position[1] + self.cameraMouseOffset.y
			
			self.clampCameraToLevel()
	#
	
	def update(self):
		if not self.cameraDragging:
			for key in self.arrowKeyState.keys():
				if self.arrowKeyState[key]:
					self.camera += self.arrowKeyMovement[key] * self.arrowKeyMovementSpeed
			self.clampCameraToLevel()
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