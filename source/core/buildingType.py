from serialization import *


class BuildingType(object):
	def __init__(self, name, income, availableUnitTypes = [], maxCapturePoints = 20):
		self.gameDatabase = None
		
		self.name = name
		self.income = income
		self.availableUnitTypes = availableUnitTypes
		self.maxCapturePoints = maxCapturePoints
	#
	
	def canBuild(self, unitType):
		return self.availableUnitTypes.count(unitType) > 0
	#
	
	
	# Serialization
	def toStream(self):
		return toStream(self.name, \
		                self.income, \
		                [self.gameDatabase.getIndexOfUnitType(unitType) for unitType in self.availableUnitTypes], \
		                self.maxCapturePoints)
	#
	
	def fromStream(self, stream):
		(self.name, \
		 self.income, \
		 self.availableUnitTypes, \
		 self.maxCapturePoints, \
		 readBytesCount) = fromStream(stream, str, int, list, int)
		
		return readBytesCount
	#
	
	def fromStreamPostProcess(self):
		self.availableUnitTypes = [self.gameDatabase.getUnitType(index) for index in self.availableUnitTypes]
	#
#