import copy
from unit import *
from serialization import *


# A unit update stores a copy of the unit and a reference to it.
# So if you create a UnitUpdate before modifying the unit,
# the update will allow you to compare between the previous and current state.
# For creating units, just pass None, and set newUnit manually.
# Likewise, for destroying units, pass None and set oldUnit manually.
class UnitUpdate(object):
	def __init__(self, game, unit):
		self.game = game
		
		self.oldUnit = copy.copy(unit) if unit != None else None
		self.newUnit = unit
	#
	
	def unitID(self):
		return self.oldUnit.id if self.oldUnit != None else self.newUnit.id
	#
	
	
	def toStream(self, hideInformation):
		stream = toStream(self.oldUnit.id if self.oldUnit != None else 0, self.newUnit.id if self.newUnit != None else 0)
		
		stream += self.__unitToStream(self.oldUnit, hideInformation)
		stream += self.__unitToStream(self.newUnit, hideInformation)
		
		return stream
	#
	
	def __unitToStream(self, unit, hideInformation):
		if unit == None:
			return ''
		else:
			return unit.toStream(hideInformation)
	#
	
	def fromStream(self, stream):
		oldUnitID, newUnitID, totalReadBytesCount = fromStream(stream, int, int)
		
		self.oldUnit, readBytesCount = self.__unitFromStream(stream[totalReadBytesCount:], oldUnitID)
		totalReadBytesCount += readBytesCount
		self.newUnit, readBytesCount = self.__unitFromStream(stream[totalReadBytesCount:], newUnitID)
		totalReadBytesCount += readBytesCount
		
		return totalReadBytesCount
	#
	
	def __unitFromStream(self, stream, unitID):
		if unitID == 0:
			return (None, 0)
		else:
			unit = Unit(self.game.gameDatabase, None, 0, Point(0, 0), None)
			readBytesCount = unit.fromStream(stream)
			return (unit, readBytesCount)
	#
#