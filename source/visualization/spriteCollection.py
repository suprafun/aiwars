from core.point import *
from sprite import *


class SpriteCollection:
	def __init__(self):
		self.position = Point(0, 0)
		
		self.images = []
		self.sprites = []
	#
	
	def addSprite(self, position, image):
		self.sprites.append(Sprite(position, image))
	#
	
	def draw(self, screen, offset):
		for sprite in self.sprites:
			sprite.draw(screen, offset)
	#
#