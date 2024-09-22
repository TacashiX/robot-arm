// let socket = new WebSocket('ws://localhost:8765');
import { updateSim } from "./sim.js";
const wsConnectionStatus = document.getElementById("ws-connection-status");
const ctrlConnectionStatus = document.getElementById("ctrl-connection-status");
const anglesData = document.getElementById("lbl-angles");
const coordsData = document.getElementById("lbl-coords");
const gripperData = document.getElementById("lbl-gripper");
var socket;

function connect() {
	socket = new WebSocket('ws://' + location.hostname + ':8765');

	socket.onopen = () => {
		wsConnectionStatus.classList.remove("disconnected")
		wsConnectionStatus.classList.add("connected")
	}

	socket.onmessage = (event) => {
		console.log('Received:', event.data);
		var data = JSON.parse(event.data);
		anglesData.innerHTML = data[0];
		coordsData.innerHTML = data[1];
		gripperData.innerHTML = data[2];
		console.log(typeof data[0]);
		updateSim(data[0]);
	};

	socket.onclose = () => {
		console.log('Connection closed. Trying to reconnect...');
		wsConnectionStatus.classList.remove("connected")
		wsConnectionStatus.classList.add("disconnected")
		anglesData.innerHTML = "N/A";
		coordsData.innerHTML = "N/A";
		gripperData.innerHTML = "N/A";
		setTimeout(function() {
			connect()
		}, 1000);
	};
}
connect()


var start;

var rAF = window.mozRequestAnimationFrame ||
	window.webkitRequestAnimationFrame ||
	window.requestAnimationFrame;

var rAFStop = window.mozCancelRequestAnimationFrame ||
	window.webkitCancelRequestAnimationFrame ||
	window.cancelRequestAnimationFrame;

window.addEventListener("gamepadconnected", function() {
	var gp = navigator.getGamepads()[0];
	ctrlConnectionStatus.classList.remove("disconnected")
	ctrlConnectionStatus.classList.add("connected")

	mainLoop();
});

window.addEventListener("gamepaddisconnected", function() {
	ctrlConnectionStatus.classList.remove("connected")
	ctrlConnectionStatus.classList.add("disconnected")

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
			mainLoop();
			clearInterval(interval);
		}
	}
}

function mainLoop() {
	var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads : []);
	if (!gamepads)
		return;

	var gp = gamepads[0];
	var gp_input = [gp.axes[0].toFixed(3), gp.axes[1].toFixed(3), gp.axes[3].toFixed(3), gp.buttons[6].value.toFixed(3), gp.buttons[7].value.toFixed(3), gp.buttons[9].value, gp.buttons[16].value]
	if (document.getElementById("toggle-controller").classList.contains("active") && socket.readyState == WebSocket.OPEN) {
		socket.send(gp_input);
	}
	// array: [ x,y,z,ltrig, rtrig, start, guide ] 
	var start = rAF(mainLoop);
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
					sendHttpRequest("POST", "setmode", { "mode": "M" });
					//enable inputts 
					document.querySelectorAll(`.${"m-control"}`).forEach(element => { element.disabled = false; });
					break;

				case 'toggle-controller':
					sendHttpRequest("POST", "setmode", { "mode": "C" });
					//disable buttons and fields
					document.querySelectorAll(`.${"m-control"}`).forEach(element => { element.disabled = true; });
					break;

				case 'toggle-disable':
					sendHttpRequest("POST", "setmode", { "mode": "E" });
					//disable 
					document.querySelectorAll(`.${"m-control"}`).forEach(element => { element.disabled = true; });
					break;

			}
		});
	});
});

const eventSource = new EventSource('/logs');
const consoleOutput = document.getElementById('console-output');
const consoleContainer = document.getElementById('console-container');

eventSource.onmessage = function(event) {
	consoleOutput.innerHTML += event.data + "\n";
	consoleContainer.scrollTop = consoleContainer.scrollHeight;  // Auto-scroll to the bottom
};

const sendHttpRequest = (method, endpoint, data) => {
	return fetch(`http://` + location.host + `/${endpoint}`, {
		method: method,
		body: JSON.stringify(data),
		headers: { "Content-Type": "application/json" },
	}).then((response) => {
		// console.log(response); // response is stream data
		// Handle HTTP errors
		if (!response.ok) {
			// convert stream data to JSON
			return response.json().then((errorResponseData) => {
				const error = new Error();
				error.message = "Something went wrong!";
				error.data = errorResponseData;
				throw error;
			});
		} else if (response.status == 204) {
			return
		}
		return response.json();
	});
};

var conf = await sendHttpRequest("GET", "config");
console.log(conf);
document.getElementById("accmin").value = conf["min"];
document.getElementById("accmax").value = conf["max"];
document.getElementById("speed").value = conf["speed"];
document.getElementById("stdev").value = conf["stdev"];


document.getElementById("btn-config").onclick = updateButton;
function updateButton() {
	var data = { "min": document.getElementById("accmin").value, "max": document.getElementById("accmax").value, "speed": document.getElementById("speed").value, "stdev": document.getElementById("stdev").value };
	sendHttpRequest("POST", "config", data);
}

document.getElementById("btn-home").onclick = home;
function home() {
	sendHttpRequest("GET", "home");
}

const coordsRegex = new RegExp('^-?\\d+\\.\\d{2}(,-?\\d+\\.\\d{2}){2}$');
const coordsInput = document.getElementById("coords-input");
const checkSmoothing = document.getElementById("check-smoothing");
document.getElementById("btn-coords").onclick = moveCoords;
function moveCoords() {
	if (coordsRegex.test(coordsInput.value)) {
		sendHttpRequest("POST", "movecoords", { "coords": coordsInput.value.split(','), "smooth": checkSmoothing.checked });
	} else {
		coordsInput.style.borderColor = "red";
		setTimeout(function() {
			coordsInput.style.borderColor = "initial";
		}, 100);
	}
}

const anglesRegex = new RegExp('^\\d{1,3}(,\\d{1,3}){5}$');
const anglesInput = document.getElementById("angles-input");
document.getElementById("btn-angles").onclick = moveAngles;
function moveAngles() {
	if (anglesRegex.test(anglesInput.value)) {
		sendHttpRequest("POST", "moveangles", { "angles": anglesInput.value.split(','), "smooth": checkSmoothing.checked });
	} else {
		anglesInput.style.borderColor = "red";
		setTimeout(function() {
			anglesInput.style.borderColor = "initial";
		}, 100);
	}

}

const gripRange = document.getElementById("grip-range");
gripRange.onmouseup = moveGrip;
function moveGrip() {
	sendHttpRequest("POST", "grip", { "pos": gripRange.value })
}

