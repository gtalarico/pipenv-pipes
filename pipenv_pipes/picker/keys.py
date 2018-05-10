import curses
import curses.ascii

KEYS_UP = (
    curses.KEY_UP,
)

KEYS_DOWN = (
    curses.KEY_DOWN,
)

KEYS_ENTER = (
    curses.KEY_ENTER,
    curses.KEY_RIGHT,
    ord('\n'),             # MacOs Enter
    ord('\r'),
    # 32,                    # Space
)

KEYS_CLEAR = (
    curses.KEY_DC,         # MacOs Delete
    curses.ascii.DEL,             # MacOs Backpace
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
