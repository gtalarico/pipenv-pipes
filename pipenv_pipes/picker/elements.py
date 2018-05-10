

MARGIN = 2


class Line():

    MARKER = '●'

    def __init__(self, text, color, selected=False):
        """
        text (str): text to be shown
        color (color): picker.Color object
        """

        self._text = text
        self.color = color
        self.selected = selected

    @property
    def text(self):
        if self.selected:
            return '{} {}'.format(self.MARKER, self._text)
        else:
            space = ' ' * len(self.MARKER)
            return '{} {}'.format(space, self._text)

    def render(self, screen, x, y):
        max_y, max_x = screen.getmaxyx()
        max_width = max_x - MARGIN
        screen.addnstr(y, x, self.text, max_width, self.color.as_pair)
