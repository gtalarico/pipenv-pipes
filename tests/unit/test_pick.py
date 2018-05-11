#-*-coding:utf-8-*-

"""
Modified from https://github.com/wong2/pick/
Pick - create curses based interactive selection list in the terminal
LICENSE MIT
"""

import pytest
from collections import defaultdict

from pipenv_pipes.picker import Picker


class TestPick():

    @pytest.fixture
    def picker(self, environments):
        # Colors cannot be initialized outside of application
        # so let's replace color objects with a mock dict.
        picker = Picker(environments)
        picker.colors = defaultdict(list)
        return picker

    def test_move_up_down(self, picker, environments):
        envs = environments
        first = envs[0]
        second = envs[1]
        third = envs[2]
        last = envs[-1]
        picker = Picker(envs)
        assert picker.get_selected() == (first, 0)
        picker.move_down()
        assert picker.get_selected() == (second, 1)
        picker.move_down()
        assert picker.get_selected() == (third, 2)
        picker.move_up()
        assert picker.get_selected() == (second, 1)
        picker.move_up()
        picker.move_up()
        assert picker.get_selected() == (last, len(envs) - 1)

    def test_get_lines(self, picker, environments):
        rv = picker.get_option_lines()
        assert len(rv) == len(environments)
        assert hasattr(rv[0], 'render')
        assert picker.get_title_lines()

    def test_get_current_line(self, picker):
        title = picker.get_title_lines()
        lines, current = picker.get_lines()
        assert current == len(title) + 1

    def test_expand(self, picker):
        assert picker.expanded == 0
        picker.expand_next()
        assert picker.expanded == 1
        picker.expand_next()
        assert picker.expanded == 2
        picker.expand_next()
        assert picker.expanded == 0

