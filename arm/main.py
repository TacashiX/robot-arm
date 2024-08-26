import time
import numpy as np

# from sim import bulletsim

class Fenrir:
    
    RGB_BLUE_CHANNEL = 0
    RGB_GREEN_CHANNEL = 1
    RGB_RED_CHANNEL = 2
    GRIPPER_CHANNEL = 4
    J5_CHANNEL = 5
    J4_CHANNEL = 6
    J3_CHANNEL = 7
    J2_CHANNEL = 11
    J1L_CHANNEL = 12
    J1R2_CHANNEL = 13
    J1R1_CHANNEL = 14
    BASE_CHANNEL = 8

    BUTTON_GPIO = 25
    RED = (255, 0, 0)
    ORANGE = (255, 50, 0)
    GREEN = (0, 100, 0)


    offsets = [0, [1,0,-7],0 ,0 ,0, 0, 0]
    "List of servo offsets, Format: [base, [j1r1,j1r2,j1l], j2, j3, j4, j5, gripper]"
    home_pos = [84, 40, 140, 100, 180, 90, 90]
    curr_pos = [84, 40, 140, 100, 180, 90, 90]
    speed = 15
    "time to move servo 1 degree in ms" 
    accel_minmax = [30,100]
    accel_std_dev = 4
    "higher value -> faster acceleration"

    def __init__(self, bullet, simulate=False):
        self.simulate = simulate
        self.bullet = bullet
        if not self.simulate: 
            from board import SCL, SDA
            import busio
            import adafruit_rgbled
            from adafruit_motor import servo
            from adafruit_pca9685 import PCA9685
            import RPi.GPIO as GPIO

            #Create I2C bus interface and PCA class instance
            i2c_bus = busio.I2C(SCL, SDA)
            self.pca = PCA9685(i2c_bus)
            
            #PMW frequency 
            self.pca.frequency = 50
            
            #LED init 
            self.status_led = adafruit_rgbled.RGBLED(self.pca.channels[self.RGB_RED_CHANNEL], self.pca.channels[self.RGB_GREEN_CHANNEL], self.pca.channels[self.RGB_BLUE_CHANNEL], invert_pwm=True) 
            self.status_led.color = self.ORANGE

            #Set up gpio for button
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            #Initialize servos
            self.servolist = []
            "List of servo objects, Format: [base, [j1r1,j1r2,j1l], j2, j3, j4, j5, gripper]"
            self.servolist.append(servo.Servo(self.pca.channels[BASE_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180))
            self.servolist.append((servo.Servo(self.pca.channels[J1R1_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180), servo.Servo(self.pca.channels[J1R2_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180), servo.Servo(self.pca.channels[J1L_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180)))
            self.servolist.append( servo.Servo(self.pca.channels[J2_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180))
            self.servolist.append(servo.Servo(self.pca.channels[J3_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180))
            self.servolist.append(servo.Servo(self.pca.channels[J4_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180))
            self.servolist.append(servo.Servo(self.pca.channels[J5_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180))
            self.servolist.append(servo.Servo(self.pca.channels[GRIPPER_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180))

            self.status_led.color = self.GREEN

        #if simulate 
        # else: 
            # import ..sim
            # from .. import sim
            #just use robotobj.bullet.update() etc in main script? 
            # self.bullet = sim.Simulation()

    def move_all(self, new_position):
        #check position for validity then move or pass/red light 
        if not self.simulate and self.validate_position(new_position): 
            for i in range(len(self.servolist)):
                if type(self.servolist[i]) == list: 
                    self.move_j1(new_position[i]) 
                else: 
                    self.servolist[i].angle = new_position[i]
        else: 
            self.bullet.updatePosition(new_position)
        self.curr_pos = new_position

    def move_j1(self, pos):
        self.servolist[1][0].angle = abs(pos + self.offsets[1][0] - 180)
        self.servolist[1][1].angle = pos + self.offsets[1][1]
        self.servolist[1][2].angle = pos + self.offsets[1][2]

    def rest_j1(self):
        self.servolist[1][0].angle = None

    def home(self):
        self.move_all(self.home_pos)
        # self.move_arm(self.home_pos)

    def disable_servos(self):
        for servo in self.servolist: 
            if type(servo) == list:
                for s in servo:
                    s.angle = None
            else: 
                servo.angle = None

    def validate_position(self, pos): 
        #for now just 0-180 check, later check for set limits and use bullet collision 
        return all(x >= 0 and x <= 180 for x in pos)

    def generate_accel_curve(self, total_time):
        #calc steps, works in my head. might not work in reality
        steps = int(total_time / ((self.accel_minmax[0] + self.accel_minmax[1])/2))
        #create time vector
        time_vector = np.linspace(0, total_time, steps)
        mean = total_time / 2
        std_dev = total_time / self.accel_std_dev
        #generate curve
        curve = self.accel_minmax[1] * np.exp(-0.5 * ((time_vector - mean) / std_dev) **2)
        #scale curve to respect min and max values and flip
        curve = np.interp(curve, (curve.min(), curve.max()), (self.accel_minmax[1], self.accel_minmax[0]))
        #return array with int values instead of float
        print(f"steps: {steps}, min: {self.accel_minmax[0]}, max: {self.accel_minmax[1]}, total time: {total_time}, stdevfactor: {self.accel_std_dev}")
        print(curve.astype(int).tolist())
        return curve.astype(int).tolist()

    def move_arm(self, new_pos):
        #calc distances
        dist = np.array([(x - y) for x,y in zip(new_pos, self.curr_pos)])
        #total_time from max distance
        total_time = self.speed * abs(max(dist, key=abs))
        if abs(max(dist, key=abs)) < 5:
            self.move_all(new_pos)
            time.sleep(self.accel_minmax[1]/1000)
            return

        #generate curve
        curve = self.generate_accel_curve(total_time)
        step_distance = [ int(x/len(curve)) for x in dist ]
        # step_distance = np.astype(dist/len(curve), int)

        print(f'Current pos: {self.curr_pos}')
        print(f'New Pos    : {new_pos}')
        print(f'Distances  : {dist}')
        print(f'Step dist  : {step_distance}')
        print(f'steps: {len(curve)}')

        for ms in curve: 
            tmp_pos = [ y-1 if x == 0 and y>z else y+1 if x == 0 and y<z else x+y for x,y,z in zip(step_distance, self.curr_pos, new_pos) ]
            # print(f"Curr pos: {self.curr_pos}, Tmp pos: {tmp_pos}, Time: {ms}")
            if np.array_equal(tmp_pos, new_pos):
                print(f"Aborting at {ms}ms delay")
                self.move_all(tmp_pos)
                return

            self.move_all(tmp_pos)
            time.sleep(ms/1000)
        #go again if position not reached
        self.move_arm(new_pos)
