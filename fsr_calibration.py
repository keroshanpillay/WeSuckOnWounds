import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import serial
import time

# Open a serial connection to the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)

# Known weights in Newtons
weights = np.array([50.0, 163.07, weight3, weight4, weight5, weight6, weight7, weight8, weight9, weight10])
voltages = []

# Fixed resistor in the circuit, in ohms
R_fixed = 10000 

for weight in weights:
    # Countdown timer
    for i in range(10, 0, -1):
        print("PLACE WEIGHT {}. T-{}s".format(weight, i))
        time.sleep(1)

    # Voltage measurement and count-up timer
    print("VOLTAGE MEASUREMENT UNDERWAY. DO NOT TOUCH.")
    voltage_measurements = []
    start_time = time.time()
    while time.time() - start_time < 10:
        if ser.in_waiting:
            voltage = float(ser.readline().strip())
            voltage_measurements.append(voltage)
        # Update time remaining every second
        if int(time.time() - start_time) > len(voltage_measurements):
            print('T+{}s'.format(len(voltage_measurements)))
    voltages.append(np.mean(voltage_measurements))

voltages = np.array(voltages)

# Calculate the resistance of the FSR for each measurement
FSR_resistances = (5 - voltages) / (voltages / R_fixed)

# Fit a line to the resistance vs force data
model = LinearRegression().fit(weights.reshape((-1, 1)), FSR_resistances)

# Print the equation of the line
print('Resistance =', model.coef_[0], '* Force +', model.intercept_)

# Plot the resistance vs force data and the fitted line
plt.scatter(weights, FSR_resistances)
plt.plot(weights, model.predict(weights.reshape((-1, 1))), color='red')
plt.xlabel('Force (N)')
plt.ylabel('Resistance (Ohms)')
plt.title('FSR Resistance vs Force')
plt.show()

ser.close()
