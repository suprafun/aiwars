from guid import *
from unit import *
from building import *
from pathfinding import *
from situationUpdate import *
from visibilityMap import *


ACTION_RESULT_SUCCESS = chr(0)
ACTION_RESULT_INVALID = chr(1)
ACTION_RESULT_TRAPPED = chr(2)


class Player(object):
	def __init__(self, game, name, id):
		self.game = game
		self.name = name
		self.id = id
		
		self.money = 0
		self.buildings = []
		self.units = []
		
		# Keep track of what actions units can still perform - at the start of each turn, all units are placed in the __activeUnits list.
		# Units that have moved are moved to the __movedUnits list.
		# Units that were trapped during movement, or that have taken an action (firing, unloading, loading, supplying, etc.) are placed in the __finishedUnits list.
		self.__activeUnits = []
		self.__movedUnits = []
		self.__finishedUnits = []
		
		# Visibility maps, shows how many units can see a certain tile. It is updated every time a unit is created, moved, loaded, unloaded, or destroyed,
		# and every time a building is captured or lost.
		self.__visibilityMap = VisibilityMap(self.game.gameData, self.game.level)
		
		
		# Listeners should implement the following methods:
		# onPlayerStartsTurn(player)
		# onPlayerEndsTurn(player)
		# NOTE: The following one is deprecated!!!
		# onPlayerSituationUpdate(player, situationUpdate)
		self.__listeners = []
	#
	
	def addListener(self, listener):
		if not listener in self.__listeners:
			self.__listeners.append(listener)
	#
	
	def removeListener(self, listener):
		if listener in self.__listeners:
			self.listeners.remove(listener)
	#
	
	def addBuilding(self, building):
		if not building in self.buildings:
			self.buildings.append(building)
			building.player = self
			
			self.__visibilityMap.addVision(building.position, 0, 0)
	#
	
	def getBuildingByID(self, buildingID):
		for building in self.buildings:
			if building.id == buildingID:
				return building
		return None
	#
	
	def getBuildingAtPosition(self, position):
		for building in self.buildings:
			if building.position == position:
				return building
		return None
	#
	
	def hasBuilding(self, building):
		return building in self.buildings
	#
	
	def removeBuilding(self, building):
		if building in self.buildings:
			buildings.remove(building)
			building.player = None
			self.__visibilityMap.removeVision(building.position, 0, 0)
			
			# If the building was critical, check if there's still any other critical buildings left!
			if building.isCritical():
				for building in self.buildings:
					if building.isCritical():
						break
				else:
					self.game.playerHasLost(self)
	#
	
	def addUnit(self, unit):
		if not unit in self.units:
			self.units.append(unit)
			unit.player = self
		
			self.unitIsFinished(unit)
			self.__visibilityMap.addVision(unit.position, unit.currentVision(), unit.currentStealthDetectionRange())
	#
	
	def getUnitByID(self, unitID):
		for unit in self.units:
			if unit.id == unitID:
				return unit
		return None
	#
	
	def getUnitAtPosition(self, position):
		for unit in self.units:
			if unit.position == position and not unit.isLoaded():
				return unit
		return None
	#
	
	def hasUnit(self, unit):
		return unit in self.units
	#
	
	def removeUnit(self, unit):
		if unit in self.units:
			self.units.remove(unit)
			unit.player = None
			
			if unit in self.__activeUnits:
				self.__activeUnits.remove(unit)
			if unit in self.__movedUnits:
				self.__movedUnits.remove(unit)
			if unit in self.__finishedUnits:
				self.__finishedUnits.remove(unit)
			
			if not unit.isLoaded():
				self.__visibilityMap.removeVision(unit.position, unit.currentVision(), unit.currentStealthDetectionRange())
			
			for loadedUnit in unit.loadedUnits:
				self.removeUnit(loadedUnit)
	#
	
	# NOTE: Not used? Current approach is to let each command function return a situation update, which is then handled by the caller.
	# No more listener-informing when it comes to situation updates!
	'''
	# Informs this player about the movement of another players units.
	def situationUpdate(self, situationUpdate):
		for listener in self.__listeners:
			listener.onPlayerSituationUpdate(situationUpdate)
	#
	'''
	
	def startTurn(self):
		situationUpdate = SituationUpdate(self.game)
		
		# Add income
		for building in self.buildings:
			self.money += building.type.income
		
		# First, units that consume fuel per turn will do so.
		for unit in filter(lambda unit: unit.fuelConsumptionForTurn() > 0, self.units):
			unitUpdate = situationUpdate.addUnitUpdateForPlayer(self, unit)
			unit.consumeFuelForTurn()
			if unit.needsFuelToStayAlive() and unit.fuel <= 0:
				self.__addLoadedUnitRemovalsToSituationUpdate(unit, situationUpdate)
				self.removeUnit(unit)
				unitUpdate.newUnit = None
		
		# Check all units that can be resupplied or repaired:
		# - units standing on friendly buildings
		# - units standing next to supplying units
		# - units that are carried by a supplying unit
		# Units standing on friendly buildings that can repair them will be repaired up to 2 hitpoints (less if not enough funds is available).
		# Units are checked in the order that they're built.
		supplyingUnits = filter(Unit.canSupply, self.units)
		for unit in filter(lambda unit: unit.needsResupply() or unit.needsRepair, self.units):
			building = self.getBuildingAtPosition(unit.position)
			
			resupply = False
			if unit.needsResupply():
				if unit.isLoaded() and unit.carriedBy.canSupply():
					resupply = True
				elif building != None:
					resupply = True
				else:
					for supplyingUnit in supplyingUnits:
						if manhattanDistance(supplyingUnit.position, unit.position) == 1:
							resupply = True
							break
			
			repair = False
			if unit.needsRepair():
				if building != None and building.canRepair(unit.type):
					repair = True
			
			if resupply or repair:
				situationUpdate.addUnitUpdateForPlayer(self, unit)
				
				if resupply:
					unit.supply()
				
				if repair:
					actualRepairAmount = unit.actualRepairAmount(building.repairAmount())
					repairCost = unit.repairCost(1)
					unitRepaired = False
					while actualRepairAmount > 0:
						if repairCost <= self.money:
							self.money -= repairCost
							unit.repair(1)
							actualRepairAmount -= 1
							unitRepaired = True
						else:
							break
		
		self.__activeUnits = self.units[:]
		self.__movedUnits = []
		self.__finishedUnits = []
		
		for listener in self.__listeners:
			listener.onPlayerStartsTurn(self)
		
		situationUpdate.updateMoneyAmountForPlayer(self, self.money)
		return (ACTION_RESULT_SUCCESS, situationUpdate)
	#
	
	# Returns a (result, situationUpdate) tuple - the situation update is None if the result is invalid.
	def moveUnit(self, unitID, route):
		unit = self.getUnitByID(unitID)
		if unit == None or not self.unitCanMove(unit):
			return (ACTION_RESULT_INVALID, None)
		
		# If this unit doesn't have sufficient fuel and movement points for the specified route, it's an invalid move.
		if not isRouteValid(self.game.level, unit, route):
			return (ACTION_RESULT_INVALID, None)
		
		# Check up to what point the given route is unobstructed.
		(unobstructedRoute, route, obstructingUnit) = isRouteUnobstructed(self.game.getOtherPlayers(), route)
		fuelCost = fuelCostForRoute(self.game.level, unit, route)
		
		# An empty route is invalid!
		if len(route) == 0:
			return (ACTION_RESULT_INVALID, None)
		
		# If the obstructing unit was visible, then this route is invalid - units can't cross enemy units!
		if self.__visibilityMap.unitIsVisible(obstructingUnit):
			return (ACTION_RESULT_INVALID, None)
		else:
			situationUpdate = SituationUpdate(self.game)
			situationUpdate.addUnitUpdateForPlayer(self, unit)
			
			# Otherwise, the unit has been trapped.
			self.__visibilityMap.removeVision(unit.position, unit.currentVision(), unit.currentStealthDetectionRange())
			unit.moveTo(route[-1], fuelCost)
			self.unitIsFinished(unit)
			self.__visibilityMap.addVision(unit.position, unit.currentVision(), unit.currentStealthDetectionRange())
			
			return (ACTION_RESULT_TRAPPED, situationUpdate)
		
		# If none of the above applies, then check if there's a friendly unit at the destination.
		# The move command is context-sensitive, and can turn into a load or combine action.
		unitAtDestination = self.getUnitAtPosition(route[-1])
		
		if unitAtDestination != None:
			if unitAtDestination.canLoad(unit):
				unit.fuel -= fuelCost
				return self.__loadUnit(unit, unitAtDestination)
			elif unit.canCombineWithUnit(unitAtDestination):
				unit.fuel -= fuelCost
				return self.__combineUnits(unit, unitAtDestination)
			else:
				return (ACTION_RESULT_INVALID, None)
		else:
			situationUpdate = SituationUpdate(self.game)
			situationUpdate.addUnitUpdateForPlayer(self, unit)
			
			self.__visibilityMap.removeVision(unit.position, unit.currentVision(), unit.currentStealthDetectionRange())
			unit.moveTo(route[-1], fuelCost)
			self.__visibilityMap.addVision(unit.position, unit.currentVision(), unit.currentStealthDetectionRange())
			
			if unit.canActAfterMoving():
				self.unitHasMoved(unit)
			else:
				self.unitIsFinished(unit)
			
			return (ACTION_RESULT_SUCCESS, situationUpdate)
	#
	
	# Utility function, called from within moveUnit
	def __loadUnit(self, unit, unitAtDestination):
		situationUpdate = SituationUpdate(self.game)
		situationUpdate.addUnitUpdateForPlayer(self, unitAtDestination)
		situationUpdate.addUnitUpdateForPlayer(self, unit)
		
		# Load this unit.
		self.__visibilityMap.removeVision(unit.position, unit.currentVision(), unit.currentStealthDetectionRange())
		unitAtDestination.loadUnit(unit)
		# Loaded units can't see!
		
		return (ACTION_RESULT_SUCCESS, situationUpdate)
	#
	
	# Utility function, called from within moveUnit - unitAtDestination will be absorbed by unit
	def __combineUnits(self, unit, unitAtDestination):
		situationUpdate = SituationUpdate(self.game)
		situationUpdate.addUnitRemovalForPlayer(self, unitAtDestination)
		situationUpdate.addUnitUpdateForPlayer(self, unit)
		
		# Combine the units. Any left-over hitpoints are turned into cash.
		self.__visibilityMap.removeVision(unit.position, unit.currentVision(), unit.currentStealthDetectionRange())
		leftOverHitpoints = unit.combineWithUnit(unitAtDestination)
		self.__visibilityMap.addVision(unit.position, unit.currentVision(), unit.currentStealthDetectionRange())
		
		self.removeUnit(unitAtDestination)
		self.money += unit.repairCost(leftOverHitpoints)
		
		situationUpdate.updateMoneyAmountForPlayer(self, self.money)
		return (ACTION_RESULT_SUCCESS, situationUpdate)
	#
	
	def unloadUnit(self, unitID, destination):
		unit = self.getUnitByID(unitID)
		if unit == None or not unit.isLoaded() or not self.unitCanMove(unit):
			return (ACTION_RESULT_INVALID, None)
		
		# Units can only be unloaded onto tiles that they can move across, but they must also be able to cross the tile that the transporting unit is on.
		if not unit.canMoveAcross(self.game.level.getTerrainType(unit.position)) or not unit.canMoveAcross(self.game.level.getTerrainType(destination)):
			return (ACTION_RESULT_INVALID, None)
		
		for player in self.game.getAllPlayers():
			if player.getUnitAtPosition(destination) != None:
				return (ACTION_RESULT_INVALID, None)
		
		situationUpdate = SituationUpdate(self.game)
		situationUpdate.addUnitUpdateForPlayer(self, unit)
		situationUpdate.addUnitUpdateForPlayer(self, unit.carriedBy)
		
		unit.carriedBy.unloadUnit(unit, destination)
		
		self.unitIsFinished(unit)
		self.__visibilityMap.addVision(unit.position, unit.currentVision(), unit.currentStealthDetectionRange())
		return (ACTION_RESULT_SUCCESS, situationUpdate)
	#
	
	def supplySurroundingUnits(self, unitID):
		unit = self.getUnitByID(unitID)
		if unit == None or not unit.type.canSupply() or not self.unitCanPerformAction(unit):
			return (ACTION_RESULT_INVALID, None)
		
		neighboringUnits = []
		for offset in [Point(-1, 0), Point(0, -1), Point(1, 0), Point(0, 1)]:
			neighboringUnit = self.getUnitAtPosition(unit.position + offset)
			if neighboringUnit != None:
				neighboringUnits.append(neighboringUnit)
		
		# Filter out units that are fully supplied already
		neighboringUnits = filter(Unit.needsResupply, neighboringUnits)
		if len(neighboringUnits) == 0:
			return (ACTION_RESULT_INVALID, None)
		
		situationUpdate = SituationUpdate(self.game)
		
		for neighboringUnit in neighboringUnits:
			situationUpdate.addUnitUpdateForPlayer(self, neighboringUnit)
			neighboringUnit.resupply()
		
		self.unitIsFinished(unit)
		return (ACTION_RESULT_SUCCESS, situationUpdate)
	#
	
	def attackUnit(self, unitID, targetID):
		unit = self.getUnitByID(unitID)
		if unit == None or not self.unitCanPerformAction(unit):
			return (ACTION_RESULT_INVALID, None)
		
		targetUnit = None
		for player in self.game.getOtherPlayers(self):
			targetUnit = player.getUnitByID(targetID)
			if targetUnit != None:
				break
		else:
			return (ACTION_RESULT_INVALID, None)
		
		if not unit.canAttackUnit(targetUnit, unit in self.__movedUnits):
			return (ACTION_RESULT_INVALID, None)
		
		situationUpdate = SituationUpdate(self.game)
		unitUpdate = situationUpdate.addUnitUpdateForPlayer(self, unit)
		targetUnitUpdate = situationUpdate.addUnitUpdateForPlayer(targetUnit.player, targetUnit)
		
		unit.attackUnit(targetUnit)
		
		if not targetUnit.alive():
			self.__addLoadedUnitRemovalsToSituationUpdate(targetUnit, situationUpdate)
			targetUnit.player.removeUnit(targetUnit)
			targetUnitUpdate.newUnit = None
		
		if not unit.alive():
			self.__addLoadedUnitRemovalsToSituationUpdate(unit, situationUpdate)
			self.removeUnit(unit)
			unitUpdate.newUnit = None
		else:
			self.unitIsFinished(unit)
		
		return (ACTION_RESULT_SUCCESS, situationUpdate)
	#
	
	def buildUnit(self, buildingID, unitTypeID):
		building = self.getBuildingByID(buildingID)
		unitType = self.game.gameDatabase.getUnitType(unitTypeID)
		if building == None or not building.canBuild(unitType) or self.money < unitType.cost:
			return (ACTION_RESULT_INVALID, None)
		
		for player in self.game.getOtherPlayers(self):
			if player.getUnitAtPosition(building.position) != None:
				return (ACTION_RESULT_INVALID, None)
		
		situationUpdate = SituationUpdate(self.game)
		
		self.money -= unitType.cost
		unit = Unit(self.game, unitType, getGUID(), self)
		self.addUnit(unit)
		
		self.unitIsFinished()
		
		situationUpdate.addUnitCreationForPlayer(self, unit)
		situationUpdate.updateMoneyAmountForPlayer(self, self.money)
		return (ACTION_RESULT_SUCCESS, situationUpdate)
	#
	
	def captureBuilding(self, unitID):
		unit = self.getUnitByID(unitID)
		if unit == None or not unit.type.canCapture() or not self.unitCanPerformAction(unit):
			return (ACTION_RESULT_INVALID, None)
		
		building = self.game.level.getBuildingAtPosition(unit.position)
		if building in self.buildings:
			return (ACTION_RESULT_INVALID, None)
		
		situationUpdate = SituationUpdate(self.game)
		
		if unit.captureBuilding(building):
			situationUpdate.addBuildingRemovalForPlayer(building.player, building)
			if building.player != None:
				building.player.removeBuilding(building)
			
			self.addBuilding(building)
			situationUpdate.addBuildingCreationForPlayer(self, building)
		
		self.unitIsFinished(unit)
		return (ACTION_RESULT_SUCCESS, situationUpdate)
	#
	
	def hideUnit(self, unitID, hide):
		unit = self.getUnitByID(unitID)
		if unit == None or not unit.type.canHide() or not self.unitCanPerformAction(unit):
			return (ACTION_RESULT_INVALID, None)
		
		situationUpdate = SituationUpdate(self.game)
		situationUpdate.addUnitUpdateForPlayer(self, unit)
		
		if hide:
			unit.hide()
		else:
			unit.unhide()
		
		self.unitIsFinished(unit)
		return (ACTION_RESULT_SUCCESS, situationUpdate)
	#
	
	def endTurn(self):
		self.__activeUnits = []
		self.__movedUnits = []
		self.__finishedUnits = self.units[:]
		
		self.game.playerEndsTurn(self)
		
		for listener in self.__listeners:
			listener.onPlayerStartsTurn(self)
		
		return (ACTION_RESULT_SUCCESS, SituationUpdate(self.game))
	#
	
	
	# Recursively adds a unit removal update to the situation update for all transported units (excluding the transporting unit).
	def __addLoadedUnitRemovalsToSituationUpdate(self, unit, situationUpdate):
		if unit.isTransportingUnits():
			for loadedUnit in unit.loadedUnits:
				situationUpdate.addUnitRemovalForPlayer(loadedUnit.player, loadedUnit)
				self.__addLoadedUnitRemovalsToSituationUpdate(loadedUnit, situationUpdate)
	#
	
	def unitCanMove(self, unit):
		return unit in self.__activeUnits
	#
	
	def unitCanPerformAction(self, unit):
		return not unit in self.__finishedUnits
	#
	
	def unitHasMoved(self, unit):
		if unit in self.__finishedUnits:
			return
		if unit in self.__activeUnits:
			self.__activeUnits.remove(unit)
		if not unit in self.__movedUnits:
			self.__movedUnits.remove(unit)
	#
	
	def unitIsFinished(self, unit):
		if unit in self.__activeUnits:
			self.__activeUnits.remove(unit)
		if unit in self.__movedUnits:
			self.__movedUnits.remove(unit)
		if not unit in self.__finishedUnits:
			self.__finishedUnits.append(unit)
	#
	
	# Returns this players visibility map. Do not alter!
	def getVisibilityMap(self):
		return self.__visibilityMap
	#
	
	# Returns a copy of this players visibility map, as it was before the given situation update.
	# That is, any changes to this players units and buildings are reverted
	def getOldVisibilityMapForSituationUpdate(self, situationUpdate):
		oldVisibilityMap = copy.copy(self.__visibilityMap)
		if situationUpdate.playerUpdates.has_key(self):
			playerUpdate = situationUpdate.playerUpdates[self]
			
			# Remove the current vision and add the old vision for each unit and building - depending on whether or not they had and have vision.
			for unitUpdate in playerUpdate.unitUpdates:
				if unitUpdate.newUnit != None and not unitUpdate.newUnit.isLoaded():
					oldVisibilityMap.removeVision(unitUpdate.newUnit.position, \
					                              unitUpdate.newUnit.currentVision(), \
					                              unitUpdate.newUnit.currentStealthDetectionRange())
				if unitUpdate.oldUnit != None and not unitUpdate.oldUnit.isLoaded():
					oldVisibilityMap.addVision(unitUpdate.oldUnit.position, \
					                           unitUpdate.oldUnit.currentVision(), \
					                           unitUpdate.oldUnit.currentStealthDetectionRange())
			
			for buildingUpdate in playerUpdate.buildingUpdates:
				if buildingUpdate.newBuilding != None:
					oldVisibilityMap.removeVision(buildingUpdate.newBuilding.position, 0, 0)
				if buildingUpdate.oldBuilding != None:
					oldVisibilityMap.addVision(buildingUpdate.oldBuilding.position, 0, 0)
		
		return oldVisibilityMap
	#
	
	
	# Serialization - these functions are only used to send player information to clients.
	# Only the player ID and name are sent. hideinformation is only there for consistency with other toStream functions,
	# and currently serves no purpose.
	def toStream(self, hideInformation):
		return toStream(self.id, \
		                self.name)
	#
	
	# All but the game variable will be deserialized.
	def fromStream(self, stream):
		(self.id, \
		 self.name, \
		 readBytesCount) = fromStream(stream, int, str)
		
		return readBytesCount
	#
#