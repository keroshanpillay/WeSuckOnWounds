import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

# Function to process and plot each trial
def plot_trial(file_name, label):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_name)

    # Convert "Force (g)" and "Timestamp" columns to numeric
    df["Force (g)"] = pd.to_numeric(df["Force (g)"], errors='coerce')
    df["Timestamp"] = pd.to_numeric(df["Timestamp"], errors='coerce')

    #Area parameters
    D_exit = 2e-2
    area = np.pi * (D_exit / 2)**2 # Exit area of syringe, in meters squared

    # Convert force to pressure
    df["Pressure (Pa)"] = (df["Force (g)"]*9.8/1000) / area

    # Remove any rows with NaN values
    df = df.dropna()

    # Trim the data to start at the first non-zero reading and end at the last non-zero reading
    CUTOFF = 0
    df = df[df["Pressure (Pa)"] > CUTOFF]

    # Convert timestamp to relative time (in seconds)
    df['Relative Time (s)'] = df['Timestamp'] - df['Timestamp'].iloc[0]

    # Apply Savitzky-Golay filter to the Pressure
    # df['Filtered Pressure (Pa)'] = savgol_filter(df['Pressure (Pa)'], 51, 3) # window size 51, polynomial order 3

    # Plot the filtered pressure vs time
    plt.plot(df['Relative Time (s)'], df['Pressure (Pa)'], label=label)

# List of CSV files for each trial
file_names = ['retrofit1.csv', 'retrofit2.csv', 'retrofit4.csv', 'retrofit5.csv', 'retrofit6.csv', 'retrofit7.csv']  # Add more file names as needed

# Plot each trial
for i, file_name in enumerate(file_names):
    plot_trial(file_name, f'Trial {i+1}')

#Declare parameters
p_min = 40e3 

# Set the labels and title
plt.xlabel('Time (s)')
plt.ylabel('Filtered Pressure (Pa)')
plt.title('Filtered Pressure vs Time')
#plt.axhline(y=p_min, color='r', linestyle='-', label='Desired Pressure')
plt.legend()

# Show the plot
plt.show()
