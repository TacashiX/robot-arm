from flask import Flask, render_template, Response, send_from_directory, request, jsonify
import time
import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# Custom static data
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
        print(f"updated config: {data}")
        print(f'{data["min"]}')
        return Response(status=204)
    else: 
        current_config = { "min": 1, "max": 2, "speed": 3, "stdev":4 } 
        return current_config

@app.route('/setmode',methods=['POST'])
def setmode():
    #set mode
    m = request.get_json()
    print(f"Set mode to {m['mode']}") 
    return Response(status=204)

@app.route('/home')
def home(): 
    print("moving home")
    return Response(status=204)

@app.route('/grip', methods=['POST'])
def grip():
    data = request.get_json()
    print(f'{data["pos"]}')
    return Response(status=204)

@app.route('/movecoords', methods=['POST'])
def movecoord():
    data = request.get_json()
    print (f"moving to {data['coords']}. {data['smooth']=}")
    return Response(status=204)

@app.route('/moveangles', methods=['POST'])
def moveangles():
    data = request.get_json()
    print (f"moving to {data['angles']}. {data['smooth']=}")
    return Response(status=204)


if __name__ == "__main__":
    # subprocess.Popen(['firefox', 'localhost:5000'])
    app.run(host='0.0.0.0', port=5000, debug=True)
    

