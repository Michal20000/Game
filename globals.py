# todo: clients<ID, Client>
# todo: waiting_rooms<ID, GameRoom>
# todo: during_game_rooms<ID, GameRoom>
import uuid as uuid_lib
import sqlite3
import datetime
import random


def uuid():
	return str(uuid_lib.uuid4()).upper()


CONNECTION = "connect"
DISCONNECTION = "disconnect"
BEGIN = "begin"
END = "end"
FRAME = "frame"
DIRECTION = "direction"

DIRECTION_LEFT = 0
DIRECTION_UPWARD = 1
DIRECTION_RIGHT = 2
DIRECTION_DOWNWARD = 3

DARK_GREEN = 0
LIGHT_GREEN = 1
LIGHT_YELLOW = 2
LIGHT_BROWN = 3
DARK_BROWN = 4

EMPTY = 0
FOOD = 1
HOST_HEAD = 2
HOST_NODE = 3
GUEST_HEAD = 4
GUEST_NODE = 5
BOMB = 6

clients = dict()
waiting_rooms = dict()
during_game_rooms = dict()



def calculateRating(client, opponent, gameResult):
	value = (opponent.rating - client.rating) / 400
	value = 10 ** value
	chance = 1 / (1 + value)
	buffer = 10 + (800 / client.games())

	wins = buffer * (1.0 - chance)
	draws = buffer * (0.5 - chance)
	losses = buffer * (0.0 - chance)
	print(F"W: {round(wins)} D: {round(draws)} L:{round(losses)}")
	return round(buffer * (gameResult - chance))


if __name__ == "__main__":
	values = [0, 5, 10, 15, 20]
	print(random.randrange(1, 5, 1))
	print(random.randrange(1, 5, 1))
	print(random.randrange(1, 5, 1))
	print(random.randrange(1, 5, 1))
	print(random.randrange(1, 5, 1))

	connection = sqlite3.connect("databases/main.db")
	cursor = connection.cursor()
	try:
		#cursor.execute(open("./queries/create-clients.sql").read())
		#cursor.execute(open("./queries/insert-client.sql").read(), (uuid(), "sdsd", "dds", "dsdd", 1, 1, 1))
		#cursor.execute(open("./queries/update-client.sql").read(), (2, 3, 1, "8C8EE663-18F0-4447-8D64-5FBEF4B11DF6"))
		#cursor.execute(open("./queries/select-client.sql").read(), ("8C8EE663-18F0-4447-8D64-5FBEF4B11DF6",))
		#print(cursor.fetchone())
		#cursor.execute(open("./queries/delete-matches.sql").read())
		#cursor.execute(open("./queries/create-matches.sql").read())
		connection.commit()
	except sqlite3.Error as error:
		print(error)
		print('SQLite error: %s' % (' '.join(error.args)))
		print("Exception class is: ", error.__class__)
		print('SQLite traceback: ')
	connection.close()


	#x = { 1: 3, 2: 4, 3: 5 }
	#for i in x:
		#print(i)
	#print(1 in x)
	#print(uuid())
