import numpy as np

def create_acceleration_curve_non_linear(total_values, specified_value, ramp_length, high_value):
    # Ensure ramp_length is reasonable
    assert ramp_length * 2 < total_values, "Ramp length is too large for the total number of values."
    
    # Create the exponential decay for the ramp down
    ramp_down = high_value * np.exp(-np.linspace(0, 1, ramp_length))
    ramp_down = np.append(ramp_down[:-1], specified_value)  # Append specified value at the end

    # Create the exponential growth for the ramp up
    ramp_up = high_value * np.exp(np.linspace(-1, 0, ramp_length))
    ramp_up = np.append(specified_value, ramp_up[1:])  # Prepend specified value at the start

    # Fill the middle values with the specified value
    middle_length = total_values - 2 * ramp_length
    middle_values = np.full(middle_length, specified_value)

    # Combine all values
    combined_values = np.concatenate((ramp_down, middle_values, ramp_up))

    # Round the values to the nearest integers
    rounded_values = np.round(combined_values).astype(int)

    return rounded_values

# Parameters
total_values = 40
specified_value = 15
ramp_length = 13
high_value = 63

# Generate the acceleration curve
acceleration_curve = create_acceleration_curve_non_linear(total_values, specified_value, ramp_length, high_value)
print(acceleration_curve)

