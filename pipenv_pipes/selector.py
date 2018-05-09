# coding=utf-8

# http://asciimatics.readthedocs.io/en/latest/io.html#attributes

from asciimatics.screen import Screen
from time import sleep


COLOUR_BLACK = 0
COLOUR_RED = 1
COLOUR_GREEN = 2
COLOUR_YELLOW = 3
COLOUR_BLUE = 4
COLOUR_MAGENTA = 5
COLOUR_CYAN = 6
COLOUR_WHITE = 7


def window(screen):
    screen.print_at('Environments', 0, 0, COLOUR_RED)
    screen.print_at('1: Project 1', 3, 2, COLOUR_BLUE)
    screen.print_at('2: Project 2', 3, 3, COLOUR_BLUE)
    screen.print_at('> ', 0, 3, COLOUR_YELLOW)
    screen.print_at('Query: ', 0, 5, COLOUR_CYAN)

    screen.refresh()
    sleep(5)


if __name__ == '__main__':
    Screen.wrapper(window)
