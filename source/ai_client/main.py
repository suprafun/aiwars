import sys
from core.game import *
from core.gameDatabase import *
from core.gameClient import *


class Main(object):
	def __init__(self, host, port, name):
		self.name = name
		
		self.gameDatabase = GameDatabase();
		self.game = Game(self.gameDatabase)
		
		self.gameClient = GameClient()
		self.gameClient.connectToServer(host, port)
		self.gameClient.listenForData(self.onDataReceivedFromServer)
	#
	
	def onDataReceivedFromServer(self, data):
		print 'received data from server:', data
		self.gameClient.sendMessageToServer('Thanks from ' + self.name)
	#
#