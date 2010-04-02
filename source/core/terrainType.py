

class TerrainType:
	def __init__(self, name, cover, movementCost, hideUnits = False):
		self.name = name                                # Terrain name, for example 'plains', or 'mountains'
		
		self.cover = cover                              # Cover value - every cover point reduces incoming damage by 10%
		self.movementCost = movementCost
		self.hideUnits = hideUnits
	#
#