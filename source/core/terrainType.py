

class TerrainType(object):
	def __init__(self, name, cover, movementCost, hideUnits = False, buildingType = None):
		self.name = name                                # Terrain name, for example 'plains', or 'mountains'
		
		self.cover = cover                              # Cover value - every cover point reduces incoming damage by 10%
		self.movementCost = movementCost                # Most terrain will cost one point per tile, but difficult terrain can cost more, so units can travel less far.
		self.hideUnits = hideUnits                      # Some dense terrain types will hide units in fog-of-war mode.
		
		self.buildingType = buildingType                # Some terrain types are associated to buildings. For example: cities, bases, headquarters...
	#
#