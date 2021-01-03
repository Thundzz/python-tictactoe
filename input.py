import curses

class Input:

    def __init__(self, stdscr, timeout):
        self.stdscr = stdscr
        self.timeout = timeout

    def initialize(self):
        self.stdscr.nodelay(1)
        self.stdscr.timeout(self.timeout)

    def poll_events(self):
        keys = []
        for i in range(50):
            key = self.stdscr.getch()
            if key != -1:
                keys.append(key)
        return keys



