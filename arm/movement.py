import arm
from time import sleep
from threading import Thread

home_pos = [84, 40, 140, 100, 180, 90, 90]
last_pos = [84, 40, 140, 100, 180, 90, 90]
default_speed = 1000
servos = []
servos.append(arm.base_servo)
servos.append(arm.j1_servo)
servos.append(arm.j2_servo)
servos.append(arm.j3_servo)
servos.append(arm.j4_servo)
servos.append(arm.j5_servo)
servos.append(arm.gripper_servo)

# def move_j1 (pos):
#     L_off = -7
#     R1_off = 1
#     R2_off = 0


#     arm.j1r2_servo.angle = pos + R2_off
#     arm.j1l_servo.angle = pos + L_off
#     arm.j1r1_servo.angle = abs(pos + R1_off - 180)
    
#     #Finish moving then disable Motors that might cause Strain (L or R1) 
#     sleep(1)
#     arm.j1r1_servo.angle = None
#     print("moved j1")

def basic_move(angles):
    arm.base_servo.angle = angles[0]
    #move_j1(angles[1])
    #Thread(target=move_j1, args=[angles[1]]).run()
    arm.j1_servo.angle = angles[1]
    arm.j2_servo.angle = angles[2]
    arm.j3_servo.angle = angles[3]
    arm.j4_servo.angle = angles[4]
    arm.j5_servo.angle = angles[5]
    arm.gripper_servo.angle = angles[6]
    print("moved everything")
    sleep(1)
    arm.j1_servo.rest()
    global last_pos
    last_pos = angles

def disable_all():
    arm.base_servo.angle = None
    arm.j1r2_servo.angle = None
    arm.j1r1_servo.angle = None
    arm.j1l_servo.angle = None
    arm.j2_servo.angle = None
    arm.j3_servo.angle = None
    arm.j4_servo.angle = None
    arm.j5_servo.angle = None
    arm.gripper_servo.angle = None
    print("servos disabled")

def move(angles, smooth, speed):
    if not smooth:
        basic_move(angles)
    else: 
        global last_pos
        for i in range(len(angles)):
            Thread(target=smooth_move, args=[servos[i], last_pos[i], angles[i], int(speed)]).run()
        print('Last Pos:')
        print(last_pos)
        print('New Pos:')
        print(angles)

        last_pos = angles

def smooth_move(servo, old_pos, new_pos, ms):
    steps = new_pos - old_pos
    if steps > 0:
        for i in range(1,steps+1):
            servo.angle = old_pos + i
            sleep(ms/steps/1000)
    if steps < 0:
        for i in range(-1,steps-1):
            servo.angle = old_pos + i
            sleep(ms/steps/1000)
