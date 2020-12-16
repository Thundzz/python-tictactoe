import curses
from curses import textpad
import time
import random

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
        get_vline(11, 1, 34),
        get_vline(22, 1, 34),
        get_hline(11, 1, 34),
        get_hline(22, 1, 34)
    ]

    while True:
        stdscr.clear()
        
        for line in lines:
            for x, y in line:
                stdscr.addstr(y, x, "X")
        
        box = [[y1, x1], [y2, x2]]

        # print(box)
        # time.sleep(2)
        for box in boxes:
            for x, y in box:
                stdscr.addstr(y, x, "*")

        stdscr.refresh()
        time.sleep(5)
    # stdscr.getch()
    # for i in range(10):
        # time.sleep(1)

if __name__ == '__main__':
    curses.wrapper(main)


