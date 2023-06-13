import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

# A list to hold max pressure from each trial
max_pressures = []

# Function to process and plot each trial
def plot_trial(file_name, label):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_name)

    # Convert "Force (g)" and "Timestamp" columns to numeric
    df["Force (g)"] = pd.to_numeric(df["Force (g)"], errors='coerce')
    df["Timestamp"] = pd.to_numeric(df["Timestamp"], errors='coerce')

    #Area parameters
    D_exit = 1.25e-2
    area = np.pi * (D_exit / 2)**2 # Exit area of syringe, in meters squared

    rho = 997
    v = 1
    # Convert force to pressure
    df["Pressure (Pa)"] = ((df["Force (g)"]*1.25*9.8/1000) / area) 

    # Remove any rows with NaN values
    df = df.dropna()

    # Trim the data to start at the first non-zero reading and end at the last non-zero reading
    CUTOFF = 0
    df = df[df["Pressure (Pa)"] > CUTOFF]

    # Convert timestamp to relative time (in seconds)
    df['Relative Time (s)'] = df['Timestamp'] - df['Timestamp'].iloc[0]

    # Apply Savitzky-Golay filter to the Pressure
    df['Filtered Pressure (Pa)'] = savgol_filter(df['Pressure (Pa)'], 21, 2) 

    # Find max pressure and add to the list
    max_pressures.append(df['Filtered Pressure (Pa)'].max())

    # Plot the filtered pressure vs time
    plt.plot(df['Relative Time (s)'], df['Filtered Pressure (Pa)'])

# List of CSV files for each trial
# file_names = ['retrofit1.csv', 'retrofit4.csv', 'retrofit5.csv', 'retrofit6.csv', 'retrofit7.csv', 'retrofit8.csv', 'retrofit10.csv']  # Add more file names as needed
file_names = ['millitube1.csv']





# Set the labels and title
fig = plt.figure()
plt.xlabel('Time (s)')
plt.ylabel('Static Pressure (Pa)')
plt.title('Static Pressure vs Time')
# Plot each trial
for i, file_name in enumerate(file_names):
    plot_trial(file_name, f'Trial {i+1}')
# Calculate mean max pressure
mean_max_pressure = np.mean(max_pressures)
plt.axhline(y=mean_max_pressure, color='r', linestyle='-', label='Mean max = {:.2f} Pa'.format(mean_max_pressure))
plt.legend()
plt.savefig('static_pressure.png')

fig2 = plt.figure()
plt.plot(max_pressures, 'o')
plt.axhline(y=mean_max_pressure, color='r', linestyle='-', label='Mean max = {:.2f} Pa'.format(mean_max_pressure))
plt.xlabel('Trial')
plt.ylabel('Max Pressure (Pa)')
plt.title('Max Pressure vs Trial')
plt.legend()
plt.savefig('max_pressure.png')

# Show the plot
plt.show()
