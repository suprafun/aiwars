from guid import *
from unit import *
from building import *
from pathfinding import *
from situationUpdate import *


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
		self.__visibleTiles = []
		self.__stealthDetectedTiles = []
		for y in xrange(self.game.level.height()):
			self.__visibleTiles.append([0] * self.game.level.width())
			self.__stealthDetectedTiles.append([0] * self.game.level.width())
		
		
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
			
			self.__updateVisibilityMaps(building.position, 0, -1, 1)
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
			self.__updateVisibilityMaps(building.position, 0, -1, -1)
			
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
			self.__updateVisibilityMaps(unit.position, unit.currentVision(), unit.currentStealthDetectionRange(), 1)
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
			
			self.__updateVisibilityMaps(unit.position, unit.currentVision(), unit.currentStealthDetectionRange(), -1)
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
		
		# Check all units that can be resupplied or repaired. Units standing on friendly buildings or next to supplying units will be supplied.
		# Units standing on friendly buildings that can repair them will be repaired up to 2 hitpoints (less if not enough funds is available).
		# Units are checked in the order that they're built.
		supplyingUnits = filter(Unit.canSupply, self.units)
		for unit in filter(lambda unit: unit.needsResupply() or unit.needsRepair, self.units):
			building = self.getBuildingAtPosition(unit.position)
			
			resupply = False
			if unit.needsResupply():
				if building != None:
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
		
		# TODO: Subtract fuel for units that use fuel each turn and remove any crashed units (units that ran out of fuel with the setting 'needs-fuel-to-survive')
		
		self.__activeUnits = self.units[:]
		self.__movedUnits = []
		self.__finishedUnits = []
		
		for listener in self.__listeners:
			listener.onPlayerStartsTurn(self)
		
		situationUpdate.updateMoneyAmountForPlayer(self, self.money)
		return (ACTION_RESULT_SUCCESS, situationUpdate)
		# TODO: Send listeners a situationUpdate! resupplied units + money update!
	#
	
	# Returns a (result, situationUpdate) tuple - the situation update is None if the result is invalid.
	# TODO: Add a utility function that updates the visibility/stealth detection maps and that extracts a list
	# of no-longer visible and newly visible units/buildings from other players!
	def moveUnit(self, unitID, route):
		unit = self.getUnitByID(unitID)
		if unit == None or not self.unitCanMove(unit):
			return (ACTION_RESULT_INVALID, None)
		
		if not isRouteValid(self.game.level, unit.type, route):
			return (ACTION_RESULT_INVALID, None)
		
		# TODO: Also tell what unit obstructed the route, and check if that unit was previously visible - if visible, it's an INVALID move. If invisible, it's a TRAPPED situation!!!
		(unobstructedRoute, route, obstructingUnit) = isRouteUnobstructed(self.game.getOtherPlayers(), route)
		
		# An empty route is invalid!
		if len(route) == 0:
			return (ACTION_RESULT_INVALID, None)
		
		# If the obstructing unit was visible, then this route is invalid - units can't cross enemy units!
		if self.canSeeEnemyUnit(obstructingUnit):
			return (ACTION_RESULT_INVALID, None)
		else:
			situationUpdate = SituationUpdate(self.game)
			situationUpdate.addUnitUpdateForPlayer(self, unit)
			
			# Otherwise, the unit has been trapped.
			self.__updateVisibilityMaps(unit.position, unit.currentVision(), unit.currentStealthDetectionRange(), -1)
			unit.moveTo(route[-1])
			self.unitIsFinished(unit)
			self.__updateVisibilityMaps(unit.position, unit.currentVision(), unit.currentStealthDetectionRange(), 1)
			
			return (ACTION_RESULT_TRAPPED, situationUpdate)
		
		# If none of the above applies, then check if there's a friendly unit at the destination.
		# The move command is context-sensitive, and can turn into a load or combine action.
		unitAtDestination = self.getUnitAtPosition(route[-1])
		
		if unitAtDestination != None:
			if unitAtDestination.canLoad(unit):
				return self.__loadUnit(unit, unitAtDestination)
			elif unit.canCombineWithUnit(unitAtDestination):
				return self.__combineUnits(unit, unitAtDestination)
			else:
				return (ACTION_RESULT_INVALID, None)
		else:
			situationUpdate = SituationUpdate(self.game)
			situationUpdate.addUnitUpdateForPlayer(self, unit)
			
			self.__updateVisibilityMaps(unit.position, unit.currentVision(), unit.currentStealthDetectionRange(), -1)
			unit.moveTo(route[-1])
			self.__updateVisibilityMaps(unit.position, unit.currentVision(), unit.currentStealthDetectionRange(), 1)
			
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
		self.__updateVisibilityMaps(unit.position, unit.currentVision(), unit.currentStealthDetectionRange(), -1)
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
		self.__updateVisibilityMaps(unit.position, unit.currentVision(), unit.currentStealthDetectionRange(), -1)
		leftOverHitpoints = unit.combineWithUnit(unitAtDestination)
		self.__updateVisibilityMaps(unit.position, unit.currentVision(), unit.currentStealthDetectionRange(), 1)
		
		self.removeUnit(unitAtDestination)
		self.money += unit.repairCost(leftOverHitpoints)
		
		situationUpdate.updateMoneyAmountForPlayer(self, self.money)
		return (ACTION_RESULT_SUCCESS, situationUpdate)
	#
	
	def unloadUnit(self, unitID, destination):
		unit = self.getUnitByID(unitID)
		if unit == None or unit.carriedBy == None or not self.unitCanMove(unit):
			return (ACTION_RESULT_INVALID, None)
		
		for player in self.game.getAllPlayers():
			if player.getUnitAtPosition(destination) != None:
				return (ACTION_RESULT_INVALID, None)
		
		situationUpdate = SituationUpdate(self.game)
		situationUpdate.addUnitUpdateForPlayer(self, unit)
		situationUpdate.addUnitUpdateForPlayer(self, unit.carriedBy)
		
		unit.carriedBy.unloadUnit(unit, destination)
		
		self.unitIsFinished(unit)
		self.__updateVisibilityMaps(unit.position, unit.currentVision(), unit.currentStealthDetectionRange(), 1)
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
			targetUnit.player.removeUnit(targetUnit)
			targetUnitUpdate.newUnit = None
		
		if not unit.alive():
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
	
	# All tiles are visible in normal mode, but in fog-of-war mode, only tiles within sight are visible.
	# Some terrain types can hide units, they are only visible when a unit is standing directly next to them.
	def canSeeTile(self, position):
		if not self.game.fogOfWar:
			return True
		else:
			return self.__visibleTiles[position.y][position.x] > 0
	#
	
	# Returns True if the specified tile lies within the stealth detection range of at least one friendly unit.
	# Usually this means that there's a friendly unit next to the specified tile (if stealth detection range is 1).
	def canStealthDetectTile(self, position):
		return self.__stealthDetectedTiles[position.y][position.x] > 0
	#
	
	# Checks if the enemy unit is visible. If it is hidden, it can only be detected by units next to it.
	def canSeeEnemyUnit(self, enemyUnit):
		if enemyUnit.isLoaded() and self.game.fogOfWar:
			return False
		elif enemyUnit.isHiding():
			return self.canSeeHiddenUnit(enemyUnit)
		else:
			return self.canSeeTile(enemyUnit.position)
	#
	
	# Hidden units can only be seen when they're within a friendly units stealth detection range.
	def canSeeHiddenUnit(self, hiddenUnit):
		return self.canStealthDetectTile(hiddenUnit.position)
	#
	
	# When moving a unit from one location to another, call this function twice: once with it's original position and a modifier of -1,
	# and then with it's new position and a modifier of 1. When a unit is destroyed, call this function once, with a modifier of -1,
	# and when a unit is built, call it once with a modifier of 1.
	# The same is done for adding and removing buildings: when adding, call with the building position, a visionRange of 1 and a modifier of 1.
	# When the building is lost, call this function again with a modifier of -1.
	def __updateVisibilityMaps(self, position, visionRange, stealthDetectionRange, modifier):
		for y in xrange(position.y - visionRange, position.y + visionRange + 1):
			width = visionRange - abs(y - position.y)
			for x in xrange(position.x - width, position.x + width + 1):
				if x >= 0 and y >= 0 and x < self.game.level.width() and y < self.game.level.height():
					oldValue = self.__visibleTiles[y][x]
					self.__visibleTiles[y][x] += modifier
		
		for y in xrange(position.y - stealthDetectionRange, position.y + stealthDetectionRange + 1):
			width = stealthDetectionRange - abs(y - position.y)
			for x in xrange(position.x - width, position.x + width + 1):
				if x >= 0 and y >= 0 and x < self.game.level.width() and y < self.game.level.height():
					oldValue = self.__stealthDetectedTiles[y][x]
					self.__stealthDetectedTiles[y][x] += modifier
	#
	
	
	# Serialization - these functions are only used to send player information to clients.
	# Only the player ID and name are sent. hideinformation is only there for consistency with other toStream functions,
	# and currently serves no purpose.
	def toStream(self, hideInformation):
		return toStream(self.id, \
		                self.name)
		# TODO: Also send units and buildings along?
	#
	
	# All but the game variable will be deserialized.
	def fromStream(self, stream):
		(self.id, \
		 self.name, \
		 readBytesCount) = fromStream(stream, int, str)
		
		return readBytesCount
	#
#