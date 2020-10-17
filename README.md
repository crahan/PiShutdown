# Raspberry Pi shutdown button with LED

This repository is a combination of [Howchoo/pi-power-button](https://github.com/Howchoo/pi-power-button) and [TonyLHansen/raspberry-pi-safe-off-switch](https://github.com/TonyLHansen/). The Python code runs as a systemd service and waits for the button to be pressed. Once pressed it will start a 6-second (default) countdown timer and blink the LED until the timeout has been reached and the Raspberry Pi cleanly shuts down ([video demo](https://raw.githubusercontent.com/crahan/pi-shutdown-button/main/media/demo.mp4)). 

If you use GPIO 3 (default) to detect the button press you can also use the button to boot the Pi. LED is set to GPIO 13. You will need the `gpiozero` Python package which can be installed using `sudo apt install python3-gpiozero`.

As the button and LED each have their own GPIO pin you're free to use either a button with an integrated LED (e.g. [example 1](https://www.aliexpress.com/item/32960427833.html) or [example 2](https://www.aliexpress.com/item/10000308383839.html)) or keep the LED separate.

![gps-plus example](https://raw.githubusercontent.com/crahan/pi-shutdown-button/main/media/inside.jpeg)

![gps-plus example](https://raw.githubusercontent.com/crahan/pi-shutdown-button/main/media/outside.jpeg)
