import serial
import time
import csv
import numpy as np

ser = serial.Serial('/dev/cu.usbmodem2101', 9600) # Check your COM port

def calculate_pressure(force, area):
    return force / area

def to_resistance(voltage, R_fixed):
    if voltage !=0:
        return (5 - voltage) / (voltage / R_fixed)
    else:
        return 1e6

time.sleep(2) # Wait for the serial connection to initialize

#This is data based on the FSR plot -- change for another pressure sensor
forces = np.array([20, 80, 200, 400, 800, 30, 50]) # Convert from grams to Newtons 
resistances = np.array([70e3, 20e3, 8500, 5000, 3000, 50000, 30e3])

def getFit(forces, resistances):
    log_forces = np.log(forces)
    log_resistances = np.log(resistances)
    coefficients = np.polyfit(log_forces, log_resistances, 1)
    return coefficients

def getForce(force_data, resistance_data, resistance):
    coefficients = getFit(force_data, resistance_data)
    log_resistance = np.log(resistance)
    log_force = (log_resistance - coefficients[1]) / coefficients[0]
    force = np.exp(log_force)
    return force

R_FIXED = 2200 # Fixed resistor in the circuit, in ohms

with open('resistance_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Resistance (Ohms)", "Force (g)"]) # Write the header

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip() # read a '\n' terminated line
            voltage = float(line)
            resistance = to_resistance(voltage, R_FIXED)
            print("Resistance: ", resistance)
            force = getForce(forces, resistances, resistance)
            print("Force: ", force)
            writer.writerow([time.time(), resistance, force]) # Write timestamp and pressure data to the .csv file
