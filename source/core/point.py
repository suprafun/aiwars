

class Point(object):
	__slots__ = ('x', 'y')
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
	#
	
	def set(self, other):
		self.x = other.x
		self.y = other.y
	#
	
	# + operator
	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)
	#
	
	# - operator
	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)
	#
	
	# += operator
	def __radd__(self, other):
		self.x += other.x
		self.y += other.y
	#
	
	# -= operator
	def __rsub__(self, other):
		self.x -= other.x
		self.y -= other.y
	#
	
	# == operator
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	#
#


def manhattanDistance(a, b):
	return abs(a.x - b.x) + abs(a.y - b.y)
#