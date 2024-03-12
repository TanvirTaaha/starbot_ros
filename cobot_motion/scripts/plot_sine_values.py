import matplotlib.pyplot as plt
import numpy as np

# Define parameters
amplitude = np.pi / 2  # Amplitude (half pi)
period = 10  # Period in seconds
sampling_rate = 100  # Samples per second

# Calculate time step between samples
dt = 1.0 / sampling_rate

# Create time vector
time = np.arange(0, period, dt)

# Generate sine wave values
sine_values = amplitude * np.sin(2 * np.pi * time / period)

# Create the plot
plt.figure(figsize=(8, 5))  # Adjust figure size as needed
plt.plot(time, sine_values, label='Sine Wave')

# Set plot labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.title('Sine Wave Plot')

# Add grid and legend
plt.grid(True)
plt.legend()

# Show the plot
plt.show()
