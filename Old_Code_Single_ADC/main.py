#!/usr/bin/python
# -*- coding:utf-8 -*-
###########################################GUI####################################################






############################################SAMPLING###############################################


import time
import ADS1256
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
import os

adcpin1 = []
counter = 0
retString = ""
channels = 5

#Setup for ADS
ADC = ADS1256.ADS1256()
ADC.ADS1256_init()
strt_time = time.time()
cur_time = strt_time

#What actually starts it
retList = ADC.ADS1256_GetAll()
end_time = time.time()
GPIO.cleanup()
with open("data.txt", "w") as f:
    f.write(str(retList))
f.close()

#################################################FFT################################################

import numpy as np
import matplotlib.pyplot as plt

def separate_files(input_file):
    # Open the input file
    with open(input_file, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Extract the first value from the line
            first_value = line.strip().split()[0]
            
            # Define the output file name based on the first value
            output_file = f"{first_value}.txt"
            
            # Write the line to the appropriate output file
            with open(output_file, 'a') as out_file:
                out_file.write(line)

separate_files('data.txt')
'''
for i in range(5):
    # Load data from CSV file
    file_name = f'{i},.txt'
    fftdata = np.loadtxt(file_name, delimiter=',')

    # Extract time and sample value columns
    time = fftdata[:, 1]
    samples = fftdata[:,2]
        
    # Perform Fast Fourier Transform (FFT)
    Fs = 1 / (time[1] - time[0])  # Sampling frequency
    L = len(samples)  # Length of signal
    Y = np.fft.fft(samples)
    print(Y)
    # Plot the original signal
    #plt.figure(1)
    #plt.subplot(3, 1, 1)
    #plt.plot(time, samples)
    #plt.title('Original Signal')
    #plt.xlabel('Time (s)')
    #plt.ylabel('Amplitude')
    # Save the figure containing the original signal
    #plt.savefig('original_signal.png')

    # Compute the one-sided spectrum
    P2 = np.abs(Y / L)
    P1 = P2[:L//2+1]
    P1[1:-1] = 2 * P1[1:-1]
    freq = Fs * np.arange(0, L/2+1) / L
    print(freq)
    # Perform Inverse Fast Fourier Transform (IFFT)
    reconstructed_signal = np.fft.ifft(Y)
    print(reconstructed_signal)

    # Plot the one-sided FFT spectrum
    #plt.subplot(3, 1, 2)
    #plt.plot(freq, P1)              
    #plt.title('One-Sided Amplitude Spectrum of Signal')
    #plt.xlabel('Frequency (Hz)')
    #plt.ylabel('Amplitude')

    # Plot the reconstructed signal from IFFT
    #plt.subplot(3, 1, 3)
    #plt.plot(time, np.real(reconstructed_signal))
    #plt.title('Reconstructed Signal from IFFT')
    #plt.xlabel('Time (s)')
    #plt.ylabel('Amplitude')
    # Save the figure containing both the FFT spectrum and the reconstructed signal
    #plt.savefig('fft_and_reconstructed_signal.png')

    # Plot the reconstructed signal from IFFT overlayed
    #plt.figure(2)
    #plt.plot(time, samples, label='Original')
    #plt.plot(time, np.real(reconstructed_signal), 'r', label='Reconstructed')
    #plt.legend()
    #plt.title('Overlay of Original and Reconstructed Signals')
    #plt.xlabel('Time (s)')
    #plt.ylabel('Amplitude')
    # Save the overlay plot
    #plt.savefig('overlayed_signals.png')


#print ("\r\nProgram end: " + str(counter) + " samples in " + str(end_time - strt_time) + " seconds. This is " + str(counter / (end_time - strt_time)) + " samples per second on " + str(channels) + " channels.")

'''

# Function to calculate RMS value
def rms(signal):
    rms_out = np.sqrt(np.mean(signal**2))
    #print(rms_out)
    return rms_out
    
# setup plot to visualize results    
fig, axes = plt.subplots(2,3, figsize=(15,8))
fig.tight_layout(pad=3.0)
axes = axes.flatten()
    

for i in range(6):
    dataNumber = i+1
    # Load data from CSV file
    file_name = f'{dataNumber},.txt'
    fftdata = np.loadtxt(file_name, delimiter=',')
    
        
    # Extract time and sample value columns
    time = fftdata[:, 1]                # Column 2
    value = fftdata[:, 2]               # Column 3
    #print(fftdata)
  
    # Compute the average time difference between consecutive samples
    average_time_difference = np.mean(np.diff(time))
    print("Avg Time Diff:" + str(average_time_difference))
    
    # Calculate the sampling frequency
    Fs = 1 / average_time_difference        
    L = len(value)  # Length of signal      
    Y = np.fft.fft(value) 

    # Compute the one-sided spectrum
    P2 = np.abs(Y / L)
    P1 = P2[:L//2+1]
    P1[1:-1] = 2 * P1[1:-1]
    freq = Fs * np.arange(0, L/2+1) / L

    # Find the dominant frequency
    dominant_freq = freq[np.argmax(P1)]
   
    # Compute RMS values
    rms_value = rms(value)
    print(f"RMS Value: {rms_value:.2f}")
    print(f"Dominant Frequency: {dominant_freq:.2f} Hz")
    
    axes[i].plot(time, value)
    axes[i].set_title(f'Subplot Channel {i}')
    axes[i].set_ylabel('Values')
    axes[i].set_xlabel('Time')
    axes[i].grid(True)
    

plt.show()                          # show the plot created in the loop above

# List of file paths to delete
file_paths = ["1,.txt", "2,.txt", "3,.txt", "4,.txt", "5,.txt", "6,.txt"]

# Iterate over each file path
for file_path in file_paths:
    # Check if the file exists before attempting to delete it
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"{file_path} does not exist.")


# need to convert dataq samples to voltages before RMS conversion 
# need to find the current measurments 
# need to figure out issue with channel 0 (returns zero, could be current)
# need to examine fft frequency calculations
# fix sampling fequency calculations
# need to connect to second A-D converter, the GPIO addressing is wrong
# need pin to value mapping 
# setup share SPI bus 
# establish conversion values for voltage and current 

