import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.ndimage import gaussian_filter1d

df = pd.read_json("data.json")
df = df[(df['x'] != 0) | (df['y'] != 0)]
df['date'] = pd.to_datetime(df['date'])

# Smooth the x and y coordinates to simulate the racing line more smoothly
x_smoothed = gaussian_filter1d(df['x'], sigma=2)
y_smoothed = gaussian_filter1d(df['y'], sigma=2)

track_width = 100  # Adjust based on your data scale

dx = np.gradient(x_smoothed)
dy = np.gradient(y_smoothed)
normals = np.vstack([-dy, dx])
norm_length = np.sqrt(normals[0]**2 + normals[1]**2 + 1e-6)
normals /= norm_length

outer_bound_x = x_smoothed + normals[0] * (track_width / 2)
outer_bound_y = y_smoothed + normals[1] * (track_width / 2)
inner_bound_x = x_smoothed - normals[0] * (track_width / 2)
inner_bound_y = y_smoothed - normals[1] * (track_width / 2)

# For the spline fitting, we'll focus on a unified approach rather than fitting X on Y and Y on X separately.
# This means choosing either X or Y as the independent variable based on the track orientation.

# Assuming the track is more horizontally oriented:
# Prepare data for spline fitting by sorting by the independent variable (X in this case)
indices_sorted = np.argsort(x_smoothed)
x_sorted = x_smoothed[indices_sorted]
y_outer_sorted = outer_bound_y[indices_sorted]
y_inner_sorted = inner_bound_y[indices_sorted]

# Fit splines to the sorted data
spline_outer = UnivariateSpline(x_sorted, y_outer_sorted, s=10)  # Adjust 's' as needed for smoothness
spline_inner = UnivariateSpline(x_sorted, y_inner_sorted, s=10)

# Generate fitted curves
x_fitted = np.linspace(x_sorted.min(), x_sorted.max(), 1000)
y_outer_fitted = spline_outer(x_fitted)
y_inner_fitted = spline_inner(x_fitted)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['x'], df['y'], 'r.', alpha=0.5, label='Racing Line')  # Original racing line
plt.plot(x_fitted, y_outer_fitted, 'b-', label='Fitted Outer Bound')
plt.plot(x_fitted, y_inner_fitted, 'g-', label='Fitted Inner Bound')
plt.axis('equal')
plt.legend()
plt.title('Refined Approximated Track Bounds with Spline Fitting')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.show()