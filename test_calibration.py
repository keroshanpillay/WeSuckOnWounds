import numpy as np
import pandas as pd

def import_csv_column(filename, column_index):
    df = pd.read_csv(filename)
    column_array = df.iloc[:, column_index].to_numpy()
    return column_array

#Manual Data for FSR 1"
forces_man = np.array([20, 80, 200, 400, 800, 30, 50]) # Convert from grams to Newtons 
resistances_man = np.array([70e3, 20e3, 8500, 5000, 3000, 50000, 30e3])

#Auto data for FST 1"
filename = 'FSR_calibration_data_1inch.csv'
forces = import_csv_column(filename, 0)
resistances = import_csv_column(filename, 1)

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

test_resistance = np.inf

print(getForce(forces, resistances, test_resistance)) 
print(getForce(forces_man, resistances_man, test_resistance))