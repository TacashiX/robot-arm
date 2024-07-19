from os import access
import numpy as np
from matplotlib import pyplot as plt

def generate_acceleration_curve(min_val, max_val, total_time, num_points=100):
    """
    Generates an acceleration curve.
    
    Parameters:
    - min_val (float): The minimum value of the acceleration.
    - max_val (float): The maximum value of the acceleration.
    - total_time (float): The total time for the acceleration.
    - num_points (int): The number of points in the acceleration curve.
    
    Returns:
    - list: A list containing the acceleration values.
    """
    # Create a time vector from 0 to total_time with num_points elements
    time_vector = np.linspace(0, total_time, num_points)
    
    # Create a quadratic acceleration curve
    acceleration_curve = np.interp(time_vector, 
                                   [0, total_time / 2, total_time], 
                                   [min_val, max_val, min_val])
    
    return acceleration_curve.tolist()

def generate_bell_curve(min_val, max_val, total_time, std_dev_factor=6, num_points=40):

    # Create a time vector from 0 to total_time with num_points elements
    time_vector = np.linspace(0, total_time, num_points)
    
    # Calculate the mean and standard deviation for the Gaussian function
    mean = total_time / 2
    std_dev = total_time / std_dev_factor  # Adjust the std_dev_factor to change the curve shape
    
    # Generate the Gaussian curve
    gaussian_curve = max_val * np.exp(-0.5 * ((time_vector - mean) / std_dev) ** 2)
    
    # Scale the curve to ensure min and max constraints
    gaussian_curve = np.interp(gaussian_curve, (gaussian_curve.min(), gaussian_curve.max()), (min_val, max_val))
    
    return gaussian_curve.tolist()



# Example usage
min_val = 30
max_val = 15
total_time = 1000

#higher = narrower
std_dev_factor = 4

# acceleration_curve = generate_bell_curve(min_val, max_val, total_time)
acceleration_curve = generate_bell_curve(min_val, max_val, total_time, std_dev_factor)

print(acceleration_curve)
plt.plot(acceleration_curve)
plt.show()
