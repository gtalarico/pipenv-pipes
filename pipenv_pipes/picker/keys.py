import curses
import curses.ascii

KEYS_UP = (
    curses.KEY_UP,
)

KEYS_DOWN = (
    curses.KEY_DOWN,
)

KEYS_RIGHT = (
    curses.KEY_RIGHT,
)

KEYS_LEFT = (
    curses.KEY_LEFT,
)

KEYS_ENTER = (
    curses.KEY_ENTER,
    ord('\n'),             # MacOs Enter
    ord('\r'),
    # 32,                  # Space
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
