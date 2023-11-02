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

# label channels 
red_led = pca.channels[2]
green_led = pca.channels[1]
blue_led = pca.channels[0]

#initialize led object
led = adafruit_rgbled.RGBLED(red_led, green_led, blue_led, invert_pwm=True)
#initialize servo 
# probably need to calibrate servos and find proper pulse limits for accurate movements
# servo7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2600)
# also set actuation_range. default is 135
servo15 = servo.Servo(pca.channels[15], min_pulse=500, max_pulse=2500, actuation_range=180)

#Setup GPIO for Button
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Button Loop
while True:
  if GPIO.input(25) == GPIO.HIGH:
    print("No")
    led.color = (255, 50, 0)
    servo15.angle = 90
  elif GPIO.input(25) == GPIO.LOW:
    print("Yep")
    led.color = (0, 100, 0)
    servo15.angle = 0
  sleep(0.15)

#Orange
#led.color = (255, 50, 0)

#Green
#led.color = (0, 100, 0)

#Red 
#led.color = (255, 0, 0)

#should probably use this before shutting down 
#pca.deinit()