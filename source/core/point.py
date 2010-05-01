

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
	
	def __copy__(self):
		return Point(self.x, self.y)
	#
	
	# + operator
	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)
	#
	
	# - operator
	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)
	#
	
	# * operator
	def __mul__(self, scalar):
		return Point(self.x * scalar, self.y * scalar)
	#
	
	# / operator
	def __div__(self, scalar):
		return Point(self.x / scalar, self.y / scalar)
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
	
	# *= operator
	def __rmul__(self, scalar):
		self.x *= scalar
		self.y *= scalar
	#
	
	# /= operator
	def __rdiv__(self, scalar):
		self.x /= scalar
		self.y /= scalar
	#
	
	# == operator
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	#
	
	# Emulate a list of 2 items
	def __len__(self):
		return 2
	#
	
	def __getitem(self, index):
		if index == 0:
			return self.x
		return self.y
	#
	
	def __str__(self):
		return '(' + str(self.x) + ', ' + str(self.y) + ')'
	#
#


def manhattanDistance(a, b):
	return abs(a.x - b.x) + abs(a.y - b.y)
#