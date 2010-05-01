import os
import sys
import pygame
import threading
from core.game import *
from core.gameDatabase import *
from core.gameClient import *
from core.messageTypes import *
from core.serialization import *
from core.situationUpdate import *
from gameScreen import *
from imageCache import *


class Main:
	def __init__(self, host, port, name):
		# Pygame initialization
		pygame.init()
		self.screenDimension = (800, 600)
		self.window = pygame.display.set_mode(self.screenDimension, pygame.SWSURFACE)
		self.screen = pygame.display.get_surface()
		pygame.display.set_caption('AI Wars')
		self.clock = pygame.time.Clock()
		
		self.imageCache = ImageCache()
		
		
		# Observer client initialization
		self.name = name
		
		self.gameDatabase = GameDatabase()
		self.game = Game(self.gameDatabase)
		
		self.gameScreen = GameScreen(self.game, self.imageCache, self.screenDimension)
		self.running = False
		
		self.gameClient = GameClient()
		self.gameClient.setCallbackForMessageType(STC_DATABASE_DATA, self.onDatabaseData)
		self.gameClient.setCallbackForMessageType(STC_MAP_DATA, self.onMapData)
		self.gameClient.setCallbackForMessageType(STC_GAME_DATA, self.onGameData)
		self.gameClient.setCallbackForMessageType(STC_START_GAME, self.onStartGame)
		
		# Listen for data in a separate thread, so the visualization does not get blocked
		self.gameClient.connectToServer(host, port, 30)
		self.connectionThread = threading.Thread(target = self.gameClient.listenForData)
		self.connectionThread.start()
	#
	
	def run(self):
		self.running = True
		
		while self.running:
			
			self.handleEvents()
			self.update()
			self.draw(self.screen)
			
			self.clock.tick(30.0)
	#
	
	def handleEvents(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYDOWN:
				self.gameScreen.onKeyDown(event.key)
			elif event.type == pygame.KEYUP:
				self.gameScreen.onKeyUp(event.key)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.gameScreen.onMouseDown(event.button, event.pos)
			elif event.type == pygame.MOUSEBUTTONUP:
				self.gameScreen.onMouseUp(event.button, event.pos)
			elif event.type == pygame.MOUSEMOTION:
				self.gameScreen.onMouseMove(event.pos)
	#
	
	def update(self):
		self.gameScreen.update()
	#
	
	def draw(self, screen):
		screen.fill((255, 255, 255))
		self.gameScreen.draw(screen)
		pygame.display.flip()
	#
	
	
	# Server message handling
	def onDatabaseData(self, message):
		print 'Database data received from server'
		self.gameDatabase.fromStream(message)
	#
	
	def onMapData(self, message):
		print 'Map data received from server'
		self.game.level.fromStream(message)
		
		self.gameScreen.updateLevel()
	#
	
	def onGameData(self, message):
		print 'Game data received from server'
		self.game.gameData.fromStream(message)
		
		self.gameClient.sendMessageToServer(CTS_SET_NAME, toStream(self.name))
		self.gameClient.sendMessageToServer(CTS_SET_MODE, CLIENT_MODE_OBSERVER)
	#
	
	def onStartGame(self, message):
		self.playerID, playerCount, totalReadBytes = fromStream(message, int, int)
		for i in xrange(playerCount):
			# TODO: Change game.addPlayer to accept a Player object instead of a name and id!
			player = Player(self.game, '', 0)
			totalReadBytes += player.fromStream(message[totalReadBytes:])
			self.game.addPlayer(player.name, player.id)
		print 'Start the game!'
		
		# Stop listening for pre-game data
		self.gameClient.setCallbackForMessageType(STC_DATABASE_DATA, None)
		self.gameClient.setCallbackForMessageType(STC_MAP_DATA, None)
		self.gameClient.setCallbackForMessageType(STC_GAME_DATA, None)
		self.gameClient.setCallbackForMessageType(STC_START_GAME, None)
		
		# Start listening for observer-specific messages
		self.gameClient.setCallbackForMessageType(STC_PLAYER_STARTED_TURN, self.onPlayerStartedTurn)
		self.gameClient.setCallbackForMessageType(STC_PLAYER_ENDED_TURN, self.onPlayerEndedTurn)
		self.gameClient.setCallbackForMessageType(STC_SITUATION_UPDATE, self.onSituationUpdate)
	#
	
	
	# Observer-specific message handling
	def onPlayerStartedTurn(self, message):
		playerID, readBytes = fromStream(message, int)
		print 'Player', playerID, 'turn has started.'
	#
	
	def onPlayerEndedTurn(self, message):
		playerID, readBytes = fromStream(message, int)
		print 'Player', playerID, 'turn has ended.'
	#
	
	def onSituationUpdate(self, message):
		situationUpdate = SituationUpdate(self.game)
		situationUpdate.fromStream(message)
		
		self.game.applySituationUpdate(situationUpdate)
		
		print 'Full situation update!'
		print len(situationUpdate.playerUpdates), 'players involved:'
		for player, playerUpdate in situationUpdate.playerUpdates.iteritems():
			print 'player', player.id, 'has', len(playerUpdate.unitUpdates), 'unit updates and', len(playerUpdate.buildingUpdates), 'building updates'
	#
#