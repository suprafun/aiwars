from unitType import *
from guid import *
from point import *


class Unit:
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
	
	def currentVision(self):
		return self.type.visionOn(self.field.getTerrainType(self.position))
	#
	
	def movementCostFor(self, terrainType):
		return self.type.movementCostFor(terrainType)
	#
	
	def freeTransportSlots(self):
		freeSlots = self.type.maxTransportSlots
		for unit in self.loadedUnits:
			freeSlots -= self.type.transports[unit.type]
		return freeSlots
	#
	
	def canLoad(self, unitType):
		return self.type.transports.contains(unitType) and self.freeTransportSlots >= self.type.transports[unitType]
	#
	
	def repairCost(self, amount):
		return int(self.type.cost / 10) * amount
	#
	
	
	def loadUnit(self, unit):
		if self.canLoad(unit.type):
			self.loadedUnits.append(unit)
			unit.carriedBy = self
	#
	
	def unloadUnit(self, unit, destination):
		if unit.carriedBy is self and manhattanDistance(self.position, destination) == 1:
			self.loadedUnits.remove(unit)
			unit.position.set(destination)
			unit.carriedBy = None
	#
	
	def supplyWithAmmunition(self):
		self.ammunition = self.type.maxAmmunition
	#
	
	def repair(self, amount):
		previousHitpoints = self.hitpoints
		self.hitpoints = min(self.type.maxHitpoints, self.type.hitpoints + amount)
		return self.hitpoints - previousHitpoints
	#
	
	def attackUnit(self, target, didMove):
		if didMove and not self.type.canFireAfterMove:
			return False
		
		if self.unitWithinRange(target):
			self.__fireAtTarget(target)
			target.retaliate(self)
	#
	
	def retaliate(self, target):
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
	
	def applyDamage(self, damage):
		# Take cover into account - each cover point reduces incoming damage by 10%
		finalDamage = round(damage - (damage * self.field.getTerrainType(self.position).cover * 0.1))
		self.hitpoints = max(0, self.hitpoints - finalDamage)
	#
	
	def unitWithinRange(self, unit):
		manhattanDistance = manhattanDistance(self.position, unit.position)
		return manhattanDistance >= self.type.minRange and manhattanDistance <= self.type.maxRange
	#
	
	def alive(self):
		return self.hitpoints > 0
	#
	
	def canCombineWith(self, unit):
		# Same type, and at least one of them is damaged?
		return self.type is unit.type and (self.hitpoints < self.type.maxHitpoints or unit.hitpoints < unit.type.maxHitpoints)
	#
	
	def combineWith(self, unit):
		totalHitpoints = self.hitpoints + unit.hitpoints
		self.hitpoints = min(self.type.maxHitpoints, self.hitpoints + unit.hitpoints)
		self.ammunition = min(self.type.maxAmmunition, self.ammunition + unit.ammunition)
		# TODO: Take care of loaded units!!! Perhaps don't allow combining when units are carrying other units?
		
		return round(self.type.cost * (totalHitpoints - self.hitpoints) * 0.1)
	#
	
	def canCapture(self):
		return self.type.canCapture
	#
	
	def canSupply(self):
		return self.type.canSupply
	#
#