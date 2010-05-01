

class LevelPlayerData(object):
	def __init__(self):
		self.buildings = []
		self.units = []
	#
	
	def addBuilding(self, building):
		self.buildings.append(building)
	#
	
	def addUnit(self, unit):
		self.units.append(unit)
	#
#