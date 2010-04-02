from buildingType import *
from guid import *


class Building:
	def __init__(self, type, position):
		self.type = type
		self.id = guid.getGUID()
		self.position = position
		
		self.capturePoints = self.type.maxCapturePoints
	#
	
	def canBuild(self, unitType):
		return self.type.canBuild(unitType)
	#
	
	'''Some units can capture buildings. This function returns true if the building has been fully captured.'''
	def capture(self, amount):
		self.capturePoints = max(0, self.capturePoints - amount)
		return self.capturePoints == 0
	#
	
	def restoreCapturePoints(self):
		self.capturePoints = self.type.maxCapturePoints
	#
#