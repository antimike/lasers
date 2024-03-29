import numpy as np
from scipy import optimize
from inspect import signature
import collections

# Convenience struct types:
Data_With_Errors = collections.namedtuple('Data_With_Errors', ['x', 'y', 'ebars'])
Regression_Result = collections.namedtuple('Regression_Result', ['params', 'std_devs'])
Linear_Regression = collections.namedtuple(
    'Linear_Regression', ['slope', 'intercept', 'r_value', 'p_value', 'std_err']
)

def weighted_regression(data_with_errors, functional_form, initial_guess):
    func_sig = signature(functional_form)
    arg_list = [p.name for p in func_sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
    param_names = arg_list[1:]
    seed_vals = [initial_guess.get(name, 0) for name in param_names]
    params, cov_matrix = optimize.curve_fit(
        functional_form,
        data_with_errors.x,
        data_with_errors.y,
        seed_vals,
        sigma=data_with_errors.ebars,
        absolute_sigma=True
    )
    return Regression_Result(
        dict(zip(param_names, params)),
        dict(zip(param_names, np.sqrt(np.diag(cov_matrix))))
    )

def flatten_data_array(xvals, yvals_array, ddof=0):
    return Data_With_Errors(xvals, np.average(yvals_array, axis=0),
        np.std(yvals_array, axis=0, ddof=ddof))
