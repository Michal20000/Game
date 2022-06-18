from globals import *
from bomb import Bomb
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
		values = [0, 5, 10, 15, 20]

		self.headH = Head()
		self.headH.imageValue = random.choice(values)
		values.remove(self.headH.imageValue)

		self.headG = Head()
		self.headG.imageValue = random.choice(values)
		values.remove(self.headG.imageValue)

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

				ratingH = calculateRating(self.clientH, self.clientG, 0.0)
				ratingG = calculateRating(self.clientG, self.clientH, 1.0)
				self.insert(self.clientH.rating, self.clientG.rating, ratingH, ratingG)
				self.clientH._rating(ratingH)
				self.clientG._rating(ratingG)
				# todo: clientG wins

				self.clientH._game()
				self.clientG._game()

			elif self.clientG.client == client:
				self.clientH._wins(1)
				self.clientG._losses(1)

				ratingH = calculateRating(self.clientH, self.clientG, 1.0)
				ratingG = calculateRating(self.clientG, self.clientH, 0.0)
				self.insert(self.clientH.rating, self.clientG.rating, ratingH, ratingG)
				self.clientH._rating(ratingH)
				self.clientG._rating(ratingG)
				# todo: clientH wins

				self.clientH._game()
				self.clientG._game()

		elif self.clientH is not None:
			waiting_rooms.pop(self.game, None)
			self.clientH._game()

	def run(self):
		with self.application.test_request_context("/"):
			io.emit(BEGIN, [ self.clientH.username, self.clientG.username, self.headH.imageValue, self.headG.imageValue ], room = self.game, namespace = "/game-room")

		self.clientH._direction()
		self.clientG._direction()

		for i in range(0, 20):
			self.board.append(list())
			for j in range(0, 12):
				self.board[i].append(0)

		values = [0, 5, 10, 15, 20]
		counter = 0

		headH = self.headH
		headH.indexX = 1
		headH.indexY = 1

		headG = self.headG
		headG.indexX = 18
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
		bombs = list()
		bombs.append(Bomb())
		bombs.append(Bomb())
		bombs.append(Bomb())

		time.sleep(5)

		while self.board[headH.indexX][headH.indexY] not in [HOST_NODE, GUEST_HEAD, GUEST_NODE, BOMB] and self.board[headG.indexX][headG.indexY] not in [HOST_HEAD, HOST_NODE, GUEST_NODE, BOMB] and self.running:

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

			counter = counter + 1
			if counter % 20 == 0:
				foods.append(Food())
			if counter % 30 == 0:
				bombs.append(Bomb())

			self.generateBoard(headH, headG, foods, bombs)
			frame = self.generateFrame(headH, headG, foods, bombs)
			with self.application.test_request_context("/"):
				io.emit(FRAME, frame, room = self.game, namespace = "/game-room")
			time.sleep(0.0625)

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

				ratingH = calculateRating(self.clientH, self.clientG, 0.5)
				ratingG = calculateRating(self.clientG, self.clientH, 0.5)
				self.insert(self.clientH.rating, self.clientG.rating, ratingH, ratingG)
				self.clientH._rating(ratingH)
				self.clientG._rating(ratingG)
				# todo: clientH draws
				# todo: clientG draws

			elif winnerH == False:
				self.clientH._losses(1)
				self.clientG._wins(1)

				ratingH = calculateRating(self.clientH, self.clientG, 0.0)
				ratingG = calculateRating(self.clientG, self.clientH, 1.0)
				self.insert(self.clientH.rating, self.clientG.rating, ratingH, ratingG)
				self.clientH._rating(ratingH)
				self.clientG._rating(ratingG)
				# todo: clientG wins

			elif winnerG == False:
				self.clientH._wins(1)
				self.clientG._losses(1)

				ratingH = calculateRating(self.clientH, self.clientG, 1.0)
				ratingG = calculateRating(self.clientG, self.clientH, 0.0)
				self.insert(self.clientH.rating, self.clientG.rating, ratingH, ratingG)
				self.clientH._rating(ratingH)
				self.clientG._rating(ratingG)
				# todo: clientH wins

			self.clientH._game()
			self.clientG._game()
			during_game_rooms.pop(self.game, None)
		print("Game is finished!")

	def generateBoard(self, headH, headG, foods, bombs):
		for i in range(0, 20):
			for j in range(0, 12):
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

		for bomb in bombs:
			self.board[bomb.indexX][bomb.indexY] = BOMB

	def generateFrame(self, headH, headG, foods, bombs):
		frame = list()
		for food in foods:
			imageValue = food.imageValue << 16
			indexX = food.indexX << 8
			indexY = food.indexY
			value = imageValue ^ indexX ^ indexY
			frame.append(value)

		buffer = headH
		imageValue = buffer.imageValue << 16
		indexX = buffer.indexX << 8
		indexY = buffer.indexY
		value = imageValue ^ indexX ^ indexY
		frame.append(value)

		buffer = headG
		imageValue = buffer.imageValue << 16
		indexX = buffer.indexX << 8
		indexY = buffer.indexY
		value = imageValue ^ indexX ^ indexY
		frame.append(value)

		buffer = headH
		while buffer.node is not None:
			buffer = buffer.node
			imageValue = buffer.imageValue << 16
			indexX = buffer.indexX << 8
			indexY = buffer.indexY
			value = imageValue ^ indexX ^ indexY
			frame.append(value)

		buffer = headG
		while buffer.node is not None:
			buffer = buffer.node
			imageValue = buffer.imageValue << 16
			indexX = buffer.indexX << 8
			indexY = buffer.indexY
			value = imageValue ^ indexX ^ indexY
			frame.append(value)

		for bomb in bombs:
			imageValue = bomb.imageValue << 16
			indexX = bomb.indexX << 8
			indexY = bomb.indexY
			value = imageValue ^ indexX ^ indexY
			frame.append(value)

		return frame

	def insert(self, host_rating, guest_rating, host_change, guest_change):
		connection = sqlite3.connect("main.db")
		cursor = connection.cursor()
		cursor.execute(open("./queries/insert-match.sql").read(), (self.game, self.clientH.client, self.clientG.client, self.headH.imageValue, self.headG.imageValue, host_rating, guest_rating, host_change, guest_change, datetime.date.today()))
		connection.commit()
		connection.close()

	def __repr__(self):
		return F"<GameRoom game: {self.game} host: {self.clientH}, guest: {self.clientG}>"
