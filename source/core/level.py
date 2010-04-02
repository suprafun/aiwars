from point import *
from building import *
from levelPlayerData import *


class Level(object):
	def __init__(self, gameDatabase):
		self.gameDatabase = gameDatabase
		self.reset()
	#
	
	def reset(self):
		self.name = 'Unnamed'
		self.playersData = []
		
		self.terrain = [[]]
		
		self.buildings = []
	#
	
	def loadFromFile(self, filename):
		self.reset()
		execfile(filename, {'level': self})
	#
	
	def setTileData(self, tileData):
		self.terrain = tileData
		
		# Post-process the map data: store references to terrain directly rather than indices
		for y in xrange(len(self.terrain)):
			for x in xrange(len(self.terrain[0])):
				terrainType = self.gameDatabase.getTerrainType(self.terrain[y][x])
				self.terrain[y][x] = terrainType
				
				if terrainType.buildingType != None:
					self.addBuilding(Building(terrainType.buildingType, Point(x, y)))
	#
	
	def addBuilding(self, building):
		self.buildings.append(building)
	#
	
	def addPlayer(self):
		playerData = LevelPlayerData()
		self.playersData.append(playerData)
		return playerData
	#
	
	def loadFromBuffer(self, buffer):
		self.reset()
		pass
	#
	
	def saveToBuffer(self, buffer):
		pass
	#
	
	
	def getPlayersCount(self):
		return len(self.playersData)
	#
	
	def getTerrainType(self, x, y):
		return self.terrain[y][x]
	#
	
	def getBuildingAt(self, x, y):
		for building in self.buildings:
			if building.position.x == x and building.position.y == y:
				return building
		return None
	#
#