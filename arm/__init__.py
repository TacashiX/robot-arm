from board import SCL, SDA
import busio
import adafruit_rgbled

from adafruit_motor import servo
# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Import GPIO for Button 
import RPi.GPIO as GPIO
from time import sleep

from arm import movement


# CONSTANTS
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


# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency
pca.frequency = 50

#initialize led object
status_led = adafruit_rgbled.RGBLED(pca.channels[RGB_RED_CHANNEL], pca.channels[RGB_GREEN_CHANNEL], pca.channels[RGB_BLUE_CHANNEL], invert_pwm=True)
status_led.color = ORANGE

#Setup GPIO for Button
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Initialize Servos

gripper_servo = servo.Servo(pca.channels[GRIPPER_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180)
j5_servo = servo.Servo(pca.channels[J5_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180)
j4_servo = servo.Servo(pca.channels[J4_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180)
j3_servo = servo.Servo(pca.channels[J3_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180)
j2_servo = servo.Servo(pca.channels[J2_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180)
j1l_servo = servo.Servo(pca.channels[J1L_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180)
j1r2_servo = servo.Servo(pca.channels[J1R2_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180)
j1r1_servo = servo.Servo(pca.channels[J1R1_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180)
base_servo = servo.Servo(pca.channels[BASE_CHANNEL], min_pulse=500, max_pulse=2500, actuation_range=180)


#Done initializing 
status_led.color = GREEN
movement.disable_all()
print("-----------------------------INIT RAN-------------------------------")
