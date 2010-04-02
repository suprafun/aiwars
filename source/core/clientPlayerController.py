from messageTypes import *
from serialization import *


class ClientPlayerController(object):
	def __init__(self, client):
		self.client = client
		
		self.isObserving = True
		
		self.name = ''
		self.player = None
		self.ready = False
	#
	
	def setPlayer(self, player):
		self.player = player
	#
	
	
	#================================================================================
	# Messages received from the client
	
	# Before the game has started, self.player is still None, so 
	def onSetNameCommand(self, message):
		(name, readBytesCount) = fromStream(message, str)
		self.name = name
		
		print 'Client', self.client, 'set name to [' + self.name +']'
	#
	
	def onSetModeCommand(self, message):
		self.isObserving = (message == CLIENT_MODE_OBSERVER)
		
		modestr = 'player'
		if self.isObserving:
			modestr = 'observer'
		print 'Client', self.client, 'set mode to', modestr
	#
	
	def onSetReadyCommand(self, message):
		self.ready = True
		
		print 'Client', self.client, 'is ready!'
	#
	
	
	# Translate messages sent by the client into player commands
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
	
	
	#================================================================================
	# Server-side actions, send message to the client
	
	def sendDatabaseData(self, message):
		self.client.sendMessage(STC_DATABASE_DATA, message)
	#
	
	def sendMapData(self, message):
		self.client.sendMessage(STC_MAP_DATA, message)
	#
	
	def sendGameData(self, message):
		self.client.sendMessage(STC_GAME_DATA, message)
	#
	
	def startGame(self, message):
		self.client.sendMessage(STC_START_GAME, message)
	#
	
	# Player-specific
	
	
	# Observer-specific
#