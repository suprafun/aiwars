

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	#
	
	def set(self, other):
		self.x = other.x
		self.y = other.y
	#
#


def manhattanDistance(a, b):
	return abs(a.x - b.x) + abs(a.y - b.y)
#