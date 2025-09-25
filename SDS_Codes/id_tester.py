#this script tests SPI identities and confirms there is a device there with a response

import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BCM)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000
spi.mode = 1

def test_both_devices():
    # Define pins for both devices
    devices = [
        #{"cs": 2, "drdy": 4, "reset": 26},
        #{"cs": 22, "drdy": 23, "reset": 24}
        {"cs": 7, "drdy": 26, "reset": 19},       # cs is grey, reset is brown, drdy is white
        {"cs": 22, "drdy": 23, "reset": 24}
    ]
 
    
    for i, dev in enumerate(devices):
        # Setup pins
        GPIO.setup(dev["cs"], GPIO.OUT)
        GPIO.setup(dev["drdy"], GPIO.IN)
        GPIO.setup(dev["reset"], GPIO.OUT)
        
        # Reset device
        GPIO.output(dev["cs"], GPIO.HIGH)
        GPIO.output(dev["reset"], GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(dev["reset"], GPIO.HIGH)
        time.sleep(0.05)
        
        # Select device
        GPIO.output(dev["cs"], GPIO.LOW)
        
        # Wait for DRDY
        timeout = time.time() + 0.5
        drdy_ok = False
        while GPIO.input(dev["drdy"]) == GPIO.HIGH:
            if time.time() > timeout:
                break
            drdy_ok = True
        
        # Read ID register
        spi.xfer2([0x10, 0x00])  # RREG command for STATUS register
        chip_id = spi.xfer2([0x00])[0] >> 4
        
        # Deselect device
        GPIO.output(dev["cs"], GPIO.HIGH)
        
        print(f"Device {i+1}: DRDY responded: {drdy_ok}, Chip ID: {chip_id}")

test_both_devices()
