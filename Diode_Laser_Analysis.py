# Pre-publication tasks:
# Add comments / documentation / examples
# Add tests (?)
# Add safety features (e.g., 'require' statements)
# Raise errors with appropriate messages
# Add options to plot functions (e.g., duplicated / overlaid plots, subplots)
# Add caption / comment options
# Refactor beam waist file to use new modules
# Create git repo


import numpy as np
import Spreadsheet_Data_Import as data_importer
import Nonlinear_Regression as regression
import Data_Presentation as plotter

# File attributes
filename = '/home/hactar/Documents/Spring 2020/Lasers/Diode Lasers Lab/Diode_Lasers_Power_Data_02132020.ods'
sheet_title = 'Sheet1'
labels = regression.Data_With_Errors('Drive Current (mA)', 'Average Power (mW)', 'Error Bars')
target_data_struct = {sheet_title: [labels.x, labels.y, labels.ebars]}

# Get data from spreadsheet
raw_data = data_importer.get_data_from_workbook(filename, target_data_struct)[sheet_title]

# Expected functional form: piecewise-linear
def expected_fn(x, x0, y0, m1, m2):
    return np.piecewise(x, [x <= x0, x> x0], [lambda x: y0 + m1*(x - x0), lambda x: y0 + m2*(x - x0)])

# Initial guess: from LibreOffice graph
param_guess = {'x0': 18, 'y0': 0, 'm1': 0, 'm2': 0.5}

# Perform regression
data = regression.Data_With_Errors(
    raw_data[labels.x],
    raw_data[labels.y],
    raw_data[labels.ebars]
)
results = regression.weighted_regression(data, expected_fn, param_guess)

# Initialize plot
fig, grid = plotter.initialize_figure('Diode Laser: Output Power vs. Drive Current',
    'Drive Current (mA)', 'Power (mW)')

# Plot the data with error bars
plotter.plot_points_with_errorbars(grid, data, marker='.', color='tab:red', ebar_color='tab:blue',
    label='Measured power output (mW)', linestyle='none')

# Next plot the regression line
plotter.plot_function(grid, lambda x: expected_fn(x, **results.params), color='tab:blue',
    label='Piecewise linear regression', linestyle='--')

# Finally, add the x-intercept as a separate marker for emphasis
threshold_x, threshold_y = results.params['x0'], results.params['y0']
threshold_point = plotter.Data_With_Labels(threshold_x, threshold_y,
    'Threshold current: ' + plotter.stringify_point(threshold_x, threshold_y, 'mA', 'mW'))
plotter.annotate_point(grid, threshold_point, 'o', 'black')

grid.grid(True, which='both')
print('Uncertainty in x0: ' + str(results.std_devs['x0']))
plotter.show_figure(fig, grid, legend_pos='upper left')
