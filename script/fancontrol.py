#!/usr/bin/env python3

import subprocess
import time

from gpiozero import OutputDevice


ON_THRESHOLD = 50 * 1000  # (degrees Celsius) Fan kicks on at this temperature.
OFF_THRESHOLD = 45 * 1000  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.
GPIO_PIN = 2  # Which GPIO pin you're using to control the fan.
LED_PIN = 3  # Which GPIO pin you're using to control the LED.


def get_temp():
    """Get the core temperature.

    Read file from /sys to get CPU temp in temp in C *1000

    Returns:
        int: The core temperature in thousanths of degrees Celsius.
    """
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        temp_data = f.read()

    return int(temp_data)


if __name__ == '__main__':
    # Validate the on and off thresholds
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    fan = OutputDevice(GPIO_PIN)
    led = OutputDevice(LED_PIN)

    led.on()
   
    while True:
        temp = get_temp()

        # Start the fan if the temperature has reached the limit and the fan
        # isn't already running.
        # NOTE: `fan.value` returns 1 for "on" and 0 for "off"
        if temp > ON_THRESHOLD and not fan.value:
            fan.on()
            led.off()

        # Stop the fan if the fan is running and the temperature has dropped
        # to 10 degrees below the limit.
        elif fan.value and temp < OFF_THRESHOLD:
            fan.off()
            led.on()

        time.sleep(SLEEP_INTERVAL)

