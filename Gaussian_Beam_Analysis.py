import numpy as np
import scipy.special as special_fns
import Gaussian_Beam_Utilities as util
import Nonlinear_Regression as regress
import Data_Presentation as plotter
import Spreadsheet_Data_Import as importer

filename = '/home/hactar/Documents/Spring 2020/Lasers/Gaussian Beam Lab/Gaussian_Beam_Data_01302020.ods'
sheet_names = ['First_Measurement_19,8cm', 'Second_Measurement_73,1cm', 'Third_Measurement_35,1cm']
sheet_zs = [19.8, 73.1, 35.1] # Lateral distances at which measurements were performed
sheet_results = dict(zip(sheet_names, sheet_zs)) # This will be mutated to hold the regressions later
y_col_labels = ['Power ' + str(i) for i in np.arange(1, 6, 1)] # 5 different measurements per data point
col_labels = ['Micrometer reading', *y_col_labels]

raw_data = importer.get_data_from_workbook(
    filename,
    {sheet_name: col_labels for sheet_name in sheet_names}
)
data = {sheet_name: get_plotdata(sheet_dict) for sheet_name, sheet_dict in raw_data.items()}

def get_plotdata(col_dict):
    xs, ys_array = col_dict[col_labels[0]], [col_dict[label] for label in y_col_labels]
    return regress.flatten_data_array(xs, ys_array)

def expected_fn(x, sigma, vertical_offset, lateral_offset, total_power):
    return vertical_offset - total_power*special_fns.erf((x - lateral_offset)/(np.sqrt(2)*sigma))

seed_vals = {'sigma': 30, 'vertical_offset': 1.5, 'lateral_offset': 1.5, 'total_power': 100}
    # From Desmos

sheet_results = {
    z: regress.weighted_regression(data[name], expected_fn, seed_vals)
    for name, z in sheet_results.items()
}

plotter.initialize_figure(title='Beam Waist Measurements at Different $z$-values',
    xlabel='')
