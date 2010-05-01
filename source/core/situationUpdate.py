from unit import *
from building import *
from serialization import *
from playerUpdate import *


# A situation update stores al unit and building updates for all involved players.
# It contains a dictionary that maps a player reference to a tuple that contains a list of (old unit, new unit) tuples
# and a list of (old building, new building) tuples.
class SituationUpdate(object):
	def __init__(self, game):
		self.game = game
		
		self.reset()
	#
	
	def reset(self):
		self.playerUpdates = {}
	#
	
	def addUnitCreationForPlayer(self, player, unit):
		if unit == None:
			return
		
		self.playerUpdates.setdefault(player, PlayerUpdate(self.game, player))
		
		existingUnitUpdate = self.getUnitUpdateForUnitID(unit.id)
		if existingUnitUpdate == None:
			unitUpdate = UnitUpdate(self.game, None)
			unitUpdate.newUnit = unit
			self.playerUpdates[player].unitUpdates.append(unitUpdate)
			return unitUpdate
		else:
			return existingUnitUpdate
	#
	
	def addUnitUpdateForPlayer(self, player, unit):
		if unit == None:
			return
		
		self.playerUpdates.setdefault(player, PlayerUpdate(self.game, player))
		
		existingUnitUpdate = self.getUnitUpdateForUnitID(unit.id)
		if existingUnitUpdate == None:
			unitUpdate = UnitUpdate(self.game, unit)
			self.playerUpdates[player].unitUpdates.append(unitUpdate)
			return unitUpdate
		else:
			return existingUnitUpdate
	#
	
	def addUnitRemovalForPlayer(self, player, unit):
		if unit == None:
			return
		
		self.playerUpdates.setdefault(player, PlayerUpdate(self.game, player))
		
		existingUnitUpdate = self.getUnitUpdateForUnitID(unit.id)
		if existingUnitUpdate == None:
			unitUpdate = UnitUpdate(self.game, unit)
			unitUpdate.newUnit = None
			self.playerUpdates[player].unitUpdates.append(unitUpdate)
			return unitUpdate
		else:
			return existingUnitUpdate
	#
	
	# TODO: Refactor this into the above unit design!!!
	def addBuildingCreationForPlayer(self, player, building):
		if building == None:
			return
		
		self.playerUpdates.setdefault(player, PlayerUpdate(self.game, player))
		
		existingBuildingUpdate = self.getBuildingUpdateForBuildingID(building.id)
		if existingBuildingUpdate == None:
			buildingUpdate = BuildingUpdate(self.game, None)
			buildingUpdate.newBuilding = building
			self.playerUpdates[player].buildingUpdates.append(buildingUpdate)
			return buildingUpdate
		else:
			return existingBuildingUpdate
	#
	
	def addBuildingUpdateForPlayer(self, player, building):
		if building == None:
			return
		
		self.playerUpdates.setdefault(player, PlayerUpdate(self.game, player))
		
		existingBuildingUpdate = self.getBuildingUpdateForUnitID(building.id)
		if existingBuildingUpdate == None:
			buildingUpdate = BuildingUpdate(self.game, building)
			self.playerUpdates[player].buildingUpdates.append(buildingUpdate)
			return buildingUpdate
		else:
			return existingBuildingUpdate
	#
	
	def addBuildingRemovalForPlayer(self, player, building):
		if building == None:
			return
		
		self.playerUpdates.setdefault(player, PlayerUpdate(self.game, player))
		
		existingBuildingUpdate = self.getBuildingUpdateForUnitID(building.id)
		if existingBuildingUpdate == None:
			buildingUpdate = BuildingUpdate(self.game, building)
			buildingUpdate.newBuilding = None
			self.playerUpdates[player].buildingUpdates.append(buildingUpdate)
			return buildingUpdate
		else:
			return existingBuildingUpdate
	#
	
	def updateMoneyAmountForPlayer(self, player, newMoneyAmount):
		self.playerUpdates.setdefault(player, PlayerUpdate(self.game, player))
		self.playerUpdates[player].newMoneyAmount = newMoneyAmount
	#
	
	def getUnitUpdateForUnitID(self, unitID):
		for playerUpdate in self.playerUpdates.itervalues():
			for unitUpdate in playerUpdate.unitUpdates:
				if unitUpdate.unitID() == unitID:
					return unitUpdate
		return None
	#
	
	def getBuildingUpdateForBuildingID(self, buildingID):
		for playerUpdate in self.playerUpdates.itervalues():
			for buildingUpdate in playerUpdate.buildingUpdates:
				if buildingUpdate.buildingID() == buildingID:
					return buildingUpdate
		return None
	#
	
	# Serialization format:
	# (int - player count)
	# for each player:
	#     (int - player ID)
	#     (int - old money amount)
	#     (int - new money amount)
	#     (int - unit update count)
	#     (int - building update count)
	#     for each unit update:
	#         (int - old unit ID, 0 if old unit is None)
	#         (int - new unit ID, 0 if new unit is None)
	#         (old unit serialization - only if old unit ID is not 0)
	#         (new unit serialization - only if new unit ID is not 0)
	#     for each building update:
	#         (int - old building ID, 0 if old building is None)
	#         (int - new building ID, 0 if new building is None)
	#         (old building serialization - only if old building ID is not 0)
	#         (new building serialization - only if new building ID is not 0)
	#
	# Note that during fog-of-war, player clients only receive updates that are visible to them.
	# Enemy money amounts and enemy transported units are hidden (a value of 0 and an empty list are sent, respectively) 
	def toStream(self, hideInformation):
		players = self.playerUpdates.keys()
		stream = toStream(len(players))
		
		for playerUpdate in self.playerUpdates.itervalues():
			stream += playerUpdate.toStream(hideInformation)
		
		return stream
	#
	
	def fromStream(self, stream):
		self.reset()
		
		(playerCount, totalReadBytesCount) = fromStream(stream, int)
		
		for i in xrange(playerCount):
			playerUpdate = PlayerUpdate(self.game, None)
			readBytesCount = playerUpdate.fromStream(stream[totalReadBytesCount:])
			totalReadBytesCount += readBytesCount
			
			self.playerUpdates[playerUpdate.player] = playerUpdate
		
		return totalReadBytesCount
	#
#