from messageTypes import *
from serialization import *


class ClientPlayerController(object):
	def __init__(self, player):
		self.player = player
	#
	
	def onMoveCommand(self, message):
		pass
	#
	
	def onUnloadCommand(self, message):
		pass
	#
	
	def onSupplySurroundingUnitsCommand(self, message):
		pass
	#
	
	def onAttackUnitCommand(self, message):
		pass
	#
	
	def onBuildUnitCommand(self, message):
		pass
	#
	
	def onCaptureBuildingCommand(self, message):
		pass
	#
	
	def onHideUnitCommand(self, message):
		pass
	#
	
	def onEndTurnCommand(self, message):
		pass
	#
#