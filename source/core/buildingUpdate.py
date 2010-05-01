import copy
from building import *
from point import *
from serialization import *


# A building update stores a copy of the building and a reference to it.
# So if you create a BuildingUpdate before modifying the building,
# the update will allow you to compare between the previous and current state.
# For newly captured building, just pass None, and set newBuilding manually.
# Likewise, for lost buildings, pass None and set oldBuilding manually.
class BuildingUpdate(object):
	def __init__(self, game, building):
		self.game = game
		
		self.oldBuilding = copy.copy(building) if building != None else None
		self.newBuilding = building
	#
	
	def buildingID(self):
		return self.oldBuilding.id if self.oldBuilding != None else self.newBuilding.id
	#
	
	
	def toStream(self, hideInformation):
		stream = toStream(self.oldBuilding.id if self.oldBuilding != None else 0, self.newBuilding.id if self.newBuilding != None else 0)
		
		stream += self.__buildingToStream(self.oldBuilding, hideInformation)
		stream += self.__buildingToStream(self.newBuilding, hideInformation)
		
		return stream
	#
	
	def __buildingToStream(self, building, hideInformation):
		if building == None:
			return ''
		else:
			return building.toStream(hideInformation)
	#
	
	def fromStream(self, stream):
		oldBuildingID, newBuildingID, totalReadBytesCount = fromStream(stream, int, int)
		
		self.oldBuilding, readBytesCount = self.__buildingFromStream(stream[totalReadBytesCount:], oldBuildingID)
		totalReadBytesCount += readBytesCount
		self.newBuilding, readBytesCount = self.__buildingFromStream(stream[totalReadBytesCount:], newBuildingID)
		totalReadBytesCount += readBytesCount
		
		return totalReadBytesCount
	#
	
	def __buildingFromStream(self, stream, buildingID):
		if buildingID == 0:
			return (None, 0)
		else:
			building = Building(self.game, None, 0, Point(0, 0), None)
			readBytesCount = building.fromStream(stream)
			return (building, readBytesCount)
	#
#