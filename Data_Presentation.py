import matplotlib.pyplot as plot
import numpy as np
import collections

Data_With_Labels = collections.namedtuple('Data_With_Labels', ['x', 'y', 'labels'])

def initialize_figure(title, xlabel, ylabel, *comments):
    fig, grid = plot.subplots()
    plot.title(title, fontweight='bold', fontsize=14)
    grid.set_xlabel(xlabel)
    grid.set_ylabel(ylabel)
    caption = '\n'.join(comments)
    fig.subplots_adjust(bottom=.8)
    plot.figtext(0.5, 0.01, caption, wrap=True, ha='center', va='top', fontsize=12)
    return fig, grid

def show_figure(figure, grid, legend_pos):
    grid.legend(loc=legend_pos)
    figure.tight_layout()
    plot.show()

def plot_points_with_errorbars(grid, data, marker, color, ebar_color, label, linestyle):
    grid.errorbar(x=data.x, y=data.y, xerr=None, yerr=data.ebars, ecolor=ebar_color,
        color=color, label=label, marker=marker, linestyle=linestyle)
    pass

def plot_function(grid, fn, color, label, linestyle):
    min, max = plot.xlim()
    fn_x = np.linspace(min, max, 100)
    grid.plot(fn_x, fn(fn_x), color=color, label=label, linestyle=linestyle)
    pass

def annotate_points(grid, points, marker, color):
    for x, y, label in zip(points.x, points.y, points.labels):
        plot.annotate(label, (x, y), textcoords='offset points', xytext=(0,10), ha='center')
    pass

def annotate_point(grid, point, marker, color):
    plot.plot(point.x, point.y, color=color, marker=marker)
    plot.annotate(point.labels, (point.x, point.y), textcoords='offset points', xytext=(0,10), ha='center')
    pass

def stringify_point(x, y, *units):
    def unitize_number(num, unit):
        return "{:.2f}".format(num) + ' ' + unit
    unit_list = list(units or ())
    if len(unit_list) < 2:
        unit_list += ['']*(2 - len(unit_list))
    return '(' \
        + unitize_number(x, unit_list[0]) \
        + ',' + unitize_number(y, unit_list[1]) \
        + ')'
    pass