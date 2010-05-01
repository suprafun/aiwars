from serialization import *


class UnitType(object):
	def __init__(self, name, cost, movementPoints, vision, maxAmmunition, maxHitpoints = 10, minRange = 1, maxRange = 1, canActAfterMoving = True, canRetaliate = True, canSupply = False, canCapture = False, canHide = False):
		self.gameDatabase = None
		
		self.name = name                                # This type's name, for example 'tank', or 'attack helicopter'.
		self.cost = cost                                # How expensive this unit type is to construct.
		self.movementPoints = movementPoints            # How many movement points this unit has (some tiles cost more points to cross than others).
		self.vision = vision                            # How far this unit can see.
		self.stealthDetectionRange = 1					# Stealth detection range - 1 by default. Scanners could have a higher range
		self.maxHitpoints = maxHitpoints                # Maximum number of hitpoints. Usually 10.
		
		self.primaryDamage = {}                         # Primary damage dealt against other unit types, uses ammunition.
		self.secondaryDamage = {}                       # Secondary damage dealt against other unit types, uses no ammunition.
		self.maxAmmunition = maxAmmunition              # Maximum ammunition for primary weapon.
		
		self.minRange = minRange                        # Minimum range (1 for assault units, usually a little higher for artillery)
		self.maxRange = maxRange                        # Maximum range (1 for assault units, usually much higher for artillery)
		self.canActAfterMoving = canActAfterMoving	    # Whether this unit can perform actions after moving. Attacking, supplying, etc, are all actions. Usually False for artillery.
		self.canRetaliate = canRetaliate                # Some units fire back after being attacked. Usually only assault units.
		
		self.movementCostOverride = {}                  # Override cost for specific terrain types. For example, aerial units can override all terrain types with a cost of 1.
		self.visionOverride = {}                        # Some terrain types can affect sight, for example tall mountains can increase sight.
		
		self.canSupply = canSupply                      # Can this unit supply surrounding units with ammunition?
		self.canCapture = canCapture                    # Can this unit capture buildings?
		self.canHide = canHide                          # Can this unit hide anywhere? (a submarine can submerge itself)
		
		self.transports = {}                            # The unit types that can be transported, and how much room they occupy.
		self.maxTransportSlots = 0                      # Maximum transport capacity (some units can take up multiple slots).
		
		# TODO: Add fuel capacity, fuel usage per turn and needs-fuel-to-stay-alive flag!
	#
	
	def setDamageAgainst(self, unitType, primaryDamage, secondaryDamage):
		self.primaryDamage[unitType] = primaryDamage
		self.secondaryDamage[unitType] = secondaryDamage
	#
	
	def overrideMovementCostForTerrainType(self, terrainType, movementCost):
		self.movementCostOverride[terrainType] = movementCost
	#
	
	def overrideVisionForTerrainType(self, terrainType, sightOverride):
		self.visionOverride[terrainType] = sightOverride
	#
	
	def canTransport(self, unitType, slots):
		self.transports[unitType] = slots
	#
	
	def setMaximumTransportSlots(self, maxTransportSlots):
		self.maxTransportSlots = maxTransportSlots
	#
	
	
	def movementCostFor(self, terrainType):
		if self.movementCostOverride.has_key(terrainType):
			return self.movementCostOverride[terrainType]
		else:
			return terrainType.movementCost
	#
	
	def visionOn(self, terrainType):
		if self.sightOverride.contains(terrainType):
			return self.visionOverride[terrainType]
		else:
			return self.vision
	#
	
	def primaryDamageAgainst(self, unitType):
		return self.primaryDamage[unitType]
	#
	
	def secondaryDamageAgainst(self, unitType):
		return self.secondaryDamage[unitType]
	#
	
	
	# Serialization
	def toStream(self):
		return toStream(self.name, \
		                self.cost, \
		                self.movementPoints, \
		                self.vision, \
		                self.maxHitpoints, \
		                self.__dictionaryToList(self.primaryDamage, self.gameDatabase.getIndexOfUnitType), \
		                self.__dictionaryToList(self.secondaryDamage, self.gameDatabase.getIndexOfUnitType), \
		                self.maxAmmunition, \
		                self.minRange, \
		                self.maxRange, \
		                self.canActAfterMoving, \
		                self.canRetaliate, \
		                self.__dictionaryToList(self.movementCostOverride, self.gameDatabase.getIndexOfTerrainType), \
		                self.__dictionaryToList(self.visionOverride, self.gameDatabase.getIndexOfTerrainType), \
		                self.canSupply, \
		                self.canCapture, \
		                self.canHide, \
		                self.__dictionaryToList(self.transports, self.gameDatabase.getIndexOfUnitType), \
		                self.maxTransportSlots)
	#
	
	def __dictionaryToList(self, dictionary, getIndexFunction):
		listOutput = []
		for key in dictionary:
			listOutput.extend([getIndexFunction(key), dictionary[key]])
		return listOutput
	#
	
	def fromStream(self, stream):
		(self.name, \
		 self.cost, \
		 self.movementPoints, \
		 self.vision, \
		 self.maxHitpoints, \
		 self.primaryDamage, \
		 self.secondaryDamage, \
		 self.maxAmmunition, \
		 self.minRange, \
		 self.maxRange, \
		 self.canActAfterMoving, \
		 self.canRetaliate, \
		 self.movementCostOverride, \
		 self.visionOverride, \
		 self.canSupply, \
		 self.canCapture, \
		 self.canHide, \
		 self.transports, \
		 self.maxTransportSlots, \
		 readBytesCount) = fromStream(stream, str, int, int, int, int, list, list, int, int, int, bool, bool, list, list, bool, bool, bool, list, int)
		
		return readBytesCount
	#
	
	def fromStreamPostProcess(self):
		self.primaryDamage = self.__listToDictionary(self.primaryDamage, self.gameDatabase.getUnitType)
		self.secondaryDamage = self.__listToDictionary(self.secondaryDamage, self.gameDatabase.getUnitType)
		
		self.movementCostOverride = self.__listToDictionary(self.movementCostOverride, self.gameDatabase.getTerrainType)
		self.visionOverride = self.__listToDictionary(self.visionOverride, self.gameDatabase.getTerrainType)
		
		self.transports = self.__listToDictionary(self.transports, self.gameDatabase.getUnitType)
	#
	
	def __listToDictionary(self, _list, getTypeFunction):
		dictionaryOutput = {}
		for i in xrange(0, len(_list), 2):
			index = _list[i]
			value = _list[i + 1]
			dictionaryOutput[getTypeFunction(index)] = value
		return dictionaryOutput
	#
#