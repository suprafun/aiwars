import sys
from core.game import *
from core.gameDatabase import *
from core.gameClient import *
from core.messageTypes import *
from core.serialization import *


class Main(object):
	def __init__(self, host, port, name):
		self.name = name
		self.playerID = 0
		self.myTurn = False
		
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
		self.playerID, playerCount, totalReadBytes = fromStream(message, int, int)
		for i in xrange(playerCount):
			# TODO: Change game.addPlayer to accept a Player object instead of a name and id!
			player = Player(self.game, '', 0)
			totalReadBytes += player.fromStream(message[totalReadBytes:])
			self.game.addPlayer(player.name, player.id)
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
		(playerID, readBytes) = fromStream(message, int)
		self.game.activePlayer = self.game.getPlayerByID(playerID)
		
		self.myTurn = self.playerID == playerID
	#
	
	def onEndTurn(self, message):
		print 'Turn has ended!'
		
		self.myTurn = False
	#
	
	def onSituationUpdate(self, message):
		situationUpdate = SituationUpdate(self.game)
		situationUpdate.fromStream(message)
		
		self.game.applySituationUpdate(situationUpdate)
		
		print 'Received situation update. Current situation is now:'
		self.printSituation()
		
		if self.myTurn:
			print '\nExecute code on self.game.activePlayer.:'
			codeString = raw_input('Run code:')
			print eval('self.game.activePlayer.' + codeString)
	#
	
	def onResult(self, message):
		print 'Result: ' + {SERVER_RESULT_SUCCESS: 'success', SERVER_RESULT_TRAPPED: 'trapped', SERVER_RESULT_INVALID: 'invalid', SERVER_RESULT_NOT_YOUR_TURN: 'not your turn'}[message]
		pass
	#
	
	def onEndGame(self, message):
		print 'Game has ended!'
		pass
	#
	
	
	# Debug functions
	def printSituation(self):
		for player in self.game.players:
			selfString = '' if player.id != self.playerID else ' (MYSELF)'
			print 'Player #' + str(player.id) + ' (' + player.name + ')' + selfString + ' has $' + str(player.money) + '.'
			print 'Buildings:'
			for building in player.buildings:
				print '\t' + building.type.name + ' #' + str(building.id) + ' at ' + str(building.position) + ', has ' + str(building.capturePoints) + ' capture points.'
			print 'Units:'
			for unit in player.units:
				print '\t' + unit.type.name + ' #' + str(unit.id) + ' at ' + str(unit.position) + ', has ' + str(unit.hitpoints) + ' hitpoints.'
	#
#