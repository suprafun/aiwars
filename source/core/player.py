from unit import *
from building import *


class Player(object):
	def __init__(self, name):
		self.name = name
		
		self.money = 0
		self.buildings = []
		self.units = []
		
		# Keep track of what actions units can still perform - at the start of each turn, all units are placed in the __activeUnits list.
		# Units that have moved are moved to the __movedUnits list.
		# Units that were trapped during movement, or that have taken an action (firing, unloading, loading, supplying, etc.) are placed in the __finishedUnits list.
		self.__activeUnits = []
		self.__movedUnits = []
		self.__finishedUnits = []
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
	
	
	def startTurn(self):
		for building in self.buildings:
			self.money += building.type.income
		
		self.__activeUnits = self.units[:]
		self.__movedUnits = []
		self.__finishedUnits = []
	#
	
	def moveUnit(self, unit, route):
		if unit in self.__activeUnits:
			
#