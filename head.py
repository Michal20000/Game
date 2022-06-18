from node import Node
import random

class Head:

	def __init__(self):
		self.indexX = 0
		self.indexY = 0
		self.lastX = 0
		self.lastY = 0
		self.imageValue = 0
		self.node = None

	def move(self, valueX, valueY):
		self.lastX = self.indexX
		self.lastY = self.indexY
		self.indexX += valueX
		self.indexY += valueY

		if self.indexX == 20:
			self.indexX = 0
		elif self.indexX == -1:
			self.indexX = 19

		if self.indexY == 12:
			self.indexY = 0
		elif self.indexY == -1:
			self.indexY = 11

		if self.node is not None:
			self.node.move(self.lastX, self.lastY)

	def attach(self):
		value = self.imageValue
		buffer = self
		while buffer.node is not None:
			buffer = buffer.node

		node = Node()
		node.indexX = buffer.lastX
		node.indexY = buffer.lastY
		node.imageValue = value + random.randrange(1, 5, 1)
		buffer.node = node

	def __repr__(self):
		return F"<Head X: {self.indexX} Y: {self.indexY}>"
