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
	
	
	# Pre-game messages
	def onDatabaseData(self, message):
		print 'Database data received from server'
		self.gameDatabase.fromStream(message)
	#
	
	def onMapData(self, message):
		print 'Map data received from server'
		self.game.level.fromStream(message)
	#
	
	def onGameData(self, message):
		print 'Game data received from server'
		self.game.gameData.fromStream(message)
		
		self.gameClient.sendMessageToServer(CTS_SET_NAME, toStream(self.name))
		self.gameClient.sendMessageToServer(CTS_SET_MODE, CLIENT_MODE_PLAYER)
		self.gameClient.sendMessageToServer(CTS_READY, '')
	#
	
	def onStartGame(self, message):
		print 'Start the game!'
		
		# Stop listening for pre-game data
		self.gameClient.setCallbackForMessageType(STC_DATABASE_DATA, None)
		self.gameClient.setCallbackForMessageType(STC_MAP_DATA, None)
		self.gameClient.setCallbackForMessageType(STC_GAME_DATA, None)
		self.gameClient.setCallbackForMessageType(STC_START_GAME, None)
		
		# Start listening for game-specific messages
		self.gameClient.setCallbackForMessageType(STC_START_TURN, self.onStartTurn)
		self.gameClient.setCallbackForMessageType(STC_END_TURN, self.onEndTurn)
		self.gameClient.setCallbackForMessageType(STC_SITUATION_UPDATE, self.onSituationUpdate)
		self.gameClient.setCallbackForMessageType(STC_RESULT, self.onResult)
		self.gameClient.setCallbackForMessageType(STC_END_GAME, self.onEndGame)
	#
	
	
	# Game-specific messages
	def onStartTurn(self, message):
		print 'Starting turn!'
		pass
	#
	
	def onEndTurn(self, message):
		print 'Turn has ended!'
		pass
	#
	
	def onSituationUpdate(self, message):
		print 'Situation update!'
		pass
	#
	
	def onResult(self, message):
		print 'Result: ' + {SERVER_RESULT_SUCCESS: 'success', SERVER_RESULT_TRAPPED: 'trapped', SERVER_RESULT_INVALID: 'invalid', SERVER_RESULT_NOT_YOUR_TURN: 'not your turn'}[message]
		pass
	#
	
	def onEndGame(self, message):
		print 'Game has ended!'
		pass
	#
#