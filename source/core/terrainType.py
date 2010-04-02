from serialization import *


class TerrainType(object):
	def __init__(self, name, cover, movementCost, hideUnits = False, buildingType = None):
		self.gameDatabase = None
		
		self.name = name                                # Terrain name, for example 'plains', or 'mountains'
		self.cover = cover                              # Cover value - every cover point reduces incoming damage by 10%
		self.movementCost = movementCost                # Most terrain will cost one point per tile, but difficult terrain can cost more, so units can travel less far.
		self.hideUnits = hideUnits                      # Some dense terrain types will hide units in fog-of-war mode.
		
		self.buildingType = buildingType                # Some terrain types are associated to buildings. For example: cities, bases, headquarters...
	#
	
	
	# Serialization
	def toStream(self):
		buildingTypeIndex = -1
		if self.buildingType != None:
			buildingTypeIndex = self.gameDatabase.getIndexOfBuildingType(self.buildingType)
		
		return toStream(self.name, \
		                self.cover, \
		                self.movementCost, \
		                self.hideUnits, \
		                buildingTypeIndex)
	#
	
	def fromStream(self, stream):
		(self.name, \
		self.cover, \
		self.movementCost, \
		self.hideUnits, \
		self.buildingType, \
		readBytesCount) = fromStream(stream, str, int, int, bool, int)
		
		if self.buildingType == -1:
			self.buildingType = None
		else:
			self.buildingType = self.gameDatabase.getBuildingType(self.buildingType)
		
		return readBytesCount
	#
#