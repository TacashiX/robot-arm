import time
import numpy as np
import logging
import ikpy.chain
log = logging.getLogger(__name__)

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
    home_pos = [84, 40, 140, 100, 180, 90]
    chain_home_pos = [ 0, -1.675516266666666, 0, 0,-0.872664444444444, 0, 0.872664444444444, 0, 1.745329444444444, 0,  0.785398000000000, 0, 1.570796, 0, 0]
    curr_pos = [84, 40, 140, 100, 180, 90]
    speed = 15
    "time to move servo 1 degree in ms" 
    accel_minmax = [30,100]
    accel_std_dev = 4
    "higher value -> faster acceleration"
    orientation_axis = "X"
    target_orientation = [0,0,1]
    gripper_limit = [0,50]
    gripper_pos = 20
    mode = "M"
    "Current mode. M | C | E (Manual, Controller, Error Stop)" 
    coords = [0,-0.15,0.2]

    def __init__(self, bullet=None, simulate=False, urdf_path="model/Fenrir.urdf"):
        self.simulate = simulate
        self.bullet = bullet
        self.urdf_path = urdf_path
        #Init IK chain
        self.ikchain = ikpy.chain.Chain.from_urdf_file(urdf_path, base_elements=["base_link"],active_links_mask=[False, True, False, False, True, False, True, False, True, False, True, False, True, False, False])
        self.ikpos = self.chain_home_pos #home pos in radian here


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
            log.info("Fenrir initialized")

    def move_all(self, new_position):
        #check position for validity then move or pass/red light 
        if not self.simulate and self.validate_position(new_position): 
            for i in range(len(self.servolist)):
                if type(self.servolist[i]) == list: 
                    self.move_j1(new_position[i]) 
                else: 
                    self.servolist[i].angle = self.apply_limit(new_position[i] + self.offsets[i], 0, 180, dec=0)
        else: 
            self.bullet.updatePosition(new_position)
        self.curr_pos = new_position

    def grip(self, step):
        tmp_pos = self.apply_limit(self.gripper_pos + step, self.gripper_limit[0],self.gripper_limit[1],dec=0)
        if not self.simulate:
            self.servolist[6].angle = tmp_pos
        else: 
            log.info(f"Moving gripper {step} steps to {tmp_pos}")
        self.gripper_pos = tmp_pos

    def move_j1(self, pos):
        self.servolist[1][0].angle = abs(pos + self.offsets[1][0] - 180)
        self.servolist[1][1].angle = pos + self.offsets[1][1]
        self.servolist[1][2].angle = pos + self.offsets[1][2]

    def rest_j1(self):
        self.servolist[1][0].angle = None

    def home(self):
        log.info(f"Moving to home position {self.home_pos}")
        self.move_all(self.home_pos)
        self.ikpos = self.chain_home_pos
        # self.move_arm(self.home_pos)

    def disable_servos(self):
        log.info("Disabling servos")
        if not self.simulate:
            for servo in self.servolist: 
                if type(servo) == list:
                    for s in servo:
                        s.angle = None
                else: 
                    servo.angle = None

    def validate_position(self, pos): 
        #for now just 0-180 check, later check for set limits and use bullet collision 
        valid = all(x >= 0 and x <= 180 for x in pos)
        if not valid: 
            log.warning(f"position {pos} is not valid, aborting movement")

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
        log.debug(f"steps: {steps}, min: {self.accel_minmax[0]}, max: {self.accel_minmax[1]}, total time: {total_time}, stdevfactor: {self.accel_std_dev}")
        log.debug(f'Acc curve: {curve.astype(int).tolist()}')
        return curve.astype(int).tolist()

    def move_arm(self, new_pos):
        #calc distances
        log.info(f'Moving arm to {new_pos} from {self.curr_pos}')
        dist = np.array([(x - y) for x,y in zip(new_pos, self.curr_pos)])
        #total_time from max distance
        total_time = self.speed * abs(max(dist, key=abs))
        if abs(max(dist, key=abs)) < 6:
            log.debug('Less than 5 degrees remaining, finishing movement')
            self.move_all(new_pos)
            time.sleep(self.accel_minmax[1]/1000)
            return

        #generate curve
        curve = self.generate_accel_curve(total_time)
        step_distance = [ int(x/len(curve)) for x in dist ]

        log.debug(f'{self.curr_pos=}')
        log.debug(f'{new_pos=}')
        log.debug(f'{dist=}')
        log.debug(f'{step_distance=}')
        log.debug(f'steps: {len(curve)}')

        for ms in curve: 
            tmp_pos = [ y-1 if x == 0 and y>z else y+1 if x == 0 and y<z else x+y for x,y,z in zip(step_distance, self.curr_pos, new_pos) ]
            if np.array_equal(tmp_pos, new_pos):
                log.debug("finishing movement in main pass")
                self.move_all(tmp_pos)
                return

            self.move_all(tmp_pos)
            time.sleep(ms/1000)
        #go again if position not reached
        log.debug("position not reached, going again")
        self.move_arm(new_pos)


    def move_coord(self, coords, smooth=False): 
        # log.debug(f"chain: {self.ikchain}, {self.ikpos=}, {coords=}")
        r = self.ikchain.inverse_kinematics(coords, self.target_orientation, orientation_mode=self.orientation_axis,initial_position=self.ikpos)
        self.ikpos = r
        self.coords = coords
        if not smooth:
            self.move_all(self.chain_to_deg(r))
        else:
            self.move_arm(self.chain_to_deg(r))


    def button_pressed(self): 
        if not self.simulate:
            if GPIO.input(self.BUTTON_GPIO) == GPIO.LOW:
                log.debug("Button pressed")
                return True
            else:
                return False
        else:
            return False
    
    def apply_limit(self,val, min_val, max_val, dec=3):
        if dec > 0: 
            return round(max(min(val, max_val),min_val),dec)
        else: 
            return int(round(max(min(val, max_val),min_val),dec))

    def chain_to_deg(self, rad_positions):
        #might have to invert some values, no idea how physical servos are oriented
        scaled_degrees = []
        for i in [1,4,6,8,10,12]:
            max_rad = self.ikchain.links[i].bounds[1]
            min_rad = self.ikchain.links[i].bounds[0]
            scaled_deg = 180* (rad_positions[i] - min_rad) / (max_rad - min_rad)
            scaled_degrees.append(int(scaled_deg))
        # scaled_degrees.append(0)
        return scaled_degrees
