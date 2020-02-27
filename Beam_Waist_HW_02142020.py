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

###########################################
### Ring cavity analysis and plot functions
###########################################

def main(wavelength, R, L, side, step):
    epsilon = 0.1       # Graphing right at the stability edge results in errorbarf, so we edge a little bit away from it
    xmin, xmax = R + epsilon, R*(L + 2*side)/(L + 2*side - R) - epsilon     # Stability edges for upper cavity length
    xrange = np.arange(xmin, xmax, step)
    small_waist_data, large_waist_data = get_graph_data(xrange, R, L, side, wavelength)
    xlabel, ylabel_base = 'Curved mirror separation (cm)', 'waist ($\mu$m)'
    comments = ['$R_1 = R_2 = 7.5$ cm', '$d_1 = '+str(L)+'$ cm', '$d_2 = '+str(side)+'$ cm', '$\lambda ='+str(wavelength*(10**7))+'$ nm']
        # These will be placed in the middle of the plot
    make_plot('Ring Cavity Beam Waists vs. Curved Mirror Separation',
        (xrange, xlabel), ([y*1e4 for y in small_waist_data], 'Small '+ylabel_base),
        ([y*1e4 for y in large_waist_data], 'Large '+ylabel_base), comments)
        # Factors of 10000 included to convert from cm --> um

def get_graph_data(xvals, R, bottom, side, wavelength):
    waist_tuples = [get_ring_cavity_waists(R, top, bottom, side, wavelength) for top in xvals]
    return ([small for small, large in waist_tuples], [large for small, large in waist_tuples])

def make_plot(title, xaxis, first, second, comments):
    # Destructure tuples
    xvals, xlabel = xaxis
    data1, label1 = first
    data2, label2 = second

    fig, ax1 = plot.subplots()
    ax1.set_xlabel(xlabel)

    def setup_axis(axis, label, data, color, linestyle, legendpos):
        axis.set_ylabel(label)
        axis.plot(xvals, data, color=color, label=label, linestyle=linestyle)
        axis.tick_params(axis='y', labelcolor=color)
        axis.legend(loc=legendpos)

    setup_axis(ax1, label1, data1, 'tab:red', '-', 'upper left')
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    setup_axis(ax2, label2, data2, 'tab:blue', '--', 'upper right')

    plot.title(title, fontweight='bold', fontsize=14)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax1.text(0.5*(xvals[0] + xvals[-1]), 0.5*(max(data1) + min(data1)), '\n'.join(comments), horizontalalignment='center')
        # Add specified comments to center of plot
    plot.show()

def get_ring_cavity_waists(R, top, bottom, side, wavelength):
    M = get_mirror_matrix(R).dot(get_propagation_matrix(2*side + bottom)).dot(get_mirror_matrix(R)).dot(get_propagation_matrix(top))
    A, B, C, D = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
    disc = (A - D)**2 + 4*B*C       # Discriminant--should be negative
    if disc >= 0:
        print('q parameter has no imaginary part: discriminant = ' + str(disc))
        print('Failed parameters: (R, top, bottom, side, wavelength) = ('
            + str(R) + ', ' + str(top) + ', ' + str(bottom) + ', ' + str(side) + ', ' + str(wavelength) + ')')
        raise ValueError
    else:
        qinv = (D - A)/(2*B) - abs((1/(2*B))*math.sqrt(-disc))*(1j)
            # Using the sqrt function directly on a negative number causes problems
            # Also, we know that the imaginary part should be negative (hence the 'abs' call)
        q_upper = qinv**(-1)
            # q parameter at the reference plane (upper left-hand mirror)
        small_waist = extract_waist(q_upper, wavelength, 1)
        q_lower = propagate_q_param(get_mirror_matrix(-R), q_upper)
            # q parameter in the lower cavity (i.e., between the flat mirrors)
        large_waist = extract_waist(q_lower, wavelength, 1)
        return (small_waist, large_waist)

main(wavelength=1.0e-4, R=7.5, L=30, side=15, step=0.01)
