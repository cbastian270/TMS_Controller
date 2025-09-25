#this script manually closes the breakers to put the UPS on power and activates the output of the non-critial outlets

import tkinter as tk
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Define GPIO pins for each switch (modify as needed)
gpio_pins = [27, 12, 5, 6, 16, 13] #13, 32, 29, 31, 36, 33

def toggle_switch_state(pin):
    state = switch_states[pin].get()
    GPIO.output(gpio_pins[pin], not state)  # Reverse state since GPIO output is opposite of switch state

def create_toggle_switches(root):
    switch_frame = tk.Frame(root)
    switch_frame.pack()

    for i in range(6):
        state = tk.BooleanVar()
        state.set(False)  # Initial state is off
        switch_states.append(state)

        switch = tk.Checkbutton(switch_frame, text=f"Switch {i+1}", variable=state, command=lambda idx=i: toggle_switch_state(idx))
        switch.pack(side=tk.TOP, padx=5, pady=5)

def main():
    root = tk.Tk()
    root.title("Manual Control")

    create_toggle_switches(root)

    root.mainloop()

if __name__ == "__main__":
    switch_states = []  # List to store the state of each toggle switch

    # Set up GPIO pins as outputs
    for pin in gpio_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)  # Set initial state to high (off)

    main()
