from gui import CursesInterface
from input import Input
from game import Game
from menu import MenuScreen
from network import Client, Server

import curses
import sys
import time
import random


def render_game(gui, game):
    gui.draw_symbol("cursor", game.xc, game.yc)
    gui.draw_grid()

    for (x, y), c in game.get_positions():
        symbol = "x" if c == 1 else "o"
        gui.draw_symbol(symbol, x, y)

    gui.display_messages(list(game.messages)[:10])
    # gui.refresh()

def render_menu(gui, menu):
    gui.display_menu(menu.title, menu.subtitle, menu.entries, menu.current_idx)
    gui.display_server_ip(menu.get_server_ip_str())



class LocalVsGameWrapper:
    def __init__(self, inpt, game):
        self.inpt = inpt
        self.game = game

    def initialize(self):
        pass

    def update(self):
        l_events = self.inpt.poll_events()
        events = [
            (self.game.currentPlayer, l_event)
            for l_event in l_events
        ]
        self.game.update(events)

    def cleanup(self):
        pass

class LocalAiGameWrapper:
    def __init__(self, inpt, game):
        self.inpt = inpt
        self.game = game
        self.local_p_id = 1
        self.remote_p_id = 2

    def initialize(self):
        pass

    def update(self):
        l_events = self.inpt.poll_events()
        moves = [
            curses.KEY_LEFT,
            curses.KEY_RIGHT,
            curses.KEY_UP,
            curses.KEY_DOWN,
        ]
        enter = 10
        events = [
            (self.local_p_id, l_event)
            for l_event in l_events
        ] + [
            (self.remote_p_id, random.choice(moves)) for _ in range(100)
        ] + [ (self.remote_p_id, enter) ]

        self.game.update(events)

    def cleanup(self):
        pass

class NetworkedGameWrapper:
    def __init__(self, inpt, game, conn, local_p_id, remote_p_id):
        self.conn = conn
        self.inpt = inpt
        self.game = game
        self.local_p_id = local_p_id
        self.remote_p_id = remote_p_id

    def initialize(self):
        self.game.add_message(f"You are player {self.local_p_id} !")
        self.conn.start()

    def update(self):
        l_events = self.inpt.poll_events()
        self.conn.send_messages([str(e) for e in l_events])
        rcvd = self.conn.get_messages()
        r_events = [int(e) for e in rcvd]
        events = [
            (self.local_p_id, l_event)
            for l_event in l_events
        ] + [
            (self.remote_p_id, r_event)
            for r_event in r_events
        ]
        self.game.update(events)

    def cleanup(self):
        self.conn.stop()

def main(stdscr):
    finished = False

    gui = CursesInterface(stdscr)
    inpt = Input(stdscr, 0)

    menu = MenuScreen()
    game = Game()

    gui.initialize()
    inpt.initialize()

    while not menu.finished:
        events = inpt.poll_events()
        gui.clear()
        menu.update(events)
        render_menu(gui, menu)
        gui.refresh()
        time.sleep(0.1)

    if menu.current_idx == 0:
        gamewrapper = LocalVsGameWrapper(inpt, game)
    elif menu.current_idx == 1:
        gamewrapper = LocalAiGameWrapper(inpt, game)
    elif menu.current_idx == 2:
        gamewrapper = NetworkedGameWrapper(inpt, game, Server(), 1, 2)
    else:
        gamewrapper = NetworkedGameWrapper(inpt, game, Client(menu.get_server_ip_str()), 2, 1)

    gamewrapper.initialize()
    while not game.finished:
        gamewrapper.update()
        gui.clear()
        render_game(gui, game)
        time.sleep(0.05)

    gamewrapper.cleanup()

    while True:
        events = inpt.poll_events()
        if events:
            return
        time.sleep(0.1)


if __name__ == '__main__':
    curses.wrapper(main)