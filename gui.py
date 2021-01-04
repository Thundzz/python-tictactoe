import curses
from curses import textpad
import time
import random
from itertools import product
from input import Input

class CursesInterface:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curs_pos = list(product(enumerate([1, 11, 21]), repeat=2))
        self.cursors_b2s = { 
            (boardX, boardY) : (screenX, screenY)  
            for (boardX, screenX), (boardY, screenY) in curs_pos
        }

        sprite_pos = list(product(enumerate([2, 12, 22]), repeat=2))
        self.sprite_b2s = { 
            (boardX, boardY) : (screenX, screenY)  
            for (boardX, screenX), (boardY, screenY) in sprite_pos
        }


    def initialize(self):
        sh, sw = self.stdscr.getmaxyx()

        while sh <= 40 or sw <= 40:
            curses.resize_term(100,100)
            self.stdscr.clear()
            sh, sw = self.stdscr.getmaxyx()
            self.stdscr.addstr(0, 0, "Please increase screensize to at least 40x40, current %s %s"% (sh, sw))
            self.stdscr.refresh()
            time.sleep(0.5)

    def clear(self):
        self.stdscr.clear()

    def refresh(self):
        self.stdscr.refresh()

    def display_messages(self, messages):
        x0, y0 = 0, 40
        for idx, message in enumerate(messages):
            self.stdscr.addstr(x0+idx, y0, message)


    def draw_grid(self):
        lines = [
            self.__get_vline(0, 0, 30),
            self.__get_vline(10, 0, 30),
            self.__get_vline(20, 0, 30),
            self.__get_vline(30, 0, 30),
            self.__get_hline(0, 0, 30),
            self.__get_hline(10, 0, 30),
            self.__get_hline(20, 0, 30),
            self.__get_hline(30, 0, 30)
        ]
        for line in lines:
            for x, y in line:
                # print(x, y)
                self.stdscr.addstr(y, x, "#")

    def draw_symbol(self, c, x, y):
        mapping = self.cursors_b2s if c == "cursor" else self.sprite_b2s

        sx, sy = mapping[(x, y)]
        symbol = self.__get_sprite(c)
        for idx, line in enumerate(symbol):
            self.stdscr.addstr(sy+idx, sx, line)

    @staticmethod
    def __get_sprite(c):
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

    @staticmethod
    def __get_vline(x, ylim1, ylim2):
        return [(x, i) for i in range(ylim1, ylim2+1)]

    @staticmethod
    def __get_hline(x, ylim1, ylim2):
        return [(i, x) for i in range(ylim1, ylim2+1)]

def main(stdscr):
    curses.curs_set(0)

    gui = CursesInterface(stdscr)
    inpt = Input(stdscr, 0)

    gui.initialize()
    inpt.initialize()

    xc, yc = 0, 0
    events = []
    symbols = random.sample(9*["o", "x"], 9)
    while True:
        gui.clear()
        gui.draw_grid()

        messages = map(chr, events)

        # gui.display_messages(messages)

        # positions = product(range(3), repeat=2)
        # xc, yc = random.choice(list(positions))

        for event in events:
            if event == curses.KEY_UP:
                yc -= 1
            if event == curses.KEY_DOWN:
                yc += 1
            if event == curses.KEY_RIGHT:
                xc += 1
            if event == curses.KEY_LEFT:
                xc -= 1
        if xc > 2:
            xc = 2
        if xc < 0:
            xc = 0
        if yc > 2:
            yc = 2
        if yc < 0:
            yc = 0

        gui.draw_symbol("cursor", xc, yc)
        positions = product(range(3), repeat=2)

        for idx, (xo, yo) in enumerate(positions):
            symbol = random.choice(["o", "x"])
            gui.draw_symbol(symbols[idx], xo, yo)

        events = inpt.poll_events()
        gui.refresh()
        time.sleep(0.05)

if __name__ == '__main__':
    curses.wrapper(main)


