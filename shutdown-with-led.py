#!/usr/bin/env python3
#
# Based on:
# https://github.com/Howchoo/pi-power-button
# https://github.com/TonyLHansen/raspberry-pi-safe-off-switch/
#
from gpiozero import Button, LED
from signal import pause
import warnings, os, sys

# GPIO 3 allows the button to be used to power on the Raspberry Pi
offGPIO = int(sys.argv[1]) if len(sys.argv) >= 2 else 3
offtime = int(sys.argv[2]) if len(sys.argv) >= 3 else 6

mintime = 1   # Notice switch after mintime seconds
ledGPIO = 13  # LED GPIO pin

def shutdown(b):
    # Calculate how long the button has been pressed
    p = int(b.pressed_time)
    # Blink rate will increase the longer we hold the button down
    # E.g., at 2 seconds, use a 1/4 second blink rate
    led.blink(on_time=0.5/p, off_time=0.5/p)
    if p > offtime:
        led.off()
        os.system("sudo poweroff")

def when_pressed():
    # Start blinking with 1/2 second rate
    led.blink(on_time=0.5, off_time=0.5)

def when_released():
    # Turn the LED back on when the button is released early
    led.on()

led = LED(ledGPIO)
led.on()

btn = Button(offGPIO, hold_time=mintime, hold_repeat=True)
btn.when_held = shutdown
btn.when_pressed = when_pressed
btn.when_released = when_released

pause()
