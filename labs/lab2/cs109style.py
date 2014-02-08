from __future__ import print_function

from IPython.core.display import HTML
from matplotlib import rcParams

#colorbrewer2 Dark2 qualitative color table
dark2_colors = [(0.10588235294117647, 0.6196078431372549, 0.4666666666666667),
                (0.8509803921568627, 0.37254901960784315, 0.00784313725490196),
                (0.4588235294117647, 0.4392156862745098, 0.7019607843137254),
                (0.9058823529411765, 0.1607843137254902, 0.5411764705882353),
                (0.4, 0.6509803921568628, 0.11764705882352941),
                (0.9019607843137255, 0.6705882352941176, 0.00784313725490196),
                (0.6509803921568628, 0.4627450980392157, 0.11372549019607843),
                (0.4, 0.4, 0.4)]

def customize_mpl():
    """Tweak matplotlib visual style"""
    print("Setting custom matplotlib visual style")

    rcParams['figure.figsize'] = (10, 6)
    rcParams['figure.dpi'] = 150
    rcParams['axes.color_cycle'] = dark2_colors
    rcParams['lines.linewidth'] = 2
    rcParams['axes.grid'] = True
    rcParams['axes.facecolor'] = '#eeeeee'
    rcParams['font.size'] = 14
    rcParams['patch.edgecolor'] = 'none'


def customize_css():
    print("Setting custom CSS for the IPython Notebook")
    styles = open('custom.css', 'r').read()
    return HTML(styles)
