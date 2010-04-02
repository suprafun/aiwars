from serialization import *


class GameData(object):
	def __init__(self, fogOfWar, playerCount):
		self.fogOfWar = fogOfWar
		self.playerCount = playerCount
	#
	
	# Serialization
	def toStream(self):
		return toStream(self.fogOfWar, \
		                self.playerCount)
	#
	
	def fromStream(self, stream):
		(self.fogOfWar, \
		 self.playerCount, \
		 readBytesCount) = fromStream(stream, bool, int)
	#
#