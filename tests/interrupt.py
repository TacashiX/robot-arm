#!/usr/bin/env python3
import signal
import sys
import RPi.GPIO as GPIO
BUTTON_GPIO = 25


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    print("Button pressed!")

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # takes gpio pin, FALLING/RISING/BOTH, function to call when interrupt is triggered and optionally bounce time to trigger only once and disable for x milliseconds
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, 
            callback=button_pressed_callback, bouncetime=200)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()