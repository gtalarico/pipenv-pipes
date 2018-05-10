import curses
import curses.ascii

KEYS_UP = (
    curses.KEY_UP,
)

KEYS_DOWN = (
    curses.KEY_DOWN,
)

KEYS_SPACE = (
    32,                  # Space
)

KEYS_ENTER = (
    curses.KEY_ENTER,
    curses.KEY_RIGHT,
    ord('\n'),             # MacOs Enter
    ord('\r'),
)

KEYS_BACKSPACE = (
    curses.ascii.DEL,      # MacOs Backpace
)

KEYS_CLEAR = (
    curses.KEY_DC,         # MacOs Delete
    curses.KEY_BACKSPACE,  # MacOs fn + del
)

KEYS_ESCAPE = (
    21,                    # MacOs Escape
    5
)

KEYS_HOME = (
    curses.KEY_HOME,
)

KEYS_END = (
    curses.KEY_END,
)
