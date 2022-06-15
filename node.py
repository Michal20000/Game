class Node:

	def __init__(self):
		self.indexX = 0
		self.indexY = 0
		self.lastX = 0
		self.lastY = 0
		self.node = None

	def move(self, indexX, indexY):
		self.lastX = self.indexX
		self.lastY = self.indexY
		self.indexX = indexX
		self.indexY = indexY

		if self.node is not None:
			self.node.move(self.lastX, self.lastY)

	def __repr__(self):
		return F"<Node X: {self.indexX} Y: {self.indexY}>"
