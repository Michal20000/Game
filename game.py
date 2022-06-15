from globals import *
from head import Head
from food import Food
import threading
import flask_socketio as io
import time


class GameRoom:

	def __init__(self, application, client):
		self.application = application
		self.game = uuid()
		self.running = True
		self.clientH = clients[client]
		self.clientH._game(self.game)
		self.clientG = None
		self.board = list()
		waiting_rooms[self.game] = self
		# todo: joinH, joinG

	def join(self, client):
		self.clientG = clients[client]
		self.clientG._game(self.game)
		waiting_rooms.pop(self.game, None)
		during_game_rooms[self.game] = self
		thread = threading.Thread(target = self.run)
		thread.start()

	def leave(self, client):
		if self.clientH is not None and self.clientG is not None:
			self.running = False
			during_game_rooms.pop(self.game, None)

			if self.clientH.client == client:
				self.clientG._wins(1)
				self.clientH._losses(1)
				# todo: clientG wins
				self.clientH._game()
				self.clientG._game()

			elif self.clientG.client == client:
				self.clientH._wins(1)
				self.clientG._losses(1)
				# todo: clientH wins
				self.clientH._game()
				self.clientG._game()

		elif self.clientH is not None:
			waiting_rooms.pop(self.game, None)
			self.clientH._game()

	def run(self):
		self.clientH._direction()
		self.clientG._direction()

		for i in range(0, 16):
			self.board.append(list())
			for j in range(0, 16):
				self.board[i].append(0)

		headH = Head()
		headH.indexX = 1
		headH.indexY = 1
		headG = Head()
		headG.indexX = 14
		headG.indexY = 1

		foods = list()
		foods.append(Food())
		foods.append(Food())
		foods.append(Food())
		foods.append(Food())
		foods.append(Food())
		foods.append(Food())
		foods.append(Food())
		foods.append(Food())

		time.sleep(1)

		while self.board[headH.indexX][headH.indexY] not in [HOST_NODE, GUEST_HEAD, GUEST_NODE] and self.board[headG.indexX][headG.indexY] not in [HOST_HEAD, HOST_NODE, GUEST_NODE] and self.running:

			if self.clientH.direction == DIRECTION_LEFT:
				headH.move(-1, 0)
			elif self.clientH.direction == DIRECTION_UPWARD:
				headH.move(0, -1)
			elif self.clientH.direction == DIRECTION_RIGHT:
				headH.move(1, 0)
			elif self.clientH.direction == DIRECTION_DOWNWARD:
				headH.move(0, 1)

			if self.clientG.direction == DIRECTION_LEFT:
				headG.move(-1, 0)
			elif self.clientG.direction == DIRECTION_UPWARD:
				headG.move(0, -1)
			elif self.clientG.direction == DIRECTION_RIGHT:
				headG.move(1, 0)
			elif self.clientG.direction == DIRECTION_DOWNWARD:
				headG.move(0, 1)

			if self.board[headH.indexX][headH.indexY] == FOOD:
				headH.attach()
				# print(headH)
				# print(headH.node)
				for food in foods:
					if food.indexX == headH.indexX and food.indexY == headH.indexY:
						food.move()
			if self.board[headG.indexX][headG.indexY] == FOOD:
				headG.attach()
				# print(headG)
				# print(headG.node)
				for food in foods:
					if food.indexX == headG.indexX and food.indexY == headG.indexY:
						food.move()

			# todo: check maybe something else
			# todo: if it is do some action
			self.generate(headH, headG, foods)
			with self.application.test_request_context("/"):
				io.emit(FRAME, self.board, room = self.game, namespace = "/game-room")
			time.sleep(0.0625)
			#time.sleep(0.5)

		# todo: someone wins
		winnerH = True
		winnerG = True

		if self.running:
			if self.board[headH.indexX][headH.indexY] in [HOST_NODE, GUEST_HEAD, GUEST_NODE]:
				winnerH = False
			if self.board[headG.indexX][headG.indexY] in [HOST_HEAD, HOST_NODE, GUEST_NODE]:
				winnerG = False

			if winnerH == False and winnerG == False:
				self.clientH._draws(1)
				self.clientG._draws(1)
			elif winnerH == False:
				self.clientH._losses(1)
				self.clientG._wins(1)
			elif winnerG == False:
				self.clientH._wins(1)
				self.clientG._losses(1)

			self.clientH._game()
			self.clientG._game()
			during_game_rooms.pop(self.game, None)
		print("Game is finished!")

	def generate(self, headH, headG, foods):
		for i in range(0, 16):
			for j in range(0, 16):
				self.board[i][j] = 0
		for food in foods:
			self.board[food.indexX][food.indexY] = FOOD

		self.board[headH.indexX][headH.indexY] = HOST_HEAD
		self.board[headG.indexX][headG.indexY] = GUEST_HEAD

		buffer = headH
		while buffer.node is not None:
			buffer = buffer.node
			self.board[buffer.indexX][buffer.indexY] = HOST_NODE
		buffer = headG
		while buffer.node is not None:
			buffer = buffer.node
			self.board[buffer.indexX][buffer.indexY] = GUEST_NODE

	def __repr__(self):
		return F"<GameRoom game: {self.game} host: {self.clientH}, guest: {self.clientG}>"
