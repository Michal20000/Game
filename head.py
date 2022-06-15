from node import Node


class Head:

	def __init__(self):
		self.indexX = 0
		self.indexY = 0
		self.lastX = 0
		self.lastY = 0
		self.node = None

	def move(self, valueX, valueY):
		self.lastX = self.indexX
		self.lastY = self.indexY
		self.indexX += valueX
		self.indexY += valueY

		if self.indexX == 16:
			self.indexX = 0
		elif self.indexX == -1:
			self.indexX = 15

		if self.indexY == 16:
			self.indexY = 0
		elif self.indexY == -1:
			self.indexY = 15

		if self.node is not None:
			self.node.move(self.lastX, self.lastY)

	def attach(self):
		buffer = self
		while buffer.node is not None:
			buffer = buffer.node

		node = Node()
		node.indexX = buffer.lastX
		node.indexY = buffer.lastY
		buffer.node = node

	def __repr__(self):
		return F"<Head X: {self.indexX} Y: {self.indexY}>"
