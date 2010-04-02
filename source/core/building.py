from buildingType import *
from serialization import *


class Building(object):
	def __init__(self, game, gameDatabase, type, id, position, player):
		self.game = game
		self.gameDatabase = gameDatabase
		self.type = type
		self.id = id
		self.position = position
		
		self.player = player
		
		self.capturePoints = self.type.maxCapturePoints
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
		self.capturePoints = max(0, self.capturePoints - amount)
		return self.capturePoints == 0
	#
	
	def restoreCapturePoints(self):
		self.capturePoints = self.type.maxCapturePoints
	#
	
	
	# Serialization
	def toStream(self):
		playerID = -1
		if self.player != None:
			playerID = self.player.id
		
		return toStream(self.gameDatabase.getIndexOfBuildingType(self.type), \
		                self.id, \
		                self.position.x, \
		                self.position.y, \
		                playerID, \
		                self.capturePoints)
	#
	
	def fromStream(self, stream):
		(self.type, \
		 self.id, \
		 self.position.x, \
		 self.position.y, \
		 self.player, \
		 self.capturePoints, \
		 readBytesCount) = fromStream(stream, int, int, int, int, int, int)
		
		self.type = self.gameDatabase.getBuildingType(self.type)
		self.player = self.game.getPlayerByID(self.player)
		
		return readBytesCount
	#
#