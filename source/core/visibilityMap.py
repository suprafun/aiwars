import copy


class VisibilityMap(object):
	def __init__(self, gameData, level):
		self.gameData = gameData
		self.level = level
		
		self.__visibleTiles = [[0] * level.width()] * level.height()
		self.__stealthDetectedTiles = [[0] * level.width()] * level.height()
		
		self.width = level.width()
		self.height = level.height()
	#
	
	# Check vision
	def tileIsVisible(self, x, y):
		return self.__visibleTiles[y][x] > 0
	#
	
	def tileIsStealthDetected(self, x, y):
		return self.__stealthDetectedTiles[y][x] > 0
	#
	
	def unitIsVisible(self, unit):
		if self.gameData.fogOfWar:
			if unit.isHiding() or unit.isHiddenByTerrain():
				return self.tileIsStealthDetected(unit.position.x, unit.position.y)
			else:
				return self.tileIsVisible(unit.position.x, unit.position.y)
		else:
			if unit.isHiding():
				return self.tileIsStealthDetected(unit.position.x, unit.position.y)
			else:
				return True
	#
	
	def buildingIsVisible(self, building):
		if self.gameData.fogOfWar:
			return self.tileIsVisible(building.position.x, building.position.y)
		else:
			return True
	#
	
	
	# Update vision
	def addVision(self, position, visionRange, stealthDetectionRange):
		self.__updateVision(position, visionRange, stealthDetectionRange, 1)
	#
	
	def removeVision(self, position, visionRange, stealthDetectionRange):
		self.__updateVision(position, visionRange, stealthDetectionRange, -1)
	#
	
	def __updateVision(self, position, visionRange, stealthDetectionRange, modifier):
		self.__updateMap(self.__visibleTiles, position, visionRange, modifier)
		self.__updateMap(self.__stealthDetectedTiles, position, stealthDetectionRange, modifier)
	#
	
	def __updateMap(self, visibilityMap, position, range, modifier):
		for y in xrange(max(0, position.y - range), min(self.height, position.y + range + 1)):
			width = range - abs(y - position.y)
			for x in xrange(max(0, position.x - width), min(self.width, position.x + width + 1)):
				visibilityMap[y][x] += modifier
	#
	
	
	# Special method, called when making a copy
	def __copy__(self):
		visibilityMap = VisibilityMap(self.gameData, self.level)
		
		# Duplicate the tile data
		for y in xrange(self.height):
			for x in xrange(self.width):
				visibilityMap.__visibleTiles[y][x] = self.__visibleTiles[y][x]
				visibilityMap.__stealthDetectedTiles[y][x] = self.__stealthDetectedTiles[y][x]
		
		return visibilityMap
	#
#