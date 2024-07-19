import numpy as np

# Original list parameters
n = 20
specified_value = 15
original_list = [20] * n
original_sum = sum(original_list)

# Ensure the specified value is within a reasonable range
mean = 20
std_dev = 2  # Adjust this to control the spread

# Generate n//2 - 1 values from a normal distribution (excluding the first and last)
half_values = np.random.normal(mean, std_dev, n//2 - 1)

# Sort the values to ensure a bell curve shape and insert the specified start/end value
sorted_half_values = np.sort(half_values)
first_half = np.insert(sorted_half_values, 0, specified_value)

# Create a symmetric list by mirroring the first half
symmetric_values = np.concatenate((first_half, first_half[::-1]))

# Adjust the symmetric values to have the same total sum as the original list
scaling_factor = (original_sum - 2 * specified_value) / sum(symmetric_values[1:-1])
adjusted_values = symmetric_values[1:-1] * scaling_factor

# Reassemble the full list with the specified start/end values
adjusted_values_full = np.concatenate(([specified_value], adjusted_values, [specified_value]))

# Round the values to the nearest integers
rounded_values = np.round(adjusted_values_full).astype(int)

# Adjust the rounded values to ensure the sum matches the original sum
difference = original_sum - sum(rounded_values)
# rounded_values[-2] += difference  # Adjust the second to last value to compensate

print(rounded_values)
print("sum:", sum(rounded_values))

