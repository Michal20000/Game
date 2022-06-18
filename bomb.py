import random


class Bomb:

	def __init__(self):
		self.indexX = random.randrange(0, 20)
		self.indexY = random.randrange(0, 12)
		self.imageValue = random.randrange(30, 35, 1)
