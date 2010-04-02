import os
import pygame
from core.point import *
from tilemap import *
from spriteCollection import *
from levelProcessor import *
from textBox import *


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
		
		self.camera = Point(0, 0)
		
		# Level visualization
		self.tileSize = Point(32, 32)
		self.baseTilemap = Tilemap()
		self.gridTilemap = Tilemap()
		self.spriteCollection = SpriteCollection()
		
		self.tooltip = TextBox(Point(0, 0), Point(0, 0), '', fontsize = 14, color = (255, 255, 225))
		self.tooltip.visible = False
		#self.tooltip.label.antiAliasing = False
	#
	
	def onKeyDown(self, key):
		if key == ord('g'):
			self.gridTilemap.visible = not self.gridTilemap.visible
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
		
		self.updateToolTip()
	#
	
	def draw(self, screen):
		self.baseTilemap.draw(screen, self.camera)
		self.spriteCollection.draw(screen, self.camera)
		self.gridTilemap.draw(screen, self.camera)
		self.tooltip.draw(screen, Point(0, 0))
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
		
		self.baseTilemap.setSize(Point(self.game.level.width(), self.game.level.height()))
		self.clampCameraToLevel()
		
		createTilemapFromLevel(self.baseTilemap, \
		                       '../textures/terrain/tiles', \
		                       self.spriteCollection, \
		                       '../textures/terrain/sprites', \
		                       self.tileSize, \
		                       self.imageCache, \
		                       self.game.level, \
		                       self.game.gameDatabase)
		
		self.gridTilemap.addImage(self.imageCache.getImage('../textures/terrain/grid_lines.png'))
		self.gridTilemap.addImage(self.imageCache.getImage('../textures/terrain/fog_of_war.png'))
		self.gridTilemap.setSize(Point(self.game.level.width(), self.game.level.height()), 0)
	#
	
	def updateToolTip(self):
		mousePosition = Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
		tileCoordinates = self.getTileAtScreenPosition(mousePosition)
		if tileCoordinates.x >= 0 and tileCoordinates.y >= 0 and tileCoordinates.x < self.game.level.width() and tileCoordinates.y < self.game.level.height():
			terrainType = self.game.level.getTerrainType(tileCoordinates)
			self.tooltip.label.text = terrainType.name + ' - ' + str(terrainType.cover * 10) + ' % cover'
			#self.tooltip.label.text = terrainType.name + ' - ' + ''.ljust(terrainType.cover, '*')
			self.tooltip.label.refresh()
			self.tooltip.resizeToLabel()
			self.tooltip.position = mousePosition - Point(0, self.tooltip.height() + 5)
			self.tooltip.visible = True
		else:
			self.tooltip.visible = False
	#
	
	def getTileAtScreenPosition(self, screenPosition):
		worldPosition = screenPosition - self.camera
		return Point(worldPosition.x / self.tileSize.x, worldPosition.y / self.tileSize.y)
	#
#