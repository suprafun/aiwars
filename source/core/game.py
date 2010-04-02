from gameData import *
from level import *
from player import *


class Game(object):
	def __init__(self, gameDatabase):
		self.gameDatabase = gameDatabase
		self.gameData = GameData(False)
		self.level = Level(self, self.gameDatabase)
		
		self.players = []
		self.observers = []
	#
	
	def addPlayer(self, name, id):
		player = Player(self, name, id)
		self.players.append(player)
		return player
	#
	
	def removePlayer(self, player):
		if player in self.players:
			self.players.remove(player)
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
	
	def getPlayerByID(self, playerID):
		for player in self.players:
			if player.id == playerID:
				return player
		return None
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
	
	
	def getUnitByID(self, unitID):
		for player in self.players:
			unit = player.getUnitByID(unitID)
			if unit != None:
				return unit
		return None
	#
	
	def getBuildingByID(self, buildingID):
		return self.level.getBuildingByID(buildingID)
	#
#