from tilemap import *
from core.point import *


class GameScreen:
	def __init__(self, game, imageCache):
		self.game = game
		self.imageCache = imageCache
		
		# Level visualization
		self.baseTilemap = Tilemap()
		self.gridTilemap = Tilemap()
	#
	
	def onKeyDown(self, key):
		pass
	#
	
	def onKeyUp(self, key):
		pass
	#
	
	def onMouseDown(self, button, position):
		pass
	#
	
	def onMouseUp(self, button, position):
		pass
	#
	
	def onMouseMove(self, position):
		pass
	#
	
	def update(self):
		pass
	#
	
	def draw(self, screen):
		self.baseTilemap.draw(screen)
		self.gridTilemap.draw(screen)
	#
	
	
	def updateLevel(self):
		self.baseTilemap = Tilemap()
		self.gridTilemap = Tilemap()
		
		# TODO: Move terrain --> sprite mapping code to another class / function!!! Data-driven!
		spriteMapping = {'Road': 0, \
		                 'Plains': 0, \
		                 'Forest': 0, \
		                 'Mountain': 0, \
		                 'River': 1, \
		                 'Bridge': 1, \
		                 'Shoal': 2, \
		                 'Sea': 3, \
		                 'Reef': 3, \
		                 'City': 0, \
		                 'Base': 0, \
		                 'Headquarters': 0, \
		                 'Airport': 0, \
		                 'Dock': 0}
		
		self.baseTilemap.addImage(self.imageCache.getImage('../textures/terrain/tiles/t----0----.png'))
		self.baseTilemap.addImage(self.imageCache.getImage('../textures/terrain/tiles/t----0----.png'))
		self.baseTilemap.addImage(self.imageCache.getImage('../textures/terrain/tiles/t----0----.png'))
		self.baseTilemap.addImage(self.imageCache.getImage('../textures/terrain/tiles/t333333333.png'))
		
		self.gridTilemap.addImage(self.imageCache.getImage('../textures/terrain/grid_lines.png'))
		
		size = Point(self.game.level.width(), self.game.level.height())
		self.baseTilemap.setSize(size)
		self.gridTilemap.setSize(size, 0)
		
		for y in xrange(self.baseTilemap.height()):
			for x in xrange(self.baseTilemap.width()):
				self.baseTilemap.setTile(Point(x, y), spriteMapping[self.game.level.terrain[y][x].name])
		print 'Level is now', self.baseTilemap.width(), 'by', self.baseTilemap.height()
	#
#