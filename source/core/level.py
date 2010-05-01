import os
from guid import *
from point import *
from building import *
from levelPlayerData import *
from serialization import *
from levelLoaders import *


class Level(object):
	def __init__(self, game, gameDatabase):
		self.game = game
		self.gameDatabase = gameDatabase
		
		# Support for multiple level file formats
		self.mapLoaders = {'.py': loadFromPythonFile, \
		                   '.awm': loadFromAwmFile, \
		                   '.aws': loadFromAwsFile, \
		                   '.aw2': loadFromAw2File, \
		                   '.awd': loadFromAwdFile}
		
		self.reset()
	#
	
	def reset(self):
		self.name = 'Unnamed'
		self.author = 'Unknown'
		self.description = 'No description'
		self.supportedDatabases = []
		self.playersData = {}
		
		self.terrain = []
		self.buildings = []
	#
	
	def getBuildingsForPlayerNumber(self, playerNumber):
		return self.playersData.values()[playerNumber].buildings
	#
	
	def getUnitsForPlayerNumber(self, playerNumber):
		return self.playersData.values()[playerNumber].units
	#
	
	def loadFromFile(self, filename):
		extension = os.path.splitext(filename)[1]
		if self.mapLoaders.has_key(extension):
			self.reset()
			self.mapLoaders[extension](self, filename)
			
			print '\n==============================================================================='
			print 'Level:    ' + self.name
			print 'Author:   ' + self.author
			print '\nDescription:\n' + self.description
			print '==============================================================================='
		else:
			print 'File type [' + extension + '] not supported!'
	#
	
	def setTileData(self, tileData):
		self.terrain = tileData
		
		# Post-process the map data: store references to terrain directly rather than indices
		for y in xrange(len(self.terrain)):
			for x in xrange(len(self.terrain[0])):
				terrainType = self.gameDatabase.getTerrainType(self.terrain[y][x])
				self.terrain[y][x] = terrainType
				
				if terrainType.buildingType != None:
					self.addBuilding(Building(self.game, terrainType.buildingType, getGUID(), Point(x, y), None))
	#
	
	def addBuilding(self, building):
		self.buildings.append(building)
	#
	
	def getPlayerData(self, team):
		if not self.playersData.has_key(team):
			playerData = LevelPlayerData()
			self.playersData[team] = playerData
		return self.playersData[team]
	#
	
	def getPlayersCount(self):
		return len(self.playersData)
	#
	
	def getTerrainType(self, position):
		return self.terrain[position.y][position.x]
	#
	
	def getBuildingByID(self, buildingID):
		for building in self.buildings:
			if building.id == buildingID:
				return building
		return None
	#
	
	def getBuildingAtPosition(self, position):
		for building in self.buildings:
			if building.position.x == position.x and building.position.y == position.y:
				return building
		return None
	#
	
	def width(self):
		if self.height() == 0:
			return 0
		else:
			return len(self.terrain[0])
	#
	
	def height(self):
		return len(self.terrain)
	#
	
	
	# Serialization
	def toStream(self):
		tiles = []
		for row in self.terrain:
			for tile in row:
				tiles.append(self.gameDatabase.getIndexOfTerrainType(tile))
		
		buildingsStream = ''
		for building in self.buildings:
			buildingsStream += building.toStream(False)
		
		return toStream(self.name, \
		                self.author, \
		                self.description, \
		                self.width(), \
		                self.height(), \
		                tiles, \
		                len(self.buildings)) + buildingsStream
	#
	
	def fromStream(self, stream):
		(self.name, \
		 self.author, \
		 self.description, \
		 width, \
		 height, \
		 tiles, \
		 buildingsCount, \
		 readBytesCount) = fromStream(stream, str, str, str, int, int, list, int)
		
		self.buildings = []
		for i in xrange(buildingsCount):
			# TODO: Instead of having to create a Building instance with some default type, construct one directly from a stream?
			building = Building(self.game, self.gameDatabase.getBuildingType(0), 0, Point(0, 0), None)
			readBytesCount += building.fromStream(stream[readBytesCount:])
			self.buildings.append(building)
		
		self.terrain = []
		for row in xrange(height):
			self.terrain.append([self.gameDatabase.getTerrainType(tile) for tile in tiles[row * width:row * width + width]])
		
		return readBytesCount
	#
	
	# For debugging purposes, gives a string visualization of the map.
	def toString(self):
		strrep = ''
		for row in self.terrain:
			for terrainType in row:
				strrep += str(self.gameDatabase.getIndexOfTerrainType(terrainType)).ljust(3, ' ')
			strrep += '\n'
		return strrep
	#
#