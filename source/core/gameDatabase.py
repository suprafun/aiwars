from terrainType import *
from unitType import *
from buildingType import *


class GameDatabase:
	def __init__(self):
		self.reset()
	#
	
	def reset(self):
		self.terrainTypes = []
		self.unitTypes = []
		self.buildingTypes = []
	#
	
	# Loads the game database from a file. The file actually contains Python code that 'fills in' this object (the variable name 'database' refers to this GameDatabase instance).
	def loadFromFile(self, filename):
		self.reset()
		execfile(filename, {'database': self, 'TerrainType': TerrainType, 'UnitType': UnitType, 'BuildingType': BuildingType})
	#
	
	def loadFromBuffer(self, buffer):
		self.reset()
		pass
	#
	
	def saveToBuffer(self, buffer):
		pass
	#
#