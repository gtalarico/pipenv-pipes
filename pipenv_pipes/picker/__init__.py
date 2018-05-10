#-*-coding:utf-8-*-

"""
Modified from https://github.com/wong2/pick/
Pick - create curses based interactive selection list in the terminal
LICENSE MIT
"""

import sys
import curses
import string

from .colors import get_colors
from .elements import Line
from .keys import (
    KEYS_UP,
    KEYS_DOWN,
    KEYS_ENTER,
    KEYS_CLEAR,
    KEYS_ESCAPE,
    KEYS_HOME,
    KEYS_END,
)


__all__ = ['Picker']


class Picker(object):

    def __init__(self, options,):

        if not options:
            raise ValueError('Invalid Options')

        self.options = options
        self.query = []
        self.index = 0

    def config_curses(self):
        # use the default colors of the terminal
        curses.use_default_colors()
        # hide the cursor
        curses.curs_set(0)
        # setup colors
        self.colors = get_colors()

    def _start(self, screen):
        self.screen = screen
        self.config_curses()
        return self.run_loop()

    def start(self):
        return curses.wrapper(self._start)

    def move_up(self, positions=1):
        self.index -= positions
        if self.index < 0:
            self.index = len(self.options) - 1

    def move_down(self, positions=1):
        self.index += positions
        if self.index >= len(self.options):
            self.index = 0

    def get_selected(self):
        return self.options[self.index], self.index

    def get_option_lines(self):
        lines = []
        for index, option in enumerate(self.options):

            is_selected = index == self.index

            if is_selected:
                color = self.colors['YELLOW']
            else:
                color = self.colors['WHITE']

            line = Line(text=option, color=color, selected=is_selected)
            lines.append(line)

        return lines

    def get_lines(self):
        title_color = self.colors['GREEN']
        title_lines = [
            Line('===================', color=title_color),
            Line('Pipenv Environments', color=title_color),
            Line('===================', color=title_color),
            Line('\n', color=title_color),
        ]
        # exit_line = [Line('Exit', color=self.colors['BLUE'])]

        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def draw(self, debug_info=None):
        """draw the curses ui on the screen, handle scroll if needed"""
        self.screen.clear()

        x, y = 1, 1  # start point
        max_y, max_x = self.screen.getmaxyx()
        max_rows = max_y - y  # the max rows we can draw

        lines, current_line = self.get_lines()

        # calculate how many lines we should scroll, relative to the top
        scroll_top = getattr(self, 'scroll_top', 0)
        if current_line <= scroll_top:
            scroll_top = 0
        elif current_line - scroll_top > max_rows:
            scroll_top = current_line - max_rows
        self.scroll_top = scroll_top

        bottom_scroll = scroll_top + max_rows
        lines_to_draw = lines[scroll_top: bottom_scroll]

        for n, line in enumerate(lines_to_draw):
            line.render(self.screen, x=x, y=y)
            y += 1

        # THESE BREAK SCROLLING:
        #   # Adde space before Exit
        #   # if n == len(lines_to_draw) - 2:
        #       # y += 1
        # query = '$ {}'.format(''.join(self.query))
        # self.screen.addnstr(y + 2, x + 2, query, max_x-2, curses.color_pair(2))

        if debug_info:
            self.add_debug_info(debug_info)
        self.screen.refresh()

    def add_debug_info(self, debug_info):
        self.screen.addnstr(60, 1, debug_info, 30)

    def run_loop(self):
        debug_info = None

        while True:
            self.draw(debug_info=debug_info)
            key = self.screen.getch()
            # Uncomment to disable debug. add cli > kwargs
            debug_info = '{} | {}'.format(str(key), chr(key))

            if key in KEYS_ESCAPE:
                sys.exit(0)

            elif key == curses.KEY_PPAGE:
                self.move_up(5)

            elif key == curses.KEY_NPAGE:
                self.move_down(5)

            elif key in KEYS_UP:
                self.query = []
                self.move_up(1)

            elif key in KEYS_DOWN:
                self.query = []
                self.move_down(1)

            elif key in KEYS_ENTER:
                return self.get_selected()

            elif key in KEYS_HOME:
                self.query = []
                self.index = 0

            elif key in KEYS_END:
                self.query = []
                self.index = len(self.options) - 2

            elif key in KEYS_CLEAR:
                self.query = []

            else:
                # Only Query Alphanim ascii characters
                if 32 <= key >= 126:
                    continue
                self.query.append(chr(key))
                for n, option in enumerate(self.options):
                    if option.startswith(''.join(self.query)):
                        self.index = n

