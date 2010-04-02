from serialization import *


class BuildingType(object):
	def __init__(self, name, income, maxCapturePoints = 20, availableUnitTypes = [], canRepairUnitTypes = [], repairAmount = 2, critical = False):
		self.gameDatabase = None
		
		self.name = name                              # This building type's name, for example 'City' or 'Base'.
		self.income = income                          # The income that this building type generates per turn.
		self.maxCapturePoints = maxCapturePoints      # Each turn, a capturing unit subtracts it's own hitpoints from the building's capture points.
		
		self.availableUnitTypes = availableUnitTypes  # The unit types that this building can create.
		self.canRepairUnitTypes = canRepairUnitTypes  # The unit types that this building can repair and resupply.
		self.repairAmount = repairAmount              # The number of hitpoints restored each turn.
		
		self.critical = critical                      # If a player looses all of it's critical buildings, he looses.
	#
	
	def canBuild(self, unitType):
		return self.availableUnitTypes.count(unitType) > 0
	#
	
	def canRepair(self, unitType):
		return self.canRepairUnitTypes.count(unitType) > 0
	#
	
	
	# Serialization
	def toStream(self):
		return toStream(self.name, \
		                self.income, \
		                self.maxCapturePoints, \
		                [self.gameDatabase.getIndexOfUnitType(unitType) for unitType in self.availableUnitTypes], \
		                [self.gameDatabase.getIndexOfUnitType(unitType) for unitType in self.canRepairUnitTypes], \
		                self.repairAmount, \
		                self.critical)
	#
	
	
		self.name = name                              # This building type's name, for example 'City' or 'Base'.
		self.income = income                          # The income that this building type generates per turn.
		self.maxCapturePoints = maxCapturePoints      # Each turn, a capturing unit subtracts it's own hitpoints from the building's capture points.
		
		self.availableUnitTypes = availableUnitTypes  # The unit types that this building can create.
		self.canRepairUnitTypes = canRepairUnitTypes  # The unit types that this building can repair and resupply.
		self.repairAmount = repairAmount              # The number of hitpoints restored each turn.
		
		self.critical = critical                      # If a player looses all of it's critical buildings, he looses.
	
	def fromStream(self, stream):
		(self.name, \
		 self.income, \
		 self.maxCapturePoints, \
		 self.availableUnitTypes, \
		 self.canRepairUnitTypes, \
		 self.repairAmount, \
		 self.critical, \
		 readBytesCount) = fromStream(stream, str, int, int, list, list, int, bool)
		
		return readBytesCount
	#
	
	def fromStreamPostProcess(self):
		self.availableUnitTypes = [self.gameDatabase.getUnitType(index) for index in self.availableUnitTypes]
		self.canRepairUnitTypes = [self.gameDatabase.getUnitType(index) for index in self.canRepairUnitTypes]
	#
#