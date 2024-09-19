let socket = new WebSocket('ws://localhost:8765');
const robotData = document.getElementById("robot-data");
const wsConnectionStatus = document.getElementById("ws-connection-status");
const ctrlConnectionStatus = document.getElementById("ctrl-connection-status");

socket.onmessage = (event) => {
	console.log('Received:', event.data);
	robotData.innerHTML = event.data;
	//need this to update the robot status labels. 
};

socket.onclose = () => {
	console.log('Connection closed');
};

const gamepadInfo = document.getElementById("gamepad-info");
const gamepadData = document.getElementById("gamepad-data");
var start;

var rAF = window.mozRequestAnimationFrame ||
	window.webkitRequestAnimationFrame ||
	window.requestAnimationFrame;

var rAFStop = window.mozCancelRequestAnimationFrame ||
	window.webkitCancelRequestAnimationFrame ||
	window.cancelRequestAnimationFrame;

window.addEventListener("gamepadconnected", function() {
	var gp = navigator.getGamepads()[0];
	gamepadInfo.innerHTML = "Gamepad connected at index " + gp.index + ": " + gp.id + ". It has " + gp.buttons.length + " buttons and " + gp.axes.length + " axes.";

	gameLoop();
});

window.addEventListener("gamepaddisconnected", function() {
	gamepadInfo.innerHTML = "Waiting for gamepad.";

	rAFStop(start);
});

if (!('GamepadEvent' in window)) {
	// No gamepad events available, poll instead.
	var interval = setInterval(pollGamepads, 500);
}

function pollGamepads() {
	var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads : []);
	for (var i = 0; i < gamepads.length; i++) {
		var gp = gamepads[i];
		if (gp) {
			gamepadInfo.innerHTML = "Gamepad connected at index " + gp.index + ": " + gp.id + ". It has " + gp.buttons.length + " buttons and " + gp.axes.length + " axes.";
			gameLoop();
			clearInterval(interval);
		}
	}
}

function gameLoop() {
	var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads : []);
	if (!gamepads)
		return;

	var gp = gamepads[0];
	var stuff = [gp.axes[0].toFixed(3), gp.axes[1].toFixed(3), gp.axes[3].toFixed(3), gp.buttons[6].value.toFixed(3), gp.buttons[7].value.toFixed(3), gp.buttons[9].value, gp.buttons[16].value]
	gamepadData.innerHTML = "GP data: \n" + stuff;
	socket.send(stuff)
	// need to get this shit into correct format, triggers 7 and 8th=?
	// array: [ x,y,z,ltrig, rtrig, start, guide ] 
	var start = rAF(gameLoop);
};


document.addEventListener("DOMContentLoaded", function() {
	document.getElementById("toggle-manual").classList.add("active");
	const toggleButtons = document.querySelectorAll(".tri-state-toggle-button");

	toggleButtons.forEach(function(button) {
		button.addEventListener("click", function() {
			toggleButtons.forEach(function(btn) {
				btn.classList.remove("active");
			});
			this.classList.add("active");

			switch (this.id) {
				case 'toggle-manual':
					console.log("State 1: Toggle Button 1 active");
					//enable buttons and fields
					wsConnectionStatus.classList.remove("disconnected")
					wsConnectionStatus.classList.add("connected")
					break;

				case 'toggle-controller':
					console.log("State 2: Toggle Button 2 active");
					//disable buttons and fields
					ctrlConnectionStatus.classList.remove("disconnected")
					ctrlConnectionStatus.classList.add("connected")
					break;

				case 'toggle-disable':
					console.log("State 3: Toggle Button 3 active");
					//disable 
					ctrlConnectionStatus.classList.remove("connected")
					wsConnectionStatus.classList.remove("connected")
					wsConnectionStatus.classList.add("disconnected")
					ctrlConnectionStatus.classList.add("disconnected")
					break;

			}
		});
	});
});
