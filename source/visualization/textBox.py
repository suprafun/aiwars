from label import *
from core.point import *


class TextBox(object):
	def __init__(self, position, size, text, fontname = 'arial', fontsize = 12, color = (255, 255, 255), borderColor = (0, 0, 0)):
		self.position = position
		self.size = size
		self.color = color
		self.borderColor = borderColor
		
		# The labels position is relative to it's parent textbox
		self.margins = [5, 0, 5, 0] # left, top, right, bottom
		self.label = Label(Point(self.margins[0], self.margins[1]), text, fontname, fontsize)
		
		self.visible = True
	#
	
	def draw(self, screen, offset):
		if not self.visible:
			return
		
		pygame.draw.rect(screen, self.color, pygame.Rect((self.position.x + offset.x, self.position.y + offset.y), (self.size.x, self.size.y)))
		pygame.draw.rect(screen, self.borderColor, pygame.Rect((self.position.x + offset.x, self.position.y + offset.y), (self.size.x, self.size.y)), 1)
		self.label.draw(screen, self.position + offset)
	#
	
	def resizeToLabel(self):
		self.size.x = self.label.width() + self.margins[0] + self.margins[2]
		self.size.y = self.label.height() + self.margins[1] + self.margins[3]
	#
	
	def width(self):
		return self.size.x
	#
	
	def height(self):
		return self.size.y
	#
#