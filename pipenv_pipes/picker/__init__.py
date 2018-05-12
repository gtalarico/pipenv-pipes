# -*-coding:utf-8-*-

"""
Modified from https://github.com/wong2/pick/
Pick - create curses based interactive selection list in the terminal
LICENSE MIT
"""

import re
import sys
import curses
import json
from itertools import cycle

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
    KEYS_RIGHT,
    KEYS_LEFT,
)


__all__ = ['Picker']

OPTION_COLOR = 'WHITE'
SELECTED_OPTION = 'YELLOW'
TITLE_COLOR = 'BLUE'
IS_TESTING = 'pytest' in sys.modules


class Picker(object):

    def __init__(self, environments, query='', debug_mode=False):

        if not environments:
            raise ValueError('invalid environments value')

        self._environments = environments
        self.query = query
        self.index = 0
        self.debug_mode = debug_mode

        self.CYCLES = range(4)
        self.expand_next()

    def config_curses(self):
        curses.use_default_colors()  # use the default colors of the terminal
        curses.curs_set(0)           # hide the cursor
        self.colors = get_colors()   # initialize temrinal colors

    def _start(self, screen):
        self.screen = screen
        self.config_curses()
        return self.run_loop()

    def start(self):
        if IS_TESTING:
            data = json.dumps({
                'query': self.query,
                'envs': len(self.environments),
                })
            raise SystemExit(data)
        return curses.wrapper(self._start)

    def move_up(self, pos=1):
        self.index -= pos
        if self.index < 0:
            self.index = len(self.environments) - 1
        # self.clear_query()

    def move_down(self, pos=1):
        self.index += pos
        if self.index >= len(self.environments):
            self.index = 0
        # self.clear_query()

    def move_top(self):
        self.index = 0
        # self.clear_query()

    def move_bottom(self):
        self.index = len(self.environments) - 1
        # self.clear_query()

    def clear_query(self):
        self.query = ''

    def expand_next(self):
        if not hasattr(self, '_cycle'):
            self._cycle = cycle(self.CYCLES)
        self.expanded = next(self._cycle)

    def expand_prev(self):
        for _ in self.CYCLES[:-1]:
            self.expand_next()

    def get_selected(self):
        return self.environments[self.index]

    @property
    def environments(self):
        if self.query:
            return [e for e in self._environments
                    if self.query in e.envname.lower()]
        else:
            return self._environments

    def get_option_lines(self):
        envs = self.environments
        lines = []
        for index, environment in enumerate(envs):
            is_selected = index == self.index
            if is_selected:
                color = self.colors[SELECTED_OPTION]
            else:
                color = self.colors[OPTION_COLOR]
            line = EnvLine(
                env=environment,
                color=color,
                selected=is_selected,
                expanded=self.expanded)
            lines.append(line)
        return lines

    def get_title_lines(self):
        color = self.colors[TITLE_COLOR]
        title = 'Pipenv Environments'
        title_line = Line(title, color=color, pad=2)
        bar_line = Line('-' * len(title), color=color, pad=2)
        blank_line = Line('', color=None)
        return [
            blank_line, title_line, bar_line, blank_line]

    def get_lines(self):
        title_lines = self.get_title_lines()
        environment_lines = self.get_option_lines()
        lines = title_lines + environment_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def draw(self, debug_info=None):
        self.screen.clear()

        pad_top = 0
        pad_left = 1
        pad_bottom = 4
        pad_right = 1
        x, y = pad_left, pad_top

        max_y, max_x = self.screen.getmaxyx()
        max_rows = max_y - pad_top - pad_bottom
        max_cols = max_x - pad_right
        if max_y < 5 or max_x < 10:
            self.screen.addnstr(0, 0, 'Help!', max_cols)
            return

        lines, current_line = self.get_lines()
        if current_line <= max_rows:
            visible_lines = lines[:max_rows]
        else:
            delta = current_line - max_rows
            visible_lines = lines[delta:][:max_rows]

        for n, line in enumerate(visible_lines):
            line.render(self.screen, x=x, y=y)
            y += 1

        last_line = len(visible_lines) + 1
        # header = len(self.get_title_lines())
        # height = header - 2
        color = self.colors[SELECTED_OPTION]
        query = Line('$ {}'.format(self.query), color=color)
        query.render(self.screen, x=pad_left, y=last_line)

        if debug_info:
            self.print_debug_info(debug_info)

        self.screen.refresh()

    def print_debug_info(self, debug_info):
        key = debug_info.get('key')
        char = '' if not key else repr(chr(key))
        query = repr(self.query)
        index = self.index
        text = "key: '{}' | char: '{}' | index: '{}' | query: '{}'".format(
            key, char, index, query)
        max_y, max_x = self.screen.getmaxyx()
        pos_y = max_y - 1
        pos_x = 0
        self.screen.addnstr(pos_y, pos_x, text, max_y, 0)

    def run_loop(self):
        debug_info = None
        while True:
            self.draw(debug_info=debug_info)
            key = self.screen.getch()

            try:
                key_string = chr(key)
            except ValueError:
                continue

            if self.debug_mode and key > 0:
                # when stretching windows, key = -1
                debug_info = {'key': key}

            if key in KEYS_ESCAPE:
                sys.exit(0)

            if key in KEYS_ENTER:
                if not self.environments:
                    continue
                return self.get_selected()

            if re.search(r'[A-Za-z0-9\s\-_]', key_string):
                self.query += key_string
                self.expanded = 0
                for n, environment in enumerate(self.environments):
                    if environment.envname.startswith(self.query):
                        self.index = n
                        break

            elif key == curses.KEY_PPAGE:
                self.move_up(5)

            elif key == curses.KEY_NPAGE:
                self.move_down(5)

            elif key in KEYS_UP:
                self.move_up(1)

            elif key in KEYS_DOWN:
                self.move_down(1)

            elif key in KEYS_HOME:
                self.move_top()

            elif key in KEYS_END:
                self.move_bottom()

            elif key in KEYS_CLEAR:
                self.clear_query()

            elif key in KEYS_RIGHT:
                self.expand_next()

            elif key in KEYS_LEFT:
                self.expand_prev()

            elif key in KEYS_BACKSPACE:
                self.query = self.query[:-1]
