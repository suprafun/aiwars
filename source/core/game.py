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
		
		self.activePlayer = None
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
		return [p for p in self.players if p != player]
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
	
	# Starts the game, sets the first player to active
	def start(self):
		print 'Game started!'
		
		self.activePlayer = self.players[0]
		self.activePlayer.startTurn()
	#
	
	def playerHasLost(self, player):
		# TODO!
		print 'Player', player.name, 'has lost!'
	#
	
	def playerEndsTurn(self, player):
		print 'Player', player.name, 'turn has ended!'
		
		playerIndex = self.players.index(player)
		self.activePlayer = self.players[(playerIndex + 1) % len(self.players)]
		self.activePlayer.startTurn()
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
	
	
	def getFilteredSituationUpdateForPlayer(self, situationUpdate, player):
		# TODO: Filter the situation update by sight, keeping the previous unit/building states in mind for sight!
		# Step 1: determine sight for player according to old unit/building states.
		# Step 2: determine difference with current sight.
		# Step 3: check the unit/building updates in the given situation update - modify them according to sight.
		# Step 4: check if any previously seen units/buildings have now become invisible - add them as removed to the situation update.
		# Step 5: check if any units/buildings have become visible - add them as new to the situation update.
		
		return situationUpdate
	#
	
	
	# Clients can't alter the game-state directly, they have to send commands to the server and apply the situation updates they receive:
	def applySituationUpdate(self, situationUpdate):
		for playerUpdate in situationUpdate.playerUpdates.itervalues():
			player = playerUpdate.player
			player.money = playerUpdate.newMoneyAmount
			
			for unitUpdate in playerUpdate.unitUpdates:
				unit = player.getUnitByID(unitUpdate.unitID())
				if unitUpdate.oldUnit == None:
					player.addUnit(unitUpdate.newUnit)
				elif unitUpdate.newUnit == None:
					player.removeUnit(unit)
				else:
					unit.applyUnitUpdate(unitUpdate)
			
			for buildingUpdate in playerUpdate.buildingUpdates:
				building = player.getBuildingByID(buildingUpdate.buildingID())
				if buildingUpdate.oldBuilding == None:
					player.addBuilding(buildingUpdate.newBuilding)
				elif buildingUpdate.newBuilding == None:
					player.removeBuilding(building)
				else:
					building.applyBuildingUpdate(buildingUpdate)
	#
#