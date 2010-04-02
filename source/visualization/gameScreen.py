import os
from core.point import *
from tilemap import *
from spriteCollection import *
from levelProcessor import *


class GameScreen:
	def __init__(self, game, imageCache):
		self.game = game
		self.imageCache = imageCache
		
		self.camera = Point(0, 0)
		
		# Level visualization
		self.baseTilemap = Tilemap()
		self.gridTilemap = Tilemap()
		self.spriteCollection = SpriteCollection()
	#
	
	def onKeyDown(self, key):
		pass
	#
	
	def onKeyUp(self, key):
		pass
	#
	
	def onMouseDown(self, button, position):
		#print 'down', button
		pass
	#
	
	def onMouseUp(self, button, position):
		#print 'up', button
		pass
	#
	
	def onMouseMove(self, position):
		#print 'move', position
		pass
	#
	
	def update(self):
		pass
	#
	
	def draw(self, screen):
		self.baseTilemap.draw(screen, self.camera)
		self.spriteCollection.draw(screen, self.camera)
		self.gridTilemap.draw(screen, self.camera)
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
	#
#

def matchPattern(pattern, images):
	matches = []
	for i in xrange(len(images)):
		for j in xrange(len(pattern)):
			if images[i][j] != None and images[i][j] != pattern[j]:
				break
		else:
			matches.append(i)
	if len(matches) == 0:
		return None
	
	bestMatch = matches[0]
	bestMatchCount = images[bestMatch].count(None)
	for match in matches[1:]:
		matchCount = images[match].count(None)
		if matchCount < bestMatchCount:
			bestMatch = match
			bestMatchCount = matchCount
	return bestMatch
#

def processLevel(level, images):
	# Create a border around the levels tilemap, to circumvent boundary checks
	tiles = level.terrain[:]
	for y in xrange(len(tiles)):
		tiles[y] = level.terrain[y][:]
		tiles[y].insert(0, tiles[y][0])
		tiles[y].append(tiles[y][-1])
	tiles.insert(0, tiles[0][:])
	tiles.append(tiles[-1][:])
	
	# Do actual pattern matching
	for y in xrange(level.height()):
		for x in xrange(level.width()):
			pattern = []
			for oy in xrange(3):
				for ox in xrange(3):
					pattern.append(tiles[y + oy][x + ox])
			# Do pattern matching!
			print prints[matchPattern(pattern, images)],
		print ''
#