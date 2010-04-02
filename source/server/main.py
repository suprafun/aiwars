import sys
from core.game import *
from core.gameDatabase import *
from core.gameServer import *

from core.messageTypes import *
from core.serialization import *


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
		
		self.gameServer.listenForConnections(self.onClientConnected)
	#
	
	def onClientConnected(self, client):
		print 'client connected:', client, 'sending database and map data'
		client.sendMessage(STC_DATABASE_DATA, self.gameDatabase.toStream())
		client.sendMessage(STC_MAP_DATA, self.game.level.toStream())
	#
	
	def onClientSetsMode(self, client, message):
		if message == CLIENT_MODE_PLAYER:
			print 'Client #' + str(client.id) + ' sets mode to PLAYER'
		elif message == CLIENT_MODE_OBSERVER:
			print 'Client #' + str(client.id) + ' sets mode to OBSERVER'
		else:
			print 'Client #' + str(client.id) + ' sets mode to invalid mode!'
	#
	
	def onClientSetsName(self, client, message):
		(name, readBytesCount) = fromStream(message, str)
		print 'Client #' + str(client.id) + ' sets name to ' + name
	#
	
	def onClientReady(self, client, message):
		print 'Client #' + str(client.id) + ' is READY!'
	#
#