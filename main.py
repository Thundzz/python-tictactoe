from gui import CursesInterface
from input import Input
import curses
import time

class Game():
    def __init__(self):
        self.grid = [[0 for i in range(3)] for j in range(3)]


    def print_grid(self):
        for line in self.grid:
            for cell in line:
                print(self.get_repr(cell), end=' ')
            print()
            

    def has_won(self, player):
        for config in self.to_test():
            if all(self.grid[x][y] == player for (x, y) in config):
                return True
        return False

    def is_full(self):
        return all(all(cell != 0 for cell in line) for line in self.grid)

    def play(self, player, X, Y):
        
        if  0 <= X <= 2 and 0 <= Y <= 2:
            currentValue = self.grid[X][Y] 
            if currentValue  == 0:
                self.grid[X][Y] = player
                return True
            return False
        return False

    def get_positions(self):
        return {   (i, j) : self.grid[i][j]
            for i in range(3) 
            for j in range(3) 
            if self.grid[i][j] != 0
        }.items()

    @staticmethod
    def get_repr(player):
        if player == 0:
            return "."
        if player == 1:
            return "X"
        else:
            return "O"
    @staticmethod
    def to_test():
        return [
             [(0,0), (0,1), (0,2)],
             [(1,0), (1,1), (1,2)],
             [(1,0), (1,1), (1,2)],

             [(0,0), (1,0), (2,0)],
             [(0,1), (1,1), (2,1)],
             [(0,1), (1,1), (2,1)],

             [(0,0), (1,1), (2,2)],
             [(2,0), (1,1), (0,2)]
        ]


def get_player_input(player):
    got_input = False
    while not got_input:
        try:
            s = input("Player %d : please enter coordinates.\n" % player)
            s = s.strip()
            splitted = s.split()

            X, Y = splitted
            
            return (int(X), int(Y))
        except Exception as e:
            print("Could not understand your input, please try again.")
            print(e)

def next_player(player):
    if(player == 1):
        return 2
    elif (player == 2):
        return 1

def update_cursor_position(events, xc, yc):
    for event in events:
        if event == curses.KEY_UP:
            yc = max(yc -1, 0)
        if event == curses.KEY_DOWN:
            yc = min(yc + 1, 2)
        if event == curses.KEY_RIGHT:
            xc = min(xc + 1, 2)
        if event == curses.KEY_LEFT:
            xc = min(yc + 1, 0)

    return xc, yc

def main(stdscr):
    curses.curs_set(0)
    finished = False
    currentPlayer = 1
    game = Game()
    gui = CursesInterface(stdscr)
    inpt = Input(stdscr, 0)

    gui.initialize()
    inpt.initialize()

    events = []
    messages = []
    xc, yc = 0, 0
    while not finished:
        hasPlayed = False

        gui.clear()
        events = inpt.poll_events()

        # messages = list(map(chr, events)) + messages

        xc, yc = update_cursor_position(events, xc, yc)
        if 10 in events:
            hasPlayed = game.play(currentPlayer, xc, yc)
            messages.insert(0, f"Player {currentPlayer} played at ({xc}, {yc})")

        # game.print_grid()

        if(game.has_won(currentPlayer)):
            win_message = "Game is finished. Player %d won !" % currentPlayer
            messages.insert(0, win_message)
            win_message = "Press any key to leave."
            messages.insert(0, win_message)
            finished = True
        elif(game.is_full()):
            draw_message = "Game is finished. Seems like it's a draw !"
            messages.insert(0, draw_message)
            win_message = "Press any key to leave."
            messages.insert(0, win_message)
            finished = True

        if hasPlayed:
            currentPlayer = next_player(currentPlayer)
        # else: 
        #     print("That was an invalid move buddy :)")


        gui.draw_symbol("cursor", xc, yc)
        gui.draw_grid()

        for (x, y), c in game.get_positions():
            symbol = "x" if c == 1 else "o"
            gui.draw_symbol(symbol, x, y)

        gui.display_messages(messages)
        events = inpt.poll_events()
        gui.refresh()
        time.sleep(0.1)

    while True:
        events = inpt.poll_events()
        if events:
            return
        time.sleep(0.1)


if __name__ == '__main__':
    curses.wrapper(main)