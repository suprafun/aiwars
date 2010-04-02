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
		self.gameClient.connectToServer(host, port)
		self.gameClient.listenForData(self.onMessageReceivedFromServer)
	#
	
	def onMessageReceivedFromServer(self, messageType, message):
		print 'received message from server'
		
		if messageType == STC_DATABASE_DATA:
			print 'Database data received!'
		elif messageType == STC_MAP_DATA:
			print 'Map data received!'
			self.gameClient.sendMessageToServer(CTS_SET_NAME, toStream(self.name))
			self.gameClient.sendMessageToServer(CTS_SET_MODE, CLIENT_MODE_PLAYER)
	#
#