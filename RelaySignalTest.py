
import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM numbering
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin number you want to use
gpio_pin = 16

# Set the pin as an output
GPIO.setup(gpio_pin, GPIO.OUT)

# Send a 3-volt signal (HIGH) to the pin
GPIO.output(gpio_pin, GPIO.HIGH)

# Wait for a while
time.sleep(1)

# Turn off the signal
GPIO.output(gpio_pin, GPIO.LOW)

# Clean up the GPIO settings
GPIO.cleanup()
