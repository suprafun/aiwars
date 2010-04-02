from unitType import *
from guid import *
from point import *


class Unit:
	# Creates a new unit, of a given type, at the specified position. Units keep a reference to the Field instance that they're located on, in order to check their surroundings.
	def __init__(self, type, position, field):
		self.type = type
		self.id = getGUID()
		self.field = field
		
		self.hitpoints = self.type.maxHitpoints
		self.position = position
		self.ammunition = self.type.maxAmmunition
		
		self.loadedUnits = []
		self.carriedBy = None
	#
	
	# Returns the current vision range, taking terrain type into account.
	def currentVision(self):
		return self.type.visionOn(self.field.getTerrainType(self.position))
	#
	
	# Returns the movement cost for the given terrain type.
	def movementCostFor(self, terrainType):
		return self.type.movementCostFor(terrainType)
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
	
	# Returns the repair cost for the specified number of hitpoints. This function does not take the current and maximum number of hitpoints into account.
	def repairCost(self, amount):
		return int(self.type.cost / 10) * amount
	#
	
	
	# Loads the specified unit, if possible.
	def loadUnit(self, unit):
		if self.canLoad(unit.type):
			self.loadedUnits.append(unit)
			unit.carriedBy = self
	#
	
	# Unload the specified unit at the given destination.
	def unloadUnit(self, unit, destination):
		if unit.carriedBy is self and manhattanDistance(self.position, destination) == 1:
			self.loadedUnits.remove(unit)
			unit.position.set(destination)
			unit.carriedBy = None
	#
	
	# Fully restore this units ammunition supply.
	def supplyWithAmmunition(self):
		self.ammunition = self.type.maxAmmunition
	#
	
	# Repairs this unit and returns the number of hitpoints that were actually repaired. A unit can not be repaired beyond it's maximum number of hitpoints.
	def repair(self, amount):
		previousHitpoints = self.hitpoints
		self.hitpoints = min(self.type.maxHitpoints, self.type.hitpoints + amount)
		return self.hitpoints - previousHitpoints
	#
	
	# Attack the specified unit, if possible. If the unit was successfully attacked, it will retaliate, if possible.
	def attackUnit(self, target, didMove):
		if didMove and not self.type.canFireAfterMove:
			return False
		
		if self.unitWithinRange(target):
			self.__fireAtTarget(target)
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
		finalDamage = max(0, round(damage - (damage * self.field.getTerrainType(self.position).cover * 0.1)))
		previousHitpoints = self.hitpoints
		self.hitpoints = max(0, self.hitpoints - finalDamage)
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
	
	# Returns True if this unit can be combined with the specified unit. Both units must be of the same type and at least one of the units must be damaged. None of them must contain any other units.
	def canCombineWith(self, unit):
		# Same type, and at least one of them is damaged?
		return self.type is unit.type and \
		       (self.hitpoints < self.type.maxHitpoints or unit.hitpoints < unit.type.maxHitpoints) and \
		       (not self.isTransportingUnits() and not unit.isTransportingUnits())
	#
	
	# Combines this unit with the specified unit. Returns the number of hitpoints that were left over.
	def combineWith(self, unit):
		totalHitpoints = self.hitpoints + unit.hitpoints
		self.hitpoints = min(self.type.maxHitpoints, self.hitpoints + unit.hitpoints)
		self.ammunition = min(self.type.maxAmmunition, self.ammunition + unit.ammunition)
		# TODO: Take care of loaded units!!! Perhaps don't allow combining when units are carrying other units?
		
		return round(self.type.cost * (totalHitpoints - self.hitpoints) * 0.1)
	#
	
	# Returns True if this unit can capture buildings.
	def canCapture(self):
		return self.type.canCapture
	#
	
	# Returns True if this unit can supply other units.
	def canSupply(self):
		return self.type.canSupply
	#
#