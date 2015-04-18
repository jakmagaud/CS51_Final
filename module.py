#Objects
from graphics import *
from abc import ABCMeta, abstractmethod

class WorldObject(object):
	"""Attributes: 
	position: tuple of ints, signifies position, (0,0) denotes top left corner
	color: string, signifies color
	movable: boolean, signifies whether object can move
	boundedbox: tuple of ints, indicates size of box (for collision detection)
	"""

	__metaclass__ = ABCMeta
	movable = false

	def __init__(self, xpos, ypos, color, xbox, ybox):
		self.position = (xpos, ypos)
		self.color = color
		self.boundedbox = (xbox, ybox)

	def move(self):
		if movable:
			pass
		else:
			pass

	@abstractmethod
	def to_string(self):
		pass

class PlayerObject(WorldObject):
	"""The player-controlled object"""
	movable = true
	color = "Blue"

    def move(self):
    	

	def to_string(self):
		return "Player: " + self.position


class WallObject(WorldObject):
	"""Object representing the walls the player must avoid"""
	movable = false
	color = "Black"

	def to_string(self):
		return "Wall: " + self.position

