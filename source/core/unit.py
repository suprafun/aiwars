import copy
from unitType import *
from serialization import *


class Unit(object):
	# Creates a new unit, of a given type, at the specified position. Units use the GameDatabase and the Level reference in the given Game instance.
	def __init__(self, game, type, id, position, player):
		self.game = game
		self.type = type
		self.id = id
		self.player = player
		
		self.hitpoints = self.type.maxHitpoints if self.type != None else 10
		self.position = position
		self.ammunition = self.type.maxAmmunition if self.type != None else 0
		
		self.loadedUnits = []
		self.carriedBy = None
		
		self.hiding = False
		
		self.captureTarget = None
	#
	
	# Returns the current vision range, taking terrain type into account.
	def currentVision(self):
		return self.type.visionOn(self.game.level.getTerrainType(self.position))
	#
	
	def currentStealthDetectionRange(self):
		return self.type.stealthDetectionRange
	#
	
	# Returns the movement cost for the given terrain type.
	def movementCostFor(self, terrainType):
		return self.type.movementCostFor(terrainType)
	#
	
	# Move to the specified position, instantly (route checking is up to the player). Also moves all units that are being transported.
	def moveTo(self, position, useFuel = True):
		self.position.set(position)
		# TODO: Subtract fuel!
		for unit in self.transports:
			unit.moveTo(position, False)
	#
	
	# Returns True if this unit is currently transporting one or more units.
	def isTransportingUnits(self):
		return len(self.loadedUnits) > 0
	#
	
	# Returns the number of unoccupied transport slots.
	def freeTransportSlots(self):
		freeSlots = self.type.maxTransportSlots
		for unit in self.loadedUnits:
			freeSlots -= self.type.transports[unit.type]
		return freeSlots
	#
	
	# Returns True if this unit has enough transport slots left for the specified unit.
	def canLoad(self, unitType):
		return self.type.transports.contains(unitType) and self.freeTransportSlots >= self.type.transports[unitType]
	#
	
	# Returns True if this unit is not at full health.
	def isDamaged(self):
		return self.hitpoints < self.type.maxHitpoints
	#
	
	# Returns the repair cost for the specified number of hitpoints. This function does not take the current and maximum number of hitpoints into account.
	def repairCost(self, amount):
		return int(self.type.cost / 10) * amount
	#
	
	# Returns how much hitpoints can actually be repaired, taking the current and maximum number of hitpoints into account.
	def actualRepairAmount(self, amount):
		return min(amount, self.type.maxHitpoints - self.hitpoints)
	#
	
	# Returns true if this unit can perform actions after moving.
	def canActAfterMoving(self):
		return self.type.canActAfterMoving
	#
	
	# Returns True if this unit can capture buildings.
	def canCapture(self):
		return self.type.canCapture
	#
	
	# Returns True if this unit can supply other units.
	def canSupply(self):
		return self.type.canSupply
	#
	
	# Returns true if this unit can hide anywhere.
	def canHide(self):
		return self.type.canHide
	#
	
	
	# Loads the specified unit, if possible.
	def loadUnit(self, unit):
		if self.canLoad(unit.type):
			self.loadedUnits.append(unit)
			unit.carriedBy = self
			unit.moveTo(self.position)
			unit.resupply()
	#
	
	# Unload the specified unit at the given destination.
	def unloadUnit(self, unit, destination):
		if unit.carriedBy is self and manhattanDistance(self.position, destination) == 1:
			self.loadedUnits.remove(unit)
			unit.moveTo(destination)
			unit.carriedBy = None
	#
	
	# Returns true if this unit is being transported by another unit.
	def isLoaded(self):
		return self.carriedBy != None
	#
	
	# Does this unit need any supplies?
	def needsResupply(self):
		return self.ammunition < self.type.maxAmmunition
		# TODO: Or when missing some fuel!
	#
	
	# Fully restores this units ammunition supply.
	def resupply(self):
		self.ammunition = self.type.maxAmmunition
		# TODO: Resupply fuel too!
	#
	
	# Is this unit damaged?
	def needsRepair(self):
		return self.hitpoints < self.type.maxHitpoints
	#
	
	# Repairs this unit and returns the number of hitpoints that were actually repaired. A unit can not be repaired beyond it's maximum number of hitpoints.
	def repair(self, amount):
		actualRepairAmount = self.actualRepairAmount(amount)
		self.hitpoints += actualRepairAmount
		return actualRepairAmount
	#
	
	# Returns true if this unit can attack the specified unit. Checks if this unit can fire after moving, if the target unit is within range
	# and whether or not this unit can actually damage the target.
	def canAttackUnit(self, target, moved):
		if moved and not self.type.canFireAfterMove:
			return False
		
		if not self.unitWithinRange(target):
			return False
		
		primaryDamage = self.type.primaryDamageAgainst(target.type)
		secondaryDamage = self.type.secondaryDamageAgainst(target.type)
		return (self.ammunition > 0 and primaryDamage > 0) or (secondaryDamage > 0)
	#
	
	# Attack the specified unit. Call canAttackUnit() first to see if it's possible to attack the given unit. This function performs no such checks.
	def attackUnit(self, target):
		self.__fireAtTarget(target)
		
		if target.alive():
			target.__retaliate(self)
	#
	
	def __retaliate(self, target):
		if self.type.canRetaliate and self.unitWithinRange(target):
			self.__fireAtTarget(target)
	#
	
	def __fireAtTarget(self, target):
		primaryDamage = self.type.primaryDamageAgainst(target.type)
		secondaryDamage = self.type.secondaryDamageAgainst(target.type)
		if self.ammunition > 0 and primaryDamage > secondaryDamage:
			target.applyDamage(primaryDamage)
			self.ammunition -= 1
		else:
			target.applyDamage(secondaryDamage)
	#
	
	# Apply damage to this unit. Terrain cover will be taken into account, so there may be less actual damage dealt. Returns the actual damage done.
	def applyDamage(self, damage):
		# Take cover into account - each cover point reduces incoming damage by 10%. Reductions beyond 100% are capped to 100% (e.g. more cover does not result in healing)
		finalDamage = max(0, int(round(damage - (damage * self.game.level.getTerrainType(self.position).cover * 0.1))))
		previousHitpoints = self.hitpoints
		self.hitpoints = int(max(0, self.hitpoints - finalDamage))
		return previousHitpoints - self.hitpoints
	#
	
	# Returns True if the specified unit is within range.
	def unitWithinRange(self, unit):
		manhattanDistance = manhattanDistance(self.position, unit.position)
		return manhattanDistance >= self.type.minRange and manhattanDistance <= self.type.maxRange
	#
	
	# Returns True if this unit is still alive.
	def alive(self):
		return self.hitpoints > 0
	#
	
	# Returns True if this unit can be combined with the specified unit. Both units must be of the same type
	# and at least the target units must be damaged. None of them must contain any other units or be loaded themselves.
	def canCombineWithUnit(self, unit):
		# Same type, and at least one of them is damaged?
		return (self.type is unit.type) and \
		       (unit.hitpoints < unit.type.maxHitpoints) and \
		       (not self.isTransportingUnits() and not unit.isTransportingUnits()) and \
		       (not self.isLoaded() and not unit.isLoaded())
	#
	
	# Combines this unit with the specified unit. Returns the number of hitpoints that were left over. First call canCombineWithUnit() to see if these units can be combined!
	def combineWithUnit(self, unit):
		totalHitpoints = self.hitpoints + unit.hitpoints
		self.hitpoints = min(self.type.maxHitpoints, self.hitpoints + unit.hitpoints)
		self.ammunition = min(self.type.maxAmmunition, self.ammunition + unit.ammunition)
		
		return totalHitpoints - self.hitpoints
	#
	
	# Captures the given building. Returns True if the building has fully been captured.
	def captureBuilding(self, building):
		self.captureTarget = building
		if self.captureTarget.capture(self.hitpoints):
			self.captureTarget.restoreCapturePoints()
			self.captureTarget = None
			return True
	#
	
	# Hides this unit, if it can. For example, a sub that submerges itself goes into hiding. Hidden units can only be seen by units directly next to them.
	def hide(self):
		if self.canHide():
			self.hiding = True
	#
	
	# Unhides the unit. For example, an emerging submarine.
	def unhide(self):
		self.hiding = False
	#
	
	# True if this unit is hiding. For example, a submerged submarine would return True if it is submerged, and False if it's on the surface.
	def isHiding(self):
		return self.hiding
	#
	
	# True if this unit is hidden by terrain
	def isHiddenByTerrain(self):
		return self.game.level.getTerrainType(self.position).hideUnits
	#
	
	
	# Forcefully kill this unit.
	def kill(self):
		self.hitpoints = 0
		self.onDeath()
	#
	
	# Clean up some things when this unit dies.
	def onDeath(self):
		# If this unit was capturing a building, undo all capturing progress.
		if self.captureTarget != None:
			self.captureTarget.restoreCapturePoints()
			self.captureTarget = None
		
		# If this unit was transporting other units, kill them.
		for unit in self.loadedUnits:
			unit.kill()
		self.loadedUnits = []
	#
	
	# Special method, called when making a shallow copy
	def __copy__(self):
		unit = Unit(self.game, self.type, self.id, copy.copy(self.position), self.player)
		
		unit.hitpoints = self.hitpoints
		unit.ammunition = self.ammunition
		
		unit.loadedUnits = self.loadedUnits[:]
		unit.carriedBy = self.carriedBy
		
		unit.hiding = self.hiding
		
		unit.captureTarget = self.captureTarget
		
		return unit
	#
	
	def applyUnitUpdate(self, unitUpdate):
		self.hitpoints = unitUpdate.newUnit.hitpoints
		self.position = unitUpdate.newUnit.position
		self.ammunition = unitUpdate.newUnit.ammunition
		
		self.loadedUnits = unitUpdate.newUnit.loadedUnits
		self.carriedBy = unitUpdate.newUnit.carriedBy
		
		self.hiding = unitUpdate.newUnit.hiding
		
		self.captureTarget = unitUpdate.newUnit.captureTarget
	#
	
	
	# Serialization - certain variables can be hidden, such as which units are carried - used during fog-of-war matches.
	# This does not change the serialized data layout, it just writes empty lists and zeroes instead of the actual values.
	# The clients should know that such data is not disclosed during fog-of-war matches.
	# Note that the game variable is not serialized, and references to other objects are turned into IDs or indices.
	def toStream(self, hideInformation):
		carriedByID = 0
		if self.carriedBy != None:
			carriedByID = self.carriedByID.id
		
		captureTargetID = 0
		if self.captureTarget != None:
			captureTargetID = self.captureTarget.id
		
		loadedUnitIDs = [unit.id for unit in self.loadedUnits]
		if hideInformation:
			loadedUnitIDs = []
		
		return toStream(self.game.gameDatabase.getIndexOfUnitType(self.type), \
		                self.id, \
		                self.player.id, \
		                self.hitpoints, \
		                self.position.x, \
		                self.position.y, \
		                self.ammunition, \
		                loadedUnitIDs, \
		                carriedByID, \
		                self.hiding, \
		                captureTargetID)
	#
	
	# All but the game variable will be deserialized.
	def fromStream(self, stream):
		(typeIndex, \
		 self.id, \
		 playerID, \
		 self.hitpoints, \
		 self.position.x, \
		 self.position.y, \
		 self.ammunition, \
		 loadedUnitIDs, \
		 carriedByID, \
		 self.hiding, \
		 captureTargetID, \
		 readBytesCount) = fromStream(stream, int, int, int, int, int, int, int, list, int, bool, int)
		
		self.type = self.game.gameDatabase.getUnitType(typeIndex)
		self.player = self.game.getPlayerByID(playerID)
		
		self.loadedUnits = [self.player.getUnitByID(unitID) for unitID in loadedUnitIDs]
		
		if carriedByID == 0:
			self.carriedBy = None
		else:
			self.carriedBy = self.player.getUnitByID(carriedByID)
		
		if captureTargetID == 0:
			self.captureTarget = None
		else:
			self.captureTarget = self.player.game.getBuildingByID(captureTargetID)
		
		return readBytesCount
	#
#