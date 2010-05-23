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
		oldVisibilityMap = player.getOldVisibilityMapForSituationUpdate(situationUpdate)
		newVisibilityMap = player.getVisibilityMap()
		
		filteredSituationUpdate = SituationUpdate(situationUpdate.game)
		
		# A player can always see changes to it's own units and buildings
		if situationUpdate.playerUpdates.has_key(player):
			filteredSituationUpdate.playerUpdates[player] = situationUpdate.playerUpdates[player]
		
		# Check the units and buildings for the other players, taking any changes into account, and check which part of these updates are visible to the player.
		for otherPlayer in self.getOtherPlayers(player):
			otherPlayerUpdate = None
			if situationUpdate.playerUpdates.has_key(otherPlayer):
				otherPlayerUpdate = situationUpdate.playerUpdates[otherPlayer]
			
			# First, create a dictionary for all units, that maps their ID to a (oldUnit, newUnit) tuple. If a unit has not been modified,
			# both oldUnit and newUnit will refer to the same Unit.
			unitComparisons = {}
			for unit in otherPlayer.units:
				unitComparisons[unit.id] = (unit, unit)
			if otherPlayerUpdate:
				for unitUpdate in otherPlayerUpdate.unitUpdates:
					unitComparisons[unitUpdate.unitID()] = (unitUpdate.oldUnit, unitUpdate.newUnit)
			
			# The same goes for buildings.
			buildingComparisons = {}
			for building in otherPlayer.buildings:
				buildingComparisons[building.id] = (building, building)
			if otherPlayerUpdate:
				for buildingUpdate in otherPlayerUpdate.buildingUpdates:
					buildingComparisons[buildingUpdate.buildingID()] = (buildingUpdate.oldBuilding, buildingUpdate.newBuilding)
			
			# Check which units have changed, from this players point of view
			for oldUnit, newUnit in unitComparisons.itervalues():
				wasVisible = (oldUnit != None and oldVisibilityMap.unitIsVisible(oldUnit))
				isVisible = (newUnit != None and newVisibilityMap.unitIsVisible(newUnit))
				
				# If the unit's visibility has changed, or, if it has stayed visible but has also been modified, include it in the situation update
				if wasVisible != isVisible or (wasVisible and isVisible and newUnit != oldUnit):
					if not wasVisible:
						filteredSituationUpdate.addUnitCreationForPlayer(otherPlayer, newUnit)
					elif not isVisible:
						filteredSituationUpdate.addUnitRemovalForPlayer(otherPlayer, oldUnit)
					else:
						unitUpdate = filteredSituationUpdate.addUnitUpdateForPlayer(otherPlayer, oldUnit)
						unitUpdate.newUnit = newUnit
			
			# The same goes for buildings.
			for oldBuilding, newBuilding in buildingComparisons.itervalues():
				wasVisible = (oldBuilding != None and oldVisibilityMap.buildingIsVisible(oldBuilding))
				isVisible = (newBuilding != None and newVisibilityMap.buildingIsVisible(newBuilding))
				
				# If the buildings visibility has changed, or, if it has stayed visible but has also been modified, include it in the situation update
				if wasVisible != isVisible or (wasVisible and isVisible and newBuilding != oldBuilding):
					if not wasVisible:
						filteredSituationUpdate.addBuildingCreationForPlayer(otherPlayer, newBuilding)
					elif not isVisible:
						filteredSituationUpdate.addBuildingRemovalForPlayer(otherPlayer, oldBuilding)
					else:
						buildingUpdate = filteredSituationUpdate.addBuildingUpdateForPlayer(otherPlayer, oldBuilding)
						buildingUpdate.newBuilding = newBuilding
		
		return filteredSituationUpdate
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