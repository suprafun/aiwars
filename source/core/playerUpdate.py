import copy
from unit import *
from serialization import *
from unitUpdate import *
from buildingUpdate import *


# A player update stores the previous amount of money and the current amount of money,
# as well as any unit and building updates associated to this player. Be sure to set
# the new amount of money!
class PlayerUpdate(object):
	def __init__(self, game, player):
		self.game = game
		self.player = player
		
		self.reset()
	#
	
	def reset(self):
		self.oldMoneyAmount = self.player.money if self.player != None else 0
		self.newMoneyAmount = self.player.money if self.player != None else 0
		
		self.unitUpdates = []
		self.buildingUpdates = []
	#
	
	
	def toStream(self, hideInformation):
		stream = toStream(player.id, \
		                  self.oldMoneyAmount if not hideInformation else 0, \
		                  self.newMoneyAmount if not hideInformation else 0, \
		                  len(self.unitUpdates), \
		                  len(self.buildingUpdates))
		
		for unitUpdate in self.unitUpdates:
			stream += unitUpdate.toStream()
		
		for buildingUpdate in self.buildingUpdates:
			stream += buildingUpdate.toStream()
		
		return stream
	#
	
	def fromStream(self, stream):
		self.reset()
		
		(playerID,
		 self.oldMoneyAmount,
		 self.newMoneyAmount,
		 unitUpdateCount,
		 buildingUpdateCount,
		 totalReadBytesCount) = fromStream(stream, int, int, int, int, int)
		
		self.player = self.game.getPlayerByID(playerID)
		
		for i in xrange(unitUpdateCount):
			unitUpdate = UnitUpdate(self.game, None)
			readBytesCount = unitUpdate.fromStream(stream[totalReadBytesCount:])
			totalReadBytesCount += readBytesCount
			
			self.unitUpdates.append(unitUpdate)
		
		for i in xrange(buildingUpdateCount):
			buildingUpdate = BuildingUpdate(self.game, None)
			readBytesCount = buildingUpdate.fromStream(stream[totalReadBytesCount:])
			totalReadBytesCount += readBytesCount
			
			self.buildingUpdates.append(buildingUpdate)
		
		return totalReadBytesCount
	#
#