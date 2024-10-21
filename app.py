from flask import Flask, render_template, Response, send_from_directory, request, jsonify
import time
import logging, sys
import json
import threading
import asyncio
import src.arm as arm
import src.bulletsim as sim
import src.control  as control

app = Flask(__name__)
log = logging.getLogger(__name__)
bsim = sim.Simulation(urdf="model/Fenrir.urdf")
robot = arm.Fenrir(bullet=bsim, simulate=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model/<path:filename>')
def custom_static(filename):
    return send_from_directory('model/', filename)

@app.route('/logs')
def logs():
    def generate_logs():
        with open('log.txt', 'r') as log_file:
            while True:
                line = log_file.readline()
                if line:
                    yield f"data: {line}\n\n"
                time.sleep(0.1)
    return Response(generate_logs(), mimetype='text/event-stream')

@app.route('/config', methods=['POST','GET'])
def config():
    if request.method == "POST":
        data = request.get_json()
        # gettting min max speed stdev 
        robot.accel_minmax = [int(data['min']), int(data['max'])]
        robot.speed = int(data['speed'])
        robot.accel_std_dev = int(data['stdev'])
        log.info(f"Config updated: {data}")
        return Response(status=204)
    else: 
        current_config = { "min": robot.accel_minmax[0], "max": robot.accel_minmax[1], "speed": robot.speed, "stdev": robot.accel_std_dev, "gripmin": robot.gripper_limit[0], "gripmax": robot.gripper_limit[1] } 
        return current_config

@app.route('/setmode',methods=['POST'])
def setmode():
    data = request.get_json()
    robot.mode = data['mode']
    log.info(f"Set mode to {data['mode']}") 
    return Response(status=204)

@app.route('/home')
async def home(): 
    await robot.home()
    return Response(status=204)

@app.route('/grip', methods=['POST'])
def grip():
    data = request.get_json()
    robot.grip(data["pos"], abs=True)
    log.info(f'Gripper set to: {data["pos"]}')
    return Response(status=204)

@app.route('/movecoords', methods=['POST'])
async def movecoord():
    data = request.get_json()
    log.info(f"Moving to {data['coords']}. {data['smooth']=}")
    await robot.move_coord(data['coords'], data['smooth'])
    return Response(status=204)

@app.route('/moveangles', methods=['POST'])
async def moveangles():
    data = request.get_json()
    if data['smooth']:
        await robot.move_arm(data['angles'])
    else: 
        robot.move_all(data['angles'])
    return Response(status=204)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(levelname)s: %(message)s")
    logging.getLogger('websockets.server').setLevel(logging.ERROR)
    logging.getLogger('websockets.protocol').setLevel(logging.ERROR)

    threading.Thread(target=asyncio.run, args=(control.start(robot,bsim),),daemon=True).start()
    threading.Thread(target=asyncio.run, args=(bsim.update_loop(),),daemon=True).start()

    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    

