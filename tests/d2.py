import numpy as np

def create_acceleration_curve(total_values, specified_value, ramp_length, high_value):
    # Ensure ramp_length is reasonable
    assert ramp_length * 2 < total_values, "Ramp length is too large for the total number of values."
    
    # Create the ramp down values at the beginning
    ramp_down = np.linspace(high_value, specified_value, ramp_length + 1)[:-1]
    
    # Create the ramp up values at the end
    ramp_up = np.linspace(specified_value, high_value, ramp_length + 1)[1:]
    
    # Fill the middle values with the specified value
    middle_length = total_values - 2 * ramp_length
    middle_values = np.full(middle_length, specified_value)
    
    # Combine all values
    combined_values = np.concatenate((ramp_down, middle_values, ramp_up))
    
    # Round the values to the nearest integers
    rounded_values = np.round(combined_values).astype(int)
    
    return rounded_values

# Parameters
total_values = 30
specified_value = 15
ramp_length = 7
high_value = 53

# Generate the acceleration curve
acceleration_curve = create_acceleration_curve(total_values, specified_value, ramp_length, high_value)
print(acceleration_curve)
print(sum(acceleration_curve))
