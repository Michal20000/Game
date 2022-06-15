var socketIO = io("/game-room");
var hostContainer = document.querySelector("#host");
var guestContainer = document.querySelector("#guest");
var screen = document.querySelector("#game-room");
var context = screen.getContext("2d");

const EMPTY = 0;
const FOOD = 1;
const HOST_HEAD = 2;
const HOST_NODE = 3;
const GUEST_HEAD = 4;
const GUEST_NODE = 5;

const KEYBOARD = "keypress";
const FIRST = "first";
const LAST = "last";
const FRAME = "frame";
const DIRECTION = "direction";

DIRECTION_LEFT = 0
DIRECTION_UPWARD = 1
DIRECTION_RIGHT = 2
DIRECTION_DOWNWARD = 3

console.log(io);
console.log(socketIO);



const onKeyboard = (event) => {
	console.log(event.code);
	if (event.code == "KeyA") {
		socketIO.emit(DIRECTION, DIRECTION_LEFT);

	}
	else if (event.code == "KeyW") {
		socketIO.emit(DIRECTION, DIRECTION_UPWARD);

	}
	else if (event.code == "KeyD") {
		socketIO.emit(DIRECTION, DIRECTION_RIGHT);

	}
	else if (event.code == "KeyS") {
		socketIO.emit(DIRECTION, DIRECTION_DOWNWARD);

	}

}
const onFirst = function(colors) {


};
const onFrame = function(board) {
	let positionX = 0;
	let positionY = 0;

	context.fillStyle = "#161616"
	context.fillRect(0, 0, 640, 640)
	// console.log(board);

	for (column of board) {
		positionY = 0;
		for (square of column) {
			if (square == FOOD) {
				context.fillStyle = "#00FF00";
				context.fillRect(positionX, positionY, 40, 40);
				// console.log("FOOD: " + positionX + " " + positionY);

			}
			else if (square == HOST_HEAD) {
				context.fillStyle = "#0000FF";
				context.fillRect(positionX, positionY, 40, 40);
				// console.log("HOST_HEAD: " + positionX + " " + positionY);

			}
			else if (square == HOST_NODE) {
				context.fillStyle = "#0000FF";
				context.fillRect(positionX, positionY, 40, 40);
				// console.log("HOST_NODE: " + positionX + " " + positionY);

			}
			else if (square == GUEST_HEAD) {
				context.fillStyle = "#FF0000";
				context.fillRect(positionX, positionY, 40, 40);
				// console.log("GUEST_HEAD: " + positionX + " " + positionY);

			}
			else if (square == GUEST_NODE) {
				context.fillStyle = "#FF0000";
				context.fillRect(positionX, positionY, 40, 40);
				// console.log("GUEST_NODE: " + positionX + " " + positionY);

			}
			positionY = positionY + 40;

		}
		positionX = positionX + 40;

	}

};
const onLast = function() {
	console.log("");

};



socketIO.on(FIRST, onFirst);
socketIO.on(FRAME, onFrame);
socketIO.on(LAST, onLast);
document.addEventListener(KEYBOARD, onKeyboard);
