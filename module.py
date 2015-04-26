#!/usr/bin/python
#Objects
from abc import ABCMeta, abstractmethod
import pygame

#Abstract class representing object in the world
class WorldObject(pygame.sprite.Sprite):

	__metaclass__ = ABCMeta

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()

	@abstractmethod
	def to_string(self):
		pass

class PlayerObject(WorldObject):
	"""The player-controlled object"""
	def __init__(self):
		WorldObject.__init__(self)
		self.image = pygame.image.load("Images/player.png")
		self.rect = self.image.get_rect()
		self.speed = 5
		self.movepos = [0,0]
		self.num_lives = 3

	def update(self):
		newpos = pygame.Rect.move(self.rect, self.movepos[0],self.movepos[1])
		if self.area.contains(newpos):
			self.rect = newpos
		pygame.event.pump()

	def move(self, dx, dy):
		self.movepos[0] += dx
		self.movepos[1] += dy

	def to_string(self):
		return "x position: "  + self.rect.x + "y position: "  + self.rect.y

class WallObject(WorldObject):
	"""Object representing the walls the player must avoid"""
	def __init__(self):
		WorldObject.__init__(self)
		self.image = pygame.image.load("Images/wall.png")
		self.rect = self.image.get_rect()

	def update(self, player):
		if self.rect.colliderect(player.rect) == 1:
			COLLISION = pygame.USEREVENT + 2
			collisionevent = pygame.event.Event(COLLISION)
			pygame.event.post(collisionevent)
			pygame.event.pump()

	def to_string(self):
		pass

