

class SpriteRuleset(object):
	def __init__(self):
		self.reset()
	#
	
	def reset(self):
		self.rules = {}
	#
	
	def addRule(self, terrainTypeName, imageFilename, boundingBox):
		if not self.rules.has_key(terrainTypeName):
			self.rules[terrainTypeName] = []
		
		self.rules[terrainTypeName].append(SpriteRule(imageFilename, boundingBox))
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