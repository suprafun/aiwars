from terrainType import *
from unitType import *
from buildingType import *


class GameDatabase(object):
	def __init__(self):
		self.reset()
	#
	
	def reset(self):
		self.name = ''
		
		self.terrainTypes = []
		self.unitTypes = []
		self.buildingTypes = []
	#
	
	# Loads the game database from a file. The file actually contains Python code that 'fills in' this object (the variable name 'database' refers to this GameDatabase instance).
	def loadFromFile(self, filename):
		self.reset()
		execfile(filename, {'database': self, 'TerrainType': TerrainType, 'UnitType': UnitType, 'BuildingType': BuildingType})
		
		# Give each type object a reference to this database, for lookup purposes (useful for reconstructing references, after being loaded from a stream)
		for terrainType in self.terrainTypes:
			terrainType.gameDatabase = self
		for unitType in self.unitTypes:
			unitType.gameDatabase = self
		for buildingType in self.buildingTypes:
			buildingType.gameDatabase = self
	#
	
	
	def getIndexOfTerrainType(self, terrainType):
		return self.terrainTypes.index(terrainType)
	#
	
	def getIndexOfUnitType(self, unitType):
		return self.unitTypes.index(unitType)
	#
	
	def getIndexOfBuildingType(self, buildingType):
		return self.buildingTypes.index(buildingType)
	#
	
	def getTerrainType(self, index):
		return self.terrainTypes[index]
	#
	
	def getUnitType(self, index):
		return self.unitTypes[index]
	#
	
	def getBuildingType(self, index):
		return self.buildingTypes[index]
	#
	
	
	# Serialization
	def toStream(self):
		terrainTypesStream = ''
		for terrainType in self.terrainTypes:
			terrainTypesStream += terrainType.toStream()
		
		unitTypesStream = ''
		for unitType in self.unitTypes:
			unitTypesStream += unitType.toStream()
		
		buildingTypesStream = ''
		for buildingType in self.buildingTypes:
			buildingTypesStream += buildingType.toStream()
		
		return toStream(self.name, \
		                len(self.terrainTypes), \
		                len(self.unitTypes), \
		                len(self.buildingTypes)) + terrainTypesStream + unitTypesStream + buildingTypesStream
	#
	
	def fromStream(self, stream):
		(self.name, \
		 terrainTypesCount, \
		 unitTypesCount, \
		 buildingTypesCount, \
		 readBytesCount) = fromStream(stream, str, int, int, int)
		
		self.terrainTypes = []
		for i in xrange(terrainTypesCount):
			terrainType = TerrainType('', 0, 0)
			terrainType.gameDatabase = self
			readBytesCount += terrainType.fromStream(stream[readBytesCount:])
			self.terrainTypes.append(terrainType)
		
		self.unitTypes = []
		for i in xrange(unitTypesCount):
			unitType = UnitType('', 0, 0, 0, 0)
			unitType.gameDatabase = self
			readBytesCount += unitType.fromStream(stream[readBytesCount:])
			self.unitTypes.append(unitType)
		
		self.buildingTypes = []
		for i in xrange(buildingTypesCount):
			buildingType = BuildingType('', 0)
			buildingType.gameDatabase = self
			readBytesCount += buildingType.fromStream(stream[readBytesCount:])
			self.buildingTypes.append(buildingType)
		
		for terrainType in self.terrainTypes:
			terrainType.fromStreamPostProcess()
		for unitType in self.unitTypes:
			unitType.fromStreamPostProcess()
		for buildingType in self.buildingTypes:
			buildingType.fromStreamPostProcess()
		
		return readBytesCount
	#
#