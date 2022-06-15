from globals import *


class Client:

	def __init__(self):
		self.client = None
		self.username = None
		self.email = None
		self.password = None
		self.wins = 0
		self.draws = 0
		self.losses = 0
		self.game = None
		self.direction = None

	def create(self, username, email, password):
		self.client = uuid()
		self.username = username
		self.email = email
		self.password = password
		self.wins = 0
		self.draws = 0
		self.losses = 0
		clients[self.client] = self

		connection = sqlite3.connect("main.db")
		cursor = connection.cursor()
		cursor.execute(open("./queries/insert-client.sql").read(), (self.client, self.username, self.email, self.password, self.wins, self.draws, self.losses))
		connection.commit()
		connection.close()

	def restore(self, client):
		connection = sqlite3.connect("main.db")
		cursor = connection.cursor()
		cursor.execute(open("./queries/select-client.sql").read(), (client,))
		client = cursor.fetchone()
		connection.commit()
		connection.close()

		self.client = client[0]
		self.username = client[1]
		self.email = client[2]
		self.password = client[3]
		self.wins = client[4]
		self.draws = client[5]
		self.losses = client[6]
		clients[self.client] = self

	def update(self):
		connection = sqlite3.connect("main.db")
		cursor = connection.cursor()
		cursor.execute(open("./queries/update-client.sql").read(), (self.wins, self.draws, self.losses, self.client))
		connection.commit()
		connection.close()

	def _wins(self, wins = 0):
		self.wins += wins
		self.update()

	def _draws(self, draws = 0):
		self.draws += draws
		self.update()

	def _losses(self, losses = 0):
		self.losses += losses
		self.update()

	def _game(self, game = None):
		self.game = game

	def _direction(self, direction = DIRECTION_DOWNWARD):
		self.direction = direction

	def __repr__(self):
		return F"<Client client: {self.client}, username: {self.username}, email: {self.email}, wins: {self.wins}, draws: {self.draws}, losses: {self.losses}, game: {self.game}, direction: {self.direction}>"
