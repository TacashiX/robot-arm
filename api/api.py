from flask import Flask, jsonify, request
from flask_cors import CORS
import arm
import arm.movement

app = Flask(__name__)
CORS(app)

@app.route("/api")
def hell():
    return "Hello, World!"

@app.route("/api/basic", methods=['POST'])
def basic():
    data = request.get_json()
    
    #arm.movement.basic_move(data['angles'])
    arm.movement.move(data['angles'], data['smoothing'], data['speed'])
    
    return data['angles']
    #return '', 204

@app.route("/api/disable", methods=['POST'])
def hello_world():
    #arm.j3_servo.angle
    arm.movement.disable_all()
    return '', 204

@app.route("/api/home", methods=['POST'])
def arm_home():
    data = request.get_json()
    arm.movement.move(arm.movement.home_pos, data['smoothing'], data['speed'])
    #arm.movement.basic_move(arm.movement.home_pos)

#Gotta add verification that speed is not null