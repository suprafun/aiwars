from unit import *
from building import *


class Player(object):
	def __init__(self):
		self.buildings = []
		self.units = []
	#
	
	def getBuildingByID(self, buildingID):
		for building in self.buildings:
			if building.id == buildingID:
				return building
		return None
	#
	
	def getUnitByID(self, unitID):
		for unit in self.units:
			if unit.id == unitID:
				return unit
		return None
	#
#