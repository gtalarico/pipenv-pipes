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


class Colors():

    CONSTANTS = OrderedDict(
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

    def __init__(self):
        self._colors = {}

    def initialize(self):
        """ This can only be executed after curses.wrapper() """
        curses.use_default_colors()  # use the default colors of the terminal
        for name, integer in Colors.CONSTANTS.items():
            color = Color(index=integer, fg=integer, bg=Color.TRANSPARENT)
            self._colors[name] = color

    def __getitem__(self, key):
        if self._colors:
            return self._colors[key]
        raise RuntimeError('Colors is not initialized')


colors = Colors()
