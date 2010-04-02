

class TerrainType:
	def __init__(self, name, texture, cover, movementCost, hideUnits = False):
		self.name = name
		self.texture = texture
		
		self.cover = cover
		self.movementCost = movementCost
		self.hideUnits = hideUnits
	#
#