import sys
from core.game import *
from core.gameDatabase import *
from core.gameServer import *
from core.messageTypes import *
from core.serialization import *
from core.clientPlayerController import *


class Main(object):
	def __init__(self, host, port, levelfile, databasefile):
		self.gameDatabase = GameDatabase();
		self.gameDatabase.loadFromFile('../databases/' + databasefile)
		
		self.game = Game(self.gameDatabase)
		self.game.loadLevelFromFile('../levels/' + levelfile)
		
		self.gameServer = GameServer(host, port)
		self.gameServer.setCallbackForMessageType(CTS_SET_MODE, self.onClientSetsMode)
		self.gameServer.setCallbackForMessageType(CTS_SET_NAME, self.onClientSetsName)
		self.gameServer.setCallbackForMessageType(CTS_READY, self.onClientReady)
		
		self.controllers = {}
		self.playerControllers = []
		self.observerControllers = []
		
		self.gameServer.listenForConnections(self.onClientConnected, 0.5)
	#
	
	def startGame(self):
		print 'Starting the game!'
		
		# Ignore mode, name and ready messages during the game!
		self.gameServer.setCallbackForMessageType(CTS_SET_MODE, None)
		self.gameServer.setCallbackForMessageType(CTS_SET_NAME, None)
		self.gameServer.setCallbackForMessageType(CTS_READY, None)
		
		# Listen for game-specific messages
		self.gameServer.setCallbackForMessageType(CTS_MOVE_UNIT, self.onClientMoveCommand)
		self.gameServer.setCallbackForMessageType(CTS_UNLOAD_UNIT, self.onClientUnloadCommand)
		self.gameServer.setCallbackForMessageType(CTS_SUPPLY_SURROUNDING_UNITS, self.onClientSupplySurroundingUnitsCommand)
		self.gameServer.setCallbackForMessageType(CTS_ATTACK_UNIT, self.onClientAttackUnitCommand)
		self.gameServer.setCallbackForMessageType(CTS_BUILD_UNIT, self.onClientBuildUnitCommand)
		self.gameServer.setCallbackForMessageType(CTS_CAPTURE_BUILDING, self.onClientCaptureBuildingCommand)
		self.gameServer.setCallbackForMessageType(CTS_HIDE_UNIT, self.onClientHideUnitCommand)
		self.gameServer.setCallbackForMessageType(CTS_END_TURN, self.onClientEndTurnCommand)
		
		for controller in self.playerControllers:
			controller.startGame('')
		
		# TODO!
		# NOTE: the client threads will keep the server alive... should we enter a busy loop here or join those threads?
		pass
	#
	
	def readyPlayersCount(self):
		readyPlayers = 0
		for controller in self.playerControllers:
			if controller.ready:
				readyPlayers += 1
		return readyPlayers
	#
	
	
	# Lobby message handling
	def onClientConnected(self, client):
		print 'client connected:', client, 'sending database and map data'
		
		controller = ClientPlayerController(client)
		self.controllers[client] = controller
		self.observerControllers.append(controller)
		
		controller.sendDatabaseData(self.gameDatabase.toStream())
		controller.sendMapData(self.game.level.toStream())
		controller.sendGameData(self.game.gameData.toStream())
	#
	
	def onClientSetsMode(self, client, message):
		controller = self.controllers[client]
		controller.onSetModeCommand(message)
		
		# Place the controller in the correct list
		if controller.isObserving and controller not in self.observerControllers:
			self.playerControllers.remove(controller)
			self.observerControllers.append(controller)
		elif not controller.isObserving and controller not in self.playerControllers:
			self.observerControllers.remove(controller)
			self.playerControllers.append(controller)
	#
	
	def onClientSetsName(self, client, message):
		self.controllers[client].onSetNameCommand(message)
	#
	
	def onClientReady(self, client, message):
		controller = self.controllers[client]
		controller.onSetReadyCommand(message)
		
		# TODO: What to do with additional players who haven't sent the ready signal yet? How about possible threading issues here?
		if self.readyPlayersCount() == self.game.level.getPlayersCount():
			self.gameServer.stopListeningForConnections()
			self.startGame()
	#
	
	
	# Game message handling
	def onClientMoveCommand(self, client, message):
		self.controllers[client].onMoveCommand(message)
	#
	
	def onClientUnloadCommand(self, client, message):
		self.controllers[client].onUnloadCommand(message)
	#
	
	def onClientSupplySurroundingUnitsCommand(self, client, message):
		self.controllers[client].onSupplySurroundingUnitsCommand(message)
	#
	
	def onClientAttackUnitCommand(self, client, message):
		self.controllers[client].onAttackUnitCommand(message)
	#
	
	def onClientBuildUnitCommand(self, client, message):
		self.controllers[client].onBuildUnitCommand(message)
	#
	
	def onClientCaptureBuildingCommand(self, client, message):
		self.controllers[client].onCaptureBuildingCommand(message)
	#
	
	def onClientHideUnitCommand(self, client, message):
		self.controllers[client].onHideUnitCommand(message)
	#
	
	def onClientEndTurnCommand(self, client, message):
		self.controllers[client].onEndTurnCommand(message)
	#
#