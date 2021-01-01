#!/usr/bin/env python3
#
# Based on:
# https://github.com/Howchoo/pi-power-button
# https://github.com/TonyLHansen/raspberry-pi-safe-off-switch/
#
import argparse
import logging
import os
import warnings
from signal import pause
from threading import Timer
from gpiozero import Button, LED


class PiShutdownButton:
    """PiShutdownButton."""

    def __init__(
            self,
            gpio_btn,
            gpio_led,
            btn_hold_time=1,
            reset_time=2,
            shutdown_mode_time=3):
        """Initialize a PiShutdownButton object."""
        self.btn = Button(gpio_btn, hold_time=btn_hold_time, hold_repeat=True)
        self.btn.when_held = self.btn_hold
        self.btn.when_pressed = self.btn_press
        self.btn.when_released = self.btn_release

        self.led = LED(gpio_led)
        self.led.on()

        self.shutdown_mode_time = shutdown_mode_time
        self.shutdown_mode = False  # Shutdown mode is active
        self.shutdown_timer = False  # Shutdown timer is active
        self.shutdown_triggered = False  # Shutdown is in progress
        self.reset_time = reset_time
        self.reset_timer = None

    def reset(self):
        """Reset application state."""
        logging.debug('Resetting application state.')
        self.shutdown_mode = False
        self.shutdown_timer = False
        self.shutdown_triggered = False
        self.led.on()

    def btn_hold(self, button):
        """Handle button hold."""
        logging.debug('Button is being held.')
        if not self.shutdown_mode:
            pressed_time = int(button.pressed_time)
            if (pressed_time > self.shutdown_mode_time) and not self.shutdown_mode:
                logging.debug("Entering shutdown mode.")
                self.led.blink(on_time=0.1, off_time=0.1)
                self.shutdown_mode = True

    def btn_press(self):
        """Handle button press."""
        logging.debug('Button is pressed.')
        if not self.shutdown_mode:
            self.led.blink(on_time=0.5, off_time=0.5)

    def btn_release(self):
        """Handle button release."""
        logging.debug('Button is released.')
        if not self.shutdown_mode:
            logging.debug('Turning LED on.')
            # Not in the shutdown mode, turn the LED on
            self.led.on()
        elif not self.shutdown_timer:
            # Shutdown mode is active, start the reset timer
            logging.debug('Starting shutdown timer.')
            self.shutdown_timer = True
            self.reset_timer = Timer(self.reset_time, self.reset)
            self.reset_timer.start()
        elif not self.shutdown_triggered:
            # Shutdown timer is active, initiate shutdown
            logging.debug('Shutting down system.')
            self.shutdown_triggered = True
            self.reset_timer.cancel()
            self.led.off()
            os.system('sudo poweroff')


def main():
    """Start the application."""
    parser = argparse.ArgumentParser()
    # GPIO 3 allows the button to be used to power on the Raspberry Pi
    parser.add_argument('-b', '--button', type=int, default=3, help='Button GPIO pin, defaults to pin 3.')
    parser.add_argument('-l', '--led', type=int, default=13, help='LED GPIO pin, defaults to pin 13.')
    parser.add_argument('-d', '--delay', type=int, default=4, help='Shutdown mode delay, defaults to 4 seconds.')
    parser.add_argument('-r', '--reset', type=int, default=2, help='Shutdown mode reset time, defaults to 2 seconds.')
    parser.add_argument('--loglevel', type=str, default='INFO', help='Log level, defaults to INFO.')
    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {args.loglevel}')
    logging.basicConfig(level=numeric_level)

    _button = PiShutdownButton(
        args.button,
        args.led,
        btn_hold_time=1,
        reset_time=args.reset,
        shutdown_mode_time=args.delay
    )

    pause()


if __name__ == "__main__":
    main()
