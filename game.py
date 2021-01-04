from collections import deque
import curses

class Game():
    def __init__(self):
        self.grid = [[0 for i in range(3)] for j in range(3)]
        self.messages = deque()
        self.currentPlayer = 1
        self.xc = 0
        self.yc = 0
        self.finished = False

    def update(self, events):
        xc, yc = self.update_cursor_position(events, self.xc, self.yc)
        self.xc = xc
        self.yc = yc
        hasPlayed = False
        if 10 in events:
            hasPlayed = self.play(self.currentPlayer, xc, yc)
            self.add_message(f"Player {self.currentPlayer} played at ({xc}, {yc})")

        if(self.has_won(self.currentPlayer)):
            end_message = "Game is finished. Player %d won !" % self.currentPlayer
            self.finished = True

        elif(self.is_full()):
            end_message = "Game is finished. Seems like it's a draw !"
            self.finished = True

        if self.finished:
            self.add_message(end_message)
            self.add_message("Press any key to leave.")

        if hasPlayed:
            self.currentPlayer = self.next_player(self.currentPlayer)

    def has_won(self, player):
        for config in self.position_combinations():
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

    def add_message(self, message):
        self.messages.appendleft(message)

    @staticmethod
    def position_combinations():
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

    @staticmethod
    def next_player(player):
        if(player == 1):
            return 2
        elif (player == 2):
            return 1

    @staticmethod
    def update_cursor_position(events, xc, yc):
        for event in events:
            if event == curses.KEY_UP:
                yc = max(yc - 1, 0)
            if event == curses.KEY_DOWN:
                yc = min(yc + 1, 2)
            if event == curses.KEY_RIGHT:
                xc = min(xc + 1, 2)
            if event == curses.KEY_LEFT:
                xc = max(xc - 1, 0)

        return xc, yc