from gui import CursesInterface
from input import Input
from game import Game
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

def main(stdscr):
    finished = False

    game = Game()
    gui = CursesInterface(stdscr)
    inpt = Input(stdscr, 0)

    gui.initialize()
    inpt.initialize()

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