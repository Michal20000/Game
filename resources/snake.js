var canvas = null
var ctx = null
var objects = []

function getFoods() {
	var foods = []
	for (var i = 0; i < objects.length; i++) {
		if (objects[i].isFood) {
			foods.push(objects[i])
		}
	}
	return foods
}

function SnakeHead() {
	this.x = 40
	this.y = 40
	this.lastX = 0
	this.lastY = 0
	this.nextBody = null
	this.direction = "R"
	this.score = 0
	this.bestScore = 0
	this.start = function() {
		document.addEventListener("keydown", this.setDirection)
	}
	this.update = function() {
		this.lastX = this.x
		this.lastY = this.y

		if (this.direction == "T") this.moveTop();
		if (this.direction == "B") this.moveBottom();
		if (this.direction == "L") this.moveLeft();
		if (this.direction == "R") this.moveRight();

		for (var i = 9; i < objects.length; i++) {
			if (objects[i].x == this.x && objects[i].y == this.y) {
				score = document.querySelector("#score")
				if (this.score > this.bestScore) {
					this.bestScore = this.score
				}
				score.innerHTML = "=--= " + this.bestScore + " =--="
				this.score = 0
				this.nextBody = null
				while (objects.length != 9) {
					objects.pop()
				}
				break;
			}
		}

		var foods = getFoods()
		console.log(foods)
		for (var i = 0; i < foods.length; i++) {
			food = foods[i]
			if (food.x == this.x && food.y == this.y) {
				food.isFood = false
				this.score++

				if (!this.nextBody) {
					body = new SnakeBody(this.x, this.y, this)
					this.nextBody = body
					objects.push(body)
				}
				else {
					this.nextBody.createBody()
				}
				break
			}
		}
	}
	this.draw = function() {
		ctx.fillStyle = "#0000FF"
		ctx.fillRect(this.x, this.y, 40, 40)
	}
	this.moveTop = function() {
		this.y -= 40
		if (this.y == -40) this.y = 760;
	}
	this.moveBottom = function() {
		this.y += 40
		if (this.y == 800) this.y = 0;
	}
	this.moveLeft = function() {
		this.x -= 40
		if (this.x == -40) this.x = 760;
	}
	this.moveRight = function() {
		this.x += 40
		if (this.x == 800) this.x = 0;
	}
	this.setDirection = function(event) {
		if (event.keyCode == 65 || event.keyCode == 97) objects[0].direction = "L";
		if (event.keyCode == 68 || event.keyCode == 100) objects[0].direction = "R";
		if (event.keyCode == 87 || event.keyCode == 119) objects[0].direction = "T";
		if (event.keyCode == 83 || event.keyCode == 115) objects[0].direction = "B";
	}
}
function SnakeBody(x, y, parent) {
	this.x = x
	this.y = y
	this.lastX = 0
	this.lastY = 0
	this.parent = parent
	this.nextBody = null
	this.isBody = true
	this.start = function() {
	}
	this.update = function() {
		this.lastX = this.x
		this.lastY = this.y
		this.x = parent.lastX
		this.y = parent.lastY
	}
	this.createBody = function() {
		if (!this.nextBody) {
			body = new SnakeBody(this.x, this.y, this)
			this.nextBody = body
			objects.push(body)
		}
		else {
			this.nextBody.createBody()
		}
	}
	this.draw = function() {
		ctx.fillStyle = "#00FF00"
		ctx.fillRect(this.x, this.y, 40, 40)
	}	
}
function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}
function Food(x, y) {
	this.x = 40
	this.y = 40
	this.isFood = false
	this.start = function() {
	}
	this.update = function() {
		if (!this.isFood) {
			this.x = getRandomInt(0,20) * 40
			this.y = getRandomInt(0,20) * 40
			this.isFood = true
		}
	}
	this.draw = function() {
		ctx.fillStyle = "#FF0000"
		ctx.fillRect(this.x, this.y, 40, 40)
	}	
}

function mainLoop() {
	/* ctx.fillStyle = "#343A40" */
	ctx.fillStyle = "#161616"
	ctx.fillRect(0, 0, 800, 800)
	for (var i = 0; i < objects.length; i++) {
		objects[i].update()
	}
	for (var i = 0; i < objects.length; i++) {
		objects[i].draw()
	}
	setTimeout(mainLoop, 1000 / 20)
}
function main() {
	canvas = document.querySelector("canvas")
	ctx = canvas.getContext("2d")
	objects = [
		new SnakeHead(),
		new Food(),
		new Food(),
		new Food(),
		new Food(),
		new Food(),
		new Food(),
		new Food(),
		new Food()
	]
	for (var i = 0; i < objects.length; i++) {
		objects[i].start()
	}
	mainLoop()
}
window.onload = main
