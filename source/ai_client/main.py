import sys
from core.game import *
from core.gameDatabase import *
from core.gameClient import *

from core.messageTypes import *
from core.serialization import *


class Main(object):
	def __init__(self, host, port, name):
		self.name = name
		
		self.gameDatabase = GameDatabase();
		self.game = Game(self.gameDatabase)
		
		self.gameClient = GameClient()
		self.gameClient.setCallbackForMessageType(STC_DATABASE_DATA, self.onDatabaseData)
		self.gameClient.setCallbackForMessageType(STC_MAP_DATA, self.onMapData)
		self.gameClient.setCallbackForMessageType(STC_GAME_DATA, self.onGameData)
		self.gameClient.setCallbackForMessageType(STC_START_GAME, self.onStartGame)
		
		self.gameClient.connectToServer(host, port, 30)
		self.gameClient.listenForData()
	#
	
	def onDatabaseData(self, message):
		print 'Database data received from server'
		self.gameDatabase.fromStream(message)
	#
	
	def onMapData(self, message):
		print 'Map data received from server'
		self.game.level.fromStream(message)
		
		self.gameClient.sendMessageToServer(CTS_SET_NAME, toStream(self.name))
		self.gameClient.sendMessageToServer(CTS_SET_MODE, CLIENT_MODE_PLAYER)
	#
	
	def onGameData(self, message):
		print 'Game data received from server'
		pass
	#
	
	def onStartGame(self, message):
		print 'Start the game!'
		pass
	#
#