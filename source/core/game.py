from level import *


class Game(object):
	def __init__(self, gameDatabase):
		self.gameDatabase = gameDatabase
		self.level = Level(self.gameDatabase)
		
		# TODO!
	#
	
	def loadLevelFromFile(self, filename):
		self.level.loadFromFile(filename)
	#
#