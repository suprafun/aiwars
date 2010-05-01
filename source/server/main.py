import sys
from core.game import *
from core.gameDatabase import *
from core.gameServer import *
from core.messageTypes import *
from core.serialization import *
from core.clientPlayerController import *
from core.guid import *
from core.situationUpdate import *
from clientPlayerCheck import *


class Main(object):
	def __init__(self, host, port, levelfile, databasefile):
		self.gameDatabase = GameDatabase()
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
		
		self.startGame()
	#
	
	def startGame(self):
		print 'Starting the game!'
		
		# Ignore mode, name and ready messages during the game!
		self.gameServer.setCallbackForMessageType(CTS_SET_MODE, None)
		self.gameServer.setCallbackForMessageType(CTS_SET_NAME, None)
		self.gameServer.setCallbackForMessageType(CTS_READY, None)
		
		# Listen for game-specific messages - the callbacks are wrapped in a small class that checks if the clients player is the active player, so the real callback will not be called
		# if a client sends messages while it's not it's turn. The client will receive a SERVER_RESULT_NOT_YOUR_TURN message in that case.
		# The player controllers will 
		self.gameServer.setCallbackForMessageType(CTS_MOVE_UNIT, ClientPlayerCheck(self, self.onClientMoveCommand))
		self.gameServer.setCallbackForMessageType(CTS_UNLOAD_UNIT, ClientPlayerCheck(self, self.onClientUnloadCommand))
		self.gameServer.setCallbackForMessageType(CTS_SUPPLY_SURROUNDING_UNITS, ClientPlayerCheck(self, self.onClientSupplySurroundingUnitsCommand))
		self.gameServer.setCallbackForMessageType(CTS_ATTACK_UNIT, ClientPlayerCheck(self, self.onClientAttackUnitCommand))
		self.gameServer.setCallbackForMessageType(CTS_BUILD_UNIT, ClientPlayerCheck(self, self.onClientBuildUnitCommand))
		self.gameServer.setCallbackForMessageType(CTS_CAPTURE_BUILDING, ClientPlayerCheck(self, self.onClientCaptureBuildingCommand))
		self.gameServer.setCallbackForMessageType(CTS_HIDE_UNIT, ClientPlayerCheck(self, self.onClientHideUnitCommand))
		self.gameServer.setCallbackForMessageType(CTS_END_TURN, ClientPlayerCheck(self, self.onClientEndTurnCommand))
		
		# Add players to the game:
		for controller in self.playerControllers:
			if controller.ready:
				player = self.game.addPlayer(controller.name, getGUID())
				
				playerNumber = len(self.game.players) - 1
				for building in self.game.level.getBuildingsForPlayerNumber(playerNumber):
					player.addBuilding(building)
				
				# TODO: Add existing units - for pre-deployed scenarios!
				for unit in self.game.level.getUnitsForPlayerNumber(playerNumber):
					player.addUnit(unit)
				
				controller.setPlayer(player)
		
		# Send start-game messages to all clients:
		playerData = toStream(len(self.game.getAllPlayers()))
		for player in self.game.getAllPlayers():
			playerData += player.toStream(False)
		
		for controller in self.playerControllers:
			controller.startGame(toStream(controller.player.id) + playerData)
		
		for controller in self.observerControllers:
			controller.startGame(toStream(0) + playerData)
		
		# Create the initial situation update:
		situationUpdate = SituationUpdate(self.game)
		for player in self.game.players:
			for unit in player.units:
				situationUpdate.addUnitCreationForPlayer(player, unit)
			for building in player.buildings:
				situationUpdate.addBuildingCreationForPlayer(player, building)
		
		# Send initial situation-updates to all clients (player clients get filtered messages, based on their vision)
		for controller in self.observerControllers:
			controller.sendSituationUpdate(situationUpdate.toStream(False))
		
		for controller in self.playerControllers:
			print 'Sending filtered sit. update to player', controller.player.id
			filteredSituationUpdate = self.game.getFilteredSituationUpdateForPlayer(situationUpdate, controller.player)
			controller.sendSituationUpdate(filteredSituationUpdate.toStream(self.game.gameData.fogOfWar))
		
		self.game.start()
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
	
	
	# Replies
#