import unittest

import main

class TestStringMethods(unittest.TestCase):


    def test_noone_should_have_won(self):
        game = main.Game()

        game.grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        self.assertFalse(game.has_won(1))
        self.assertFalse(game.has_won(2))

    def test_player1_should_have_won(self):
        game = main.Game()

        game.grid = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]

        self.assertTrue(game.has_won(1))
        self.assertFalse(game.has_won(2))

    
    def test_player_1_should_nothave_won(self):
        game = main.Game()

        game.grid = [
            [2, 0, 0],
            [0, 2, 0],
            [0, 0, 2]
        ]
        self.assertTrue(game.has_won(2))
        self.assertFalse(game.has_won(1))
    
    def test_should_be_full(self):
        game = main.Game()

        game.grid = [
            [2, 1, 2],
            [2, 1, 1],
            [1, 2, 2]
        ]
        self.assertTrue(game.is_full())
    
    def test_should_not_be_full(self):
        game = main.Game()

        game.grid = [
            [2, 1, 2],
            [2, 0, 1],
            [1, 2, 2]
        ]
        self.assertFalse(game.is_full())

if __name__ == '__main__':
    unittest.main()