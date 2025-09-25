

import spidev
import RPi.GPIO as GPIO
import time


#Pin definition for AD 1
RST_PIN         = 24           # brown 
CS_PIN          = 22           # grey (GPIO pin, physical pin 15)
DRDY_PIN        = 23            # white

#currSPI = 0
# SPI device, bus = 0, device = 0
SPI = spidev.SpiDev(0, 0)
SPI.mode = 1                        # set SPI Mode

def digital_write(pin, value):
    GPIO.output(pin, value)

def digital_read(pin):
    return GPIO.input(DRDY_PIN)

def delay_ms(delaytime):
    #time.sleep(delaytime // 1000000.0)     #original time delay
    time.sleep(delaytime // 10000.0)         # reduced time delay

def spi_writebyte(data):
    SPI.writebytes(data)

def spi_readbytes(reg):
    return SPI.readbytes(reg)
    

def module_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RST_PIN, GPIO.OUT)
    GPIO.setup(CS_PIN, GPIO.OUT)
    #GPIO.setup(DRDY_PIN, GPIO.IN)
    GPIO.setup(DRDY_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    SPI.max_speed_hz = 100000
    SPI.mode = 0b01
    return 0;
    
    

