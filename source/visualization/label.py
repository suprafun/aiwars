import pygame
from core.point import *


class Label(object):
	def __init__(self, position, text, fontname, fontsize):
		self.font = pygame.font.SysFont(fontname, fontsize)
		self.__textColor = (0, 0, 0)
		self.__antiAliasing = True
		self.__text = text
		self.__dirty = True
		self.refresh()
		
		self.position = position
		
		self.visible = True
	#
	
	def draw(self, screen, offset):
		if not self.visible:
			return
		
		# Lazy updating of the internal surface - so if text, color and anti-aliasing are all changed between two render calls,
		# the surface is only recreated once.
		if self.__dirty:
			self.refresh()
		
		screen.blit(self.__surface, (self.position.x + offset.x, self.position.y + offset.y))
	#
	
	def width(self):
		return self.__surface.get_width()
	#
	
	def height(self):
		return self.__surface.get_height()
	#
	
	def refresh(self):
		self.__surface = self.font.render(self.__text, self.__antiAliasing, self.__textColor)
		self.__dirty = False
	#
	
	def __setTextColor(self, textColor):
		if self.__textColor != textColor:
			self.__textColor = textColor
			self.__dirty = True
	#
	
	def __getTextColor(self):
		return self.__textColor
	#
	
	def __setAntiAliasing(self, antiAliasing):
		if self.__antiAliasing != antiAliasing:
			self.__antiAliasing = antiAliasing
			self.__dirty = True
	#
	
	def __getAntiAliasing(self):
		return self.__antiAliasing
	#
	
	def __setText(self, text):
		if self.__text != text:
			self.__text = text
			self.__dirty = True
	#
	
	def __getText(self):
		return self.__text
	#
	
	textColor = property(__getTextColor, __setTextColor)
	antiAliasing = property(__getAntiAliasing, __setAntiAliasing)
	text = property(__getText, __setText)
#