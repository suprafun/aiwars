

class SpriteRuleset(object):
	def __init__(self):
		self.reset()
	#
	
	def reset(self):
		self.rules = {}
	#
	
	def setSpriteCount(self, terrainTypeName, minimum, maximum):
		if not self.rules.has_key(terrainTypeName):
			self.rules[terrainTypeName] = [minimum, maximum, []]
		else:
			self.rules[terrainTypeName][0] = minimum
			self.rules[terrainTypeName][1] = maximum
	#
		
	def addRule(self, terrainTypeName, imageFilename, boundingBox):
		if not self.rules.has_key(terrainTypeName):
			self.rules[terrainTypeName] = [0, 0, []]
		
		self.rules[terrainTypeName][2].append(SpriteRule(imageFilename, boundingBox))
	#
	
	def loadFromFile(self, filename):
		execfile(filename, {'rules': self})
	#
#


class SpriteRule(object):
	def __init__(self, imageFilename, boundingBox):
		self.imageFilename = imageFilename
		self.boundingBox = boundingBox
	#
#