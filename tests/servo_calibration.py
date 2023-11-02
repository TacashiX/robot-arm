from board import SCL, SDA
import busio
import adafruit_rgbled

from adafruit_motor import servo
# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Import GPIO for Button 
import RPi.GPIO as GPIO
from time import sleep

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 50

#initialize servo 
# probably need to calibrate servos and find proper pulse limits for accurate movements
# servo7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2600)
# also set actuation_range. default is 135
servo15 = servo.Servo(pca.channels[15], min_pulse=500, max_pulse=2500, actuation_range=180)
servo12 = servo.Servo(pca.channels[12], min_pulse=500, max_pulse=2500, actuation_range=180)
servo14 = servo.Servo(pca.channels[14], min_pulse=500, max_pulse=2500, actuation_range=180)


def move_j1 (pos):
    L_off = -7
    R1_off = 1
    R2_off = 0

    servo15.angle = pos + R2_off
    servo12.angle = pos + L_off
    servo14.angle = abs(pos + R1_off - 180)
    #Finish moving then disable Motors that might cause Strain (L or R1) 
    sleep(2)
    servo14.angle = None
    servo12.angle = None
move_j1(90)


