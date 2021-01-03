import curses
from curses import textpad
import time
import random
from itertools import product

def get_vline(x, ylim1, ylim2):
    return [(x, i) for i in range(ylim1, ylim2+1)]

def get_hline(x, ylim1, ylim2):
    return [(i, x) for i in range(ylim1, ylim2+1)]

def get_sprite(c):
    if c == "o":
        return [
            "0000000",
            "0     0",
            "0     0",
            "0     0",
            "0     0",
            "0     0",
            "0000000",
        ]
    elif c == "x":
        return [
            "X     x",
            " X   X ",
            "  X X  ",
            "   X   ",
            "  X X  ",
            " X   X ",
            "X     x"
        ]
    elif c == "cursor":
        return [
            r"%%%%%%%%%",
            r"%       %",
            r"%       %",
            r"%       %",
            r"%       %",
            r"%       %",
            r"%       %",
            r"%       %",
            r"%%%%%%%%%",
        ]
    else:
        raise Exception(f"Could not find sprite for symbol {c}")

def draw_grid(stdscr):
    lines = [
        get_vline(0, 0, 30),
        get_vline(10, 0, 30),
        get_vline(20, 0, 30),
        get_vline(30, 0, 30),
        get_hline(0, 0, 30),
        get_hline(10, 0, 30),
        get_hline(20, 0, 30),
        get_hline(30, 0, 30)
    ]
    for line in lines:
        for x, y in line:
            print(x, y)
            stdscr.addstr(y, x, "#")

def draw_symbol(stdscr, c, x, y):
    symbol = get_sprite(c)
    for idx, line in enumerate(symbol):
        stdscr.addstr(y+idx, x, line)

def main(stdscr):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()

    while sh <= 40 or sw <= 40:
        curses.resize_term(100,100)
        stdscr.clear()
        sh, sw = stdscr.getmaxyx()
        stdscr.addstr(0, 0, "Please increase screensize to at least 40x40, current %s %s"% (sh, sw))
        stdscr.refresh()
        time.sleep(0.5)

    while True:
        stdscr.clear()
        
        draw_grid(stdscr)
        # draw_symbol(stdscr, "cursor", 1, 1)

        positions = product([1, 11, 21], repeat=2)
        # for xc, yc in positions:
        xc, yc = random.choice(list(positions))
        draw_symbol(stdscr, "cursor", xc, yc)

        positions = product([2, 12, 22], repeat=2)
        for xo, yo in positions:
            symbol = random.choice(["o", "x"])
            draw_symbol(stdscr, symbol, xo, yo)

        stdscr.refresh()
        time.sleep(0.5)


if __name__ == '__main__':
    curses.wrapper(main)


