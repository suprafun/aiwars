from point import *


# Returns a tuple: a bool that indicates whether or not a path was found, and a list of points that indicates the path, including the start and end tiles.
# The list is empty if no path was found.
def getShortestPath(level, start, destination):
	openList = [__Node(None, 0, start)]
	closedList = []
	
	while len(openList) > 0:
		openList.sort(lambda a, b: a.cost - b.cost)
		node = openList.pop(0)
		closedList.append(node)
		tile = node.position
		
		for neighbor in [Point(tile.x - 1, tile.y), Point(tile.x, tile.y - 1), Point(tile.x + 1, tile.y), Point(tile.x, tile.y + 1)]:
			if neighbor.x >= 0 and neighbor.y >= 0 and neighbor.x < level.width() and neighbor.y < level.height() and not __tileInNodeList(neighbor, openList) and not __tileInNodeList(neighbor, closedList):
				movementCost = unitType.movementCostFor(level.getTerrainType(neighbor))
				openList.append(__Node(node, node.cost + movementCost, neighbor))
				
				if neighbor == destination:
					path = []
					pathNode = openList[-1]
					while pathNode != None:
						path.insert(0, pathNode.position)
						pathNode = pathNode.parent
					return (True, path)
	
	return (False, [])
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
				movementCost = unitType.movementCostFor(level.getTerrainType(neighbor))
				if node.cost + movementCost <= unitType.movementPoints:
					openList.append(__Node(node, node.cost + movementCost, neighbor))
	
	return [node.position for node in closedList]
#

# Checks if the specified unit type can follow the given route within one turn. This fu nction only checks the terrain, it does not look for obstructing units.
def isRouteValid(level, unitType, route):
	movementPointsLeft = unitType.movementPoints
	for tile in route:
		movementPointsLeft -= unitType.movementCostFor(level.getTerrainType(tile))
		if movementPointsLeft < 0:
			return False
	return True
#

# Checks if any of the specified players have a unit somewhere on the given route.
# Do not pass the player object that needs to check whether a path is unobstructed, because friendly units do not trap each other.
# Returns (success, route, obstructing unit). If there is no obstructing unit, (True, original route, None) is returned.
# Otherwise, (False, route up to the obstructing unit, obstructing unit) is returned.
def isRouteUnobstructed(players, route):
	for i in xrange(len(route)):
		for player in players:
			obstructingUnit = player.getUnitAtPosition(route[i])
			if obstructingUnit != None:
				return (False, route[:i], obstructingUnit)
	return (True, route, None)
#


def __tileInNodeList(tile, nodeList):
	for node in nodeList:
		if tile == node.position:
			return True
	return False
#

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