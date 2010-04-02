from player import *
from messageTypes import *
from serialization import *
from point import *


resultToMessage = {ACTION_RESULT_SUCCESS: SERVER_RESULT_SUCCESS,
                   ACTION_RESULT_INVALID: SERVER_RESULT_INVALID,
                   ACTION_RESULT_TRAPPED: SERVER_RESULT_TRAPPED}


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
		
		self.player.addListener(self)
	#
	
	
	def onPlayerStartsTurn(self, player):
		self.client.sendMessage(STC_START_TURN, '')
	#
	
	def onPlayerEndsTurn(self, player):
		self.client.sendMessage(STC_END_TURN, '')
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
		(unitID, route, readBytesCount) = fromStream(message, int, list)
		route = self.__intListToPointList(route)
		
		result = self.player.moveUnit(unitID, route)
		self.client.sendMessage(STC_RESULT, resultToMessage[result])
	#
	
	def onUnloadCommand(self, message):
		(unitID, destinationX, destinationY, readBytesCount) = fromStream(message, int, int, int)
		destination = Point(destinationX, destinationY)
		
		result = self.player.unloadUnit(unitID, destination)
		self.client.sendMessage(STC_RESULT, resultToMessage[result])
	#
	
	def onSupplySurroundingUnitsCommand(self, message):
		(unitID, readBytesCount) = fromStream(message, int)
		
		result = self.player.supplySurroundingUnits(unitID)
		self.client.sendMessage(STC_RESULT, resultToMessage[result])
	#
	
	def onAttackUnitCommand(self, message):
		(unitID, targetID, readBytesCount) = fromStream(message, int, int)
		
		result = self.player.attackUnit(unitID, targetID)
		self.client.sendMessage(STC_RESULT, resultToMessage[result])
	#
	
	def onBuildUnitCommand(self, message):
		(buildingID, unitTypeID, readBytesCount) = fromStream(message, int, int)
		
		result = self.player.buildUnit(buildingID, unitTypeID)
		self.client.sendMessage(STC_RESULT, resultToMessage[result])
	#
	
	def onCaptureBuildingCommand(self, message):
		(unitID, readBytesCount) = fromStream(message, int)
		
		result = self.player.captureBuilding(unitID)
		self.client.sendMessage(STC_RESULT, resultToMessage[result])
	#
	
	def onHideUnitCommand(self, message):
		(unitID, hide, readBytesCount) = fromStream(message, int, bool)
		
		result = self.player.hideUnit(unitID, hide)
		self.client.sendMessage(STC_RESULT, resultToMessage[result])
	#
	
	def onEndTurnCommand(self, message):
		result = self.player.endTurn()
		self.client.sendMessage(STC_RESULT, resultToMessage[result])
	#
	
	def __intListToPointList(self, intList):
		pointList = []
		for i in xrange(0, len(intList), 2):
			pointList.append(Point(intList[i], intList[i + 1]))
		return pointList
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