from core.point import *
from sprite import *


class SpriteCollection:
	def __init__(self):
		self.position = Point(0, 0)
		
		self.images = []
		self.sprites = []
		
		self.visible = True
	#
	
	def addSprite(self, position, image):
		self.sprites.append(Sprite(position, image))
	#
	
	def draw(self, screen, offset):
		if not self.visible:
			return
		
		for sprite in self.sprites:
			sprite.draw(screen, offset)
	#
#