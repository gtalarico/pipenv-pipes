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
        picker = Picker(envs)
        assert picker.get_selected() == envs[0]
        picker.move_down()
        assert picker.get_selected() == envs[1]
        picker.move_down()
        assert picker.get_selected() == envs[2]
        picker.move_up()
        assert picker.get_selected() == envs[1]
        picker.move_up()
        picker.move_up()
        assert picker.get_selected() == envs[-1]

    def test_query_filter(self, environments):
        picker = Picker(environments, query=environments[2].envname)
        assert len(picker.environments) == 1
        assert picker.get_selected() == environments[2]
        picker.move_up()
        assert picker.get_selected() == environments[2]

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
        assert picker.expanded == 3
        picker.expand_next()
        assert picker.expanded == 0
        picker.expand_next()
        assert picker.expanded == 1

    def test_expand_pre(self, picker):
        assert picker.expanded == 0
        picker.expand_prev()
        assert picker.expanded == 3
