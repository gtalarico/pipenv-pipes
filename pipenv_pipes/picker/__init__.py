#-*-coding:utf-8-*-

"""
Modified from https://github.com/wong2/pick/
Pick - create curses based interactive selection list in the terminal
LICENSE MIT
"""

import re
import sys
import curses
import string

from .colors import get_colors
from .elements import Line, EnvLine
from .keys import (
    KEYS_UP,
    KEYS_DOWN,
    KEYS_ENTER,
    KEYS_CLEAR,
    KEYS_BACKSPACE,
    KEYS_ESCAPE,
    KEYS_HOME,
    KEYS_END,
)


__all__ = ['Picker']


class Picker(object):

    def __init__(self, environments, debug_mode=False):

        if not environments:
            raise ValueError('invalid environments value')

        self.options = environments
        self.query = []
        self.index = 0
        self.debug_mode = debug_mode

    def config_curses(self):
        curses.use_default_colors()  # use the default colors of the terminal
        curses.curs_set(0)           # hide the cursor
        self.colors = get_colors()   # initialize temrinal colors

    def _start(self, screen):
        self.screen = screen
        self.config_curses()
        return self.run_loop()

    def start(self):
        return curses.wrapper(self._start)

    def move_up(self, pos=1):
        self.index -= pos
        if self.index < 0:
            self.index = len(self.options) - 1
        self.clear_query()

    def move_down(self, pos=1):
        self.index += pos
        if self.index >= len(self.options):
            self.index = 0
        self.clear_query()

    def move_top(self):
        self.index = 0
        self.clear_query()

    def move_bottom(self):
        self.index = len(self.options) - 1
        self.clear_query()

    def clear_query(self):
        self.query = []

    def get_selected(self):
        return self.options[self.index], self.index

    def get_option_lines(self):
        lines = []
        for index, option in enumerate(self.options):
            is_selected = index == self.index
            if is_selected:
                color = self.colors['RED']
            else:
                color = self.colors['WHITE']
            line = EnvLine(env=option, color=color, selected=is_selected)
            lines.append(line)
        return lines

    def get_title_lines(self):
        color = self.colors['GREEN']
        title = 'Pipenv Environments'
        title_line = Line(title, color=color, pad=2)
        bar_line = Line('=' * len(title), color=color, pad=2)
        blank_line = Line('', color=None)
        return [bar_line, title_line, bar_line, blank_line]

    def get_lines(self):
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def draw(self, debug_info=None):
        self.screen.clear()

        pad_top = 0
        pad_left = 1
        pad_bottom = 4
        x, y = pad_left, pad_top

        max_y, max_x = self.screen.getmaxyx()
        max_rows = max_y - pad_top - pad_bottom

        lines, current_line = self.get_lines()
        if current_line <= max_rows:
            visible_lines = lines[:max_rows]
        else:
            delta = current_line - max_rows
            visible_lines = lines[delta:][:max_rows]

        for n, line in enumerate(visible_lines):
            line.render(self.screen, x=x, y=y)
            y += 1

        last_line = max_rows + 1
        query = '$ {}'.format(''.join(self.query))
        self.screen.addnstr(last_line, pad_left, query, max_x-2, curses.color_pair(2))

        if debug_info:
            self.print_debug_info(debug_info)

        self.screen.refresh()

    def print_debug_info(self, debug_info):
        max_y, max_x = self.screen.getmaxyx()
        pos_y = max_y - 1
        pos_x = max_x - len(debug_info) - 2
        self.screen.addnstr(pos_y, pos_x, debug_info, 30)

    def run_loop(self):
        debug_info = None

        while True:
            self.draw(debug_info=debug_info)
            key = self.screen.getch()

            if self.debug_mode and key > 0:
                # when stretching windows, key = -1
                debug_info = '{} | {}'.format(str(key), chr(key))

            if key in KEYS_ESCAPE:
                sys.exit(0)

            try:
                key_string = chr(key)
            except ValueError:
                continue

            if re.search(r'[A-Za-z0-9\s\-_]', key_string):
                self.query.append(key_string)
                for n, option in enumerate(self.options):
                    if option.startswith(''.join(self.query)):
                        self.index = n

            if key == curses.KEY_PPAGE:
                self.move_up(5)

            elif key == curses.KEY_NPAGE:
                self.move_down(5)

            elif key in KEYS_UP:
                self.move_up(1)

            elif key in KEYS_DOWN:
                self.move_down(1)

            elif key in KEYS_ENTER:
                return self.get_selected()

            elif key in KEYS_HOME:
                self.move_top()

            elif key in KEYS_END:
                self.move_bottom()

            elif key in KEYS_CLEAR:
                self.clear_query()

            elif key in KEYS_BACKSPACE:
                self.query = self.query[:-1]
