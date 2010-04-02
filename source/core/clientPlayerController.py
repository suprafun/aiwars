from messageTypes import *
from serialization import *


class ClientPlayerController(object):
	def __init__(self, client, player):
		self.client = client
		self.player = player
		
		self.ready = False
	#
	
	def setReady(self, ready):
		self.ready = ready
	#
	
	def isReady(self):
		return self.ready
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