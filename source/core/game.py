from level import *


class Game(object):
	def __init__(self, gameDatabase):
		self.gameDatabase = gameDatabase
		self.level = Level(self.gameDatabase)
		
		self.fogOfWar = False
		
		# TODO!
	#
	
	def loadLevelFromFile(self, filename):
		self.level.loadFromFile(filename)
	#
#