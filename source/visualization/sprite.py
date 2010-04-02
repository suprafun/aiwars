from core.point import *


class Sprite:
	def __init__(self, position, image):
		self.position = position
		self.image = image
		
		self.visible = True
	#
	
	def width(self):
		return self.image.get_width()
	#
	
	def height(self):
		return self.image.get_height()
	#
	
	def draw(self, screen, offset):
		if not self.visible:
			return
		
		screen.blit(self.image, (self.position.x + offset.x, self.position.y + offset.y))
	#
#