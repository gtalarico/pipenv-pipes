from ..utils import collapse_path

MARGIN = 2


class Line():

    MARKER = '●'

    def __init__(self, text=None, color=None, pad=0):
        self._text = text
        self.color = color
        self.pad = pad

    @property
    def text(self):
        return ' ' * self.pad + self._text

    def render(self, screen, x, y):
        max_y, max_x = screen.getmaxyx()
        max_width = max_x - MARGIN
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
        envname = self.env.envname
        envpath = collapse_path(self.env.envpath)
        expanded_envname = '{0}'.format(envpath)
        prefix = self.MARKER if self.selected else ' ' * len(self.MARKER)
        text = envname if not self.expanded else expanded_envname
        return '{prefix} {text}'.format(prefix=prefix, text=text)
