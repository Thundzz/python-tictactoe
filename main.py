from gui import CursesInterface
from input import Input
from game import Game
from menu import MenuScreen
import curses
import time

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

    while not game.finished:
        events = inpt.poll_events()
        gui.clear()
        game.update(events)
        render_game(gui, game)
        time.sleep(0.1)

    while True:
        events = inpt.poll_events()
        if events:
            return
        time.sleep(0.1)


if __name__ == '__main__':
    curses.wrapper(main)