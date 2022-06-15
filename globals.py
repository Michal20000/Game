# todo: clients<ID, Client>
# todo: waiting_rooms<ID, GameRoom>
# todo: during_game_rooms<ID, GameRoom>
import uuid as uuid_lib
import sqlite3


def uuid():
	return str(uuid_lib.uuid4()).upper()


CONNECTION = "connect"
DISCONNECTION = "disconnect"
FIRST = "first"
LAST = "last"
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

clients = dict()
waiting_rooms = dict()
during_game_rooms = dict()

if __name__ == "__main__":
	connection = sqlite3.connect("main.db")
	cursor = connection.cursor()
	try:
		cursor.execute(open("./queries/create.sql").read())
		#cursor.execute(open("./queries/insert-client.sql").read(), (uuid(), "sdsd", "dds", "dsdd", 1, 1, 1))
		#cursor.execute(open("./queries/update-client.sql").read(), (2, 3, 1, "8C8EE663-18F0-4447-8D64-5FBEF4B11DF6"))
		#cursor.execute(open("./queries/select-client.sql").read(), ("8C8EE663-18F0-4447-8D64-5FBEF4B11DF6",))
		#print(cursor.fetchone())
		#cursor.execute(open("./queries/delete.sql").read())
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
