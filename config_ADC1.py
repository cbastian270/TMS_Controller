# /*****************************************************************************
# * | File        :	  EPD_1in54.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * |	This version:   V1.0
# * | Date        :   2019-01-24
# * | Info        :   
# ******************************************************************************/
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


import spidev
import RPi.GPIO as GPIO
import time

# Pin definition
#RST_PIN         = 25
#CS_PIN          = 26
# CS_DAC_PIN      = 23
#DRDY_PIN        = 12

spi = 0

#SPI0 pins
RST_PIN  = 24
CS_PIN   = 22
DRDY_PIN = 23


# SPI device, bus = 0, device = 0
SPI0 = spidev.SpiDev()
# SPI device, bus = 0, device = 0
#SPI1 = spidev.SpiDev()

def digital_write(pin, value):
    GPIO.output(pin, value)

def digital_read(pin):
    return GPIO.input(DRDY_PIN)

def delay_ms(delaytime):
    time.sleep(delaytime // 1000.0)

def spi_writebyte(data):
    SPI0.writebytes(data)
    
def spi_readbytes(reg):
    return SPI0.readbytes(reg)

def module_init():
    SPI0.open(0, 0)
    #SPI1.open(1, 0)
    print('I am here A')
    GPIO.setmode(GPIO.BCM)
    print('I am here B')
    GPIO.setwarnings(False)
    print('I am here C')
    GPIO.setup(RST_PIN, GPIO.OUT)
    print('I am here D')
    # GPIO.setup(CS_DAC_PIN, GPIO.OUT)
    print('I am here E')
    GPIO.setup(CS_PIN, GPIO.OUT)
    print('I am here F')
    #GPIO.setup(DRDY_PIN, GPIO.IN)
    GPIO.setup(DRDY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print('I am here G')
    SPI0.max_speed_hz = 25000
    #SPI1.max_speed_hz = 25000
    print('I am here H')
    print('I am here I')
    return 0;

### END OF FILE ###
