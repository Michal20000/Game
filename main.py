import flask
import flask_session as session
import flask_socketio as io
import flask_sqlalchemy as sql
from globals import *
from client import Client
from game import GameRoom


application = flask.Flask(__name__, template_folder = "./views", static_folder = "./resources")
application.config["SECRET_KEY"] = "MM"
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = sql.SQLAlchemy(application)
application.config["SESSION_TYPE"] = "sqlalchemy"
application.config["SESSION_SQLALCHEMY"] = db
application.config["SESSION_SQLALCHEMY_TABLE"] = "sessions"
session.Session(application)
# db.create_all()
socketIO = io.SocketIO(application, manage_session = False)

#users = list()
#users.append(User("MM", "MM@mm.mm", "mmmm"))
#users.append(User("BP", "BP@bp.bp", "bp"))

#waiting_rooms = list()
#during_game_rooms = list()

@application.route("/")
def index():
	return flask.redirect("/pictures")



@application.route("/pictures")
def pictures():
	return flask.render_template("pictures.html")



@application.route("/snake")
def snake():
	return flask.render_template("snake.html")



@application.route("/album")
def album():
	return flask.render_template("album.html")



@application.route("/game")
def game():
	return flask.render_template("game.html")



@application.route("/register", methods = ["GET", "POST"])
def register():
	if flask.request.method == "GET":
		if "_profile" in flask.session:
			return flask.redirect("/profile")
		else:
			return flask.render_template("register.html")

	elif flask.request.method == "POST":
		username = flask.request.form["Username"]
		email = flask.request.form["Email"]
		password = flask.request.form["Password"]
		is_valid = True

		print(username)
		print(email)
		print(password)

		for client in clients.values():
			print(client.username)
			print(username)
			print(client.email)
			print(email)
			if client.username == username or client.email == email:
				return flask.redirect("/register")

		# todo: validation
		# todo: usernames and emails have to be unique

		if is_valid:
			client = Client()
			client.create(username, email, password)
			flask.session["_profile"] = True
			flask.session["_client"] = client.client

			return flask.redirect("/profile")

		return flask.redirect("/register")



@application.route("/login", methods = ["GET", "POST"])
def login():
	if flask.request.method == "GET":
		if "_profile" in flask.session:
			return flask.redirect("/profile")
		else:
			return flask.render_template("login.html")

	elif flask.request.method == "POST":
		username = flask.request.form["UsernameEmail"]
		email = flask.request.form["UsernameEmail"]
		password = flask.request.form["Password"]

		print(username)
		print(email)
		print(password)

		for client in clients.values():
			if client.username == username or client.email == email:
				if client.password == password:
					flask.session["_profile"] = True
					flask.session["_client"] = client.client

					return flask.redirect("/profile")

		return flask.redirect("/login")



@application.route("/profile")
def profile():
	if "_profile" in flask.session:
		client = clients[flask.session["_client"]]
		return flask.render_template("profile.html", username = client.username, email = client.email, wins = client.wins, draws = client.draws, losses = client.losses)
	else:
		return flask.redirect("/login")



@application.route("/room")
def room():
	if "_profile" in flask.session:
		client = clients[flask.session["_client"]]

		if client.game is None:
			return flask.render_template("game-room.html")
		else:
			return flask.redirect("/profile")
	else:
		return flask.redirect("/login")



@application.route("/logout")
def logout():
	connection = flask.session["_client"]
	room = clients[connection].game

	if room is not None:
		if room in waiting_rooms:
			waiting_rooms[room].leave(connection)
		elif room in during_game_rooms:
			during_game_rooms[room].leave(connection)

		print(F"Disconnection: {connection}")
		print(F"Room: {room}")

	flask.session.clear()
	return flask.redirect("/login")



@application.route("/debug")
def debug():
	print(flask.session)
	return flask.render_template("debug.html", clients = clients.values(), waiting_rooms = waiting_rooms.values(), during_game_rooms = during_game_rooms.values())



# todo: room page
# todo: find request

# {% if condition %}
# html
# {% else %}
# html
# {% endif %}

# {% for x in xxx %}
# html
# {% endfor %}

# {{ variable }}

# {% extends "page.html" %}
# html
# {% endblock %}

@socketIO.on(CONNECTION, namespace = "/game-room")
def connectionRoom(data = None):
	if "_profile" not in flask.session:
		return

	for game_room in waiting_rooms.values():
		game_room.join(flask.session["_client"])
		io.join_room(game_room.game, namespace = "/game-room")
		break
	else:
		game_room = GameRoom(application, flask.session["_client"])
		io.join_room(game_room.game, namespace = "/game-room")

	connection = flask.session["_client"]
	room = clients[connection].game
	print(F"Connection: {connection}")
	print(F"Room: {room}")



@socketIO.on(DISCONNECTION, namespace = "/game-room")
def disconnectionRoom(data = None):
	if "_profile" not in flask.session:
		return

	connection = flask.session["_client"]
	room = clients[connection].game

	if room in waiting_rooms:
		waiting_rooms[room].leave(connection)
		io.leave_room(room, namespace = "/game-room")
	elif room in during_game_rooms:
		during_game_rooms[room].leave(connection)
		io.leave_room(room, namespace = "/game-room")

	print(F"Disconnection: {connection}")
	print(F"Room: {room}")

@socketIO.on(DIRECTION, namespace = "/game-room")
def disconnectionRoom(data = None):
	if "_profile" not in flask.session:
		return

	client = clients[flask.session["_client"]]

	if data == DIRECTION_LEFT:
		client.direction = DIRECTION_LEFT
	elif data == DIRECTION_UPWARD:
		client.direction = DIRECTION_UPWARD
	elif data == DIRECTION_RIGHT:
		client.direction = DIRECTION_RIGHT
	elif data == DIRECTION_DOWNWARD:
		client.direction = DIRECTION_DOWNWARD



if __name__ == "__main__":
	connection = sqlite3.connect("main.db")
	cursor = connection.cursor()
	cursor.execute(open("./queries/select-clients.sql").read())
	for value in cursor.fetchall():
		client = Client()
		client.restore(value[0])
		print(client)
	connection.commit()
	connection.close()

	application.debug = True
	socketIO.run(application, host = "0.0.0.0", port = 1337)
	# application.run(debug = True)
