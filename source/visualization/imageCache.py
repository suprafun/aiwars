import pygame


class ImageCache(object):
	def __init__(self):
		self.images = {}
	#
	
	def getImage(self, filename):
		if not self.images.has_key(filename):
			self.images[filename] = pygame.image.load(filename)#.convert()
		
		return self.images[filename]
	#
	
	def cleanUp(self):
		self.images.clear()
	#
#