# -*- coding: utf-8 -*-
from ..utils import collapse_path
from ..core import get_binary_version, read_project_dir_file


class Line():

    MARKER = '●'
    RIGHT_MARGIN = 2

    def __init__(self, text=None, color=None, pad=0):
        self._text = text
        self.color = color
        self.pad = pad

    @property
    def text(self):
        return ' ' * self.pad + self._text

    def render(self, screen, x, y):
        max_y, max_x = screen.getmaxyx()
        max_width = max_x - Line.RIGHT_MARGIN
        color_pair = 0 if not self.color else self.color.as_pair
        screen.addnstr(y, x, self.text, max_width, color_pair)


class EnvLine(Line):

    def __init__(self, env=None, **kwargs):
        self.env = env
        self.selected = kwargs.pop('selected')
        self.expanded = kwargs.pop('expanded')
        super().__init__(env.envname, **kwargs)

    @property
    def text(self):
        prefix = self.MARKER if self.selected else ' ' * len(self.MARKER)
        project_dir = read_project_dir_file(self.env.envpath)
        has_project_dir = bool(project_dir)
        if not has_project_dir:
            project_dir = '-- Not Set --'

        if self.expanded == 0:
            text = self.env.envname
            text = text if not has_project_dir else text + ' *'
        if self.expanded == 1:
            binpath = get_binary_version(self.env.envpath)
            text = '{} ({})'.format(self.env.envname, binpath)
        if self.expanded == 2:
            text = collapse_path(self.env.envpath)
        if self.expanded == 3:
            text = project_dir

        return '{prefix} {text}'.format(prefix=prefix, text=text)
