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
        self.default_cp = curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.highlighted_cp = curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.color_pairs = { "default": 1, "highlighted" : 2 }

    def initialize(self):
        curses.curs_set(0)
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

    def display_menu(self, title, subtitle, entries, selected_index):
        _, sw = self.stdscr.getmaxyx()
        self.stdscr.addstr(5, sw//2 - len(title) // 2, title)
        subtitle_chunks = subtitle.split("\n")
        for idx, chunk in enumerate(subtitle_chunks):
            self.stdscr.addstr(8 + idx, sw//2 - len(chunk) // 2, chunk)

        for idx, entry in enumerate(entries):
            color_pair_id = self.color_pairs["highlighted"] if idx == selected_index else self.color_pairs["default"]
            cp = curses.color_pair(color_pair_id)
            self.stdscr.addstr(idx + 15, 12, entry, cp)

    def display_server_ip(self, ip):
        self.stdscr.addstr(16, 45, "Server IP: " + ip)
        # self.stdscr.addstr(12, 40, "Server Port: " + port)

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

