from level import *
from player import *


class Game(object):
	def __init__(self, gameDatabase):
		self.gameDatabase = gameDatabase
		self.level = Level(self.gameDatabase)
		
		# TODO: Add more game options?
		self.fogOfWar = False
		
		self.players = []
		self.observers = []
	#
	
	def addPlayer(self, name):
		player = Player(self, name)
		self.players.append(player)
		return player
	#
	
	def getOtherPlayers(self, player):
		otherPlayers = []
		for otherPlayer in self.players:
			if otherPlayer is not player:
				otherPlayers.append(otherPlayer)
		return otherPlayers
	#
	
	def getAllPlayers(self):
		return self.players
	#
	
	def playerHasLost(self, player):
		# TODO!
		print 'Player', player.name, 'has lost!'
	#
	
	# TODO!!!
	def addObserver(self, observer):
		self.observers.append(observer)
	#
	
	def loadLevelFromFile(self, filename):
		self.level.loadFromFile(filename)
	#
#