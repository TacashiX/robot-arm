# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This simple test outputs a 50% duty cycle PWM single on the 0th channel. Connect an LED and
# resistor in series to the pin to visualize duty cycle changes and its impact on brightness.

from board import SCL, SDA
import busio
import adafruit_rgbled

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 60

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.
# 0xffff turns led off fully, 0 turns it on fully, 
#pca.channels[0].duty_cycle = 0
#pca.channels[1].duty_cycle = 0xffff
#pca.channels[2].duty_cycle = 0xffff

red_led = pca.channels[2]
green_led = pca.channels[1]
blue_led = pca.channels[0]

led = adafruit_rgbled.RGBLED(red_led, green_led, blue_led, invert_pwm=True)

#Orange
led.color = (255, 50, 0)

#Green
#led.color = (0, 100, 0)

#Red 
#led.color = (255, 0, 0)