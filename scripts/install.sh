#!/bin/sh
#
# Based on:
# https://github.com/Howchoo/pi-power-button
# https://github.com/TonyLHansen/raspberry-pi-safe-off-switch/
#
set -e

echo "=> Installing shutdown listener...\n"
sudo cp shutdown-with-led.py /usr/local/bin/
sudo chmod 755 /usr/local/bin/shutdown-with-led.py
sudo chown root:root /usr/local/bin/shutdown-with-led.py

echo "=> Starting shutdown listener...\n"
sudo cp shutdown-with-led.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/shutdown-with-led.service
sudo chown root:root /lib/systemd/system/shutdown-with-led.service
sudo systemctl enable shutdown-with-led
sudo systemctl start shutdown-with-led

echo "Done."
