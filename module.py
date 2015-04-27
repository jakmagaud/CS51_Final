#!/usr/bin/python
#Objects
from abc import ABCMeta, abstractmethod
import pygame
import random
import math

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
			PLAYERCOLLISION = pygame.USEREVENT + 2
			playercollisionevent = pygame.event.Event(PLAYERCOLLISION)
			pygame.event.post(playercollisionevent)
			pygame.event.pump()

	def to_string(self):
		pass

class ExitObject(WorldObject):
	"""Object representing the exit"""
	def __init__(self):
		WorldObject.__init__(self)
		self.image = pygame.image.load("Images/exit.png")
		self.rect = self.image.get_rect()

	def update(self, player):
		if self.rect.colliderect(player.rect) == 1:
			REACHEXIT = pygame.USEREVENT + 3
			exitevent = pygame.event.Event(REACHEXIT)
			pygame.event.post(exitevent)
			pygame.event.pump()

	def to_string(self):
		pass

class EnemyObject(WorldObject):
	"""Object representing enemy"""
	def __init__(self):
		WorldObject.__init__(self)
		self.image = pygame.image.load("Images/enemy.png")
		self.rect = self.image.get_rect()
		self.speed = 6
		self.angle = math.radians(random.randint(0, 359))
	"""
	def move(self, dx, dy):
		self.rect.x += dx
		self.rect.y += dy"""

	def update(self, player):
		if self.rect.colliderect(player.rect) == 1:
			PLAYERCOLLISION = pygame.USEREVENT + 2
			playercollisionevent = pygame.event.Event(PLAYERCOLLISION)
			pygame.event.post(playercollisionevent)
		newpos = pygame.Rect.move(self.rect, self.speed * math.cos(self.angle), self.speed * math.sin(self.angle))
		if self.area.contains(newpos):
			self.rect = newpos
		else:
			topleft = not self.area.collidepoint(newpos.topleft)
			topright = not self.area.collidepoint(newpos.topright)
			bottomleft = not self.area.collidepoint(newpos.bottomleft)
			bottomright = not self.area.collidepoint(newpos.bottomright)
			if topright and topleft or (bottomright and bottomleft):
				self.angle = -self.angle
			if topleft and bottomleft or (topright and bottomright):
				self.angle = math.pi - self.angle
		pygame.event.pump()

	def to_string(self):
		pass

