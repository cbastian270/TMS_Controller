#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import ADS1256
import RPi.GPIO as GPIO

# Define the number of channels
counter = 7

try:
    # Initialize the ADS1256 ADC
    print('here 1')
    ADC = ADS1256.ADS1256()
    print('here 2')
    ADC.ADS1256_init1()
    print('here 3')

    # Start time for measuring execution time
    strt_time = time.time()

    # Generate a timestamp for the filename
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    # Counter for the number of samples
    counter = 0

    # Open the file with timestamp in the name, in append mode
    with open(f"data_{timestamp}.txt", "a") as f:
        # Loop indefinitely to read data
        for _ in range(10):
            # Read data from all channels
            retList = ADC.ADS1256_GetAll(counter)
            counter += 1
            # Print or process the returned list
            print(retList)
            # Write the data to the file
            f.write(retList + '\n')

except Exception as e:
    # Exception handling
    end_time = time.time()
    GPIO.cleanup()

    # Print the summary and exit the program
    # print(f"\r\nProgram end: {counter} samples in {end_time - strt_time} seconds. "
          # f"This is {counter / (end_time - strt_time)} samples per second on {channels} channels.")
    exit()
