# COLORS
import curses
from collections import OrderedDict


class Color():
    """ Curses Color Class """
    TRANSPARENT = -1

    def __init__(self, index, fg, bg):
        self.index = index
        curses.init_pair(index, fg, bg)

    @property
    def as_pair(self):
        return curses.color_pair(self.index)


color_constants = OrderedDict(
    # Index Zero causes exception on windows
    # BLACK=0,
    RED=1,
    GREEN=2,
    YELLOW=3,
    BLUE=4,
    MAGENTA=5,
    CYAN=6,
    WHITE=7,
)


def get_colors():
    """ This can only be executed after curses has initialized """
    colors = {}
    for name, integer in color_constants.items():
        colors[name] = Color(index=integer, fg=integer, bg=Color.TRANSPARENT)
    return colors
