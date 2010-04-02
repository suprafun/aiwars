from terrainType import *


class Field:
	def __init__(self):
		self.terrain = [[]]
	#
	
	def getTerrainType(self, point):
		return self.terrain[point.y][point.x]
	#
#