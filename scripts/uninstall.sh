#!/bin/sh
#
# Based on:
# https://github.com/Howchoo/pi-power-button
# https://github.com/TonyLHansen/raspberry-pi-safe-off-switch/
#
set -e

cd "$(dirname "$0")/.."

echo "=> Stopping shutdown listener...\n"
sudo systemctl stop shutdown-with-led
sudo systemctl disable shutdown-with-led

echo "=> Removing shutdown listener...\n"
sudo rm -f /lib/systemd/system/shutdown-with-led.service
sudo rm -f /usr/local/bin/shutdown-with-led.py

echo "Shutdown listener uninstalled.\n"
