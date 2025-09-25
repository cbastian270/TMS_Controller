#this is the main loop for the SDS data aquisition

import time
import ADS1256_1 as ADS1256
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
import os

adcpin1 = []
counter = 0
retString = ""
channels = 5

#Setup for ADS input
ADC = ADS1256.ADS1256()
ADC.ADS1256_init()
strt_time = time.time()
cur_time = strt_time

# Grab the data from the ADS
retList = ADC.ADS1256_GetAll()
end_time = time.time()
GPIO.cleanup()
with open("data.txt", "w") as f:
    f.write(str(retList))
f.close()

#################################################################################################

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

separate_files('data.txt')          # run script


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


# need to examine fft frequency calculations
# fix sampling fequency calculations
# establish conversion values for voltage and current 

