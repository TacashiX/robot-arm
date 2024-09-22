from flask import Flask, render_template, Response, request, jsonify
import threading
import main
import src.arm as arm
import src.bulletsim as sim 
import time

app = Flask(__name__)

# Start the robot and its main loop in a separate thread
bsim = sim.Simulation()
robot = arm.Fenrir(bullet=bsim, simulate=True)

def run_robot():
    main.main_loop(robot)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs')
def logs():
    def generate_logs():
        with open('robot_log.txt', 'r') as log_file:
            while True:
                line = log_file.readline()
                if line:
                    yield f"data: {line}\n\n"
                time.sleep(0.1)
    return Response(generate_logs(), mimetype='text/event-stream')

@app.route('/current_variable')
def current_variable():
    return jsonify({"some_variable": robot.some_variable})

@app.route('/trigger', methods=['POST'])
def trigger():
    mode = request.json.get('command')
    if mode:
        if mode == "emergency_stop":
            robot_script.current_mode = "emergency_stop"
            robot_script.interrupt_flag.set()
        else:
            robot_script.current_mode = mode
        return jsonify({"status": "success", "mode": mode})
    return jsonify({"status": "error", "message": "No command received"})

@app.route('/execute', methods=['POST'])
def execute_function():
    function_name = request.json.get('function')
    if function_name == "special_action":
        robot_script.interrupt_flag.set()  # Interrupt any ongoing loop
        robot.execute_special_action()
        return jsonify({"status": "success", "function": function_name})
    return jsonify({"status": "error", "message": "Invalid function name"})

if __name__ == "__main__":
    # Start the robot's main loop in a separate thread
    threading.Thread(target=run_robot, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True)

