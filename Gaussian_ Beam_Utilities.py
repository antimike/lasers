import numpy as np
import matplotlib.pyplot as plot
import math

###########################################
### Gaussian optics / ray-tracing functions
###########################################

def get_mirror_matrix(R):
    return np.array([[1, 0], [-2/R, 1]])

def get_propagation_matrix(d):
    return np.array([[1, d], [0, 1]])

def propagate_q_param(matrix, q):
    A, B, C, D = matrix[0, 0], matrix[0, 1], matrix[1, 0], matrix[1, 1]
    return (A*q + B)/(C*q + D)

def extract_waist(qparam, wavelength, n):
    if qparam.imag < 0:         # Some basic error handling
        print("Error encountered in function 'extract_waist':")
        print('q parameter cannot have negative imaginary part.  Im(q) = ' + str(qparam.imag))
        raise ValueError
    else:
        return math.sqrt((wavelength/(n*np.pi))*qparam.imag)

def distance_to_waist(qparam):
    return -qparam.real         # No error handling needed--this can be negative
