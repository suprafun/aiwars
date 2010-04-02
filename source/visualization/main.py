import os
import sys
import pygame
from core.game import *


class Main:
	def __init__(self):
		self.running = False
		
		# Pygame initialization
		pygame.init()
		self.screenDimension = (800, 600)
		self.screen = pygame.display.set_mode(self.screenDimension, pygame.SWSURFACE)
		pygame.display.set_caption('AI Wars')
		self.clock = pygame.time.Clock()
		
		self.game = Game()
	#
	
	def run(self):
		self.running = True
		
		while self.running:
			
			self.handleEvents()
			self.update()
			self.draw()
			
			self.clock.tick(30.0)
	#
	
	def handleEvents(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYDOWN:
				self.game.onKeyDown(event.key)
			elif event.type == pygame.KEYUP:
				self.game.onKeyUp(event.key)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.game.onMouseDown(event.button, event.pos)
			elif event.type == pygame.MOUSEBUTTONUP:
				self.game.onMouseUp(event.button, event.pos)
			elif event.type == pygame.MOUSEMOTION:
				self.game.onMouseMove(event.pos)
	#
	
	def update(self):
		self.game.update()
	#
	
	def draw(self):
		self.game.draw()
		pygame.display.flip()
	#
#

main = Main()
main.run()