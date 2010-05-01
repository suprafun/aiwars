import copy
from buildingType import *
from serialization import *


class Building(object):
	def __init__(self, game, type, id, position, player):
		self.game = game
		self.type = type
		self.id = id
		self.position = position
		
		self.player = player
		
		self.capturePoints = self.type.maxCapturePoints if self.type != None else 20
	#
	
	def canBuild(self, unitType):
		return self.type.canBuild(unitType)
	#
	
	def canRepair(self, unitType):
		return self.type.canRepair(unitType)
	#
	
	def repairAmount(self):
		return self.type.repairAmount
	#
	
	def isCritical(self):
		return self.type.critical
	#
	
	#Some units can capture buildings. This function returns true if the building has been fully captured.
	def capture(self, amount):
		self.capturePoints = int(max(0, self.capturePoints - amount))
		return self.capturePoints == 0
	#
	
	def restoreCapturePoints(self):
		self.capturePoints = self.type.maxCapturePoints
	#
	
	# Special method, called when making a shallow copy
	def __copy__(self):
		building = Building(self.game, self.type, self.id, copy.copy(self.position), self.player)
		
		building.capturePoints = self.capturePoints
		
		return building
	#
	
	
	# Serialization
	def toStream(self, hideInformation):
		playerID = 0
		if self.player != None:
			playerID = self.player.id
		
		return toStream(self.game.gameDatabase.getIndexOfBuildingType(self.type), \
		                self.id, \
		                self.position.x, \
		                self.position.y, \
		                playerID, \
		                self.capturePoints)
	#
	
	def fromStream(self, stream):
		(typeIndex, \
		 self.id, \
		 self.position.x, \
		 self.position.y, \
		 playerID, \
		 self.capturePoints, \
		 readBytesCount) = fromStream(stream, int, int, int, int, int, int)
		
		self.type = self.game.gameDatabase.getBuildingType(typeIndex)
		self.player = self.game.getPlayerByID(playerID)
		
		return readBytesCount
	#
#