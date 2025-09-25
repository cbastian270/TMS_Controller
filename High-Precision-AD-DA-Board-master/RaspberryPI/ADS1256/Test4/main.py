#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import ADS1256_ADC2
import ADS1256_ADC1
import RPi.GPIO as GPIO

try:
    print('I am here 1')
    ADC1 = ADS1256_ADC1.ADS1256()
    ADC2 = ADS1256_ADC2.ADS1256()
    print('I am here 2')
    #DAC = DAC8532.DAC8532()
    print('I am here 3')
    ADC1.ADS1256_init()
    ADC1.ADS1256_init()
    print('I am here 4')
    #DAC.DAC8532_Out_Voltage(0x30, 3)
    #DAC.DAC8532_Out_Voltage(0x34, 3)
    counter = 0
    strt_time = time.time()
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    
    with open(f"data_{timestamp}.txt", "a") as f:
        # Loop indefinitely to read data
        for _ in range(10):
            # Read data from all channels
            retList1 = ADC1.ADS1256_GetAll(counter)
            print('Finished1')
            retList2 = ADC2.ADS1256_GetAll(counter)
            print('Finished2')
           
            counter += 1
            # Print or process the returned list
            print(retList1)
            print(retList2)
            # Write the data to the file
            #f.write(retList + '\n')

except :
    GPIO.cleanup()
    print ("\r\nProgram end     ")
    exit()
