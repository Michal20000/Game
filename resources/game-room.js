var socketIO = io("/game-room");
var hostContainer = document.querySelector("#host");
var guestContainer = document.querySelector("#guest");
var hostImageContainer = document.querySelector("#host-image");
var guestImageContainer = document.querySelector("#guest-image");
var screen = document.querySelector("#game-room");
var context = screen.getContext("2d");
var imageValues = [
	"./resources/snake-parts/dark-green-head.png",
	"./resources/snake-parts/dark-green-node0.png",
	"./resources/snake-parts/dark-green-node1.png",
	"./resources/snake-parts/dark-green-node2.png",
	"./resources/snake-parts/dark-green-node3.png",

	"./resources/snake-parts/light-green-head.png",
	"./resources/snake-parts/light-green-node0.png",
	"./resources/snake-parts/light-green-node1.png",
	"./resources/snake-parts/light-green-node2.png",
	"./resources/snake-parts/light-green-node3.png",

	"./resources/snake-parts/light-yellow-head.png",
	"./resources/snake-parts/light-yellow-node0.png",
	"./resources/snake-parts/light-yellow-node1.png",
	"./resources/snake-parts/light-yellow-node2.png",
	"./resources/snake-parts/light-yellow-node3.png",

	"./resources/snake-parts/light-brown-head.png",
	"./resources/snake-parts/light-brown-node0.png",
	"./resources/snake-parts/light-brown-node1.png",
	"./resources/snake-parts/light-brown-node2.png",
	"./resources/snake-parts/light-brown-node3.png",

	"./resources/snake-parts/dark-brown-head.png",
	"./resources/snake-parts/dark-brown-node0.png",
	"./resources/snake-parts/dark-brown-node1.png",
	"./resources/snake-parts/dark-brown-node2.png",
	"./resources/snake-parts/dark-brown-node3.png",

	"./resources/snake-parts/food0.png",
	"./resources/snake-parts/food1.png",
	"./resources/snake-parts/food2.png",
	"./resources/snake-parts/food3.png",
	"./resources/snake-parts/food4.png",

	"./resources/snake-parts/bomb0.png",
	"./resources/snake-parts/bomb1.png",
	"./resources/snake-parts/bomb2.png",
	"./resources/snake-parts/bomb3.png",
	"./resources/snake-parts/bomb4.png"

];
var images = []
var x = 0;
for (let imageValue of imageValues) {
	let image = new Image();
	image.src = imageValues[x];
	images.push(image);
	++x;
	console.log(image);

}

const EMPTY = 0;
const FOOD = 1;
const HOST_HEAD = 2;
const HOST_NODE = 3;
const GUEST_HEAD = 4;
const GUEST_NODE = 5;

const KEYBOARD = "keypress";
const BEGIN = "begin";
const END = "end";
const FRAME = "frame";
const DIRECTION = "direction";

const DIRECTION_LEFT = 0;
const DIRECTION_UPWARD = 1;
const DIRECTION_RIGHT = 2;
const DIRECTION_DOWNWARD = 3;

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
const onBegin = function(data) {
	console.log(data);
	hostContainer.innerHTML = "&nbsp" + data[0];
	guestContainer.innerHTML = "&nbsp" + data[1];
	hostImageContainer.src = imageValues[data[2]];
	guestImageContainer.src = imageValues[data[3]];
	hostImageContainer.style.visibility = "visible";
	guestImageContainer.style.visibility = "visible";


};
const onFrame = function(board) {
	let imageValue = 0;
	let positionX = 0;
	let positionY = 0;

	context.fillStyle = "#161616";
	context.fillRect(0, 0, 800, 480);
	console.log(board);

	for (let node of board) {
		imageValue = (node & 0B111111110000000000000000) >> 16;
		positionX = (node & 0B1111111100000000) >> 8;
		positionY = node & 0B11111111;
		//console.log(imageValue);
		//console.log(positionX);
		//console.log(positionY);

		positionX = positionX * 40 + 4;
		positionY = positionY * 40 + 4;
		context.drawImage(images[imageValue], positionX, positionY);


	}

};
const onEnd = function() {
	console.log("");

};



socketIO.on(BEGIN, onBegin);
socketIO.on(FRAME, onFrame);
socketIO.on(END, onEnd);
document.addEventListener(KEYBOARD, onKeyboard);
