from serialization import *


class GameData(object):
	def __init__(self, fogOfWar):
		self.fogOfWar = fogOfWar
		
		# TODO: Add more game data?
		# TODO: Add turn time limit!!!
	#
	
	# Serialization
	def toStream(self):
		return toStream(self.fogOfWar)
	#
	
	def fromStream(self, stream):
		(self.fogOfWar, \
		 readBytesCount) = fromStream(stream, bool)
	#
#