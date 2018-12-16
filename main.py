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


def main():
    finished = False
    currentPlayer = 1
    game = Game()

    game.print_grid()
    while not finished:
        X, Y = get_player_input(currentPlayer)
        hasPlayed = game.play(currentPlayer, X, Y)

        game.print_grid()
        print()

        if(game.has_won(currentPlayer)):
            print("Game is finished. Player %d won !" % currentPlayer)
            return 0

        if(game.is_full()):
            print("Game is finished. Seems like it's a draw !")
            return 0

        if hasPlayed:
            currentPlayer = next_player(currentPlayer)
        else: 
            print("That was an invalid move buddy :)")





if __name__ == '__main__':
    main()