from guid import *
from unit import *
from building import *
from pathfinding import *


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
		
		# Visibility map, shows how many units can see a certain tile. It is updated every time a unit is created, moved, loaded, unloaded, or destroyed,
		# and every time a building is captured or lost.
		self.__visibleTiles = []
		for y in xrange(self.game.level.height()):
			self.__visibleTiles.append([])
			for x in xrange(self.game.level.width()):
				self.__visibleTiles[-1].append(0)
	#
	
	def addBuilding(self, building):
		if not building in self.buildings:
			self.buildings.append(building)
			self.__updateVisibilityMap(building.position, 0, 1)
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
	
	def removeBuilding(self, building):
		if building in self.buildings:
			buildings.remove(building)
			self.__updateVisibilityMap(building.position, 0, -1)
			
			# If the building was critical, check if there's still any other critical buildings left!
			if building.isCritical():
				for building in self.buildings:
					if building.isCritical():
						break
				else:
					self.game.playerHasLost(self)
	#
	
	def addUnit(self, unit):
		self.units.append(unit)
		
		self.unitIsFinished(newUnit)
		self.__updateVisibilityMap(unit.position, unit.currentVision(), 1)
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
	
	def removeUnit(self, unit):
		if unit in self.units:
			self.units.remove(unit)
			
			if unit in self.__activeUnits:
				self.__activeUnits.remove(unit)
			if unit in self.__movedUnits:
				self.__movedUnits.remove(unit)
			if unit in self.__finishedUnits:
				self.__finishedUnits.remove(unit)
			
			self.__updateVisibilityMap(unit.position, unit.currentVision(), -1)
	#
	
	
	def startTurn(self):
		# Add income
		for building in self.buildings:
			self.money += building.type.income
		
		# Repair units that are standing on buildings that can repair their type, if enough funds is available. Checks units in the order that they were created.
		# If there is insufficient funds, the unit is not repaired - even if repairing a single hitpoint would've been affordable.
		for unit in self.units:
			building = self.getBuildingAtPosition(unit.position)
			if building != None and building.canRepair(unit.type):
				actualRepairAmount = unit.actualRepairAmount(building.repairAmount())
				repairCost = unit.repairCost(actualRepairAmount)
				if repairCost <= self.money:
					self.money -= repairCost
					unit.repair(actualRepairAmount)
		
		self.__activeUnits = self.units[:]
		self.__movedUnits = []
		self.__finishedUnits = []
	#
	
	def moveUnit(self, unitID, route):
		unit = self.getUnitByID(unitID)
		if unit == None or not self.unitCanMove(unit):
			return ACTION_RESULT_INVALID
		
		if not isRouteValid(self.game.level, unit.type, route):
			return ACTION_RESULT_INVALID
		
		# TODO: Also tell what unit obstructed the route, and check if that unit was previously visible - if visible, it's an INVALID move. If invisible, it's a TRAPPED situation!!!
		(unobstructedRoute, route, obstructingUnit) = isRouteUnobstructed(self.game.getOtherPlayers(), route)
		
		# An empty route is invalid!
		if len(route) == 0:
			return ACTION_RESULT_INVALID
		
		# If the obstructing unit was visible, then this route is invalid - units can't cross enemy units!
		if self.canSeeEnemyUnit(obstructingUnit):
			return ACTION_RESULT_INVALID
		else:
			# Otherwise, the unit has been trapped.
			self.__updateVisibilityMap(unit.position, unit.currentVision(), -1)
			unit.moveTo(route[-1])
			self.unitIsFinished(unit)
			self.__updateVisibilityMap(unit.position, unit.currentVision(), 1)
			
			return ACTION_RESULT_TRAPPED
		
		# If none of the above applies, then check if there's a friendly unit at the destination.
		# The move command is context-sensitive, and can turn into a load or combine action.
		unitAtDestination = self.getUnitAtPosition(route[-1])
		
		if unitAtDestination != None:
			if unitAtDestination.canLoad(unit):
				
				# Load this unit.
				self.__updateVisibilityMap(unit.position, unit.currentVision(), -1)
				unitAtDestination.loadUnit(unit)
				# Loaded units can't see!
				
				return ACTION_RESULT_SUCCESS
			elif unit.canCombineWithUnit(unitAtDestination):
				
				# Combine the units. Any left-over hitpoints are turned into cash.
				self.__updateVisibilityMap(unit.position, unit.currentVision(), -1)
				leftOverHitpoints = unit.combineWithUnit(unitAtDestination)
				self.__updateVisibilityMap(unit.position, unit.currentVision(), 1)
				
				self.removeUnit(unitAtDestination)
				self.money += unit.repairCost(leftOverHitpoints)
				return ACTION_RESULT_SUCCESS
			else:
				return ACTION_RESULT_INVALID
		else:
			self.__updateVisibilityMap(unit.position, unit.currentVision(), -1)
			unit.moveTo(route[-1])
			self.__updateVisibilityMap(unit.position, unit.currentVision(), 1)
			
			if unit.canActAfterMoving():
				self.unitHasMoved(unit)
			else:
				self.unitIsFinished(unit)
			
			return ACTION_RESULT_SUCCESS
	#
	
	def unloadUnit(self, unitID, destination):
		unit = self.getUnitByID(unitID)
		if unit == None or unit.carriedBy == None or not self.unitCanMove(unit):
			return ACTION_RESULT_INVALID
		
		for player in self.game.getAllPlayers():
			if player.getUnitAtPosition(destination) != None:
				return ACTION_RESULT_INVALID
		
		unit.carriedBy.unloadUnit(unit, destination)
		
		self.unitIsFinished(unit)
		self.__updateVisibilityMap(unit.position, unit.currentVision(), 1)
		return ACTION_RESULT_SUCCESS
	#
	
	def supplySurroundingUnits(self, unitID):
		unit = self.getUnitByID(unitID)
		if unit == None or not unit.type.canSupply() or not self.unitCanPerformAction(unit):
			return ACTION_RESULT_INVALID
		
		neighboringUnits = []
		for offset in [Point(-1, 0), Point(0, -1), Point(1, 0), Point(0, 1)]:
			neighboringUnit = self.getUnitAtPosition(unit.position + offset)
			if neighboringUnit != None:
				neighboringUnits.append(neighboringUnit)
		
		if len(neighboringUnits) == 0:
			return ACTION_RESULT_INVALID
		
		for neighboringUnit in neighboringUnits:
			neighboringUnit.resupply()
		
		self.unitIsFinished(unit)
		return ACTION_RESULT_SUCCESS
	#
	
	def attackUnit(self, unitID, targetID):
		unit = self.getUnitByID(unitID)
		if unit == None or not self.unitCanPerformAction(unit):
			return ACTION_RESULT_INVALID
		
		targetUnit = None
		for player in self.game.getOtherPlayers(self):
			targetUnit = player.getUnitByID(targetID)
			if targetUnit != None:
				break
		else:
			return ACTION_RESULT_INVALID
		
		if not unit.canAttackUnit(targetUnit, unit in self.__movedUnits):
			return ACTION_RESULT_INVALID
		
		unit.attackUnit(targetUnit)
		
		if not targetUnit.alive():
			targetUnit.player.removeUnit(targetUnit)
		
		if not unit.alive():
			self.removeUnit(unit)
		else:
			self.unitIsFinished(unit)
		
		return ACTION_RESULT_SUCCESS
	#
	
	def buildUnit(self, buildingID, unitTypeID):
		building = self.getBuildingByID(buildingID)
		unitType = self.game.gameDatabase.getUnitType(unitTypeID)
		if building == None or not building.canBuild(unitType) or self.money < unitType.cost:
			return ACTION_RESULT_INVALID
		
		for player in self.game.getOtherPlayers(self):
			if player.getUnitAtPosition(building.position) != None:
				return ACTION_RESULT_INVALID
		
		self.money -= unitType.cost
		self.addUnit(Unit(self.game.gameDatabase, unitType, getGUID(), self.game.level, self))
		
		self.unitIsFinished()
		return ACTION_RESULT_SUCCESS
	#
	
	def captureBuilding(self, unitID):
		unit = self.getUnitByID(unitID)
		if unit == None or not unit.type.canCapture() or not self.unitCanPerformAction(unit):
			return ACTION_RESULT_INVALID
		
		building = self.game.level.getBuildingAtPosition(unit.position)
		if building in self.buildings:
			return ACTION_RESULT_INVALID
		
		if unit.captureBuilding(building):
			self.addBuilding(building)
			for player in self.game.getOtherPlayers(self):
				player.removeBuilding(building)
		
		self.unitIsFinished(unit)
		return ACTION_RESULT_SUCCESS
	#
	
	def hideUnit(self, unitID, hide):
		unit = self.getUnitByID(unitID)
		if unit == None or not unit.type.canHide() or not self.unitCanPerformAction(unit):
			return ACTION_RESULT_INVALID
		
		if hide:
			unit.hide()
		else:
			unit.unhide()
		
		self.unitIsFinished(unit)
		return ACTION_RESULT_SUCCESS
	#
	
	def endTurn(self):
		self.__activeUnits = []
		self.__movedUnits = []
		self.__finishedUnits = self.units[:]
		
		return ACTION_RESULT_SUCCESS
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
	
	# Checks if the enemy unit is visible. If it is hidden, it can only be detected by units next to it.
	def canSeeEnemyUnit(self, enemyUnit):
		if enemyUnit.isHiding():
			return self.canSeeHiddenUnit(enemyUnit)
		elif self.game.fogOfWar:
			return self.canSeeTile(enemyUnit.position)
		else:
			return True
	#
	
	# Hidden units can only be seen by units directly next to them.
	def canSeeHiddenUnit(self, hiddenUnit):
		hUnitPos = hiddenUnit.position
		for position in [Point(hUnitPos.x - 1, hUnitPos.y), Point(hUnitPos.x, hUnitPos.y - 1), Point(hUnitPos.x + 1, hUnitPos.y), Point(hUnitPos.x, hUnitPos.y + 1)]:
			if self.getUnitAtPosition(position) != None:
				return True
		return False
	#
	
	# When moving a unit from one location to another, call this function twice: once with it's original position and a modifier of -1,
	# and then with it's new position and a modifier of 1.
	# The same is done for adding and removing buildings: when adding, call with the building position, a visionRange of 1 and a modifier of 1.
	# When the building is lost, call this function again with a modifier of -1.
	def __updateVisibilityMap(self, position, visionRange, modifier):
		for y in xrange(position.y - visionRange, position.y + visionRange + 1):
			width = visionRange - abs(y - position.y)
			for x in xrange(position.x - width, position.x + width + 1):
				if x >= 0 and y >= 0 and x < self.game.level.width() and y < self.game.level.height():
					self.__visibleTiles[y][x] += modifier
	#
#