#!/usr/bin/python
#This file defines all the objects using in the game
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

class PlayerObject(WorldObject):
	"""The player-controlled object: initializes using super class constructor, then loads image, sets rectangle for collision detection, sets speed, 
	and sets lives
	"""
	def __init__(self):
		WorldObject.__init__(self)
		self.image = pygame.image.load("Images/player.png")
		self.rect = self.image.get_rect()
		self.speed = 5
		self.movepos = [0,0]
		self.num_lives = 3

	"""Updates player to respond to movement events"""
	def update(self):
		newpos = pygame.Rect.move(self.rect, self.movepos[0],self.movepos[1])
		if self.area.contains(newpos):
			self.rect = newpos
		pygame.event.pump()

	"""Moves player sprite"""
	def move(self, dx, dy):
		self.movepos[0] += dx
		self.movepos[1] += dy

class WallObject(WorldObject):
	"""Object representing the walls the player must avoid"""
	def __init__(self):
		WorldObject.__init__(self)
		self.image = pygame.image.load("Images/wall.png")
		self.rect = self.image.get_rect()

	"""Wall responds to collision with player, fires event to decrease number of lives and/or end game"""
	def update(self, player):
		if self.rect.colliderect(player.rect) == 1:
			PLAYERCOLLISION = pygame.USEREVENT + 2
			playercollisionevent = pygame.event.Event(PLAYERCOLLISION)
			pygame.event.post(playercollisionevent)
			pygame.event.pump()

class ExitObject(WorldObject):
	"""Object representing the exit"""
	def __init__(self):
		WorldObject.__init__(self)
		self.image = pygame.image.load("Images/exit.png")
		self.rect = self.image.get_rect()

	"""Responds to collision with player, fires event to advance to next level"""
	def update(self, player):
		if self.rect.colliderect(player.rect) == 1:
			REACHEXIT = pygame.USEREVENT + 3
			exitevent = pygame.event.Event(REACHEXIT)
			pygame.event.post(exitevent)
			pygame.event.pump()

class BasicEnemyObject(WorldObject):
	"""Basic bject representing enemy, bounces around walls until it hits the player"""
	def __init__(self):
		WorldObject.__init__(self)
		self.image = pygame.image.load("Images/enemy.png")
		self.rect = self.image.get_rect()
		self.speed = 6
		self.angle = math.radians(random.randint(0, 359))

	"""Basic enemy moves at set speed around window, bouncing off edges"""
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

class FastEnemyObject(BasicEnemyObject):
	"""Faster enemy that is twice as fast, otherwise behaves like basic enemy"""
	def __init__(self):
		BasicEnemyObject.__init__(self)
		self.image = pygame.image.load("Images/fast.png")
		self.rect = self.image.get_rect()
		self.speed = 12

class LockOnEnemyObject(BasicEnemyObject):
	"""Slower enemy that chases the player, otherwise behaves like basic enemy"""
	def __init__(self, player):
		BasicEnemyObject.__init__(self)
		self.image = pygame.image.load("Images/lockon.png")
		self.rect = self.image.get_rect()
		self.speed = 2

	def update(self, player):
		if self.rect.colliderect(player.rect) == 1:
			PLAYERCOLLISION = pygame.USEREVENT + 2
			playercollisionevent = pygame.event.Event(PLAYERCOLLISION)
			pygame.event.post(playercollisionevent)
		dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
		distance = math.hypot(dx,dy) + .01 #Add .01 to avoid division by zero
		self.rect.x += dx * self.speed / distance
		self.rect.y += dy * self.speed / distance
		pygame.event.pump()
