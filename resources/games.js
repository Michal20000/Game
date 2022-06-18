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
	"./resources/snake-parts/food4.png"

];

var images = document.querySelectorAll(".head");
for (let image of images) {
	let source = image.getAttribute("source");
	console.log(source);
	image.setAttribute("src", imageValues[source]);
	image.style.visibility = "visible";

}
