from input import Input
import curses
import time

class MenuScreen:

    def __init__(self):
        self.title = "Tic Tac Toe !!"
        self.subtitle = "Use UP and DOWN keys to navigate the menu!\nEnter a server IP using the number keys and the . key !"
        self.entries = [
            "Local two players game",
            "Against AI",
            "Host new remote game",
            "Connect to remote game"
        ]
        self.current_idx = 0
        self.server_ip = []
        self.finished = False
        # self.server_port = []

    def update(self, events):
        accepted_chars = set(range(ord("0"), ord("9")+1)) | set([ord(".")])
        for event in events:
            if event in accepted_chars:
                self.server_ip.append(event)
            elif event in { curses.KEY_BACKSPACE, ord('\b'), 127 }:
                if self.server_ip:
                    self.server_ip.pop()
            elif event == curses.KEY_DOWN:
                self.current_idx = (self.current_idx + 1) % len(self.entries)
            elif event == curses.KEY_UP:
                self.current_idx = (self.current_idx - 1) % len(self.entries)
            elif event == 10:
                self.finished = True

    def get_server_ip_str(self):
        return "".join(map(chr, self.server_ip))

    def get_server_port_str(self):
        return "".join(map(chr, self.server_port))

