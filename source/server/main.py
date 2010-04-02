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
		
		self.clientPlayerControllers = []
		
		self.gameServer.listenForConnections(self.onClientConnected, 0.5)
	#
	
	def startGame(self):
		# TODO!
		pass
	#
	
	def onClientConnected(self, client):
		print 'client connected:', client, 'sending database and map data'
		client.sendMessage(STC_DATABASE_DATA, self.gameDatabase.toStream())
		client.sendMessage(STC_MAP_DATA, self.game.level.toStream())
	#
	
	def onClientSetsMode(self, client, message):
		if message == CLIENT_MODE_PLAYER:
			player = self.game.addPlayer('Unnamed player #' + str(client.id), client.id)
			self.clientPlayerControllers.append(ClientPlayerController(client, player))
			
			print 'Client #' + str(client.id) + ' sets mode to PLAYER'
		elif message == CLIENT_MODE_OBSERVER:
			player = self.game.getPlayerByID(client.id)
			if player != None:
				self.game.removePlayer(player)
			
			clientPlayerController = self.getClientPlayerControllerByID(client.id)
			if clientPlayerController != None:
				self.clientPlayerControllers.remove(clientPlayerController)
			
			# TODO: Register observer!!!
			print 'Client #' + str(client.id) + ' sets mode to OBSERVER'
		else:
			print 'Client #' + str(client.id) + ' sets mode to invalid mode!'
	#
	
	def onClientSetsName(self, client, message):
		(name, readBytesCount) = fromStream(message, str)
		clientPlayerController = self.getClientPlayerControllerByID(client.id)
		if clientPlayerController != None:
			clientPlayerController.name = name
		
		print 'Client #' + str(client.id) + ' sets name to ' + name
	#
	
	def onClientReady(self, client, message):
		clientPlayerController = self.getClientPlayerControllerByID(client.id)
		if clientPlayerController != None:
			clientPlayerController.setReady(True)
		
		print 'Client #' + str(client.id) + ' is READY!'
		
		if len(self.game.players) == self.game.level.getPlayersCount() and self.allPlayerClientsReady():
			print 'All clients are ready now!'
			self.gameServer.stopListeningForConnections()
			
			self.startGame()
	#
	
	
	def getClientPlayerControllerByID(self, clientPlayerControllerID):
		for clientPlayerController in self.clientPlayerControllers:
			if clientPlayerController.client.id == clientPlayerControllerID:
				return clientPlayerController
		return None
	#
	
	def allPlayerClientsReady(self):
		for clientPlayerController in self.clientPlayerControllers:
			if not clientPlayerController.isReady():
				return False
		return True
	#
#