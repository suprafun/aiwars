from level import *


class Game(object):
	def __init__(self, gameDatabase):
		self.gameDatabase = gameDatabase
		self.level = Level(self.gameDatabase)
		
		# TODO: Add more game options?
		self.fogOfWar = False
		
		self.players = []
		self.observers = []
	#
	
	def addPlayer(self, player):
		self.players.append(player)
	#
	
	def addObserver(self, observer):
		self.observers.append(observer)
	#
	
	def loadLevelFromFile(self, filename):
		self.level.loadFromFile(filename)
	#
#