import random


class Food:

	def __init__(self):
		self.indexX = random.randrange(0, 20)
		self.indexY = random.randrange(0, 12)
		self.imageValue = random.randrange(25, 30, 1)

	def move(self):
		self.indexX = random.randrange(0, 20)
		self.indexY = random.randrange(0, 12)
