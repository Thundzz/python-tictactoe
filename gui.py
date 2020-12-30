import curses
from curses import textpad
import time
import random
from itertools import product

def get_vline(x, ylim1, ylim2):
    return [(x, i) for i in range(ylim1, ylim2)]

def get_hline(x, ylim1, ylim2):
    return [(i, x) for i in range(ylim1, ylim2)]

def get_box(x_coord, x_coord2, y_coord, y_coord2):
    pixels = []
    for x in range(x_coord, x_coord2):
        for y in range(y_coord, y_coord2):
            pixels.append((x, y))
    return pixels

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
    else:
        return [
            "X     x",
            " X   X ",
            "  X X  ",
            "   X   ",
            "  X X  ",
            " X   X ",
            "X     x"
        ]
def main(stdscr):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    margin = 3
    boxes = [
        get_box(1, 11, 1, 11)
    ]

    x1 = 0
    y1 = 0
    x2 = 33
    y2 = 33
    
    lines = [
        get_vline(12, 1, 34),
        get_vline(23, 1, 34),
        get_hline(12, 1, 34),
        get_hline(23, 1, 34)
    ]

    while True:
        stdscr.clear()
        for line in lines:
            for x, y in line:
                stdscr.addstr(y, x, "#")
        
        box = [[y1, x1], [y2, x2]]
        o_symbol = get_sprite("o")
        x_symbol = get_sprite("x")

        positions = product([3, 14, 25], repeat=2)
        for xo, yo in positions:
            symbol = random.choice([o_symbol, x_symbol])
            for idx, line in enumerate(symbol):
                stdscr.addstr(yo+idx, xo, line)
        # print(box)
        # time.sleep(2)
        # for box in boxes:
        #     for x, y in box:
        #         stdscr.addstr(y, x, "*")

        stdscr.refresh()
        time.sleep(0.05)
    # stdscr.getch()
    # for i in range(10):
        # time.sleep(1)

if __name__ == '__main__':
    curses.wrapper(main)


