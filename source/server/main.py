import sys
from core.game import *
from core.gameDatabase import *
from core.gameServer import *

from core.messageTypes import *


class Main(object):
	def __init__(self, host, port, levelfile, databasefile):
		self.gameDatabase = GameDatabase();
		self.gameDatabase.loadFromFile('../databases/' + databasefile)
		
		self.game = Game(self.gameDatabase)
		self.game.loadLevelFromFile('../levels/' + levelfile)
		
		self.gameServer = GameServer(host, port)
		self.gameServer.onClientConnected = self.onClientConnected
		self.gameServer.onDataReceivedFromClient = self.onDataReceivedFromClient
		self.gameServer.listenForConnections()
	#
	
	def onClientConnected(self, client):
		print 'client connected:', client, 'sending database and map data'
		client.sendMessage(STC_DATABASE_DATA + self.gameDatabase.toStream())
		client.sendMessage(STC_MAP_DATA + self.game.level.toStream())
	#
	
	def onDataReceivedFromClient(self, client, data):
		print 'client', client, 'has sent data:', data
	#
#