import random


class Food:

	def __init__(self):
		self.indexX = random.randrange(0, 16)
		self.indexY = random.randrange(0, 16)

	def move(self):
		self.indexX = random.randrange(0, 16)
		self.indexY = random.randrange(0, 16)
