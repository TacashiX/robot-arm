import * as THREE from 'three';
import { LoadingManager } from 'three';
import URDFLoader from 'urdf-loader';

const scene = new THREE.Scene();
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
// const geometry = new THREE.BoxGeometry(1, 1, 1);
// const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
//
//
// function animate() {
// 	cube.rotation.x += 0.01;
// 	cube.rotation.y += 0.01;
//
// 	renderer.render(scene, camera);
// }
// renderer.setAnimationLoop(animate);
//
let robot;
// CONTAINER SETUP
var container = document.getElementById('top-left');

scene.background = new THREE.Color('gainsboro');


// camera that uses the container's size

var camera = new THREE.PerspectiveCamera(5, container.clientWidth / container.clientHeight);
camera.position.set(1, 20, 1);
camera.lookAt(scene.position);

// renderer that uses the container's size and is inserted in it

var renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth - 16, container.clientHeight - 16);
renderer.setAnimationLoop(animationLoop);
container.appendChild(renderer.domElement);


var controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

var ambientLight = new THREE.AmbientLight('white', 0.5);
scene.add(ambientLight);

var light = new THREE.DirectionalLight('white', 0.5);
light.position.set(1, 1, 1);
scene.add(light);

scene.add(new THREE.AxesHelper(2));




// URDF Loader 

const manager = new LoadingManager();
const loader = new URDFLoader(manager);

// loader.packages = {
// 	packageName: '../../../../robot-arm/'
// };
loader.load(
	'model/Fenrir.urdf',
	result => {

		robot = result;

	});

manager.onLoad = () => {

	scene.add(robot);
	// robot.rotation.x = Math.PI / 2;
};

function animationLoop(t) {
	// robot.rotation.x = Math.sin(t / 700);
	// cube.rotation.y = Math.sin(t / 900);
	controls.update();
	light.position.copy(camera.position);
	renderer.render(scene, camera);
}
