from ..utils import collapse_path
from ..core import get_binary_version



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

        if self.expanded == 0:
            text = self.env.envname
        if self.expanded == 1:
            text = '{} ({})'.format(
                self.env.envname,
                get_binary_version(self.env.envpath
                ))
        if self.expanded == 2:
            text = collapse_path(self.env.envpath)

        return '{prefix} {text}'.format(prefix=prefix, text=text)
