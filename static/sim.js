import {
	WebGLRenderer,
	PerspectiveCamera,
	Scene,
	Mesh,
	PlaneGeometry,
	ShadowMaterial,
	DirectionalLight,
	PCFSoftShadowMap,
	Color,
	AmbientLight,
	Box3,
	LoadingManager,
	MathUtils,
} from 'three';

import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import URDFLoader from 'urdf-loader';

export const homePos = [90, 40, 140, 100, 180, 90]
let scene, camera, renderer, robot, controls;
var container = document.getElementById('top-left');

init();
render();

function init() {

	scene = new Scene();
	scene.background = new Color(0x3d5c85);

	camera = new PerspectiveCamera(4, container.clientWidth / container.clientHeight);
	camera.position.set(0, 5, 10);

	renderer = new WebGLRenderer({ antialias: true });
	renderer.shadowMap.enabled = true;
	renderer.shadowMap.type = PCFSoftShadowMap;
	container.appendChild(renderer.domElement);

	const directionalLight = new DirectionalLight(0xffffff, 1.0);
	directionalLight.castShadow = true;
	directionalLight.shadow.mapSize.setScalar(1024);
	directionalLight.position.set(5, 30, 5);
	scene.add(directionalLight);

	const ambientLight = new AmbientLight(0xffffff, 0.2);
	scene.add(ambientLight);

	const ground = new Mesh(new PlaneGeometry(), new ShadowMaterial({ opacity: 0.25 }));
	ground.rotation.x = -Math.PI / 2;
	ground.scale.setScalar(30);
	ground.receiveShadow = true;
	scene.add(ground);

	controls = new OrbitControls(camera, renderer.domElement);
	controls.minDistance = 2;
	controls.update();

	// Load robot
	const manager = new LoadingManager();
	const loader = new URDFLoader(manager);
	loader.load('model/Fenrir.urdf', result => {

		robot = result;

	});

	// wait until all the geometry has loaded to add the model to the scene
	manager.onLoad = () => {

		robot.rotation.x = -Math.PI / 2;
		robot.rotation.z = -Math.PI / 3;
		robot.traverse(c => {
			c.castShadow = true;
		});

		robot.updateMatrixWorld(true);

		const bb = new Box3();
		bb.setFromObject(robot);

		robot.traverse(o => {
			if (o.isMesh) {
				o.material.color.set(0xffffff);
			}
		});


		updateSim(homePos);

		robot.position.set(0, 0, 0);
		controls.target = robot.position;
		camera.lookAt(robot.position);
		robot.position.y -= bb.min.y;
		scene.add(robot);

	};

	onResize();
	window.addEventListener('resize', onResize);
}

function onResize() {

	renderer.setSize(container.clientWidth, container.clientHeight);
	renderer.setPixelRatio(window.devicePixelRatio);

	camera.aspect = container.clientWidth / container.clientHeight;
	camera.updateProjectionMatrix();


	const w = container.clientWidth;
	const h = container.clientHeight;
	const fullWidth = w * 3;
	const fullHeight = h * 2;
	// w increase moves left, h increase up
	camera.setViewOffset(fullWidth, fullHeight, w * 0.855, h * 0.2, w, h);
}

function render() {
	requestAnimationFrame(render);
	renderer.render(scene, camera);

	var angles = document.getElementById("lbl-angles").innerHTML;

}

function degToRad(d_pos, jmin, jmax) {
	const rad = jmin + (d_pos / 180) * (jmax - jmin);
	return rad;
}

export function updateSim(angles) {
	const jlist = ['base_joint', 'j1', 'j2', 'j3', 'j4', 'j5'];

	if (angles != "N/A") {
		// angles = angles.split(',').map(Number);
		// console.log(angles);
		console.log(angles[0]);
		for (let i = 0; i < jlist.length; i++) {
			robot.joints[jlist[i]].setJointValue(degToRad(angles[i], robot.joints[jlist[i]]['limit']['lower'], robot.joints[jlist[i]]['limit']['upper']));
		}
	}
}
