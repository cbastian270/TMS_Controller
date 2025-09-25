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

# Pin definition BY PHYSICAL PIN NUMBER
RST_PIN0  = 24
CS_PIN0   = 22
DRDY_PIN0 = 23
RST_PIN1  = 25
CS_PIN1   = 26
DRDY_PIN1 = 12

#Initialize SPI0 and SPI1
SPI0 = spidev.SpiDev()
SPI1 = spidev.SpiDev()

##ADC 0
# SPI device, bus = 0, device = 0
def digital_write(pin, value):
    GPIO.output(pin, value)

def digital_read(pin):
    return GPIO.input(DRDY_PIN0)

def delay_ms(delaytime):
    time.sleep(delaytime // 10000.0)



def spi_writebyte0(data):
    SPI0.writebytes(data)
    
def spi_readbytes0(reg):
    return SPI0.readbytes(reg)
    
##ADC 1
# SPI device, bus = 1, device = 0


def spi_writebyte1(data):
    SPI1.writebytes(data)
    
def spi_readbytes1(reg):
    return SPI1.readbytes(reg)

def module_init():
    SPI0.open(0, 0)
    SPI1.open(1, 0)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RST_PIN0, GPIO.OUT)
    GPIO.setup(CS_PIN0, GPIO.OUT)
    GPIO.setup(RST_PIN1, GPIO.OUT)
    GPIO.setup(CS_PIN1, GPIO.OUT)
    GPIO.setup(DRDY_PIN0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DRDY_PIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    SPI0.max_speed_hz = 25000
    SPI1.max_speed_hz = 25000
    SPI0.mode = 0b01
    SPI1.mode = 0b10
    return 0;

### END OF FILE ###
