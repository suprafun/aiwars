from point import *


class __Node(object):
	__slots__ = ('parent', 'cost', 'position')
	
	def __init__(self, parent, cost, position):
		self.parent = parent
		self.cost = cost
		self.position = position
	#
	
	def __eq__(self, other):
		return self.position == other.position
	#
#


# Returns a tuple: a bool that indicates whether or not a path was found, and a list of points that indicates the path, including the start and end tiles.
# The list is empty if no path was found.
def getShortestPath(level, start, end):
	openList = [__Node(None, 0, start)]
	closedList = []
	
	while True:
		pass
#

# Returns a list of reachable tile positions, for the given start position and the specified unit type. Takes unit-type specific movement modifiers into account.
def getReachableTiles(level, start, unitType):
	openList = [__Node(None, 0, start)]
	closedList = []
	
	while len(openList) > 0:
		node = openList.pop(0)
		closedList.append(node)
		tile = node.position
		
		for neighbor in [Point(tile.x - 1, tile.y), Point(tile.x, tile.y - 1), Point(tile.x + 1, tile.y), Point(tile.x, tile.y + 1)]:
			if neighbor.x >= 0 and neighbor.y >= 0 and neighbor.x < level.width() and neighbor.y < level.height() and not __tileInNodeList(neighbor, openList) and not __tileInNodeList(neighbor, closedList):
				movementCost = unitType.movementCostFor(level.getTerrainType(neighbor.x, neighbor.y))
				if node.cost + movementCost <= unitType.movementPoints:
					openList.append(__Node(node, node.cost + movementCost, neighbor))
	
	return [node.position for node in closedList]
#

def __tileInNodeList(tile, nodeList):
	for node in nodeList:
		if tile == node.position:
			return True
	return False
#