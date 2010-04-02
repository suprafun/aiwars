

class BuildingType:
	def __init__(self, name, texture, income, availableUnitTypes = [], maxCapturePoints = 20):
		self.name = name
		self.texture = texture
		
		self.income = income
		self.availableUnitTypes = availableUnitTypes
		self.maxCapturePoints = maxCapturePoints
	#
	
	def canBuild(self, unitType):
		return self.availableUnitTypes.count(unitType) > 0
	#
#