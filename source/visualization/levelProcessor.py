import os
import random
from core.point import *
from spriteRuleset import *


# First, tiles are mapped to so-called base tiles - transitions from sea to plains and from sea to forests are the same, anyway
# Note that terrain names, as specified in the game database, are used to determine the base type. So this table is quite database-specific.
__baseTiles = {'Road': 0, \
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
               'Dock': 3}
# NOTE: Bridge type needs special handling?!?

__cornerPositions = {'tl': Point(0, 0), \
                     'tr': Point(1, 0), \
                     'br': Point(1, 1), \
                     'bl': Point(0, 1)}

def createTilemapFromLevel(tilemap, tilefolder, spriteCollection, spritefolder, tileSize, imageCache, level, gameDatabase):
	# Scan the tile folder for tile images, load the images and associate them with a tile pattern (which is parsed from their filenames)
	if not tilefolder.endswith('/') and not tilefolder.endswith('\\'):
		tilefolder += '/'
	tiles = {}
	filenames = os.listdir(tilefolder)
	for filename in filenames:
		if filename.endswith('.png'):
			image = imageCache.getImage(tilefolder + filename)
			imageIndex = tilemap.addImage(image)
			
			(corner, tile) = __getTileFromFilename(filename, imageIndex)
			if not tiles.has_key(corner):
				tiles[corner] = []
			tiles[corner].append(tile)
	
	# Copy the terrain data - tiles is our local copy of terrain type indices. baseTileData contains the tile data, converted to base types
	tileData = []
	baseTileData = []
	for row in level.terrain:
		tileData.append([gameDatabase.getIndexOfTerrainType(terrainType) for terrainType in row])
		baseTileData.append([__baseTiles[terrainType.name] for terrainType in row])
	
	# Add a border around the tile data, so we can skip boundary checks
	for y in xrange(len(tileData)):
		tileData[y] = [tileData[y][0]] + tileData[y] + [tileData[y][-1]]
	tileData = [tileData[0][:]] + tileData + [tileData[-1][:]]
	# And a border around our base tile data
	for y in xrange(len(baseTileData)):
		baseTileData[y] = [baseTileData[y][0]] + baseTileData[y] + [baseTileData[y][-1]]
	baseTileData = [baseTileData[0][:]] + baseTileData + [baseTileData[-1][:]]
	
	# Size the tilemap - it holds 4 times as much tiles as the level, because tiles are split up into 4 corner tiles. This makes composing
	# maps with various tile transitions easier.
	tilemap.setSize(Point(level.width() * 2, level.height() * 2), -1)
	tilemap.setTileSize(tileSize / 2)
	
	# Do the actual pattern matching, based on these base terrain types
	for y in xrange(level.height()):
		for x in xrange(level.width()):
			pattern = []
			#print x, y
			for (ox, oy) in [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)]:
				#print '  ', x + ox, y + oy
				#print '    ', baseTileData[y + oy][x + ox]
				pattern.append(baseTileData[y + oy][x + ox])
			for corner in ['tl', 'tr', 'br', 'bl']:
				bestRank = 0
				bestTile = None
				for tile in tiles[corner]:
					if tile.type == baseTileData[y + 1][x + 1]:
						rank = tile.matchRank(pattern)
						if rank > bestRank:
							bestRank = rank
							bestTile = tile
				if bestTile != None:
					tilemap.setTile(Point(x * 2, y * 2) + __cornerPositions[corner], bestTile.imageIndex)
	
	__decorateTiles(spriteCollection, spritefolder, tileSize, imageCache, level)
#

def __decorateTiles(spriteCollection, spritefolder, tileSize, imageCache, level):
	if not spritefolder.endswith('/') and not spritefolder.endswith('\\'):
		spritefolder += '/'
	
	# Can't do anything without a sprite rules file
	if not os.path.exists(spritefolder + 'spriterules.py'):
		return
	
	ruleset = SpriteRuleset()
	ruleset.loadFromFile(spritefolder + 'spriterules.py')
	
	# Always seed with the same number - so the same map will always look the same!
	# TODO: Number can be generated by hashing some level data!
	random.seed(65)
	for y in xrange(level.height()):
		for x in xrange(level.width()):
			terrainTypeName = level.getTerrainType(Point(x, y)).name
			if ruleset.rules.has_key(terrainTypeName):
				# Place some sprites semi-randomly, sort on depth (bottom)
				sprites = []
				for i in xrange(random.randint(3, 6)):
					spriteRule = random.choice(ruleset.rules[terrainTypeName])
					spriteX = x * tileSize.x + random.randint(0, tileSize.x - spriteRule.boundingBox[2])
					spriteY = y * tileSize.y + random.randint(0, tileSize.y - spriteRule.boundingBox[3])
					# TODO: Perform some collision checking here??
					sprites.append((Point(spriteX, spriteY), imageCache.getImage(spritefolder + spriteRule.imageFilename)))
				
				sprites.sort(lambda a, b: (a[0].y + a[1].get_height()) - (b[0].y + b[1].get_height()))
				for sprite in sprites:
					spriteCollection.addSprite(sprite[0], sprite[1])
#


# Returns a (corner, __Tile) tuple, which allows the calling code to store the __Tile in a corner-specific list
def __getTileFromFilename(filename, imageIndex):
	(type, corner, a, b, c) = filename.replace('.png', '').split()
	type = int(type)
	return (corner, __Tile(type, corner, [a, b, c], imageIndex))
#

# Which corner needs to check which neighbors for matches, and in what order (indices into the surroundingTiles list):
# [0, 1, 2]
# [3,    4]
# [5, 6, 7]
cornerNeighbors = {'tl': (3, 0, 1), \
                   'tr': (1, 2, 4), \
                   'br': (4, 7, 6), \
                   'bl': (6, 5, 3)}
#

class __Tile(object):
	def __init__(self, type, corner, patterns, imageIndex):
		self.type = type
		self.neighbors = cornerNeighbors[corner]
		self.imageIndex = imageIndex
		
		self.patterns = []
		for pattern in patterns:
			if pattern == 'x':
				self.patterns.append([])
			else:
				self.patterns.append([int(token) for token in pattern.split(',')])
	#
	
	# Surrounding tiles are given as a single list: [top left, top, top right, left, right, bottom left, bottom, bottom right]
	# Returns the match rank - more precise matches score higher, so pick the best match you can find.
	# This should always give you at least some tiles to work with, even if they don't match perfectly.
	def matchRank(self, surroundingTiles):
		rank = 0
		for i in xrange(len(self.patterns)):
			if len(self.patterns[i]) == 0:
				# A wildcard match scores 1 point
				rank += 1
			elif surroundingTiles[self.neighbors[i]] in self.patterns[i]:
				# An exact match scores 2 points
				rank += 2
		return rank
	#
#