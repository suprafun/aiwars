

class TerrainType:
	def __init__(self, name, cover, movementCost, hideUnits = False):
		self.name = name
		
		self.cover = cover
		self.movementCost = movementCost
		self.hideUnits = hideUnits
	#
#