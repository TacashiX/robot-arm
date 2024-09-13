from flask import Flask, render_template, Response, send_from_directory
import time
import subprocess

app = Flask(__name__)

somevar = "whaddup"

def generate_logs():
    # Assuming your robot's script is `robot_script.py`
    # Replace this with how you run your robot's code
    process = subprocess.Popen(['python3', '../../entry.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield f"data: {line.decode()}\n\n"
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html', somevar=somevar)

# Custom static data
@app.route('/model/<path:filename>')
def custom_static(filename):
    return send_from_directory('../../../robot-arm/model/', filename)

# @app.route('')
# def logs():
#     return Response(generate_logs(), mimetype='text/event-stream')

if __name__ == "__main__":
    # subprocess.Popen(['firefox', 'localhost:5000'])
    app.run(host='0.0.0.0', port=5000, debug=True)
    

