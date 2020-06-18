import matplotlib.pyplot as plot
import numpy as np
import collections
from enum import Enum

Data_With_Labels = collections.namedtuple('Data_With_Labels', ['x', 'y', 'labels'])
Text_Attributes = collections.namedtuple(
    'Text_Attributes',
    ['size', 'weight', 'ha', 'va'],
    defaults=[Text_Size.MEDIUM, Text_Weight.NORMAL, Text_Align.CENTER, Text_Align.CENTER]
)


class Figure_Container:
    def __init__(self, title, title_attrs=default_title_attrs, dims=(1, 1)):
        self.__fig, axes, self.__dims = plot.subplots(nrows=dims[0], ncols=dims[1]), dims
        self.__fig.suptitle(title, fontweight=title_attrs.weight, fontsize=title_attrs.size,
            ha=title_attrs.ha, va=title_attrs.va)
        self.__curr_subplot = self.__axes[0][0]
        self.__flattened_axis_list = [item for row in axes for item in row]


    def add_scatterplot(self, increment_subplot=True):
        pass
    def add_function(self, increment_subplot=True):
        pass
    # What other methods could I define here:
    # 'setters'--redundant, should be in the constructor

default_title_attrs = Text_Attributes(Text_Size.LARGE, Text_Weight.BOLD, Text_Align.CENTER, Text_Align.CENTER)

def initialize_new_figure(title, title_attrs=default_title_attrs, dims=(1,1)):
    fig, axes = plot.subplots(nrows=dims[0], ncols=dims[1])
    fig.suptitle(title, fontweight=title_attrs.weight, fontsize=title_attrs.size,
        ha=title_attrs.ha, va=title_attrs.va)
    return fig, axes

# def add_subplot_to_figure(fig):
#     pass

def initialize_new_subplot(title, title_attrs=default_title_attrs):
    pass

def add_comments_to_subplot(sp):
    pass

def add_twin_to_subplot(sp):
    pass

def create_subplot(figure):
    pass

def show_all_figures(tight_layout=True):
    pass

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

class Colors(Enum):
    RED: 'tab:red'
    BLUE: 'tab:blue'

class Text_Weight(Enum):
    NORMAL: 'normal'
    BOLD: 'bold'
    ULTRALIGHT: 'ultralight'
    LIGHT: 'light'
    REGULAR: 'regular'
    BOOK: 'book'
    MEDIUM: 'medium'
    ROMAN: 'roman'
    SEMIBOLD: 'semibold'
    DEMIBOLD: 'demibold'
    DEMI: 'demi'
    HEAVY: 'heavy'
    EXTRA_BOLD: 'extra bold'
    BLACK: 'black'

class Text_Size(Enum):
    XX_SMALL: 'xx-small'
    X_SMALL: 'x-small'
    SMALL: 'small'
    MEDIUM: 'medium'
    LARGE: 'large'
    X_LARGE: 'x-large'
    XX_LARGE: 'xx-large'

class Text_Align(Enum):
    CENTER: 'center'
    LEFT: 'left'
    RIGHT: 'right'
    TOP: 'top'
    BOTTOM: 'bottom'
    BASELINE: 'baseline'
