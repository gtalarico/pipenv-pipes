

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
        super().__init__(env.envname, **kwargs)

    @property
    def text(self):
        envname = self.env.envname
        if self.selected:
            return '{} {}'.format(self.MARKER, envname)
        else:
            space = ' ' * len(self.MARKER)
            return '{} {}'.format(space, envname)
