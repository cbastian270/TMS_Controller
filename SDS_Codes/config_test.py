#this script tests the SPI configuration to verify both ADCs are connected

import RPi.GPIO as GPIO
import spidev
import time

# Initialize SPI and GPIO
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 100000
spi.mode = 1
GPIO.setmode(GPIO.BCM)

# Define possible pin configurations
configurations = [
    {'name': 'Config 2', 'cs': 7, 'drdy': 26, 'reset': 19},
    {'name': 'Config 1', 'cs': 22, 'drdy': 23, 'reset': 24},

    # Add more configurations as needed
]

def check_ads1256(config):
    cs = config['cs']
    drdy = config['drdy']
    reset = config['reset']
    
    # Setup pins
    GPIO.setup(cs, GPIO.OUT)
    GPIO.setup(drdy, GPIO.IN)
    GPIO.setup(reset, GPIO.OUT)
    
    GPIO.output(cs, GPIO.HIGH)
    GPIO.output(reset, GPIO.HIGH)
    
    # Reset the device
    GPIO.output(reset, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(reset, GPIO.HIGH)
    time.sleep(0.05)
    
    # Try to read chip ID
    GPIO.output(cs, GPIO.LOW)
    
    # Wait for DRDY
    timeout = time.time() + 0.5
    while GPIO.input(drdy) == GPIO.HIGH:
        if time.time() > timeout:
            GPIO.output(cs, GPIO.HIGH)
            return False
    
    # Read ID register
    spi.xfer2([0x10, 0x00])  # RREG command for STATUS register
    chip_id = spi.xfer2([0x00])[0] >> 4
    
    GPIO.output(cs, GPIO.HIGH)
    
    return chip_id == 3  # ADS1256 ID is 3

try:
    for config in configurations:
        print(f"Testing {config['name']} - CS: {config['cs']}, DRDY: {config['drdy']}, RESET: {config['reset']}")
        
        if check_ads1256(config):
            print(f"✓ ADS1256 FOUND with {config['name']}")
        else:
            print(f"✗ No ADS1256 detected with {config['name']}")
finally:
    GPIO.cleanup()
    spi.close()
