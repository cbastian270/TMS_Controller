import tkinter as tk
import RPi.GPIO as GPIO
import threading
import time
import ADS1256

class TMG_GUI:
    def __init__(self, master):
        self.master = master
        master.title("SMART DECISION SYSTEM")
        master.configure(background='black')

        self.create_toggle_switches()
        self.create_adc_readings()

        # Initialize ADS1256
        self.ADC = ADS1256.ADS1256()
        self.ADC.ADS1256_init()

        # Start reading ADC channels in a separate thread
        self.read_adc_thread = threading.Thread(target=self.read_adc_loop)
        self.read_adc_thread.daemon = True
        self.read_adc_thread.start()

    def create_toggle_switches(self):
        switch_frame = tk.Frame(self.master)
        switch_frame.pack()

        self.switch_states = []  # List to store the state of each toggle switch

        for i in range(6):
            state = tk.BooleanVar()
            state.set(False)  # Initial state is off
            self.switch_states.append(state)

            switch = tk.Checkbutton(switch_frame, text=f"Switch {i+1}", variable=state, command=lambda idx=i: self.toggle_switch_state(idx))
            switch.pack(side=tk.TOP, padx=5, pady=5)

    def create_adc_readings(self):
        readings_frame = tk.Frame(self.master, bg="black")
        readings_frame.pack()

        # Create ADC readings for Power Demand
        power_demand_frame = tk.Frame(readings_frame, bg="black")
        power_demand_frame.pack(side=tk.LEFT, padx=5, pady=5)

        self.power_demand_readings = []
        for i in range(3):
            adc_reading = tk.StringVar()
            adc_reading.set("X")
            self.power_demand_readings.append(adc_reading)

            label = tk.Label(power_demand_frame, text=f"Power Demand Load {i+1} :", fg="white", bg="black")
            label.pack(pady=5)

            entry = tk.Entry(power_demand_frame, textvariable=adc_reading, state="readonly", fg="white", bg="black", bd=0, highlightthickness=0)
            entry.pack(pady=5)

        # Create ADC readings for Voltage
        voltage_frame = tk.Frame(readings_frame, bg="black")
        voltage_frame.pack(side=tk.LEFT, padx=5, pady=5)

        self.voltage_readings = []
        for i in range(3):
            adc_reading = tk.StringVar()
            adc_reading.set("X")
            self.voltage_readings.append(adc_reading)

            label = tk.Label(voltage_frame, text=f"Voltage Load {i+1} :", fg="white", bg="black")
            label.pack(pady=5)

            entry = tk.Entry(voltage_frame, textvariable=adc_reading, state="readonly", fg="white", bg="black", bd=0, highlightthickness=0)
            entry.pack(pady=5)
            
        # Create ADC readings for Current
        current_frame = tk.Frame(readings_frame, bg="black")
        current_frame.pack(side=tk.LEFT, padx=5, pady=5)

        self.current_readings = []
        for i in range(3):
            adc_reading = tk.StringVar()
            adc_reading.set("X")
            self.current_readings.append(adc_reading)

            label = tk.Label(current_frame, text=f"Current Load {i+1} :", fg="white", bg="black")
            label.pack(pady=5)

            entry = tk.Entry(current_frame, textvariable=adc_reading, state="readonly", fg="white", bg="black", bd=0, highlightthickness=0)
            entry.pack(pady=5)

        # Create ADC readings for Phase Angle
        phase_angle_frame = tk.Frame(readings_frame, bg="black")
        phase_angle_frame.pack(side=tk.LEFT, padx=5, pady=5)

        self.phase_angle_readings = []
        for i in range(3):
            adc_reading = tk.StringVar()
            adc_reading.set("X")
            self.phase_angle_readings.append(adc_reading)

            label = tk.Label(phase_angle_frame, text=f"Phase Angle Load {i+1} :", fg="white", bg="black")
            label.pack(pady=5)

            entry = tk.Entry(phase_angle_frame, textvariable=adc_reading, state="readonly", fg="white", bg="black", bd=0, highlightthickness=0)
            entry.pack(pady=5)

    def toggle_switch_state(self, pin):
        state = self.switch_states[pin].get()
        print(f"Switch {pin+1} state: {'ON' if state else 'OFF'}")

    def read_adc_loop(self):
        while True:
            # Read all ADC channels
            retList = self.ADC.ADS1256_GetAll()

            # Update ADC readings in the GUI
            for i in range(3):
                self.power_demand_readings[i].set(str(retList[i]))
                self.voltage_readings[i].set(str(retList[i+3]))
                self.current_readings[i].set(str(retList[i+6]))
                self.phase_angle_readings[i].set(str(retList[i+9]))

            # Adjust the sleep time as needed based on the desired update frequency
            time.sleep(1)  # Update frequency: 1 second

root = tk.Tk()
gui = TMG_GUI(root)

root.mainloop()


