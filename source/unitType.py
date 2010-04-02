

class UnitType:
	def __init__(self, name, texture, cost, movementPoints, vision, maxAmmunition, maxHitpoints = 10, minRange = 1, maxRange = 1, canFireAfterMove = True, canRetaliate = True, canSupply = False, canCapture = False, maxTransportSlots = 0):
		self.name = name                                # This type's name, for example 'tank', or 'attack helicopter'.
		self.texture = texture                          # This type's texture.
		self.cost = cost                                # How expensive this unit type is to construct.
		self.movementPoints = movementPoints            # How many movement points this unit has (some tiles take cost points to cross than others).
		self.vision = vision                            # How far this unit can see.
		self.maxHitpoints = maxHitpoints                # Maximum number of hitpoints. Usually 10.
		
		self.primaryDamage = {}                         # Primary damage dealt against other unit types, uses ammunition.
		self.secondaryDamage = {}                       # Secondary damage dealt against other unit types, uses no ammunition.
		self.maxAmmunition = maxAmmunition              # Maximum ammunition for primary weapon.
		
		self.minRange = minRange                        # Minimum range (1 for assault units, usually a little higher for artillery)
		self.maxRange = maxRange                        # Maximum range (1 for assault units, usually much higher for artillery)
		self.canFireAfterMove = canFireAfterMove	    # Whether this unit can fire after moving. Usually false for artillery.
		self.canRetaliate = canRetaliate                # Some units fire back after being attacked. Usually only assault units.
		
		self.movementCostOverride = {}                  # Override cost for specific terrain types. For example, aerial units can override all terrain types with a cost of 1.
		self.visionOverride = {}                        # Some terrain types can affect sight, for example tall mountains can increase sight.
		
		self.canSupply = canSupply                      # Can this unit supply surrounding units with ammunition?
		self.canCapture = canCapture                    # Can this unit capture buildings?
		
		self.transports = {}                            # The unit types that can be transported, and how much room they occupy.
		self.maxTransportSlots = maxTransportSlots      # Maximum transport capacity (some units can take up multiple slots).
	#
	
	def setDamageAgainst(self, unitType, primaryDamage, secondaryDamage)
		self.primaryDamage[unitType] = primaryDamage
		self.secondaryDamage[unitType] = secondaryDamage
	#
	
	def overrideMovementCostForTerrainType(self, terrainType, movementCost):
		self.movementCostOverride[terrainType] = movementCost
	#
	
	def overrideSightForTerrainType(self, terrainType, sightOverride):
		self.visionOverride[terrainType] = sightOverride
	#
	
	def canTransport(self, unitType, slots):
		self.transports[unitType] = slots
	#
	
	
	def movementCostFor(self, terrainType):
		if self.movementCostOverride.contains(terrainType):
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
#