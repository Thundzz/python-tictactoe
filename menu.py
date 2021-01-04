from input import Input
import curses
import time

class MenuScreen:

    def __init__(self):
        self.title = "Tic Tac Toe !!"
        self.entries = [
            "Local two players game",
            "Against AI",
            "Host new remote game",
            "Connect to remote game"
        ]
        self.current_idx = 0
        self.server_ip = []
        self.server_port = []

    def update(self, events):
        accepted_chars = set(range(ord("0"), ord("9")+1)) | set([ord(".")])
        for event in events:
            if event in accepted_chars:
                self.server_ip.append(event)
            elif event == curses.KEY_BACKSPACE:
                self.server_ip.pop()

    def get_server_ip_str(self):
        return "".join(map(chr, self.server_ip))

    def get_server_port_str(self):
        return "".join(map(chr, self.server_port))


def main(stdscreen):
    from gui import CursesInterface

    menu = MenuScreen()
    gui = CursesInterface(stdscreen)
    inpt = Input(stdscreen, 0)

    gui.initialize()
    inpt.initialize()
    idx = 0
    while True:
        gui.clear()
        events = inpt.poll_events()
        menu.update(events)
        gui.display_menu(menu.title, menu.entries, idx)

        gui.display_server_ip(menu.get_server_ip_str(), menu.get_server_port_str())

        idx = (idx + 1) % len(menu.entries)
        gui.refresh()
        time.sleep(0.5)

if __name__ == '__main__':
    curses.wrapper(main)