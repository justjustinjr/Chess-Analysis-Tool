import numpy as np
from scipy.interpolate import interp1d

def approximate_table(x):
    # Given data points
    x_points = np.array([1, 2, 3, 4])
    y_points = np.array([0.714, 0.703, 0.704, 0.701])
    # Create an interpolation function with extrapolation
    interpolating_function = interp1d(x_points, y_points, kind='linear', fill_value="extrapolate")
    # Return the interpolated or extrapolated value for x
    return float(interpolating_function(x))

def estimate_time(d, k, b, limit, original_side, depth=0, is_original_side_turn=True):
    # Base case: If the depth is greater than or equal to the maximum depth
    if depth >= d:
        return k * limit

    # Time to analyze moves at the current depth
    if is_original_side_turn:
        current_level_time = b * limit
        next_level_time = b * estimate_time(d, k, b, limit, original_side, depth + 1, not is_original_side_turn)
    else:
        current_level_time = limit
        next_level_time = estimate_time(d, k, b, limit, original_side, depth + 1, not is_original_side_turn)

    return current_level_time + next_level_time

